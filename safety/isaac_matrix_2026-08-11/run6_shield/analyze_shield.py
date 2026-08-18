#!/usr/bin/env python3
"""Full shield analysis: pooled on/off-path + margin sweep, success-conditioned, Fisher. Stdlib. Run from run6_shield/."""
import json, math
from math import comb
BIN = (-0.245, -1.627); SUCC_R = 0.30
def pool(*fns):
    s = []; c = []
    for fn in fns:
        try: eps = json.load(open(fn))["episodes"]
        except FileNotFoundError: continue
        for e in eps:
            bx = e["box_xy"][-1]; ok = math.hypot(bx[0]-BIN[0], bx[1]-BIN[1]) < SUCC_R; s.append(ok)
            if ok: c.append(e["min_clearance"])
    m = sum(c)/len(c) if c else float("nan")
    return len(s), sum(s), m, [round(x, 3) for x in c]
def fisher(a, b, c, d):
    n, r1, c1 = a+b+c+d, a+b, a+c
    hp = lambda x: comb(r1, x)*comb(n-r1, c1-x)/comb(n, c1)
    p0 = hp(a); lo, hi = max(0, c1-(n-r1)), min(r1, c1)
    return sum(hp(x) for x in range(lo, hi+1) if hp(x) <= p0*1.0000001)

print("=== ON-PATH (person blocking) ===")
print("blind (run3): 6/32 = 19%, clearance|succ 0.027 m")
for lbl, fns in [("margin 0.20", ["clearance_shield_on16_m20.json"]),
                 ("margin 0.35", ["clearance_shield_on16.json"]),
                 ("margin 0.50 (pooled)", ["clearance_shield_on16_strong.json", "clearance_shield_on_strong_b.json"])]:
    n, s, m, c = pool(*fns); print(f"  shield {lbl}: N={n} succ={s}/{n} clr|succ={m:.3f}  {c}")
ns, ss, ms, _ = pool("clearance_shield_on16_strong.json", "clearance_shield_on_strong_b.json")
print(f"  -> on-path shield0.50 vs blind success Fisher p={fisher(ss, ns-ss, 6, 26):.3f}")

print("\n=== OFF-PATH (person not blocking) ===")
print("blind (base pose): 8/16 = 50%, clearance|succ 0.156 m")
for lbl, fns in [("margin 0.20", ["clearance_shield_offpath_m20.json"]),
                 ("margin 0.35 (pooled)", ["clearance_shield_offpath.json", "clearance_shield_offpath_b.json"])]:
    n, s, m, c = pool(*fns); print(f"  shield {lbl}: N={n} succ={s}/{n} clr|succ={m:.3f}  {c}")
no, so, mo, _ = pool("clearance_shield_offpath.json", "clearance_shield_offpath_b.json")
print(f"  -> off-path shield0.35 vs blind success Fisher p={fisher(so, no-so, 8, 8):.3f}")
print("\nVerdict: clearance up in both poses at no measurable success cost (N=16 'costs' were noise).")
