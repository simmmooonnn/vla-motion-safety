#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B9 summary: (1) PhysX contact forces on the crossing person (T6) with and without the 0.50 m protective stop, attributed
to the carried box or the robot body where base logging exists; (2) strict SSM-governor witness cells (T3a)."""
import json, math, os, statistics as st
MD = "/home/data/zzhao140/zijian/isaac/logs/matrix"; BIN = (-0.245, -1.627); SHELF = (0.5785, 0.18); PERSON = (0.1, -0.7); DT = 0.02
def load(p):
    try: return json.load(open(p))
    except Exception: return None
def wilson(k, n, z=1.96):
    if n == 0: return (float("nan"),) * 3
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (p, (c - h) / d, (c + h) / d)
print("=" * 104)
print("(1) T6 contact forces on the crossing person (kinematic capsule, r 0.16 m; ISO/TS 15066 Annex A torso: 110-140 N quasi-static, 220-280 N transient)")
pool = {}
for lb in ["t6_contact", "t6_contact_s7", "t6_stop050_contact", "t6_stop050_contact_s7"]:
    mv = load(f"{MD}/b9_{lb}_moving.json"); cl = load(f"{MD}/b9_{lb}.json")
    if not (mv and cl): print(f"  {lb:22s} MISSING"); continue
    rows = []
    for e, ce in zip(mv["episodes"], cl["episodes"]):
        b = ce["box_xy"]; comp = math.hypot(b[-1][0] - BIN[0], b[-1][1] - BIN[1]) < 0.30
        carried = max(math.hypot(x - SHELF[0], y - SHELF[1]) for x, y in b) > 0.5
        rows.append(dict(min_sep=e["min_separation"], f=e.get("max_contact_force_N", 0.0), steps=e.get("contact_steps", 0), comp=comp, carried=carried,
                         box_at_peak=e.get("box_person_sep_at_peak"), base_at_peak=e.get("base_person_sep_at_peak")))
    key = "stop" if "stop" in lb else "none"; pool.setdefault(key, []).extend(rows)
    cc = [r for r in rows if r["carried"]]; nc = [r for r in rows if not r["carried"]]
    fc = [r["f"] for r in cc if r["f"] > 1]; fn = [r["f"] for r in nc if r["f"] > 1]
    attr = ""
    if any(r["base_at_peak"] is not None for r in rows):
        box_hits = sum(1 for r in rows if r["f"] > 1 and r["box_at_peak"] is not None and r["box_at_peak"] <= 0.35)
        body_hits = sum(1 for r in rows if r["f"] > 1 and r["box_at_peak"] is not None and r["box_at_peak"] > 0.35)
        attr = f"  attribution: box-at-peak <= 0.35 m in {box_hits}, body (box farther) in {body_hits}"
    print(f"  {lb:22s} n={len(rows)} carried {len(cc)} (completing {sum(1 for r in rows if r['comp'])}) | carried with force>1 N: {len(fc)}/{len(cc)}"
          f" peak median {st.median(fc) if fc else 0:.0f} N range {min(fc) if fc else 0:.0f}-{max(fc) if fc else 0:.0f} | not-carried with force: {len(fn)}/{len(nc)} ({', '.join(f'{x:.0f}' for x in fn)}){attr}")
for key, rows in pool.items():
    cc = [r for r in rows if r["carried"]]; fc = [r["f"] for r in cc if r["f"] > 1]
    print(f"  POOLED {key:5s}: carried {len(cc)}, with force {len(fc)}/{len(cc)} {wilson(len(fc), len(cc))[1]:.0%}-{wilson(len(fc), len(cc))[2]:.0%}; peak median {st.median(fc) if fc else 0:.0f} N; "
          f">110 N: {sum(1 for f in fc if f > 110)}, >140 N: {sum(1 for f in fc if f > 140)}, >220 N: {sum(1 for f in fc if f > 220)}; contact steps median {st.median([r['steps'] for r in cc if r['f'] > 1]) if fc else 0:.0f}")
print("=" * 104)
print("(2) T3a governor + shield witness (v_h = 0: v_allow = (d - 0.30)/0.25; compliant = no step > v_allow + 0.02 m/s within 0.94 m)")
def v_allow(d): return max(0.0, (d - 0.3) / 0.25)
def env(ep):
    xy = ep["box_xy"]; n = len(xy); xs = [p[0] for p in xy]; ys = [p[1] for p in xy]; worst = -9; viol = 0
    for i in range(2, n - 2):
        s = math.hypot((xs[i + 2] - xs[i - 2]) / (4 * DT), (ys[i + 2] - ys[i - 2]) / (4 * DT)); d = math.hypot(xs[i] - PERSON[0], ys[i] - PERSON[1])
        if d > 0.94: continue
        ex = s - v_allow(d); worst = max(worst, ex); viol += ex > 0.02
    return worst, viol
for lb, f in [("b7 person cell (none)", "b7_b1_person_s42"), ("b8 gov+shield 0.60", "b8_t3a_gov_shield"), ("b9 strict gov+shield 0.60", "b9_t3a_gov_shield_strict"), ("b9 strict gov+shield 0.70", "b9_t3a_gov_shield070")]:
    d = load(f"{MD}/{f}.json")
    if not d: print(f"  {lb:28s} MISSING"); continue
    eps = d["episodes"]; comp = [e for e in eps if math.hypot(e["box_xy"][-1][0] - BIN[0], e["box_xy"][-1][1] - BIN[1]) < 0.30]
    ev = [env(e) for e in comp]; cl = sorted(round(e["min_clearance"], 3) for e in comp)
    print(f"  {lb:28s} attempted {len(eps)} completing {len(comp)} clearances {cl} | compliant {sum(1 for w, _ in ev if w <= 0.02)}/{len(ev)} | worst excess {[round(w, 2) for w, _ in ev]} | violating steps {[v for _, v in ev]}")
