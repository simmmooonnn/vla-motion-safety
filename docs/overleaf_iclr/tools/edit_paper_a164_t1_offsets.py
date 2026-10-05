# -*- coding: utf-8 -*-
# ICLR-readiness review (wf_425459e6-f4b, item 12): the tabletop T1 pools two regimes -- at 0.20 m a straight carry grazes the
# radius, at 0.28 m it clears it -- so 5.1 gives each offset with the control's. Exec'd after a163 (uses t, _rn2, V).
_o = V.get("t1_by_off") or {}
if _o.get("pi05") and _o.get("scripted"):
    _rn2("On the tabletop the scored T1 is a marker or a bystander's resting hand 0.20 or 0.28 m *beside* the transport, offsets a "
         "direct carry clears: π0.5 enters it on " + V["pi_T1"] + " against the blind carrier's " + V["ik_T1"] + ".",
         "On the tabletop the scored T1 is a marker or a bystander's resting hand 0.20 or 0.28 m *beside* the transport: a direct "
         "carry grazes the first (the blind carrier enters it on " + _o["scripted"]["20"] + ") and clears the second ("
         + _o["scripted"]["28"] + "), and π0.5 enters them on " + _o["pi05"]["20"] + " and " + _o["pi05"]["28"] + " ("
         + V["pi_T1"] + " in all) — the policy's bow toward the far side, present without any keep-out, sets the rate (E.8).")

# page budget: details that the appendix carries
_rn2("With the bystander beside the workspace at four positions (*N* = 8 each), a robot link comes within 0.10 m of the body "
     "surface on 27/32 episodes and touches it on 19/32 — the hands at the right pick and the drop, the shoulder at the left — "
     "where a margin to the person's *axis* registers only 8/32. The rate is set by the scoring geometry as much as by the policy "
     "(Fig. \\ref{fig:t4thr}), so we report the threshold curve and the contact count (Appendix E.3).",
     "With the bystander beside the workspace (four positions, *N* = 8 each), a robot link comes within 0.10 m of the body surface "
     "on 27/32 episodes and touches it on 19/32, where a margin to the person's *axis* registers only 8/32; the rate is set by the "
     "scoring geometry as much as by the policy (threshold curve: Fig. \\ref{fig:t4thr}, E.3).")
_rn2("(6/6 matched, 16/16 on the §5.1 person cell: closest 0.16 m at 0.29 m/s, and faster inside 0.60 m than beyond, 0.247 vs "
     "0.202 m/s; Fig. \\ref{fig:ssm})", "(6/6 matched, 16/16 on the §5.1 person cell; Fig. \\ref{fig:ssm})")
_rn2("On π0.5 a spatial command leaves the plow-through at 15/16 against 14/16 but cuts success to 62 %, and in one session "
     "keep-the-hot-coffee-upright", "In one session keep-the-hot-coffee-upright")
