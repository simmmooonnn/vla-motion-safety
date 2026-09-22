# -*- coding: utf-8 -*-
"""Round 3: the three-level appearance ablation and the re-rendered small bystanders."""
import io

p = "gen_a45_numbers.py"
s = io.open(p, encoding="utf-8").read()
a = 'N["matched"] = _matched()'
assert s.count(a) == 1

blk = '''N["matched"] = _matched()
# ---- appearance of the scored bystander: capsule proxy / photorealistic human mesh / not rendered (review round 3, C2)
def _ap_pool(pre, side, kind):
    if kind == "T3":
        ls = [l for l in S if base(l).startswith(pre) and ("_" + side + "_") in base(l) and g(l, "t3") is not None]
        k, n = pool(ls, "t3_90", lenk="t3")
    else:
        ls = [l for l in S if base(l).startswith(pre) and g(l, "t2_n")]
        k, n = pool(ls, "t2_viol", "t2_n")
    return f"{k}/{n}" if n else "—"
N["appear"] = {
    "capsule": {"T3_R": _ap_pool("t3_sci", "R", "T3"), "T3_L": _ap_pool("t3_sci", "L", "T3"), "T2": _ap_pool("t2_R", "R", "T2")},
    "mesh": {"T3_R": _ap_pool("hm_t3_sci", "R", "T3"), "T3_L": _ap_pool("hm_t3_sci", "L", "T3"), "T2": _ap_pool("hm_t2_R", "R", "T2")},
    "hidden": {"T3_R": _ap_pool("hv_t3_sci", "R", "T3"), "T3_L": _ap_pool("hv_t3_sci", "L", "T3"), "T2": _ap_pool("hv_t2", "R", "T2")},
}
# ---- the small bystanders before and after the rendered body was made to follow the scored band (review round 3, C6)
def _sv_pair(old, new):
    out = {}
    for tag, pre in (("old", old), ("new", new)):
        t2 = [l for l in S if base(l).startswith(pre + "_t2") and g(l, "t2_n")]
        t3 = [l for l in S if base(l).startswith(pre + "_t3_sci") and g(l, "t3") is not None]
        sv = [l for l in S if base(l).startswith(pre.replace("ch", "svch").replace("st", "svst") + "_mug_R") and g(l, "tilt_trans")]
        out[tag + "_T2"] = "{}/{}".format(*pool(t2, "t2_viol", "t2_n")) if t2 else "—"
        out[tag + "_T3"] = "{}/{}".format(*pool(t3, "t3_90", lenk="t3")) if t3 else "—"
        out[tag + "_T4"] = "{}/{}".format(*pool(sv, "t45", lenk="tilt_trans")) if sv else "—"
    return out
N["small_vis"] = {"child": _sv_pair("ch", "chv"), "seated": _sv_pair("st", "stv")}'''

s = s.replace(a, blk)
io.open(p, "w", encoding="utf-8").write(s)
print("patched")
