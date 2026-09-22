# -*- coding: utf-8 -*-
# Page budget: the last three lines. §5.1's off-path paragraph folds into the T1 paragraph it precedes, and §8 loses a
# redundant clause. Exec'd after a87 (uses t, RN, V).
_t1 = V.get("t1_off", {})
if _t1.get("d28", {}).get("rate", "0/0") != "0/0":
    RN("**T1 off the path.** The scored marker sits on the transport, so entry is forced and the rate is a ceiling. Moved off "
       "the path the same cell discriminates: " + _t1["on"]["rate"] + " at the midpoint, " + _t1["d12"]["rate"] + " at 0.12 m "
       "(median clearance " + _t1["d12"]["dmed"] + " m — inside the offset, so the path bends toward it) and " +
       _t1["d28"]["rate"] + " at 0.28 m, which a direct carry clears. The off-path series is the trajectory measurement with "
       "headroom; the midpoint cell is exposure.",
       "**T1 off the path.** The scored marker sits on the transport, so entry is forced. Moved off it the cell discriminates: " +
       _t1["on"]["rate"] + " at the midpoint, " + _t1["d12"]["rate"] + " at 0.12 m (median clearance " + _t1["d12"]["dmed"] +
       " m, inside the offset) and " + _t1["d28"]["rate"] + " at 0.28 m, which a direct carry clears — the series with headroom.")
RN("the operator standards scored against (ISO 10218, ISO/TS 15066) are applied to untrained bystanders, whom ISO 13482 would "
   "treat more conservatively.",
   "the operator standards scored against are applied to untrained bystanders, whom ISO 13482 would treat more conservatively.")
