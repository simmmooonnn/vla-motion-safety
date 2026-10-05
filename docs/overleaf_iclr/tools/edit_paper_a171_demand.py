# -*- coding: utf-8 -*-
# ICLR-readiness review (item 18): "demand" made operational where a stop is instrumented -- the share of carries on which the
# whole-arm protective stop fires and how long it holds the arm. E.8, the crossing-hand witness sentence. Exec'd after a170
# (uses t, _rn2, V).
_dm = (V.get("stop_demand") or {}).get("crossing") or {}
if _dm.get("held_med", "—") != "—":
    _rn2("A whole-arm protective stop (0.10 m margin, 0.05 m hysteresis) brings the reach to 0/16 and the touch to 0/16, and delivers 16/16.",
         "A whole-arm protective stop (0.10 m margin, 0.05 m hysteresis) brings the reach to 0/16 and the touch to 0/16, and delivers "
         "16/16. It fires on " + _dm["fired"] + " carries and holds the arm a median " + _dm["held_med"] + " s each: the *demand* "
         "π0.5's carry places on the layer, read off as how often the stop must act and for how long.")
else:
    print("  [a171] no stop demand yet")
