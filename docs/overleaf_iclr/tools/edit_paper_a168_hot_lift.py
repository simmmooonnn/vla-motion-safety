# -*- coding: utf-8 -*-
# ICLR-readiness review (item 10): the hot-coffee instruction changes the carry, not the grasp. One second after the lift the
# mug's tilt is the same under both instructions; the tilt past 45 deg builds during the transport. E, T4 paragraph. Exec'd
# after a167 (uses t, _rn2, V).
_hl = V.get("hot_lift") or {}
_hh, _hn = _hl.get("hot") or {}, _hl.get("neutral") or {}
if _hh.get("n") and _hn.get("n"):
    _rn2("and the date moves the neutral rate only a little (office 0/8 on 2026-09-16, 2/8 now).",
         "and the date moves the neutral rate only a little (office 0/8 on 2026-09-16, 2/8 now). The instruction changes the carry, "
         "not the grasp: one second after the lift the mug stands at a median " + _hh["l1_med"] + "° under the hot-coffee "
         "instruction and " + _hn["l1_med"] + "° under the neutral one, and of the " + _hh["over"] + " hot-coffee carries that pass "
         "45° in transport " + _hh["over_at_lift"] + " had done so by then (" + str(_hh["n"]) + " carries; neutral "
         + _hn["over_at_lift"] + " of " + _hn["over"] + (f"; on the prompt control's new seeds {_hl['pv_C']['over_at_lift']} of the "
         f"{_hl['pv_C']['over']} under the keep-upright sentence" if _hl.get("pv_C", {}).get("n") else "") + ").")
else:
    print("  [a168] no tilt_l1 yet (pull with the 2026-10-05 analyzer)")
