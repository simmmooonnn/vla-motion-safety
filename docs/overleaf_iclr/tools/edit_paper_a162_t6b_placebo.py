# -*- coding: utf-8 -*-
# ICLR-readiness review (wf_425459e6-f4b, item 7(2)): T6b had no null. The phase-matched placebo reads the same predicate on
# carries with no passer-by, at the same delay after the lift as each scored closest approach (analyze_fr t6b_plc_dk, mv_dk):
# a person-blind carry would be "not slowed" there on ~70 %, so the policy's 78 % is the absence of slowing, not a rate the
# policy adds. Exec'd after a161 (uses t, _rn2, V).
_pl = V.get("t6b_placebo_pi05") or {}
if _pl.get("phase_expected_pct"):
    _rn2("97/125 carried episodes (closest 0.44–0.94 m) — no anticipatory slowing, as on the G1, where no deceleration precedes any of "
         "the 11 contacts.",
         _pl["observed"] + " carried episodes (closest 0.44–0.94 m), where a carry blind to the person, read at the same moment after "
         "the lift, would be on " + _pl["phase_expected_pct"] + " % (binomial *p* = " + _pl["phase_p"] + "): no anticipatory slowing, as "
         "on the G1, where no deceleration precedes any of the 11 contacts.")
    _rn2("The tabletop T5a and T5b are exposure and T6b has no control, so they have no row.",
         "The tabletop T5a and T5b are exposure, so they have no row; T6b has no control, and against a phase-matched placebo (the same "
         "predicate on carries with no passer-by, at the same delay after the lift) π0.5 reads " + _pl["observed"] + " against "
         + _pl["phase_expected_pct"] + " % (binomial *p* = " + _pl["phase_p"] + "): not distinguishable, and not safer.")
