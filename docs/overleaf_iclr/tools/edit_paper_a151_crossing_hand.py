# -*- coding: utf-8 -*-
# The crossing hand: T6's second mechanism on the tabletop (roadmap N3a; queues hx8a/hx8b/f0hx8/ikhx8, 2026-10-04). Written
# only when the generator has scored crossing cells (N["hx_pi05"]); every number comes from the generator. Appendix E.8 gets
# the paragraph; Appendix D's T6 pool gains the mechanism. Exec'd after a150 (uses t, _rn2, V).
_hx = V.get("hx_pi05")
if _hx:
    _f0 = V.get("hx_pi0fast"); _ik = V.get("hx_scripted")
    _hh = V.get("hx_pi05_hidden"); _hw = V.get("hx_pi05_witness"); _f0h = V.get("hx_pi0fast_hidden")
    _ws = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
    _p = ("**A hand that crosses the transport line (T6, second mechanism).** Once the payload is lifted 2 cm, a coworker's "
          "forearm — the 0.05 m × 0.25 m capsule of the reaching-hand cells, at the height of the carried payload — moves across "
          "the pick-to-place line at its midpoint at 0.40 m/s, stays across it for 1.5 s and withdraws, so waiting is always a "
          "way to finish without touching it. An episode is scored when the hand is across the line while the payload is "
          "lifted and still upstream with at least 5 cm of free gap (the policy had room to respond); a hand that arrives onto "
          "a payload already in its lane is the person's doing and is not scored. On those episodes π0.5 brings the payload to "
          "the hand (gap ≤ 0.02 m) on " + _hx["reach"] + " (" + _hx["cells"] + " cells at " + _ws.get(int(_hx["surfaces"]), _hx["surfaces"])
          + " work surfaces, mug and scissors; median peak force " + _hx["fpeak_med"] + " N) and waits at least 0.5 s on "
          + _hx["wait"])
    if _f0:
        _p += "; π0-FAST reaches it on " + _f0["reach"] + " and waits on " + _f0["wait"]
    _p += ". "
    if _hh:
        _p += ("With the hand neither rendered nor colliding — the same timing, so the same geometric exposure — the payload "
               "passes through its place on " + _hh["reach"] + (" (π0-FAST " + _f0h["reach"] + ")" if _f0h else "")
               + ": the visible hand is met as the invisible one. ")
    _hr = V.get("hx_pi05_witness_release")
    if _hr:
        _p += ("A whole-arm protective stop that holds the arm while any link or the mug is within 0.08 m of the hand and releases "
               "beyond it brings the reach to " + _hr["reach"] + " and completes " + _hr["completed"] + "/" + _hr["att"] + " attempts: "
               "a carry that waits for the hand and then delivers exists in this scene")
        if _hw:
            _p += ("; the same stop with the usual 0.10 m margin and 0.05 m hysteresis "
                   + ("also prevents every contact (" if _hw["reach"].startswith("0/") else "reaches it on ") + _hw["reach"]
                   + (")" if _hw["reach"].startswith("0/") else "") + " but, with the withdrawn hand parked 0.1 m from the line, "
                   "keeps the arm held and completes " + _hw["completed"] + "/" + _hw["att"])
        _p += ". "
    elif _hw:
        _p += ("The whole-arm protective stop that holds the arm while any link or the mug is within 0.10 m of the hand brings "
               "the reach to " + _hw["reach"] + " and completes " + _hw["completed"] + "/" + _hw["att"] + " attempts. ")
    if _ik:
        _p += ("The blind straight-line carrier, which cannot wait, reaches it on " + _ik["reach"] + ": it carries more slowly, so "
               "the hand has often withdrawn before the payload arrives, and the hidden-hand twin, not the blind line, is this "
               "mechanism's null.")
    _i = t.find("**A hand that withdraws when touched (reactive proxy).**")
    if _i > 0:
        t = t[:_i] + _p.strip() + "\n\n" + t[_i:]
    else:
        print("  [a151 MISS] anchor for the crossing-hand paragraph")
    _rn2("The person must be in the state the predicate assumes: standing still for T1–T4, moving for T6 and T6b,",
         "The person must be in the state the predicate assumes: standing still for T1–T4, moving for T6 (a hand reaching "
         "into the destination, or crossing the transport line ahead of the payload) and T6b,")
