## Devil's Advocate Re-Review — v0.26 ("A Diagnostic Benchmark for How a Safe Task Gets Done")

**Credit.** The T4 retraction, un-conditioned T1 view, T6 threshold band, shield margin dependence and Appendix A are real, costly concessions.

### Disposition of my first-round findings

| # | Status | Rebuttal log |
|---|---|---|
| C1 freeze-as-reaction | **Downgraded → MAJOR** | [4/5] New evidence: all 37 non-completers stall at the shelf. Core survives, relocated (M2). |
| C2 person cell n=1 | **Maintained CRITICAL** | [2/5] Deferred to GPU (B1); n=5 after a second run, payload still a benign box. |
| C3 T4 threshold | **Withdrawn** | [5/5] Curves, contact counts, reading retracted. |
| M1 language control | Maintained | [2/5] B3 pending; the command perturbs π0.5's success (§6), no spatial-following test. |
| M2 navigate_cmd | Maintained | [2/5] B8 pending. |
| M3 T3a/T5 by construction | Maintained for T3a | [2/5] T5 relabelled "discrimination" — accepted; T3a still has no witness. |
| M4 so-what | Re-targeted | [3/5] Answered by "demand rate" — see M1 below. |
| m1 / m2 | Maintained / partly fixed | Null-vs-defect labelling persists (m1 below). |
| m3 electric shield | Withdrawn | [5/5] Now reported: 6/12 violate at 0.50 m. |

Concession rate 30 %.

### Strongest Counter-Argument

The revision swaps "the policy should own safety" for "the policy sets the demand rate on a certified layer" (§1). It is unmeasured: no protective stop (B7), no G1 stop distance (B5), the "fall hazard" asserted. And §1 says a geometric stop "cannot supply" T6 while Table VI states the standard's prescribed response to a moving person *is* a protective stop. The new thesis is untested and self-contradicted.

What is the policy shown to own? By the authors' admissions T4's rate is set by scoring geometry (§5.8), T6's count by the 0.30 m label (§5.7), and §6(iii) refuses to attribute either to the policy until a feasibility witness exists. T3a is the same case unnamed: with d₀ = 0.94 m in a 1.9 m corridor, 6/6 violate because *any* traversal violates (§5.4). What remains is T1 — straight carries through an on-path point on two policies, unpromptable — and T2's frozen yaw: "imitation policies replay the demonstrated path." The claimed novel cell — a *hazardous* payload past a *person* — is still a relabelled box ("blade", "cup") plus five person-cell carries that look exactly like the stove's. The person adds a noun, not a phenomenon.

And the one cell where GR00T behaves *differently* with a person — completion 1/11 vs 6/12 absent (Table IV) — is dismissed as "visual clutter" (§5.2). Under the paper's own frame a policy that will not proceed past a person has demand rate zero; success-conditioning discards that outcome and scores the rare completer 100 %.

### Issue List

#### CRITICAL
| # | Dimension | Issue | Location | Field-norm | Rationale |
|---|---|---|---|---|---|
| C1 | Logic-chain break | §6(iii) withdraws policy attribution for T4/T6 pending a witness; the abstract, Table II ("demonstrated (defect)") and §8's last sentence keep both as demonstrated defects. Three of five measured "defects" (T3a, T4, T6) are conceded scene- or threshold-set. | Abstract; Table II; §5.4; §5.7; §5.8; §6; §8 | — | — |
| C2 | Foundation | Unique cell unmeasured: no scene carries a hazardous object; person-cell T1 is n=5 with a benign box; 100 % is identical across strip/stove/person — "human-referenced" is a label. | §2(ii); Tables III, V | — | — |

#### MAJOR
| # | Dimension | Issue | Location | Field-norm | Rationale |
|---|---|---|---|---|---|
| M1 | Evidence gap | "Demand rate" unmeasured (no stop layer, no stop distance, fall hazard asserted); §1 "stop cannot supply T6" contradicts Table VI. | §1; §7; Appendix D | — | — |
| M2 | Data–conclusion | Perception *does* move behaviour (hidden 20/36 vs blind 10/35, p=0.03). §3.2's by-elimination logic assumes it does not; §1 item 3 and §2 still say "no detectable change"; the promised abstract sentence (A2) is absent. | §1; §2; §3.2; §5.2; Table IV | — | — |
| M3 | Logic | T6 "needs anticipation" rests on 6/7 near-misses under a live-pose shield whose margin and minima are unreported, while §5.2 shows repulsion clears only at ≈2× keep-out — a margin artefact, not a reactive/anticipatory distinction. | §5.7; §5.2; Appendix B T6 | — | — |
| M4 | Cherry-pick + consistency | Abstract headlines the best shield cell (8/8→0/10); electric 6/12 and person 2/10 still violate (electric clears only at n=3). Table V says 0/8, 33 %; §5.2 says 0/10, 42 %. | Abstract; §5.2; Table V | — | — |
| M5 | Cherry-pick | T3a: a stationary proxy scored with v_h=1.6 m/s; no witness; 6/6 is a property of the corridor. | §5.4; §6(iii) | — | — |
| M6 | Overclaim | "Scenes… are released" (present tense), "leaderboard-ready": no URL, licence or version; one task family; two policies; canonical thresholds deferred. | Abstract; §5.8; §7 | NeurIPS Datasets & Benchmarks track requires an accessible URL and licence | "Benchmark" is in the title with no artefact |

#### MINOR
| # | Dimension | Issue | Location |
|---|---|---|---|
| m1 | Consistency | T3a is a "standards-grounded defect" (§1, §4, Table II) and a "de-confounded null" (§8 closing). | §1; §4; §8 |
| m2 | Consistency | §1 "25–100 % of completing episodes" — T4 is all-episode; abstract pairs π0.5 pooled contact (8/32) with GR00T's worst position (8/8). | §1; Abstract; §5.5 |
| m3 | Metric | Body model omits legs, uses link origins; "contact unlikely" elsewhere conflicts with axis minima 0.07–0.18 m inside a 0.16 m radius. | §5.5; §5.8 |
| m4 | Cross-refs | Appendix B T2 → "§5.4" (should be §5.3); T3 → "§5.3" (should be §5.4); §5.6 "(§4)" now Appendix B; Chinese abstract stale. | Appendix B; §5.6 |
| m5 | Overgeneralization | "First on a locomoting humanoid" vs Safety-CHORES [21]. | §2 |

### Ignored Alternative Explanations
1. **OOD collapse, not clutter.** A person suppresses the grasp far more than a stove; the fine-tune saw no humans — and by the standard, stalling is safe.
2. **T6 shield failure is a margin artefact** (M3).
3. **Replay.** Straight paths on both policies may be open-loop replay (B8 untested).
4. **T4 contact is a body-model choice** — capsule radius, no legs, origins not meshes.

### Missing Stakeholder Perspectives
- Certifiers: named; their quantities (stop performance, stopping distance) absent.
- Training-data curators: the corpus hypothesis (§2) is never inspected; B10 tests it.
- Benchmark users: nothing to download.

### Unexamined Premise
That unshielded violation rates predict demand on a safety layer; a stop alters what the policy observes next, so demand must be measured with the layer in place. The frames also collide: success-conditioning discards the stall demand-rate would count as best.

### Observations (Non-Defects)
- Survives: the paired promptability null on two policies (§6); T2 yaw invariance (§5.3); the threshold-curve/contact lesson (§5.8); margin-dependence reporting (§5.2); Appendices A, D.
- The honest paper: "imitation-trained VLAs replay the demonstrated path and cannot be prompted out of it; here is how to score that."

### What would now change my mind
**MUST**
1. *Protective-stop layer + demand rate* (B7): completion and stop-fire count per channel. Buys the thesis. ~1 GPU-day.
2. *Feasibility witnesses for T3a/T4/T6* (B6): scripted violation-free paths. Buys attribution; without it C1 stands. ~1 day, no policy server.
3. *Hazardous-payload-past-person cell, N ≥ 20*, rendered knife/cup (B1). Buys C2. 1–2 GPU-days.

**SHOULD**
4. Re-run the T6 shield at ≥0.60 m margin; report minima (M3). Hours.
5. No GPU: reconcile abstract/Table V shield counts; relabel T4/T6 "attribution pending"; add the A2 sentence; state the T6 shield margin; fix cross-refs.
6. Language-following control (B3); `navigate_cmd` logs (B8).

**NICE**
7. Fine-tune on detour demonstrations (B10) — the one test that can falsify the training-distribution hypothesis.
8. Public repository, licence, versioned thresholds — before "benchmark" stays in the title.
