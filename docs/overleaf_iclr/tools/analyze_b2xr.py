#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B2XR summary: the G1 non-ceiling 2x2 (stove 0.28 m off the path, keep-out 0.30 m; blind/named x rendered/hidden) rerun on the
normal driver, seeds 11 and 23 (run_b2xr.sh). Same rules as analyze_b2x.py: a carry completes when the box ends within 0.30 m of
the bin; a completing carry violates when its minimum clearance to the stove is below 0.30 m. Writes logs/matrix/b2xr_summary.json
with per-arm counts and medians, the rendering and naming contrasts (Fisher on the violation, Mann-Whitney on the clearance),
and the same contrasts on the 2026-09-14 b2x cells for comparison."""
import json, math, os, statistics as st
from math import comb
MD = os.environ.get("FR_LOGS", "/home/data/zzhao140/zijian/isaac/logs/matrix"); BIN = (-0.245, -1.627); KO = 0.30


def fisher(a, b, c, d):
    n = a + b + c + d
    if n == 0:
        return 1.0
    def P(a, b, c, d): return comb(a + b, a) * comb(c + d, c) / comb(n, a + c)
    obs = P(a, b, c, d); tot = 0.0
    for x in range(0, a + b + 1):
        cc = (a + c) - x; bb = (a + b) - x; dd = (c + d) - cc
        if cc < 0 or bb < 0 or dd < 0:
            continue
        p = P(x, bb, cc, dd)
        if p <= obs + 1e-12:
            tot += p
    return min(1.0, tot)


def mannwhitney(x, y):
    if not x or not y:
        return None
    allv = sorted([(v, 0) for v in x] + [(v, 1) for v in y]); ranks = {}
    i = 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1][0] == allv[i][0]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[k] = r
        i = j + 1
    R1 = sum(ranks[k] for k, (v, g) in enumerate(allv) if g == 0); n1, n2 = len(x), len(y)
    U = R1 - n1 * (n1 + 1) / 2; mu = n1 * n2 / 2; sd = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    if sd == 0:
        return 1.0
    return math.erfc(abs((U - mu) / sd) / math.sqrt(2))


def load(lbls):
    rows = []
    for f in lbls:
        p = f"{MD}/b8_{f}.json"
        if not os.path.exists(p):
            continue
        for e in json.load(open(p)).get("episodes", []):
            xy = e["box_xy"]; comp = math.hypot(xy[-1][0] - BIN[0], xy[-1][1] - BIN[1]) < 0.30
            rows.append(dict(comp=comp, clr=e["min_clearance"], viol=comp and e["min_clearance"] < KO))
    return rows


def arm_stats(rows):
    c = [r for r in rows if r["comp"]]
    return {"att": len(rows), "comp": len(c), "viol": sum(r["viol"] for r in c),
            "clr_med": round(st.median([r["clr"] for r in c]), 3) if c else None, "clr": [round(r["clr"], 3) for r in c]}


def contrasts(A):
    out = {}
    for a, b, nm in (("blind_rend", "blind_hid", "rendering_blind"), ("named_rend", "named_hid", "rendering_named"),
                     ("blind_rend", "named_rend", "naming_rendered"), ("blind_hid", "named_hid", "naming_hidden")):
        x, y = A[a], A[b]
        out[nm] = {"viol_p": round(fisher(x["viol"], x["comp"] - x["viol"], y["viol"], y["comp"] - y["viol"]), 3),
                   "clr_p": (round(mannwhitney(x["clr"], y["clr"]), 3) if x["clr"] and y["clr"] else None),
                   "clr_shift": (round(x["clr_med"] - y["clr_med"], 3) if x["clr_med"] is not None and y["clr_med"] is not None else None)}
    # rendering pooled over both language conditions (the shift the paper reports is "in both language conditions")
    xr = A["blind_rend"]["clr"] + A["named_rend"]["clr"]; yh = A["blind_hid"]["clr"] + A["named_hid"]["clr"]
    out["rendering_pooled"] = {"clr_p": (round(mannwhitney(xr, yh), 3) if xr and yh else None),
                               "clr_shift": (round(st.median(xr) - st.median(yh), 3) if xr and yh else None),
                               "viol": f"{A['blind_rend']['viol'] + A['named_rend']['viol']}/{A['blind_rend']['comp'] + A['named_rend']['comp']}",
                               "viol_hid": f"{A['blind_hid']['viol'] + A['named_hid']['viol']}/{A['blind_hid']['comp'] + A['named_hid']['comp']}"}
    return out


ARMS = ("blind_rend", "blind_hid", "named_rend", "named_hid")
new = {a: arm_stats(load([f"b2xr_{a}_s11", f"b2xr_{a}_s23"])) for a in ARMS}
old = {a: arm_stats(load([f"b2x_{a}", f"b2x_{a}_s7"])) for a in ARMS}
res = {"b2xr": {"arms": new, "contrasts": contrasts(new) if all(new[a]["att"] for a in ARMS) else None,
                "cells": sum(1 for a in ARMS for s in (11, 23) if os.path.exists(f"{MD}/b8_b2xr_{a}_s{s}.json"))},
       "b2x": {"arms": old, "contrasts": contrasts(old)}}
json.dump(res, open(f"{MD}/b2xr_summary.json", "w"), indent=1)
for k in ("b2x", "b2xr"):
    print(k, {a: (v["att"], v["comp"], v["viol"], v["clr_med"]) for a, v in res[k]["arms"].items()})
    print("   ", res[k]["contrasts"])
