# Methodology Review Report (Peer Reviewer 1)

**Paper:** *Execution-Phase Safety for VLA Agents* (draft v0.45, 1755 lines)
**Reviewer:** Peer Reviewer 1 — research design, statistical validity, reproducibility
**Charge:** is the diversity and scene design sufficient to carry four dimensions x five policies?

## Scores

| Sub-score | /20 |
|---|---|
| Research design & construct validity | 13 |
| Sampling, independence, sample size | 8 |
| Analysis methods (aggregation, inference, multiplicity) | 8 |
| Results integrity & selective reporting | 13 |
| Reproducibility | 12 |
| **Total** | **54 / 100** |

**Recommendation:** Major Revision. **Confidence:** 4/5. **Statistical reporting completeness:** Needs Improvement.

## Summary

An unusually large and unusually candid empirical effort: 6159 tabletop episodes (Table IVb), Wilson intervals on every cell, feasibility witnesses, explicit "attribution-pending" marks, and a Limitations section that pre-empts several of my objections. Instruments (link recorder, contact sensor, ISO-referenced envelopes) are well specified in Appendix C.

The diversity claim does not hold as stated. I re-derived the Table III pools from `_scratch/gen_a45_numbers.py` and `_scratch/fr_summary.json`. The `canonical()` rule admits only pick-and-place plus two person-behaviour variants; everything that would supply breadth (serving, clutter, pour, drawer, handover, tool use) is excluded by rule into Table IV. Most Table III cells therefore rest on **one task**, several on **one surface and one seed**. Separately, the pooling behind the headline T3 and T6 rates violates independence in the way the paper's own mechanism predicts, and the equal-weight mean yields a structurally uninformative 50 in four of six rows. None of this contradicts the qualitative conclusion — the failures are real and large — but the *matrix*, as a benchmark artifact, is not yet defensible.

## CRITICAL

**C1. "Several tasks per dimension" is false for every cell; it is not even true for pi0.5.**
Re-deriving the pools: pi0's scored T1 is 3 cells, all `sc_kit_t1` at the kitchen counter (16/16); pi0-FAST's is 4 cells, same single surface; GR00T N1.6-DROID's is **one cell, one seed** (`sc_kit_t1_s42`, 2/2). T3 for pi0-FAST (6 cells) and GR00T-DROID (4 cells) is the dining table only. T5b and T6 for every policy but pi0.5 come from the *same* `t6_hand` cells — one task, one surface (pi0-FAST: 2 cells); GR00T-DROID's T6b is one cell with zero scored episodes. On the G1, all eight sub-types come from **one** shelf-to-bin carry in **one** corridor. So each dimension rests on one task with several *metrics*, not several tasks — and E.7's second-room result (0/31 delivered) shows the one G1 scene does not even transfer within the repo.
*Threat:* the design note says the T2 rate "is set by where the task sends the arm"; with one task per cell, each score is a property of that task choice, not of the policy.
*Fix:* restate as "several *predicates* per dimension, one canonical task", or promote >=2 exercised battery tasks per dimension into the matrix with the between-task spread. **Re-analysis only** for pi0.5 (serving, clutter, walk-past exist); **new compute** for the other three policies and any second G1 task.

**C2. Pooling T3 over sides, objects and surfaces is not statistically legitimate; the "at chance" claim does not survive clustering.**
The 14 contributing pi0.5 cells are bimodal: 0/8, 0/7, 0/5, 1/5 on one side versus 4/4, 6/6, 4/4, 5/6 on the other — exactly the mechanism §5.2 reports ("the object's pose sets it"), so episodes within a cell share a near-deterministic outcome. I estimate a design effect of **3.80** (mean cluster size 5.4, n_eff ~= 20 of 75); the iid Wilson [32, 54] becomes **[22, 65]** under a cell bootstrap. T6 likewise: 78/83, 11 cells, deff 4.33, [87,97] -> **[83,100]**. T4 is milder (deff 1.76); T2 and T5b are clean.
*Threat:* "43 %, against the 50 % chance level" is uninterpretable — the interval covers 22–65 %, and the point estimate is set by the *ratio of left- to right-side cells run*, a design-composition choice.
*Fix:* report cell-bootstrap intervals for T3, T6, T4; drop "at chance" and headline the per-bearing rates. **Re-analysis only.**

**C3. The equal-weight mean of sub-type rates is not a defensible aggregation.**
Trajectory = mean(T1, T2). T1 is saturated (100 % for all four Franka policies and the control) and T2 floored (0–1 %), so trajectory is **exactly 50 for pi0.5, pi0, pi0-FAST and the person-blind scripted control** (Table III); the delta-method interval [50, 51] is spuriously tight because the number is a ceiling/floor artifact, not an estimate. Worse for construct validity: the scripted control, blind to the person *by construction*, scores **safer** than every learned policy on orientation (30 vs 46–60) and equal on speed and force (6 vs 0–7). A score that ranks a person-blind baseline as safer than the policies it evaluates has no discriminative validity. No dimension score carries an interval anywhere in the paper.
*Fix:* stop averaging — headline the sub-type vector (Table IIIb is the better table) — or weight explicitly with a bootstrap interval, and add a "vs. blind control" delta column. **Re-analysis only.**

## MAJOR

**M4. The speed-and-force dimension is one sub-type on one task, and three of its five scores come from 9 episodes.** Table III prints a bold **0** for pi0, pi0-FAST and GR00T-DROID; each is T5b = 0/9 from the hand-reach cell alone — Wilson [0, 30], Fisher vs pi0.5's 6/83 *p* = 1.0. A bold 0 beside GR00T's 86 invites a reading the data cannot support. *Fix:* mark it underpowered or raise to n >= 40 (**new compute**, ~5 cells/policy).

**M5. Forty-two p-values, no multiplicity control.** I counted 42 reported p-values; the manuscript contains no Bonferroni, Holm, FDR or pre-registered primary comparison. Finding (ii) — "a rendered hazard pulls the path closer" — rests on Mann-Whitney *p* = 0.013 and 0.005 plus a *post-hoc* near/far-side split on pi0.5; under Holm over the paper's own 42 tests the threshold is ~0.0013 and neither survives. *Fix:* declare 3–5 primary comparisons, correct the rest, label (ii) exploratory. **Re-analysis only.**

**M6. The T2 denominator is opportunistic, and the canonical rule selects the most benign version.** pi0.5's 3/605 comprises **240** episodes from T1 off-path/offset probes, **64** from the "keep hot coffee upright" command arm, only **80** from dedicated `t2_*` cells and 61 from scissors/fork cells; the dedicated cells alone give 2/80 = 2 % [1, 9]. The rule is not uniform — the "hot" command arm is *excluded* from T4's pool but *included* in T2's. Meanwhile serving beside the person (tier *exercised*, 160 episodes) gives T2 = 19 % (30/160) and is excluded by `canonical()`. The headline T2 thus sits anywhere in 0–19 % under defensible pooling. *Fix:* pre-specify one T2 denominator, exclude ablation arms from headline pools, add a pooling-sensitivity row. **Re-analysis only.**

**M7. Capability boundaries remove the hardest scenes non-randomly (survivorship).** Lost: cordless drill 0/32 carried, pitcher 0/16, push 4/16, clear-the-table 3/16, door 0/8, drawer 0 delivered, island kitchen 6/32, G1 second room 0/31 — precisely the third hazardous object, the liquid vessel, the unheld payload and the second room that would test generalization. §8 lists them, yet the matrix is still read as a policy profile. *Fix:* state that the matrix is conditioned on performable scenes, and print attempted denominators beside every score. **Re-analysis only.**

**M8. Success-conditioning conditions on a post-treatment collider in the ablation arms.** The non-ceiling 2x2 (Table XI) has completion 29/47/61/68 % across arms while conditional rates 37/29/21/16 % are compared; §6 itself notes named-plus-visible "halves completion, p <= 0.001", so the four samples are differently selected. The T1 defence (all 41 non-completers stall before the hazard) is good and should be repeated per arm; McNemar on 19 of 265 episodes is not a substitute. *Fix:* add an always-completer/principal-stratification analysis plus an unconditional rate per arm. **Re-analysis only.**

**M9. The G1 row is not generated from logs.** `gen_a45_numbers.py` hard-codes `G1 = {...}` "typed in from the paper's Appendix A / E", while the Reproducibility Statement claims every number traces to a log in Appendix A. **15/21** (T5b) and **17/18** (T6b) appear nowhere outside Table IIIb and no appendix cell or sum reproduces them (§5.3 gives 10/13 above 110 N; E.7 gives 6/11 for the child crosser). The abstract also reports the crossing person as **15/16** where Table IIIb gives T6 = **21/24**. *Fix:* generate the G1 row from logs; publish cell -> (k, n). **Re-analysis only.**

## MINOR

**m10.** The eight-episode floor is asserted, never justified; there is no power analysis anywhere, and it applies to the *success-conditioned* denominator, so a "scored" cell can be 1–5 episodes (T3 cells average 5.4).
**m11.** No repo URL, commit hash, asset manifest, seed->placement map or `franka_safety_table` flag list; Appendix C gives thresholds but not the 51 task flags, so the scene set cannot be rebuilt from the manuscript alone.
**m12.** The Chinese abstract says 69 % for the mug tilt where the English says 77 %.
**m13.** "Six work surfaces" is oversold: only pi0.5 exceeds five, the island kitchen is a capability boundary, and scored T1/T3/T5b/T6 are single-surface for three policies.

## Fallacies detected

Survivorship bias (M7); post-treatment/collider conditioning (M8); clustering treated as iid (C2) — Appendix C addresses per-step but not cell-level dependence; uncorrected multiple comparisons (M5); an ecological-style step in C2, where a between-cell mixture is read as a single episode-level rate. No evidence of p-hacking or selective omission: null cells are reported throughout and superseded statistics are flagged.

## Questions for authors

1. What is the pre-specified rule for which cells enter a headline pool, and why does it exclude the "hot" command arm from T4 but not from T2?
2. Do the T3/T6 conclusions hold under cell-level bootstrap intervals?
3. Which comparisons are primary, and do the four findings survive correction over the 42 tests?
4. Can 15/21 and 17/18 be traced to logged cells?
