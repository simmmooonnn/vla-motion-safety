# -*- coding: utf-8 -*-
# GR00T N1.6-DROID on the discriminating trajectory cell. Guarded on the floor. Exec'd after a109 (uses t, RN, V).
_gg = V.get("t1_off_gr00t", {})
try:
    _ngg = int(_gg.get("rate", "0/0").split("/")[1])
except Exception:
    _ngg = 0
if _ngg >= 8:
    RN("So the 0.28 m cell is a trajectory measurement the policy owns (π0, over the four surfaces, enters it on " +
       V.get("t1_off_pi0", {}).get("d28", {}).get("rate", "3/12") + " of its carries at a median clearance of " +
       V.get("t1_off_pi0", {}).get("d28", {}).get("dmed", "0.21") + " m)",
       "So the 0.28 m cell is a trajectory measurement the policy owns (π0, over the four surfaces, enters it on " +
       V.get("t1_off_pi0", {}).get("d28", {}).get("rate", "3/12") + " of its carries at a median clearance of " +
       V.get("t1_off_pi0", {}).get("d28", {}).get("dmed", "0.21") + " m; GR00T N1.6-DROID, which carries " + _gg["car"] + "/" +
       _gg["att"] + " there, on " + _gg["rate"] + " at " + _gg["dmed"] + " m)")
