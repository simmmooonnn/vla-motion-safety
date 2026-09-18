# Copyright (c) 2026. SPDX-License-Identifier: Apache-2.0
"""A visual marker that follows the hazardous end of the carried object (figures and the demo reel).

The object's hazardous axis (the same one analyze_fr scores for T3) is a column of its rotation; the tip is the object
centre plus that axis times half the object's length. Every sim step this recorder writes a small kinematic sphere to
that point, so a viewer can see which way the blade or the tines point. It records the tip as well. No collider, no
effect on any measurement.
"""
import torch
import warp as wp

from isaaclab.managers.recorder_manager import RecorderTerm, RecorderTermCfg
from isaaclab.utils.configclass import configclass
from isaaclab.utils.math import quat_apply

AX = {"x+": (0, 1.0), "x-": (0, -1.0), "y+": (1, 1.0), "y-": (1, -1.0), "z+": (2, 1.0), "z-": (2, -1.0)}


def _t(x):
    return x if torch.is_tensor(x) else wp.to_torch(x)


class HazardTipRecorder(RecorderTerm):
    def __init__(self, cfg, env):
        super().__init__(cfg, env)
        self.object_name, self.marker_name = cfg.object_name, cfg.marker_name
        i, s = AX[cfg.axis]
        v = [0.0, 0.0, 0.0]
        v[i] = s * cfg.half
        self._v = torch.tensor(v, device=env.device, dtype=torch.float32).unsqueeze(0)
        self.name = "hazard_tip"
        self._err = 0

    def record_post_step(self):
        env = self._env
        try:
            obj = env.scene[self.object_name]
            pos = _t(obj.data.root_pos_w).to(torch.float32)
            quat = _t(obj.data.root_quat_w).to(torch.float32)          # (w, x, y, z)
            tip = pos + quat_apply(quat, self._v.expand(pos.shape[0], -1))
            mk = env.scene[self.marker_name]
            ident = torch.tensor([[1.0, 0.0, 0.0, 0.0]], device=tip.device).expand(pos.shape[0], -1)
            mk.write_root_pose_to_sim(torch.cat([tip, ident], dim=-1))
            mk.write_root_velocity_to_sim(torch.zeros(pos.shape[0], 6, device=tip.device))
            return self.name, tip.clone()
        except Exception as exc:  # noqa: BLE001
            if self._err < 3:
                self._err += 1
                print(f"[HAZ_TIP] marker skipped this step: {exc!r}", flush=True)
            return None, None


@configclass
class HazardTipRecorderCfg(RecorderTermCfg):
    class_type: type[RecorderTerm] = HazardTipRecorder
    object_name: str = ""
    marker_name: str = "haz_tip"
    axis: str = "y+"
    half: float = 0.06
