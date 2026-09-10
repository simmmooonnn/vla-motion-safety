# Editorial Decision — "Execution-Phase Safety for Embodied VLA Agents" (draft v0.24, ICLR 2027 target)

Review date 2026-09-09 · Mode: full (EIC + R1 methodology + R2 domain + R3 safety-engineering + Devil's Advocate) plus a peer-paper figure/experiment survey. Every point below traces to a report in this folder (`r0_eic.md`, `r1_methodology.md`, `r2_domain.md`, `r3_perspective.md`, `r4_devils_advocate.md`, `peer_figures_experiments.md`).

## Decision: MAJOR REVISION

Weighted scores: EIC 61 · R1 64 · R2 64 · R3 65 — unanimous Major Revision. The Devil's Advocate raised three CRITICAL issues (C1–C3), so Accept is excluded by rule. All five reviewers judge the phenomena real and the reporting honest (EIC S4, R1 S1–S3, R2 S1–S4, R3 S1–S3, DA "what survives"); the revision is about evidence placement, denominators, one unmeasured headline cell, and framing.

## Consensus (raised independently by ≥3 reviewers)

| # | Issue | Raised by | Severity |
|---|---|---|---|
| K1 | The headline "carried hazard past a passive bystander" cell has n = 1 completing carry (Table III); T2/T5/T6 carry a benign box | DA C2, R2 W1, R1 MUST-6, EIC MUST-5 | Critical |
| K2 | T4 cross-policy comparison is metric-unmatched: π0.5 scored on a 0.16 m capsule, GR00T's 25 % on a 0.10 m axis; GR00T never re-scored in 3-D at all four positions | DA C3, R1 MUST-4, EIC MUST-6, R3 SHOULD-7 | Critical |
| K3 | Table IV shows hidden > blind completion in all three hazards (20/36 vs 10/35, Fisher p ≈ 0.02): a perception effect on *completion* that success-conditioning removes, then "no detectable change" is claimed | DA C1, R1 detailed §5.2 | Critical |
| K4 | The promptability test cannot move its metric (violation saturated among completing carries; §6's "powered" rate equals completion) → the central hypothesis is untested | R1 W1 (Critical), DA M1, EIC W5 | Critical |
| K5 | No feasibility witness that a completing, non-violating trajectory exists for T4/T6 → rates may describe the scene, not the policy | R1 W3, DA alt-2, R3 §5.7 comment | Major |
| K6 | T6 "reactive cannot fix it" tests one repulsion design; the ISO-canonical reactive response (protective stop / SSM governor) is untested | R2 W5, R3 §5.7 + SHOULD-5, R1 W3 | Major |
| K7 | Denominators switch silently between §5 (conditioned) and §6 (unconditioned); headline 10/10 has Wilson lower bound 72 % | R1 W2, EIC W3 | Major |
| K8 | Standards: ISO/TS 15066:2016 withdrawn into ISO 10218-2:2025; ISO 13482 named but uncited; SSM parameters (T_r+T_s = 0.4 s, C = 0.2 m) asserted, not measured for a biped | R2 W3, R3 W3 | Major |
| K9 | Identity/length: position-vs-benchmark unresolved (ICLR has no position track); ~12k words vs 10 pages; ~700-word abstract | EIC W1/W4, R1 minor, R2 minor, DA obs | Major |
| K10 | No overview Figure 1 / pipeline figure / success-vs-safety plot — present in 5–6 of 6 peer benchmarks | Survey §"common denominators", EIC MUST-1, R2 MUST-1/4, R1 NICE-11 | Major |
| K11 | Missing literature: VLA safety-filter cluster (VLSA [22] uncited; CBF filters; SPARK on G1), classical HRI safety, handover-orientation lineage, Habitat 3.0 human-collision metric; [32]–[34] placeholders | R2 W4/W5, DA (VLSA) | Major |

## Disagreements and arbitration

1. **Third policy vs same-embodiment pair.** EIC/R2 want a different-architecture policy (OpenVLA-OFT) for a ≥3-policy leaderboard; R1 says the like-for-like fix (GR00T Franka/DROID checkpoint vs π0.5 on the same arm) matters more than count; the survey shows 4/6 peers have ≥6 policies. *Arbitration:* do the same-embodiment pair first (removes the embodiment confound R1 and DA flag), then OpenVLA-OFT; do not chase 6+ policies for this paper.
2. **What the policy should "own".** R3 (Critical W1) says a certifier will dismiss "the policy implements no SSM"; DA says the competence hypothesis is unfalsifiable. Both converge on the same rewrite: the external layer is non-negotiable; policy behavior sets its *demand rate*, and geometric stops cannot cover T2/T5/T6. *Arbitration:* adopt R3's reframing in §1/§6 and title; it also answers DA's "so what".
3. **Position or benchmark.** EIC: benchmark with release. Survey: ICML position papers frame evidence as motivating analysis and carry "Alternative Views". *Arbitration:* diagnostic-benchmark identity (release code/configs/logs), keep one hypothesis section written with an explicit Alternative Views paragraph.
4. **Real robot.** All reviewers rank it NICE; survey: 2/6 peers, one a single demo. Not required.

## Revision Roadmap

### A. Offline / no GPU (do first)
- A1 Unified count table: attempted / completing / violating + Wilson CI for every cell in §5–§6 (K7).
- A2 Un-condition T1: all 35 episodes, displacement vs hazard visibility, freeze/abort classification; test hidden-vs-blind completion (K3).
- A3 Re-score GR00T T4 on the identical 0.16 m capsule at the positions already logged (K2, partial).
- A4 Threshold-sensitivity curves for T4 margin, T6 TTC/near-miss, T2 θ, T5 tilt (R1 SHOULD-9, R3 SHOULD-7).
- A5 SSM envelope figure: v_allow(d) nominal/lenient over the six speed-vs-separation traces + 250 mm/s line (R3 MUST-3, R2 SHOULD-9).
- A6 Success-vs-safety scatter, one point per policy × channel × condition (K10).
- A7 Figure 1 overview (three axes + six types + tuple + top-down scene), pipeline figure, top-down trajectory overlays blind/named/rendered/shielded (K10).
- A8 Standards-mapping table T1–T6 ↔ ISO 12100 / 10218-2:2025 / 13482, SSM-only vs PFL-eligible; taxonomy crosswalk vs ForesightSafety / SafeVLA-Bench / ISO 13482 (R3 MUST-4, R2 MUST-2).
- A9 Bibliography: ISO 10218-1/2:2025, ISO 13482:2014, cite VLSA [22], real authors for [32]–[34], HRI classics, VLA-CBF cluster, Habitat 3.0 (K11).
- A10 Restructure: ≤250-word abstract, 10-page main text, §5 in T1→T6 order, headline the N = 24 fire shield / N = 22 π0.5 / paired promptability runs, R3's demand-rate reframing in §1/§6, Alternative Views paragraph (K9, arbitration 2–3).

### B. GPU (when chaowei is back)
- B1 T1 person-proxy cell to ≥ 16–20 completing carries with a hazard-class payload (K1). ~8 GPU-h.
- B2 Non-ceiling 2×2 naming × rendering ablation at a lateral offset with ≈ 50 % blind violation, ≥ 40 completing carries per arm (K4). ~10–15 GPU-h.
- B3 Language-following control: neutral spatial instruction on the same checkpoint (DA MUST-1). ~1 GPU-day.
- B4 GR00T T4 3-D sweep at all four positions (K2). ~2 GPU-h.
- B5 G1 stop-time / stop-distance test under its WBC; recompute d_0, v_allow (K8). Hours.
- B6 Feasibility witnesses: scripted stop-and-wait (T6) and retracted reach (T4) with completion rates (K5). 1–2 days.
- B7 Protective-stop / SSM-governor reference layer on T1-person, T3a, T6; report violation and completion vs d_0 (K6). Days. (Run before, or instead of, the staged anticipatory shield.)
- B8 Log `navigate_cmd` across conditions; hazard-free completion baseline (R1 MUST-2, EIC MUST-7). ~3 GPU-h.
- B9 Same-embodiment pair (GR00T Franka/DROID vs π0.5), then OpenVLA-OFT on T1/T4, N ≥ 24 (arbitration 1). 2–3 GPU-days each.
- B10 SHOULD: fine-tune on a few hundred detour demonstrations and re-measure T1 — the most direct test of §6 (EIC SHOULD-9). 20–40 GPU-h.
- B11 NICE: human-model variants (child / seated / reaching), T6 crossing-speed sweep, real hazardous-axis objects for T2, hardware replay.

### C. Figures to add (merged)
Fig. 1 overview · pipeline/scene-construction · taxonomy as a diagram · six-type scenario gallery · top-down trajectory overlays · success-vs-safety scatter · SSM envelope vs measured profile · T2 polar plot · per-cell dot plots with Wilson CIs replacing bars · T4 axis-vs-capsule, both policies × both metrics.
