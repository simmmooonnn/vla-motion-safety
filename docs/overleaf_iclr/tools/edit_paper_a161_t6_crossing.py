# -*- coding: utf-8 -*-
# ICLR-readiness review (wf_425459e6-f4b, item 7): the tabletop T6 is the hand crossing the transport line; the hand reaching
# into the bowl stays there, so delivery itself demands the contact (blind carrier 16/16) and that cell is exposure. Every
# number from V. Exec'd after a160 (uses t, _rn2, V).
_hh = V.get("hx_pi05_hidden") or {}; _hw = V.get("hx_pi05_witness") or {}; _f0 = V.get("hx_pi0fast") or {}
_old = t.find("On the tabletop π0.5 lowers the mug onto a coworker's hand reaching into the bowl on ")
_end = t.find("**T6b**", _old)
if _old > 0 and _end > _old and V.get("T6_wait_pi05"):
    t = t[:_old] + ("On the tabletop the scored T6 is a coworker's forearm crossing the transport line ahead of the payload: π0.5 "
                    "carries into it on " + V["pi_T6"] + " and waits on " + V["T6_wait_pi05"] + " (pouring included; π0-FAST "
                    + _f0.get("reach", "—") + " and " + V.get("T6_wait_pi0fast", "—") + "). With the hand neither rendered nor colliding "
                    "the payload passes through its place as often (" + _hh.get("reach", "—") + "), and a whole-arm stop removes the "
                    "contact (" + _hw.get("reach", "—") + ") and still delivers (" + _hw.get("completed", "—") + "/" + _hw.get("att", "—")
                    + "): the null and the witness (E.8). A hand reaching into the bowl is lowered onto on " + V["pi_T6_hand"]
                    + " carried episodes, but there delivery itself demands the contact (the blind carrier 16/16), so that cell is "
                    "exposure. ") + t[_end:]
else:
    print("  [a161 MISS] 5.4 tabletop T6")
_rn2("and T6 pools the hand reaching into the destination (every carried episode) and the hand crossing the transport line (the "
     "episodes in which it crosses ahead of the payload; E.8); the control's T6 is the reaching hand alone.",
     "and T6 the hand crossing the transport line (the episodes in which it crosses ahead of the payload); the hand reaching into "
     "the destination, whose delivery forces the contact, is exposure (E.8).")
