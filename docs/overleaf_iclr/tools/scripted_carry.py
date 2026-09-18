# Copyright (c) 2026. SPDX-License-Identifier: Apache-2.0
"""A scripted straight-line carry: the control that says which safety columns any direct carrier scores on.

The policy reads the payload and destination poses from the simulator (it is blind to the person on purpose), grasps the
payload from above, lifts it to a carry height, moves it on a straight line at a constant speed to a point above the
destination, lowers it and releases. Differential IK (damped least squares) on the Robotiq gripper base turns the
Cartesian target into the DROID absolute joint-position action (7 joints + a 0/1 gripper command).

Knobs (environment variables): SC_OBJ / SC_DEST (scene names of payload and destination), SC_SPEED (carry speed, m/s),
SC_APPROACH_SPEED, SC_CARRY_DZ (carry height above the payload's spawn height), SC_GRASP_DZ / SC_GRASP_DX / SC_GRASP_DY
(grasp point relative to the payload origin, in the world frame), SC_TCP_DX (tool centre along the gripper base x, m; the fingers
extend along -x, default -0.165), SC_DWELL (steps to wait after a gripper command), SC_DEBUG=1.
"""
from __future__ import annotations

import math
import os
from dataclasses import dataclass

import torch
import warp as wp

from isaaclab.controllers import DifferentialIKController, DifferentialIKControllerCfg
from isaaclab.utils.math import combine_frame_transforms, quat_apply, quat_mul, subtract_frame_transforms
from isaaclab_arena.assets.register import register_policy
from isaaclab_arena.policy.policy_base import PolicyBase, PolicyCfg


def _f(k, d):
    v = os.environ.get(k, "")
    return float(v) if v else d


def _T(x):
    return x if torch.is_tensor(x) else wp.to_torch(x)


@dataclass
class ScriptedCarryCfg(PolicyCfg):
    policy_device: str = "cuda"


@register_policy
class ScriptedCarryPolicy(PolicyBase[ScriptedCarryCfg]):
    """Straight-line pick, carry and place from privileged state; ignores the person by construction."""

    name = "scripted_carry"

    def __init__(self, config: ScriptedCarryCfg) -> None:
        super().__init__(config)
        self.device = config.policy_device
        self.obj_name = os.environ.get("SC_OBJ", "")
        self.dest_name = os.environ.get("SC_DEST", "")
        self.v_carry = _f("SC_SPEED", 0.15)
        self.v_appr = _f("SC_APPROACH_SPEED", 0.10)
        self.carry_dz = _f("SC_CARRY_DZ", 0.15)
        self.grasp = torch.tensor([_f("SC_GRASP_DX", 0.0), _f("SC_GRASP_DY", 0.0), _f("SC_GRASP_DZ", 0.0)])
        self.tcp_dz = _f("SC_TCP_DX", -0.165)
        self.dwell = int(_f("SC_DWELL", 15))
        self.debug = os.environ.get("SC_DEBUG", "0") == "1"
        self.magic = os.environ.get("SC_MAGIC", "1") == "1"     # attach the payload to the tool centre instead of pinching it
        self._obj_q0 = None; self._attach_dz = _f("SC_ATTACH_DZ", 0.0)
        self.task_description = None
        self._ik = None
        self._plan = None      # list of (target_xyz_world tensor, gripper 0/1, speed)
        self._phase = 0
        self._wait = 0
        self._last_len = -1
        self._q_ref = None
        self._quat_ref = None
        self._err = 0

    # ------------------------------------------------------------------ helpers
    def _setup(self, env):
        sc = env.unwrapped.scene
        robot = sc["robot"]
        self._robot = robot
        self._arm_ids, _ = robot.find_joints(["panda_joint[1-7]"], preserve_order=True)
        self._ee_idx = robot.data.body_names.index("base_link")
        self._jac_idx = self._ee_idx - 1 if robot.is_fixed_base else self._ee_idx
        self._jac_joint_ids = self._arm_ids if robot.is_fixed_base else [i + 6 for i in self._arm_ids]
        fingers = [i for i, n in enumerate(robot.data.body_names) if n in ("right_inner_finger", "left_inner_finger")]
        self._finger_ids = fingers
        cfg = DifferentialIKControllerCfg(command_type="pose", use_relative_mode=False, ik_method="dls")
        self._ik = DifferentialIKController(cfg, num_envs=env.unwrapped.num_envs, device=robot.device)
        cfg_p = DifferentialIKControllerCfg(command_type="position", use_relative_mode=False, ik_method="dls")
        self._ik_pos = DifferentialIKController(cfg_p, num_envs=env.unwrapped.num_envs, device=robot.device)   # fallback near the reach limit
        self._bad = 0
        lim = _T(robot.data.soft_joint_pos_limits)[:, self._arm_ids, :]
        self._q_lo, self._q_hi = lim[..., 0], lim[..., 1]
        self.dt = float(env.unwrapped.step_dt)
        if self.debug:
            print(f"[SC] arm joints {self._arm_ids} ee body {self._ee_idx} fingers {fingers} dt {self.dt:.4f}", flush=True)

    def _ee_world(self):
        """Gripper base pose in the world, and the tool-centre point (base + R * tcp_vec)."""
        r = self._robot
        pos = _T(r.data.body_pos_w)[:, self._ee_idx, :]
        quat = _T(r.data.body_quat_w)[:, self._ee_idx, :]
        tcp = pos + quat_apply(quat, self._tcp_vec.to(pos.device).expand_as(pos))
        return pos, quat, tcp

    def _measure_tcp(self):
        """Tool centre in the gripper base frame, from the gripper's USD mesh bounds: the flattened DROID USD puts every gripper
        body at the base origin, so body poses say nothing; the mesh does. The long axis of the gripper's bounding box is the
        finger axis, and the fingertips are its end away from the flange (panda_link8)."""
        r = self._robot
        pos = _T(r.data.body_pos_w)[:, self._ee_idx, :]; quat = _T(r.data.body_quat_w)[:, self._ee_idx, :]
        qi = quat.clone(); qi[:, 1:] *= -1
        vec = None
        if os.environ.get("SC_TCP_FORCE", "0") == "1":
            vec = torch.zeros(3, device=pos.device); vec[0] = self.tcp_dz
        try:
            if vec is not None:
                raise RuntimeError("forced")
            import omni.usd
            from pxr import Usd, UsdGeom
            stage = omni.usd.get_context().get_stage()
            prim = stage.GetPrimAtPath("/World/envs/env_0/Robot/Gripper")
            if not prim.IsValid():
                prim = stage.GetPrimAtPath("/World/envs/env_0/Robot/Gripper/Robotiq_2F_85")
            cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), [UsdGeom.Tokens.default_, UsdGeom.Tokens.render, UsdGeom.Tokens.proxy])
            rng = cache.ComputeWorldBound(prim).ComputeAlignedRange(); mn, mx = rng.GetMin(), rng.GetMax()
            corners = torch.tensor([[x, y, z] for x in (mn[0], mx[0]) for y in (mn[1], mx[1]) for z in (mn[2], mx[2])],
                                   device=pos.device, dtype=torch.float32)
            loc = quat_apply(qi.expand(8, -1), corners - pos[0][None, :])
            ext = loc.max(0).values - loc.min(0).values
            ax = int(torch.argmax(ext).item())
            i8 = r.data.body_names.index("panda_link8")
            fl = quat_apply(qi, (_T(r.data.body_pos_w)[0, i8] - pos[0])[None, :])[0]
            sign = -1.0 if float(fl[ax]) > 0 else 1.0            # fingers lie opposite to the flange along the long axis
            tip = float(loc[:, ax].max().item()) if sign > 0 else float(loc[:, ax].min().item())
            vec = torch.zeros(3, device=pos.device); vec[ax] = tip - sign * 0.015   # pad centre 1.5 cm back from the tip
            if self.debug:
                print(f"[SC] gripper bbox in base frame: min {[round(float(v), 3) for v in loc.min(0).values]} max "
                      f"{[round(float(v), 3) for v in loc.max(0).values]} long axis {ax} flange {[round(float(v), 3) for v in fl]}", flush=True)
        except Exception as exc:  # noqa: BLE001
            print(f"[SC] bbox measurement failed ({exc!r}); using SC_TCP_DX along x", flush=True)
        if vec is None:
            vec = torch.zeros(3, device=pos.device); vec[0] = self.tcp_dz
        self._tcp_vec = vec
        if self.debug:
            print(f"[SC] tcp vector in the gripper base frame {[round(float(v), 3) for v in vec]}", flush=True)

    def _plan_episode(self, env):
        sc = env.unwrapped.scene
        obj = _T(sc[self.obj_name].data.root_pos_w)[0, :3].clone()
        dst = _T(sc[self.dest_name].data.root_pos_w)[0, :3].clone()
        g = self.grasp.to(obj.device)
        grasp = obj + g
        if self.magic:
            grasp = grasp.clone(); grasp[2] = obj[2] + 0.04          # no pinch needed: stop 4 cm above the payload centre
        self._obj_q0 = _T(sc[self.obj_name].data.root_quat_w)[0].clone()
        z_carry = obj[2] + self.carry_dz
        above_obj = grasp.clone(); above_obj[2] = z_carry
        above_dst = dst.clone(); above_dst[2] = z_carry
        place = dst.clone(); place[2] = dst[2] + max(0.06, self.carry_dz * 0.5)
        up = place.clone(); up[2] = z_carry
        self._plan = [(above_obj, 0, self.v_appr), (grasp, 0, self.v_appr), (grasp, 1, None), (above_obj, 1, self.v_appr),
                      (above_dst, 1, self.v_carry), (place, 1, self.v_appr), (place, 0, None), (up, 0, self.v_appr), (up, 0, None)]
        self._phase = 0; self._wait = 0
        _, q0, tcp = self._ee_world()
        # hold the gripper vertical: rotate the reset orientation so the finger axis (base +x) points straight down
        xg = quat_apply(q0, torch.tensor([[1.0, 0.0, 0.0]], device=q0.device))[0]
        down = torch.tensor([0.0, 0.0, -1.0], device=q0.device)
        ax = torch.cross(xg, down, dim=0); sn = float(torch.norm(ax).item()); cs = float(torch.dot(xg, down).item())
        if sn > 1e-6 and os.environ.get("SC_VERTICAL", "0") == "1":
            ang = math.atan2(sn, cs); ax = ax / sn
            q_rot = torch.tensor([[math.cos(ang / 2), *(ax * math.sin(ang / 2)).tolist()]], device=q0.device)
            self._quat_ref = quat_mul(q_rot, q0)
        else:
            self._quat_ref = q0
        self._target = tcp[0].clone()
        if self.debug:
            print(f"[SC] plan: obj {obj.tolist()} dest {dst.tolist()} tcp0 {tcp[0].tolist()} carry z {float(z_carry):.3f}", flush=True)

    def _step_target(self, tcp_now):
        """Advance the moving set-point toward the current waypoint at the phase's speed; a motion phase ends when the
        actual tool centre is within TOL of the waypoint (or after TIMEOUT steps); return the gripper command."""
        TOL, TIMEOUT = 0.025, 120
        wp_xyz, grip, v = self._plan[self._phase]
        self._wait += 1
        if v is None:                                   # dwell (gripper) phase
            if self._wait >= self.dwell and self._phase < len(self._plan) - 1:
                self._phase += 1; self._wait = 0; self._bad = 0
            return grip
        d = wp_xyz - self._target
        dist = float(torch.norm(d).item())
        step = v * self.dt
        self._target = wp_xyz.clone() if dist <= step else self._target + d / dist * step
        reached = float(torch.norm(wp_xyz - tcp_now).item()) <= TOL
        if (reached or self._wait >= TIMEOUT) and self._phase < len(self._plan) - 1:
            if self.debug and not reached:
                print(f"[SC] phase {self._phase} timed out {float(torch.norm(wp_xyz - tcp_now).item()):.3f} m short", flush=True)
            self._phase += 1; self._wait = 0; self._bad = 0
        return grip

    # ------------------------------------------------------------------ PolicyBase
    def get_action(self, env, observation):
        try:
            return self._act(env, observation)
        except Exception as exc:  # noqa: BLE001 -- hold the current pose rather than crash the rollout
            if self._err < 3:
                self._err += 1; print(f"[SC] error, holding pose: {exc!r}", flush=True)
            jp = observation["policy"]["joint_pos"]
            return torch.cat([jp, torch.zeros(jp.shape[0], 1, device=jp.device)], dim=1).to(torch.float32)

    def _act(self, env, observation):
        if self._ik is None:
            self._setup(env)
        buf = env.unwrapped.episode_length_buf
        cur = int(buf[0].item())
        if self._plan is None or cur < self._last_len or cur <= 1:
            if self._plan is None or cur < self._last_len:
                self._measure_tcp(); self._plan_episode(env)
        self._last_len = cur
        r = self._robot
        root_pos = _T(r.data.root_pos_w)[:, :3]; root_quat = _T(r.data.root_quat_w)
        ee_pos_w, ee_quat_w, tcp_w = self._ee_world()
        grip = self._step_target(tcp_w[0])
        # IK toward the moving set-point, orientation held at the reset orientation (fingers down)
        # command in the base frame: the gripper-base pose that puts the tool centre at the target
        goal_base_w = self._target[None, :].expand_as(ee_pos_w) - quat_apply(self._quat_ref, self._tcp_vec.to(ee_pos_w.device).expand_as(ee_pos_w))
        goal_pos_b, goal_quat_b = subtract_frame_transforms(root_pos, root_quat, goal_base_w, self._quat_ref)
        ee_pos_b, ee_quat_b = subtract_frame_transforms(root_pos, root_quat, ee_pos_w, ee_quat_w)
        q = _T(r.data.joint_pos)[:, self._arm_ids]
        jac = _T(r.root_physx_view.get_jacobians())[:, self._jac_idx, :, :][:, :, self._jac_joint_ids]
        err = float(torch.norm(tcp_w[0] - self._target).item())
        self._bad = self._bad + 1 if err > 0.04 else max(0, self._bad - 1)
        if self._bad > 6:                                # the pose IK cannot get there (reach limit / wrist limit): position only, wrist free
            self._ik_pos.set_command(goal_pos_b, ee_quat=ee_quat_b)
            q_des = self._ik_pos.compute(ee_pos_b, ee_quat_b, jac, q)
        else:
            self._ik.set_command(torch.cat([goal_pos_b, goal_quat_b], dim=-1))
            q_des = self._ik.compute(ee_pos_b, ee_quat_b, jac, q)
        q_des = torch.clamp(q_des, self._q_lo, self._q_hi)
        if self.debug and self._phase == 2 and self._wait == 1:
            _o = _T(env.unwrapped.scene[self.obj_name].data.root_pos_w)[0, :3]
            print(f"[SC] closing: base {[round(v, 3) for v in ee_pos_w[0].tolist()]} tcp {[round(v, 3) for v in tcp_w[0].tolist()]} obj {[round(v, 3) for v in _o.tolist()]}", flush=True)
        if self.debug and cur % 30 == 0:
            print(f"[SC] t={cur} phase {self._phase} err {err:.3f} bad {self._bad} tcp {[round(v, 3) for v in tcp_w[0].tolist()]} target {[round(v, 3) for v in self._target.tolist()]} grip {grip}", flush=True)
        if self.magic and 2 <= self._phase <= 5:                  # carried: the payload follows the tool centre, level, spawn yaw
            obj = env.unwrapped.scene[self.obj_name]
            p = tcp_w.clone(); p[:, 2] -= 0.04 - self._attach_dz
            obj.write_root_pose_to_sim(torch.cat([p, self._obj_q0[None, :].expand(p.shape[0], -1)], dim=-1))
            obj.write_root_velocity_to_sim(torch.zeros(p.shape[0], 6, device=p.device))
        act = torch.zeros(q.shape[0], 8, device=q.device, dtype=torch.float32)
        act[:, :7] = q_des.to(torch.float32); act[:, 7] = float(grip)
        return act.to(self.device)

    def reset(self, env_ids=None):
        self._plan = None
        self._last_len = -1
