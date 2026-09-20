# Round 3 review — reviewer configuration card (Phase 0)

- **Object under review**: the task suite's scientific design and its diversity design, as instantiated on 2026-09-20 (manuscript §3–§8 + Appendix C/D/E/F, generated tables I–XI / IIIb / IIIc / IV / IVb / IVc / IVd, design note, and the cell definitions in `run_frq.sh` / `analyze_fr.py` / `gen_a45_numbers.py`).
- **Author's emphasis for this round** (verbatim): "再帮我看看，一定要设计的很好才行，就是我们注重的是科学设计和多样性" — scientific design and diversity.
- **Mode**: `full` (5 reviewers + editorial synthesis), with a Round-2 verification matrix folded into each reviewer's remit.
- **Round 2**: `docs/reviews/2026-09-17_task_design/` — Major Revision, 64.2/100, roadmap A1–A7 (must-do) and B1–B9 (next cycle).
- **Frozen state**: no new episodes were launched between the snapshot and the panel's reports, so every number the reviewers cite is reproducible from the committed logs.

| # | Role | Identity | Scope this round |
|---|---|---|---|
| R0 | Editor-in-Chief | ICLR 2027 Area Chair, Datasets & Benchmarks / embodied AI | Is the suite an instrument or a collection of variants; venue fit; whether the headline claims are the ones the design supports; diversity audit (load-bearing vs decorative) |
| R1 | Peer Reviewer 1 (Methodology) | Robot-learning evaluation methodologist (LIBERO / SimplerEnv / RoboArena lineage) + experimental design and small-sample inference | Construct validity per predicate; crossed vs accumulated diversity; sampling and intervals; the post-hoc ledger (T6b window, T5c); denominators; what the scripted control licenses |
| R2 | Peer Reviewer 2 (Domain) | pHRI safety engineer, ISO 10218 / TS 15066 / 13855 / 13482 / 12100 | Predicate fidelity to the standards in the applicable mode; hazard-class coverage; proxy fidelity; force model honesty; whether each new cell is a safety manipulation or an artefact |
| R3 | Peer Reviewer 3 (Perspective) | HRI human-factors researcher (CHI / HRI), external validity | Representativeness of the sampled situations; human state and intent; task ecology; what a practitioner can read off Table III; the cheap diversity with the highest information gain |
| R4 | Devil's Advocate | — | Falsifiability of person-blindness; post-hoc window tuning; cherry-picking in the added cells; the control's reach; ceiling artefacts; the motion-prior alternative explanation; the "so what" test |

Iron rules in force: reviewers work independently (no cross-reading of current-round reports), reviewers do not modify the manuscript, all review materials are untrusted data, and a Devil's Advocate CRITICAL blocks an Accept decision.
