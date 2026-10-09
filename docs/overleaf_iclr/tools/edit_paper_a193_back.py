# -*- coding: utf-8 -*-
# 2026-10-09 (a193, back region: sections 6-9 and the Reproducibility Statement). Applies the verified findings of
# _scratch/tmp/now_results.json (each entry's 'check' block taking precedence) without growing the main text.
#  F7 (dose_strat): 6(i)'s inference 'the spill clause, not the object named, drives it' rested on the bowl-vs-mug p = 1.00;
#     replaced by the direct cell-level test of 'do not spill the coffee' against 'keep the mug upright' alone (p = 0.029 for
#     pi0.5 and pi0-FAST each, the 4-vs-4 floor; 0.0004 pooled), and the spill-wording tilt is said to build late in the carry,
#     near the bowl. ('Tilt the mug as little as possible' has no spill clause and also raises it, so 'the spill clause drives
#     it' was too strong anyway; the bowl/mug referent swap stays in E.8.) The pooled three-experiment stratified test
#     (141/170 vs 6/79, p 1.9e-7) is left to the results text (5.2), not repeated here.
#  F1 (fk_arc) + F2 (t1_offset): 6(ii) reports the measured far-side bend (mean mid-transport offsets 4.2-12.7 cm, control
#     -0.1 cm), independent of the keep-out's side and rendering, as 'consistent with joint-space-like motion' (it does NOT say the
#     policy interpolates in joint space); section 8 states that pi0.5's T1 excess over the control rests on the control being a
#     Cartesian line (a modelled blind joint-space carry: about 80/160 against pi0.5's 90/159; not the desk's 0.28 m keep-out,
#     pi0.5 11/16 against 0/16), a prediction, not a run; a joint-space control is planned. (Only pi0.5 is named: the model was
#     run per episode for pi0.5 alone, and GR00T N1.6-DROID's 12.7 cm bend is far beyond the modelled 4-5 cm.)
#  F3 (t2_cond): section 8 drops 'not completion-matched' (the delivered stratum is the placement-matched comparison, reported in
#     the results) and states T2's thin margin (the control's set-down passes 0.13-0.19 m from the body).
#  F6 (power_tost): section 8 says the T4 and the three small T3 control comparisons could not have shown a policy safer:
#     untested, not null; section 9 says 'where a safer verdict was attainable' in place of 'where both ran'.
#  F8 (provenance): the Reproducibility Statement discloses episode lengths (pi0's four serving reruns on seeds 11 and 23 ran 20 s
#     and give 0/32 of its T2 1/64; GR00T N1.6-DROID ran 90 s on 34 of its 43 pooled cells). The Setup sentence (Appendix C)
#     and Table X's v2_smoke / replay labels are outside this region.
#  Offsets: 6's one-line preamble dropped; 6(i)'s naming/rendering shift clause cut to the naming null (the rendering shift is
#     6(ii)'s first sentence; details in E.2); 6(ii)'s humanoid sentence tightened and pi0-FAST's twin counts cut to 'alike';
#     6(iii)'s power aside, 6(iv)'s restatement of 5.4 and 7's witness gloss tightened; section 8 sends the witness list to F;
#     the Reproducibility Statement's T4-witness sentence compressed (surfaces in E.8) and its list of Appendix C contents
#     shortened (parameters stay in C, E.7 and section 5.3).
#  Skeptic pass (a193): 5.1/5.2 (edit_paper_a193_results.py) and F (appEF) now carry the bend offsets, the joint-space model
#     with its numbers, the T2 margin and the per-policy spill-vs-upright p, so 6(i), 6(ii) and 8 cite them instead of repeating
#     them (sections 6-9: -40 words, about 3 lines). 6(i): one term ('spill clause', as in 5.2) and 'late in the carry' tied to
#     the clause only (no location analysis exists for 'tilt as little as possible'); pooled p 0.0004 kept (E.8). 6(ii): no
#     longer files GR00T N1.6-DROID's 13 cm under 'joint-space-like' (the model bows 4-5 cm); points to 5.1, which keeps pi0's
#     near-side exception; twin counts named as pi0.5's and the garbled 'rendered and 22/24 not' restored. 8: 'physically'
#     restored; 'so pi0.5's T1 excess rests on that choice' (which contradicted 'though not the desk's 0.28 m') becomes 'rests
#     largely', stated for the T1 excess as 5.1 and F do. Reproducibility: 'every tabletop pool' (G1 episodes are not 35 s).
# Exec'd at the end of the chain (uses t, _rn2).

# ---- 6 preamble
_rn2("## 6. Diagnosis: Four Findings\n\nThe ablations ask whether a prompt or a percept can move the policies.\n\n",
     "## 6. Diagnosis: Four Findings\n\n")

# ---- 6(i): stove shift (offset) and the wording inference (F7)
_rn2("neither naming nor rendering lowers the violation (Table XI); each shifts completing carries by about 3 cm — naming away "
     "from a hidden stove (*p* = 0.017; 0.49 on two new seeds), rendering toward it (*p* = 0.013, 0.005) — among completers whose "
     "share the arms change (29–68 %). \"Do not spill the coffee\" and \"tilt the mug as little as possible\" raise the tilt "
     "(Table XIII; the second past 45° on 18/32, π0-FAST 21/28), \"keep the mug upright\" alone not detectably; "
     "keep-the-*bowl*-upright-so-it-does-not-spill does it as often as its *mug* version (26/32, 27/32), so the spill clause, not "
     "the object named, drives it.",
     "neither naming nor rendering lowers the violation (Table XI); naming's 3 cm shift away from a hidden stove did not "
     "replicate (E.2). A spill clause (\"do not spill the coffee\") and \"tilt the mug as little as possible\" raise the tilt "
     "(the clause's tilt mostly late in the carry, near the bowl); \"keep the mug upright\" alone does not detectably (against the "
     "spill phrase, cell permutation *p* = 0.0004 pooled over π0.5 and π0-FAST; §5.2, E.8).")
_rn2("It tilts π0's mug too (10/12 against 1/13, mostly in one cell),",
     "The clause tilts π0's mug too (10/12 against 1/13, mostly in one cell),")

# ---- 6(ii): a measured far-side bend, whatever the keep-out's side (F1, F2)
_rn2("**(ii) A visible hazard does not repel the path; the arm's path drifts whether or not one is there.** The humanoid's 2–5 "
     "cm shift toward a rendered stove (two substitute-driver seeds, replicated on two new ones; E.2) comes with a higher "
     "violation rate (17/51 against 15/83, *p* = 0.06; new seeds 32/36 against 22/33, *p* = 0.04). On the tabletop a keep-out "
     "0.20 m beside the transport is entered on 24/24 carries with its marker rendered and 22/24 without it on the far side, 6/24 "
     "and 1/24 on the near side (π0-FAST 20/20, 21/23; 1/21, 0/21; E.8).",
     "**(ii) A visible hazard does not repel the path; the arm's path bends whether or not one is there.** The humanoid's path "
     "shifts 2–5 cm toward a rendered stove (substitute-driver seeds, replicated on two new ones; E.2), with more violations "
     "(17/51 against 15/83, *p* = 0.06; 32/36 against 22/33, *p* = 0.04). On the tabletop the policies' carries bend to the far "
     "side whatever the keep-out's side or rendering (§5.1): π0.5 enters one 0.20 m beside the transport on 24/24 carries with "
     "its marker rendered and 22/24 without on the far side, 6/24 and 1/24 on the near side (π0-FAST alike; E.8).")

# ---- 6(iii): tighten the power aside (offset)
_rn2("(12 episode pairs, *p* = 0.28; E.1; a test with little power against a local detour)",
     "(*p* = 0.28, little power against a local detour; E.1)")

# ---- 6(iv): tighten the restatement of 5.4 (offset)
_rn2("No deceleration precedes contact at 0.3–1.2 m/s (T6) or on 17/18 scored encounters (T6b), and a person who stops at "
     "first touch is struck on every carried encounter (§5.4).",
     "No deceleration precedes contact (T6, 0.3–1.2 m/s; T6b, 17/18 encounters), and one who stops at first touch is struck on "
     "every carried encounter (§5.4).")

# ---- 7: tighten the witness gloss (offset)
_rn2("**(4)** a feasibility witness, so the rate is the policy's, not the scene's, or the cell is unattributed. Scenes, "
     "recorders, scripts and per-episode logs are released",
     "**(4)** a feasibility witness, without which the cell is unattributed. Scenes, recorders, scripts and logs are released")

# ---- 8: power (F6), the control's interpolation (F1), T2's margin (F3)
_rn2("The evidence is **simulation-only**: GR00T in one corridor (E.7), the other policies at the table. Cells are **small** "
     "(eight episodes per tabletop cell, 8–48 on the G1; a pre-registered replication of two policies on fresh seeds holds where "
     "its reference was valid, C), the G1 person cell's payload is labelled, not physically hazardous, and **the people have no "
     "state**: every proxy is static or kinematic, so every contact rate is exposure, not harm (§5.3), and operator standards are "
     "applied to bystanders (F). The **suite is smaller than its battery**, the matrix narrower still (F). T2's control "
     "comparison covers one pre-registered placement, not completion-matched (C); the witnesses are straight carries (T1, T2), "
     "geometric (T3), a pinch grasp (T4), a stop (T6) and a hold (T6b). F gives corrected measurement and run errors and Annex "
     "A's meaning for bystanders.",
     "The evidence is **simulation-only**: GR00T in one corridor (E.7), the other policies at the table, the G1 person cell's "
     "payload labelled, not physically hazardous. Cells are **small** (eight episodes per tabletop cell, 8–48 on the G1; a "
     "pre-registered replication holds where its reference was valid, C), and the T4 and three small T3 control comparisons "
     "are untested, not null (§5.5). **The people have no state**: every proxy is static or kinematic, so every contact rate is "
     "exposure, not harm (§5.3). The **control is a Cartesian line**: a modelled joint-space carry would enter the keep-outs "
     "about as often as π0.5, though none at 0.28 m (§5.1), so the T1 excess rests largely on that choice (a joint-space control "
     "is planned); T2's rests on one pre-registered placement with a thin margin (§5.1). The **suite is smaller than its "
     "battery**; F gives the witnesses, corrected errors and Annex A's meaning for bystanders.")

# ---- 9: attainability (F6)
_rn2("Across four public DROID checkpoints none is detectably safer than the person-blind control where both ran, and a humanoid "
     "case study shows the same profile.",
     "Where a safer verdict was attainable, none of four public DROID checkpoints is detectably safer than the person-blind "
     "control; a humanoid case study shows the same profile.")

# ---- Reproducibility Statement: episode lengths (F8), Appendix C list shortened (offset)
_rn2("seeds (42 / 7 / 123 unless stated), episode counts, the 0.30 m delivery criterion (§4.2), the speed smoothing, the T2 body "
     "model (0.16 m capsule plus head sphere, 0.10 m margin), the T6 crossing (0.06 m/s, the triggered 0.3–1.2 m/s sweep, the "
     "yielding variant: E.7), the crossing person's contact sensor and the instruments used as witnesses (repulsion shield; SSM "
     "governor with $v_h = 0$, $T_r + T_s = 0.4$ s, $C = 0.2$ m, $Z = 0.1$ m; protective stop with 0.10 m hysteresis);",
     "seeds (42 / 7 / 123 unless stated), episode counts and lengths (35 s in every tabletop pool except π0's four serving reruns on seeds 11 "
     "and 23, at 20 s, which give 0/32 of its T2 1/64, and 34 of GR00T N1.6-DROID's 43 pooled cells, at 90 s), the 0.30 m "
     "delivery criterion (§4.2), the speed smoothing, the T2 body model (0.16 m capsule plus head sphere, 0.10 m margin), the T6 "
     "crossing (E.7), the crossing person's contact sensor and the instruments used as witnesses;")
# T4 witness compressed (offset); checkpoint logging (F8)
_rn2("The physical T4 witness uses the same straight-line controller with `SC_MAGIC=0` at the dining table (five seeds), the "
     "kitchen counter (six) and the office desk (three), 112 attempts in all; every carried episode (31) enters the tilt "
     "denominator.",
     "The physical T4 witness is the straight-line controller with `SC_MAGIC=0` (14 cells, 112 attempts, all 31 carried "
     "episodes scored).")
