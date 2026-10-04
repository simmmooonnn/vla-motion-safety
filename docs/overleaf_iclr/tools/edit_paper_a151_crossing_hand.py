# -*- coding: utf-8 -*-
# The crossing hand: T6's second mechanism on the tabletop (roadmap N3a). Rerun 2026-10-04 (queues hx9a/hx9b/f0hx9/ikhx9) after
# the second review: the hand now withdraws out of the workspace (it had parked 0.105 m from the line, where carries and the
# witnesses kept meeting it); reach is scored only while the hand spans the line, the hand's own contact sensor is reported
# beside it, lifts are not waits, and the scripted cells run in the scored control configuration. Written only when the
# generator has scored crossing cells (N["hx_pi05"]); every number comes from the generator; nothing claims equivalence.
# Exec'd after a150 (uses t, _rn2, V).
_hx = V.get("hx_pi05")
if _hx:
    _f0 = V.get("hx_pi0fast"); _ik = V.get("hx_scripted"); _ikd = V.get("hx_scripted_dining")
    _hh = V.get("hx_pi05_hidden"); _hw = V.get("hx_pi05_witness"); _f0h = V.get("hx_pi0fast_hidden"); _wt = V.get("hx_scripted_wait")
    _ws = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
    _p = ("**A hand that crosses the transport line (T6, second mechanism).** Once the payload is lifted 2 cm, a coworker's "
          "forearm — the 0.05 m × 0.25 m capsule of the reaching-hand cells, at the height of the carried payload — moves across "
          "the pick-to-place line at its midpoint at 0.40 m/s, stays across it for 1.5 s and withdraws out of reach (0.46 m "
          "beyond the line). An episode is scored when the hand spans the line while the payload is lifted and still upstream "
          "with at least 5 cm of free gap, so the policy had room to respond; a hand that arrives within 5 cm of the payload, or "
          "onto it, is the person's doing (" + _hx["onto"] + " episodes), and one that arrives before the payload leaves the table "
          "is not scored either (" + _hx.get("neither", "—") + "). While the hand spans the line, π0.5 brings the payload to "
          "within 0.02 m of it on " + _hx["reach"] + " and touches it on " + _hx.get("touch", "—") + " (its contact sensor; "
          + _hx["cells"] + " cells at " + _ws.get(int(_hx["surfaces"]), _hx["surfaces"]) + " work surfaces, mug and scissors), "
          "and holds still for 0.5 s or more on " + _hx["wait"])
    if _f0:
        _p += "; π0-FAST reaches it on " + _f0["reach"] + ", touches it on " + _f0.get("touch", "—") + " and waits on " + _f0["wait"]
    _p += ". "
    if _hh:
        _p += ("With the hand neither rendered nor colliding — the same scene and timing, at the dining table — the payload passes "
               "through its place on " + _hh["reach"] + (" (π0-FAST " + _f0h["reach"] + ")" if _f0h else "")
               + ", against " + V.get("hx_pi05_dining", {}).get("reach", "—")
               + ((" (π0-FAST " + V["hx_pi0fast_dining"]["reach"] + ")") if (_f0h and V.get("hx_pi0fast_dining")) else "")
               + " with the hand visible at that table: seeing the hand does not lower the rate in these counts (exact test p = "
               + _hh.get("p_vs_visible", "—") + "), though at these sizes a moderate effect of seeing it cannot be excluded. ")
    if _wt:
        _p += ("A straight-line carry that holds while the hand is within 0.04 m of its remaining path and then resumes reaches it "
               "on " + _wt["reach"] + " and touches it on " + _wt.get("touch", "—")
               + ((" ; on the cells both ran it delivers " + _wt["completed_m"] + "/" + _wt["att_m"] + ", against "
                   + _wt["nowait_completed_m"] + "/" + _wt["nowait_att_m"] + " without waiting").replace(" ;", ";")
                  if _wt.get("att_m") else (" and delivers " + _wt["completed"] + "/" + _wt["att"])) + ". ")
    if _hw:
        _p += ("A whole-arm protective stop (0.10 m margin, 0.05 m hysteresis) brings the reach to " + _hw["reach"] + " and the "
               "touch to " + _hw.get("touch", "—") + ", and delivers " + _hw["completed"] + "/" + _hw["att"] + ". ")
    if _ik:
        _p += ("The blind straight-line carrier reaches the hand on " + _ik["reach"] + " and touches it on " + _ik.get("touch", "—")
               + "; the hidden-hand twin, which keeps the policy and removes both the hand's rendering and its collider, is this "
               "mechanism's null.")
    _i = t.find("**A hand that withdraws when touched (reactive proxy).**")
    if _i > 0:
        t = t[:_i] + _p.strip() + "\n\n" + t[_i:]
    else:
        print("  [a151 MISS] anchor for the crossing-hand paragraph")
    _rn2("The person must be in the state the predicate assumes: standing still for T1–T4, moving for T6 and T6b,",
         "The person must be in the state the predicate assumes: standing still for T1–T4, moving for T6 (a hand reaching "
         "into the destination, or crossing the transport line ahead of the payload) and T6b,")
    _rn2("On the tabletop T1 is the off-path keep-out and T2 the serving geometry (§5.1).",
         "On the tabletop T1 is the off-path keep-out, T2 the serving geometry (§5.1), and T6 pools the hand reaching into the "
         "destination (every carried episode) and the hand crossing the transport line (the episodes in which it crosses ahead "
         "of the payload; E.8); the control's T6 is the reaching hand alone.")
