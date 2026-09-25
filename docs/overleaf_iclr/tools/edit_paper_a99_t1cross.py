# -*- coding: utf-8 -*-
# The off-path keep-out as a cross-policy, four-surface, four-level measurement: a 0.20 m level, the packing station and the
# drawer kitchen with their blind-control witnesses, and pi0 on the 0.28 m cell. All guarded. Exec'd after a98 (uses t, RN, V).
_t1, _tc, _p0, _sf = V.get("t1_off", {}), V.get("t1_off_ctrl", {}), V.get("t1_off_pi0", {}), V.get("t1_off_surf", {})

if _t1.get("d20", {}).get("rate", "0/0") != "0/0" and _sf.get("packing", {}).get("pi", "—") != "—":
    RN("The midpoint cell stays exposure: there the control violates " + _tc["on"]["rate"] + " at zero clearance.",
       "The midpoint cell stays exposure: there the control violates " + _tc["on"]["rate"] + " at zero clearance. A 0.20 m level, "
       "where a straight line would pass at exactly the keep-out radius, fills the series in: π0.5 enters on " + _t1["d20"]["rate"] +
       " with a median clearance of " + _t1["d20"]["dmed"] + " m — again inside the offset — so the four levels read " +
       _t1["on"]["rate"] + ", " + _t1["d12"]["rate"] + ", " + _t1["d20"]["rate"] + ", " + _t1["d28"]["rate"] + " for the policy against " +
       _tc["on"]["rate"] + ", " + _tc["d12"]["rate"] + " and " + _tc["d28"]["rate"] + " for the blind carrier at the levels it was run. "
       "The 0.28 m rate is pooled over four work surfaces and is not uniform across them: the policy enters the keep-out on " +
       _sf["desk"]["pi"] + " carries at the office desk but " + _sf["counter"]["pi"] + " at the kitchen counter, " + _sf["packing"]["pi"] +
       " at the packing station and " + _sf["drawer"]["pi"] + " in the drawer kitchen, while the control enters it on " +
       _sf["counter"]["ik"] + ", " + _sf["desk"]["ik"] + ", " + _sf["packing"]["ik"] + " and " + _sf["drawer"]["ik"] + ". The attraction is "
       "real and it is scene-dependent; the pooled number is what Table IV carries, and the desk is where it lives.")

if _p0.get("d28", {}).get("rate", "0/0") not in ("0/0", "") and int(_p0["d28"]["rate"].split("/")[1]) >= 8:
    RN("So the 0.28 m cell is a trajectory measurement the policy owns",
       "So the 0.28 m cell is a trajectory measurement the policy owns (π0, on the counter and the desk, enters it on " +
       _p0["d28"]["rate"] + " of its carries at a median clearance of " + _p0["d28"]["dmed"] + " m)")
    RN("is entered on " + _t1["d28"]["rate"] + ".",
       "is entered on " + _t1["d28"]["rate"] + " by π0.5 and " + _p0["d28"]["rate"] + " by π0.")
