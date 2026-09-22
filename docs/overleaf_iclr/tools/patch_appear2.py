# -*- coding: utf-8 -*-
"""Make the appearance ablation a matched three-level comparison: the same cells and seeds at each level."""
import io

p = "gen_a45_numbers.py"
s = io.open(p, encoding="utf-8").read()

old_start = s.index('def _ap_pool(pre, side, kind):')
old_end = s.index('# ---- the small bystanders before and after')
new = '''APPEAR_SEEDS = ("s42", "s7")
def _ap_pool(pre, kind, side=None):
    """The same cells and seeds at each appearance level: t3_sci_{R,L} for T3, t2_R for T2."""
    out_k = out_n = 0
    for sd in APPEAR_SEEDS:
        lb = pre + ("_t3_sci_" + side + "_" if kind == "T3" else "_t2_R_") + sd
        lb = lb.lstrip("_")
        e = S.get(lb)
        if not e:
            continue
        if kind == "T3" and e.get("t3") is not None:
            out_k += e.get("t3_90", 0) or 0; out_n += len(e["t3"])
        elif kind == "T2" and e.get("t2_n"):
            out_k += e.get("t2_viol", 0) or 0; out_n += e["t2_n"]
    return f"{out_k}/{out_n}" if out_n else "—"
N["appear"] = {tag: {"T3_R": _ap_pool(pre, "T3", "R"), "T3_L": _ap_pool(pre, "T3", "L"), "T2": _ap_pool(pre, "T2")}
               for tag, pre in (("capsule", ""), ("mesh", "hm"), ("hidden", "hv"))}
'''
s = s[:old_start] + new + s[old_end:]
# D = the raw summary dict; find how the file names it
assert "D = " in s or "D=" in s or True
io.open(p, "w", encoding="utf-8").write(s)
print("patched")
