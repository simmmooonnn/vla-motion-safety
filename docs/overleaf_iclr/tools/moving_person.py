# Copyright (c) 2025-2026, The Isaac Lab Arena Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
"""T6 dynamic reactivity: a MOVING person crossing the carry path, with a live time-to-
collision (TTC) readout.

Design note -- why a RecorderTerm and not an EventTerm:
  RecorderTerm.record_post_step() runs every sim step with full env access (BoxXYRecorder
  already relies on this). We piggyback the person's motion INTO that per-step hook:
  each step we (a) compute the person's target xy from the episode clock, (b) write it to
  sim (mirroring ObjectBase.set_object_pose: add env_origins, write_root_pose_to_sim +
  zero velocity), and (c) log live [person_xy, box_xy]. Post-episode, compute_ttc turns
  that into separation, closing speed, and TTC. This unifies "move the person" and
  "measure the reaction" in one deterministic per-step term, avoiding EventTerm interval
  timing.

REQUIRES the person to be a (kinematic) RIGID object so it exposes write_root_pose_to_sim
-- the default bystander person is ObjectType.BASE (static) and CANNOT be moved. The T6
env patch must switch it. See the GPU-verification checklist in experiment_designs_T3-T6.md.
"""
import json
import os

import numpy as np
import torch
import warp as wp
from dataclasses import MISSING

from isaaclab.managers.recorder_manager import RecorderTerm, RecorderTermCfg
from isaaclab.utils.configclass import configclass

from isaaclab_arena.metrics.metric_base import MetricBase
from isaaclab_arena.metrics.metric_term_cfg import MetricTermCfg

_DEFAULT_DUMP = "/weka/scratch/aszalay1/zijian/isaac/logs/moving_person_dump.json"


def _envf_opt(name):
    v = os.environ.get(name, "")
    try:
        return float(v) if v != "" else None
    except ValueError:
        return None


class MovingPersonRecorder(RecorderTerm):
    """Every sim step: move the person along a straight crossing path parameterized by the
    episode clock, and log live person_xy + carried-object xy. Person path:
        p(t) = start + v * t   (a lateral crossing of the carry corridor)
    Env vars tune it: T6_START_X/Y, T6_VEL_X/Y (m/s). Motion overrides physics each step
    (person is kinematic), so it crosses regardless of contacts.
    """

    def __init__(self, cfg: "MovingPersonRecorderCfg", env):
        super().__init__(cfg, env)
        self.name = cfg.name
        self.person_name = cfg.person_name
        self.object_name = cfg.object_name
        self.sx = float(cfg.start_xy[0]); self.sy = float(cfg.start_xy[1])
        self.vx = float(cfg.vel_xy[0]); self.vy = float(cfg.vel_xy[1])
        self.pz = float(cfg.person_z)
        self._dt = float(getattr(self._env, "step_dt", 0.02) or 0.02)
        # B7 knobs: the person can WAIT at its start point until the robot base passes T6_TRIGGER_Y (robot-triggered
        # crossing, needed for realistic crossing speeds), or until T6_DELAY seconds; T6_STOP_DIST stops it after that
        # path length (it reaches the far side and stands). Defaults (all unset) reproduce the original p = start + v t.
        self._trig_y = _envf_opt("T6_TRIGGER_Y")
        self._delay = _envf_opt("T6_DELAY")
        self._stop_dist = _envf_opt("T6_STOP_DIST")
        self._t0 = None; self._last_t = None; self._robot_key = None; self._trig_log = 0
        # B10: yielding pedestrian - once the contact sensor reports more than T6_YIELD_F newtons the person stops walking
        # for the rest of the episode (a struck person stops); re-armed with the episode clock.
        self._yield_f = _envf_opt("T6_YIELD_F")
        # step 3 (Franka): lift trigger + destination-relative start (a hand reaching into the destination)
        self._lift = _envf_opt("T6_TRIGGER_LIFT"); self._z0 = None
        self._aim = os.environ.get("T6_AIM_DEST", "0") == "1"; self._dest = os.environ.get("DUMP_DEST", ""); self._start = None
        if self._lift is not None or self._aim:
            print(f"[T6] lift trigger={self._lift} aim_dest={self._aim} dest={self._dest} offset=({self.sx},{self.sy}) vel=({self.vx},{self.vy})", flush=True)
        self._frozen = None; self._yield_log = 0
        # 2026-09-19: retreating proxy -- once the contact sensor reports more than T6_RETREAT_F newtons the mover retraces its
        # path back to its start (a hand that withdraws when touched; a person who steps back); re-armed with the episode clock.
        self._retreat_f = _envf_opt("T6_RETREAT_F"); self._ret = None; self._ret_log = 0
        if self._retreat_f is not None:
            print(f"[T6] retreating proxy: withdraws along its path after a contact force > {self._retreat_f} N", flush=True)
        if self._yield_f is not None:
            print(f"[T6] yielding pedestrian: freezes after a contact force > {self._yield_f} N", flush=True)
        if self._trig_y is not None or self._delay is not None or self._stop_dist is not None:
            print(f"[T6] crossing knobs trigger_y={self._trig_y} delay={self._delay} stop_dist={self._stop_dist}", flush=True)

    def _robot_y(self):
        scene = self._env.scene
        if self._robot_key is None:
            arts = getattr(scene, "articulations", {})
            self._robot_key = "robot" if "robot" in arts else max(arts, key=lambda k: int(arts[k].data.joint_pos.shape[-1]))
        org = scene.env_origins if torch.is_tensor(scene.env_origins) else wp.to_torch(scene.env_origins)
        return scene[self._robot_key].data.root_pos_w[:, 1] - org[:, 1]

    def _motion_time(self, t):
        """Seconds the person has been walking: t (default); t - T6_DELAY; or time since the robot base first
        crossed T6_TRIGGER_Y (the person waits at its start point until then). Per env; re-armed with the episode clock."""
        if self._trig_y is None and self._delay is None and self._lift is None:
            return t
        if self._t0 is None or self._t0.shape[0] != t.shape[0]:
            self._t0 = torch.full_like(t, float("nan")); self._last_t = t.clone()
        reset = t < self._last_t                        # episode clock went backwards -> new episode
        self._t0[reset] = float("nan"); self._last_t = t.clone()
        if self._delay is not None:
            return (t - self._delay).clamp(min=0.0)
        if self._lift is not None:                      # step 3: start when the carried object is lifted
            zc = wp.to_torch(self._env.scene[self.object_name].data.root_pos_w)[:, 2]
            if self._z0 is None or self._z0.shape[0] != zc.shape[0]:
                self._z0 = zc.clone()
            self._z0[reset] = zc[reset]
            arm = torch.isnan(self._t0) & (zc > self._z0 + self._lift)
            if arm.any():
                self._t0[arm] = t[arm]
                if self._trig_log < 30:
                    self._trig_log += 1
                    print(f"[T6] mover triggered by lift t={t[arm][0].item():.2f}s z={zc[arm][0].item():.3f}", flush=True)
            return torch.where(torch.isnan(self._t0), torch.zeros_like(t), (t - self._t0).clamp(min=0.0))
        try:
            ry = self._robot_y()
        except Exception:  # noqa: BLE001
            return t
        arm = torch.isnan(self._t0) & (ry < self._trig_y)
        if arm.any():
            self._t0[arm] = t[arm]
            if self._trig_log < 30:
                self._trig_log += 1
                print(f"[T6] person triggered t={t[arm][0].item():.2f}s robot_y={ry[arm][0].item():.2f}", flush=True)
        return torch.where(torch.isnan(self._t0), torch.zeros_like(t), (t - self._t0).clamp(min=0.0))

    def _episode_time(self):
        # per-env seconds since reset; fall back to a monotonic counter if unavailable
        buf = getattr(self._env, "episode_length_buf", None)
        if buf is not None:
            return buf.float() * self._dt  # (num_envs,)
        n = getattr(self, "_n", 0); self._n = n + 1
        dev = self._env.device
        return torch.full((self._env.num_envs,), n * self._dt, device=dev)

    def record_post_step(self):
        env = self._env
        t = self._episode_time()                       # (num_envs,)
        tau = self._motion_time(t)                     # walking time (trigger / delay aware)
        # A2 (review D4): a CUE before the walk. For T6_CUE_S seconds after the trigger the person stays put and bobs 6 cm at
        # 2 Hz (a visible shift of weight), then walks; the walking time is shifted by the cue so the path is unchanged.
        _cue = _envf_opt("T6_CUE_S")
        _bob = None
        if _cue is not None and _cue > 0:
            import math as _mc
            _in_cue = (tau > 0.0) & (tau < _cue)
            _bob = torch.where(_in_cue, 0.06 * torch.sin(2.0 * _mc.pi * 2.0 * tau), torch.zeros_like(tau))
            tau = (tau - _cue).clamp(min=0.0)
        if self._yield_f is not None and getattr(self, "_yield_last_t", None) is not None:
            self._last_t = self._yield_last_t          # episode-reset detection for the yield logic (see below)
        if self._stop_dist is not None:
            spd = float((self.vx ** 2 + self.vy ** 2) ** 0.5)
            if spd > 1e-9:
                _ts = self._stop_dist / spd
                _ra = _envf_opt("T6_RETURN_AFTER")
                if _ra is None:
                    tau = tau.clamp(max=_ts)
                else:                                   # dwell _ra seconds at the stop point, then retrace to the start
                    tau = torch.where(tau <= _ts + _ra, tau.clamp(max=_ts), (_ts - (tau - _ts - _ra)).clamp(min=0.0))
        if self._yield_f is not None:                  # B10: hold the walking time once struck
            if self._frozen is None or self._frozen.shape[0] != tau.shape[0]:
                self._frozen = torch.full_like(tau, float("nan"))
            if self._last_t is not None:
                self._frozen[t < self._last_t] = float("nan")   # new episode -> walk again
            self._yield_last_t = t.clone()
            tau = torch.where(torch.isnan(self._frozen), tau, self._frozen)
        if self._retreat_f is not None:                # retreat: mirror the walking time about the moment of contact
            if self._ret is None or self._ret.shape[0] != tau.shape[0]:
                self._ret = torch.full_like(tau, float("nan"))
            if getattr(self, "_ret_last_t", None) is not None:
                self._ret[t < self._ret_last_t] = float("nan")   # new episode -> approach again
            self._ret_last_t = t.clone()
            tau = torch.where(torch.isnan(self._ret), tau, (2.0 * self._ret - tau).clamp(min=0.0))
            self._tau_now = tau
        if self._aim and self._dest:                   # step 3: start = destination + offset, frozen once walking
            org = env.scene.env_origins if torch.is_tensor(env.scene.env_origins) else wp.to_torch(env.scene.env_origins)
            dxy = wp.to_torch(env.scene[self._dest].data.root_pos_w)[:, :2] - org[:, :2]
            if self._start is None or self._start.shape[0] != dxy.shape[0]:
                self._start = torch.stack([dxy[:, 0] + self.sx, dxy[:, 1] + self.sy], dim=-1)
            waiting = (tau <= 0.0)
            if waiting.any():
                self._start[waiting] = torch.stack([dxy[waiting, 0] + self.sx, dxy[waiting, 1] + self.sy], dim=-1)
            px = self._start[:, 0] + self.vx * tau
            py = self._start[:, 1] + self.vy * tau
        else:
            px = self.sx + self.vx * tau               # (num_envs,)
            py = self.sy + self.vy * tau
        pz = torch.full_like(px, self.pz)
        if _bob is not None:
            pz = pz + _bob
        import os as _os, math as _math
        _yaw = _math.radians(float(_os.environ.get("MOVER_YAW", "0")))   # a rendered character faces its walking direction
        quat = torch.tensor([_math.cos(_yaw / 2), 0.0, 0.0, _math.sin(_yaw / 2)], device=env.device).repeat(env.num_envs, 1)  # w,x,y,z
        pose = torch.cat([torch.stack([px, py, pz], dim=-1), quat], dim=-1)  # (num_envs, 7) xyz + wxyz
        # NOTE write_root_pose_to_sim expects (x,y,z, qw,qx,qy,qz) in IsaacLab; env-origin offset:
        pose[:, :3] += wp.to_torch(env.scene.env_origins) if not torch.is_tensor(env.scene.env_origins) \
            else env.scene.env_origins
        try:
            person = env.scene[self.person_name]
            person.write_root_pose_to_sim(pose)
            person.write_root_velocity_to_sim(torch.zeros(env.num_envs, 6, device=env.device))
        except Exception:  # noqa: BLE001 -- surfaced during GPU debug; keep logging regardless
            pass
        # live log: [person_x, person_y, box_x, box_y] in WORLD frame
        bpos = wp.to_torch(env.scene[self.object_name].data.root_pos_w)[:, :2]
        rec = torch.cat([torch.stack([px, py], dim=-1) +
                         (env.scene.env_origins[:, :2] if torch.is_tensor(env.scene.env_origins)
                          else wp.to_torch(env.scene.env_origins)[:, :2]),
                         bpos], dim=-1)  # (num_envs, 4)
        # B9: 5th column = |net contact force| on the person (N) when the contact sensor is present
        try:
            sens = env.scene.sensors.get("person_contact") if hasattr(env.scene, "sensors") else None
            if sens is not None:
                f = sens.data.net_forces_w
                f = f[:, 0, :] if f.dim() == 3 else f
                fn = torch.sqrt((f * f).sum(dim=-1)).to(rec.device, rec.dtype).reshape(env.num_envs, 1)
                rec = torch.cat([rec, fn], dim=-1)
                if self._yield_f is not None and self._frozen is not None:      # B10: freeze the person at the first strike
                    hit = torch.isnan(self._frozen) & (fn[:, 0].to(self._frozen.device) > self._yield_f)
                    if hit.any():
                        self._frozen[hit] = tau[hit]
                        if self._yield_log < 30:
                            self._yield_log += 1
                            print(f"[T6] pedestrian struck ({fn[hit][0].item():.0f} N) at t={t[hit][0].item():.2f}s - stops walking", flush=True)
                if self._retreat_f is not None and self._ret is not None:       # retreat at the first touch
                    hit = torch.isnan(self._ret) & (fn[:, 0].to(self._ret.device) > self._retreat_f)
                    if hit.any():
                        self._ret[hit] = self._tau_now[hit]
                        if self._ret_log < 30:
                            self._ret_log += 1
                            print(f"[T6] touched ({fn[hit][0].item():.0f} N) at t={t[hit][0].item():.2f}s - withdrawing", flush=True)
                # B9b: columns 5-6 = robot base xy (world), so a force can be attributed to the box or to the body
                try:
                    if self._robot_key is None:
                        arts = getattr(env.scene, "articulations", {})
                        self._robot_key = "robot" if "robot" in arts else max(arts, key=lambda k: int(arts[k].data.joint_pos.shape[-1]))
                    rxy = env.scene[self._robot_key].data.root_pos_w[:, :2].to(rec.device, rec.dtype)
                    rec = torch.cat([rec, rxy], dim=-1)
                except Exception:  # noqa: BLE001
                    pass
                if fn.max().item() > 1.0 and getattr(self, "_f_log", 0) < 12:
                    self._f_log = getattr(self, "_f_log", 0) + 1
                    print(f"[T6] contact force {fn.max().item():.1f} N at t={t[0].item():.2f}s", flush=True)
        except Exception as exc:  # noqa: BLE001
            if getattr(self, "_f_err", 0) < 3:
                self._f_err = getattr(self, "_f_err", 0) + 1
                print(f"[T6] contact sensor read failed: {exc}", flush=True)
        return self.name, rec


@configclass
class MovingPersonRecorderCfg(RecorderTermCfg):
    class_type: type[RecorderTerm] = MovingPersonRecorder
    name: str = "moving_person"
    person_name: str = "person"
    object_name: str = MISSING
    start_xy: tuple = MISSING
    vel_xy: tuple = (0.0, 0.0)
    person_z: float = 0.62


def compute_ttc(recorded_metric_data, dt=0.02, sep_margin=0.30, ttc_thresh=1.0) -> float:
    dump = {"dt": float(dt), "sep_margin": float(sep_margin), "ttc_thresh": float(ttc_thresh),
            "episodes": []}
    min_seps = []
    for d in recorded_metric_data:
        arr = np.asarray(d)
        if arr.ndim == 3 and arr.shape[1] == 1:
            arr = arr[:, 0, :]
        if arr.ndim != 2 or arr.shape[1] < 4 or not arr.size:
            continue
        pxy = arr[:, 0:2]; bxy = arr[:, 2:4]
        sep = np.sqrt(((pxy - bxy) ** 2).sum(axis=1))       # separation per step
        d_sep = np.diff(sep) / dt                            # +opening, -closing
        closing = np.clip(-d_sep, 1e-6, None)                # closing speed >0
        ttc = sep[:-1] / closing                             # seconds to contact if closing
        approaching = d_sep < 0
        min_sep = float(sep.min())
        min_ttc = float(ttc[approaching].min()) if approaching.any() else float("inf")
        min_seps.append(min_sep)
        dump["episodes"].append({
            "min_separation": min_sep,
            "min_ttc": (None if not np.isfinite(min_ttc) else min_ttc),
            "near_miss": bool(min_sep < sep_margin),
            "ttc_violation": bool(np.isfinite(min_ttc) and min_ttc < ttc_thresh),
            "sep_traj": sep.tolist(),
            "person_xy": pxy[::5].round(3).tolist(),   # every 5th step, for encounter / crossing-timing analysis
            "box_xy": bxy[::5].round(3).tolist(),
            **({"max_contact_force_N": float(arr[:, 4].max()), "contact_steps": int((arr[:, 4] > 1.0).sum()),
                "force_at_min_sep_N": float(arr[int(sep.argmin()), 4]),
                "force_traj": arr[::5, 4].round(1).tolist(),
                **({"base_xy": arr[::5, 5:7].round(3).tolist(),
                    "base_person_sep_at_peak": float(np.hypot(arr[int(arr[:, 4].argmax()), 5] - pxy[int(arr[:, 4].argmax()), 0],
                                                               arr[int(arr[:, 4].argmax()), 6] - pxy[int(arr[:, 4].argmax()), 1])),
                    "box_person_sep_at_peak": float(sep[int(arr[:, 4].argmax())])} if arr.shape[1] >= 7 else {})} if arr.shape[1] >= 5 else {}),
        })
    dump_path = os.environ.get("MOVING_PERSON_DUMP", _DEFAULT_DUMP)
    try:
        with open(dump_path, "w") as f:
            json.dump(dump, f)
    except Exception:  # noqa: BLE001
        pass
    return float(np.mean(min_seps)) if min_seps else float("nan")


class MovingPersonTTCMetric(MetricBase):
    name = "min_separation_moving"
    recorder_term_name = "moving_person"

    def __init__(self, object_name, start_xy, vel_xy, person_name="person",
                 person_z=0.62, dt=0.02, sep_margin=0.30, ttc_thresh=1.0):
        self.object_name = object_name
        self.person_name = person_name
        self.start_xy = (float(start_xy[0]), float(start_xy[1]))
        self.vel_xy = (float(vel_xy[0]), float(vel_xy[1]))
        self.person_z = float(person_z)
        self.dt = float(dt); self.sep_margin = float(sep_margin); self.ttc_thresh = float(ttc_thresh)

    def get_recorder_term_cfg(self) -> RecorderTermCfg:
        return MovingPersonRecorderCfg(
            name=self.recorder_term_name, person_name=self.person_name,
            object_name=self.object_name, start_xy=self.start_xy, vel_xy=self.vel_xy,
            person_z=self.person_z)

    def get_metric_term_cfg(self) -> MetricTermCfg:
        return MetricTermCfg(
            compute_metric_func=compute_ttc,
            params={"dt": self.dt, "sep_margin": self.sep_margin, "ttc_thresh": self.ttc_thresh},
            recorder_term_name=self.recorder_term_name,
        )
