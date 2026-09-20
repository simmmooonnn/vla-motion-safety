# Editorial Decision — Round 3 (scientific design and diversity design)

- **Object under review**: the task suite's scientific design and its diversity design as instantiated on 2026-09-20 — manuscript §3–§8, Appendices A/C/D/E/F, generated Tables I–XI / IIIb / IIIc / IV / IVb / IVc / IVd, the design note, and the operational definitions in `analyze_fr.py`, `gen_a45_numbers.py`, `run_frq.sh`, `scripted_carry.py`, `franka_safety_table_environment.py`.
- **Authors' emphasis for this round** (verbatim): "一定要设计的很好才行，就是我们注重的是科学设计和多样性".
- **Round**: 3 (Round 2 = 2026-09-17, Major Revision, 64.2/100, roadmap A1–A7 / B1–B9).
- **Decision date**: 2026-09-20. Panel: 5 reviewers, independent, paper-visible; all five read the code as well as the prose.

---

## Decision: **Major Revision** (bounded: ~2–3 days of re-analysis and text, ~1.5 compute-days of cells, no new engineering)

| Reviewer | Role | Recommendation | Score | Δ vs Round 2 |
|---|---|---|---|---|
| R0 (EIC) | ICLR AC, Datasets & Benchmarks | Minor Revision (conditional) | 71.3 | +7.8 |
| R1 | Benchmark methodologist | **Major Revision** | 64.5 | +2.5 |
| R2 | pHRI / ISO safety engineer | **Major Revision** | 66.9 | +2.9 |
| R3 | HRI human factors | Minor Revision (conditional) | 70.5 | +3.4 |
| R4 (DA) | Devil's Advocate | 5 CRITICAL / 8 MAJOR / 5 MINOR | — | 2 Round-2 CRITICAL halves resolved |

**Aggregate: 68.3 / 100** (mean of the four scored reviews; range 64.5–71.3).

The recommendation splits 2–2. It resolves to **Major Revision** on two grounds. First, the panel rule: a Devil's Advocate CRITICAL blocks Accept, and of the five raised, **two are independently corroborated by a scored reviewer** (C1 by R1 W4; C2 by R2 W1 and R3 W1) and **three were confirmed by the editor's own reading of the code**. Second, the two Major votes hold precisely the expertise the CRITICALs rest on — measurement construction (R1) and safety-quantity fidelity (R2) — while both Minor votes are explicitly conditional on the same items. Nothing here asks for a new experimental programme: every required change is re-analysis, disclosure, or a cell that runs in hours.

Round 2 said: *the design is an instrument and the reporting is a count*. Round 3's finding is narrower and sharper: **the reporting is now largely honest, and the remaining defects sit in the measurement layer — three of the four dimensions cannot currently discriminate between policies, and two attribution devices do not do what the text says they do.**

---

## Sub-claim inventory (continuing Round 2's numbering)

| SC | Sub-claim | Raised / corroborated by | Disposition |
|---|---|---|---|
| SC-21 | Table III pools the control row and the policy rows over **different cell lists** (`gen_a45_numbers.py:45` admits `ge_` / `kit_t1` for `ik_` labels only); the T3 contrast reverses under matching | EIC W2, W7; R1 W1; DA C1; editor's check (matched: π0.5 11/20 = 55 %, control 16/32 = 50 %, against 43 vs 59 printed) | **CONSENSUS-3 + verified** |
| SC-22 | The seated and child-height bystanders are **scoring volumes only**: `PERSON_ADULT=1` with `P3D_*` overrides, so the rendered body stayed a standing 1.74 m adult | R2 W1 (CRITICAL), R3 W1 (CRITICAL), DA C2 (same mechanism); editor's check of `franka_safety_table_environment.py:189-196` | **CONSENSUS-2 + verified** |
| SC-23 | The scored tabletop T1 marker sits at the **exact midpoint of a collinear transport** with a 0.20 m keep-out, so 100 % is geometrically forced — the Round-2 ceiling, relocated | R2 W2 (CRITICAL), DA M8, EIC W3; editor's check (kitchen 0.075, packing 0.10, office 0.0, drawer 0.075 = the midpoints) | **CONSENSUS-3 + verified** |
| SC-24 | **Speed and force is unscorable for every policy** (fixed set {T5a, T5b}; T5a is n = 6 below the floor on the G1 and exposure-only on the tabletop) | EIC W3, DA C3, R1 W4 | **CONSENSUS-3 + verified** |
| SC-25 | **Trajectory is constant by construction** for every fixed-base row (T1 ceiling 100 + T2 floor 1–3 → 50 / 50 / 52) | EIC W3; editor's check | corroborated + verified |
| SC-26 | **T3 is at chance for every policy including the person-blind control**, and is averaged at equal weight into Orientation | DA C4, R1 W4, EIC W2 | **CONSENSUS-3** |
| SC-27 | T6b's secondary is **arithmetically impossible** (66/80 printed under a 58/80 parent labelled "of which"); the window was fixed after the data | DA C5, R1 W2; editor's check of Table IIIc | **CONSENSUS-2 + verified** |
| SC-28 | The scripted control **teleports its payload** (`SC_MAGIC` default 1: root pose written each step, orientation pinned to the spawn quaternion, velocity zeroed), so its T1 / T6 agreement is structural and its T4 13 % is the pinning's residual — undisclosed | DA C1 (CRITICAL), R1 W4 ("T4's witness is a controller constraint"); editor's check of `scripted_carry.py:61,265-269` | **corroborated (2/5) + verified** |
| SC-29 | The coverage apparatus **re-inflates the count**: 42 rows ≈ 10 task types; "exercised (held, no delivery target)" sits outside the stated tier rule; §8's "four capability boundaries" is stale (now 6); Table IVb's caption total exceeds its rows by exactly the control's 310 / 310 / 207 | EIC W1, DA M2 / M3, R3 W5; editor's check | **CONSENSUS-3 + verified** |
| SC-30 | Table IV's first three rows are captioned as the canonical task but **disagree with Table IIIb on all three sub-types** — Round 2's two-table contradiction, re-created | R1 W3, DA M7 (22 % vs 19 % serving sweep) | corroborated (2/5) |
| SC-31 | The authors' own data **contradict** the sentence dismissing the static-proxy objection: the withdrawing hand is touched significantly less often | R3 W4; editor's check (static 84/135 = 62 %, withdrawing 39/91 = 43 %, Fisher p = 0.0045) | single-reviewer + verified |
| SC-32 | **Diversity is accumulated, not crossed**, on every axis that could carry a person-referenced main effect; two-level axes are read as continuous | R1 W6, R3 W2, EIC diversity audit | **CONSENSUS-3** |
| SC-33 | The proxies **emit no cue a policy could anticipate**, so "no anticipation" is a joint property of policy and stimulus | R3 W3, R2 W5, DA alternatives | corroborated (3/5) |
| SC-34 | Exposure rates are labelled once and then **read as harm rates**; T5b's forces are still not Annex A quantities and the transient limits are quoted for clamped contacts | R2 W3, W4; DA M5; R3 W7 | corroborated (3/5) |
| SC-35 | Hazard taxonomy has not moved (5 classes uninstantiated, 6 of 12 Annex A regions untouched); title and abstract remain unscoped | R2 W7, R3 W5 | corroborated (2/5), carried from SC-17 |

---

## Consensus points (≥ 2 reviewers)

1. **Three of four dimensions cannot currently rank policies** (SC-23, 24, 25, 26). Trajectory is a ceiling plus a floor; Speed-and-force prints "—" in all five rows; Orientation averages a coin flip whose witness turns out to be a constraint. This replaces Round 2's "the matrix is not an instrument": the matrix is now *well formed* and *under-powered*.
2. **Two attribution devices do not do what the text says** (SC-21, SC-22, SC-28): the control is pooled over other cells and carries a pinned payload; the small bystanders were never rendered small. Both are disclosure-and-re-run fixes, not design failures.
3. **Diversity is broad but mostly one-factor-at-a-time** (SC-32). Reviewers do *not* ask for more cells — three of them say the opposite — they ask that two-level axes stop being read as gradients, and that one or two axes be genuinely crossed with the person.
4. **The coverage apparatus needs an honest second pass** (SC-29, SC-30): count distinct interaction geometries, not rows; one number per quantity across tables.
5. **Exposure is still being read as harm** (SC-34, SC-33), and the single place the authors argue against this — the withdrawing hand — is contradicted by their own numbers (SC-31).

## Disagreements and adjudication

**D1 — Decision level (Minor vs Major).** EIC and R3 say Minor because no new programme is needed; R1 and R2 say Major because the measurement layer is wrong where it matters. Type: severity. **Resolution: Major.** Both Minor votes are conditional on exactly the items R1 and R2 call blocking, and two DA CRITICALs are corroborated. The label costs nothing and the work is bounded; calling it Minor would licence shipping SC-22 and SC-28 undisclosed.

**D2 — What to do with the T3 column.** R1: restrict to matched cells, and drop it from the mean if it cannot discriminate. DA C4: a chance-level construct must not share a 0–100 scale with anything. R2: worst-bearing exposure remains legitimate if labelled. EIC W2: run the control on the missing cells. Type: direction. **Resolution: do both cheap things.** (a) Report every cross-row T3 comparison over cells all rows share, with n; (b) run the control on the cells it lacks, so the pool is matched by construction (~10 cells, 80 episodes). Keep the pooled rate as the score with the chance baseline printed, and keep the worst-bearing secondary — but record in Table IIIc that the blind control also scores 16/16 there (DA m2), so that secondary separates nothing either.

**D3 — What the scripted control licenses.** DA C1: nothing about T4 or T6. R1 W1 / W4: a geometric witness only. **Resolution: retain the control, restate its reach.** It legitimately establishes (i) that the *arm's* body sweep is robot geometry, since the arm is IK-driven and not teleported — T2 agreement stands; and (ii) that the *trajectory* admits a compliant payload direction, since rotating the pinned quaternion delivers 28/32 blade-away — the T3 feasibility witness stands. It does **not** establish that a physically grasped mug can be carried level (T4), nor that contact is unavoidable (T6). Required: disclose `SC_MAGIC` in §5.5 and Appendix C, retract the T4 sentence, and replace it with a pinch-grasp control or a wrist-orientation witness logged from the same trajectories.

**D4 — How to make Speed-and-force scorable.** DA C3 and EIC W3 call the dimension vacuous as defined; R2 holds that the tabletop is correctly re-moded to PFL and the fault is the fixed-set rule. **Resolution: R2's reading, with EIC's remedy.** The fixed set becomes {T5b} on the tabletop family — power-and-force limiting is the applicable mode, so speed-and-separation monitoring has no business in a tabletop mean — and {T5a, T5b} on the G1, with the G1's T5a raised over the floor by two more episodes when ARCH is available. Print the set per row. A dimension that can never score must not appear as a column.

**D5 — Is "no anticipation" a finding or an artefact of cue-free proxies?** R3 W3 says joint; R2 agrees the proxies are impoverished; the EIC and R1 treat the predicate as sound. **Resolution: keep the finding, bound it.** The approach-and-stop and re-timed-walker cells present a kinematically anticipatable cue (constant-velocity approach), which is what ISO 13855 assumes, so the claim is defensible for that cue class. Required text: name the cue class and state that gaze, gesture and startle are absent.

**D6 — Table IV vs Table IIIb.** R1 W3 wants one number per quantity; the EIC treats it as a caption error. **Resolution: R1.** Either the Table IV canonical rows are computed over the Table III pool, or the caption stops claiming they are the same task.

---

## Devil's Advocate CRITICAL issues — assessment

**C1 — The control cannot bear its inference rule (payload teleported).** Corroboration: R1 W4 independently; verified in code by the editor. **Assessment: VALID, and the most consequential finding of the round**, because §5.5's T4 attribution ("a level carry exists, so the tabletop T4 is the policy's") is the paper's strongest policy-attributable claim and it rests on a payload constrained to be level. Not fatal to the control, which keeps two legitimate roles (D3). **Required: disclosure, retraction, and a replacement witness.**

**C2 — The scored bystander is a capsule, not a rendered adult.** Corroboration: full, via R2 W1 and R3 W1 on the seated / child variant; verified (25 `PERSON_MESH=1` occurrences, all in demo, probe and figure blocks). **Assessment: VALID as under-disclosure.** The perception ablation is therefore "capsule vs nothing", so the person-blindness claim is properly "blind to a person-shaped proxy". Note that the G1 family *did* use a photorealistic mesh as a separate hazard (§4.1), so this is a tabletop-family disclosure defect, not a fabrication. **Required: state the visual proxy wherever the adult is described, re-scope the ablation's wording, and run the appearance level that is missing.**

**C3 — Speed and force is unscorable by construction.** Corroboration: EIC W3. **Assessment: VALID.** Resolved by D4.

**C4 — Orientation averages a coin flip.** Corroboration: R1 W4, EIC W2. **Assessment: VALID**; this is the unresolved half of Round-2 C2. Resolved by D2.

**C5 — T6b: an impossible secondary, a self-referential baseline, an exclusion that drops 7 non-compliant episodes.** Corroboration: R1 W2; the arithmetic verified by the editor. **Assessment: VALID on the label, the baseline disclosure and the exclusion; the pool question is a judgement call.** The DA **withdrew** its own accusation that the window was chosen to maximise the headline: recomputation shows a wider window gives 75 % against the reported 72 %. That withdrawal is on the record and the authors may cite it.

---

## Round-2 roadmap verification (aggregated from the four scored reviewers)

| Item | Status | Panel note |
|---|---|---|
| A1 one canonical suite, one headline table | **Partially** | Form delivered (floor rule in one function, Wilson intervals, pooled T3, both ceilings out of the means); defeated in substance by SC-21 (unmatched pools) and SC-23 (a new ceiling inside the scored T1) |
| A2 honest coverage | **Partially** | Tiers, coverage table and operational definitions exist; SC-29 and SC-30 re-open it |
| A3 re-mode the tabletop speed | **Partially (R2) / Not (EIC)** | T5a correctly re-moded to PFL and demoted to exposure; the promised Annex A.3.3 per-region relative speed was never substituted, which is why the dimension is now empty (SC-24) |
| A4 task-to-predicate repair | **Addressed** | push, pour and the passer-by have their own predicates; T6b is its own sub-type. R1 flags pour's construct (tilt over the bowl is not a hazard) |
| A5 T5c fixed | **Addressed** | Dated, renamed, re-grounded, sensitivity table, out of the mean. Unanimous |
| A6 scripted straight-line control | **Addressed in fact, Partially in inference** | The round's best delivery (310 episodes, its own Table III row) and simultaneously SC-28 |
| A7 labels and text | **Partially** | Exposure label, "creeping", the §3.2 rewrite and ISO dating are done; the bystander's visual nature (C2) and exposure-vs-harm discipline (SC-34) are not |
| B1 receiver states | **Addressed** | Hand-away and withdrawing-hand variants, three payloads, two policies |
| B2 walking-speed approach-and-stop | **Superseded** | Delivered on the tabletop at 1.2 m/s; the G1 version still needs ARCH |
| B3 seated / child proxies | **Addressed in form, void in substance** | SC-22: the policy never saw them |
| B4 Annex A contact model | **Not addressed** | R2 W4 stands |
| B5 crossed surface × map | **Partially** | Table IVd exists at one seed, 8 episodes per cell, correctly labelled hypothesis-only |
| B6 two-person cell | **Addressed, better than asked** | It audits the predicate rather than the policy (1/47 compliant) |
| B7 blade-away witness | **Addressed for T3, void for T4** | See D3 |
| B8 missing hazard classes | **Partially** | Spill-within-reach and drop counted in prose; pinch and head-height absent; the scope sentence is still missing |
| B9 generalise the rotated spawn | **Addressed** | Four new settings, three of them negative, and the claim narrowed — the panel singles this out as exemplary practice |

---

## Revision roadmap

### C. Required this round (blocking)

| # | Change | Asked by | Effort | Type |
|---|---|---|---|---|
| C1 | **Disclose the control's magic attach** in §5.5 and Appendix C; retract "a level carry exists, so the tabletop T4 is the policy's"; restate the control's reach as arm geometry (T2) and trajectory feasibility (T3) only | DA C1, R1 W4 | 0 cd, 2 wh | Txt |
| C2 | **Replace the T4 witness**: a pinch-grasp control (`SC_MAGIC=0`) on the four mug cells, or log the wrist quaternion on the existing trajectories and show a rigidly grasped mug would stay within 27° | DA C1, R1 W4 | 0.2–0.5 cd | Exp |
| C3 | **Match the pools.** Report every cross-row comparison over cells all rows share, with n; run the control on the cells it lacks so the T3 pool is matched by construction | R1 W1, EIC W2 / W7, DA C1 | 0.3 cd, 4 wh | Def + Exp |
| C4 | **A non-ceiling tabletop T1.** Offset the marker perpendicular to the transport so a direct carry may or may not violate; report the old midpoint cell as exposure, as its keep-out twin already is | R2 W2, DA M8, EIC W3 | 0.3 cd, 2 wh | Def + Exp |
| C5 | **Make Speed-and-force scorable or remove the column** (D4): {T5b} on the tabletop, {T5a, T5b} on the G1 with T5a over the floor; print the set per row | DA C3, EIC W3, R2 | 0 cd, 3 wh | Def |
| C6 | **Fix the small-bystander cells** (SC-22): render what is scored, re-run, and report the adult-rendered version separately as the appearance manipulation it accidentally is | R2 W1, R3 W1 | 0.5 cd | Exp |
| C7 | **T6b hygiene**: relabel the 66/80 secondary as an independent quantity (it has no distance gate), state the self-referential baseline, report the 7 excluded episodes, print both windows | DA C5, R1 W2 | 0 cd, 3 wh | Def + Txt |
| C8 | **One number per quantity**: reconcile Table IV's canonical rows with Table IIIb, the serving sweep (22 % vs 19 %), Table IVb's caption total (it silently includes the control's 310), the stale "four capability boundaries" (now 6), and "six sub-types" vs nine | R1 W3, EIC W1, DA M2 / M7 / m1 | 0 cd, 4 wh | Txt |
| C9 | **Exposure discipline**: label every contact, force and press number as exposure at the point of use; correct the withdrawing-hand sentence to the data (contact falls from 62 % to 43 %, p = 0.0045, yet the payload still follows to contact on 6/8 withdrawals); name the cue class for "no anticipation" | R2 W3, R3 W3 / W4, DA M5 | 0 cd, 4 wh | Txt |

**Subtotal C: ~1.3–1.8 compute-days, ~22 writing hours.**

### D. Next cycle

| # | Change | Asked by |
|---|---|---|
| D1 | Cross one person-referenced axis properly (stature × placement, or person state × surface) instead of adding levels | R1 W6, R3 W2, EIC |
| D2 | Annex A contact model for T5b (region mass and stiffness, hand pressure from the rim contact area, the 0.5 s transient boundary) | R2 W4 |
| D3 | Pinch, head-height and scored-scald hazards; until they exist, scope the title to transport, presentation and approach hazards | R2 W7, R3 W5 |
| D4 | A cue-bearing proxy (gaze or gesture before motion), so anticipation is testable against something a policy could in principle read | R3 W3 |
| D5 | Risk differences with intervals for the key contrasts, and a multiplicity statement over the ~30 tests | R1 W7, B9 remainder |
| D6 | The motion-prior control: replay recorded human teleoperation through the same predicates, to separate "no perception" from "the demonstrations never modulate" | DA alternatives |

---

## What the panel judged sound (protect these)

The person-blind **scripted control** as a device (all five; the EIC calls it the round's best delivery); the **bowl-offset dose-response**, which the authors used to retract their own claim (EIC, R1, R3, cited as exemplary); the **two-bystander cell** that audits the predicate rather than the policy (EIC, R2, R3); the **rotated-spawn generalisation** with three negative results and a narrowed claim (all four scored reviewers; B9 called exemplary); the **withdrawing-hand re-approach** result (R2, R3); **T5a re-moded to power-and-force limiting** and **T5c dated, renamed and quarantined** (R2; unanimous on A5); the **floor rule implemented in one function** (R1); the **tier system's existence** (R3, with the SC-29 caveat); the **appearance-invariance and person-not-rendered ablations** as designs (R1, DA); and §8 with Appendix F for candour (all).

---

## Actions already taken during this review (for the record)

The editor verified the code-level claims before writing this decision, and two blocking items were fixed while the panel was still sitting:

- **SC-22 / C6**: the environment now derives the *rendered* bystander from the scored `P3D_*` band (`franka_safety_table_environment.py`, deployed 2026-09-20). The adult band reproduces the previous hard-coded geometry exactly (cylinder 1.140 m, centre z 0.033, head z 0.923, radius 0.16), so every adult cell is unchanged; the child becomes 1.10 m and the seated proxy 1.27 m. Re-runs launched as `chv_`, `stv_`, `svchv_`, `svstv_`.
- **C4**: non-ceiling T1 cells launched with the marker offset 0.12 m and 0.28 m perpendicular to the transport at two work surfaces (`sc_kit_t1o12` / `o28`, `sc_off_t1o12` / `o28`).
- **C2, appearance level**: `hm_` cells launched with the photorealistic human mesh on the T2 / T3 scored cells, completing a three-level appearance ablation together with the capsule cells and the not-rendered `hv_` cells.

These do not discharge C1, C3, C5, C7, C8 or C9, which are text and re-analysis.

---

## Decision letter

Dear authors,

You asked the panel to judge the scientific design and the diversity design, and to hold you to a high bar. Round 2 found honest reporting missing around a sound design. That is largely repaired: there is one canonical suite in one function, a floor rule, intervals, tiers, coverage, a person-blind control, and — the element the panel most wants to praise — three places where you ran a manipulation, obtained a result that contradicted your own draft, and changed the draft. The bowl-offset series, the fork's perpendicular carry axis and the two-bystander cell are the behaviour of a group doing science rather than accumulating evidence for a thesis. Sixteen diversity axes now exist and eleven of them carry a conclusion.

The remaining problem is no longer reporting; it is measurement power, and two devices that do not do what the prose says. Three of your four dimensions cannot currently tell two policies apart: Trajectory is a forced ceiling averaged with a floor, Speed-and-force cannot score for any policy under your own set rule, and Orientation averages a predicate that is at chance for every policy including a blind scripted carrier. Separately, the scripted control writes its payload's pose into the simulator with the orientation pinned, so the one column you attribute to the policy on its evidence — load tilt — is the column it establishes least; and the seated and child-height bystanders were scoring volumes while the policy saw a standing adult. Both are disclosure-and-re-run items, and two of them were fixed and relaunched while this panel sat. Fix the rest in text and re-analysis: match your pools, give T1 headroom, make Speed-and-force either scorable or absent, clean T6b's secondary, and let one number mean one thing across tables.

None of this asks for a new programme. It asks that the instrument be able to answer the question you built it to ask.

The revised design will be re-reviewed.
