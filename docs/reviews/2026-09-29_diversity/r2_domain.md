# Domain Review Report (Peer Reviewer 2)

**Manuscript:** *Execution-Phase Safety for VLA Agents* (draft v0.45) · **Domain:** embodied AI / VLA / robot-safety benchmarks & standards · **Confidence:** 4/5 (logs not inspected; 2026 competitors checked against arXiv/venue records)

## Score: 58 / 100 — Major Revision

| Sub-score | / 20 |
|---|---|
| Literature coverage & positioning | 12 |
| Theoretical framework (four dimensions, sub-type construction) | 13 |
| Predicate accuracy vs. the standards community | 13 |
| Domain contribution / novelty | 12 |
| **Diversity & scene design (review focus)** | **8** |

## Summary Assessment

The cut is real: safety judged on the *trajectory* rather than the instruction or terminal state, four dimensions, nine predicates, each scored against a human-referenced quantity and each paired with a *feasibility witness* and a *fixability ablation* (§4.2, §6). "Witness, or the cell is marked unattributed" is better epistemic hygiene than any 2026 suite I know.

The weakness is exactly what the authors ask about. On raw counts the tabletop battery sits at the current norm for a *safety* suite; but the diversity is one-dimensional, the effective policy count is two families, and the cell carrying the novelty claim — a locomoting humanoid carrying a hazard past a bystander — is one room with one policy that the authors report does not transfer (0/31 delivered in two other rooms, §8). A benchmark whose headline cell has *n* = 1 scene is a case study plus a tabletop suite. Add one missed concurrent competitor drawing the same before/during/after cut, two mis-cited references, and one predicate (T3) whose chance level makes its dimension score uninterpretable.

## Strengths

1. **The decomposition is principled, not decorative** (§3.2). Appendix B's "which layer below the policy covers this?" argument survives the "collision avoidance renamed" objection.
2. **Witness-and-attribution discipline.** Marking T2 attribution-pending, and the tabletop T5a and midpoint keep-out *exposure* rather than scores, is rare and right.
3. **ISO/TS 15066 Annex A used correctly.** 110 N abdomen / 140 N hand quasi-static and 220 / 280 N transient match Table A.2 and the 2× rule, and the quasi-static limit is rightly applied to a 1.7 s clamping contact.
4. **Battery tiering by capability** (Table IV) avoids safety rates on tasks the policy cannot do; I re-counted the 51 / 40 / 6 figures and they match §8.

## Issues

**CRITICAL 1 — A concurrent benchmark draws the same three-phase cut and is not cited.** SafeStage (arXiv:2609.21223, Sept 2026) is "a lifecycle-structured benchmark for evaluating manipulation safety before, during, and after task execution," with an explicit **Execution-Time Safety** stage scoring "unsafe contacts, trajectories, region entries, and object interactions during execution," 97 risk scenarios, and π0.5 and GR00T N1.7 among its four policies — the paper's §3.1 axis and two of its policies. *Fix:* cite it, add a Table I row, re-scope the claim. SafeStage has **no human proxy** in any scenario and cites **no ISO standard**, so what survives is "human-referenced predicates + standards grounding + witnesses," not "execution-phase safety as a new axis." Say that in §1 bullet 1 and §2.

**CRITICAL 2 — The novel cell has no scene diversity, and the paper shows it does not travel.** The G1 family is one corridor, one task, one policy; §8 reports 0/31 deliveries in two other rooms; T1's primary cell is 10 completing carries, T6 11. The scene norm is set by RoboCasa (120 kitchen scenes, 100 tasks) and BEHAVIOR-1K (50 scenes, 1,000 activities); HumanoidBench (27 tasks) shows a low *task* count is forgivable on a humanoid — one *scene* is not. *Fix:* get the corridor into ≥ 3 rooms (a reported finetune is acceptable), or demote the humanoid to a labelled case study and let the tabletop family carry the benchmark claim — achievable this cycle.

**MAJOR 3 — T2's 0.10 m threshold misreads the SSM formula.** Appendix D: "0.10 m is the intrusion-and-uncertainty allowance we use for $Z$ … inside it contact cannot be excluded." The violation in ISO/TS 15066 is $S < S_p$; $Z_d + Z_r$ is one *summand* of $S_p$, not a criterion. Appendix F itself computes the ISO 13855 approach term alone at ≈ 0.48 m (0.3 s), so §5.1 and Appendix D conflict. *Fix:* keep 0.10 m as a renamed *contact-plausibility* margin and add the $S_p$-referenced rate — your threshold curve already has it.

**MAJOR 4 — The T5a envelope mixes an incompatible $K$ and $C$.** $d_0 = 0.94$ m from $v_h = 1.6$ m/s, $T_r+T_s = 0.4$ s, $C = 0.2$ m, $Z = 0.1$ m. $C \approx 0.2$ m follows ISO 13855's $C = 8(d-14)$ only for a **40 mm-resolution (finger/hand)** field, while $K = 1.6$ m/s is the **whole-body** approach speed; a body-detected bystander carries a far larger $C$. *Fix:* state the assumed resolution, or give $d_0$ over $C \in [0.2, 0.85]$ m; the direction is conservative, so the finding survives.

**MAJOR 5 — The orientation dimension score has no calibrated null.** T3's half-space predicate has a 50 % chance level (pooled π0.5 43 %, GR00T 52 %). Averaged with T4 (null 0 %), the *person-blind scripted control* scores 30 and π0 46 — not readable as unsafety. *Fix:* report T3 as excess over chance with a CI, or narrow the cone to 30–45°, and headline the worst-bearing rate (20/20, 10/10 — the honest one). Never average a 50 %-null predicate into a mean.

**MAJOR 6 — Effective policy diversity is two families, not four or five.** §4.1 concedes π0.5 / π0 / π0-FAST are "one backbone, two action decoders"; GR00T N1.6 and N1.6-DROID are one family. §5.5's recurrence therefore rests on 2 independent policies, against LIBERO-Safety's 10 and SafeVLA-Bench's 9. *Fix:* add one architecturally distinct policy (OpenVLA or a diffusion policy, as Appendix F plans); meanwhile say "two policy families."

**MAJOR 7 — Two references are mis-cited, both flagged "verify at camera-ready."** [56] arXiv:2606.18632 is *ROBOSHACKLES: A Safety Dataset for Human-Injury Prevention in Embodied Foundation Models* (Yin et al.; 10,000 clips, 100 % unsafe-action rate), not "Video-level safety evaluation…". [57] arXiv:2605.31196 is *Probing Collision Grounding in VLMs for Safe Human-Robot Collaboration* (Wang, Xu, Huang) — separated / colliding / about-to-collide with **people** — not "TouchSafeBench." Both are closer to this work than the placeholders, so §2's "sit elsewhere" is unsupported.

**MINOR 8 — Design-space coverage is a small corner.** Appendix B names 7 payload-danger classes × 4 vulnerable parties × 5 person states × 5 safe moves; instantiated are 3 carried hazardous objects (drill 0/32 and pitcher 0/16 are capability boundaries) and 3 person states, none reactive. State which corner is covered and which axes are open.

**MINOR 9 — Terminology.** (a) T6b: the SSM human-velocity term enters $S_p$; it does not "presuppose" robot deceleration (stopping or detouring is equally compliant) — re-word to "a response SSM compliance would require." (b) ISO 10218-1:2025 retains 250 mm/s *and* consolidates ISO/TS 15066; §4.1 reads as if the TS were still free-standing. (c) Child-height cells score a child against adult Annex A limits, which do not cover children — label those exposure.

**MINOR 10 — Competitor scale is never stated,** so breadth cannot be judged. Put LIBERO-Safety's 500+ tasks / 10 models, HazardArena's 40 tasks / 7 categories, SafeStage's 97 scenarios and AGENTSAFE's 1,350 tasks into Table I. Your 51 / 40 then reads as *comparable in count, differently sampled* — the true and defensible position.

## Closest prior work → what this adds

| Closest prior work | Already does | What we add |
|---|---|---|
| **SafeStage** (2609.21223) | before/during/after lifecycle; execution-time contacts, trajectories, region entries; 97 scenarios; π0.5 + GR00T N1.7 | a **human** in the scene; ISO-referenced predicates; witnesses; orientation and anticipation |
| **LIBERO-Safety** (2606.23686, ECCV 2026) | 500+ tasks, hand proxy, kinematic perturbation, 10 models | locomoting embodiment; sweep vs. body *surface*; carried-hazard keep-out; fixability |
| **SafeVLA-Bench** (2606.00773) | STL clauses, succeed-but-unsafe, 9 policies, tilt, force ceiling | human referent for force (body region) and speed (SSM); orientation; reactivity |
| **SafeVLA / Safety-CHORES** (2503.03480) | the one mobile-manipulation safety suite | humans present; carried-hazard and presentation channels |
| **Handover line** ([32]–[34], [53]–[55]) | hazard-away presentation to a *cooperating receiver* | the **passive, non-receiving bystander**; orientation invariance |
| **ROBOSHACKLES** (2606.18632) | human-injury dataset, 10k clips, 100 % unsafe rate | closed-loop physics, not video-level judgement |

Also cite: *Probing Collision Grounding in VLMs* (2605.31196); *How Long Until Your Robot Ignores You?* (2609.07288 — human–humanoid, ISO 10218-2:2025-grounded); AGENTSAFE (CVPR 2026); RoboCasa, BEHAVIOR-1K, HumanoidBench for the breadth argument; and the socially-aware-navigation line (Kruse et al. 2013; Rios-Martinez et al. 2015), which owns bystander clearance for mobile bases.

## Questions for the Authors

1. Can the corridor family be shown in ≥ 2 rooms with a delivering policy this cycle? If not, will you demote it to a case study?
2. What is the excess-over-chance orientation rate per policy, with CI — and does the ranking survive it?
3. Do the T2 and T5a rates hold against a full $S_p$ rather than $Z$ and a finger-resolution $C$?
4. Which Appendix B design-space axes do you claim to have sampled, at what episode counts?
