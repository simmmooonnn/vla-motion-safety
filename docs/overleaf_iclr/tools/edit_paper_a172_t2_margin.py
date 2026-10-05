# -*- coding: utf-8 -*-
# ICLR-readiness review (item 19): the tabletop T2 distance is taken from link origins; a link's surface lies roughly 4-8 cm out,
# so a 0.10 m surface margin is a 0.14-0.18 m origin margin. E, at the end of the tabletop T2 paragraph. Exec'd after a171
# (uses t, _rn2, V).
_tm = V.get("t2_margin") or {}
_i2 = t.find("**T2.** A fixed-base arm works inside the table's footprint.")
_j2 = t.find("\n\n", _i2)
if _tm.get("pi05") and _tm.get("scripted") and _tm.get("pi05_pp") and _i2 > 0 and _j2 > _i2 and "taken from link origins, and a link's surface" not in t:
    _pct = lambda s_: f"{round(100 * int(s_.split('/')[0]) / int(s_.split('/')[1]))} %"
    t = t[:_j2] + (" The distance is taken from link origins, and a link's surface lies roughly 4–8 cm out, so a 0.10 m margin to the "
                   "surface is a 0.14–0.18 m margin to the origins: there π0.5's rate is " + _pct(_tm["pi05"]["0.14"]) + " and "
                   + _pct(_tm["pi05"]["0.18"]) + " (" + _tm["pi05"]["0.14"] + ", " + _tm["pi05"]["0.18"] + "); on the pick-and-place "
                   "cells the person-blind control ran, " + _pct(_tm["pi05_pp"]["0.14"]) + " and " + _pct(_tm["pi05_pp"]["0.18"])
                   + " against the control's " + _pct(_tm["scripted"]["0.14"]) + " and " + _pct(_tm["scripted"]["0.18"])
                   + " (at 0.10 m " + _tm["pi05_pp"]["0.1"] + " against " + _tm["scripted"]["0.1"] + "). Both rise with the margin, and at no "
                   "margin does the policy differ detectably from the control (two-sided Fisher *p* ≥ " + _tm.get("p_min", "—") + ").") + t[_j2:]
elif not _tm.get("pi05"):
    print("  [a172] no t2_margin")
else:
    print("  [a172 MISS] E tabletop T2 paragraph")
