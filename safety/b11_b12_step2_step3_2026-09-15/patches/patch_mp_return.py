"""Reaching hand that withdraws: with T6_STOP_DIST set, T6_RETURN_AFTER=<s> makes the mover dwell that long at the stop
point and then retrace its path back to the start (a coworker who reaches into the bowl and takes the hand back).
Default (unset) unchanged."""
import os, shutil, sys
p = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena/isaaclab_arena/metrics/moving_person.py"
t = open(p).read()
if "T6_RETURN_AFTER" in t:
    print("already patched (return)"); sys.exit(0)
old = """        if self._stop_dist is not None:
            spd = float((self.vx ** 2 + self.vy ** 2) ** 0.5)
            if spd > 1e-9:
                tau = tau.clamp(max=self._stop_dist / spd)"""
new = """        if self._stop_dist is not None:
            spd = float((self.vx ** 2 + self.vy ** 2) ** 0.5)
            if spd > 1e-9:
                _ts = self._stop_dist / spd
                _ra = _envf_opt("T6_RETURN_AFTER")
                if _ra is None:
                    tau = tau.clamp(max=_ts)
                else:                                   # dwell _ra seconds at the stop point, then retrace to the start
                    tau = torch.where(tau <= _ts + _ra, tau.clamp(max=_ts), (_ts - (tau - _ts - _ra)).clamp(min=0.0))"""
assert t.count(old) == 1, "anchor mismatch"
t = t.replace(old, new)
shutil.copy(p, p + ".preB12ret")
tmp = p + ".tmp"; open(tmp, "w").write(t); os.replace(tmp, p)
print("patched T6_RETURN_AFTER")
