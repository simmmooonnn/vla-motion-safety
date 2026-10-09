# -*- coding: utf-8 -*-
# 2026-10-09, a193 region appEF (Appendices D-H only; the main text is untouched, word delta 0).
# Folds the skeptic-checked findings of _scratch/tmp/now_results.json into the appendices (each entry's 'check' block wins):
#  F1 fk_arc     : a joint-space-linear blind carry between the same pick/place poses (kinematic model, not a run) bows 4-5 cm to
#                  the far side and would enter the far 0.20 m keep-out 64/64, the 0.28 m 0/64, the near side 0/24; ~80/160 of the
#                  matched T1 pool vs pi0.5 90/159 (Fisher 0.26, heuristic vs a deterministic model). Unexplained: desk 0.28 m 11/16
#                  vs 0/16, near-side rendered twin 6/24 vs 0/24 (p 0.022 uncorrected, vs a noiseless arm). pi0.5's logged joint
#                  commands are NOT a joint-space line -> "consistent with joint-space-like motion"; T1 excess over the control
#                  depends on its Cartesian interpolation; an actual joint-space control (A2) is planned.  -> E.8 grid, twin, new
#                  kinematic-model paragraph, radius probe, Table IIIf caption, F bullet, F closing.
#  F2 t1_offset  : signed mid-transport offset +4.3/+4.2/+5.8/+12.7 cm vs control -0.1; side/rendering-independent; T1 cannot
#                  identify 'base-relative' (all transports along -y; serving cells point both ways) -> "consistent far-side bend";
#                  0.20 m is tangent to the control's line, 0.28 m informative (36/144 vs 0/144 two-sided); pi0 near side at packing.
#  F3 t2_cond    : delivered (placement-matched) stratum 26/56, 32/56, 14/14, 5/6 vs 0/24 (p 0.0003/0.0002/0.0002/0.0008); entries at
#                  the bowl during placement; thin margin (control 0.131-0.185 m; 9/24 at 0.14 m, 17/24 at 0.15 m); pi0 0/57 is a
#                  capability boundary (3/57 reach the bowl); GR00T "with or without the mug" = uncarried 31/32, 36/48.
#  F4 g0_cut35   : GR00T 90 s T1/T4 cut at 35 s: T1 8/9 (IIIf 8/9 vs 5/48, 4 vs 6 cells, p 0.019, Holm 0.171), T4 18/57 (IIIf 3/10
#                  vs 3/31, p 0.307; stratified exact 0.316); 0.28 m 7/8 of 8/23 carries; t1u28 15/17; t1n28 0/13.
#  F5 t5a_vh0    : v_h = 0 floors the canonical T5a for every arm incl. the control; serving-cell excess is proximity, not speed,
#                  on a 2 cm margin -> the tabletop exposure reading rests on v_h = 1.6 m/s (D, IIIb, IVe, E.8 T5a, GR00T, F).
#  F6 power_tost : only 3 of 12 IIIf rows could read 'safer' after Holm; T1 rows + GR00T T4 exclude a safer difference; pi0.5 T3 at
#                  most 21 pts safer; small T3 rows and T4 rows untested, not null (IIIf caption, F bullet, F closing).
#  F7 dose_strat : stratified cell-level test over the three prompt experiments (pi0.5 141/170 vs 6/79, p 1.9e-7; pi0-FAST 33/64 vs
#                  4/48, p 0.0013, all from the dose experiment; pooled 2.5e-10); spill vs upright alone 0.029 per policy (floor),
#                  0.0004 pooled; tilt builds late, mostly over the bowl (E.8 T4, F bullet).
#  F8 provenance : GR00T 242/803 splits 148/367 (90 s) + 94/436 (35 s); pi0's four 20 s serving cells inside T2 1/64 and 1/48
#                  (IIIb note, E.8 T2 paragraphs).  (Table X labels and the Setup sentence live in Appendices A/C: not this region.)
# Exec'd at the end of the chain (uses t, _rn2).

# ---------------------------------------------------------------- Appendix D
_rn2("(tabletop π0.5 87/93 at a 0.20 m offset, 12/94 at 0.28 m), so both offsets are reported",
     "(tabletop π0.5 87/93 at a 0.20 m offset, 12/94 at 0.28 m), so both offsets are reported; at 0.20 m the control's straight "
     "line runs tangent to the keep-out, so its rate there is set by millimetres and the 0.28 m level is the informative one for "
     "the comparison with the control (E.8)")
_rn2("scored on the mobile G1 only — a table-side arm works inside the stop distance, and its collaborative mode is power-and-force "
     "limiting (T5b)",
     "scored on the mobile G1 only — a table-side arm works inside the stop distance that the walking-human term sets ($v_h$ = 1.6 "
     "m/s, $d_0$ = 0.94 m; with $v_h$ = 0, the G1 governor's setting, every tabletop arm and the control sit near zero on the "
     "canonical cells, E.8), and its collaborative mode is power-and-force limiting (T5b)")

# ---------------------------------------------------------------- E.8: Table IIIb caption
_rn2("T5a on the tabletop is exposure (the arm works inside $d_0$), not a score;",
     "T5a on the tabletop is exposure (the arm works inside $d_0$ = 0.94 m, which the walking-human term $v_h$ = 1.6 m/s sets; at "
     "$v_h$ = 0 the canonical cells floor near zero for every arm, the control included; E.8), not a score;")
_rn2("6/7 in two further seeds; §5.4, E.7).\n\n| Policy | T1 payload path",
     "6/7 in two further seeds; §5.4, E.7). GR00T N1.6-DROID's T1–T4 cells ran 90 s episodes (all but one T3 cell), its T6 and "
     "T6b cells and the control's cells 35 s: cut at 35 s, its T1 reads 8/9 and its T4 18/57 (E.8). Four of π0's eight T2 cells "
     "(0/32) ran 20 s episodes, and one of them also enters its T3 and another its T4; without them its T2 reads 1/32, its T3 "
     "7/12 and its T4 8/129.\n\n| Policy | T1 payload path")

# ---------------------------------------------------------------- E.8: Table IVe caption and T5a row
_rn2("T5a is exposure on the tabletop and scored on the humanoid only;",
     "T5a is exposure on the tabletop (at the walking-human term $v_h$ = 1.6 m/s; E.8) and scored on the humanoid only;")
_rn2("| the humanoid corridor; on the tabletop an exposure (the arm works inside $d_0$) |",
     "| the humanoid corridor; on the tabletop an exposure (the arm works inside $d_0$ = 0.94 m, set by the walking-human term) |")

# ---------------------------------------------------------------- E.8: Table IIIf caption (F1, F4, F6)
_rn2("No row reads *safer than the control*.\n\n| Policy | Sub-type | Policy k/n",
     "No row reads *safer than the control*, but only three rows could have (π0.5 T1, π0 T1, π0.5 T3): for the other nine even "
     "a policy with no violations on the same cells would not reach Holm significance. The four T1 rows and GR00T N1.6-DROID's "
     "T4 (in its 90 s episodes) exclude any safer difference (one-sided 95 % bounds +16 to +75 and +11 points) and π0.5's T3 is "
     "at most 21 points safer; "
     "π0's, π0-FAST's and GR00T N1.6-DROID's T3 (60–108 relabellings) and the other three T4 rows (the control tilts on 3/31) "
     "could not have shown a policy safer, so their *not distinguishable* means untested, not null. The T1 rows compare each policy with a Cartesian "
     "straight line, which at 0.20 m runs tangent to the keep-out: a kinematic model that interpolates in joint space between the "
     "same pick and place poses bows 4–5 cm to the far side and would enter on about 80/160 of the matched carries against "
     "π0.5's 90/159 (Fisher *p* 0.26, heuristic), so the T1 excess depends on the control's interpolation (E.8); the model enters "
     "no 0.28 m keep-out, which every policy enters on some carries (GR00T N1.6-DROID on 15/15). A joint-space control is planned. "
     "GR00T N1.6-DROID's T1 and T4 rows come from 90 s episodes against the control's 35 s; cut at 35 s they read 8/9 against "
     "5/48 (4 vs 6 cells, *p* 0.019, Holm 0.171: not distinguishable, and with 4 vs 6 cells no data could reach Holm "
     "significance) and 3/10 against 3/31 (*p* 0.307).\n\n| Policy | Sub-type | Policy k/n")

# ---------------------------------------------------------------- E.8: GR00T T4 paragraph after Table IIIf (F4)
_rn2("and is not seen past 27° (10/18 against 13/31, *p* = 0.45; Table IIIf). ",
     "and is not seen past 27° (10/18 against 13/31, *p* = 0.45; Table IIIf). Its carries come from 90 s episodes; cut at 35 s "
     "the three placements give 3/10 against 3/31 (cell permutation *p* 0.307; the stratified exact test 0.316). ")

# ---------------------------------------------------------------- E.8: T2 paragraph (F3, F8)
_rn2("π0 does not come closer (1/64).",
     "π0 comes within the band on 1/64 (four of its eight cells, 0/32, ran 20 s episodes), but it rarely brings the mug to the "
     "bowl: on the pre-registered cell its lifted mug reaches the bowl on 3/57, so its 0/57 there measures competence, not a "
     "safe carry.")
_rn2("links 0.13–0.19 m from the body on every episode; delivered 24/64)",
     "links 0.13–0.19 m from the body on every episode; delivered 24/64, the other 40 holding the mug above the bowl until the 35 s "
     "timeout)")

# ---------------------------------------------------------------- E.8: T4 dose experiment (F7)
_rn2("the clause about spilling raises the tilt on its own (π0.5 30/32, π0-FAST 14/27; Fisher *p* < 0.001 each against neutral),",
     "the clause about spilling raises the tilt on its own (π0.5 30/32, π0-FAST 14/27; Fisher *p* < 0.001 each against neutral; "
     "against the upright clause alone, with cells as units, *p* = 0.029 for each policy, the smallest that four cells against "
     "four allow, and 0.0004 pooled over the two),")
_rn2("though placed first it lowers π0-FAST's deliveries (21/32 against 32/32, *p* < 0.001).",
     "though placed first it lowers π0-FAST's deliveries (21/32 against 32/32, *p* < 0.001). Over the three prompt experiments "
     "(the same-day rerun, the prompt control and the dose experiment), a cell-level permutation test stratified by experiment and "
     "policy gives π0.5 141/170 carries past 45° with the spill clause against 6/79 with the neutral instruction (*p* = 1.9 × "
     "10⁻⁷, the smallest attainable) and π0-FAST 33/64 against 4/48 (*p* = 0.0013, all of it from the dose experiment; its prompt-control run is null); "
     "pooled, *p* = 2.5 × 10⁻¹⁰.")
_rn2("on the prompt control's new seeds 3 of the 27 under the sentence alone).",
     "on the prompt control's new seeds 3 of the 27 under the sentence alone). Over the three prompt experiments the excess comes "
     "late along the path: before the mug is half-way to the bowl it is small (π0.5 15/170 against 1/79, cell permutation *p* "
     "0.072), and π0.5's first exceedance falls within 0.10 m of the bowl on 93/141 spill-clause carries, so much of the tilt is "
     "over the bowl, where it may be a pour rather than a spill toward the person. For π0.5 the excess is not a matter of the "
     "spill-clause carries lasting longer: it is already there within 3 s of the lift (81/170 against 4/79, *p* 8 × 10⁻⁴); "
     "π0-FAST's is not detectable that early (3/64 against 0/48, inconclusive).")

# ---------------------------------------------------------------- E.8: T5a (F5)
_rn2("**T5a.** With the person at the table, transports exceed the envelope's allowed speed on 255/272 (exposure, not scored; the "
     "arm works inside the 0.94 m stop distance), and the near-band payload speed is",
     "**T5a.** With the person at the table, transports exceed the envelope's allowed speed on 255/272 (exposure, not scored; the "
     "arm works inside the 0.94 m stop distance). That reading rests on the walking-human term ($v_h$ = 1.6 m/s): re-scored post "
     "hoc with $v_h$ = 0, the G1 governor's setting ($d_0$ = 0.30 m), the canonical cells floor near zero for every arm, the "
     "control included (π0.5 2/272, π0 0/40, π0-FAST 0/78, GR00T N1.6-DROID 0/35, control 2/208; the transports pass a median "
     "0.54–0.70 m from the person), a floor the control shares, so the tabletop speed column stays the exposure reading at $v_h$ "
     "= 1.6 m/s and enters no score. On the pre-registered serving cell, read exploratorily at $v_h$ = 0, π0-FAST and GR00T "
     "N1.6-DROID exceed the control (24/59 and, in 90 s episodes, 12/22 against 3/64; π0.5 does not, "
     "3/57), but the excess is proximity, not speed — at the closest approach the violating policies move slower than the control (median 0.065 and "
     "0.125 against 0.145 m/s) — and it turns on a 2 cm margin (the bowl sits 0.316–0.330 m from the person's centre; at $d_0$ = "
     "0.32 m the control enters on 19/64). The near-band payload speed is")

# ---------------------------------------------------------------- E.8: GR00T N1.6-DROID paragraph (F4, F5, F8)
_rn2("runs in this family but slowly: with 90 s episodes it carries on 242/803 episodes. Where it carries, the mug leaves upright by "
     "more than 45° on 36/97 (9–125°); its links come within 0.10 m of the person on 27/38 episodes with the bowl beside them; "
     "transports with the person at the table exceed the envelope's allowed speed on 35/35;",
     "runs in this family but slowly: it carries on 242/803 episodes (148/367 on its 57 cells with 90 s episodes, 94/436 on its 59 "
     "cells with 35 s ones). Where it carries, the mug leaves upright by more than 45° on 36/97 (9–125°; 90 s cells, and 40 of the "
     "97 carries start after 35 s: cut at 35 s, 18/57); its links come within 0.10 m of the person on 27/38 episodes with the bowl "
     "beside them (90 s cells); transports with the person at the table exceed the envelope's allowed speed on 35/35 (exposure; "
     "0/35 at $v_h$ = 0);")

# ---------------------------------------------------------------- E.8: off-path keep-out grid (F1, F2, F4)
_rn2("GR00T N1.6-DROID, which carries 15/23 there, on 15/15 at 0.13 m)",
     "GR00T N1.6-DROID, which carries 15/23 there in its 90 s episodes, on 15/15 at 0.13 m; within the first 35 s it carries 8/23 "
     "and enters on 7/8)")
_rn2("— a straight carry clears the keep-out and π0.5 enters it on 12/64 carries —",
     "— a straight carry clears the keep-out, and so would a joint-space line between the same poses (0/64 in the kinematic model "
     "below), and π0.5 enters it on 12/64 carries —")
_rn2("while the policy enters on 62/63 — the sharpest and most uniform contrast in the series, every surface alike;",
     "while the policy enters on 62/63 — the most uniform contrast in the series, every surface alike, but its size is set by the "
     "control: the straight line runs tangent to the keep-out, so its rate turns on millimetres, and a joint-space line between the "
     "same poses would enter on 64/64 (kinematic model below);")
_rn2("and GR00T N1.6-DROID on 10/10 of its carries (median 0.10 m).",
     "and GR00T N1.6-DROID on 10/10 of its carries (median 0.10 m, in 90 s episodes; their first 35 s hold one carry, which "
     "enters).")

# ---------------------------------------------------------------- E.8: twin paragraph -> signed offset (F2)
_rn2("the keep-out rate of Table III is the policies' bow toward the far side, which a rendered hazard neither causes nor corrects.",
     "the keep-out rate of Table III is the policies' bow toward the far side, which a rendered hazard neither causes nor corrects. "
     "Measured as the carried object's signed offset from the pick-to-place line at mid-transport (positive to the far side; "
     "cell-clustered 95 % intervals, Table III's T1 pools), the bow is +4.3 cm [3.4, 5.2] for π0.5, +4.2 [2.1, 6.3] for π0, +5.8 "
     "[4.6, 7.0] for π0-FAST and +12.7 [10.3, 15.2] for GR00T N1.6-DROID, against −0.1 cm for the control; it does not detectably "
     "change with the keep-out's side or rendering (far minus near on the twin: π0.5 +0.6 cm [−0.6, +1.9], π0-FAST +0.1 [−0.9, +1.1]), so it "
     "is a consistent far-side bend, not a response to the hazard. π0 is the exception at the packing station, where it bends to "
     "the near side (4 cells, −2.3 to −5.1 cm). Mirroring each 0.28 m keep-out across the line makes the level two-sided: the "
     "mirrored pair is entered by π0.5 on 36/144 carries against the control's 0/144 on the cells both ran (+25 points [+9, +41]), "
     "almost only on the far side.")

# ---------------------------------------------------------------- E.8: reversal -> 'base-relative' withdrawn (F2 check)
_rn2("the bow stays on the same side of the world, away from the base, when the transport is reversed: it is base-relative, a "
     "property of where the arm is mounted, not of the direction of travel.",
     "the bow stays on the same side of the world, away from the base, when the transport is reversed, though at the desk it "
     "halves: its side is not set by the direction of travel. Whether it is referenced to the base or to the world cannot be told "
     "from these cells, whose transports all run parallel to the y axis on the +x side of the base, so that away from the base and "
     "+x coincide; the serving cells, whose transports run in other directions, point both ways (π0.5 bends toward the base at the kitchen counter and away from it at the office desk, with a person beside the "
     "bowl in both), so on the T1 cells we call it a consistent far-side bend.")

# ---------------------------------------------------------------- E.8: radius probe + kinematic model paragraph (F1)
_rn2("The shrinking is consistent with a pull toward the demonstrations' workspace, but the probe does not establish the cause.",
     "The shrinking is consistent with a pull toward the demonstrations' workspace and, qualitatively, with joint-space-like "
     "motion (below), but the probe does not establish the cause.")
_rn2("the inner edge of the demonstrations' workspace.\n\n**π0-FAST on the task battery.**",
     "the inner edge of the demonstrations' workspace.\n\n"
     "**A joint-space reading of the bend (kinematic model, not a run).** The control interpolates in Cartesian space. A blind "
     "carry that instead interpolates linearly in joint space between the same pick and place poses (Franka kinematics, inverse "
     "kinematics at each episode's logged endpoints, tool vertical) bows to the far side by 0.054 m at the counter and the drawer "
     "kitchen, 0.043 m at the desk and 0.036 m at the packing station, never to the near side, and stays on the far side over "
     "carry height, tool length, elbow swivel and tool tilts up to 40° (counter 0.051–0.065 m, desk 0.041–0.061 m, packing "
     "0.032–0.057 m); it is close to an arc about the base. Scored on the T1 cells, such an arm would "
     "enter every far-side 0.20 m keep-out (64/64), no 0.28 m one (0/64) and no near-side one (0/24 on the twin): about 80/160 of "
     "Table IIIf's matched pool, against π0.5's 90/159 (Fisher *p* 0.26, a heuristic test against a deterministic model) and the "
     "Cartesian control's 18/160. Two sets of entries remain that it would not make: the desk's 0.28 m keep-out (π0.5 11/16 against "
     "0/16; π0.5 bows 0.089 m there, twice the model) and the near-side rendered twin (6/24 against 0/24, *p* 0.022 uncorrected, "
     "against a noiseless model arm, so a weak excess). The model matches the bend's direction and, in peak excursion, roughly its "
     "size at the counter and the packing station (π0.5's path is flatter than the model's arc and, at mid-transport, lower: "
     "0.035 against 0.054 m at the counter), but not the desk, nor the radius probe's fall-off (0.068 to 0.031 m against π0.5's "
     "0.099 to 0.018 m), nor the halving on the reversed desk transport. Joint commands logged on four π0.5 scissors carries "
     "(another geometry, 0.60–0.70 m from the base) leave the joint-space line by 15–36 % of the joint travel and on two of them "
     "bend opposite to the model, so π0.5 does not move in a joint-space line: the bend is consistent with joint-space-like "
     "motion, and π0.5's T1 excess over the control (Tables IIIb, IIIf) depends on the control being a Cartesian line. GR00T "
     "N1.6-DROID's bend (+12.7 cm at mid-transport) is well beyond the model's, which would make none of its 0.28 m entries "
     "(15/15). An actual joint-space control on the T1 cells is the planned test.\n\n"
     "**π0-FAST on the task battery.**")

# ---------------------------------------------------------------- E.8: two markers / GR00T near side (F2, F4)
_rn2("The bend is one-sided — away from the base — so a second hazard neither cancels it nor draws its own. GR00T N1.6-DROID, whose "
     "far-side entries were 15/15, enters the near-side marker on 0/16 and the unrendered far-side keep-out on 23/25: the same "
     "base-relative bend.",
     "The bend is one-sided — to the far side, away from the base — so a second hazard neither cancels it nor draws its own. GR00T "
     "N1.6-DROID, whose far-side entries were 15/15, enters the near-side marker on 0/16 and the unrendered far-side keep-out on "
     "23/25 (90 s episodes; cut at 35 s, 7/8, 0/13 and 15/17): the same far-side bend.")

# ---------------------------------------------------------------- E.8: serving T2 pool paragraph (F3, F8)
_rn2("π0 1/48 = 2 % [0, 11] over 6,",
     "π0 1/48 = 2 % [0, 11] over 6 (four of them, 0/32, with 20 s episodes; 1/16 without),")
_rn2("Like T1, then, T2 separates three of the four policies from a straight line to a bowl beside a person; π0, which carries on "
     "16/57, does not.",
     "The excess is not a matter of carrying more. It holds among carried episodes and among delivered ones, the stratum that "
     "matches the control's placement (the control's 40 undelivered episodes hold the mug above the bowl until the timeout, "
     "farther from the body, median 0.179 m): π0.5 26/56, π0-FAST 32/56 and GR00T N1.6-DROID 14/14 (90 s) and 5/6 (35 s) against "
     "the control's 0/24 (post hoc strata; cell permutation *p* 0.0003, 0.0002, 0.0002 and 0.0008). The policies' entries happen at the bowl during "
     "placement (π0.5 26/26, π0-FAST 33/34 with the mug within 0.15 m of the bowl). The margin is thin: the control's placement "
     "passes 0.131–0.185 m from the body, so at a 0.14 m threshold it enters on 9/24 delivered episodes and at 0.15 m on 17/24, "
     "while the policies' excess persists at every threshold from 0.08 to 0.15 m. GR00T N1.6-DROID's arm sweeps the body with or "
     "without the mug: on the episodes in which it never carries it, on 31/32 (90 s) and 36/48 (35 s). T2 thus separates three of "
     "the four policies from a straight line to a bowl beside a person. π0 does not, but its lifted mug reaches the bowl on only "
     "3/57 episodes (0/3 in the band there): its 0/57 measures competence, not a safe carry, though, unlike GR00T "
     "N1.6-DROID's, its arm also stays out of the band on the episodes in which it never carries the mug (0/41).")
_rn2("π0-FAST 16/96 (17 %), π0 1/64 (2 %),",
     "π0-FAST 16/96 (17 %), π0 1/64 (2 %; the same four 20 s cells included),")

# ---------------------------------------------------------------- Appendix F: coverage, new bullets, closing
_rn2("T5c is post hoc, the tabletop T5a and speed-and-force cell are exposure,",
     "T5c is post hoc, the tabletop T5a and speed-and-force cell are exposure (T5a at the walking-human term; at $v_h$ = 0 every "
     "arm and the control floor near zero),")
_rn2("Every quantitative claim should be read as a small-sample, simulation-only result.\n",
     "Every quantitative claim should be read as a small-sample, simulation-only result.\n"
     "- **What the T1 control fixes.** The straight-line control interpolates in Cartesian space, and at 0.20 m its line runs "
     "tangent to the keep-out, so its 18/160 is set by millimetres. A kinematic model that interpolates in joint space between the "
     "same poses bows 4–5 cm to the far side and would enter on about 80/160 of π0.5's matched carries (π0.5 90/159; Fisher *p* "
     "0.26, heuristic), leaving for π0.5 only the desk's 0.28 m cells (11/16 against 0/16) and a weak near-side excess (6/24 "
     "against 0/24, uncorrected *p* 0.022) unexplained (E.8). The policies' T1 excess over the control, and the T1 rows of Table "
     "IIIf, therefore depend on the control's interpolation, though the model makes none of the 0.28 m entries (GR00T N1.6-DROID "
     "15/15); the bend itself — pooled, +4 to +13 cm at mid-transport for every policy, −0.1 cm for the control — is measured. π0.5's logged joint commands do not follow a joint-space line, so the model is a reference, not the mechanism; an "
     "actual joint-space control is planned.\n"
     "- **Power of the control comparisons.** Only three of Table IIIf's twelve rows (π0.5 T1, π0 T1, π0.5 T3) could have read "
     "*safer than the control* after Holm correction. The four T1 rows and GR00T N1.6-DROID's T4 (90 s episodes) exclude a safer "
     "difference by their one-sided bounds and π0.5's T3 is at most 21 points safer; the other three T3 rows and three T4 rows (the control "
     "tilts on 3/31 carries) could not have shown a policy safer, so they are untested, not null. A 20-point safer T3 would need "
     "about 65 cells of eight scored episodes per arm with the current interval (114 under Holm), or at least 16 (20 under Holm) "
     "with a pre-registered placement-stratified one, which needs two cells on each of eight placements; several arms score only "
     "0.3–0.7 episodes per attempt (the T4 control 31 of 112), so the run cost is higher still.\n"
     "- **Episode lengths.** GR00T N1.6-DROID's T1–T4 cells ran 90 s episodes (all but one T3 cell; 57 of its 116 cells overall, "
     "59 at 35 s), the control's 35 s. Most of its T1 carries start after 35 s (16/25); cut at 35 s its T1 reads 8/9 and its T4 "
     "18/57, and its Table IIIf T1 row 8/9 against 5/48 (Holm 0.171, about the lowest that 4 vs 6 cells allow). π0's four 20 s "
     "serving reruns sit in its T2 (0/32), and two of them in its T3 and T4 (one cell each). Both are disclosed beside the values "
     "(Table IIIb, E.8).\n"
     "- **A thin T2 margin.** The pre-registered T2 contrast holds placement-matched (delivered: π0.5 26/56, π0-FAST 32/56, GR00T "
     "N1.6-DROID 14/14 against 0/24), but the control's placement passes 0.131–0.185 m from the body: a placement about 3 cm "
     "closer would enter the band, and at a 0.15 m threshold the control enters on 17/24 delivered episodes. π0's 0/57 is a "
     "competence limit (its lifted mug reaches the bowl on 3/57 episodes).\n"
     "- **What the prompt effect is.** The spill clause's tilt comes late along the path and mostly over the bowl (π0.5's first "
     "exceedance within 0.10 m of it on 93/141), so part of it may be a pour into the bowl rather than a spill toward the person; "
     "its relevance to a scald is not assessed.\n")
_rn2("a keep-out defect on every policy (T1),",
     "a far-side bend into the keep-out on every policy (T1; its excess over the control depends on the control's Cartesian line, "
     "E.8),")
_rn2("(26/60, 34/64 and 51/54 against 0/64; T2)",
     "(26/60, 34/64 and 51/54 against 0/64; placement-matched, 26/56, 32/56 and 14/14 against 0/24; T2)")
_rn2("whose mug stays upright unless they are told not to spill the coffee.",
     "whose mug stays upright unless they are told not to spill the coffee; where no safer verdict was attainable (Table IIIf), "
     "the comparison is reported as untested.")
