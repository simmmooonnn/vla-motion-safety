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
        if self._trig_y is None and self._delay is None:
            return t
        if self._t0 is None or self._t0.shape[0] != t.shape[0]:
            self._t0 = torch.full_like(t, float("nan")); self._last_t = t.clone()
        reset = t < self._last_t                        # episode clock went backwards -> new episode
        self._t0[reset] = float("nan"); self._last_t = t.clone()
        if self._delay is not None:
            return (t - self._delay).clamp(min=0.0)
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
        if self._stop_dist is not None:
            spd = float((self.vx ** 2 + self.vy ** 2) ** 0.5)
            if spd > 1e-9:
                tau = tau.clamp(max=self._stop_dist / spd)
        px = self.sx + self.vx * tau                   # (num_envs,)
        py = self.sy + self.vy * tau
        pz = torch.full_like(px, self.pz)
        quat = torch.tensor([1.0, 0.0, 0.0, 0.0], device=env.device).repeat(env.num_envs, 1)  # w,x,y,z
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
