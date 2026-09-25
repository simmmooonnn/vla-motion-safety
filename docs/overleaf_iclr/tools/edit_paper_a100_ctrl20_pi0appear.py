# -*- coding: utf-8 -*-
# The blind control at the 0.20 m level, and pi0 on the appearance ablation. Guarded. Exec'd after a99 (uses t, RN, V).
_tc, _a0 = V.get("t1_off_ctrl", {}), V.get("appear_pi0", {})
if _tc.get("d20", {}).get("rate", "0/0") != "0/0":
    RN("A 0.20 m level, where a straight line would pass at exactly the keep-out radius, fills the series in: π0.5 enters on " +
       V["t1_off"]["d20"]["rate"] + " with a median clearance of " + V["t1_off"]["d20"]["dmed"] + " m — again inside the offset — so the four levels read " +
       V["t1_off"]["on"]["rate"] + ", " + V["t1_off"]["d12"]["rate"] + ", " + V["t1_off"]["d20"]["rate"] + ", " + V["t1_off"]["d28"]["rate"] +
       " for the policy against " + _tc["on"]["rate"] + ", " + _tc["d12"]["rate"] + " and " + _tc["d28"]["rate"] + " for the blind carrier at the levels it was run.",
       "A 0.20 m level, where a straight line passes at exactly the keep-out radius, fills the series in: π0.5 enters on " +
       V["t1_off"]["d20"]["rate"] + " with a median clearance of " + V["t1_off"]["d20"]["dmed"] + " m — again inside the offset — where the blind carrier, on the boundary, scores " +
       _tc["d20"]["rate"] + " at " + _tc["d20"]["dmed"] + " m, so the four levels read " + V["t1_off"]["on"]["rate"] + ", " + V["t1_off"]["d12"]["rate"] + ", " +
       V["t1_off"]["d20"]["rate"] + ", " + V["t1_off"]["d28"]["rate"] + " for the policy against " + _tc["on"]["rate"] + ", " + _tc["d12"]["rate"] + ", " +
       _tc["d20"]["rate"] + ", " + _tc["d28"]["rate"] + " for a straight line.")
def _n_of(x):
    try: return int(x.split("/")[1])
    except Exception: return 0
_a0_ok = all(_n_of(_a0.get(k, {}).get("T3_R", "—")) >= 8 for k in ("mesh", "hidden"))
if _a0_ok:
    RN("Person-blindness is therefore blindness to a person at any appearance we can render, not an artefact of an impoverished proxy.",
       "π0 gives the same answer on the same cells: " + _a0["capsule"]["T3_R"] + ", " + _a0["mesh"]["T3_R"] + " and " + _a0["hidden"]["T3_R"] +
       " on the right, " + _a0["capsule"]["T3_L"] + ", " + _a0["mesh"]["T3_L"] + " and " + _a0["hidden"]["T3_L"] + " on the left. Person-blindness "
       "is therefore blindness to a person at any appearance we can render, on both policies, not an artefact of an impoverished proxy.")
elif _a0.get("hidden", {}).get("T3_R", "—") != "—":
    RN("Person-blindness is therefore blindness to a person at any appearance we can render, not an artefact of an impoverished proxy.",
       "Person-blindness is therefore blindness to a person at any appearance we can render, not an artefact of an impoverished proxy. "
       "(π0 was run on the same cells but carries the scissors on at most two episodes per level, below the floor; it adds no second policy here.)")
