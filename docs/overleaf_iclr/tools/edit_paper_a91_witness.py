# -*- coding: utf-8 -*-
# Review round 3, C4 discharged: the off-path keep-out now has its geometric witness, so the 0.28 m rate is attributable.
# Exec'd after a90 (uses t, RN, V).
_t1, _tc = V.get("t1_off", {}), V.get("t1_off_ctrl", {})
if _tc.get("d28", {}).get("rate", "0/0") != "0/0":
    RN("and " + _t1["d28"]["rate"] + " at 0.28 m (median " + _t1["d28"]["dmed"] + " m, minimum " + _t1["d28"]["dmin"] +
       " m), an offset a direct carry clears by construction. We report the off-path series as the trajectory measurement with "
       "headroom and keep the midpoint cell as exposure.",
       "and " + _t1["d28"]["rate"] + " at 0.28 m (median " + _t1["d28"]["dmed"] + " m, minimum " + _t1["d28"]["dmin"] + " m). "
       "The person-blind scripted carrier supplies the witness that fixes what those rates mean: on the same cells it violates " +
       _tc["d28"]["rate"] + " at 0.28 m, passing at exactly the offset (median " + _tc["d28"]["dmed"] + " m), and " +
       _tc["d12"]["rate"] + " at 0.12 m, again at the full offset (median " + _tc["d12"]["dmed"] + " m) where π0.5 closes to " +
       _t1["d12"]["dmed"] + " m. So the 0.28 m cell is a trajectory measurement the policy owns — a straight carry clears the "
       "keep-out and π0.5 enters it on " + _t1["d28"]["rate"] + " carries — and the 0.12 m clearances put a number on the "
       "attraction of §6 (ii): the blind carrier keeps the offset it was given, the policy gives away two thirds of it. The "
       "midpoint cell stays exposure: there the control violates " + _tc["on"]["rate"] + " at zero clearance.")
    RN("and one moved 0.28 m off the transport, clear of a direct carry, is entered on " + _t1["d28"]["rate"] + ".",
       "and one moved 0.28 m off the transport, which the blind scripted carrier clears " + _tc["d28"]["rate"] + ", is entered on " +
       _t1["d28"]["rate"] + ".")
