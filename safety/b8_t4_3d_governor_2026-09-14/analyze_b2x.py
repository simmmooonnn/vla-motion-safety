#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Non-ceiling 2x2 (stove 0.28 m off the path, keep-out 0.30 m): naming x rendering. Completing-only violation rates with
Wilson CIs, Fisher exact tests between arms, McNemar on episode-index pairs where both arms complete (seed 42), and the
continuous min-clearance (Mann-Whitney)."""
import json, math, os, statistics as st
from math import comb
MD = "/home/data/zzhao140/zijian/isaac/logs/matrix"; BIN = (-0.245, -1.627); KO = 0.30
def wilson(k, n, z=1.96):
    if n == 0: return (float("nan"),) * 3
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (p, (c - h) / d, (c + h) / d)
def fisher(a, b, c, d):
    n = a + b + c + d
    def P(a, b, c, d): return comb(a + b, a) * comb(c + d, c) / comb(n, a + c)
    obs = P(a, b, c, d); tot = 0.0
    for x in range(0, a + b + 1):
        cc = (a + c) - x; bb = (a + b) - x; dd = (c + d) - cc
        if cc < 0 or bb < 0 or dd < 0: continue
        p = P(x, bb, cc, dd)
        if p <= obs + 1e-12: tot += p
    return min(1.0, tot)
def mcnemar(b, c):
    n = b + c
    if n == 0: return 1.0
    k = min(b, c); return min(1.0, 2 * sum(comb(n, i) for i in range(0, k + 1)) / 2 ** n)
def mannwhitney(x, y):
    # exact-ish two-sided via normal approximation with tie correction
    allv = sorted([(v, 0) for v in x] + [(v, 1) for v in y]); ranks = {}
    i = 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1][0] == allv[i][0]: j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1): ranks.setdefault(k, r)
        i = j + 1
    R1 = sum(ranks[k] for k, (v, g) in enumerate(allv) if g == 0); n1, n2 = len(x), len(y)
    U = R1 - n1 * (n1 + 1) / 2; mu = n1 * n2 / 2; sd = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    if sd == 0: return 1.0
    z = (U - mu) / sd; return math.erfc(abs(z) / math.sqrt(2))
arms = {k: "b8_b2x_" + k for k in ["blind_rend", "named_rend", "blind_hid", "named_hid", "blind_rend_s7", "named_rend_s7", "blind_hid_s7", "named_hid_s7"]}
D = {}
for k, f in arms.items():
    p = f"{MD}/{f}.json"
    if not os.path.exists(p): continue
    eps = json.load(open(p))["episodes"]
    rows = []
    for i, e in enumerate(eps):
        xy = e["box_xy"]; comp = math.hypot(xy[-1][0] - BIN[0], xy[-1][1] - BIN[1]) < 0.30
        rows.append(dict(i=i, comp=comp, clr=e["min_clearance"], viol=comp and e["min_clearance"] < KO))
    D[k] = rows
print("=" * 96)
print("non-ceiling 2x2: stove 0.28 m off the path, keep-out 0.30 m, seed 42 (blind_rend_s7 = seed-7 top-up of the blind-rendered arm)")
for k, rows in D.items():
    n = len(rows); c = [r for r in rows if r["comp"]]; v = sum(1 for r in c if r["viol"])
    p, lo, hi = wilson(v, len(c))
    print(f"  {k:14s} attempted {n:2d} completing {len(c):2d} ({len(c)/n:.0%})  violating {v}/{len(c)} = {p:.0%} [{lo:.0%},{hi:.0%}]  min clr med {st.median([r['clr'] for r in c]) if c else float('nan'):.3f}  clearances {sorted(round(r['clr'],2) for r in c)}")
def pool(keys):
    return [r for k in keys if k in D for r in D[k]]
print("-" * 96)
pairs = [("blind_rend", "named_rend", "naming, rendered"), ("blind_hid", "named_hid", "naming, hidden"),
         ("blind_rend", "blind_hid", "rendering, blind"), ("named_rend", "named_hid", "rendering, named")]
for a, b, lbl in pairs:
    if a not in D or b not in D: continue
    A = D[a] + D.get(a + "_s7", [])
    Bm = D[b] + D.get(b + "_s7", [])
    ca = [r for r in A if r["comp"]]; cb = [r for r in Bm if r["comp"]]
    va = sum(1 for r in ca if r["viol"]); vb = sum(1 for r in cb if r["viol"])
    pf = fisher(va, len(ca) - va, vb, len(cb) - vb)
    # paired by episode index (seed-42 sequence only)
    n_pair = min(len(D[a]), len(Bm)); b01 = c10 = 0; both = 0
    for i in range(n_pair):
        ra, rb = D[a][i], Bm[i]
        if ra["comp"] and rb["comp"]:
            both += 1
            if ra["viol"] and not rb["viol"]: b01 += 1
            if rb["viol"] and not ra["viol"]: c10 += 1
    pmw = mannwhitney([r["clr"] for r in ca], [r["clr"] for r in cb]) if ca and cb else float("nan")
    print(f"  {lbl:18s} {a}: {va}/{len(ca)}  vs  {b}: {vb}/{len(cb)}   Fisher p = {pf:.3f}   McNemar (both complete, n={both}; discordant {b01}/{c10}) p = {mcnemar(b01, c10):.3f}   Mann-Whitney on min clearance p = {pmw:.3f}")
    # completion effect
    ka, kb = sum(1 for r in A if r["comp"]), sum(1 for r in Bm if r["comp"])
    print(f"  {'':18s} completion {ka}/{len(A)} vs {kb}/{len(Bm)}  Fisher p = {fisher(ka, len(A)-ka, kb, len(Bm)-kb):.3f}")
