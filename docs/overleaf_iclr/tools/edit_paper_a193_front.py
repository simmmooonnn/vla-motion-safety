# -*- coding: utf-8 -*-
# 2026-10-09 (a193, front region: Abstract, Introduction, sections 2-4). Applies the verified findings of
# _scratch/tmp/now_results.json (each entry's 'check' block taking precedence) to the front matter, without growing it.
#  F6 (power_tost): of Table IIIf's 12 rows only 3 could have yielded a Holm-significant 'safer' verdict; the small T3 rows and
#     the T4 rows could not show a policy safer -> abstract and contribution 3 now say 'where a safer verdict was attainable',
#     and 4.2 defines an *untested* row.
#  F1 (fk_arc) + F2 (t1_offset): T1 is a consistent far-side bend (mid-transport means 4.2-12.7 cm, control -0.1 cm); its excess
#     over the control depends on the control being a Cartesian line (a modelled blind joint-space carry: about 80/160 against
#     pi0.5's 90/159, Fisher p 0.26). A model prediction, not a run, and the policy is NOT said to interpolate in joint space.
#     Abstract, contribution 3 and 4.2 (Attribution) qualify 'worse than the control' on T1 accordingly.
#  F3 (t2_cond): T2's placement-matched stratum is DELIVERED (pi0.5 26/56, pi0-FAST 32/56, GR00T-DROID 14/14 against the
#     control's 0/24); pi0's 0/57 is a capability boundary (it brings the mug to the bowl on 3/57), so it is no longer paired with
#     the control as 'none'. The pre-registered numbers (26/60, 34/64, 51/54 against 0/64) are kept as they are. Abstract, 4.2.
#  F4 (g0_cut35): GR00T-DROID's T4 36/97 over 90 s is 18/57 = 32 % in its first 35 s -> contribution 3.
#  F5 (t5a_vh0): left to 5.3 (results region); see the note at 4.2 (Dimension score).
#  F7 (dose_strat): the spill-clause tilt builds mainly late in transport; 'keep the mug upright' alone is given beside the neutral
#     counts (the direct spill-vs-upright test belongs to the results text) -> abstract; 4.2 (Fixability) names the stratified
#     cell-level permutation over the prompt experiments beside Fisher.
#  Offsets, so that the main text shrinks (front delta -13 words after the skeptic pass): the intro's 'incomplete in the same way' sentence pair, the
#     'Why this is not collision avoidance' external-layer clause, section 2's pointer, hypothesis and novelty sentences tightened
#     (meaning kept); 3.2's closing sentence on lower layers dropped (the introduction makes the point); 4.2's figure gloss for
#     fig:scatter and 'rather than one cell' dropped; contribution 3's 'body sweep varies by policy (2-71 %)' dropped (pi0's 2 % is
#     a capability boundary, F3); the abstract's 'no other difference survives Holm' clause dropped (superseded by the
#     attainability wording, F6).
# Exec'd at the end of the chain (uses t, _rn2).

# ---- Abstract: the control is a Cartesian line (F1)
_rn2("against a person-blind control (a scripted straight-line carry) and a witness",
     "against a person-blind control (a scripted Cartesian straight-line carry) and a witness")

# ---- Abstract: headline, T1, T2 (F6, F1/F2, F3)
_rn2("**none is detectably safer than the person-blind control on any sub-type both ran**; all four bow into a keep-out beside "
     "the transport that the control rarely enters (π0.5 90/159 against 18/160), and no other difference survives Holm correction "
     "over 12 matched comparisons; pre-registered tests add the body sweep: π0.5's, π0-FAST's and GR00T N1.6-DROID's arms come within "
     "0.10 m of a bystander beside the bowl on 26/60, 34/64 and 51/54 episodes, π0's and the control's on none (0/57, 0/64).",
     "**where a safer verdict was attainable, none is detectably safer than the person-blind control**. All four bend to the "
     "transport's far side (mean 4–13 cm), into a keep-out that the control rarely enters (π0.5 90/159 against 18/160) but a "
     "modelled blind joint-space carry would (about 80/160). Pre-registered tests add the body sweep: π0.5's, π0-FAST's and GR00T N1.6-DROID's "
     "arms come within 0.10 m of a bystander beside the bowl on 26/60, 34/64 and 51/54 episodes against the control's 0/64 "
     "(delivered: 26/56, 32/56, 14/14 against 0/24); π0's on 0/57, bringing the mug to the bowl too rarely to tell (3/57).")

# ---- Abstract: prompt sentence (F7)
_rn2("tilt the mug past 45° on 30/32 and 14/27 carries (neutral 3/32, 0/32), π0 on 10/12 (1/13; mostly one cell), GR00T "
     "N1.6-DROID not detectably (2/9, 6/12), while \"keep the mug upright\" alone does not detectably raise π0.5's or π0-FAST's "
     "(5/32, 1/31).",
     "tilt the mug past 45°, mainly late in transport, on 30/32 and 14/27 carries (neutral 3/32, 0/32; \"keep the mug upright\" "
     "alone 5/32, 1/31), π0 on 10/12 (1/13; mostly one cell), GR00T N1.6-DROID not detectably (2/9, 6/12).")

# ---- Introduction, paragraph 1 (offset)
_rn2("Both are worthwhile, and both are incomplete in the same way. They judge the endpoints of behavior and say nothing about the "
     "physical process in between.",
     "Both are worthwhile, and both judge only the endpoints of behavior, not the physical process in between.")

# ---- Introduction, 'Why this is not collision avoidance' (offset, meaning kept)
_rn2("speed-and-separation monitoring and force limiting sit in an external layer the policy leaves to do all the work;",
     "speed-and-separation monitoring and force limiting are left wholly to an external layer;")

# ---- Contribution 3 (F6, F1/F2, F3, F4)
_rn2("none detectably safer than the person-blind control on any sub-type both ran and all worse on the keep-out (three also on "
     "the body sweep, one pre-registered cell), and a humanoid case study (GR00T N1.6, G1); the well-sampled policies' payload "
     "orientation ignores the person, none tested avoids a moving person or hand, body sweep varies by policy (2–71 %), and GR00T "
     "N1.6-DROID tilts a cup (37 %; its matched excess does not survive Holm correction) where the humanoid's box stays level.",
     "none detectably safer than the person-blind control where a safer verdict was attainable, all entering a keep-out beside the "
     "transport more often than its Cartesian straight carry, three sweeping the body at one pre-registered cell, and a humanoid "
     "case study (GR00T N1.6, G1); the well-sampled policies' payload orientation ignores the person, none tested avoids a moving "
     "person or hand, and GR00T N1.6-DROID tilts a cup (37 %, 32 % within 35 s; its matched excess not significant after Holm) "
     "where the humanoid's "
     "box stays level.")

# ---- Section 2 (offsets, meaning kept)
_rn2("The competence is simply *absent from the training distribution* — our mechanistic hypothesis for the findings of §6, on "
     "which prompting or perception cannot retrieve a behavior that was never represented. It is a hypothesis, and two concurrent "
     "results bear on it:",
     "Our hypothesis for the findings of §6 is that the competence is *absent from the training distribution*, so prompting or "
     "perception cannot retrieve it; two concurrent results bear on this:")
_rn2("We add the human reference with attribution: every sub-type is scored on a trajectory quantity, mostly person-referenced, "
     "and, where available, read against a person-blind control and a feasibility witness, with fixability ablations where the "
     "rate can move, and a humanoid case study.",
     "We add the human reference with attribution: mostly person-referenced trajectory quantities read, where available, against "
     "a person-blind control and a feasibility witness, with fixability ablations and a humanoid case study.")

# ---- 3.2 closing sentence (offset; the introduction's 'Why this is not collision avoidance' makes the point)
_rn2(" Each dimension also names a risk that layers below the policy — collision checker, protective stop, force limit — at best "
     "intercept (Appendix B).", "")

# ---- 4.2 Unsafe rate: T2's placement-matched stratum and pi0's capability boundary (F3); 'untested' rows (F6); offset
_rn2("the destination 0.28–0.35 m beside the person, the placement that brings the arm to them (§5.1) — not over carries, since "
     "the arm can sweep without carrying.", "the destination 0.28–0.35 m beside the person (§5.1) — not over carries, since the "
     "arm can sweep without carrying.")
_rn2("transport sub-types condition on carried (E.8).",
     "transport sub-types condition on carried, and T2's placement-matched reading on delivered; where a policy rarely delivers, "
     "its T2 measures competence, not safety (§4.1, E.8).")
_rn2("Holm-corrected over Table IIIf's 12 rows (the primary family),",
     "Holm-corrected over Table IIIf's 12 rows (the primary family; a row is *untested* where no data could make a safer verdict "
     "significant and its one-sided bound allows one),")
_rn2("{fig:scatter}: ablation cells' completion against unsafe rate).", "{fig:scatter}).")

# ---- 4.2 Dimension score (F5): no edit here. 'Under the envelope's walking-human term' was dropped by the skeptic pass: the
#     envelope is first defined in 5.3, and the tabletop's speed-and-force exposure also covers T5b (a constraint force), which
#     that term does not govern; 5.3 (results region) carries the walking-human qualification.

# ---- 4.2 Fixability: the wording effect is also tested by cells permuted within experiments (F7)
_rn2("(seven phrasings against neutral, Fisher on carries; Table XIII)",
     "(seven phrasings against neutral, Fisher on carries and cell permutation within experiments; Table XIII)")

# ---- 4.2 Dimension score (offset)
_rn2("in which its predicate is *available* rather than one cell;", "in which its predicate is *available*;")

# ---- Section 2, instruction-level (offset)
_rn2("(The VLA lineage and the classical motion-safety machinery this work builds on are summarized in Appendix G.)",
     "(Appendix G summarizes the VLA lineage and the classical motion-safety machinery.)")

# ---- 4.2 Attribution: the control is a Cartesian line (F1/F2)
_rn2("The *person-blind control*, a scripted straight-line carry that reads the scene but not the person, measures what ignoring "
     "the person yields;",
     "The *person-blind control*, a scripted Cartesian straight-line carry that reads the scene but not the person, measures what "
     "ignoring the person yields on that path (a joint-space path would bend, §5.1);")
