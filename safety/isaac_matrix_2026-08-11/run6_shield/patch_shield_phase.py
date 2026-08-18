#!/usr/bin/env python3
"""Add an OPTIONAL phase-aware fade to the (already-folded-in) shield in the base
remote policy. Gated by env SHIELD_PHASE=1 (default off → no behaviour change).

Rationale: fade the repulsive push to zero within SHIELD_FADE_R of the grasp START
(box origin) and of the GOAL (bin), so the push acts only during free transit and never
perturbs the pick or the place. On the G1 bystander task the margin gate already spares
grasp/placement when the person is mid-corridor, so this mainly hardens the shield for
scenarios where the bystander sits near the shelf or the bin.

Idempotent: no-op if already applied. Run with the arena venv python on ARCH."""
import sys

F = "/weka/scratch/aszalay1/zijian/arena/IsaacLab-Arena/isaaclab_arena_gr00t/policy/gr00t_remote_closedloop_policy.py"
src = open(F, encoding="utf-8").read()

if "_shield_phase" in src:
    print("phase-aware already applied; nothing to do"); sys.exit(0)
assert "[SHIELD] engaged" in src, "base shield not present — apply patch_shield.py first"

# 1. init: parse phase-aware params inside the SHIELD block
a1 = '            self.shield_object = os.environ.get("SHIELD_OBJECT") or os.environ.get("OBJECT") or "brown_box"\n'
assert src.count(a1) == 1, "init object anchor not found"
init_add = a1 + '''            self._shield_phase = os.environ.get("SHIELD_PHASE", "0") == "1"
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
'''
src = src.replace(a1, init_add)

# 2. _apply_shield: fade the speed near grasp/goal
a2 = "        spd = (self.sh_gain * intr).clamp(max=self.sh_vmax)\n"
assert src.count(a2) == 1, "apply spd anchor not found"
a2_add = a2 + '''        if getattr(self, "_shield_phase", False):
            ds = torch.sqrt((obj[:, 0] - self._sh_start[0]) ** 2 + (obj[:, 1] - self._sh_start[1]) ** 2)
            dg = torch.sqrt((obj[:, 0] - self._sh_goal[0]) ** 2 + (obj[:, 1] - self._sh_goal[1]) ** 2)
            fade = torch.minimum((ds / self._sh_fade_r).clamp(0.0, 1.0), (dg / self._sh_fade_r).clamp(0.0, 1.0))
            spd = spd * fade
'''
src = src.replace(a2, a2_add)

open(F, "w", encoding="utf-8").write(src)
print("PHASE-AWARE PATCHED", F)
