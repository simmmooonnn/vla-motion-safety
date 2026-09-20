# -*- coding: utf-8 -*-
# The withdrawing hand met with scissors; the bowl-offset fall-off on the left side. Exec'd after a69 (uses t, RN, V).
_hs, _sd, _sl = V.get("hw_sci", {}), V.get("svd_side", {}), V.get("svh_L", {})
if _hs.get("car", "0") not in ("0", ""):
    RN("the exposure rates of the static hand are not an artefact of a proxy that cannot move away.",
       "the exposure rates of the static hand are not an artefact of a proxy that cannot move away. Carrying scissors toward the same withdrawing hand (" +
       _hs["car"] + "/" + _hs["att"] + " carried), the policy reaches it on " + _hs["reach"] + ", touches it on " + _hs["touch"] + (", follows it back on " + _hs["follow"] if _hs.get("follow", "0/0") != "0/0" else "") +
       " and presents the blade toward it on " + _hs["ho"] + ".")
if _sd.get("d45L", {}).get("att", "0") not in ("0", "") and _sd.get("d55L", {}).get("att", "0") not in ("0", ""):
    RN("the body-sweep exposure is set by where the task puts the destination, not by the policy noticing who stands beside it.",
       "the body-sweep exposure is set by where the task puts the destination, not by the policy noticing who stands beside it (left side: " +
       _sl.get("adult", {}).get("T2", "8/64") + " at 0.32 m, " + _sd["d45L"]["T2"] + " at 0.45 m, " + _sd["d55L"]["T2"] + " at 0.55 m).")
