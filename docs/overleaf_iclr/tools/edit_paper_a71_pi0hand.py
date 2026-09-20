# -*- coding: utf-8 -*-
# The withdrawing hand on pi0. Exec'd after a70 (uses t, RN, V).
_h0 = V.get("hw_pi0", {})
if _h0.get("car", "0") not in ("0", ""):
    RN("and presents the blade toward it on " + V.get("hw_sci", {}).get("ho", "6/13") + ".",
       "and presents the blade toward it on " + V.get("hw_sci", {}).get("ho", "6/13") + ". π0, which carries on " + _h0["car"] + "/" + _h0["att"] +
       " of the same episodes, reaches the withdrawing hand on " + _h0["reach"] + " and touches it on " + _h0["touch"] +
       ((", following it back on " + _h0["follow"]) if _h0.get("follow", "0/0") != "0/0" else "") + "." +
       ((" With the fork (" + V["hw_fork"]["car"] + "/" + V["hw_fork"]["att"] + " carried) π0.5 reaches the hand on " + V["hw_fork"]["reach"] + " and points the tines toward it on " + V["hw_fork"]["ho"] + ".") if V.get("hw_fork", {}).get("car", "0") not in ("0", "") else ""))
