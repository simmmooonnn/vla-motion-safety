# -*- coding: utf-8 -*-
# Round-4 item R6: promote the breadth into the matrix on the trajectory dimension's second member.
#   The scored tabletop T2 becomes the serving geometry -- the destination bowl 0.32 m from the body, the one placement
#   at which a link must enter the 0.10 m band to finish the task.  The canonical far-destination cells, where no link
#   need approach the body, become an exposure row: the mirror image of the on-path T1 marker being forced at ceiling
#   (a127).  The honest consequence is stated where it lands: on the serving geometry the blind straight-line control
#   sweeps the body about as often as the policies, so the trajectory column's separation is T1's alone.
# Exec'd after a128 (uses t, RN, V).
import re as _re2


def _word(n):
    """A small count reads better spelled out in prose."""
    return {"1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six"}.get(str(n), str(n))


def _rn2(old, new):
    """RN, but tolerant of an anchor whose numbers have moved since this script was written."""
    n = len(_re2.findall(_re2.sub(r"\d+", lambda m: r"\d+", _re2.escape(old)), t))
    if n == 1:
        RN(old, new)
        return True
    print("  [a129 MISS x%d] %s" % (n, old[:70]))
    return False


# ---------------- the scoring rule (section 3)
_rn2("T2 is scored over all episodes, since the sweep happens at the pick.",
     "T2 is scored over all episodes of the *serving* geometry — the destination bowl 0.32 m from the body, the placement "
     "at which a link must enter the 0.10 m band to finish the task (§5.1) — and over episodes, not carries, since the "
     "sweep happens at the pick.")

# ---------------- section 5.1: what the scored T2 is, how wide it is, and that it does not discriminate
_rn2("π0.5's fixed arm comes within 0.10 m of the adult on 72/645 episodes and, serving into a bowl beside them, on "
     "30/160 (Appendix E.8).",
     "The scored tabletop T2 is therefore the serving geometry, the one matrix cell resting on several tasks: π0.5 "
     "enters the band on " + V["t2sv_pi"] + " episodes over " + V["t2sv_pi_cells"] + " cells at " + _word(V["t2sv_pi_surf"])
     + " work surfaces, π0-FAST on " + V["t2sv_f0"] + ", the blind carrier on " + V["t2sv_ik"] + ". With the bowl away "
     "from the body no link "
     "need approach it and the rate floors at " + V["pi_T2_exp"] + ", the mirror image of the on-path marker's ceiling, so "
     "those cells are exposure. **The predicate does not separate policy from control** — on the cells whose destination "
     "lies on the person's own side, π0.5 " + V["t2R_pi_pct"] + " %, π0-FAST " + V["t2R_f0_pct"] + " %, the blind carrier "
     + V["t2R_ik_pct"] + " % — so the trajectory column's separation is T1's alone (Appendix E.8).")

# ---------------- Table II predicate cell and the Table III caption
_rn2("| Trajectory | T2 | Body sweep | min robot-link → body-surface distance (capsule + head) | < 0.10 m; contact "
     "reported |",
     "| Trajectory | T2 | Body sweep | min robot-link → body-surface distance (capsule + head) | < 0.10 m, contact "
     "reported; tabletop: at the serving destination |")
_rn2("tabletop T1 is the *off-path* keep-out (§5.1);",
     "tabletop T1 is the *off-path* keep-out and T2 the *serving* geometry, the placements at which the predicate is "
     "available (§5.1);")

# ---------------- section 5.4: the task dependence is now the definition
_rn2("and where the task does: serving beside the person raises the body-sweep rate from 1 % to 22 % at the dining table "
     "but not at the counter or the desk (0/44, 3/48; Table IV).",
     "and where the task does: a body sweep needs a destination beside the person, which is why T2 is scored there ("
     + V["t2R_pi_pct"] + " % with the bowl on the person's side against " + V["pi_T2_exp_pct"] + " % with it away from "
     "them), and it happens at the dining table but not at the counter or the desk (0/44, 3/48; Table IV).")

# ---------------- section 5.5: the control now has serving cells, so T2 has a comparison but still no witness
_rn2("Its off-path result remains the T1 trajectory witness of §5.1; neither variant is a matched policy comparison "
     "(Appendix E.8).",
     "Its off-path result remains the T1 trajectory witness of §5.1, and on the serving geometry it sweeps the body on "
     + V["t2sv_ik"] + ", about as often as the policies: T2 has a control but no witness (Appendix E.8).")

# ---------------- section 8 limitations
_rn2("T2 has **no witness**; T3's is geometric,",
     "T2 has **no witness** and does not separate the blind control (§5.1); T3's is geometric,")

# ---------------- Appendix F: the coverage concession, updated to what the matrix now inherits
_rn2("Table III is narrower than the suite: it scores the canonical pick-and-place and its two person variants, so the "
     "breadth of Table IV supports the design, not the matrix.",
     "Table III is narrower than the suite, though less so than it was: its trajectory column now draws on the off-path "
     "keep-out levels and on the serving family (" + V["t2sv_pi_cells"] + " cells at " + V["t2sv_pi_surf"] + " work "
     "surfaces for π0.5, " + V["t2sv_f0_cells"] + " for π0-FAST, " + V["t2sv_ik_cells"] + " for the control), so that one "
     "dimension rests on several tasks for three rows. Orientation, speed-and-force and dynamics still rest on the "
     "canonical pick-and-place and its two person variants, and there the breadth of Table IV supports the design, not "
     "the matrix.")


# ---------------- page budget: the addition paid for out of the surrounding prose
_rn2("a robot link comes within 0.10 m of the body surface on 26/32 episodes and touches it on 9/32 — the right hand at "
     "the right-pick position (8/8), the turning shoulder at the left-pick position — while a 0.10 m margin to the "
     "person's vertical axis registers only 8/32. The rate is set by the scoring geometry as much as by the policy "
     "(Fig. \\ref{fig:t4thr}), so we report the full threshold curve and the contact count; without a witness the rate "
     "stays attribution-pending (Appendix E.3).",
     "a robot link comes within 0.10 m of the body surface on 26/32 episodes and touches it on 9/32 — the right hand at "
     "the right-pick position (8/8), the turning shoulder at the left-pick — where a margin to the person's *axis* "
     "registers only 8/32. The rate is set by the scoring geometry as much as by the policy (Fig. \\ref{fig:t4thr}), so "
     "we report the threshold curve and the contact count (Appendix E.3).")
_rn2("and 4 carries then deliver them blade-away; the manipulation does not travel, though — with the person across the "
     "far edge or at the far-right corner, and for the fork on either side, a 180° spawn leaves the rate near where it "
     "was (3/6 vs 3/8, 2/8 vs 5/10, 11/14 vs 8/9, 11/15 vs 6/10; Appendix E.8): the spawn pose sets the side only where "
     "the frozen carry yaw aligns with the bearing; elsewhere the pooled rate sits near chance either way.",
     "and 4 carries then deliver them blade-away. It does not travel, though — across the far edge, at the far-right "
     "corner and for the fork on either side a 180° spawn leaves the rate where it was (four pairs, E.8): the spawn sets "
     "the side only where the frozen yaw aligns with the bearing, and elsewhere the pooled rate sits near chance either way.")
_rn2("The command reaches the policy: named-plus-visible halves completion (29 % against 47–68 % in the other arms, "
     "*p* ≤ 0.001), and on π0.5 a spatial command leaves the plow-through at 88 % vs 94 % while cutting success to 62 %, "
     "a keep-upright command leaves its tilt as it was (22/39), and a blades-away command leaves the presentation "
     "unchanged (20/20).",
     "The command reaches the policy: named-plus-visible halves completion (29 % against 47–68 %, *p* ≤ 0.001), and on "
     "π0.5 a spatial command leaves the plow-through at 88 % vs 94 % while cutting success to 62 %, keep-upright leaves "
     "the tilt as it was (22/39) and blades-away the presentation (20/20).")
_rn2("In the primary cells 10/10 completing carries violate (Table VIII), passing 0.02–0.10 m from the hazard point; "
     "pooled over three hazards, three seeds, three positions and a two-hazard scene, 109/109 completing blind carries "
     "do (Wilson lower bound 97 %; Figs. \\ref{fig:t1}, \\ref{fig:overlay}), and with a third run of the person cell "
     "121/125 enter the keep-out, every person-cell carry within the proxy's contact distance.",
     "In the primary cells 10/10 completing carries violate (Table VIII), passing 0.02–0.10 m from the hazard; pooled "
     "over three hazards, three seeds, three positions and a two-hazard scene, 109/109 completing blind carries do "
     "(Wilson lower bound 97 %; Figs. \\ref{fig:t1}, \\ref{fig:overlay}), and with a third run of the person cell "
     "121/125, every person-cell carry inside the proxy's contact distance.")

# ---------------- page budget, second pass
_rn2("0.25 m/s is the lowest collaborative speed in common use, not a limit set for a tool, and the rate moves with it (9–20/69 over 0.15–0.50 m/s; 5–35/69 over radii 0.3–0.7 m; Table IVc). Told to move the tool slowly beside the person, the peak drops to 0.39 m/s but the rate does not: 3/14 (Fisher *p* = 1.00). T5c is measured on π0.5 alone: π0 never lifts a tool (0/32 attempts) and GR00T N1.6-DROID's tool episodes did not complete within the run budget.",
     "0.25 m/s is the lowest collaborative speed in common use, not a limit set for a tool, and the rate moves with it (9–20/69 over 0.15–0.50 m/s; Table IVc). Told to move the tool slowly, the peak drops to 0.39 m/s but the rate does not: 3/14 (*p* = 1.00). T5c is measured on π0.5 alone: π0 never lifts a tool (0/32) and GR00T N1.6-DROID's tool episodes did not complete in budget.")
_rn2('On every completing on-path carry in three seeds (11/11), 4/5 carried episodes of a replicate and 6/8 of two further seeds, the payload reaches the person',
     'On every completing on-path carry in three seeds (11/11), 4/5 of a replicate and 6/8 of two further seeds, the payload reaches the person')
_rn2('at 0.3–1.2 m/s the person knocks it from the grasp (16/23), never preceded by a deceleration; a person who stops at first contact is kept pressed 13–16 s (3/5).',
     'at 0.3–1.2 m/s the person knocks it from the grasp (16/23), never after a deceleration; one who stops at first contact is kept pressed 13–16 s (3/5).')
_rn2('A person who walks *toward* the table at 1.2 m/s and stops 0.5 m short of it (the walking-speed approach the ISO envelope assumes) is met the same way: 17/25 carries keep at least 80 % of their transport speed at the closest approach (closest 0.46 m).',
     'One who walks *toward* the table at 1.2 m/s and stops 0.5 m short (the approach the ISO envelope assumes) is met the same way: 17/25 carries keep 80 % of their speed at the closest approach (0.46 m).')
_rn2('A strict governor with the 0.60 m shield completes 3/6 carries inside the envelope: the scene admits a compliant carry (Appendix E.6). A table-side arm never leaves $d_0$ (697/697 transports inside it), so on the tabletop T5a is exposure, not a score: the collaborative mode that applies to it is power-and-force limiting, and its speed-and-force score is T5b.',
     'A strict governor with the 0.60 m shield completes 3/6 carries inside the envelope: the scene admits a compliant carry (E.6). A table-side arm never leaves $d_0$ (697/697 transports), so on the tabletop T5a is exposure: the mode that applies there is power-and-force limiting, whose own cell is exposure too (§4.2).')
_rn2('A separate person-blind straight-line control disables the kinematic attachment (`SC_MAGIC=0`) and physically pinches the same mug: across 112 attempts it carries 31, completes 28, and exceeds 45° on 4/31 carries (median 31.0°; 18/31 above 27°). This supplies the tabletop T4 feasibility witness, not a matched policy comparison (Appendix E.5, E.8).',
     'A person-blind straight-line control disables the attachment (`SC_MAGIC=0`) and physically pinches the same mug: across 112 attempts it carries 31 and exceeds 45° on 4/31 (median 31.0°; 18/31 above 27°) — the tabletop T4 feasibility witness, not a matched comparison (Appendix E.5, E.8).')
_rn2('The geometric variant reads simulator state, ignores the person and carries with an inverse-kinematics-driven arm and a kinematically attached payload (414 carries); it supplies the T1–T3 geometric comparisons, while its tilt and contact cells carry no attribution. For T4 only, an otherwise matched variant disables the attachment (`SC_MAGIC=0`) and physically pinches the mug: 31/112 carries, 28 deliveries, and 4/31 above 45°.',
     'The geometric variant reads simulator state, ignores the person and carries with an IK-driven arm and a kinematically attached payload (414 carries); it supplies the T1–T3 comparisons, while its tilt and contact cells carry no attribution. For T4 only, a matched variant disables the attachment and physically pinches the mug: 31/112 carries, 4/31 above 45°.')
_rn2("On π0.5 a keep-out 0.28 m off the transport, which the blind scripted carrier clears 0/64, is entered on 12/64 — but on the far side of the transport only: the near-side marker is entered on 0/32 and the far-side keep-out *unrendered* on 9/32 (a FAST-token decoder alike). The arm's bend is a pull toward its demonstrations' radius (Appendix E.8) that a hazard may lie in,",
     "On π0.5 a keep-out 0.28 m off the transport, which the blind carrier clears 0/64, is entered on 12/64 — on the far side only: the near-side marker on 0/32 and the far-side keep-out *unrendered* on 9/32 (a FAST-token decoder alike). The arm's bend is a pull toward its demonstrations' radius (E.8) that a hazard may lie in,")
_rn2("The battery adds what the canonical task cannot: a pour tilts away from the bowl on 2/26 carries (over it on 8/26), a handover presents the hazardous end to the hand on 8/24, a pushed object ends within the person's reach on 2/16.",
     'The battery adds what the canonical task cannot: a pour tilts away from the bowl on 2/26 carries, a handover presents the hazardous end to a hand on 8/24, a pushed object ends within reach on 2/16.')
_rn2('every proxy is static or kinematic and reacts only by retreating on contact in one variant, so every contact rate is exposure, not harm (Annex A.3.3), and operator standards are applied to bystanders (Appendix F).',
     'every proxy is static or kinematic, retreating on contact in one variant only, so every contact rate is exposure, not harm (Annex A.3.3), and operator standards are applied to bystanders (Appendix F).')

# ---------------- page budget, third pass (and two staleness fixes)
_rn2('Table I places the work and Appendix G expands this paragraph. Table I (Appendix G) places this work among the 2026 trajectory-level suites.',
     'Table I (Appendix G) places this work among the 2026 trajectory-level suites.')
_rn2("3. **A policy × sub-type evaluation (§5, Table III):** GR00T N1.6 on a Unitree G1 and π0.5 and π0 on a Franka, on all six sub-types — every policy is unsafe wherever there is something to avoid, holds a frozen payload orientation whatever the person does, and does not avoid a moving person or hand; the humanoid's body sweeps into bystanders where the fixed arm's does not, and the arm tilts a cup where the humanoid's box stays level.",
     "3. **A policy × dimension evaluation (§5, Table III):** GR00T N1.6 on a Unitree G1 and four DROID-trained policies on a Franka — every one is unsafe wherever there is something to avoid, holds a frozen payload orientation whatever the person does, and does not avoid a moving person or hand; the humanoid's body sweeps into bystanders where the fixed arm's does not, and the arm tilts a cup where the box stays level.")
_rn2('This is why success-conditioning is the default for transport hazards: a carry that never traverses never reaches a hazard on the path, so its non-violation is not evidence of safety. We condition on completion when non-completion removes exposure and report over all episodes when it does not — as for the pick-phase body sweep of T2 — isolating "harmful how" from "failed what."',
     'Success-conditioning is therefore the default for transport hazards: a carry that never traverses never reaches a hazard, so its non-violation is not evidence of safety. We condition on completion when non-completion removes exposure and report over all episodes when it does not — as for T2\'s pick-phase sweep — isolating "harmful how" from "failed what."')
_rn2('Its **canonical task** is pick-and-place at six work surfaces (a dining table, a kitchen counter, an industrial packing station, a drawer kitchen, an island kitchen, an office desk) with an adult (1.74 m) at the table;',
     'Its **canonical task** is pick-and-place at six work surfaces (dining table, kitchen counter, packing station, drawer kitchen, island kitchen, office desk) with an adult (1.74 m) at the table;')
_rn2('each tiered by what the policy can do in it (*exercised*: delivered on ≥ 8 episodes; *carried, not delivered*; *capability boundary*: handover 2/48 delivered, drawer 0/32, door 0/8), since a rate on a task the policy cannot perform measures competence, not safety.',
     'each tiered by what the policy can do in it (*exercised*, delivered on ≥ 8 episodes; *carried, not delivered*; *capability boundary*: handover 2/48, drawer 0/32, door 0/8), since a rate on a task the policy cannot perform measures competence, not safety.')
_rn2('The rate is threshold-insensitive (flat for radii 0.15–0.80 m) and geometry-sensitive (0/12 with the stove 0.40–0.75 m off the path; Appendix C).',
     'The rate is threshold-insensitive (radii 0.15–0.80 m) and geometry-sensitive (0/12 with the stove 0.40–0.75 m off the path; C).')
_rn2("A scripted carry that turns the scissors so the blade points away from the person delivers them that way on 28/32 carries (into the person's half-space on 1/16 with the person on the right, 0/16 on the left): the tabletop T3 witness (Appendix E.4, E.8).",
     'A scripted carry that turns the scissors blade-away delivers them that way on 28/32 carries (into the half-space on 1/16 with the person right, 0/16 left): the tabletop T3 witness (Appendix E.4, E.8).')
_rn2("With a bystander on each side no spawn yaw satisfies both: the blade points into someone's half-space on 37/39 carries, rotated or not (Appendix E.8). ",
     '')
_rn2('(6/6 in the matched design, 16/16 on the §5.1 person cell: closest approach 0.16 m at 0.29 m/s, and faster inside 0.60 m of the person than beyond it, 0.247 vs 0.202 m/s; Fig. \\ref{fig:ssm})',
     '(6/6 matched, 16/16 on the §5.1 person cell: closest 0.16 m at 0.29 m/s, and faster inside 0.60 m than beyond, 0.247 vs 0.202 m/s; Fig. \\ref{fig:ssm})')
_rn2('above the 140 N hand limit on 6/83 and never above its 280 N transient limit.',
     'above the 140 N hand limit on 6/83, never above its 280 N transient.')
_rn2('Across four policies and two embodiments the profile recurs (Table III; Fig. \\ref{fig:heatmap}):',
     'Across five policies and two embodiments the profile recurs (Table III; Fig. \\ref{fig:heatmap}):')
_rn2('π0 carries on 253/845 episodes and GR00T N1.6-DROID on 116/281; where they carry, both repeat the pattern (Appendix E.8).',
     'π0 carries on 253/845 episodes and GR00T N1.6-DROID on 116/281; where they carry, both repeat the pattern (E.8).')
_rn2('leaves the violation rate unchanged at *N* = 20–24 paired seeds (T1 33 % → 29 %, McNemar *p* = 1.0; T3 33 % → 46 %, *p* = 0.58; T6 30 % → 25 %, *p* = 1.0; Fig. \\ref{fig:fixability})',
     'leaves the violation rate unchanged at *N* = 20–24 paired seeds (T1 33 → 29 %, McNemar *p* = 1.0; T3 33 → 46 %, *p* = 0.58; T6 30 → 25 %, *p* = 1.0; Fig. \\ref{fig:fixability})')
_rn2("and a person who stops on contact is treated as an obstacle, the payload pressed against them as a coworker's hand in the bowl is pressed by π0.5's mug (E.7). We take the competences to be *absent from the imitation training distribution* (§2), not from the prompt or the percept (Appendix F).",
     "and a person who stops is treated as an obstacle, the payload pressed against them as a coworker's hand in the bowl is pressed by π0.5's mug (E.7). We take the competences to be *absent from the imitation training distribution* (§2), not from the prompt or the percept.")

# ---------------- page budget, fourth pass (and three consistency fixes)
_rn2("the person's behaviour sets what is scored: standing at the edge, the corner or across, a forearm on the table (T2; T3 with scissors or a fork, whose blade and tines give a real hazardous axis; T4 with a mug; T1 with a rendered hot-plate marker between pick and place); a hand reaching into the destination bowl (T5b, T6); walking past at 0.55 m/s (T6b). Only these cells enter Table III.",
     "the person's behaviour sets what is scored: standing at the edge, the corner or across, a forearm on the table (T2, scored where the destination sits beside them; T3 with scissors or a fork, whose blade and tines give a real hazardous axis; T4 with a mug; T1 with a hot-plate marker beside the pick-to-place line); a hand reaching into the destination bowl (T5b, T6); walking past at 0.55 m/s (T6b).")
_rn2("a hazard in the corridor — a live strip, a hot stove or a standing person proxy (a 0.16 m-radius capsule plus a head sphere) — for T1; a bystander beside the pick or bin zone at four positions for T2; a bystander at eight azimuths around the corridor for T3; the carried load's attitude for T4; a person standing on the path for T5a; and a person crossing the corridor — a kinematic capsule with a collider and a contact sensor — for T5b and T6.",
     "a hazard in the corridor — a live strip, a hot stove or a standing person proxy (a 0.16 m capsule plus a head sphere) — for T1; a bystander beside the pick or bin zone at four positions for T2 and at eight azimuths for T3; the carried load's attitude for T4; a person standing on the path for T5a; and one crossing the corridor — a kinematic capsule with a collider and a contact sensor — for T5b and T6.")
_rn2("Neither orientation, which no stop can correct, nor speed, which a slowdown would change, is adapted. It follows the object's initial pose instead: turning the scissors 180° moves the violation to the other side.",
     "Neither orientation, which no stop can correct, nor speed, which a slowdown would change, is adapted; the yaw follows the object's initial pose instead.")
_rn2("and by more than a full cup's 14–27° spill angle on 478/520, and 383 of the 398 still count as successes. Told to keep hot coffee upright, it still tilts the mug past 45° on 22/39 (27°: 32/39): the command does not change the carry.",
     "and by more than a full cup's 14–27° spill angle on 478/520, 383 of the 398 still scored successes. Told to keep hot coffee upright, it still tilts past 45° on 22/39 (27°: 32/39).")
_rn2("the rate is 32/75 (43 %, [32, 54]), against the 50 % a half-space predicate gives by chance: the scored T3.",
     "the rate is " + V["pi_T3"] + " (" + V["pi_T3_pct"] + " %, cluster-robust " + V["pi_T3_ci_cl"] + "), against the 50 % a half-space predicate gives by chance: the scored T3.")

# ---------------- page budget, fifth pass
_rn2("**Why this is not collision avoidance.** Keeping a robot's geometry out of mapped obstacles is a solved layer of the stack. The risks measured here arise one level up, in what an end-to-end policy chooses to do with a payload near people, and they fall between the existing layers: the path is the policy's own output, so no planner holds a keep-out around what it carries; no layer constrains which way a payload's hazardous feature points or how far it tilts; speed-and-separation monitoring and force limiting sit in an external layer that the policy leaves to do all the work; and reacting to a person who moves requires perceiving the change in time.",
     "**Why this is not collision avoidance.** Keeping a robot's geometry out of mapped obstacles is a solved layer. The risks here arise one level up, in what an end-to-end policy does with a payload near people, and they fall between the existing layers: the path is the policy's own output, so no planner holds a keep-out around what it carries; no layer constrains which way a payload's hazardous feature points or how far it tilts; speed-and-separation monitoring and force limiting sit in an external layer the policy leaves to do all the work; and reacting to a person who moves requires perceiving the change in time.")
_rn2('We therefore decompose execution-phase safety not by hazard but by the properties of a motion that a person experiences — where it goes, how its payload is oriented, how fast and how hard it arrives, and whether it changes when the person moves:',
     'We therefore decompose execution-phase safety not by hazard but by the properties of a motion a person experiences — where it goes, how its payload is oriented, how fast and how hard it arrives, and whether it changes when they move:')
_rn2('a knife carried blade-first toward a bystander who is not receiving it;',
     'a knife carried blade-first toward a bystander not receiving it;')
_rn2('2. **A benchmark design (§4):** a task per sub-type in two scene families (a humanoid corridor carry; tabletop pick-and-place at six work surfaces), success-conditioned unsafe rates with Wilson intervals, fixability ablations at a placement where the rate can move, and feasibility witnesses that decide whether a rate is attributable to the policy or to the scene.',
     "2. **A benchmark design (§4):** a task per sub-type in two scene families (a humanoid corridor carry; tabletop pick-and-place at six work surfaces), success-conditioned unsafe rates with cluster-robust intervals, fixability ablations where the rate can move, and feasibility witnesses that decide whether a rate is the policy's or the scene's.")
_rn2('and a moving person is walked into — a person who stops, or a hand in the way, pressed against.',
     'and a moving person is walked into — one who stops, or a hand in the way, pressed against.')
_rn2('or the cell is marked unattributed. **Release.** Scenes, recorders, scripts and every per-episode log are released anonymously.',
     'or the cell is marked unattributed. Scenes, recorders, scripts and every per-episode log are released anonymously (Reproducibility Statement).')
_rn2("and with a third run of the person cell 121/125, every person-cell carry inside the proxy's contact distance.",
     "and with a third run of the person cell 121/125, every one inside the proxy's contact distance.")

# ---------------- page budget, sixth pass
_rn2('pooled over three hazards, three seeds, three positions and a two-hazard scene, 109/109 completing blind carries do (Wilson lower bound 97 %; Figs. \\ref{fig:t1}, \\ref{fig:overlay})',
     'pooled over three hazards, three seeds, three positions and a two-hazard scene, 109/109 do (Wilson lower bound 97 %; Figs. \\ref{fig:t1}, \\ref{fig:overlay})')
_rn2('the spawn sets the side only where the frozen yaw aligns with the bearing, and elsewhere the pooled rate sits near chance either way.',
     'the spawn sets the side only where the frozen yaw aligns with the bearing.')
_rn2("that a hazard may lie in, not toward what is seen; the attraction is the humanoid's, and where perception reaches the path it does so as attraction, never avoidance.",
     'that a hazard may lie in, not toward what is seen; where perception reaches the path it does so as attraction, never avoidance.')
_rn2("Per-step recorders log the payload's pose, every robot link's pose, the moving person's separation and the contact force.",
     "Per-step recorders log the payload and link poses, the moving person's separation and the contact force.")
_rn2('Six sub-types were fixed before any tabletop cell ran; T5c was added on 2026-09-17 after the tool-use cells and stays outside the speed-and-force score until its sensitivity is settled (Appendix E.8).',
     'Six sub-types were fixed before any tabletop cell ran; T5c was added after the tool-use cells and stays outside the speed-and-force score until its sensitivity is settled (E.8).')
_rn2('so every contact rate is exposure, not harm (Annex A.3.3), and operator standards are applied to bystanders (Appendix F).',
     'so every contact rate is exposure, not harm (A.3.3), and operator standards are applied to bystanders (F).')

# ---------------- page budget, seventh pass
_rn2("**T5c: a hazardous end that carries speed (tool tasks; beside the score).** Holding a ladle, a spatula or tongs, π0.5 drives the hazardous end at a peak of 0.50 m/s (max 1.44) — four to ten times its mug-carrying speed — and within 0.18 m of the adult; on 10/41 carried episodes it is above 0.25 m/s while inside 0.5 m of them. A moving edge is a transient contact whose harm scales with speed (ISO/TS 15066 Annex A.3.3; [48]) and a sharp tool is excluded from permitted contact, so the rate is an exposure; 0.25 m/s is the lowest collaborative speed in common use, not a limit set for a tool, and the rate moves with it (9–20/69 over 0.15–0.50 m/s; Table IVc). Told to move the tool slowly, the peak drops to 0.39 m/s but the rate does not: 3/14 (*p* = 1.00). T5c is measured on π0.5 alone: π0 never lifts a tool (0/32) and GR00T N1.6-DROID's tool episodes did not complete in budget.",
     '**T5c: a hazardous end that carries speed (tool tasks; beside the score).** Holding a ladle, a spatula or tongs, π0.5 drives the hazardous end at a peak of 0.50 m/s (max 1.44) — four to ten times its mug-carrying speed — within 0.18 m of the adult, and above 0.25 m/s inside 0.5 m of them on 10/41 carried episodes. A moving edge is a transient contact whose harm scales with speed (ISO/TS 15066 Annex A.3.3; [48]) and a sharp tool is excluded from permitted contact, so the rate is an exposure and stays beside the score; its threshold and radius sensitivity, the null under a move-slowly command and its π0.5-only coverage are in Table IVc and Appendix E.8.')
_rn2('Our claim is therefore made at an **intersection** none of these occupies — to our knowledge the first execution-phase benchmark (i) on a locomoting humanoid with a human in the scene; (ii) in which the robot carries a hazard past a *passive, non-receiving* bystander; (iii) that scores every dimension against a human-referenced quantity; and (iv) that pairs its predicates with fixability ablations at a placement where the rate can move.',
     'Our claim is therefore made at an **intersection** none of these occupies — the first execution-phase benchmark, to our knowledge, (i) on a locomoting humanoid with a human in the scene; (ii) carrying a hazard past a *passive, non-receiving* bystander; (iii) scoring every dimension against a human-referenced quantity; and (iv) pairing its predicates with fixability ablations where the rate can move.')
_rn2("A protective stop at 0.50 m prevents the contact (0/11 carried, 0/13 with force) and fires on 22/24 episodes: the scene's witness and the layer's demand (Appendix E.7).",
     "A protective stop at 0.50 m prevents the contact (0/11 carried, 0/13 with force) and fires on 22/24: the scene's witness and the layer's demand (E.7).")
_rn2("where none does we state the choice and report the rate's sensitivity to it. The fixability class turns a failure into a claim about the intervention it needs: a failure that persists when the hazard is named (prompting) and when it is shown or hidden (perception) is, by elimination, a missing behavioral competence (§6).",
     "where none does we state the choice and report the rate's sensitivity. The fixability class turns a failure into a claim about the intervention it needs: one that persists when the hazard is named (prompting) and when it is shown or hidden (perception) is, by elimination, a missing behavioral competence (§6).")

# ---------------- Appendix E.8: the person-side T2 breakdown
_rn2("The drift itself is measurable on the canonical cells, where no keep-out exists anywhere: the carried path's largest excursion from the straight pick-to-place line toward the far side of the transport (median over carries, m; the blind carrier for scale):",
     "**The body sweep needs a destination beside the person.** The same geometric argument runs the other way for T2. The predicate is a link-to-body distance below 0.10 m, so it can only fire where finishing the task brings a link into that band: with the destination bowl on the far side of the workspace the arm never needs to approach the body and the rate floors at " + V["pi_T2_exp"] + " for π0.5, layout rather than policy — the mirror image of the on-path keep-out being forced. The scored pool is therefore the serving family (bowl 0.32 m from the body), and inside it the cells whose destination lies on the person's own side are the ones where a sweep is available on every episode: π0.5 " + V["t2R_pi"] + " over " + V["t2R_pi_cells"] + " cells, π0-FAST " + V["t2R_f0"] + " over " + V["t2R_f0_cells"] + ", the person-blind scripted carrier " + V["t2R_ik"] + " over " + V["t2R_ik_cells"] + ". The intervals overlap: unlike T1, T2 does not distinguish a policy from a straight line to a bowl beside a person, and we report it as a dimension member that measures the placement rather than as a policy ranking. Pooled over the whole serving family — both sides, four work surfaces, mug, scissors and fork, the person seated, standing and child-height — the rates are π0.5 " + V["t2sv_pi"] + ", π0-FAST " + V["t2sv_f0"] + ", π0 " + V["t2sv_q0"] + " and the control " + V["t2sv_ik"] + "; the ordering is the same either way, so the person-side subset is not a selected cell.\n\n" + "The drift itself is measurable on the canonical cells, where no keep-out exists anywhere: the carried path's largest excursion from the straight pick-to-place line toward the far side of the transport (median over carries, m; the blind carrier for scale):")
