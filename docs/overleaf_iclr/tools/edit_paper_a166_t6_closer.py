# -*- coding: utf-8 -*-
# ICLR-readiness review (item 7(4)): who closed the gap in the scored crossing-hand contacts. Over the second before contact
# the gap's change is split into the hand's share (payload held where it was) and the payload's (hand held where it was);
# the hand moves along its own axis, so the payload closes it. E.8, after the policy rates. Exec'd after a165 (uses t, _rn2, V).
_c5 = V.get("hx_pi05") or {}; _cf = V.get("hx_pi0fast") or {}
_i6 = t.find("and holds still for 0.5 s or more on ")
_j6 = t.find(" With the hand neither rendered nor colliding", _i6)
if _c5.get("closer_payload") and _i6 > 0 and _j6 > _i6 and "The payload closes the gap, not the hand" not in t:
    t = t[:_j6] + (" The payload closes the gap, not the hand: over the second before contact the payload's own motion shrinks it "
                   "by a median " + _c5["dg_pay_med"].lstrip("-") + " m and the hand's by " + _c5["dg_hand_med"].lstrip("-")
                   + " m, and the payload alone closes it on " + _c5["closer_payload"] + " of π0.5's contacts (the hand alone on "
                   + _c5.get("closer_hand", "—") + "; π0-FAST " + _cf.get("closer_payload", "—") + ").") + t[_j6:]
elif not _c5.get("closer_payload"):
    print("  [a166] no closer fields yet (pull with the 2026-10-05 analyzer)")
else:
    print("  [a166 MISS] E.8 crossing paragraph")
