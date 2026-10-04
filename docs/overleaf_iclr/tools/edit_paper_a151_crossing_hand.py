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
    _hr = V.get("hx_pi05_witness_release"); _wt = V.get("hx_scripted_wait")
    if _wt:
        _p += ("A straight-line carry that holds while the hand is within 0.04 m of its remaining path and then resumes reaches it "
               "on " + _wt["reach"] + " and delivers " + _wt["completed"] + "/" + _wt["att"]
               + ((" (the same carry without waiting " + _ik["completed"] + "/" + _ik["att"] + ")") if _ik else "")
               + ": waiting finishes the task without touching the hand. ")
    if _hw or _hr:
        _p += "A whole-arm protective stop is blunter: "
        if _hw:
            _p += ("with a 0.10 m margin and 0.05 m hysteresis the payload reaches the hand on " + _hw["reach"] + ", but the arm "
                   "stays held while the withdrawn hand is parked 0.1 m from the line (" + _hw["completed"] + "/" + _hw["att"]
                   + " delivered)")
        if _hr:
            _p += (("; " if _hw else "") + "releasing at 0.08 m delivers " + _hr["completed"] + "/" + _hr["att"] + " but lets the "
                   "payload reach the hand on " + _hr["reach"])
        _p += ". "
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
    _rn2("On the tabletop T1 is the off-path keep-out and T2 the serving geometry (§5.1).",
         "On the tabletop T1 is the off-path keep-out, T2 the serving geometry (§5.1), and T6 pools the hand reaching into the "
         "destination and the hand crossing the transport line (E.8).")
