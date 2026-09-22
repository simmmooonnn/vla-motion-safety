# -*- coding: utf-8 -*-
# Page budget after the round-3 results: the off-path T1 paragraph and the §6 (ii) clause tightened. Exec'd after a86.
_t1 = V.get("t1_off", {})
if _t1.get("d28", {}).get("rate", "0/0") != "0/0":
    RN("**T1 off the path (review probe).** The scored tabletop marker sits on the transport, so entering it is forced and the "
       "rate is a ceiling; moving the same marker off the path makes the cell discriminating: " + _t1["on"]["rate"] +
       " at the midpoint, " + _t1["d12"]["rate"] + " at 0.12 m off it (median clearance " + _t1["d12"]["dmed"] +
       " m, i.e. inside the offset: the path bends toward the marker) and " + _t1["d28"]["rate"] + " at 0.28 m off it (median " +
       _t1["d28"]["dmed"] + " m, minimum " + _t1["d28"]["dmin"] + " m), where a direct carry would not violate at all. We report "
       "the off-path series as the trajectory measurement with headroom and keep the midpoint cell as exposure.",
       "**T1 off the path.** The scored marker sits on the transport, so entry is forced and the rate is a ceiling. Moved off "
       "the path the same cell discriminates: " + _t1["on"]["rate"] + " at the midpoint, " + _t1["d12"]["rate"] + " at 0.12 m "
       "(median clearance " + _t1["d12"]["dmed"] + " m — inside the offset, so the path bends toward it) and " +
       _t1["d28"]["rate"] + " at 0.28 m, which a direct carry clears. The off-path series is the trajectory measurement with "
       "headroom; the midpoint cell is exposure.")
    RN("(16/16), while a marker moved 0.28 m off the transport — which a straight carry clears — is still entered on " +
       _t1["d28"]["rate"] + " carries.",
       "(16/16), and one moved 0.28 m off the transport, clear of a direct carry, is entered on " + _t1["d28"]["rate"] + ".")
