# -*- coding: utf-8 -*-
# Pouring as a second goal for T1 and T6 (queues pourx, pourx2, f0pourx; 2026-10-04): a keep-out marker beside the jug's
# transport at the kitchen counter, and the crossing hand of the T6 cells while it pours. Written when the cells exist; every
# number from the generator. Exec'd after a153 (uses t, _rn2, V).
_po = (V.get("pour2") or {}).get("pi")
if _po:
    _f0p = (V.get("pour2") or {}).get("f0")
    _par = ("**Pouring, a second goal.** The trajectory and dynamics predicates do not depend on the instruction, so they are "
            "also run while π0.5 pours milk from a jug into the bowl (" + _po["carried"] + "/" + _po["att"] + " attempts carried). "
            "A marker 0.20 m beside the jug's transport at the kitchen counter is entered on " + _po["t1_20"] + " carries and one "
            "0.28 m beside it on " + _po["t1_28"] + ", the same far-side bow as the mug's; the crossing hand is reached on "
            + _po["hx"] + " and waited for on " + _po["hx_wait"] + "."
            + (" π0-FAST does not carry the jug (" + _f0p["carried"] + "/" + _f0p["att"] + ")." if _f0p and _f0p["carried"] == "0" else "")
            + " These cells give T1 and T6 a second goal (Table IVe).")
    _i = t.find("**A hand that withdraws when touched (reactive proxy).**")
    if _i > 0:
        t = t[:_i] + _par + "\n\n" + t[_i:]
    else:
        print("  [a154 MISS] anchor for the pouring paragraph")
