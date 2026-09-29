# Review round 4 — configuration card (2026-09-29)

**Question put to the panel.** *Is the diversity and the scene design actually sufficient?* — judged against the
advisor's framing: four dimensions (posture/orientation, trajectory, speed, dynamics), a policy × dimension matrix,
each dimension resting on several tasks, and every predicate defined with a stated reason.

**Manuscript.** `docs/execution_phase_safety_position_paper_draft.md` (1755 lines; main text to p10, 81 pp built).
Design rationale: `docs/dimension_design_2026-09-16.md`. Numbers: `_scratch/gen_a45_numbers.py`, `_scratch/analyze_fr.py`.

**Mode.** `full` — five independent reviewers (EIC, methodology, domain, perspective, devil's advocate), then editorial
synthesis. Reviewers do not read one another. No reviewer may modify the manuscript.

**Prior rounds.** `2026-09-17_task_design` (Major Revision, 64.2) and `2026-09-20_design_diversity` (Major Revision,
68.3; C1–C9 all discharged). The devil's advocate was asked to check whether any of those was discharged only
cosmetically.

## What the suite contained on the day of review

| Policy | scored cells | episodes | carries |
|---|---|---|---|
| π0.5 · Franka | 606 | 4161 | 3192 |
| π0 · Franka | 107 | 845 | 253 |
| π0-FAST-DROID · Franka | 142 | 1136 | 793 |
| GR00T N1.6-DROID · Franka | 47 | 287 | 116 |
| PaliGemma-binning · Franka | 10 | 80 | 0 (decoder boundary) |
| scripted straight-line control | 151 | 988 | 881 |
| **total** | **1072 labels** | **7497** | — |

Plus the G1 corridor family (GR00T N1.6 on a Unitree G1), typed into the generator from the b7/b9/b11 rounds and the
2026-09-28 additions (crossing person ×4 seeds, walking-speed approach, human-mesh crosser, child-height crosser).

Scenes and tasks as claimed by the manuscript: six work surfaces, four environment maps, 51 tabletop battery tasks of
which 40 are exercised and 6 are capability boundaries, one corridor scene for the humanoid — with a second corridor
room shown on 2026-09-28 to be a capability boundary (6/31 carried, 0/31 delivered).
