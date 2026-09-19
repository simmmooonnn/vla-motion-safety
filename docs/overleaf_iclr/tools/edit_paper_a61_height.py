# -*- coding: utf-8 -*-
# Serving beside a seated and a child-height bystander; a handover whose receiver withdraws when touched (2026-09-19). Exec'd after a60 (uses t, RN, V).
_sv, _hw2 = V.get("svh", {}), V.get("how", {})
if _sv.get("seated", {}).get("att", "0") not in ("0", "") and _sv.get("child", {}).get("att", "0") not in ("0", ""):
    _s, _c, _a = _sv["seated"], _sv["child"], _sv["adult"]
    RN("the receiver's state changes whether the policy hands over, not how. Both are scored in Table IV.",
       "the receiver's state changes whether the policy hands over, not how. Both are scored in Table IV. Serving into a bowl beside the seated "
       "and the child-height bystander keeps the adult cell's orientation rates (blade into their half-space on " + _s["T3"] + " and " + _c["T3"] +
       " carries, adult " + _a["T3"] + "; the mug past 45° on " + _s["T4"] + " and " + _c["T4"] + ", adult " + _a["T4"] + ", and within 0.60 m of them on " +
       _s["spill_near"] + " and " + _c["spill_near"] + "), while the arm comes within 0.10 m of the seated person on " + _s["T2"] + " episodes and of the child on " +
       _c["T2"] + " (standing adult at the same placement: " + _a["T2"] + "): a lower head is swept less because it is lower, not because the carry changes.")
if _hw2.get("car", "0") not in ("0", ""):
    RN("a lower head is swept less because it is lower, not because the carry changes.",
       "a lower head is swept less because it is lower, not because the carry changes. A handover whose receiving hand withdraws at the first touch "
       "stays a capability boundary (" + _hw2["car"] + "/" + _hw2["att"] + " carried, " + _hw2["dl"] + " delivered); on the carries, the hazardous end is presented to the hand on " +
       _hw2["ho"] + " (static hand: " + _hw2["ho_static"] + "), the hand is reached on " + _hw2["reach"] + " and touched on " + _hw2["touch"] +
       ", and on the withdrawals the payload follows it back to contact on " + _hw2["follow"] + ".")
