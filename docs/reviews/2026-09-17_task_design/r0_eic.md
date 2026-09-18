# Peer Review Report

## Manuscript Information
- **Title**: Execution-Phase Safety of VLA Policies: A Four-Dimension Benchmark (working title, from §3 / design note of 2026-09-16)
- **Manuscript ID**: review2 / round 0
- **Review Date**: 2026-09-17
- **Review Round**: Round 0 (pre-submission panel, ICLR 2027 target)

---

## Reviewer Information

### Reviewer Role
EIC (Area Chair role)

### Reviewer Identity
ICLR Area Chair for embodied AI and benchmarks; has handled many benchmark-track submissions and judges whether a task suite is a designed instrument or a count of variants.

### Review Focus
Task design and diversity design only: whether the suite of tasks, scenes and policies is a substantive design; whether "13 tasks, 6 surfaces, 6 maps" is substance or number; and whether each of the four dimensions rests on tasks whose scored predicate measures what the design note says the task adds. Statistics are left to Reviewer 1.

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
The paper defines execution-phase safety as a per-step trajectory predicate that survives when instruction and outcome are both safe (§3.1), organises it into four dimensions and seven sub-types with a stated reason per threshold (Table II), and measures four policies on two families: a G1 corridor carry and a Franka tabletop family with 13 task types, 6 work surfaces and 6 environment maps. As a piece of benchmark design, the strongest parts are the per-task "what it adds" argument and the feasibility-witness discipline: the suite is built around mechanisms (a rotated spawn as a causal test, a withdrawing hand as a witness, present-vs-absent to remove the trajectory confound), not around a variant count. The weakest part is that the diversity claimed on the headline (13 × 6 × 6 × 3) is thinner than the scored suite: the per-cell table lists 6 tasks, environment maps vary for one task on one surface, two policies cover only pick-and-place and serving, three tasks cannot be scored at all, and several tasks are mapped to a dimension by a mechanism that the scored predicate does not capture (push, pour, passer-by, close-a-door). The policy × dimension matrix also averages scene-set saturated sub-types (T5a 98–100% on every task) with near-zero ones into headline numbers that do not discriminate policies, and two pooling choices give different headlines (Table 1 vs Table III). The framework is publishable; the suite needs to be fixed, named and honestly sized before the matrix is the contribution the paper says it is.

---

## Strengths

### S1: Each dimension is argued as a residual hazard, not a synonym for collision avoidance
§3.2 and the design note give, for every dimension, a "why it is not collision avoidance" paragraph ("a protective stop freezes a pose, it does not correct one"; "only the policy could anticipate a person on a collision course"). This is the right test for a benchmark dimension and most safety suites skip it.

### S2: Tasks are chosen for the mechanism they add, and the results confirm the mechanism
The design note's per-task tables state one thing each task adds, and several are borne out with numbers: the serving task raises T2 from 2% (15/667) on neutral pick-and-place to 22% (28/128) because "the task itself sends the arm at them"; the 180°-rotated scissors move the T3 violation to the other side (right 10/10 → 5/13, left 1/10 → 12/15, E.8) while the person never moves. That is a designed causal probe, not a scene variant.

### S3: The interaction-geometry batteries answer the "wallpaper" objection substantively
The five placements (far edge, two far corners, object on the person's side, bowl between) change the geometry rather than the map, and the result is informative: T4 is present at every placement (11/16, 8/15, 8/16, 16/16, 11/11) while T2 stays ≈0 unless the task sends the arm to the person (2/32 when the object starts on their side). This is exactly the kind of variation a benchmark should carry.

### S4: T5c is a sub-type that emerged from a task, which is what a good suite should do
The tool cells produced a quantity no transport cell can show (tip speed 0.50 m/s peak, max 1.17, 5–10× carry speed, within 0.19 m; 10/41 above ISO 10218-1's 0.25 m/s inside 0.5 m). Growing the sub-type list from an observed hazard rather than from an a-priori list is evidence the task design is doing work.

### S5: Attribution via feasibility witnesses
§4.2's rule that "a rate is attributable to the policy only if the scene admits a compliant completion", with witnesses marked per cell in Table III, is a design principle that makes the suite auditable and that other benchmarks should adopt.

---

## Weaknesses

### W1: The suite's size is stated as 13 × 6 × 6 × 3 but the scored suite is far smaller
**Problem**: Table 2's header says "tasks: 13 | scenes: 6 work surfaces, 6 environment maps | policies: 3", but the per-cell table on the same page ends "23 groups | ... tasks 6 | policies 3", and the environment maps (lounge, auto shop, courtyard, woodland, warehouse) are varied for pick-and-place on the dining table only (16, 16, 16, 9 episodes) plus one warehouse cell. π0 and GR00T-DROID run only pick-and-place and serving at "scene default". Three tasks in the design note are unscorable: close a door (0/8 carried), put away in a drawer (0 delivered of 32), and cutting/wiping (no asset). Dynamics has entries for 3 of 13 tasks.
**Why it matters**: A benchmark-track reader will multiply the headline counts and expect a filled grid; the grid is mostly one policy on one task with the maps and geometries as side batteries. Tasks a policy cannot perform are not benchmark tasks yet; they are a wish-list.
**Suggestion**: Publish a named, fixed task list with a coverage matrix (task × surface × map × policy, with N), separating "scored", "defined, unscorable by current policies", and "planned". Report the map variation as what it is: a robustness check on one cell. Count only scored tasks in the abstract.
**Severity**: Critical

### W2: Several tasks are assigned to a dimension by a mechanism that no scored predicate captures
**Problem**: The design note says push carries trajectory because "the payload can leave the surface on the person's side", but Table 2 scores push at "0% (T2 0)" with no T1 or surface-exit predicate. Pour is said to turn T4 into "where the tilt happens, not whether", yet Table 2 scores pour as T4 45% with the same peak-tilt predicate. The passer-by is said to answer "does the speed respond?" dynamically, but its dynamics entry is T6 contact, 0/25, in a scene where contact is impossible by construction. Close a door is listed under dynamics with nothing scorable.
**Why it matters**: This is the difference between diversity as design and diversity as count. If the task's stated contribution is not what the predicate measures, the task is a variant of pick-and-place under a new name, and the dimension × task table (Table 2) overstates how many tasks support each dimension.
**Suggestion**: For each task, either add the predicate that scores its stated mechanism (push: payload leaves surface toward the person; pour: tilt location relative to the bowl; passer-by: speed change vs. time-varying separation, i.e. a T5a-dynamic variant) or drop the task from that dimension's row.
**Severity**: Critical

### W3: The dimension score averages scene-set saturated sub-types with near-empty ones, so the headline matrix does not discriminate
**Problem**: T5a is 98–100% for every policy on every one of 13 tasks (Table 2), and §5.3 concedes it is "scene-set (no 1.9 m traversal stays outside d0)". Yet it enters every "speed & force" score at equal weight, giving GR00T-DROID "50 (T5a 100, T5b 0)" on T5b n = 2, and π0.5 trajectory "50 (T1 100, T2 1)". T1 on the tabletop sites the keep-out "per episode at the geometric midpoint of that carry" — a predicate a direct carry violates by construction; the rendered-marker version (16/16) is the informative one. The G1 orientation "50 (T3 100, T4 0)" averages a cherry-picked azimuth pair with a rigid-box T4 the paper itself calls a weak proxy (§8).
**Why it matters**: The matrix is presented as "the benchmark's main result" (§5). A score that is ≥50 for every policy because of a scene-set term cannot rank policies and will be read as one.
**Suggestion**: Drop saturated, scene-set sub-types from the dimension mean (or report them as "scene exposure", not "unsafe rate"); use the rendered-marker T1 as the tabletop T1; require a minimum N per sub-type before it enters a policy's cell; and remove "π0.5, serving" as a row in a policy matrix — it is a task.
**Severity**: Major

### W4: The suite is not fixed: two pooling choices give two headlines
**Problem**: Table 1 (all tasks pooled) gives π0.5 orientation 62% (T3 55, T4 68) and π0 trajectory 1%; Table III gives π0.5 orientation 83 (T3 100, T4 67) and π0 trajectory 50 (T1 100, T2 0). Dynamics is 62 vs 63, trajectory 52 vs 50.
**Why it matters**: A benchmark must define which cells constitute the suite; otherwise the same data yields whichever profile the author prefers, and no one else can submit a comparable row.
**Suggestion**: Declare one canonical suite (cells, seeds, weights) and one headline table; move the "everything pooled" view to an appendix.
**Severity**: Major

### W5: Dynamics rests on one sub-type and, on the tabletop, essentially one task
**Problem**: Dynamics is T6 only. On the tabletop the score comes from the reaching hand (87/138); handover contributes 6/24 and the passer-by 0/25 (see W2). Close a door is unscorable. On the G1 the crossing person is the only task.
**Why it matters**: A dimension the paper motivates as the one that "alone is scored against a reference that moves" (§3.2) cannot claim parallel status with the other three on one predicate and one geometry per family.
**Suggestion**: Add at least one anticipation predicate that is not contact (a deceleration or re-plan before separation drops below d0), score the passer-by and handover on it, and report T6b release as its own sub-type.
**Severity**: Major

---

## Detailed Comments

### Title & Abstract
Not in the package. Ensure the counts in the abstract are those of the scored suite (W1).

### Methodology / Research Design
§4.1 lists the families clearly, but the reader must reconstruct from E.8 and tables.txt which tasks were actually run per policy. The "what it adds" tables belong in the paper's §4, not only in the design note; they are the best argument the paper has that the suite is designed.

### Results
Table III's caption honestly flags "T3 at the bearing the frozen carry axis faces" and "— = not scorable", but the cells still print 100 and 0. Table 2 is more informative than Table III for a benchmark reader and should be promoted. T5a's row of 98–100% across all tasks should be presented as a finding ("no SSM behaviour anywhere") once, not as thirteen scored cells.

### Discussion / Limitations
§8 lists small cells, weak proxies and missing witnesses, but not the task-coverage asymmetry (W1) or the pooling sensitivity (W4). The closing sentence "None of this undercuts the case" is stronger than the coverage supports for π0 and GR00T-DROID.

---

## Questions for Authors
1. What is the canonical suite? List the exact cells, seeds and per-sub-type N that produce Table III, and state whether Table 1 or Table III is the benchmark's headline.
2. For push, pour, passer-by and close-a-door: what predicate scores the mechanism the design note says each adds? If none exists, will the task be removed from that dimension's row?
3. Does any policy other than π0.5 run any task other than pick-and-place and serving? If not, how should a reader interpret the π0 and GR00T-DROID rows as profiles rather than two cells?
4. Should a scene-set sub-type (T5a at 100% by exposure geometry) enter the dimension mean at all, and if so with what weight?

---

## Minor Issues

### Figures and Tables
- Table 2 header ("tasks: 13") and the per-cell table footer ("tasks 6") disagree on the same page.
- Table III mixes a task row ("π0.5 · Franka, serving") into a policy matrix.
- "seven sub-types" (design note, 2026-09-17) vs "six sub-types" (§3.3 heading and Table II caption) — the text was not updated when T5c was adopted.
- Design note "Interaction geometry (added 2026-09-18)" is dated after tables "generated 2026-09-18" and after today's review date; align dates.

### Language
- E.8 T3 paragraph: missing space before "Spawned at 90° instead".

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|---|---|---|---|
| Originality (20%) | 72 | Adequate/Strong | Execution-phase framing, witnesses and T5c are genuine; the task suite is less novel than its count suggests |
| Methodological Rigor (25%) | 58 | Weak | Design-level: unfixed suite, scene-set sub-types in the mean, task-to-predicate mismatches (W2–W4) |
| Evidence Sufficiency (25%) | 60 | Adequate | Rich for π0.5 pick-and-place; thin for the other policies and most tasks |
| Argument Coherence (15%) | 62 | Adequate | Dimension motivation is coherent; the matrix does not follow from it as cleanly as §5 claims |
| Writing Quality (15%) | 70 | Adequate | Dense but precise; several count/heading inconsistencies |
| **Weighted Average** | **63.5** | **Major Revision** | |

### Recommendation to Peer Reviewers
Reviewer 1: check whether the Table III cells with N ≤ 6 (π0 T3 4/5, T5b 0/4, T6 3/4; DROID T3 2/6, T5b 0/2, T6 0/2) should appear in a headline at all, and the 50/62/83 discrepancies between Table 1 and Table III. Domain reviewer: is the geometric-midpoint T1 a meaningful predicate or a tautology for a direct carry, and is T5a's envelope an "unsafe rate" or a scene-exposure statistic?
