#!/usr/bin/env python3
"""Visual-twin analysis: pool per-object dumps, uniform success + clearance|success,
Fisher-exact tests. Pure stdlib (no scipy). Run from run4_visual/."""
import json, math, glob, os
from math import comb

BIN = (-0.245, -1.627)          # blue-bin destination xy (env cfg)
SUCC_R = 0.30                   # success = box final xy within 0.30 m of bin

def summarize(fn):
    d = json.load(open(fn))
    eps = d["episodes"]
    succ, clr = [], []
    for e in eps:
        bx = e["box_xy"][-1]
        ok = math.hypot(bx[0]-BIN[0], bx[1]-BIN[1]) < SUCC_R
        succ.append(ok)
        if ok:
            clr.append(e["min_clearance"])
    return len(eps), sum(succ), clr

def fisher2(a, b, c, d):
    """two-sided Fisher exact p for [[a,b],[c,d]] (rows succ/fail)."""
    n, r1, c1 = a+b+c+d, a+b, a+c
    hp = lambda x: comb(r1, x)*comb(n-r1, c1-x)/comb(n, c1)
    p0 = hp(a); lo, hi = max(0, c1-(n-r1)), min(r1, c1)
    return sum(hp(x) for x in range(lo, hi+1) if hp(x) <= p0*1.0000001)

GROUPS = {  # object -> list of dump files pooled
    "box":      ["clearance_visual_box.json", "clearance_visual_box2.json"],
    "scissors": ["clearance_visual_scissors.json", "clearance_visual_scissors2.json",
                 "clearance_visual_scissors3.json"],
    "spoon":    ["clearance_visual_spoon.json", "clearance_visual_spoon2.json",
                 "clearance_visual_spoon3.json"],   # spoon3 optional
}

pooled = {}
for obj, files in GROUPS.items():
    N = S = 0; cl = []
    for f in files:
        if not os.path.exists(f):
            continue
        n, s, c = summarize(f)
        N += n; S += s; cl += c
    pooled[obj] = (S, N, cl)
    mc = f"{sum(cl)/len(cl):.3f}" if cl else "--"
    print(f"{obj:9s} {S:2d}/{N:<2d} = {100*S/N:4.1f}%   clearance|succ={mc} (n={len(cl)})")

print()
bs, bn, _ = pooled["box"]
for obj in ("scissors", "spoon"):
    s, n, _ = pooled[obj]
    print(f"box({bs}/{bn}) vs {obj}({s}/{n}): Fisher p={fisher2(bs, bn-bs, s, n-s):.4f}")
ss, sn, _ = pooled["scissors"]; ps, pn, _ = pooled["spoon"]
print(f"scissors({ss}/{sn}) vs spoon({ps}/{pn}): Fisher p={fisher2(ss, sn-ss, ps, pn-ps):.4f}")
nbs, nbn = ss+ps, sn+pn
print(f"box({bs}/{bn}) vs nonbox({nbs}/{nbn}): Fisher p={fisher2(bs, bn-bs, nbs, nbn-nbs):.4f}")
