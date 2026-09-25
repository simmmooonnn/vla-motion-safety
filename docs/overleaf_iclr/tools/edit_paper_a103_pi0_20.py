# -*- coding: utf-8 -*-
# pi0 at the 0.20 m level, guarded on the floor. Exec'd after a102 (uses t, RN, V).
_p0 = V.get("t1_off_pi0", {})
if _p0.get("d20", {}).get("rate", "0/0") not in ("0/0", "") and int(_p0["d20"]["rate"].split("/")[1]) >= 8:
    RN("the sharpest and most uniform contrast in the series, every surface alike.",
       "the sharpest and most uniform contrast in the series, every surface alike; π0 enters on " + _p0["d20"]["rate"] +
       " of its carries at the counter and the desk (median clearance " + _p0["d20"]["dmed"] + " m).")
