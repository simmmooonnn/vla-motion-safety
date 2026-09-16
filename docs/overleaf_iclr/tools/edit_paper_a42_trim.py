# -*- coding: utf-8 -*-
# Page-budget trims for the 2026-09-15 evening round (exec'd after edit_paper_a41_trim.py; uses R, N, t). No claim removed:
# the driver numbers stay in Appendix E.7, the guard remark in §9's scope sentence.

# §8: the driver confound keeps its consequence, the numbers are in Appendix E.7
R("Cells run 2026-09-08 to 09-14 used a substitute driver under which pick success fell (32 % of episodes carried versus 71 % before); their conditional rates are unaffected, their completion rates not comparable (Appendix E.7).",
  "Cells run 2026-09-08 to 09-14 used a substitute driver that lowered pick success; their conditional rates are unaffected (Appendix E.7).")
# §7
R("A general guard, and its cost in efficiency, is outside the scope of a benchmark and left to future work; the external layers here are instruments.",
  "A general guard is left to future work; the external layers here are instruments.")
# §6 hypothesis
R("The hypothesis is falsifiable; the non-ceiling ablation is its first test, and the evidence is consistent with it but not decisive.",
  "It is falsifiable; its first test, the non-ceiling ablation, is consistent with it but not decisive.")

# §5.5: the scope caveat keeps its point in fewer words
R("This is portability across embodiment, policy and task, not a matched ranking.",
  "This is portability, not a matched ranking.")
# §5.1: the pooled T1 list
R("pooled over three hazards, three seeds, three positions, photorealistic YCB objects and a two-hazard scene, 109/109",
  "pooled over three hazards, three seeds, three positions and a two-hazard scene, 109/109")
# §5.2 T4: GR00T's null
R("GR00T's rigid box stays near-level in transit (0/17 above 45°), its grasp and release tilts (median " + N['g_t4_end'] + ") unchanged by a cup-of-water or keep-level instruction (Appendix E.5).",
  "GR00T's rigid box stays near-level in transit (0/17), its grasp and release tilts (median " + N['g_t4_end'] + ") unchanged by either instruction (Appendix E.5).")

# §5.1: the shield witness in fewer words
R("A repulsion shield handed the hazard's coordinates clears it (8/8 → 0/8, Fisher *p* = 1.6 × 10⁻⁴, completion unchanged; Fig. \\ref{fig:shield}) — the witness that a clearing path exists (Appendix E.2).",
  "A repulsion shield given the hazard's coordinates clears it (8/8 → 0/8, *p* = 1.6 × 10⁻⁴, completion kept; Fig. \\ref{fig:shield}) — the witness that a clearing path exists (E.2).")
# §5.4: the collider-off control stays in Appendix E.8
R(N['pi_t6_nocol_clause'], "")
# §9: the conclusion keeps every claim, in fewer words
R("and whether it reacts in time — and built a diagnostic benchmark that scores each policy on each.",
  "and whether it reacts — and built a benchmark that scores each policy on each.")
# a fourth policy runs on the Franka once GR00T N1.6-DROID carries often enough for a row of its own
if N.get("g0_car_ok"):
    R("and a Franka arm (π0.5, π0) doing pick-and-place beside a coworker in three scenes",
      "and a Franka arm (π0.5, π0, GR00T N1.6-DROID) doing pick-and-place beside a coworker in three scenes")
    R("以及 Franka 机械臂（π0.5、π0）在三个场景里于同事身旁做桌面取放",
      "以及 Franka 机械臂（π0.5、π0、GR00T N1.6-DROID）在三个场景里于同事身旁做桌面取放")
    R("Across two embodiments and three policies the profile recurs",
      "Across two embodiments and four policies the profile recurs")
    R("π0 carries on " + N['p0_carry'] + " episodes and where it carries repeats the pattern",
      "π0 carries on " + N['p0_carry'] + " episodes and GR00T N1.6-DROID on " + N['g0_carry'] + "; where they carry both repeat the pattern")
# §4.1: the tabletop family now carries three policies, two tasks and the hand at every table
R("A second family puts the predicates around a Franka arm doing pick-and-place, driven by π0.5 and π0 (openpi), at a dining table, a kitchen counter and a packing station",
  "A second family puts the predicates around a Franka arm doing pick-and-place, driven by π0.5, π0 (openpi) and GR00T N1.6-DROID, at a dining table, a kitchen counter and a packing station")
R("a coworker's hand reaching into the destination bowl (T5b, T6).",
  "a coworker's hand reaching into the destination bowl at each of the three tables (T5b, T6); and a second task, serving, whose bowl stands at the table edge beside the adult.")
R("The static proxies carry no collider, so their \"contacts\" are geometric penetrations; only the crossing person can be struck.",
  "The static proxies carry no collider, so their \"contacts\" are geometric penetrations.")
# §5.1: the person cell's contact distance (detail in Appendix E)
R("and with a third run of the person cell 121/125 enter the keep-out, all 21 person-cell carries coming within the proxy's body-plus-box contact distance (0.11–0.23 m from its axis).",
  "and with a third run of the person cell 121/125 enter the keep-out, every person-cell carry within the proxy's contact distance.")
# §6 (iv): the stop's incompleteness, in one clause
R("The external stop that prevents the payload contact is itself incomplete for a humanoid — referenced to the payload and the base, it is reached around by the arms, which touch the person from outside its distance (Appendix E.7).",
  "The external stop that prevents the payload contact is itself incomplete for a humanoid: referenced to the payload and the base, it is reached around by the arms (Appendix E.7).")
# §5.3 T5a: the scene-set caveat
R("The count is partly scene-set — no traversal of a 1.9 m corridor stays outside $d_0$ — so the policy-attributable finding is the absence of any slowing.",
  "The count is partly scene-set (no 1.9 m traversal stays outside $d_0$), so the policy-attributable finding is the absence of slowing.")
# §6 (i): the two pi0.5 command probes
R("and on π0.5 a spatial command leaves the plow-through at 88 % vs 94 % while cutting success from ≈ 100 % to 62 %; a keep-hot-coffee-upright command leaves π0.5's tilt as it was (" + N['pi_t4_hot'] + " vs " + N['pi_t4_pct'] + " %).",
  "and on π0.5 a spatial command leaves the plow-through at 88 % vs 94 % while cutting success to 62 %, a keep-upright command leaves its tilt as it was (" + N['pi_t4_hot'] + "), and a blades-away command leaves the presentation unchanged (" + N['pi_t3_cmd'] + ").")
