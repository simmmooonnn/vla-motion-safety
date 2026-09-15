"""FR_STOP: flush the per-episode stop statistics when the episode clock restarts (the runner does not call reset() per
episode). Applies on top of patch_pi0_stop.py."""
import os, shutil, sys
p = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena/isaaclab_arena_openpi/policy/pi0_remote_policy.py"
t = open(p).read()
if "_st_flush" in t:
    print("already patched (flush)"); sys.exit(0)
old = """    def _apply_fr_stop(self, env, observation, action):
        import torch, warp as wp
        sc = env.unwrapped.scene"""
new = """    def _st_flush(self):
        if self._st_n and self._st_dump:
            import json
            with open(self._st_dump, "a") as fh:
                fh.write(json.dumps({"fires": self._st_fires, "stopped_steps": self._st_steps, "steps": self._st_n,
                                     "min_gap": round(self._st_min, 4)}) + "\\n")
        self._st_steps = 0; self._st_fires = 0; self._st_n = 0; self._st_min = 9.0; self._st_on = None

    def _apply_fr_stop(self, env, observation, action):
        import torch, warp as wp
        buf = getattr(env.unwrapped, "episode_length_buf", None)
        if buf is not None:
            cur = int(buf[0].item())
            if cur < getattr(self, "_st_last", -1):
                self._st_flush()                       # a new episode started: write the previous one
            self._st_last = cur
        sc = env.unwrapped.scene"""
old2 = """    def reset(self, env_ids=None):
        if getattr(self, "_fr_stop", False) and self._st_n:
            if self._st_dump:
                import json
                with open(self._st_dump, "a") as fh:
                    fh.write(json.dumps({"fires": self._st_fires, "stopped_steps": self._st_steps, "steps": self._st_n,
                                         "min_gap": round(self._st_min, 4)}) + "\\n")
            self._st_steps = 0; self._st_fires = 0; self._st_n = 0; self._st_min = 9.0; self._st_on = None
        return super().reset(env_ids)"""
new2 = """    def reset(self, env_ids=None):
        if getattr(self, "_fr_stop", False):
            self._st_flush()
        return super().reset(env_ids)

    def __del__(self):
        try:
            if getattr(self, "_fr_stop", False):
                self._st_flush()
        except Exception:  # noqa: BLE001
            pass"""
assert t.count(old) == 1 and t.count(old2) == 1, "anchor mismatch"
t = t.replace(old, new).replace(old2, new2)
shutil.copy(p, p + ".preB12flush")
tmp = p + ".tmp"; open(tmp, "w").write(t); os.replace(tmp, p)
print("patched per-episode flush")
