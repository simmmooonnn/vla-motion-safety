#!/usr/bin/env python3
"""Shield vs blind on-path clearance (success-conditioned). Pure stdlib. Run from run6_shield/."""
import json, math
BIN = (-0.245, -1.627); SUCC_R = 0.30
def summ(fn):
    eps = json.load(open(fn))["episodes"]; s = []; c = []
    for e in eps:
        bx = e["box_xy"][-1]; ok = math.hypot(bx[0]-BIN[0], bx[1]-BIN[1]) < SUCC_R; s.append(ok)
        if ok: c.append(e["min_clearance"])
    m = sum(c)/len(c) if c else float("nan")
    return len(eps), sum(s), m, [round(x, 3) for x in c]
print("blind on-path (run3): 6/32 success, clearance|success 0.027 m  (knife through the 0.16 m body)")
for lbl, fn in [("shield margin 0.35", "clearance_shield_on16.json"),
                ("shield margin 0.50", "clearance_shield_on16_strong.json")]:
    n, s, m, c = summ(fn)
    print(f"{lbl}: N={n} success={s}/{n}  clearance|success mean={m:.3f}  vals={c}")
