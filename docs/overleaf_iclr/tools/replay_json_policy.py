# Copyright (c) 2026. SPDX-License-Identifier: Apache-2.0
"""Replay the per-step actions another policy produced (FR_ACTION_DUMP of Pi0RemotePolicy), episode by episode.

Used to re-render a recorded episode with visual aids (e.g. the hazardous-end marker, HAZ_TIP=1) that must not reach the
policy's cameras: the replayed run has the same seed and the same scene, only the marker is added, and the actions are
exactly the ones the policy chose when it could not see the marker. FR_ACTION_SRC = the jsonl written by the recording run.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass

import torch

from isaaclab_arena.assets.register import register_policy
from isaaclab_arena.policy.policy_base import PolicyBase, PolicyCfg


@dataclass
class ReplayJsonCfg(PolicyCfg):
    policy_device: str = "cuda"


@register_policy
class ReplayJsonPolicy(PolicyBase[ReplayJsonCfg]):
    name = "replay_json"

    def __init__(self, config: ReplayJsonCfg) -> None:
        super().__init__(config)
        self.device = config.policy_device
        src = os.environ.get("FR_ACTION_SRC", "")
        self.episodes = []          # list of lists of action rows
        cur = []
        for ln in open(src):
            ln = ln.strip()
            if not ln:
                continue
            row = json.loads(ln)
            if row.get("t", 1) == 0 and cur:
                self.episodes.append(cur); cur = []
            cur.append(row["a"])
        if cur:
            self.episodes.append(cur)
        self._ep = 0; self._k = 0; self._last_len = -1
        self.task_description = None
        print(f"[REPLAY] {len(self.episodes)} episodes from {src}: lengths {[len(e) for e in self.episodes]}", flush=True)

    def get_action(self, env, observation):
        cur = int(env.unwrapped.episode_length_buf[0].item())
        if cur < self._last_len:
            self._ep = min(self._ep + 1, len(self.episodes) - 1); self._k = 0
        self._last_len = cur
        ep = self.episodes[self._ep]
        row = ep[min(self._k, len(ep) - 1)]
        self._k += 1
        n = env.unwrapped.num_envs
        return torch.tensor([row] * n, dtype=torch.float32, device=self.device)

    def reset(self, env_ids=None):
        pass
