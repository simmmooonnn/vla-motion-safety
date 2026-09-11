# Peer Review Report

## Manuscript Information
- **Title**: Execution-Phase Safety for Embodied VLA Agents: A Diagnostic Benchmark for How a Safe Task Gets Done
- **Manuscript ID**: ICLR 2027 submission, `main.pdf` (31 pp.)
- **Review Date**: 2026-09-10 — **Round 3**

## Reviewer Information
- **Role**: Peer Reviewer 1 (Methodology)
- **Identity**: robot-learning evaluation researcher (LIBERO / SimplerEnv / RoboArena lineage), small-sample statistics background
- **Focus**: (1) third-party runnability of the protocol; (2) §5 vs Appendix A/C/E consistency; (3) what an ICLR benchmark still owes, and the statistical design of the §6 probe

## Overall Assessment
- **Recommendation**: Major Revision
- **Confidence**: 4

### Summary Assessment
The paper defines execution-phase safety, a six-type taxonomy, and instantiates it on GR00T N1.6/G1 (six channels) and π0.5/Franka (T1, T4). Design discipline is above the norm: success-conditioning defended with data, threshold curves, episode as unit, explicit limitations. But the spot-check finds the headline statistic mis-stated (8/8→0/8 is p = 1.6×10⁻⁴ two-sided, not "< 10⁻⁴"), Appendix A incomplete despite claiming "every cell", the 109/109 pool closing only under an unstated nesting, one π0.5 cell contradicting its prose, and a §6 probe called "powered" when it detects only a ≥75 % relative reduction. The qualitative picture survives, but a benchmark paper is judged on exactly these numbers. Fix the statistics and table, specify the protocol fully, and add feasibility witnesses before headlining attribution-pending rates.

## Strengths
- **S1 Success-conditioning is argued with data**: 41 non-completers stall at the shelf (p7 L361–362; p23 L1235–1238; Fig. 10); 25 blind + 16 hidden = 41 recomputes from Table 7 (p24 L1249–1250).
- **S2 Threshold sensitivity where it matters**: T1 radius sweep flat over [0.15, 0.80] m (p16 L858–862), π0.5 empty band (Fig. 13), full T4 curve (Fig. 9; p28 L1483–1484).
- **S3 Correct unit of analysis**: per-step pseudo-replication disclosed and corrected (p25 L1318–1321); Welch t ≈ 2.3, p ≈ 0.06 reproduces if "±" is a 95 % CI.
- **S4 Numbers that check out**: 10/10 (p23 L1208–1210); 6/12 (p7 L369; p14 L714); T4 6+0+0+2 = 8/32, 8/8 (p8 L396–399; p14 L732–739); T6 11/11, 6/11 (p8 L414–415; p14 L743–744); π0.5 22/22, 0/22, 17/32, 8/32 (p14 L728–742); all recomputed Wilson intervals and the hidden-vs-blind Fisher p = 0.031 match.

## Weaknesses

### W1 Headline p-value is wrong as stated — Major
"8/8→0/8, Fisher p < 10⁻⁴" (p6 L304–305; p7 L367; p20 L1027; p23 L1215, L1227). Exact two-sided p for [[8,0],[0,8]] is 2/C(16,8) = 1.55×10⁻⁴; only the one-sided p (7.8×10⁻⁵) is below 10⁻⁴, and sidedness is never declared (p7 L351; p17 L909). Report p = 1.6×10⁻⁴ or pre-declare one-sided tests for all shield comparisons.

### W2 Appendix A is not "every cell"; 109/109 needs an unstated nesting — Major
Table 3's caption (p14 L703) promises every GR00T cell. Its blind T1 rows sum to 118; 109 closes only if the primary electric (3/3) and stove (6/6) cells are subsets of their "3 seeds" rows while the person primary (1/1) is not a subset of its "second run" (4/4). In the text but absent from Table 3: T2 14/27 (p7 L376); T5 0/17 (p8 L405); §6 T2/T6 probe cells 33→46 %, 30→25 % (p9 L448–449); T6 shield cells 4/4, 6/7, 6/6 (p8 L419); stove x = 0.75 m control 0/12 (p7 L361; p17 L901–902); shield-margin sweep 0/28, 22/25, 0/3 (p7 L368; p23 L1222–1224); π0.5 fixed-point cell 20/22 (p28 L1469–1470); π0 3/3 (p9 L436). The powered stove shield row (p14 L719) omits its margin (E.2 implies ≥ 0.60 m). Mark nested rows, add the missing ones and a margin column, and label the pooled 97 % Wilson bound (p7 L359–360) descriptive — it pools 0.20/0.30 m radii and partly nested runs — as done for T2 (p24 L1274–1275).

### W3 The π0.5 rendered-marker cell contradicts its prose — Major
Table 3 (p14 L730): 22 attempted / 16 completing (73 %); E.8 says "task success preserved" (p28 L1472) and "success = 100 %" (p27 L1449–1450). "Fisher p = 0.50 vs unrendered" (p8 L428–429; p28 L1473) is against 20/22 (fixed-point cell), not the 22/22 the sentence implies (p = 1.0). The probe's neutral arm 14/16 (p14 L731) is a different run from the 16/16 rendered cell, with no run identifier. Reconcile and name runs.

### W4 The §6 probe is not "powered for a moderate effect" — Major
p9 L452. Exact McNemar needs ≥ 6 one-directional discordant pairs for p < 0.05 (5 gives 0.0625). At N = 24 with 8/24 baseline the command must convert ≥ 6 of 8 violators (33 % → ≤ 8 %); on π0.5 (N = 16, 15/16) it must reach ≤ 56 %. For T1/T6 the outcome is completion (p9 L450–451), so the test is silent on avoidance; 14/16 vs 15/16 is not "non-saturated" (p9 L452), and the T2 probe predicate is undefined. Report the minimal detectable effect per cell; drop "powered".

### W5 T6 "threshold-free contact" is an implicit threshold; the crosser is nearly static — Major
Contact is inferred from minima 0.26–0.31 m = "capsule radius + box half-extent" (p8 L414–415), nominal ≈ 0.26 m (p22 L1160). Box dimensions and the yaw-dependent half-extent are never given; the earlier 0.30 m label gave 10/11 (p27 L1426), so at least one "contact" is 5 cm beyond nominal. The crosser has a collider (p27 L1410–1411), so a physics contact event was available and not logged. At 0.06 m/s (p27 L1412) — 25× slower than the 1.6 m/s assumed for SSM (p25 L1332) — the channel tests a slowly appearing obstacle, not reactivity; the 6/11 stalls are mechanical blocks (p27 L1423–1425). TTC, T6's declared quantity (p5 L236–238), is never reported.

## Detailed Comments
- **Runnability gaps**: episode horizon; what varies between the 12 episodes of a single-seed cell (GR00T looks deterministic at fixed seed, p25 L1317–1318, so effective N may be far below episode counts); instruction strings; cameras; which 10 episodes form the T3a "absent" arm (p8 L384), whose "present" arm pools 5 dangerous-label + 1 benign (p25 L1322–1323).
- Appendix C (p17 L901) labels the 33 %/0.024 m cell "person at x = −0.01"; those are stove figures.
- **Claims vs evidence**: the novel cell (hazard past a person) rests on 5/5 carries with a benign box (p10 L503–504); abstract (p1 L022–025) and conclusion (p10 L527–531) do not say so. The abstract pairs π0.5 pooled contact 8/32 with GR00T worst-position 8/8 (p1 L029; p2 L060) — not commensurable until the GR00T 3-D sweep exists (p28 L1489–1491). Two policies versus 4–10 in every peer suite (p4 L166–167) is thin for "leaderboard-ready" (p28 L1501).

## Questions for Authors
1. Which Table 3 rows are subsets of others? Give the exact composition of 109.
2. What is randomized between episodes within one seed, and is GR00T inference deterministic?
3. What repulsion margin produced 0/8 on the stove, and what are the box dimensions behind the T6 contact distance?
4. Which run is the 14/16 neutral arm, and why does the rendered cell show 73 % completion?

## Minor Issues
- "Table III/IV" cited (p7 L357, L364; p18 L951); compiled tables are 6/7 (p23–24).
- Fig. 6 reads "100 % (10/8)" (p19 L982).
- "±" undefined in §5.4 (p8 L384) until Appendix C.
- Table 3's "contact (0 mm)" column means different events under axis vs surface metrics (1/32 vs 8/32).
- Two unrelated 0.30 m values (stove keep-out; delivery criterion) share one sentence (p23 L1215).

## Dimension Scores
| Dimension | Score | Descriptor |
|---|---|---|
| Originality (20 %) | 72 | Strong (R2's call) |
| Methodological Rigor (25 %) | 58 | Adequate |
| Evidence Sufficiency (25 %) | 50 | Weak |
| Argument Coherence (15 %) | 70 | Strong |
| Writing Quality (15 %) | 68 | Adequate |
| **Weighted** | **62** | **Major Revision** |

## Missing figures and experiments
**MUST — no GPU (existing logs; days)**
1. Correct p-values, declare sidedness (W1) — a checkable headline.
2. Complete Appendix A: missing rows, nesting flags, margin column (W2, W3) — an auditable pool and probe.
3. Minimal-detectable-effect line per McNemar/Fisher null (W4) — an honest "null at this power".
4. Per-episode T6 contact distance from logged yaw + box geometry (W5) — a defensible 11/11.
5. Protocol card: horizon, per-episode randomization, instruction strings, cameras, checkpoints, shield margins — runnability.

**MUST — GPU (G1 server; ~24 episodes/cell)**
6. Feasibility witnesses for T4 and T6, as §7 prescribes — the right to attribute those rates to the policy.
7. A non-ceiling T1 cell (hazard offset ~0.15–0.25 m, blind rate 30–60 %) with name/hide ablations re-run — an ablation that can move; today the prompting claim is logically inert.

**SHOULD — GPU**
8. T6 contact-event logging, ≥ 0.60 m shield re-run, realistic crossing speed (0.5–1.2 m/s) — a real reactivity test.
9. GR00T 3-D T4 at all four positions — a matched abstract comparison.
10. A third policy at full N on T1 + T4; ≥ 3 seeds for T3a and the T6 shield cells (now n = 4–7) — benchmark, not case study.

**NICE (no GPU)**
11. Leaderboard table (policy × channel: contact rate, threshold curve, completion) and a success-vs-safety scatter.
12. Seed-clustered bootstrap CIs on pooled T1 cells.
