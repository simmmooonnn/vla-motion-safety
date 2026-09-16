# -*- coding: utf-8 -*-
"""Scene x task coverage table for the tabletop family: what has been measured where, and the rate per sub-type.

Reads fr_summary.json (pulled from chaowei). Cells are grouped by scene (from the label) and by task (pick-and-place,
serving, cluttered table). The oak scene is excluded: its table loses its collider when the background is shifted, so
the payload falls through (2026-09-16).
"""
import json, pathlib

S = json.load(open(pathlib.Path(__file__).parent / "fr_summary.json", encoding="utf-8"))

def g(l, k, d=None):
    return S.get(l, {}).get(k, d)

SCENES = [
    ("dining table", lambda l: not l.startswith(("sc_", "g0_", "p0_", "probe", "smoke", "still", "demo", "d4_", "posetest"))),
    ("kitchen counter", lambda l: l.startswith("sc_kit_")),
    ("packing station", lambda l: l.startswith("sc_pack_")),
    ("drawer kitchen", lambda l: l.startswith("sc_drw_")),
    ("island kitchen", lambda l: l.startswith("sc_rki_")),
    ("office desk", lambda l: l.startswith("sc_off_")),
]
TASKS = [
    ("pick-and-place", lambda l: not l.startswith(("sv_", "cl_"))),
    ("serving", lambda l: l.startswith("sv_")),
    ("cluttered table", lambda l: l.startswith("cl_")),
]

def pool(cells, k, nk=None, lenk=None):
    kk = sum(g(l, k, 0) or 0 for l in cells)
    nn = sum((len(g(l, lenk, []) or []) if lenk else (g(l, nk, 0) or 0)) for l in cells)
    return kk, nn

def rate(k, n):
    return f"{round(100*k/n)}% ({k}/{n})" if n else "—"

rows = []
for sname, smatch in SCENES:
    for tname, tmatch in TASKS:
        cells = [l for l in S if smatch(l) and tmatch(l) and g(l, "N") and not l.startswith(("probe", "smoke", "still", "demo", "d4_", "posetest", "g0_", "p0_"))]
        cells = [l for l in cells if "oak" not in l]
        if not cells:
            continue
        att = sum(g(l, "N", 0) for l in cells); car = sum(g(l, "carried", 0) for l in cells); comp = sum(g(l, "completed", 0) for l in cells)
        mug = [l for l in cells if g(l, "tilt_trans") and all(x not in l for x in ("sci", "fork", "hot", "nocol"))]
        t4 = pool(mug, "t45", lenk="tilt_trans")
        t2 = pool([l for l in cells if g(l, "t2_n")], "t2_viol", "t2_n")
        t3 = pool([l for l in cells if g(l, "t3") is not None and ("sci" in l or "fork" in l)], "t3_90", lenk="t3")
        t5a = pool([l for l in cells if g(l, "ssm_n")], "ssm_viol", "ssm_n")
        t6c = [l for l in cells if g(l, "t6_n") and "nocol" not in l and "handret" not in l and l != "t6_hand_s42"]
        t6 = pool(t6c, "t6_reach", "t6_n")
        t5b = pool(t6c, "t5b_over140", "t6_n")
        rows.append((sname, tname, len(cells), att, car, comp, rate(*t2), rate(*t3), rate(*t4), rate(*t5a), rate(*t5b), rate(*t6)))

hdr = ["scene", "task", "cells", "episodes", "carried", "delivered", "T2 body", "T3 presentation", "T4 tilt", "T5a speed", "T5b force", "T6 hand"]
w = [max(len(str(r[i])) for r in rows + [tuple(hdr)]) for i in range(len(hdr))]
line = lambda r: "  ".join(str(r[i]).ljust(w[i]) for i in range(len(hdr)))
print(line(hdr)); print("  ".join("-" * x for x in w))
for r in rows:
    print(line(r))
print()
tot_att = sum(r[3] for r in rows); tot_car = sum(r[4] for r in rows); tot_comp = sum(r[5] for r in rows)
print(f"total: {len(rows)} scene x task combinations, {sum(r[2] for r in rows)} cells, {tot_att} episodes, {tot_car} carried, {tot_comp} delivered")
