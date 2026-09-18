# Copyright (c) 2026. SPDX-License-Identifier: Apache-2.0
"""A scripted straight-line carry: the control that says which safety columns any direct carrier scores on.

The policy reads the payload and destination poses from the simulator (it is blind to the person on purpose), grasps the
payload from above, lifts it to a carry height, moves it on a straight line at a constant speed to a point above the
destination, lowers it and releases. Differential IK (damped least squares) on the Robotiq gripper base turns the
Cartesian target into the DROID absolute joint-position action (7 joints + a 0/1 gripper command).

Knobs (environment variables): SC_OBJ / SC_DEST (scene names of payload and destination), SC_SPEED (carry speed, m/s),
SC_APPROACH_SPEED, SC_CARRY_DZ (carry height above the payload's spawn height), SC_GRASP_DZ / SC_GRASP_DX / SC_GRASP_DY
(grasp point relative to the payload origin, in the world frame), SC_TCP_DZ (tool centre below the gripper base, m;
measured from the finger bodies when unset), SC_DWELL (steps to wait after a gripper command), SC_DEBUG=1.
"""
from __future__ import annotations

import math
import os
from dataclasses import dataclass

import torch
import warp as wp

from isaaclab.controllers import DifferentialIKController, DifferentialIKControllerCfg
from isaaclab.utils.math import combine_frame_transforms, quat_apply, subtract_frame_transforms
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
        self.tcp_dz = _f("SC_TCP_DZ", 0.0)
        self.dwell = int(_f("SC_DWELL", 8))
        self.debug = os.environ.get("SC_DEBUG", "0") == "1"
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
        lim = _T(robot.data.soft_joint_pos_limits)[:, self._arm_ids, :]
        self._q_lo, self._q_hi = lim[..., 0], lim[..., 1]
        self.dt = float(env.unwrapped.step_dt)
        if self.debug:
            print(f"[SC] arm joints {self._arm_ids} ee body {self._ee_idx} fingers {fingers} dt {self.dt:.4f}", flush=True)

    def _ee_world(self):
        """Gripper base pose in the world, and the tool-centre point below it."""
        r = self._robot
        pos = _T(r.data.body_pos_w)[:, self._ee_idx, :]
        quat = _T(r.data.body_quat_w)[:, self._ee_idx, :]
        off = torch.zeros_like(pos); off[:, 2] = self._tcp
        tcp = pos + quat_apply(quat, off)
        return pos, quat, tcp

    def _measure_tcp(self):
        """Distance from the gripper base to the midpoint of the inner fingers, along the base's local z."""
        if self.tcp_dz > 0 or len(self._finger_ids) < 2:
            self._tcp = self.tcp_dz if self.tcp_dz > 0 else 0.16
            return
        r = self._robot
        pos = _T(r.data.body_pos_w)[:, self._ee_idx, :]; quat = _T(r.data.body_quat_w)[:, self._ee_idx, :]
        mid = _T(r.data.body_pos_w)[:, self._finger_ids, :].mean(dim=1)
        d = mid - pos
        z_axis = quat_apply(quat, torch.tensor([[0.0, 0.0, 1.0]], device=pos.device).expand_as(pos))
        meas = float((d * z_axis).sum(-1)[0].item()) + 0.02             # fingertip pads sit a little past the finger origins
        self._tcp = meas if meas > 0.08 else 0.16                          # a Robotiq 2F-85 pad centre sits ~0.15-0.17 m below its base
        if self.debug:
            print(f"[SC] measured finger midpoint offset {meas:.3f} m along the gripper z -> tcp {self._tcp:.3f}", flush=True)
            names = r.data.body_names; P = _T(r.data.body_pos_w)[0]
            qi = quat.clone(); qi[:, 1:] *= -1                             # inverse rotation of the gripper base
            for i, n in enumerate(names):
                loc = quat_apply(qi, (P[i] - pos[0])[None, :])[0]
                print(f"[SC]   body {i:2d} {n:32s} in gripper frame {[round(float(v), 3) for v in loc]}", flush=True)

    def _plan_episode(self, env):
        sc = env.unwrapped.scene
        obj = _T(sc[self.obj_name].data.root_pos_w)[0, :3].clone()
        dst = _T(sc[self.dest_name].data.root_pos_w)[0, :3].clone()
        g = self.grasp.to(obj.device)
        grasp = obj + g
        z_carry = obj[2] + self.carry_dz
        above_obj = grasp.clone(); above_obj[2] = z_carry
        above_dst = dst.clone(); above_dst[2] = z_carry
        place = dst.clone(); place[2] = dst[2] + max(0.06, self.carry_dz * 0.5)
        up = place.clone(); up[2] = z_carry
        self._plan = [(above_obj, 0, self.v_appr), (grasp, 0, self.v_appr), (grasp, 1, None), (above_obj, 1, self.v_appr),
                      (above_dst, 1, self.v_carry), (place, 1, self.v_appr), (place, 0, None), (up, 0, self.v_appr), (up, 0, None)]
        self._phase = 0; self._wait = 0
        _, self._quat_ref, tcp = self._ee_world()
        self._target = tcp[0].clone()
        if self.debug:
            print(f"[SC] plan: obj {obj.tolist()} dest {dst.tolist()} tcp0 {tcp[0].tolist()} carry z {float(z_carry):.3f}", flush=True)

    def _step_target(self):
        """Advance the moving set-point toward the current waypoint at the phase's speed; return the gripper command."""
        wp_xyz, grip, v = self._plan[self._phase]
        if v is None:                                   # dwell (gripper) phase
            self._wait += 1
            if self._wait >= self.dwell and self._phase < len(self._plan) - 1:
                self._phase += 1; self._wait = 0
            return grip
        d = wp_xyz - self._target
        dist = float(torch.norm(d).item())
        step = v * self.dt
        if dist <= step:
            self._target = wp_xyz.clone()
            if self._phase < len(self._plan) - 1:
                self._phase += 1
        else:
            self._target = self._target + d / dist * step
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
        grip = self._step_target()
        # IK toward the moving set-point, orientation held at the reset orientation (fingers down)
        r = self._robot
        root_pos = _T(r.data.root_pos_w)[:, :3]; root_quat = _T(r.data.root_quat_w)
        ee_pos_w, ee_quat_w, tcp_w = self._ee_world()
        # command in the base frame: the gripper-base pose that puts the tool centre at the target
        off = torch.zeros_like(ee_pos_w); off[:, 2] = -self._tcp
        goal_base_w = self._target[None, :].expand_as(ee_pos_w) + quat_apply(self._quat_ref, off)
        goal_pos_b, goal_quat_b = subtract_frame_transforms(root_pos, root_quat, goal_base_w, self._quat_ref)
        ee_pos_b, ee_quat_b = subtract_frame_transforms(root_pos, root_quat, ee_pos_w, ee_quat_w)
        q = _T(r.data.joint_pos)[:, self._arm_ids]
        jac = _T(r.root_physx_view.get_jacobians())[:, self._jac_idx, :, :][:, :, self._jac_joint_ids]
        self._ik.set_command(torch.cat([goal_pos_b, goal_quat_b], dim=-1))
        q_des = self._ik.compute(ee_pos_b, ee_quat_b, jac, q)
        q_des = torch.clamp(q_des, self._q_lo, self._q_hi)
        if self.debug and cur % 30 == 0:
            print(f"[SC] t={cur} phase {self._phase} tcp {tcp_w[0].tolist()} target {self._target.tolist()} grip {grip}", flush=True)
        act = torch.zeros(q.shape[0], 8, device=q.device, dtype=torch.float32)
        act[:, :7] = q_des.to(torch.float32); act[:, 7] = float(grip)
        return act.to(self.device)

    def reset(self, env_ids=None):
        self._plan = None
        self._last_len = -1
