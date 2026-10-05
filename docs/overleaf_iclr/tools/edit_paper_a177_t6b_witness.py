# -*- coding: utf-8 -*-
# T6b witness (queues ikwkwa/ikwkwb, 2026-10-05): the blind straight-line carrier that holds while the walker is within 0.6 m of
# its remaining path, the walker leaving 3 s after the lift so it meets the slow scripted transport midway (ik_wkwait_*), and
# the same carrier without the hold (ik_wkd_*). As for T3 and T4 (t3_ok_done, t4_ok_done), the witness is a compliant
# completion in the scene: a scored closest approach at which the payload is slowed, in an episode that delivers. With at
# least three, T6b has a witness: Table IIIf's note, the Table III caption's witness list and the 4.2 unattributed list change.
# Exec'd after a176 (uses t, _rn2, V).
_tw = V.get("t6b_witness") or {}

if _tw.get("cells", 0) >= 4:
    _ok = int(_tw.get("ok_done", 0)) >= 3
    _txt = (" A straight-line carry that holds while the walker is within 0.6 m of its remaining path (the walker leaving 3 s after the "
            "lift, so it meets the scripted transport midway) is passed unslowed on " + _tw["T6b"] + " scored encounters, and "
            + str(_tw.get("ok_done", 0)) + " of the slowed carries deliver the mug (delivered " + _tw["delivered"] + " in all); without "
            "the hold the same carry is unslowed on " + _tw["blind_T6b"] + " (" + str(_tw.get("blind_ok_done", 0)) + " slowed and "
            "delivered)" + (": a compliant completion exists, the T6b witness." if _ok else ", so the hold does not yet give T6b a witness."))
    _rn2("not distinguishable, and not safer.", "not distinguishable, and not safer." + _txt)
    if _ok:
        _rn2("T6b and G1 T2–T4 have no witness (unattributed);", "G1 T2–T4 have no witness (unattributed);")
        _rn2("T5a (G1), T5b and T6 (both).", "T5a (G1), T5b and T6 (both), T6b (tabletop).")
        _rn2("a pinch grasp (T4) and a stop (T6)", "a pinch grasp (T4), a stop (T6) and a hold (T6b)")
else:
    print("  [a177] T6b witness not in yet")
