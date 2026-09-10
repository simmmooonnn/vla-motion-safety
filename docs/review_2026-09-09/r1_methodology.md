# Peer Review Report

## Manuscript Information
- **Title**: Execution-Phase Safety for Embodied VLA Agents: A Taxonomy and a Case for Behavioral Safety Competence (v0.24)
- **Manuscript ID**: ICLR 2027 draft
- **Review Date**: 2026-09-09
- **Review Round**: Round 1

## Reviewer Information
### Reviewer Role
Peer Reviewer 1 (Methodology)
### Reviewer Identity
Robot-learning evaluation researcher (LIBERO/SimplerEnv/RoboArena lineage); small-sample inference and policy-evaluation design.
### Review Focus
Design validity (success-conditioning, matched T3a, T4 scoring, T1 ablation); small-cell statistics; reproducibility; benchmark scope.

## Overall Assessment
### Recommendation
- [x] **Major Revision**
### Confidence Score
4
### Summary Assessment
The paper proposes six execution-phase harm types and grounds them in Isaac Sim measurements of GR00T N1.6 on a G1 humanoid, replicating T1 and T4 on π0.5/Franka. Statistical hygiene is unusually good: Wilson intervals, episode-level units, a retracted pseudo-replicated result (§5.3), "no detectable effect" rather than "invariance" (§5.2). The keep-out sweeps (§5.8, §5.9) and oracle shield (§5.2) are well identified. However, the central "prompting cannot fix it" claim (§6) rests on a design that cannot move the metric: violation is saturated among completing carries, and the "powered" probe uses an unconditioned rate identical to completion, so it tests task success, not avoidance. Headline cells are n ≤ 10 (T1 person 1/1, T3a n = 6, pooled T1 10/10 without a CI), denominators change between §5 and §6, and neither T4 nor T6 shows a safe solution exists. The position deserves publication once the hypothesis has a non-ceiling, powered test.

## Strengths
### S1: Success-conditioning is argued, not assumed
§5.2 verifies excluded episodes are early non-traversals (0.3 m vs 1.9 m); §3.1/§5.5 state when *not* to condition (T4).
### S2: Geometry-sensitive, threshold-insensitive metric
Radius sweep (flat over [0.15, 0.80] m) and lateral sweep (33 % → 0/11 → 0/12) in §5.8, mirrored on π0.5 (§5.9).
### S3: Honest retraction and a metric-design finding
§5.3 retracts the per-step effect at episode level; §5.9's axis-vs-capsule scoring flips a policy ranking (3 % vs 53 %).

## Weaknesses
### W1: The promptability test is ceiling-limited even where called "powered"
**Problem**: §6's probe (N = 20–24 paired seeds; T1 33 % → 29 %, McNemar p = 1.0) uses the *unconditioned* rate, which equals completion because every completing carry violates — it tests completion, not avoidance. No power calculation defines "moderate"; 24 pairs detect roughly 33 % → ≤ 8 %.
**Why it matters**: No experiment in the paper can falsify its central hypothesis.
**Suggestion**: Site the hazard (§5.8 sweep) where blind conditioned violation ≈ 50 %; run the 2×2 naming×rendering ablation at ≥ 40 completing carries/arm (Fisher, α = .05, power .80 for 50 % → 20 %); pre-state the refuting drop.
**Severity**: Critical

### W2: Denominators change silently
**Problem**: T1 is 10/10 and T6 93 % conditioned (§5.2, §5.7); in §6 the same channels are 33 % and 30 % unconditioned; T2 is 52 % (§5.4) vs 33 %/46 % (§6). The headline 10/10 has no interval (Wilson [72, 100] %).
**Why it matters**: §6 cannot be compared to §5; "every carry" hides a 72 % lower bound.
**Suggestion**: One table of attempted/completing/violating with Wilson CIs for every cell in §5–§6.
**Severity**: Major

### W3: No feasibility oracle for T4 and T6
**Problem**: The T1 shield proves a clearing path exists. For T4 and T6 (crossing tuned "by construction" to intersect, §5.7) nothing shows a completing, non-violating trajectory exists; the live-pose shield failing 6/7 is equally consistent with an unavoidable crossing.
**Why it matters**: 75 %/93 % may describe the scene, not the policy; "needs anticipatory control" is unidentified.
**Suggestion**: A scripted reference trajectory per scene (stop-and-wait for T6; retracted reach for T4) with its completion rate.
**Severity**: Major

### W4: Sampling unit and independence under-specified
**Problem**: SD 0.006 m/s is attributed to "seed-repeatable trajectories" (§5.3); T5 reports "4/8 per seed". What a seed fixes, hence the effective n, is unstated; "paired runs" get an unpaired Welch t; ± is undefined.
**Why it matters**: If GR00T is near-deterministic per seed, CIs are too narrow; if paired, power is wasted.
**Suggestion**: Define seed vs episode; per-seed rates/ICC; paired tests where matched; Cohen's d (≈ 1.3) with CI.
**Severity**: Major

## Detailed Comments
### Methodology / Research Design
- §5.1: the `navigate_cmd` logging called "the clean test" is not run.
- §5.2: Mann-Whitney on clearances all ≤ 0.14 m compares within-mode jitter; TOST with 1–7 per cell is uninformative by construction — say so.
- §5.2 Table IV: hidden > rendered in all three hazards (20/36 vs 10/35, Fisher p ≈ .02) is a consistent perception effect on *completion* that conditioning removes; test it.
- §5.3: d₀ = 0.94 m in a 1.9 m corridor makes "6/6 violate" near-automatic; lead with "0/6 slower near than far".
- §5.9: GR00T's 3-D T4 score exists only at its worst position; π0.5's 53 % is pooled on a different task — the abstract's 25 % vs 53 % compares different metrics. Is the 3-D predicate a 0.10 m margin or contact?
- Reproducibility: missing seeds per cell, timeout, hazard/bystander coordinates, instruction strings, shield gains, π0.5 checkpoint, code/data release. Metrics are otherwise implementable.

## Questions for Authors
1. What does a seed fix, what varies within one, and is GR00T deterministic given seed?
2. In the §6 probe, how many *completing* carries per arm were non-violating?
3. For T6, does any completing, non-near-miss trajectory exist under the intersecting crossing?

## Minor Issues
- Abstract ≈ 650 words; cut to ≤ 250. Add risk differences with CIs to Fisher results.
- §5.1 promises McNemar for the shield; §5.2 uses Fisher. Table II "no SSM" vs §8 "null" for T3a — align.

## Dimension Scores
| Dimension | Score | Descriptor | Notes |
|---|---|---|---|
| Originality (20%) | 72 | Adequate | |
| Methodological Rigor (25%) | 60 | Adequate | ceiling design |
| Evidence Sufficiency (25%) | 55 | Weak | n ≤ 10 headline cells |
| Argument Coherence (15%) | 72 | Adequate | |
| Writing Quality (15%) | 68 | Adequate | |
| **Weighted Average** | **64** | **Major Revision** | |

## Missing experiments and figures
**MUST**
1. **Non-ceiling 2×2 naming×rendering ablation (T1)** at a lateral offset giving ≈ 50 % blind violation; ≥ 40 completing carries/arm (~500 episodes, ~10–15 GPU-h). Buys: the first experiment that can falsify the hypothesis.
2. **Log `navigate_cmd`** across blind/named/hidden/rendered (~2 GPU-h). Buys: command-vs-tracker attribution.
3. **Unified count table with Wilson CIs** (no compute). Buys: comparable denominators.
4. **GR00T T4 3-D re-score, all four positions** (offline or ~1 GPU-h). Buys: like-for-like cross-policy T4.
5. **Feasibility witnesses** for T4/T6 (scripted trajectories; 1–2 days). Buys: separates scene impossibility from policy defect.
6. **T1 person-proxy cell at ≥ 16 completing carries** (Wilson lower ≥ 80 %; ≈ 180 attempts, or re-site to the 6/12 hidden placement). Buys: the human headline now rests on one trajectory.

**SHOULD**
7. **Same-embodiment pair**: GR00T N1.6 Franka/DROID checkpoint vs π0.5 (server swap, ~2 days); then π0-FAST and OpenVLA-OFT on LIBERO/Franka for T1 (~1 day each); π0.5 on G1 has no checkpoint.
8. **T3a at ≥ 25 completing carries/arm** (d = 0.8, power .80), seed-paired, homogeneous labels (~4 GPU-h), plus per-seed rates/ICC/effective n (offline).
9. **Threshold-sensitivity curves** for T4 margin, T6 near-miss/TTC, T5 and T2 θ — offline. Buys: §5.8's robustness for all channels.

**NICE**
10. **Training-corpus audit** of the GN1x-Tuned-Arena demonstrations for detours/slow-downs (1 day). Buys: tests the "absent from distribution" premise.
11. **Figures**: per-cell dot plots (n, Wilson CIs) instead of bars; completion-vs-conditioned-violation scatter per policy×condition; top-down carried-path overlays per condition; π0.5 bimodal-clearance scatter.
12. **T3b** with a contact sensor.
