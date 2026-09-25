# -*- coding: utf-8 -*-
"""Round 3 follow-ups: the stature x side factorial (review D1) and the pinch-grasp witness per surface (C2 widened)."""
import io

p = "gen_a45_numbers.py"
s = io.open(p, encoding="utf-8").read()
a = 'N["n_tasks_exercised"] ='
assert s.count(a) == 1

blk = '''# ---- stature x side, crossed: {adult, seated, child} x {R, L} on T2 (mug) and T3 (scissors), two seeds each (review D1)
def _sxs(pre, side):
    t2 = [l for l in S if l.startswith(pre + "2_" + side + "_s") and g(l, "t2_n") and "cmd" not in l and policy(l) == "pi05"]
    t3 = [l for l in S if l.startswith(pre + "3_sci_" + side + "_s") and g(l, "t3") is not None and "cmd" not in l and policy(l) == "pi05"]
    k2, n2 = pool(t2, "t2_viol", "t2_n"); k3, n3 = pool(t3, "t3_90", lenk="t3")
    return {"T2": (f"{k2}/{n2}" if n2 else "—"), "T3": (f"{k3}/{n3}" if n3 else "—"), "T3_pct": (f"{100 * k3 / n3:.0f}" if n3 else "—")}
N["sxs"] = {st_: {side: _sxs(pre, side) for side in ("R", "L")} for st_, pre in (("adult", "t"), ("seated", "stv_t"), ("child", "chv_t"))}
N["sxs_rows"] = "\\n".join("| " + st_ + " | " + " | ".join(N["sxs"][st_][sd]["T2"] + " | " + N["sxs"][st_][sd]["T3"] for sd in ("R", "L")) + " |"
                          for st_ in ("adult", "seated", "child"))
# ---- the pinch-grasp control per work surface
def _pgs(pre):
    ls = [l for l in S if l.startswith(pre)]
    k, n = pool(ls, "t45", lenk="tilt_trans"); k7, _ = pool(ls, "t27", lenk="tilt_trans")
    return {"att": str(sum(g(l, "N", 0) for l in ls)), "car": str(sum(g(l, "carried", 0) or 0 for l in ls)),
            "dl": str(sum(g(l, "completed", 0) or 0 for l in ls)), "T4": (f"{k}/{n}" if n else "—"), "T4_27": (f"{k7}/{n}" if n else "—")}
N["pg_surf"] = {"dining": _pgs("ik_pg_t2_R"), "kitchen": _pgs("ik_pg_sc_kit"), "office": _pgs("ik_pg_sc_off")}
'''
s = s.replace(a, blk + a)
io.open(p, "w", encoding="utf-8").write(s)
print("patched")
