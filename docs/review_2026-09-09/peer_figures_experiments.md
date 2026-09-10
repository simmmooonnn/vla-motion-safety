# Peer papers: figures, tables, experiments (survey 2026-09-09)

Legend: [V] read from arXiv HTML/PDF; [U] inferred/memory. "cell" = one policy×condition.

## 1. LIBERO-Safety (2606.23686) — ECCV 2026 [V, GitHub tag]; 14 pp main (LNCS), 42 total [V]
Outline: Intro / RelWork / Benchmark (parametric env, taxonomy, keypose data pipeline) / Experiments (main, generalization+safety, failure cases) / Concl.
Figs 6 main + 8 app [V]: F1 teaser 3-panel "(a) VLA Safety Challenges … (b) Data Generation Pipeline … (c) Cross-Paradigm Assessment"; F2 overview env + "Hierarchical Safety Taxonomy" + data-gen pipeline; F3 state-space coverage vs LIBERO; F4 qualitative avoidance trajectories; F5 failure gallery "Task Incompletions"; F6 qualitative "Semantic Misalignment"; A.2–A.6 per-suite task galleries; A.7 sparkline leaderboard; A.8 real-robot 4-frame strip.
Tables 6 + 12 app [V]: T1 comparison vs 10 benchmarks × 7 axes; T2 pipeline vs teleop; T3 leaderboard 8 VLAs × 4 suites × 3 levels, mean±SD over 3 seeds; T4 semantic track (2 reasoning models, refusal rate); T5 data-scaling ablation; T6 robustness over 7 perturbation axes; A.10–A.12 extra baselines/scaling.
Experiments [V]: 10 policies (OpenVLA, OpenVLA-OFT, π0, π0.5, UniVLA, VLA-JEPA, GR00T N1.5/N1.6, RoboBrain2.0-7B, RynnBrain-CoP); 75 tasks, 7,603 scenes; 10 trials × 3 seeds = 30/cell; mean±SD, no CI/tests; ablations: data scaling, perturbations, obstacle-free generalization; no prompting ablation; no human study; real robot = ONE qualitative π0 case (bowl past fragile bottle) with vs without chunk-level CBF, no counts (App. D, Fig A.8); success–safety: "joint improvement" claim, no coefficient; mitigation = chunk-level CBF, real demo only.

## 2. SafeVLA-Bench (2606.00773) — arXiv May 2026, no venue [V]; ~9 pp main, ~40 total [V≈]
Outline: Intro / RelWork / Bench (STL spec library, per-task applicability, SBU/VSI metrics) / Results / Discussion+Limitations / App A–E.
Figs 2 main + 1 app [V]: F1 overview "task-aware STL safety specifications, per-task applicability, and SBU/VSI metrics"; F2 success-vs-safety scatter "each marker is a LIBERO model–suite cell … bars show Wilson 95% CIs" + Pareto frontier; F3 (app) "Successful rollouts can still be physically unsafe" 3-frame rows.
Tables 22 [V]: T1 comparison vs 3 benchmarks × 6 axes; T2 8 constraint families; T4 LIBERO leaderboard 5 policies × 4 suites (SR/Safety/SBU/VSI), n=200/cell; T5 RoboCasa-365 4 policies, n=900; T7–8 per-constraint violation rates; T9 threshold sensitivity; T12 per-task Wilson CIs; rest spec/registry.
Experiments [V]: 9 checkpoints (OpenVLA-7B, Cosmos-Policy-2B, GR00T-N1.7, π0.5, π-RL-130; π0, π0.5, GR00T-N1.5, RLDX-1-FT); Wilson 95% CIs + 10k bootstrap, no tests; ablation = threshold sensitivity; no prompt/perception ablation, human study, real robot, or mitigation; success–safety: scatter + rank-mismatch narrative.

## 3. SafeVLA / Safety-CHORES (2503.03480) — NeurIPS 2025 Spotlight [V]; main ~10 pp [U]
Outline: Intro / RelWork / Problem / ISA implementation / Experiments / Concl.
Figs 10 [V]: F1 ISA pipeline; F2 taxonomy "Conceptual diagrams of each safety critical component" + photorealistic renders (5 hazards); F3 cumulative-cost distributions; F4–5 method-vs-baseline bars; F6–7 ablation panels; F8 sim-to-real setup photo (dual Realman RM75); F9 logistic regression; F10 per-room improvements.
Tables [V]: T1 leaderboard ~8 methods × 3 tasks (SR, CC); T2 OOD perturbations; T3 logistic regression; app hyperparams.
Experiments [V]: ISA vs FLaRe, FLaRe-RS, SPOC×3, SPOC-GT, Poliformer; 3 tasks, 150K ProcTHOR scenes, 5 hazard types; episode count not stated; stats: logistic regression, Pearson (p<0.01), t-tests; ablations: risk elicitation, backbone, Lagrangian vs fixed, threshold; real robot sim-to-real on Safety-PickUp; correlation: FLaRe SR–cost negative, ISA decoupled; mitigation = CMDP method + reward-shaping baseline; no human study.

## 4. SafeManip (2605.12386) — arXiv Jun 2026 [V]; ~10 pp [V≈]
Outline: Intro / RelWork / Temporal safety properties (LTLf, 8 categories) / Protocol / Results RQ1–3 / Discussion / Concl.
Figs 5 [V]: F1 teaser-pipeline "grounds task-relevant predicates, instantiates reusable LTLf safety properties, and monitors rollouts"; F2a success-vs-violation scatter; F2b outcome decomposition (safe/unsafe × success/fail); F3 per-category violation/exposure bars; F4 horizon effect; F5 per-suite effect.
Tables 3 [V]: T1 comparison vs 9 benchmarks; T2 10 LTLf templates; T3 6 checkpoints.
Experiments [V]: 6 policies (π0, π0.5, GR00T N1.5 + 3 GR00T training variants); 50 RoboCasa365 tasks × 50 rollouts = 15k; NO CI/SD/tests; seeds not stated; prompting mitigation (exploratory §6): regular/short-conservative/long-constraint → SR 43.9/26.4/6.9 %, violation 71.8/69.4/65.1 %; RQ1: success gains ≠ safety gains; no human, no real robot.

## 5. ForesightSafety-VLA (2606.27079) — arXiv Jun 2026 [V]; ~10 pp IEEE [V≈]
Outline: Intro / RelWork / Design (taxonomy, scenarios, diagnostic dims) / Evaluation (dual-threshold, joint outcomes, exposure) / Experiments / Discussion.
Figs 5 [V]: F1 overview = taxonomy (Safe-Core/Lang/Vis) + 3 diagnostic dimensions; F2 conceptual "Anticipatory safety comparison" of two trajectories; F3 "Global safety–success landscape" bubble scatter (SSR vs CC, bubble=USR); F4 degradation curves vs severity; F5 keyframes + time-aligned channel safety scores.
Tables 4 [V]: T1 13-category taxonomy; T2 leaderboard 4 policies × 6 metrics; T3 per-suite (2 policies × 5 suites); T4 one-episode channel exposure.
Experiments [V]: 4 completed (OpenVLA-oft, RDT, DP, ACT) + ≤7 partial in scatter (π0.5, π0, DexVLA, LLaVA-VLA, TinyVLA, DP3); 66 RoboTwin scenarios, 5 embodiments; 50 episodes over 3 seeds per cell; means only; no ablation, human study, real robot, or mitigation; correlation qualitative ("stronger baselines are safer").

## 6. HazardArena (2604.12447) — arXiv Apr 2026 [V]; ~9 pp + App A–F [V≈]
Outline: Intro / RelWork / HazardArena (construction, stage-wise metrics) / Experiments (safe-only FT, stage-wise, SOL defense) / Concl.
Figs 5 [V]: F1 teaser "capability does not imply safety"; F2 overview risk taxonomy + "seed-matched safe/unsafe twins" pipeline; F3 twin frame strips with stage events; F4 4-panel stage-wise event-rate bars; F5 2-panel SOL effect bars.
Tables 9 [V]: T1 SR_safe/SR_unsafe, 4 backbones × early/final × 6 tasks; T2 attempt/commit/success; T3 comparison vs ~11 benchmarks × 7 features; T4 hyperparams; T5 commit predicates; T6–7 SOL rules/judge outputs; T8 inventory by 7 risk families; T9 ~30 tasks.
Experiments [V]: 4 VLAs (OpenVLA-OFT, VLA-Adapter, NORA, π0); 6 tasks, 7 families; 100 eps/task/round × 3 seeds = 300; proportions only, no CI/tests; ablations: early vs final ckpt, stage-wise vs endpoint, SOL-L1 vs L2; mitigation = SOL (rules; Qwen3-VL-32B judge); correlation: capability↑ ⇒ unsafe execution↑ (table, no scatter); no human, no real robot.

## 7. LIBERO (2306.03310) — NeurIPS 2023 D&B [U]; ~20 pp arXiv [V≈]
Figs [V]: F1 teaser 4-suite task montage; F2 procedural-generation pipeline; F3 metric diagram; F4 ordering-robustness bars with error bars; F5 algorithm×architecture bars; F6–7 architecture diagrams; F8–11 per-suite galleries; F12–20 app plots. Tables [V]: T1–3 FWT/NBT/AUC ± SE; T4 summary; T5–8 hyperparams/full grid.
Experiments [V]: 3 archs × 5 algos × 4 suites × 3 seeds = 180 runs; 20 rollouts/checkpoint; mean ± SE, two-tailed t-test; ablations: language embedding, ordering, pretraining; no human, no real robot.

## 8. RoboArena (2506.18123) — CoRL 2025 [V]; ~11 pp [V≈]
Figs 11 [V]: F1 teaser distributed pairwise-eval framework; F2 VLM categorization pipeline; F3 DROID hardware photo; F4 system architecture; F5 scene montage + oracle ranking; F6 ranking-correlation bars vs Elo/BT/PROG; F7 convergence vs #episodes; F8–9 VLM/LLM validation; F10 task diversity; F11 32-environment collage. Tables [V]: T1 EM hyperparams; T2 distribution-shift robustness (Pearson r, MMRV).
Experiments [V]: 7 policies (π0-flow/FAST-DROID, PG-{flow,FAST,FAST+,FSQ,Bin}-DROID); 7 institutions; 4,284 rollouts; Pearson r + MMRV, no CI/tests; ablations: ranking method, convergence, shift; 100 % real robot; humans as raters only.

## Position papers (ICML "Position:" track)
- **P1 Jordan et al., "Benchmarking is Limited in RL Research", ICML 2024** [venue U; content V]. ~10 pp; 5 main figs (CI width vs seeds; coverage vs N; overlapping-CI counts; four-rooms curves) + 9 app; T1 survey of 144 NeurIPS'22 papers. Empirical: ~334k runs/algo-env for ground-truth distributions, then bootstrap-coverage simulation + small exploration case study; framed as "quantifying the computational burden" and "demonstrating the alternative paradigm". Finding: ≥100 seeds for valid coverage.
- **P2 Tian, Wu, Bajcsy, "Good Embodied Reward Models Need Bad Behavior Data", ICML 2026** [V, icml.cc]. ~8–9 pp; 5 figs (task-category teaser with real-robot stills; qualitative reward-vs-failure frames; ordering-accuracy bars; in-context-negatives bars; qualitative); 0 tables. Empirical: 3 reward models (ReWind, GVL/GPT-5, Dopamine-8B) on 723 RoboArena real-robot tasks with human preferences; point estimates, no CIs. Framing: §3 "diagnostic/motivating analysis", §4 "controlled experiment"; "Alternative Views" + "Call to Action".
- **P3 Bowyer et al., "Don't use the CLT in LLM evals with fewer than a few hundred datapoints", ICML 2025** [venue keyword V; year U]. ~11 pp; 6 figs (1 real case, LangChain N=20; 5 simulation coverage plots); T1 method-property matrix. Empirical: 80k simulated datasets at N∈{3,10,30,100}; real: LangChain (N=20, 8 models), AIME (N=15). Framing: theory → simulation → real-world validation; "Alternative Views". Recommends Wilson or Bayesian Beta-Bernoulli intervals at small N — directly applicable to our 6–35-episode cells.
- **P4 "Foundation Models Need Digital Twin Representations" (2505.03798)** [content V; venue U]: 1 conceptual figure, 0 tables, no experiments — the pure-argument extreme.

## Cross-paper matrix (LS SVB SV SM FS HA | LIB RA)

| Type | LS | SVB | SV | SM | FS | HA | LIB | RA |
|---|---|---|---|---|---|---|---|---|
| Teaser/overview Fig 1 | ✓ | ✓ | ✓(pipeline) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Taxonomy as a FIGURE | ✓ | ✗(table) | ✓ | ✗(table) | ✓ | ✓ | ✗ | ✗ |
| Pipeline/env-construction figure | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ |
| Comparison-to-prior-benchmarks table | ✓ | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ | ✗ |
| Leaderboard ≥6 policies | ✓10 | ✓9 | ✓~8 | ✓6 | ✗4(+7 partial) | ✗4 | ✓15 | ✓7 |
| Per-category breakdown (radar: none) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ? |
| Success-vs-safety scatter/correlation | ✗ | ✓ | ✓(stat) | ✓ | ✓ | ~(table) | n/a | n/a |
| Qualitative failure gallery | ✓ | ✓(app) | ? | ✗ | ✓ | ✓ | ✗ | ✗ |
| Prompting ablation | ✗ | ✗ | ✗ | ✓ | ~(lang. perturb.) | ✗ | ✗ | ✗ |
| Mitigation baseline | ✓(CBF, real only) | ✗ | ✓(method) | ✓(prompts) | ✗ | ✓(SOL) | n/a | n/a |
| Human study | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ~(raters) |
| Real robot | ~(1 qual. demo) | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Sim-to-real claim | ~ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | n/a |
| CI / stat tests | SD only | Wilson CI | tests | ✗ | ✗ | ✗ | SE + t-test | ✗ |
| Seeds ≥3 | ✓ | ✗(fixed) | ? | ? | ✓ | ✓ | ✓ | n/a |
| Episodes per cell | 30 | 200 | ? | 50 | 50 | 100–300 | 20×3 | 4,284 total |

## Common denominators we lack (≥4 of 6 safety benchmarks), ranked
1. **Teaser/overview Fig 1** — 6/6. We have none.
2. **Per-category breakdown across ALL taxonomy types** — 6/6. We have it for T1 only.
3. **≥50 episodes per cell** — 5/6 (SVB 200, HA 100–300, SM/FS 50; LS 30). Ours 6–35.
4. **Pipeline / environment-construction figure** — 5/6. None.
5. **Joint success–safety analysis (scatter or correlation)** — 5/6. None, though our clearance–success confound makes it the natural figure.
6. **Leaderboard ≥6 policies** — 4/6. Ours 2 (+1 preliminary).
7. **Taxonomy as a diagram** — 4/6.
Already covered: comparison-to-prior table (4/6), mitigation baseline (4/6, our shield), qualitative failure frames (4/6).
Not common, so not a gap: radar (0/8), human study (0/6), real robot (2/6, one a single demo), significance tests (1/6), CIs (2/6 — but P3 argues Wilson/Bayes intervals are mandatory at our n).

## Position papers: pattern
1–6 figures (median 5); 3 of 4 carry experiments; none has a leaderboard. The empirical part is framed as "diagnostic/motivating analysis" (P2), "quantifying the burden + demonstrating the alternative" (P1) or "simulation + real-world validation" (P3) — never as a benchmark result. All three ICML papers end with an explicit "Alternative Views" section and a call to action [V]; P2 reuses an existing real-robot dataset rather than collecting new data. Scope is small (3 models / 8 models / 2 case studies) but each figure is a visual proof of one claim in the position — the register our GR00T/π0.5 evidence should adopt.
