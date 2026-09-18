# Peer Review Report

## Manuscript Information
- **Title**: Execution-Phase Safety: Four Dimensions, Seven Sub-types, a Tabletop Family (§3–§5, §8, App. E.8 + design note + generated tables)
- **Manuscript ID**: review2 (internal)
- **Review Date**: 2026-09-17
- **Review Round**: Round 2

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 (Methodology)

### Reviewer Identity
Robot-learning evaluation methodologist (LIBERO / SimplerEnv / RoboArena lineage); benchmark construction, task validity, small-sample inference for policy evaluation.

### Review Focus
Task design and diversity design: whether each task measures its named sub-type; how capability-boundary cells are counted; how cells are pooled into the policy × dimension matrix; whether scene and geometry variation is controlled or accumulated; per-row sample sizes; the post-hoc T5c; witnesses for T2/T4.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject

### Confidence Score
4

### Summary Assessment
The manuscript defines execution-phase safety as a per-step trajectory predicate, organises it into four dimensions and seven sub-types with standards-referenced thresholds, and reports a policy × dimension matrix over a G1 corridor carry and a Franka tabletop family (13 named tasks, 6 surfaces, 6 environment maps; π0.5, π0, GR00T-DROID). The per-predicate justifications, the rotated-spawn causal test for T3, the matched present/absent design for T5a and the T2 threshold curve are sound evaluation practice. The headline matrix, however, is not yet a valid instrument. Two columns are saturated by construction (tabletop T1 is sited at each carry's midpoint; T5a is "scene-set" at 98–100 % in all 23 groups); the dimension score is an equal-weight mean over whichever sub-types a row happens to have, so π0.5 reads 43 or 99 on Speed & force by row composition alone; the headline T3 for π0.5 (100, 10/10) is the single most-violating cell while the pooled rate is 50–55 %. Capability-boundary cells (drawer 0/16 delivered, door 0/8 carried, handover 2/48 delivered) are counted as tasks and pooled into the 1370-episode rate, and the π0 / GR00T-DROID rows rest on n = 2–6 per sub-type without intervals. The findings are probably robust; the counting that presents them is not. Major revision of the aggregation and inclusion rules, not of the experiments.

---

## Strengths

### S1: Predicates justified individually, with sensitivity reported
Table II gives a reason per threshold (ISO/TS 15066 Z = 0.10 m for T2; Annex A region limits for T5b; 45° vs the 14–27° spill angle for T4); T1 is shown flat over 0.15–0.80 m with an empty 0.10–0.245 m band (E.8).

### S2: The T3 rotated-spawn design is a real causal test
Rotating the scissors 180° moves the violation from 10/10 right / 1/10 left to 5/13 / 12/15 with the person fixed (p = 0.0027, < 0.001), and the geometry battery replicates it (11/12 when the object starts beside the person).

### S3: Matched present/absent design for T5a
0.109 vs 0.113 m/s (p = 0.79) and 0.340 vs 0.367 m/s remove the trajectory confound; the authors correctly separate the scene-set envelope violation from the policy-attributable "no slowing".

### S4: Honest T2 threshold-curve correction and witness discipline
E.8 concedes 3 % → 53 % was a threshold change, reports the full curve and elevates contact (8/32 vs 9/32) to the threshold-free statement; §4.2's attribution rule ("only if the scene admits a compliant completion") is stricter than most safety benchmarks.

---

## Weaknesses

### W1: Two headline sub-types are saturated by construction and enter the score at equal weight
**Problem**: Tabletop T1 places the keep-out "per episode at the geometric midpoint of that carry — the point a direct transport must cross" (E.8); a direct carry violates by definition, so 22/22 measures directness, not avoidance. T5a is 98–100 % in every group in tables.txt because "every transport passes inside the 0.94 m stop distance (326/326; scene-set)". Both enter Table III as 100: Trajectory 50 = mean(100, 1); Speed & force 43 = mean(100, 4, 24).
**Why it matters**: A column with zero variance across policies, tasks and scenes carries no policy information; averaging it with informative sub-types yields a number that reflects neither.
**Suggestion**: Make the fixed-location rendered marker (16/16) the headline T1 and demote the midpoint version to a portability check. Report T5a as the policy-attributable quantity the text already names (present/absent speed ratio), or as the envelope rate at a calibrated placement with blind rate < 100 % (as done for the 37 % ablation). Exclude cells with ≥ 95 % and no between-condition variance from dimension means, or report dimensions as vectors.
**Severity**: Critical

### W2: The dimension score depends on which sub-types a row contains, so rows are not comparable
**Problem**: Speed & force: π0.5 43 (T5a, T5b, T5c), π0.5-serving 99 (T5a only), π0 and GR00T-DROID 50 (T5a, T5b), G1 88. Dynamics: GR00T-DROID 0 (0/2) vs π0 75 (3/4). tables.txt Table 1 aggregates differently from Table III (G1 Trajectory "88 % (147/157)" pooled counts vs "89 (T1 97, T2 81)" mean of rates) and the π0.5 sub-type values differ between the two (T2 1 vs 4, T3 100 vs 55, T4 67 vs 68, T6 63 vs 62). Wilson CIs promised in §4.2 are absent from Table III.
**Why it matters**: A leaderboard matrix with row-dependent rules invites false rankings; the §5.5 "profile recurs" claim rests on it.
**Suggestion**: One rule stated once: fixed sub-type set per dimension, cell blank (or member-listed) if any member is unscorable, CIs and n in every cell, and a minimum-n rule (n ≥ 10 scored) below which a cell prints as a count. Reconcile or delete one of the two tables.
**Severity**: Critical

### W3: Headline T3 is a selected cell, and the construct's chance level is 50 %
**Problem**: Table III/IIIb give π0.5 T3 = 100 (10/10), the scissors-right cell alone; the matched left cell is 1/10, the pooled rate 55 % (tables.txt) or 81/161 = 50 % (Table III note), and the far-edge/corner placements give 3/8, 2/8, 5/10. Under a 90° half-space predicate a person-blind grasp yields 50 % in expectation — which is the paper's own finding.
**Why it matters**: The maximum cell overstates by 2×, and a chance-level construct cannot sit on the same 0–100 scale as T1 or T6 where 0 % is attainable.
**Suggestion**: Headline T3 = pooled rate over both sides with the split in the cell, plus a person-following statistic (circular correlation of carry yaw with person bearing). State the 50 % baseline in Table II and report deviation from it.
**Severity**: Major

### W4: Capability-boundary cells are counted as tasks and pooled into rates; the conditioning event drifts
**Problem**: "put away in a drawer" (32 eps, 22 carried, 0 delivered) is scored T3 29, T4 71, T5a 100 in Table 2 although the design note calls it "a capability boundary, not a safety rate"; "close a door" (0/8 carried) is all "—" yet counted in "tasks: 13"; "hand it over" delivers 2/48 (stops 7–35 cm short) but scores T3 64 (9/14), T6 25 (6/24); "push" is mostly lifted, so its stated rationale ("travels without being held") does not apply; "clear the table" and island-kitchen deliver 1–3 of 8–48. All pool into the 1370-episode π0.5 row. The G1 conditions on completion (box within 0.30 m of bin); the tabletop conditions on "carried", contradicting §4.2 ("the denominator is completing carries").
**Why it matters**: §3.1 itself argues non-completion removes exposure; scoring orientation "at the moment nearest to them" on carries that never approach the target measures a different event, and the headline rate becomes a function of the task mix. "12/13 task types" overstates the exercised suite (about 7–8 tasks have ≥ 8 delivered episodes).
**Suggestion**: Define carried/delivered operationally and use one consistently; add an inclusion rule (≥ 8 delivered or ≥ 50 % delivered) and move drawer, door, handover, push-as-lifted and island to a capability-boundary table reporting completion only; state "N exercised of 13 defined".
**Severity**: Major

### W5: T5c is post hoc, inconsistently reported, and its construct is weak
**Problem**: T5c was "adopted 2026-09-17" after the tool cells showed a 0.52 m/s tip peak (design note item 1); §3.3 and Table II still say "six sub-types" while listing seven. The rate is 10/41 = 24 % (§5.3), "15 carried episodes" (design note), T5c 24 in the tool-use column *and* T5c 21 in the pick-and-place column of Table 2. The tools are a ladle, spatula and tongs (§5.3), whose "hazardous end" is not obviously hazardous; the design note's hammer is absent from results.
**Why it matters**: A sub-type defined after seeing the data, with a threshold matching the observed magnitude and double-counted cells, reads as HARKing until pre-specification and sensitivity are shown.
**Suggestion**: State the adoption in §3.3; fix the count; assign tool episodes to one column; report the rate over 0.15–0.50 m/s × 0.3–0.7 m; use an asset with a real edge (scissors are in the library) or rename to "tool-end speed".
**Severity**: Major

---

## Detailed Comments

### Methodology / Research Design
- Table III's "Witness in scene: yes" row is dimension-level while §8 says T2 and T4 have none and T3 only on the tabletop; make it per sub-type. T2 (81 for G1) is "attribution-pending" yet enters Trajectory at equal weight. The T3 witness is four naturally occurring compliant carries; since the safe side is "safe by geometry", these may be geometry too. A scripted upright/blade-away carry would give T3/T4 a genuine witness cheaply.
- Scene diversity is an accumulation, not a factor: environment maps vary only at the dining table (4 maps × 9–16 eps) and the packing station; surfaces carry different tasks and N (785 dining-table episodes vs 40–56 elsewhere), so the pooled π0.5 row is ~60 % one cell and no surface or map effect is tested. Run a small crossed design (2 surfaces × 3 maps × 1 task × 16 eps) or drop "6 environment maps" from the headline.
- Interaction geometry (5 placements, 2 seeds, 8–32 eps) is descriptive, without intervals; with the person across the far edge the bearing is nearly collinear with the carry, so the half-space predicate degenerates — note it.
- Policies are stochastic at fixed seed (E.8), which weakens the "paired seeds"/McNemar framing in §4.2.

### Sampling Strategy
- π0: 175 eps, 53 carried, 29 delivered; GR00T-DROID: 113 eps, 36 carried, 17 delivered; sub-type cells of n = 2–6 are printed as percentages. No precision target is stated; 0/8 has a Wilson interval of 0–37 % and should not be printed as "0 %".

### Analysis Methods
- Many uncorrected Fisher tests (effects mostly large; list the count). Add risk differences with CIs for the key contrasts (rotated spawn, shield, stop).

### Results Presentation
- Table 2's T1 appears only in the pick-and-place column although the design note lists six tasks carrying Trajectory; in practice those tasks contribute a scene-set T2 ≈ 0. Fig. ssm should show speed vs d, not a saturated rate.

### Reproducibility
- Add operational carried/delivered definitions, the T5c adoption note, the tool-episode column rule and the script that generated tables.txt.

### Methodological Fallacies Detected
- Ceiling effects entering an average (T1 midpoint, T5a); selective reporting of the maximal cell (T3 10/10); denominator drift between families; post-hoc sub-type (T5c).

---

## Questions for Authors
1. What are the operational definitions of "carried" and "delivered", and which is the denominator for T3/T4/T5a in each Table 2 cell? Why does the drawer cell (0 delivered) score T3/T4?
2. Which cell produces π0.5 T3 = 100 (10/10) in Table III, and why is it the headline rather than the pooled 81/161?
3. Why does T5c appear in both the pick-and-place (21) and tool-use (24) columns, and how do 10/41 and "15 carried episodes" relate?
4. With midpoint-T1 and scene-set T5a removed from the means, what are the Table III scores, and does the §5.5 cross-policy profile survive?

---

## Minor Issues

### Language / Grammar
- "Six sub-types" (§3.3 heading, Table II caption) vs seven listed; Table IIIb lacks a T5c column.
- E.8 T3 paragraph: missing spaces before "Spawned at 90°" and after "As on the G1".

### Figures and Tables
- Table III: add Wilson CIs and n per cell; mark saturated and attribution-pending cells.
- tables.txt Table 2: "tasks: 13" with an all-"—" door column; label exercised vs defined.

### Layout
- The interaction-geometry block is duplicated between the design note and E.8; keep one.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 72 | Adequate–Strong | Execution-phase framing with standards-linked predicates is a clear contribution; tabletop family is an extension |
| Methodological Rigor (25%) | 55 | Weak | Sound per-predicate design undermined by saturated columns, row-dependent means, denominator drift, post-hoc T5c |
| Evidence Sufficiency (25%) | 58 | Weak–Adequate | π0.5 well sampled (1370 eps); π0 / GR00T-DROID at n = 2–6; no CIs in the headline |
| Argument Coherence (15%) | 62 | Adequate | Narrative consistent; the tables that carry it are not (Table 1 vs III; task count) |
| Writing Quality (15%) | 70 | Adequate | Dense but precise; counting inconsistencies, duplicated blocks |
| **Weighted Average** | **62** | **Major Revision** | |
