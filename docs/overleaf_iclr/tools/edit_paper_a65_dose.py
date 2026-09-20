# -*- coding: utf-8 -*-
# Body sweep as a function of the bowl's offset from the person (dining table), and serving at the packing station. Exec'd after a64 (uses t, RN, V).
_ss = V.get("sv_surf", {})
if _ss.get("d45", {}).get("att", "0") not in ("0", "") and _ss.get("d55", {}).get("att", "0") not in ("0", ""):
    _pk = _ss.get("packing", {})
    RN("the bowl beside the person being at the edge of the arm's reach).",
       "the bowl beside the person being at the edge of the arm's reach). At the dining table the sweep follows the bowl's offset from the adult's axis: within 0.10 m on " +
       V.get("sv_T2", "28/128") + " episodes at 0.32 m, " + _ss["d45"]["T2"] + " at 0.45 m and " + _ss["d55"]["T2"] + " at 0.55 m" +
       ((", and at the packing station with the bowl 0.55 m from them on " + _pk["T2"]) if _pk.get("att", "0") not in ("0", "") else "") +
       ": the body-sweep exposure is set by where the task puts the destination, not by the policy noticing who stands beside it.")
