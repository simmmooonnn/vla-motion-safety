# -*- coding: utf-8 -*-
"""Coverage of the tabletop family: work surface x environment map x task, with the rate per sub-type.

Reads fr_summary.json. Excludes the oak scene (its table loses its collider when the background is shifted) and every
probe / smoke / demo / still cell. Rates are conditioned on carried episodes, as in the paper.
"""
import json, pathlib

S = json.load(open(pathlib.Path(__file__).parent / "fr_summary.json", encoding="utf-8"))
g = lambda l, k, d=None: S.get(l, {}).get(k, d)

SKIP = ("probe", "smoke", "still", "demo", "d4_", "d5_", "posetest", "oak")

def surface(l):
    for pre, name in (("sc_kit_", "kitchen counter"), ("sc_pack_", "packing station"), ("sc_drw_", "drawer kitchen"),
                      ("sc_rki_", "island kitchen"), ("sc_off_", "office desk"), ("dw_", "drawer kitchen")):
        if l.startswith(pre) or l.startswith("p0_" + pre) or l.startswith("g0_" + pre):
            return name
    return "dining table"

def envmap(l):
    b = l[3:] if l.startswith(("p0_", "g0_")) else l
    if b.startswith("env_"):
        return {"courtyard": "outdoor courtyard", "woods": "outdoor woodland",
                "autosvc": "industrial auto shop", "lounge": "domestic lounge"}.get(b.split("_")[1], b.split("_")[1])
    if surface(l) == "packing station":
        return "industrial warehouse"
    return "scene default"

def task(l):
    b = l[3:] if l.startswith(("p0_", "g0_")) else l
    if b.startswith("sv_"):
        return "serving"
    if b.startswith("ho_"):
        return "handover"
    if b.startswith("dw_"):
        return "put away in a drawer"
    if b.startswith("cl_"):
        return "cluttered table"
    if b.startswith("wk_"):
        return "pick-and-place, passer-by"
    return "pick-and-place"

def policy(l):
    return "pi0" if l.startswith("p0_") else ("GR00T-DROID" if l.startswith("g0_") else "pi0.5")

def pool(cells, k, nk=None, lenk=None):
    kk = sum(g(l, k, 0) or 0 for l in cells)
    nn = sum((len(g(l, lenk, []) or []) if lenk else (g(l, nk, 0) or 0)) for l in cells)
    return kk, nn

def rate(k, n):
    return f"{round(100*k/n)}% ({k}/{n})" if n else "—"

cells = [l for l in S if g(l, "N") and not any(x in l for x in SKIP)]
groups = {}
for l in cells:
    groups.setdefault((policy(l), surface(l), envmap(l), task(l)), []).append(l)

rows = []
for (pol, surf, env, tsk), ls in sorted(groups.items()):
    att = sum(g(l, "N", 0) for l in ls); car = sum(g(l, "carried", 0) for l in ls); comp = sum(g(l, "completed", 0) for l in ls)
    mug = [l for l in ls if g(l, "tilt_trans") and all(x not in l for x in ("sci", "fork", "hot", "nocol"))]
    t4 = pool(mug, "t45", lenk="tilt_trans")
    t2 = pool([l for l in ls if g(l, "t2_n")], "t2_viol", "t2_n")
    t3 = pool([l for l in ls if g(l, "t3") is not None and ("sci" in l or "fork" in l)], "t3_90", lenk="t3")
    t5a = pool([l for l in ls if g(l, "ssm_n")], "ssm_viol", "ssm_n")
    t6c = [l for l in ls if g(l, "t6_n") and "nocol" not in l and "handret" not in l and l != "t6_hand_s42"]
    t6 = pool(t6c, "t6_reach", "t6_n")
    rows.append([pol, surf, env, tsk, att, car, comp, rate(*t2), rate(*t3), rate(*t4), rate(*t5a), rate(*t6)])

hdr = ["policy", "work surface", "environment", "task", "eps", "carried", "delivered", "T2", "T3", "T4", "T5a", "T6"]
w = [max(len(str(r[i])) for r in rows + [hdr]) for i in range(len(hdr))]
line = lambda r: "  ".join(str(r[i]).ljust(w[i]) for i in range(len(hdr)))
print(line(hdr)); print("  ".join("-" * x for x in w))
for r in rows:
    print(line(r))
print()
print(f"{len(rows)} groups | surfaces {len({r[1] for r in rows})} | environments {len({r[2] for r in rows})} | "
      f"tasks {len({r[3] for r in rows})} | policies {len({r[0] for r in rows})} | "
      f"{sum(r[4] for r in rows)} episodes, {sum(r[5] for r in rows)} carried, {sum(r[6] for r in rows)} delivered")
