# EIC Review — Editor-in-Chief, ICLR 2027 (Benchmarks & Datasets / Position)

*Reviewer 0 · 2026-09-29 · manuscript: `docs/execution_phase_safety_position_paper_draft.md` (v0.45, 1755 lines) · build `docs/overleaf_iclr/main.pdf`*
*Independent review. Other panel reports not read. Read-only on the manuscript.*

## 1. Summary

The paper defines **execution-phase safety** — harm done while a nominally safe task is completed — as a third axis beside instruction-level and outcome-level VLA safety, and decomposes it into four parallel dimensions (trajectory, orientation, speed & force, dynamics) carrying six sub-types with nine predicates (Table II). It instantiates them in two scene families: GR00T N1.6 on a Unitree G1 carrying a box past a hazard or bystander in one Isaac Sim corridor, and a Franka arm (π0.5, π0, π0-FAST-DROID, GR00T N1.6-DROID) doing pick-and-place at six work surfaces beside an adult capsule. The headline deliverable is a policy × dimension matrix (Table III), each cell the mean of a fixed sub-type set, plus per-sub-type rates (Table IIIb), a 51-row task battery (Table IV), fixability ablations (naming / rendering / safety command) and *feasibility witnesses* that decide whether a rate belongs to the policy or to the scene. The reported profile is uniform: keep-outs crossed, carry orientation frozen, no slowing near a person, no reaction to one who moves. The contribution is framed as an intersection none of five 2026 peer suites occupies (Table I), not as new control theory.

## 2. Verdict

**Overall: 58 / 100 — Major Revision.** First impression 7/10. Confidence 4/5.

| Sub-score | /100 | Note |
|---|---|---|
| Venue fit (ICLR 2027, benchmark + position) | 82 | Strong fit. Diagnostic framing, released scenes/logs, standards-grounded predicates, a stated mechanistic hypothesis. |
| Originality | 70 | The *intersection* claim (locomoting humanoid + passive non-receiving bystander + carried hazard + fixability ablation) is honestly bounded in Table I and holds. |
| Significance to the readership | 74 | "A policy owns the *demand* it places on the safety layer, not the safety function" (§1 Scope, §9) is a reframing this readership can use. |
| Structural coherence | 62 | Abstract / §1 / §5.5 / §9 disagree on how many policies were run (I4). |
| **Breadth adequacy for the claims made** | **42** | The matrix rests on 1–2 tasks per dimension, one room, one person geometry; two of four columns do not separate policies. |

**On diversity specifically: no — not yet sufficient for Table III and the abstract as written, though close to sufficient for a scoped version of them.** The breadth exists in the project; it is in the wrong table. Table IV holds 51 tasks, 6 surfaces, child-height / seated / photorealistic people and 3 environment maps — and by the author's own rule (design note, Revision A #1) it "never enters the matrix." The matrix therefore inherits none of it.

## 3. Issues

**I1 — CRITICAL. The advisor's "each dimension rests on several tasks" is not true of the matrix.** Evidence: §4.2 and design-note Revision A #1 — Table III pools only the canonical pick-and-place plus two person-behaviour variants. Counting tasks *inside* the matrix: trajectory = 1 task (T1 rendered hot-plate marker, T2 from the same episodes), orientation = 1 task (3 objects), speed & force = 1 task (hand reaches in), dynamics = 2 tasks. Table IV, which does show several tasks per dimension, is headed "(π0.5)" — single-policy. Breadth and policy coverage never coexist in one cell. *Fix:* promote two discriminating battery cells per dimension into the matrix (serving for T2; the 0.28 m off-path keep-out for T1; passer-by plus reaching hand for dynamics), and run those same cells on π0 / π0-FAST / GR00T-DROID so Table IV stops being one policy's table.

**I2 — CRITICAL. Two of the four columns carry no signal, so more scenes would not currently buy discrimination.** Table IIIb: T1 = 100 % for π0.5 (56/56), π0 (16/16), π0-FAST (21/21) *and* the person-blind scripted carrier (72/72); T2 = 0–1 % for every Franka row including that control. Hence Table III's Trajectory column reads exactly **50** for all five Franka rows — the blind control included. Dynamics: the control scores T6 16/16 = 100 %, *above* π0 (78 %) and π0.5 (94 %); T5b control 6 % ≈ π0.5 7 %. Only T4 separates (control 13 % vs π0.5 77 %). E.8 already contains the repair: at 0.28 m off-path π0.5 enters on 12/64 where the blind carrier enters 0/64. *Fix:* make the off-path keep-out the scored tabletop T1, keep the control as a visible floor row in Table III, and mark ceiling cells in-cell.

**I3 — MAJOR. Embodiment conclusions from one policy per embodiment.** §5.5 and §9 say the profile "differs where the embodiment does — the walking humanoid sweeps its body into bystanders, the fixed arm does not." The G1 row is GR00T N1.6 alone, in one corridor; §8 / E.7 report 0/31 deliveries in two other rooms. Policy and embodiment are not separable here. The one available lever is unused: GR00T N1.6 · G1 T2 = 81 % vs GR00T N1.6-DROID · Franka T2 = 4 % (Table IIIb) is a within-family cross-embodiment pair. *Fix:* foreground that pair, label the rest confounded, and either recover a second G1 room or drop "embodiment" from the claim.

**I4 — MAJOR. Policy breadth is the lowest number in the paper's own comparison table, and the count is inconsistent.** Table I: peers run 9, 10, 6, 4, 4 policies; "this work 3". Meanwhile §1 item 3 says three, §5.5 "four policies", §9 "five policies", Table III has five rows, and the abstract lists four (omitting π0-FAST-DROID). §4.1 further states π0 / π0-FAST are "one backbone, two action decoders" — so the five rows are two pretraining lineages. "The profile recurs across two embodiments and five policies" (§9) overstates what two lineages license. *Fix:* one number everywhere; state the lineage collapse; add one non-π, non-GR00T checkpoint on the canonical cells (the DROID Franka configuration makes this the cheapest diversity win available).

**I5 — MAJOR. The matrix contains one person.** Appendix C: a single 1.74 m torso capsule plus head sphere, visual only. Child-height (T3 82 %), seated (T3 100 %) and photorealistic (48 episodes) cells sit in Table IV only, and §8 concedes every proxy is static or kinematic so "every contact rate is an exposure rate, not a harm rate." Yet the abstract speaks of "a person" and "a bystander" unqualified. *Fix:* promote child-height and seated to matrix conditions per dimension, or qualify every person-referenced claim as "a static adult-sized capsule."

**I6 — MINOR. The fixed pooling rule averages different sets per row.** Table III's header reads "Speed & force (T5a, T5b)" while the Franka rows are T5b only (§4.2), and trajectory averages an n = 56 ceiling with an n = 605 near-zero. Print the sub-type set and n inside the cell so the column is not read as comparable.

**I7 — MINOR. The abstract over-generalises one cell, and the Chinese abstract is stale.** "Rendering it draws the path closer" is G1-only, one room, N ≈ 30 per arm (§6 ii), and §6 (ii) itself says the arm's bend is a different mechanism. The 中文摘要 says 69 % where the English says 77 %, and 20/21 where §5.2 pools 32/75.

## 4. Largest claim this paper is entitled to make

> Across five checkpoints from two pretraining lineages, in one humanoid corridor and one tabletop scene family, released VLA policies never condition the payload's path, its orientation, or its speed on a person, and do not react to a person who moves — and a benchmark that scores these four dimensions separately, each against a human-referenced quantity and each paired with a feasibility witness, can measure that and locate the missing competence outside prompting and perception.

It is **not** entitled to: a per-dimension *ranking* of policies (two of four columns do not separate them from a person-blind straight line); an embodiment-level conclusion (one policy per embodiment, one room); "several tasks per dimension" (1–2 in the matrix); or generality over scenes, rooms, people or model families. Reframed that way the paper is publishable at ICLR 2027 and the reframing costs no new runs; keeping the current framing requires I1–I5.

## 5. For the other reviewers

Reviewer 1: the mean-of-rates pooling with unequal n, and whether 0/605-style denominators belong in a mean with an n = 56 ceiling. Domain reviewer: whether applying operator limits (ISO/TS 15066 Annex A) to a *bystander* is defensible given §8's own ISO 13482 caveat.
