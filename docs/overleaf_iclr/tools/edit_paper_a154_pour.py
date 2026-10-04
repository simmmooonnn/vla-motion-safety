# -*- coding: utf-8 -*-
# Pouring as a second goal for T1 and T6 (queues pourx, f0pourx; the pour crossing cells rerun in hx9b with the hand that
# withdraws out of reach; 2026-10-04). A keep-out marker beside the jug's transport at the kitchen counter, and the crossing
# hand at the dining table. Written when the cells exist; every number from the generator; below the eight-episode floor the
# count is given and no rate is read. Exec'd after a153 (uses t, _rn2, V).
_po = (V.get("pour2") or {}).get("pi")
if _po:
    _f0p = (V.get("pour2") or {}).get("f0")
    _kh, _nh = (int(v) for v in _po["hx"].split("/")) if "/" in _po["hx"] else (0, 0)
    _par = ("**Pouring, a second goal.** The trajectory and dynamics predicates do not depend on the instruction, so they are "
            "also run while π0.5 pours milk from a jug into the bowl (" + _po["carried"] + "/" + _po["att"] + " attempts carried). "
            "A marker 0.20 m beside the jug's transport at the kitchen counter is entered on " + _po["t1_20"] + " carries and one "
            "0.28 m beside it on " + _po["t1_28"] + "; at the dining table the crossing hand is reached on " + _po["hx"]
            + (" (below the eight-episode floor, a count)" if _nh < 8 else "") + " and waited for on " + _po["hx_wait"] + "."
            + (" π0-FAST does not carry the jug (" + _f0p["carried"] + "/" + _f0p["att"] + ")." if _f0p and _f0p["carried"] == "0" else "")
            + " Table IVe counts pouring as a second goal of T1" + (" and T6" if _nh >= 8 else ", and of T6 after its plus sign") + ".")
    _i = t.find("**A hand that withdraws when touched (reactive proxy).**")
    if _i > 0:
        t = t[:_i] + _par + "\n\n" + t[_i:]
    else:
        print("  [a154 MISS] anchor for the pouring paragraph")
# the pour positive control's main-text count, generated (it had been a literal since a129)
if V.get("pour", {}).get("away"):
    _rn2("a pour tilts away from the bowl on 2/26 carries,", "a pour tilts away from the bowl on " + V["pour"]["away"] + " carries,")
