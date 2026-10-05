# -*- coding: utf-8 -*-
# T6b witness (queues ikwkwa/ikwkwb, 2026-10-05): the blind straight-line carrier that holds while the walker is within 0.6 m of
# its remaining path, the walker leaving 3 s after the lift so it meets the slow scripted transport midway (ik_wkwait_*), and
# the same carrier without the hold (ik_wkd_*). If the hold makes the carry "slowed" at the closest approach and it still
# delivers, T6b has a witness: Table IIIf's note, the Table III caption's witness list and the 4.2 unattributed list change.
# Exec'd after a176 (uses t, _rn2, V).
_tw = V.get("t6b_witness") or {}


def _r6(s_):
    try:
        k_, n_ = (int(x) for x in s_.split("/"))
        return (k_ / n_) if n_ else None, n_
    except Exception:  # noqa: BLE001
        return None, 0


if _tw.get("cells", 0) >= 4:
    (_rw, _nw), (_rd, _nd) = _r6(_tw["T6b"]), _r6(_tw["delivered"])
    _ok = _rw is not None and _nw >= 8 and _rw <= 0.25 and _rd is not None and _rd >= 0.5
    _txt = (" A straight-line carry that holds while the walker is within 0.6 m of its remaining path (the walker leaving 3 s after the "
            "lift, so it meets the scripted transport midway) is passed unslowed on " + _tw["T6b"] + " scored encounters and delivers "
            + _tw["delivered"] + "; without the hold the same carry is unslowed on " + _tw["blind_T6b"] + " (delivers "
            + _tw["blind_delivered"] + ")" + (": the T6b witness." if _ok else ", so the hold does not yet give T6b a witness."))
    _rn2("not distinguishable, and not safer.", "not distinguishable, and not safer." + _txt)
    if _ok:
        _rn2("T6b and G1 T2–T4 have no witness (unattributed);", "G1 T2–T4 have no witness (unattributed);")
        _rn2("T5a (G1), T5b and T6 (both).", "T5a (G1), T5b and T6 (both), T6b (tabletop).")
else:
    print("  [a177] T6b witness not in yet")
