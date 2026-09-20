# -*- coding: utf-8 -*-
# Serving beside the person at two more surfaces: the body-sweep rise does not travel. Exec'd after a63 (uses t, RN, V).
_ss = V.get("sv_surf", {})
if _ss.get("counter", {}).get("att", "0") not in ("0", "") and _ss.get("office", {}).get("att", "0") not in ("0", ""):
    _k, _o = _ss["counter"], _ss["office"]
    RN("a lower head is swept less because it is lower, not because the carry changes.",
       "a lower head is swept less because it is lower, not because the carry changes. The serving body-sweep rise is the dining table's, not serving's: "
       "with the bowl 0.30-0.35 m from the adult's axis at the kitchen counter and the office desk, the arm comes within 0.10 m of them on " + _k["T2"] +
       " and " + _o["T2"] + " episodes (the dining table: " + V.get("sv_T2", "28/128") + "), while the orientation exposure travels (blade into their "
       "half-space on " + _k["T3"] + " and " + _o["T3"] + " carries; the mug past 45° on " + _k["T4"] + " and " + _o["T4"] + "; the counter cell delivers "
       + _k["dl"] + "/" + _k["car"] + " carried, the bowl beside the person being at the edge of the arm's reach).")
    RN("serving beside the person raises the body-sweep rate from 1 % to 22 % (Table IV).",
       "serving beside the person raises the body-sweep rate from 1 % to 22 % at the dining table but not at the counter or the desk (0/44, 3/48; Table IV).")
