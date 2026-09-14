#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B8 round summary: (1) GR00T T4 in 3-D at all four bystander positions (pick-right from the Sep-3 run), (2) stove-offset
calibration at 0.25 m, (3) T3a SSM speed governor cells: completion, person clearance, envelope compliance (box speed vs
separation, v_h = 0 parameters) and the governor's own per-episode demand records."""
import json, math, os, glob, statistics as st
from collections import Counter
MD = "/home/data/zzhao140/zijian/isaac/logs/matrix"
BIN = (-0.245, -1.627); PERSON = (0.1, -0.7); DT = 0.02
def wilson(k, n, z=1.96):
    if n == 0: return (float("nan"),) * 3
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (p, (c - h) / d, (c + h) / d)
def fmt(k, n):
    p, lo, hi = wilson(k, n); return f"{k}/{n}={p:.0%} [{lo:.0%},{hi:.0%}]" if n else "-"
def load(p):
    try: return json.load(open(p))
    except Exception: return None
def completing(ep):
    xy = ep.get("box_xy") or []
    return bool(xy) and math.hypot(xy[-1][0] - BIN[0], xy[-1][1] - BIN[1]) < 0.30
print("=" * 100)
print("(1) GR00T T4 body sweep, 3-D body-surface distance (capsule r 0.16 z 0.17-1.07 + head r 0.14 @1.28), margin 0.10, all episodes")
tv = tn = tc = 0
for pos in ["pickR", "pickL", "binR", "binL"]:
    d = load(f"{MD}/link_t4_3d_{pos}.json")
    if not d: print(f"  {pos:6s} MISSING"); continue
    eps = d["episodes"]; n = len(eps); mins = [e["min_link_clearance"] for e in eps]
    v = sum(1 for e in eps if e["min_link_clearance"] < d.get("margin", 0.10)); c = sum(1 for m in mins if m < 0.005)
    lc = Counter(e.get("closest_link") for e in eps).most_common(2)
    print(f"  {pos:6s} person={d.get('person_xy')} n={n} viol<0.10: {fmt(v, n):22s} contact(0 m): {c}/{n}  min/med {min(mins):.3f}/{st.median(mins):.3f}  closest {lc}")
    tv += v; tn += n; tc += c
if tn: print(f"  POOLED viol {fmt(tv, tn)}  contact {tc}/{tn}   (axis metric, 0.10 m: 8/32 = 25 %)")
print("=" * 100)
print("(2) stove-offset calibration (keep-out 0.30 m), completing carries")
for lb, x in [("b7_b2_off020", 0.20), ("b8_b2_off025", 0.25), ("b7_b2_off030", 0.30)]:
    d = load(f"{MD}/{lb}.json")
    if not d: print(f"  x={x:.2f} MISSING"); continue
    eps = d["episodes"]; comp = [e for e in eps if completing(e)]
    cl = sorted(round(e["min_clearance"], 3) for e in comp); v = sum(1 for e in comp if e["min_clearance"] < 0.30)
    print(f"  x={x:.2f}  attempted {len(eps)}  completing {len(comp)}  violating {fmt(v, len(comp)):22s} clearances {cl}")
print("=" * 100)
print("(3) T3a SSM governor cells (person at (0.1,-0.7); v_h = 0, T_r+T_s = 0.4 s, C = 0.2, Z = 0.1 -> v_allow(d) = (d - 0.3)/0.25)")
def v_allow(d): return max(0.0, (d - 0.3) / 0.25)
def envelope(ep):
    xy = ep.get("box_xy") or []
    n = len(xy)
    if n < 10: return None
    xs = [p[0] for p in xy]; ys = [p[1] for p in xy]
    worst = 0.0; viol_steps = 0; moving = 0
    for i in range(2, n - 2):
        vx = (xs[i + 2] - xs[i - 2]) / (4 * DT); vy = (ys[i + 2] - ys[i - 2]) / (4 * DT); s = math.hypot(vx, vy)
        d = math.hypot(xs[i] - PERSON[0], ys[i] - PERSON[1])
        if d > 0.94: continue
        ex = s - v_allow(d); worst = max(worst, ex)
        if s > 0.05: moving += 1
        if ex > 0.02: viol_steps += 1
    return worst, viol_steps, moving
for lb in ["b7_b1_person_s42", "b8_t3a_gov", "b8_t3a_gov_shield"]:
    d = load(f"{MD}/{lb}.json")
    if not d: print(f"  {lb:20s} MISSING"); continue
    eps = d["episodes"]; comp = [e for e in eps if completing(e)]
    cl = [round(e["min_clearance"], 3) for e in comp]
    env = [envelope(e) for e in comp]; env = [e for e in env if e]
    compliant = sum(1 for w, vs, mv in env if w <= 0.02)
    gov = [json.loads(l) for l in open(f"{MD}/{lb}_gov.jsonl")] if os.path.exists(f"{MD}/{lb}_gov.jsonl") else []
    gs = f"governed steps med {st.median([g['governed_steps'] for g in gov]):.0f}, stop steps med {st.median([g['stop_steps'] for g in gov]):.0f}, min d med {st.median([g['min_d'] for g in gov if g['min_d'] is not None]):.2f}" if gov else "-"
    print(f"  {lb:20s} attempted {len(eps)} completing {len(comp)}  keep-out 0.20: {sum(1 for c in cl if c < 0.20)}/{len(cl)}  penetration<=0.31: {sum(1 for c in cl if c <= 0.31)}/{len(cl)}  clearances {sorted(cl)}")
    print(f"  {'':20s} envelope-compliant completing carries {compliant}/{len(env)}  worst excess per carry {[round(w, 2) for w, _, _ in env]}  | {gs}")
