# -*- coding: utf-8 -*-
# Consistency audit wf_fe8809d8-343, range back: confirmed findings applied (exec at the end of the chain; uses t, _rn2, V).

# ---------------- main text (§6, §8, §9, Reproducibility Statement): word delta must stay <= 0 ----------------

# finding 4 (l.153, contradiction): heading said the command leaves the violation unchanged; the same paragraph reports it raised (hot coffee)
_rn2("**(i) A safety command changes completion, not the violation.**",
     "**(i) A safety command changes completion; the violation does not detectably fall.**")
# (reviewer: 'detectably' -- naming lowers the Table XI point estimates, 37 -> 29 % and 21 -> 16 %, non-significantly, so an unqualified 'does not fall' is false)

# finding 5 (l.155, overclaim): p = 0.06 was read as 'statistically unchanged'; E.2 reports the rate higher with the stove rendered
_rn2("shift toward a rendered stove comes from one two-seed experiment run on the substitute-driver day (E.2) and leaves the violation rate statistically unchanged (17/51 against 15/83, *p* = 0.06)",
     "shift toward a rendered stove (one two-seed experiment on the substitute-driver day, E.2) comes with a non-significantly higher violation rate (17/51 against 15/83, *p* = 0.06)")
# (reviewer: the finding's fix keeps 'though not significantly'; without it 'higher' overclaims in the other direction)

# finding 6 (l.155, number): §6 used the four-surface subset (0/64, 12/64) unannounced, and 'clears 0/64' said the opposite of what was meant; use the §5.1 / Table III counts
_rn2("which the blind carrier clears 0/64, is entered on 12/64",
     "which the blind carrier clears (" + V["t1_by_off"]["scripted"]["28"] + "), is entered on " + V["t1_by_off"]["pi05"]["28"])
# (reviewer: 'clears (0/80)' with the count in parentheses is sec. 5.1's own phrasing ('clears the second (0/80)'); saves the word the hedges above need)

# finding 14 (l.157, overclaim): absolute 'not conditioned' / 'the same at every azimuth' from non-significant tests (E.6 declines the invariance reading)
_rn2("**(iii) Neither orientation nor speed is conditioned on the person.**",
     "**(iii) Neither orientation nor speed is detectably conditioned on the person.**")
_rn2("The carry yaw is the same at every bystander azimuth for GR00T, on either side of the table for π0.5 (T3) and at any rendering of the person on either embodiment (E.7, E.8);",
     "The carry yaw shows no systematic shift with bystander azimuth for GR00T, table side for π0.5 (T3) or any rendering of the person on either embodiment (E.7, E.8);")

# finding 22 (l.167, reference): '(A.3.3)' read as a non-existent Appendix A subsection; point to where the exposure argument is made
_rn2("every contact rate is exposure, not harm (A.3.3)",
     "every contact rate is exposure, not harm (§5.3)")

# finding 19 (l.167, contradiction): §8's witness list left out T2 (set-down-away straight carry) and T6 (whole-arm stop)
_rn2("the witnesses are geometric (T3), a pinch grasp (T4) and the blind carrier (T1).",
     "the witnesses are straight carries (T1, T2), geometric (T3), a pinch grasp (T4) and a stop (T6).")

# finding 7 (l.171, overclaim): control comparisons exist only for T1-T4 on the shared placements (Table IIIf); T5a/T5b exposure, T6/T6b no control
# (partially applied: the pi0 T2 note -- below the control by the stratified exact test, p = 0.012, on a policy that rarely completes -- stays in the Table IIIf note; no main-text budget)
_rn2("straight line on any sub-type, and a humanoid case study shows the same profile.",
     "straight line on matched placements (T1–T4), and a humanoid case study shows the same profile.")

# finding 16 (l.177, reference): Appendix C never gives the substitute-driver caveat; it is in E.7 (word-neutral: the list's 'and' moves to the instruments item)
_rn2("the contact sensor on the crossing person, the instruments used as witnesses",
     "the crossing person's contact sensor and the instruments used as witnesses")
_rn2(" and the substitute-driver caveat on the cells run 2026-09-08 to 09-14; Appendix E the per-sub-type protocols;",
     "; Appendix E the per-sub-type protocols and the substitute-driver caveat on the cells run 2026-09-08 to 09-14 (E.7);")

# ---------------- appendices ----------------

# finding 16 (cont., E.2): E.2's '(§8)' pointer for the substitute-driver day lands on a section without it
_rn2("and the substitute-driver day (§8).",
     "and the substitute-driver day (E.7).")

# finding 18 (l.1984, contradiction): a sixth corrected error -- the G1 T2 bystander body scored 0.8 m above the floor in the September cells (E.3 rerun)
_rn2("Five measurement errors were found and corrected after the cells had run",
     "Six measurement errors were found and corrected after the cells had run")
_rn2("the G1 crossing capsule stood 0.79 m above the floor in the September cells,",
     "the G1 crossing capsule stood 0.79 m above the floor in the September cells, the G1 T2 bystander body 0.8 m (rerun 2026-10-02, E.3),")

# finding 9 (l.1989, contradiction): 'every tabletop sub-type ... two or more goals' holds for pi0.5's scored sub-types only
_rn2("every tabletop sub-type now rests on two or more goals, each further goal on far fewer carries than the first",
     "every scored π0.5 tabletop sub-type now rests on two or more goals, each further goal on far fewer carries than the first")

# finding 3 (l.1992, invariant): the G1 is not scored on T5b (exposure), and its scored T1 is the off-path stove
_rn2("GR00T N1.6 on a Unitree G1 is scored on every sub-type in one scene family;",
     "GR00T N1.6 on a Unitree G1 is scored on every sub-type but T5b (exposure) in one scene family, its T1 at the off-path stove;")

# finding 13 (l.1992, contradiction): 'one policy per family scored across a task battery' -- pi0-FAST also carries battery tasks
_rn2("The suite therefore has one policy per family scored across a task battery, and its cross-policy claim is the recurrence of a profile, not a ranking;",
     "The suite thus scores π0.5 across the task battery, π0-FAST on " + V["n_tasks_f0"] + " of its tasks and the other arm policies on the canonical goal; its cross-policy claim is the recurrence of a profile, not a ranking;")

# finding 0 (l.1993, invariant): 10/35 comes from the humanoid's on-path cells (exposure), not the headline T1; the non-traversal check is in E.2, not §5.1
_rn2("The headline T1 rate is conditioned on task completion, and the policy completes only 29 % of carries (10/35). We verify (§5.1) that the excluded failures are early non-traversals",
     "The G1 T1 rates are conditioned on task completion, and on the on-path cells (exposure) GR00T completes only 29 % of carries (10/35). E.2 verifies that the excluded failures are early non-traversals")

# finding 1 (l.1996, contradiction): 'Small samples' bullet out of date (T1 pools, ablation arms, G1 T5a) and 'single-policy' contradicts five policies
_rn2("The T1 avoidance result rests on 10 completing carries; the language/perception ablations have 1–7 completing carries per cell; the T5a present condition contributes 6 episodes. Every quantitative claim should be read as a single-policy, small-sample simulation result.",
     "The scored T1 pools rest on " + V["pi_T1"].split("/")[1] + " carries for π0.5 and 30 completing carries on the G1; the on-path language/perception ablations have 1–7 completing carries per cell, against 21–49 per arm in the non-ceiling 2 × 2; G1 T5a rests on 22 carries, 6 of them in the matched present/absent design. Every quantitative claim should be read as a small-sample, simulation-only result.")

# finding 15 (l.1999, reference): the body-surface threshold treatment is in §5.1, E.3 and E.8, not §5.5
_rn2("the 3-D body-surface treatment (§5.5,",
     "the 3-D body-surface treatment (§5.1, E.3, E.8,")

# finding 11 (l.2000, invariant): 0.05-0.08 m describes the G1 on-path (exposure) cells; scored off-path carries pass farther, and the rate depends on the offset
_rn2("The finding is robust to this — completing carries pass essentially through the hazard point (clearance 0.05–0.08 m), so a larger, standards-derived radius would only deepen the violation —",
     "The finding is robust to this — on the on-path cells (exposure) completing carries pass essentially through the hazard point (clearance 0.05–0.08 m), and on the scored off-path cells a larger, standards-derived radius can only raise the rate (its offset dependence: §5.1, E.8) —")

# finding 8 (l.2004, contradiction): the tabletop T2 witness (set-down-away carry) was missing from the witness list
_rn2("and T1 (the blind carrier), T3, T4 (the pinch grasp) and T6 at the table;",
     "and T1 (the blind carrier), T2 (the set-down-away carry, one placement), T3, T4 (the pinch grasp) and T6 at the table;")

# findings 2 and 20 (l.2006): T5b is exposure on both embodiments (dropped from the defect list); 'a body defect on two' named and given its basis
try:
    _g1t2 = next(r["cells"][1] for r in V.get("heat_rows", []) if str(r.get("name", "")).endswith("G1"))
    _g1t2pct = str(int(round(100.0 * _g1t2[0] / _g1t2[1])))
except Exception:
    _g1t2pct = "84"
_rn2("a body defect on two (T2), orientation and speed that ignore the person (T3, T5a), forces above the body-region limits (T5b) and no reaction",
     "a body defect on the humanoid (" + _g1t2pct + " %) and, at the 0.10 m margin, on π0.5 against the blind control (T2), orientation and speed that ignore the person (T3, T5a) and no reaction")

# finding 12 (l.2010, contradiction): this paper evaluates GR00T N1.6, not N1.7; only pi0.5 is shared with SafeStage
_rn2("evaluates π0.5 and GR00T N1.7 among four policies, so two of its rows are two of ours.",
     "evaluates π0.5 and GR00T N1.7 among four policies, so one of its rows (π0.5) is one of ours and another (GR00T N1.7) is a later release of the model behind our GR00T N1.6-DROID.")

# finding 21 (l.2033, overclaim): Table I claimed a witness per sub-type; witnesses are per dimension and some cells are unattributed
_rn2("blind straight-line control; a witness per sub-type |",
     "blind straight-line control; a witness per dimension, unattributed cells marked |")

# finding 10 (l.2035, reference): the axis-vs-surface analysis is in §5.1 / E.8, and E.8 says the policy order holds at every radius (no inversion)
_rn2("and show (§5.5) that scoring to the person's *axis* rather than the body *surface* can invert a policy comparison;",
     "and show (§5.1, E.8) that at a 0.10 m margin, scoring to the person's *axis* rather than the body *surface* cuts π0.5's T2 rate from 53 % to 3 %, so we report full threshold curves rather than one margin;")
# (reviewer: '3 % -> 53 %' after 'axis rather than surface' read backwards (the axis gives 3 %), 'several-fold' understated ~18x, and
#  'a single margin can make either policy look safe' has no support -- E.8 keeps the policy order at every radius; App. F 'Metric scope' gives the curves)

# finding 17 (l.2039, overclaim): 'decisive' contradicts Appendix F (on-path ablations at a ceiling; non-ceiling ablation 'not decisive')
_rn2("are cheap, decisive, and belong in every type's protocol",
     "are cheap, informative where the rate has headroom, and belong in every type's protocol")
