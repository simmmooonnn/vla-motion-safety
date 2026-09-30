# -*- coding: utf-8 -*-
# The advisor's third requirement: each dimension should rest on several tasks. R6 made that true of trajectory; this
# makes it true of orientation. The predicates are untouched -- T3 still needs a hazardous-axis payload and a still
# bystander, T4 a spillable vessel and the neutral instruction -- and only the task scope widens, from the canonical cell
# to every battery task in which the predicate is available. The rule is stated in full in Appendix D, pointed to from
# section 4.2, and Table IVe reports how many tasks, cells and episodes sit behind every cell of Table III: the table he
# asked for. Exec'd after a134 (uses t, RN, V, _rn2, _word).
_SP = V["dimtask_spread"]

# ---------------- 4.2: the pointer
_rn2("T5a is scored on the mobile G1 only; T5c enters no score.",
     "T5a is scored on the mobile G1 only; T5c enters no score. Every pool spans every task in which its predicate is "
     "*available* rather than one cell; the conditions, and the ablations and probes that enter no score, are in "
     "Appendix D, and Table IVe gives the tasks, cells and episodes behind each cell of Table III.")

# ---------------- Appendix D: the rule itself
_rn2("**Why each predicate.** Where a standard fixes the value we adopt it; where none does we state the choice and "
     "report the rate's sensitivity to it.",
     "**What each pool spans.** A sub-type is scored over every task in the suite in which its predicate is *available*, "
     "not over one cell. Three conditions decide availability. The payload must have the property the predicate is about: "
     "a hazardous axis for T3 (scissors or a fork, not a mug), a spillable vessel for T4 (a mug or cup, not the rigid "
     "box). The person must be in the state the predicate assumes: standing still for T1–T4, moving for T6 and T6b, "
     "beside the destination for T2. And the task's own goal must not be the predicate — a pour tilts the vessel by "
     "design, so pouring is excluded from T4 and reported as that predicate's positive control, and a handover's "
     "hazardous end toward the receiver is a different predicate on its own row. Four kinds of cell are the same task "
     "under a manipulation and enter no score: the prompt ablations (an instruction naming the hazard, keeping the cup "
     "level, hurrying or going slowly), the perception and appearance ablations (the person hidden, or rendered as a "
     "photorealistic human), the witness and control treatments (the rotated spawn, the pinch grasp, the retracting hand, "
     "the collider removed) and the threshold, radius and engine probes. The interaction-geometry placements are reported "
     "as their own group (E.8), as in earlier drafts. Table IVe counts what is left, per sub-type and policy.\n\n"
     "**Why each predicate.** Where a standard fixes the value we adopt it; where none does we state the choice and "
     "report the rate's sensitivity to it.")

# ---------------- 5.2: T3 and T4 over the tasks
_rn2("Pooled over both sides, the fork and five surfaces the rate is 32/75 (43 %, cluster-robust [24, 64]), against the "
     "50 % a half-space predicate gives by chance: the scored T3.",
     "Pooled over every task in which a hazardous-axis payload is carried past a still bystander (" + V["t3task_pi_n"]
     + " tasks) the rate is " + V["t3task_pi"] + ", against the 50 % a half-space predicate gives by chance: the scored "
     "T3.")
_rn2("π0.5 carries a mug tilted: its axis leaves upright by more than 45° mid-transport on 398/520 carries (77 %) and by "
     "more than a full cup's 14–27° spill angle on 478/520, 383 of the 398 still scored successes.",
     "π0.5 carries a mug tilted: pooled over every task in which it carries a spillable vessel past a still bystander ("
     + V["t4task_pi_n"] + " tasks) its axis leaves upright by more than 45° mid-transport on " + V["t4task_pi"]
     + ", and on the canonical cell by more than a full cup's 14–27° spill angle on 478/520, 383 of whose 398 above 45° "
     "still scored successes.")

# ---------------- the canonical comparison and the across-task spread go to E.8, where there is room
_rn2("The scored pool is therefore the serving family (bowl 0.32 m from the body), and inside it the cells whose "
     "destination lies on the person's own side",
     "**The orientation pools, canonical cell against tasks.** Widening T3 and T4 from the canonical cell to every task "
     "in which the predicate is available (Appendix D) leaves T3 where it was and lowers T4: π0.5's T3 goes from "
     + V["t3can_pi_pct"] + " % (" + V["t3can_pi"] + ") to " + V["t3task_pi"] + " over " + V["t3task_pi_n"] + " tasks, "
     "and its T4 from " + V["t4can_pi_pct"] + " % (" + V["t4can_pi"] + ") to " + V["t4task_pi"] + " over "
     + V["t4task_pi_n"] + ". Neither is carried by one task and neither is uniform across them: the T3 rate runs "
     + _SP["T3"]["lo"] + "–" + _SP["T3"]["hi"] + " % and the T4 rate " + _SP["T4"]["lo"] + "–" + _SP["T4"]["hi"] + " % "
     "over the tasks above the eight-episode floor (Table IV, task by task). The pooled figure is a summary of a "
     "task-dependent quantity, which is why Table III prints the sub-type split and Table IVe the breadth behind it.\n\n"
     "The scored pool is therefore the serving family (bowl 0.32 m from the body), and inside it the cells whose "
     "destination lies on the person's own side")

# ---------------- Table III caption and the abstract
_rn2("T3 pooled over bearings (chance 50 %);",
     "T3 and T4 pooled over every task in which the predicate is available (Appendix D), T3 over bearings too (chance "
     "50 %);")
_rn2("π0.5 tilts a mug past 45° on 77 % of carries, most still scored successful;",
     "π0.5 tilts a mug past 45° on " + V["t4task_pi_pct"] + " % of carries across " + V["t4task_pi_n"] + " tasks, most "
     "still scored successful;")
_rn2("pooled over bearings a hazard points into the person's half-space at chance (GR00T 14/27, π0.5 32/75),",
     "pooled over bearings and tasks a hazard points into the person's half-space at chance (GR00T 14/27, π0.5 "
     + V["t3task_pi"].split(" = ")[0] + "),")
_rn2("π0.5 在 70% 的搬运中把杯子倾斜超过 45°（其中大多数仍判为成功）",
     "π0.5 在 " + V["t4task_pi_pct"] + "% 的搬运中把杯子倾斜超过 45°（跨 " + V["t4task_pi_n"] + " 个任务，其中大多数仍判为成功）")
_rn2("π0.5 tilts its mug on 77 % while its arm stays clear of people (Table III).",
     "π0.5 tilts its mug on " + V["t4task_pi_pct"] + " % while its arm stays clear (Table III).")

# ---------------- Appendix F: what the matrix now inherits, and what it still does not
_rn2("Table III is narrower than the suite, though less so than it was: its trajectory column now draws on the off-path "
     "keep-out levels and on the serving family (" + V["t2sv_pi_cells"] + " cells at " + V["t2sv_pi_surf"] + " work "
     "surfaces for π0.5, " + V["t2sv_f0_cells"] + " for π0-FAST, " + V["t2sv_ik_cells"] + " for the control), so that one "
     "dimension rests on several tasks for three rows. Orientation, speed-and-force and dynamics still rest on the "
     "canonical pick-and-place and its two person variants, and there the breadth of Table IV supports the design, not "
     "the matrix.",
     "Table III is narrower than the suite, and the gap is now specific. Trajectory and orientation rest on several "
     "tasks: T2 on the serving family (" + V["t2sv_pi_cells"] + " cells at " + _word(V["t2sv_pi_surf"]) + " work "
     "surfaces for π0.5), T3 on " + V["t3task_pi_n"] + " tasks and T4 on " + V["t4task_pi_n"] + ", and for π0-FAST on "
     + V["t3task_f0_n"] + " and " + V["t4task_f0_n"] + " (Table IVe). **Speed and force and dynamics do not.** Speed and "
     "force is scored on the humanoid corridor alone, since the tabletop cell is exposure; dynamics rests on one "
     "mechanism per sub-type — a hand reaching into the destination for T6, a person walking past for T6b — across six "
     "work surfaces but not across tasks. π0 and GR00T-DROID rest on two or three tasks wherever they are scored at all. "
     "So each dimension rests on several tasks for two of the four dimensions and for the two policies with a full "
     "battery; for the rest, Table IV's breadth supports the design and not the matrix.")

# ---------------- Table IVe
_IVE = ("**Table IVe. Each dimension, and how many tasks, cells and scored episodes its score rests on (tabletop "
        "family).** Every entry is *tasks / cells / episodes*: a task is a row of Table IV, a cell is one label (a "
        "placement and a seed), and an episode is one that entered that sub-type's denominator. What a pool requires is "
        "defined in Appendix D. The humanoid's rows are omitted because its corridor family is one scene with a variant "
        "per sub-type (Appendix E.7), so each of its scores rests on one task. T5a is exposure on the tabletop and "
        "scored on the humanoid only; the control's T4 is the pinch-grasp variant (§5.5), which ran on the canonical "
        "task alone.\n\n" + V["dimtask_head"] + "\n"
        + "|" + "---|" * (V["dimtask_head"].count("|") - 1) + "\n" + V["dimtask_rows"] + "\n\n")
_rn2("**Table IVb. Coverage: attempted / carried / delivered episodes per work surface and policy**",
     _IVE + "**Table IVb. Coverage: attempted / carried / delivered episodes per work surface and policy**")

# ---------------- page budget
_rn2("**T5c: a hazardous end that carries speed (tool tasks; beside the score).** Holding a ladle, a spatula or tongs, "
     "π0.5 drives the hazardous end at a peak of 0.50 m/s (max 1.44) — four to ten times its mug-carrying speed — within "
     "0.18 m of the adult, and above 0.25 m/s inside 0.5 m of them on 10/41 carried episodes. A moving edge is a "
     "transient contact whose harm scales with speed (ISO/TS 15066 Annex A.3.3; [48]) and a sharp tool is excluded from "
     "permitted contact, so the rate is an exposure and stays beside the score; its threshold and radius sensitivity, "
     "the null under a move-slowly command and its π0.5-only coverage are in Table IVc and Appendix E.8.",
     "**T5c: a hazardous end that carries speed (tool tasks; beside the score).** Holding a ladle, a spatula or tongs, "
     "π0.5 drives the hazardous end at a peak of 0.50 m/s (max 1.44) — four to ten times its mug-carrying speed — within "
     "0.18 m of the adult, and above 0.25 m/s inside 0.5 m of them on 10/41 carried episodes. A sharp tool is excluded "
     "from permitted contact, so the rate is an exposure and stays beside the score (Table IVc, E.8).")
_rn2("and 4 carries then deliver them blade-away. It does not travel, though — across the far edge, at the far-right "
     "corner and for the fork on either side a 180° spawn leaves the rate where it was (four pairs, E.8):",
     "and 4 carries then deliver them blade-away. It does not travel — across the far edge, at the far-right corner and "
     "for the fork a 180° spawn leaves the rate where it was (four pairs, E.8):")
_rn2("on 26/32 episodes and touches it on 9/32 — the right hand at the right-pick position (8/8), the turning shoulder "
     "at the left-pick — where a margin to the person's *axis* registers only 8/32.",
     "on 26/32 episodes and touches it on 9/32 — the right hand at the right-pick position, the turning shoulder at the "
     "left — where a margin to the person's *axis* registers only 8/32.")
_rn2("A kinematic capsule with a collider crosses the corridor at a creeping 0.06 m/s (a walking-speed approach: "
     "Appendix E.7).",
     "A kinematic capsule with a collider crosses the corridor at a creeping 0.06 m/s (walking speed in E.7).")
_rn2("And they are **separately scored**: each has its own predicates and a fixed rule for its score (§4.2), so a policy "
     "receives a profile rather than one number, and the dimensions differ in the percept the safe move needs — a detour "
     "a static one, a reaction a temporal one.",
     "And they are **separately scored**: each has its own predicates and a fixed rule (§4.2), so a policy receives a "
     "profile rather than one number, and they differ in the percept the safe move needs — a detour a static one, a "
     "reaction a temporal one.")
_rn2("Dynamics is kept apart from the three motion dimensions because it alone is scored against a reference that moves: "
     "the question is not where, how or how fast, but whether the motion changes in time.",
     "Dynamics is kept apart because it alone is scored against a reference that moves: not where, how or how fast, but "
     "whether the motion changes in time.")
_rn2("on a shelf-to-bin box carry — pick a box from a shelf, walk ≈ 1.9 m down a corridor, release it in a bin — and "
     "each sub-type changes what surrounds that carry",
     "on a shelf-to-bin box carry — pick from a shelf, walk ≈ 1.9 m down a corridor, release in a bin — and each "
     "sub-type changes what surrounds it")
