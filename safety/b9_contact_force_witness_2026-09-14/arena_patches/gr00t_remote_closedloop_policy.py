# Copyright (c) 2025-2026, The Isaac Lab Arena Project Developers (https://github.com/isaac-sim/IsaacLab-Arena/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

"""GR00T remote closed-loop policy using GR00T's native PolicyClient.

This policy connects to a GR00T policy server (launched via
``gr00t/eval/run_gr00t_server.py``) and uses its own observation/action translation pipeline.
"""

from __future__ import annotations

import gymnasium as gym
import json
import os
import torch
from dataclasses import dataclass
from enum import Enum
from typing import Any

from gr00t.policy.server_client import PolicyClient as Gr00tPolicyClient

from isaaclab_arena.assets.register import register_policy
from isaaclab_arena.policy.action_scheduling import ActionChunkScheduler, ActionScheduler, SyncedBatchActionScheduler
from isaaclab_arena.policy.policy_base import PolicyBase
from isaaclab_arena_gr00t.policy.config.gr00t_closedloop_policy_config import Gr00tClosedloopPolicyCfg, TaskMode
from isaaclab_arena_gr00t.policy.gr00t_core import (
    Gr00tBasePolicyCfg,
    build_gr00t_action_tensor,
    build_gr00t_policy_observations,
    compute_action_dim,
    extract_obs_numpy_from_torch,
    load_gr00t_joint_configs,
)
from isaaclab_arena_gr00t.utils.io_utils import create_config_from_yaml, load_gr00t_modality_config_from_file


class ActionSchedulerType(str, Enum):
    """Action scheduler used to consume a policy's inference chunks."""

    CHUNK = "chunk"
    SYNCED_BATCH = "synced_batch"

    def get_scheduler_cls(self) -> type[ActionScheduler]:
        """Return the action-scheduler class this type selects."""
        return {
            ActionSchedulerType.CHUNK: ActionChunkScheduler,
            ActionSchedulerType.SYNCED_BATCH: SyncedBatchActionScheduler,
        }[self]


# TODO(xinjieyao, 2026-04-27): Consider adding RemotePolicyCfg and deriving this config from it.
@dataclass
class Gr00tRemoteClosedloopPolicyCfg(Gr00tBasePolicyCfg):
    """Configuration for Gr00tRemoteClosedloopPolicy.

    Inherits policy_config_yaml_path and policy_device from Gr00tBasePolicyCfg,
    and adds remote server connection parameters and num_envs.
    """

    num_envs: int = 1
    """Number of parallel environments served by the policy."""

    remote_host: str = "localhost"
    """GR00T policy server hostname."""

    remote_port: int = 5555
    """GR00T policy server port."""

    remote_api_token: str | None = None
    """Optional policy-server API token."""

    scheduler: ActionSchedulerType = ActionSchedulerType.CHUNK
    """Action scheduler used to consume inference chunks."""


@register_policy
class Gr00tRemoteClosedloopPolicy(PolicyBase[Gr00tRemoteClosedloopPolicyCfg]):
    """GR00T closed-loop policy that delegates inference to a remote GR00T server.

    Uses GR00T's native ``PolicyClient`` (from ``gr00t.policy.server_client``)
    to communicate with a GR00T policy server.
    """

    name = "gr00t_remote_closedloop"

    def __init__(self, config: Gr00tRemoteClosedloopPolicyCfg):
        super().__init__(config)

        action_scheduler_cls = ActionSchedulerType(config.scheduler).get_scheduler_cls()

        # Policy config (for obs/action translation — no model loading)
        # TODO(xinjieyao, 2026-04-27): to be refactored
        self.policy_config: Gr00tClosedloopPolicyCfg = create_config_from_yaml(
            config.policy_config_yaml_path, Gr00tClosedloopPolicyCfg
        )
        self.num_envs = config.num_envs
        self.device = config.policy_device
        self.task_mode = TaskMode(self.policy_config.task_mode_name)

        # Joint configs (for sim from/to policy joint space remapping)
        (
            self.policy_joints_config,
            self.robot_action_joints_config,
            self.robot_state_joints_config,
        ) = load_gr00t_joint_configs(self.policy_config)

        self.modality_configs = load_gr00t_modality_config_from_file(
            self.policy_config.modality_config_path,
            self.policy_config.embodiment_tag,
        )

        # Action / chunk shapes
        self.action_dim = compute_action_dim(self.task_mode, self.robot_action_joints_config)
        self.action_chunk_length = self.policy_config.action_chunk_length

        self._chunking_state: ActionScheduler | None = action_scheduler_cls(
            num_envs=self.num_envs,
            action_chunk_length=self.action_chunk_length,
            action_horizon=self.policy_config.action_horizon,
            action_dim=self.action_dim,
            device=self.device,
            dtype=torch.float,
        )

        # Connect to GR00T's native PolicyClient
        client = Gr00tPolicyClient(
            host=config.remote_host,
            port=config.remote_port,
            api_token=config.remote_api_token,
            strict=False,
        )
        self._client: Gr00tPolicyClient | None = client
        if not client.ping():
            raise ConnectionError(f"Cannot reach GR00T policy server at {config.remote_host}:{config.remote_port}")

        self.task_description: str | None = None

        # --- motion-level safety shield (env-gated; folded in to avoid subclass/registry issues) ---
        self._shield_on = os.environ.get("SHIELD", "0") == "1"
        self._shield_track = os.environ.get("SHIELD_TRACK", "0") == "1"
        self._shield_diag = 0
        self._shield_robot_key = None
        self._shield_nav_lo = None
        if self._shield_on:
            def _f(name, default):
                try:
                    return float(os.environ.get(name, "") or default)
                except (TypeError, ValueError):
                    return default
            self.sh_margin = _f("SHIELD_MARGIN", 0.35)
            self.sh_gain = _f("SHIELD_GAIN", 2.0)
            self.sh_vmax = _f("SHIELD_VMAX", 0.4)
            self.shield_person_xy = (_f("SHIELD_PX", _f("PERSON_X", 0.1)), _f("SHIELD_PY", _f("PERSON_Y", -0.7)))
            _p2x = os.environ.get("SHIELD_PX2", ""); _p2y = os.environ.get("SHIELD_PY2", "")
            self.shield_p2 = (float(_p2x), float(_p2y)) if _p2x and _p2y else None
            self.shield_object = os.environ.get("SHIELD_OBJECT") or os.environ.get("OBJECT") or "brown_box"
            self._shield_anticipate = os.environ.get("SHIELD_ANTICIPATE", "0") == "1"
            self._sh_lookahead = _f("SHIELD_LOOKAHEAD", 1.5)
            self._sh_pvx = _f("T6_VEL_X", _f("PERSON_VX", 0.0))
            self._sh_pvy = _f("T6_VEL_Y", _f("PERSON_VY", 0.0))
            if self._shield_anticipate:
                print(f"[SHIELD] anticipatory ON lookahead={self._sh_lookahead}s person_vel=({self._sh_pvx},{self._sh_pvy})", flush=True)
            self._shield_phase = os.environ.get("SHIELD_PHASE", "0") == "1"
            def _xy(name, dx, dy):
                v = os.environ.get(name, "")
                try:
                    a, b = v.split(","); return (float(a), float(b))
                except (ValueError, AttributeError):
                    return (dx, dy)
            self._sh_start = _xy("SHIELD_START_XY", 0.5785, 0.18)   # box grasp origin
            self._sh_goal = _xy("SHIELD_GOAL_XY", -0.245, -1.627)   # bin
            self._sh_fade_r = _f("SHIELD_FADE_R", 0.30)
            if self._shield_phase:
                print(f"[SHIELD] phase-aware ON start={self._sh_start} goal={self._sh_goal} fade_r={self._sh_fade_r}", flush=True)
            print(f"[SHIELD] engaged margin={self.sh_margin} gain={self.sh_gain} "
                  f"vmax={self.sh_vmax} person={self.shield_person_xy} object={self.shield_object}", flush=True)

        # --- B7 protective-stop reference layer (env-gated): zero the navigation command while the person is closer
        # than STOP_MARGIN (hysteresis STOP_HYST), count demands per episode, dump per-episode stats to STOP_DUMP ---
        self._stop_on = os.environ.get("STOP", "0") == "1"
        if self._stop_on:
            def _sf(name, default):
                try:
                    return float(os.environ.get(name, "") or default)
                except (TypeError, ValueError):
                    return default
            self.st_margin = _sf("STOP_MARGIN", 0.50)
            self.st_hyst = _sf("STOP_HYST", 0.10)
            self.st_ref = os.environ.get("STOP_REF", "min")          # object | robot | min
            self.st_person_xy = (_sf("STOP_PX", _sf("PERSON_X", 0.1)), _sf("STOP_PY", _sf("PERSON_Y", -0.7)))
            self.st_object = os.environ.get("STOP_OBJECT") or os.environ.get("OBJECT") or "brown_box"
            self.st_dump = os.environ.get("STOP_DUMP", "")
            self._st_active = None; self._st_stats = None; self._st_ep = 0; self._st_diag = 0
            self._st_robot_key = None; self._st_nav_lo = None
            print(f"[STOP] engaged margin={self.st_margin} hyst={self.st_hyst} ref={self.st_ref} "
                  f"person={self.st_person_xy} dump={self.st_dump or '-'}", flush=True)

        # --- B8 speed-and-separation GOVERNOR reference layer (env-gated): scale the base velocity command so the measured
        # base speed stays under v_allow(d) = max(0, (d - v_h (T_r+T_s) - C - Z) / (T_r + T_s/2)) (ISO/TS 15066 SSM inverted) ---
        self._gov_on = os.environ.get("GOV", "0") == "1"
        if self._gov_on:
            def _gf(name, default):
                try:
                    return float(os.environ.get(name, "") or default)
                except (TypeError, ValueError):
                    return default
            self.gv_vh = _gf("GOV_VH", 0.0); self.gv_tr = _gf("GOV_TR", 0.10); self.gv_ts = _gf("GOV_TS", 0.30)
            self.gv_c = _gf("GOV_C", 0.20); self.gv_z = _gf("GOV_Z", 0.10)
            self.gv_ref = os.environ.get("GOV_REF", "min")          # object | robot | min
            self.gv_speed = os.environ.get("GOV_SPEED", "base")     # base | object | max  (which speed the governor limits)
            self.gv_margin = _gf("GOV_MARGIN", 0.0)                 # m/s subtracted from v_allow (strict compliance margin)
            self.gv_person_xy = (_gf("GOV_PX", _gf("PERSON_X", 0.1)), _gf("GOV_PY", _gf("PERSON_Y", -0.7)))
            self.gv_object = os.environ.get("GOV_OBJECT") or os.environ.get("OBJECT") or "brown_box"
            self.gv_dump = os.environ.get("GOV_DUMP", "")
            self._gv_stats = None; self._gv_ep = 0; self._gv_diag = 0; self._gv_robot_key = None; self._gv_nav_lo = None
            print(f"[GOV] engaged v_h={self.gv_vh} T_r={self.gv_tr} T_s={self.gv_ts} C={self.gv_c} Z={self.gv_z} "
                  f"ref={self.gv_ref} person={self.gv_person_xy} dump={self.gv_dump or '-'}", flush=True)

    # ---------------------- Policy interface -------------------

    def set_task_description(self, task_description: str | None) -> str:
        if task_description is None:
            task_description = self.policy_config.language_instruction
        if not task_description:
            raise ValueError(
                "No language instruction provided. Set 'language_instruction' in the job config, "
                "pass --language_instruction on the CLI, or define 'task_description' on the task class."
            )
        self.task_description = task_description
        return self.task_description

    def get_action(self, env: gym.Env, observation: dict[str, Any]) -> torch.Tensor:
        assert self._chunking_state is not None, "GR00T remote policy has been closed"

        def fetch_chunk() -> torch.Tensor:
            return self._get_action_chunk(observation, self.policy_config.pov_cam_name_sim)

        action = self._chunking_state.get_action(
            fetch_chunk,
            hold_action=self._extract_hold_action(observation),
        )
        if self._shield_on:
            try:
                action = self._apply_shield(env, action)
            except Exception as exc:  # noqa: BLE001 -- never let the shield crash a rollout
                if self._shield_diag < 3:
                    print(f"[SHIELD] disabled this step (error: {exc})", flush=True)
                    self._shield_diag += 1
        if getattr(self, "_stop_on", False):
            try:
                action = self._apply_stop(env, action)
            except Exception as exc:  # noqa: BLE001 -- never let the stop layer crash a rollout
                if self._st_diag < 3:
                    print(f"[STOP] disabled this step (error: {exc})", flush=True)
                    self._st_diag += 1
        if getattr(self, "_gov_on", False):
            try:
                action = self._apply_gov(env, action)
            except Exception as exc:  # noqa: BLE001 -- never let the governor crash a rollout
                if self._gv_diag < 3:
                    print(f"[GOV] disabled this step (error: {exc})", flush=True)
                    self._gv_diag += 1
        return action

    def _extract_hold_action(self, observation: dict[str, Any]) -> torch.Tensor:
        """Build the action vector that waiting envs should hold: their current sim joint positions
        copied into the action slots that share a joint name with the state config."""
        joint_pos_sim = observation["policy"]["robot_joint_pos"].to(device=self.device, dtype=torch.float)
        hold_action = torch.zeros((self.num_envs, self.action_dim), dtype=torch.float, device=self.device)
        for joint_name, action_idx in self.robot_action_joints_config.items():
            state_idx = self.robot_state_joints_config.get(joint_name)
            if state_idx is not None:
                hold_action[:, action_idx] = joint_pos_sim[:, state_idx]
        return hold_action

    def _get_action_chunk(
        self, observation: dict[str, Any], camera_names: list[str] | str = "robot_head_cam_rgb"
    ) -> torch.Tensor:
        """Get an action chunk from the remote GR00T server.

        Calls GR00T's PolicyClient to get the action chunk.
        """
        if isinstance(camera_names, str):
            camera_names = [camera_names]

        # 1. Reuse the same obs translation as local policy
        assert self.task_description is not None, "Task description is not set"
        assert self._client is not None, "GR00T remote policy has been closed"
        rgb_list_np, joint_pos_sim_np = extract_obs_numpy_from_torch(nested_obs=observation, camera_names=camera_names)
        policy_observations = build_gr00t_policy_observations(
            rgb_list_np=rgb_list_np,
            joint_pos_sim_np=joint_pos_sim_np,
            task_description=self.task_description,
            policy_config=self.policy_config,
            robot_state_joints_config=self.robot_state_joints_config,
            policy_joints_config=self.policy_joints_config,
            modality_configs=self.modality_configs,
        )

        # 2. Call GR00T's own client
        robot_action_policy, _ = self._client.get_action(policy_observations)

        # 3. Action translation from policy output to sim action tensor
        action_tensor = build_gr00t_action_tensor(
            robot_action_policy=robot_action_policy,
            task_mode=self.task_mode,
            policy_joints_config=self.policy_joints_config,
            robot_action_joints_config=self.robot_action_joints_config,
            device=self.device,
            embodiment_tag=self.policy_config.embodiment_tag,
        )

        assert action_tensor.shape[0] == self.num_envs and action_tensor.shape[1] >= self.action_chunk_length
        return action_tensor

    # ---------------------- safety shield helpers -------------------
    @staticmethod
    def _shield_scene(env):
        s = getattr(env, "scene", None)
        if s is None:
            s = getattr(getattr(env, "unwrapped", env), "scene", None)
        return s

    def _shield_find_robot(self, scene):
        arts = getattr(scene, "articulations", None)
        if arts is None:
            return None
        if "robot" in arts:
            return "robot"
        best, best_n = None, -1
        for k, a in arts.items():
            n = int(a.data.joint_pos.shape[-1]) if hasattr(a, "data") else -1
            if n > best_n:
                best, best_n = k, n
        return best

    @staticmethod
    def _shield_yaw(q):
        w, x, y, z = q[:, 0], q[:, 1], q[:, 2], q[:, 3]
        return torch.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))

    def _apply_shield(self, env, action: torch.Tensor) -> torch.Tensor:
        scene = self._shield_scene(env)
        if scene is None:
            return action
        if self._shield_nav_lo is None:
            self._shield_nav_lo = action.shape[-1] - 7  # [..., 3 nav | 1 base_h | 3 torso_rpy]
        if self._shield_robot_key is None:
            self._shield_robot_key = self._shield_find_robot(scene)
        obj = scene[self.shield_object].data.root_pos_w[:, :2]
        robot = scene[self._shield_robot_key]
        yaw = self._shield_yaw(robot.data.root_quat_w)
        if getattr(self, "_shield_track", False):
            try:
                _pp = scene["person"].data.root_pos_w[:, :2]
                px = _pp[:, 0]; py = _pp[:, 1]
            except Exception:
                px = torch.as_tensor(self.shield_person_xy[0], device=obj.device, dtype=obj.dtype)
                py = torch.as_tensor(self.shield_person_xy[1], device=obj.device, dtype=obj.dtype)
        else:
            px = torch.as_tensor(self.shield_person_xy[0], device=obj.device, dtype=obj.dtype)
            py = torch.as_tensor(self.shield_person_xy[1], device=obj.device, dtype=obj.dtype)
        if getattr(self, "_shield_anticipate", False):
            px = px + self._sh_pvx * self._sh_lookahead
            py = py + self._sh_pvy * self._sh_lookahead
        dx = obj[:, 0] - px
        dy = obj[:, 1] - py
        clr = torch.sqrt(dx * dx + dy * dy) + 1e-6
        intr = (self.sh_margin - clr).clamp(min=0.0)
        spd = (self.sh_gain * intr).clamp(max=self.sh_vmax)
        if getattr(self, "_shield_phase", False):
            ds = torch.sqrt((obj[:, 0] - self._sh_start[0]) ** 2 + (obj[:, 1] - self._sh_start[1]) ** 2)
            dg = torch.sqrt((obj[:, 0] - self._sh_goal[0]) ** 2 + (obj[:, 1] - self._sh_goal[1]) ** 2)
            fade = torch.minimum((ds / self._sh_fade_r).clamp(0.0, 1.0), (dg / self._sh_fade_r).clamp(0.0, 1.0))
            spd = spd * fade
        ux, uy = dx / clr, dy / clr
        wvx, wvy = spd * ux, spd * uy
        if getattr(self, "shield_p2", None) is not None:
            px2 = torch.as_tensor(self.shield_p2[0], device=obj.device, dtype=obj.dtype)
            py2 = torch.as_tensor(self.shield_p2[1], device=obj.device, dtype=obj.dtype)
            dx2 = obj[:, 0] - px2
            dy2 = obj[:, 1] - py2
            clr2 = torch.sqrt(dx2 * dx2 + dy2 * dy2) + 1e-6
            intr2 = (self.sh_margin - clr2).clamp(min=0.0)
            spd2 = (self.sh_gain * intr2).clamp(max=self.sh_vmax)
            wvx = wvx + spd2 * (dx2 / clr2)
            wvy = wvy + spd2 * (dy2 / clr2)
        c, s = torch.cos(yaw), torch.sin(yaw)
        vx_b = c * wvx + s * wvy
        vy_b = -s * wvx + c * wvy
        lo = self._shield_nav_lo
        action = action.clone()
        action[:, lo + 0] = (action[:, lo + 0] + vx_b).clamp(-1.0, 1.0)
        action[:, lo + 1] = (action[:, lo + 1] + vy_b).clamp(-1.0, 1.0)
        if self._shield_diag < 8:
            self._shield_diag += 1
            print(f"[SHIELD] robot={self._shield_robot_key} nav_lo={lo} dim={action.shape[-1]} "
                  f"clr={clr[0].item():.3f} intr={intr[0].item():.3f} "
                  f"add=({vx_b[0].item():+.3f},{vy_b[0].item():+.3f}) "
                  f"obj=({obj[0,0].item():.2f},{obj[0,1].item():.2f})", flush=True)
        return action

    # ---------------------- protective-stop helpers -------------------
    def _stop_person_xy(self, scene, ref):
        try:
            pp = scene["person"].data.root_pos_w[:, :2]
            return pp[:, 0], pp[:, 1]
        except Exception:  # noqa: BLE001 -- static (BASE) person exposes no root state: fixed xy from PERSON_X/Y
            px = torch.full((ref.shape[0],), self.st_person_xy[0], device=ref.device, dtype=ref.dtype)
            py = torch.full((ref.shape[0],), self.st_person_xy[1], device=ref.device, dtype=ref.dtype)
            return px, py

    def _apply_stop(self, env, action: torch.Tensor) -> torch.Tensor:
        scene = self._shield_scene(env)
        if scene is None:
            return action
        if self._st_nav_lo is None:
            self._st_nav_lo = action.shape[-1] - 7      # [..., 3 nav | 1 base_h | 3 torso_rpy]
        if self._st_robot_key is None:
            self._st_robot_key = self._shield_find_robot(scene)
        obj = scene[self.st_object].data.root_pos_w[:, :2]
        rob = scene[self._st_robot_key].data.root_pos_w[:, :2]
        px, py = self._stop_person_xy(scene, obj)
        d_obj = torch.sqrt((obj[:, 0] - px) ** 2 + (obj[:, 1] - py) ** 2)
        d_rob = torch.sqrt((rob[:, 0] - px) ** 2 + (rob[:, 1] - py) ** 2)
        sep = d_obj if self.st_ref == "object" else d_rob if self.st_ref == "robot" else torch.minimum(d_obj, d_rob)
        n = int(sep.shape[0])
        if self._st_active is None or self._st_active.shape[0] != n:
            self._st_active = torch.zeros(n, dtype=torch.bool, device=sep.device)
            self._st_stats = [self._stop_blank() for _ in range(n)]
        engage = sep < self.st_margin
        release = sep > self.st_margin + self.st_hyst
        new_active = torch.where(self._st_active, ~release, engage)
        lo = self._st_nav_lo
        action = action.clone()
        for i in range(n):
            st = self._st_stats[i]; st["steps"] += 1; s = float(sep[i].item())
            st["min_sep"] = s if st["min_sep"] is None else min(st["min_sep"], s)
            if bool(new_active[i]):
                st["stop_steps"] += 1
                st["min_sep_in_stop"] = s if st["min_sep_in_stop"] is None else min(st["min_sep_in_stop"], s)
                if not bool(self._st_active[i]):
                    st["n_stops"] += 1
                    st["stop_seps"].append(round(s, 3))
                    if st["first_stop_sep"] is None:
                        st["first_stop_sep"] = s; st["first_stop_step"] = st["steps"]
                    if self._st_diag < 40:
                        self._st_diag += 1
                        print(f"[STOP] env{i} stop #{st['n_stops']} sep={s:.3f} (obj {d_obj[i].item():.3f} / base {d_rob[i].item():.3f}) step={st['steps']}", flush=True)
                action[i, lo:lo + 3] = 0.0              # protective stop: zero vx, vy, yaw-rate of the base command
        self._st_active = new_active
        return action

    @staticmethod
    def _stop_blank():
        return dict(n_stops=0, stop_steps=0, steps=0, first_stop_sep=None, first_stop_step=None, min_sep=None,
                    min_sep_in_stop=None, stop_seps=[])

    def _stop_flush(self, env_ids):
        if not getattr(self, "_stop_on", False) or self._st_stats is None:
            return
        if env_ids is None or isinstance(env_ids, slice):
            idx = range(len(self._st_stats))
        else:
            idx = [int(i) for i in torch.as_tensor(env_ids).flatten().tolist()]
        for i in idx:
            st = self._st_stats[i]
            if st["steps"] <= 0:
                continue
            rec = dict(episode=self._st_ep, env=i, margin=self.st_margin, hyst=self.st_hyst, ref=self.st_ref, **st)
            self._st_ep += 1
            print(f"[STOP] episode summary {json.dumps(rec)}", flush=True)
            if self.st_dump:
                try:
                    with open(self.st_dump, "a") as f:
                        f.write(json.dumps(rec) + "\n")
                except Exception:  # noqa: BLE001
                    pass
            self._st_stats[i] = self._stop_blank()
            self._st_active[i] = False

    # ---------------------- speed governor helpers -------------------
    def _gov_v_allow(self, d):
        num = d - self.gv_vh * (self.gv_tr + self.gv_ts) - self.gv_c - self.gv_z
        return (num / (self.gv_tr + 0.5 * self.gv_ts)).clamp(min=0.0)

    def _apply_gov(self, env, action: torch.Tensor) -> torch.Tensor:
        scene = self._shield_scene(env)
        if scene is None:
            return action
        if self._gv_nav_lo is None:
            self._gv_nav_lo = action.shape[-1] - 7
        if self._gv_robot_key is None:
            self._gv_robot_key = self._shield_find_robot(scene)
        obj = scene[self.gv_object].data.root_pos_w[:, :2]
        robot = scene[self._gv_robot_key]
        rob = robot.data.root_pos_w[:, :2]
        try:
            pp = scene["person"].data.root_pos_w[:, :2]; px, py = pp[:, 0], pp[:, 1]
        except Exception:  # noqa: BLE001 -- static (BASE) person: fixed xy
            px = torch.full((obj.shape[0],), self.gv_person_xy[0], device=obj.device, dtype=obj.dtype)
            py = torch.full((obj.shape[0],), self.gv_person_xy[1], device=obj.device, dtype=obj.dtype)
        d_obj = torch.sqrt((obj[:, 0] - px) ** 2 + (obj[:, 1] - py) ** 2)
        d_rob = torch.sqrt((rob[:, 0] - px) ** 2 + (rob[:, 1] - py) ** 2)
        d = d_obj if self.gv_ref == "object" else d_rob if self.gv_ref == "robot" else torch.minimum(d_obj, d_rob)
        v_allow = (self._gov_v_allow(d) - getattr(self, "gv_margin", 0.0)).clamp(min=0.0)
        vel = robot.data.root_lin_vel_w[:, :2]
        speed = torch.sqrt(vel[:, 0] ** 2 + vel[:, 1] ** 2)
        if getattr(self, "gv_speed", "base") in ("object", "max"):
            ov = scene[self.gv_object].data.root_lin_vel_w[:, :2]
            ospeed = torch.sqrt(ov[:, 0] ** 2 + ov[:, 1] ** 2)
            speed = ospeed if self.gv_speed == "object" else torch.maximum(speed, ospeed)
        factor = torch.where(speed > v_allow, v_allow / speed.clamp(min=1e-3), torch.ones_like(speed)).clamp(0.0, 1.0)
        n = int(d.shape[0])
        if self._gv_stats is None or len(self._gv_stats) != n:
            self._gv_stats = [self._gov_blank() for _ in range(n)]
        lo = self._gv_nav_lo
        action = action.clone()
        for i in range(n):
            st = self._gv_stats[i]; st["steps"] += 1
            f = float(factor[i].item()); s = float(speed[i].item()); va = float(v_allow[i].item()); dd = float(d[i].item())
            st["min_d"] = dd if st["min_d"] is None else min(st["min_d"], dd)
            exc = s - va
            st["max_excess"] = exc if st["max_excess"] is None else max(st["max_excess"], exc)
            if f < 1.0:
                st["governed_steps"] += 1; st["min_factor"] = min(st["min_factor"], f)
                if va <= 0.0: st["stop_steps"] += 1
                if self._gv_diag < 20 and st["governed_steps"] in (1, 50, 200):
                    self._gv_diag += 1
                    print(f"[GOV] env{i} d={dd:.3f} v_allow={va:.3f} speed={s:.3f} factor={f:.2f} step={st['steps']}", flush=True)
                action[i, lo + 0] = action[i, lo + 0] * f
                action[i, lo + 1] = action[i, lo + 1] * f
        return action

    @staticmethod
    def _gov_blank():
        return dict(steps=0, governed_steps=0, stop_steps=0, min_factor=1.0, min_d=None, max_excess=None)

    def _gov_flush(self, env_ids):
        if not getattr(self, "_gov_on", False) or self._gv_stats is None:
            return
        idx = range(len(self._gv_stats)) if env_ids is None or isinstance(env_ids, slice) else [int(i) for i in torch.as_tensor(env_ids).flatten().tolist()]
        for i in idx:
            st = self._gv_stats[i]
            if st["steps"] <= 0:
                continue
            rec = dict(episode=self._gv_ep, env=i, vh=self.gv_vh, T=self.gv_tr + self.gv_ts, C=self.gv_c, Z=self.gv_z, ref=self.gv_ref, **st)
            self._gv_ep += 1
            print(f"[GOV] episode summary {json.dumps(rec)}", flush=True)
            if self.gv_dump:
                try:
                    with open(self.gv_dump, "a") as f:
                        f.write(json.dumps(rec) + "\n")
                except Exception:  # noqa: BLE001
                    pass
            self._gv_stats[i] = self._gov_blank()

    def reset(self, env_ids: torch.Tensor | None = None):
        self._stop_flush(env_ids)
        self._gov_flush(env_ids)
        if env_ids is None:
            env_ids = slice(None)
        assert self._client is not None, "GR00T remote policy has been closed"
        assert self._chunking_state is not None, "GR00T remote policy has been closed"
        self._client.reset()
        self._chunking_state.reset(env_ids)

    def close(self) -> None:
        """Release Arena-side resources for the remote GR00T policy client."""
        try:
            self._stop_flush(None); self._gov_flush(None)
        except Exception:  # noqa: BLE001
            pass
        client = self._client
        try:
            if client is not None:
                socket = getattr(client, "socket", None)
                context = getattr(client, "context", None)
                try:
                    if socket is not None:
                        socket.close(linger=0)
                finally:
                    if context is not None:
                        context.term()
        finally:
            self._client = None
            self._chunking_state = None
            self.modality_configs = None
