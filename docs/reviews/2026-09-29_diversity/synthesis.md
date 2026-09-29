# Editorial decision — round 4, "is the diversity and the scene design sufficient?" (2026-09-29)

**Decision: Major Revision.** Panel scores 58 (EIC), 54 (methodology), 58 (domain), 68 (perspective), 58 (devil's
advocate); mean **59.2**, down from round 3's 68.3 — not because the suite got worse, but because this round asked a
question the earlier rounds did not: whether the breadth that exists ever reaches the table that carries the claim.
The devil's advocate raised CRITICAL issues, so Accept was not available.

## The panel's answer to the question

**The diversity is real; the matrix does not inherit it.** Four of five reviewers arrived independently at the same
sentence: Table III rests on the canonical pick-and-place plus two person variants, while the 51-task, six-surface,
four-map breadth sits in Table IV, which is headed "(π0.5)" and by construction never enters the matrix. So the
advisor's requirement — *each dimension rests on several tasks* — is satisfied by the **project** and not by the
**deliverable**. Collecting more scenes would not fix this; routing the scenes already collected into the matrix would.

## Consensus (independent agreement, 4–5 reviewers)

1. **CRITICAL — the Trajectory column is arithmetically empty.** It is the equal-weight mean of a forced ceiling
   (T1 = 100 %, the marker sits at the midpoint of a collinear transport, which §5.1 and E.8 both call exposure) and a
   floored predicate (T2 = 0–1 %), so it reads **exactly 50 for π0.5, π0, π0-FAST and the person-blind scripted
   control**. Verified independently against `gen_a45_numbers.py` output. Raised by EIC #2, methodology C3,
   perspective #2, devil's advocate C3.
2. **CRITICAL — the control reproduces the profile on three of four dimensions.** Control 50 / 47 / 6 / 100 against
   π0.5's 50 / 43 / 7 / 94. Only T4 separates them (77 % vs 13 %), and that witness rests on a pinch grasp that
   carried 31 of 112 attempts. A matrix whose columns a blind straight line can match does not yet have
   discriminative validity. Raised by EIC, methodology, devil's advocate.
3. **CRITICAL — "several tasks per dimension" does not hold for any cell of Table III.** Each dimension rests on one
   canonical task carrying several *predicates*; Speed & force and Dynamics are built from the *same* reaching-hand
   episodes and denominator (`gen_a45_numbers.py:74-77`); π0's T1 is three cells at one surface, π0-FAST's four at
   one, GR00T-DROID's one cell of one seed; the G1 row is one carry in one corridor.

## Verified by the chair after the panel reported

**SafeStage (arXiv:2609.21223, submitted 18 Sept 2026) is real, concurrent, and uncited.** The domain reviewer's
CRITICAL #1 checked out: *Evaluating Safety Before, During, and After Vision-Language-Conditioned Robot
Manipulation*, 97 risk scenarios, an explicit **Execution-Time Safety** stage of 40 tasks, implemented in RoboLab on
GPU PhysX at 120 Hz with **the simulated DROID embodiment, a 7-DoF Franka Panda with a Robotiq 2F-85** — our exact
tabletop robot — and evaluating π0.5, GR00T N1.7, DreamZero and Cosmos3 Nano.

It is also the sharpest available differentiation: **it contains no humans.** No person proxy, no bystander, no
separation or force predicate, no ISO grounding. Its execution-time stage scores unsafe contacts, trajectories and
region entries as object and region events. Ours scores what the motion does to a *person*, against ISO 10218-1,
ISO/TS 15066 and ISO 13482. The surviving novelty is therefore not "execution-phase safety is a new axis" — that is
now concurrent work — but "**human-referenced execution-phase predicates, grounded in the standards, with in-scene
feasibility witnesses**". The paper must say this in §1 and §2 rather than let a reviewer discover it.

## Dissent and single-reviewer findings worth acting on

* **Perspective (CRITICAL).** The Speed & force column publishes a four-policy ranking of a quantity the paper itself
  disowns: T5b counts constraint force on an inert capsule, while E.8 says the free-hand estimate is 7 N median,
  0/202 above 140 N, and calls the Table III exceedances "the capsule's, not the hand's".
* **Methodology (CRITICAL).** Pooled rates ignore clustering by cell. T3's 32/75 is bimodal by cell (0/8, 0/7 versus
  4/4, 6/6) because the spawn pose fixes the outcome: design effect 3.80, n_eff ≈ 20, and the interval widens from
  [32, 54] to **[22, 65]**, so "at chance" is not supported. T6 similarly: deff 4.33, [87, 97] → [83, 100].
* **Devil's advocate (CRITICAL).** "Four policies" is one dataset: three openpi decoders plus GR00T-DROID, all DROID.
  E.8's own sentence — the drift is learned from the demonstrations, not added by any one action head — says so.
  Cross-policy recurrence is cross-*decoder* recurrence on one corpus.
* **Devil's advocate (CRITICAL).** Route memorisation is a live alternative for every G1 signature (fixed carry yaw,
  path invariant to naming and rendering, no slowing) and is strengthened by the new 0/31 deliveries in two other
  rooms. Appendix E.1 already names the clean test — `navigate_cmd` logging — and it has not been run.
* **Domain (MAJOR).** T2's 0.10 m threshold treats the SSM formula's uncertainty summand *Z* as if it were the
  protective separation *S_p*, which Appendix F's own ≈0.48 m approach term contradicts; and references [56], [57]
  are mis-cited — the real arXiv:2606.18632 and 2605.31196 are closer to this work than the placeholders dismissed.
* **Perspective (MAJOR).** Occluded and late-revealed people are structurally absent: the perception ablation is a
  render-hide toggle at fixed geometry, so "architecture, not perception" is established only for an always-visible
  person. Exposure *duration* is owned by no dimension.

## Revision roadmap, ordered by value per hour

| # | Action | Cost |
|---|---|---|
| R1 | Score Trajectory on the **off-path** keep-out (0.20 / 0.28 m) instead of the forced midpoint marker, which the paper already calls exposure. The data exists for five rows: π0.5 62/63 and 12/64, π0 16/17 and 4/18, π0-FAST 32/32 and 2/32, GR00T-DROID 15/15, control 14/56 and 0/64. This alone turns four identical 50s into a column that separates every policy from the blind line | re-analysis only |
| R2 | Stop publishing T5b as a policy ranking: either label Speed & force exposure on the tabletop, or score it on the Annex A free-hand estimate the paper trusts | re-analysis only |
| R3 | Cluster-robust intervals (design effect by cell) on every pooled rate, and an interval on each dimension score | re-analysis only |
| R4 | Cite and differentiate SafeStage in §1/§2; restate the contribution as human-referenced predicates + standards + witnesses | text |
| R5 | Say plainly that three tabletop rows are one backbone and all four are one dataset, and retitle the claim "recurs across action decoders trained on one corpus" | text |
| R6 | Promote breadth into the matrix: extend Table III's pools to the serving / clutter / tool cells for the policies that have them (π0-FAST already has 11 battery tasks) so "several tasks per dimension" becomes true for at least two rows | generator + a few top-up cells |
| R7 | Run the `navigate_cmd` logging test that Appendix E.1 names, to separate route memorisation from a missing competence on the G1 | compute, ~half a day |
| R8 | Fix T2's threshold derivation (Z vs S_p) and the two mis-cited references | text |

**What the paper is entitled to claim today**, on the panel's reading: that four DROID-trained decoders and one
humanoid checkpoint place a measurable demand on an external safety layer along four dimensions, in one tabletop
topology at six heights and one corridor — not that the profile generalises across scenes, and not that the matrix
ranks policies.
