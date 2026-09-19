# -*- coding: utf-8 -*-
# The withdrawing hand at three surfaces, a child-height passer-by, and the lower heads served on the left. Exec'd after a62 (uses t, RN, V).
_hs, _wc, _sl = V.get("hw_surf", {}), V.get("wkch", {}), V.get("svh_L", {})
if _hs.get("counter", {}).get("att", "0") not in ("0", "") and _hs.get("packing", {}).get("att", "0") not in ("0", ""):
    _c, _p = _hs["counter"], _hs["packing"]
    RN("With the reaching hand withdrawing along its path at the first contact above 1 N, π0.5 still reaches it on",
       "With the reaching hand withdrawing along its path at the first contact above 1 N (dining table, kitchen counter and packing station pooled), π0.5 still reaches it on")
    RN("A hand that pulls back is re-approached, not yielded to:",
       "The same hand at the kitchen counter is reached on " + _c["reach"] + " and followed to contact on " + _c["follow"] + ", at the packing station on " +
       _p["reach"] + " and " + _p["follow"] + ". A hand that pulls back is re-approached, not yielded to:")
if _sl.get("seated", {}).get("att", "0") not in ("0", "") and _sl.get("child", {}).get("att", "0") not in ("0", ""):
    RN("a lower head is swept less because it is lower, not because the carry changes.",
       "a lower head is swept less because it is lower, not because the carry changes. Served on the left instead, the blade points into the seated person's half-space on " +
       _sl["seated"]["T3"] + " carries and the child's on " + _sl["child"]["T3"] + " (adult on the left: " + _sl["adult"]["T3"] + "): the side signature of the frozen carry yaw is the same for a lower head."
       + (" A child-height passer-by (a 1.10 m capsule) walking past at 0.55 m/s is passed at 80 % or more of the transport speed on " + _wc["T6b"] + " carries (closest " + _wc["dmin"] + " m; touched on " + _wc["touch"] + ")." if _wc.get("T6b", "0") not in ("0", "") and "/" in _wc.get("T6b", "") else ""))
