# Editorial Decision — review2 (task design and diversity design)

- **Object under review**: design_note.md (2026-09-16/18), tables.txt (2026-09-18), manuscript §3–§5, §8, App. E.8
- **Scope**: task design and diversity design of the four-dimension execution-phase safety benchmark; not the paper as a whole
- **Decision date**: 2026-09-17 · **Round**: 2 (post labmate review)

---

## Decision: **Major Revision**

| Reviewer | Role | Recommendation | Confidence | Score |
|---|---|---|---|---|
| R0 (EIC) | ICLR area chair, embodied AI / benchmarks | Major Revision | 4 | 63.5 |
| R1 | Benchmark methodologist | Major Revision | 4 | 62.0 |
| R2 | pHRI / ISO safety engineer | Major Revision | 4 | 64.0 |
| R3 | HRI human-factors psychologist | Major Revision | 4 | 67.1 |
| R4 (DA) | Devil's Advocate | 2 CRITICAL / 8 MAJOR / 5 MINOR | — | (no score) |

**Aggregate score: 64.2 / 100** (mean of the four scored reviews; range 62–67.1). All four scored reviewers recommend Major Revision; R3's numeric lands at the Minor/Major boundary but recommends Major because the fixes change how T3, T6 and the press durations are read. Both DA CRITICAL issues (C1, C2) are unresolved, and C2 is corroborated by three of the four reviewers, which rules out Accept under the panel rule. This is a Major Revision of the *aggregation, inclusion and naming rules* of the suite, not of the experimental programme: every reviewer judged the underlying experiments worth keeping.

---

## Sub-claim inventory (Step 1b, compressed)

| SC | Sub-claim | Raised / corroborated by | Disposition |
|---|---|---|---|
| SC-1 | Saturated, scene-set sub-types (midpoint-T1 22/22, T5a 98–100 %) enter the dimension mean at equal weight, so the matrix cannot rank policies | EIC W3, R1 W1, R2 W1, R3 (§5.3 caption note); DA C2, M2, M4 | CONSENSUS-4 |
| SC-2 | Suite is not fixed: Table 1 and Table III give different headlines from the same data | EIC W4, R1 W2, R2 (Results); DA C2 | CONSENSUS-3 (R3 silent) |
| SC-3 | Headline T3 = worst single bearing (100) while the pooled rate is ~50 %, which is chance under a half-space predicate | EIC W3, R1 W3, R2 (Results); DA C2, m4 | SPLIT on remedy → D2 |
| SC-4 | Task count overstated: "13 tasks" vs 6 scored; door (0/8), drawer (0 delivered), handover (2/48) counted as tasks | EIC W1, R1 W4, R2 W5, R3 (Methodology); DA M1 | CONSENSUS-4 |
| SC-5 | Task-to-predicate mismatch: push, pour, passer-by, door assigned to a dimension by a mechanism no predicate scores | EIC W2, R1 (push-as-lifted, passer-by 0/25), R2 W5 (push payload exit unscored); DA M6 | CONSENSUS-3 (R3 silent) |
| SC-6 | n ≤ 6 cells printed as percentages; no Wilson CIs in Table III | EIC (W3, note to R1), R1 W2 / Sampling, R3 (Evidence); DA C2 | CONSENSUS-3 (R2 silent) |
| SC-7 | Equal-weight mean over row-dependent sub-type sets has no stated justification and no risk meaning | EIC W3, R1 W2, R2 (Results); DA M4 | CONSENSUS-3 (R3 silent) |
| SC-8 | T5c: post hoc, "six vs seven" text, 15 vs 41 episodes, double-filed under two columns, wrong ISO clause | R1 W5, R2 W3, EIC (minor), R3 (layout); DA M3 | CONSENSUS-4 |
| SC-9 | T5a applies SSM to a table-side arm where PFL is the applicable mode; the 100 % is a category error | R2 W1 | single-reviewer, conf. 4, domain expertise → adopted (D1) |
| SC-10 | T5b forces come from an infinite-mass capsule, not the Annex A spring–mass quantity | R2 W2 | single-reviewer, conf. 4 → required, next cycle |
| SC-11 | Human proxy is intent-less and non-reacting; all contact rates are exposure rates, not harm rates | R3 W1, R2 (Methodology: static, no arms); DA M7 | corroborated (2/4) |
| SC-12 | Crossing person at 0.06 m/s is not walking; fast runs are confounded by grasp knock-out | R3 W2, R2 (T6 comment) | corroborated → D3 |
| SC-13 | Standing 1.74 m proxy with forearm on the table; no seated or child-height person | R3 W3, R2 W5 | corroborated (2/4) |
| SC-14 | Six environment maps are cosmetic: varied on one cell, no safety predicate responds | EIC W1, R1 (scene accumulation), R2 (perception variable), R3 W4; DA M5 | CONSENSUS-4 |
| SC-15 | Dynamics rests on one predicate (T6 contact) and, per family, essentially one task | EIC W5, R2 W5; DA C1 | corroborated (2/4) |
| SC-16 | Denominator drift: G1 conditions on completion, tabletop on "carried"; contradicts §4.2 | R1 W4, R3 (minor, handover denominators) | corroborated (2/4) |
| SC-17 | Hazard classes a kitchen risk assessment lists first (pinch, scald, drop, head height) are absent | R2 W5 | single-reviewer, conf. 4 → scope text now, tasks next cycle |
| SC-18 | Operator standards (ISO 10218 / TS 15066) applied to untrained bystanders; ISO 13482 not cited | R3 W5, R2 W5 | corroborated → text |
| SC-19 | "π0.5 · serving" is a task row in a policy matrix | EIC (minor); DA m3 | corroborated → text |
| SC-20 | T3 witness is four naturally occurring carries; T2 / T4 have no witness | R1 (Methodology) | single-reviewer → next cycle |

---

## Consensus points (≥ 2 reviewers)

1. **The headline matrix is not yet an instrument** (SC-1, SC-2, SC-7; EIC, R1, R2, DA; R3 on the caption). Two columns are ceilings by construction, the mean runs over whichever sub-types a row happens to have, and two pooling rules give two headlines. This is the panel's central finding and the highest-value fix; it costs no compute.
2. **The suite is smaller than its count** (SC-4, SC-14; all four + DA). Six scored tasks, one policy on most of them, maps varied on one cell. Reviewers do not ask for more cells; they ask for honest naming: exercised / defined-but-unscorable / planned, with N.
3. **Several tasks do not measure what the design note says they add** (SC-5; EIC, R1, R2, DA). Push, pour, passer-by and door are assigned to dimensions by mechanisms with no predicate. Either score the mechanism or drop the task from that row.
4. **T5c must be reported as what it is** (SC-8; all four + DA): adopted after the data, mis-cited to ISO 10218-1's manual-mode TCP limit, inconsistent counts, double-filed. Nobody asks for its removal; R1, R2 and the EIC value the observation.
5. **The person has no state** (SC-11, SC-12, SC-13; R2, R3, DA). Static, collider-less, wrong height, creeping at 0.06 m/s. The rates are exposure rates and should be labelled so now; a person with a state is next-cycle work.
6. **Small cells need intervals or counts** (SC-6; EIC, R1, R3, DA).

## Disagreements and adjudication

**D1 — What to do with T5a on the tabletop.** EIC: drop scene-set sub-types from the mean or report them as "scene exposure". R1: report the present/absent speed ratio, or the envelope at a calibrated placement with blind rate < 100 %. R2: SSM is the wrong collaborative mode for a table-side arm; score SSM on the G1 only and replace tabletop T5a with Annex A.3.3 relative speed (PFL). Type: direction difference. **Resolution: adopt R2 for the scoring criterion (domain expertise), and R1's present/absent ratio as a separate, unscored "no modulation" behavioural row (R1 and R2 both propose this row).** The three remedies are compatible; R2's is the one a certifier will check.

**D2 — T3 headline.** R2: worst-bearing exposure is legitimate in safety practice if labelled. R1, DA, EIC: the pooled rate with the 50 % chance baseline stated. Type: severity/direction. **Resolution: headline = pooled rate over both sides with the split shown and the 50 % baseline in Table II; worst-bearing reported as a labelled secondary.** Evidence favours R1 (a chance-level construct cannot share a 0–100 scale with T1 / T6); R2's labelling concern is met by the secondary.

**D3 — T6 crossing speed.** R2: let the 0.3–1.2 m/s runs carry the row (matches ISO 13855's 1.6 m/s). R3: approach-and-stop at 1.0–1.3 m/s, stopping at 0.5 m, to avoid the knock-out confound (16/23). **Resolution: R3's design, at R2's speeds.** The knock-out is a different event (the design note itself says so); approach-and-stop tests anticipation without it. Relabel 0.06 m/s as "creeping approach" now.

**D4 — Are the four dimensions one latent?** DA C1 vs the EIC / R3 view that the per-dimension "why it is not collision avoidance" arguments are sound. See the DA section below.

**D5 — Human-proxy severity.** R3 rates intent-less proxies Major; EIC and R1 are silent. Within R3's expertise and cheap to address; **weighted as Major but scheduled next cycle**, because its labelling half is a text change and its experimental half does not gate the merge.

## Devil's Advocate CRITICAL issues

**C1 — "Four parallel, independent, separately scored dimensions" is not supported; a single latent (person-blindness) explains every column.** Corroboration: partial. EIC W3 agrees the independence "splits" rest on weak proxies (rigid-box T4, fixed-arm T2); R2 notes the same episodes feed several predicates; R3 independently states that "the policies show no person-conditioned behaviour at all" is the real headline. No reviewer corroborates that this makes the dimensions worthless. **Assessment: valid against the *wording* ("independent", "each has its own tasks"), not against the design.** Dimensions are distinct predicates on distinct physical quantities scored on shared episodes; that is normal for a benchmark and should be said plainly. The "several tasks each" clause is genuinely false for T1 and Dynamics (SC-4, SC-15). **Required response:** rewrite §3.2's independence claim as "distinct quantities, shared episodes"; state person-blindness as the shared finding and the dimensions as where it manifests; run the DA's cheapest disambiguator, a scripted straight-line carry control (DA alt. 4), which shows which columns are scene geometry.

**C2 — Table III cells are not policy measurements** (worst-bearing T3, ceilings averaged with n ≤ 4 cells, two headline tables). Corroboration: **full** (EIC W3 / W4, R1 W1–W3, R2 Results). **Assessment: valid.** Resolved by roadmap item A1.

---

## Decision letter

Dear authors,

The panel read the design note, the generated tables and §3–§5 / §8 / E.8 for one question: is the task suite a designed instrument or a count of variants? The answer is that the *design* is an instrument and the *reporting* is a count. Every reviewer, including the Devil's Advocate, singled out the same elements as sound: the success-conditioned definition of execution-phase safety (§3.1); the per-dimension "why it is not collision avoidance" test; the rotated-spawn T3 manipulation, which all five call the strongest single design element; the matched present/absent T5a design; the feasibility-witness attribution rule; the interaction-geometry battery; the T2 threshold curve with contact count; serving, the reaching hand and the 3 s withdrawal witness; the correct Annex A region values and spill angle; the T6b trapping observation; and the candour of §8. Do not tear these down. One caveat on the geometry battery (DA M5): T4 has no person term, so "tilt present at every placement" is expected, not a finding; the battery's value is in T2 and T3.

What must change is how cells become a matrix. Two columns are ceilings by construction, the dimension mean is row-dependent, the T3 headline is the worst bearing of a chance-level construct, n = 2–6 cells print as percentages, and two tables give two headlines. Independently, the suite's size is overstated (six scored tasks, not thirteen; maps varied on one cell; two policies on two tasks), four tasks are assigned to dimensions by mechanisms no predicate scores, T5c is mis-cited and double-filed, tabletop T5a applies the wrong collaborative mode, and the human proxy has no state, so all rates are exposure rates. None of this needs new episodes at the level that gates the merge with the labmate's ICLR paper: it needs a fixed canonical suite, one aggregation rule, honest coverage tables and re-scoring from existing logs. The experiments the reviewers ask for (receiver states, walking-speed approach, seated and child proxies, Annex A contact model, pinch / scald / drop hazards) are next-cycle work and are the natural content of your own paper.

The revised design will be re-reviewed.

---

## Revision roadmap

Effort assumes one shared GPU box (Franka env step 1/15 s), Isaac Lab-Arena with the placement, spawn-rotation, proxy and environment-map knobs of design_note.md, and existing per-step trajectory logs. "cd" = compute-days, "wh" = writing / scripting hours. Type: **Def** = design or definition change, **Exp** = new experiment, **Txt** = text.

### A. Must do before the labmate's ICLR merge (highest value per day)

| # | Change | Asked by | Effort | Type |
|---|---|---|---|---|
| A1 | **One canonical suite, one headline table.** Declare the cells, seeds and sub-type set per dimension; drop midpoint-T1 and tabletop T5a from means (rendered-marker T1 becomes the tabletop T1; T5a becomes "scene exposure"); report dimensions as vectors, or as a mean over a fixed set with the cell blank when a member is unscorable; min-n rule (n < 10 prints as a count); Wilson CIs and n in every cell; pooled T3 with the split and the 50 % baseline; remove the serving row from the policy matrix; move "everything pooled" to an appendix; reconcile or delete Table 1. | SC-1, 2, 3, 6, 7, 19: EIC, R1, R2, R3, DA C2 | 0 cd, 12–16 wh (re-tabulate from fr_summary.json) | Def + Txt |
| A2 | **Honest coverage.** Named fixed task list; coverage matrix task × surface × map × policy with N; three tiers: exercised (≥ 8 delivered or ≥ 50 % delivered), defined-but-unscorable (door, drawer, handover, island), planned (cut, wipe); operational definitions of "carried" and "delivered" and one denominator per predicate across families; capability-boundary table reporting completion only; "6 environment maps" out of the headline and reported as a one-cell robustness check; only scored tasks counted in the abstract. | SC-4, 14, 16: EIC W1, R1 W4, R2 W5, R3, DA M1, M5 | 0 cd, 6–8 wh | Def + Txt |
| A3 | **Re-mode tabletop speed.** T5a (SSM) scored on the G1 only; on the tabletop score Annex A.3.3 per-region relative speed at contact (PFL) from existing logs; present/absent "no modulation" as a separate unscored behavioural row; re-cite T2's 0.10 m as "of the order of Z_d + Z_r (ISO 13855:2024; ISO/TS 15066 §5.5.4.2.3)", not "the Z of the standard". | SC-9, D1: R2 W1, W4; R1 W1; EIC W3 | 0 cd, 6–8 wh | Def |
| A4 | **Task-to-predicate repair from existing logs.** Add: push → payload leaves the surface toward the person; pour → tilt location relative to the bowl rim; passer-by → speed change vs time-varying separation (a deceleration-before-d0 anticipation predicate, which also gives Dynamics a second, non-contact sub-type and scores handover on it); report T6b as its own sub-type. Any task whose mechanism cannot be scored from logs leaves that dimension's row. | SC-5, 15: EIC W2, W5; R1; R2 W5; DA M6, C1 | 0–0.5 cd (re-score; passer-by may need ~32 re-runs with logging), 8–12 wh | Def |
| A5 | **T5c fixed.** State the adoption date and post-hoc status in §3.3; "seven" everywhere; one column for tool episodes; reconcile 15/41, 0.52/0.50, 0.23/0.19; sensitivity over threshold 0.15–0.50 m/s × radius 0.3–0.7 m; rename "tool-end speed within reach"; ground in Haddadin et al. 2010 / Annex A.3.3 v_rel,max, not ISO 10218-1 §5.6; state that sharp tools fall under hazard elimination (ISO 12100 §6.2); keep it out of the headline mean until the sensitivity is shown. | SC-8: R1 W5, R2 W3, DA M3, EIC | 0 cd, 4–6 wh | Def + Txt |
| A6 | **Scripted straight-line carry control.** One scripted (IK) direct carry on the dining-table pick-and-place cell and the five geometry placements, scored on every predicate. Shows which columns any direct carrier scores 100 on; directly answers DA C1 / C2 and settles SC-1 empirically. | DA alt. 4, C1; supports EIC W3, R1 W1 | 1–2 cd incl. controller scripting | Exp (cheap) |
| A7 | **Labels and text.** Table III caption: "person proxies are static and non-reacting; rates are exposure rates"; 0.06 m/s → "creeping approach"; §3.2 independence rewritten as "distinct quantities, shared episodes" with person-blindness named as the shared finding; ISO 13482 / operator-vs-bystander paragraph with the direction of bias; ISO editions and clauses dated; "simulated protective stop"; fix Table 1 G1 orientation "0 % (20/20 T3)"; fork-at-boundary note (DA m4); tonemapped outdoor maps stated; dates aligned; E.8 spacing; the design note's "what this design still lacks" moved verbatim into §8; add Ortenzi 2021, Strabala 2013, Haddadin 2009 / 2010, Marvel & Norcross 2017. | SC-11, 18; all reviewers' minors; DA m1–m5 | 0 cd, 6–8 wh | Txt |

**Subtotal A: 1–2.5 compute-days, ~45–60 writing / scripting hours (about one working week).** A1–A2 alone are what the labmate's merge needs: a fixed, honestly sized task list with one scoring rule.

### B. Next cycle (your own paper)

| # | Change | Asked by | Effort | Type |
|---|---|---|---|---|
| B1 | Two static receiver states (palm-up / attending vs hand-down / away), paired seeds; reactive proxy withdrawing on first contact; T3 and T6 by state; define what the receiving hand does and what "delivered" means for handover. | R3 W1, R2 (handover intent), R1 W4, DA M7 | 0.5–1 cd + 4 wh proxy scripting | Exp |
| B2 | G1 approach-and-stop person at 1.0–1.3 m/s stopping at 0.5 m; T6 re-scored on the anticipation predicate of A4. | R3 W2, R2, D3 | 1–2 cd (G1 pipeline) | Exp |
| B3 | Seated adult (eye height ≈ 1.2 m) and child-height (≈ 1.1 m) proxies at the same five placements; T2 contact and T5c with the head at tool height; capsule with shoulders and arms. | R3 W3, R2 W5, R2 (Methodology) | 1 cd per policy | Exp |
| B4 | T5b Annex A contact model: region-specific mass / stiffness (Table A.3) or post-processing through the A.3.3 energy model; hand pressure from rim contact area; 0.5 s transient boundary; re-run the reaching-hand cells. | R2 W2 | 2–3 days engineering + 0.5 cd | Def + Exp |
| B5 | Crossed scene design 2 surfaces × 3 maps × 1 task × 16 eps (96 eps) to test a surface / map effect instead of accumulating it. | R1 (Methodology) | 1 cd | Exp |
| B6 | Two-person T3 cell (left and right, unsatisfiable by lucky spawn); person arriving at the bin mid-carry. | R3 W4 | 0.5 cd | Exp |
| B7 | Scripted upright / blade-away carry as a genuine T3 / T4 witness; witness row per sub-type in Table III. | R1 (Methodology), EIC S5 | 0.5 cd + 3 wh | Exp |
| B8 | Missing hazard classes: drawer / door pinch with a hand in the gap, scored spill-within-reach (T4 ∧ reach), scored drop event, head-height exposure. Until then, scope the title and abstract to transport, presentation and approach hazards. | R2 W5 | assets + predicates, 3–5 days; scoping text 1 wh now | Exp / Txt |
| B9 | Generalise the rotated-spawn manipulation to every hazardous object and task (the DA's suggested causal spine); risk differences with CIs for the key contrasts; list the number of uncorrected Fisher tests. | DA (observation), R1 (Analysis) | 1–2 cd + 4 wh | Exp + Txt |

---

## What the reviewers judged SOUND (keep)

- §3.1 success-conditioned definition of execution-phase safety (DA, R3, EIC).
- Per-dimension "why it is not collision avoidance" argument (EIC S1, R2 S1, R3 S1).
- Rotated-spawn T3 causal test and its replication in the geometry battery (EIC S2, R1 S2, R2, R3 S2, DA).
- Matched present / absent T5a design; the separation of the scene-set envelope from policy-attributable no-slowing (R1 S3; R2 W1 names it the surviving finding).
- Feasibility-witness attribution rule (EIC S5, R1 S4, DA).
- Interaction-geometry battery as real exposure variation, for T2 and T3 (EIC S3, R2 S4, R3 S2; DA M5 caveat on T4 accepted).
- T2 threshold curve, contact count and the retracted 3 % → 53 % (R1 S4, R2 S2, DA).
- Serving beside a seated person, the reaching hand, the 3 s withdrawal witness (EIC S2, R3 S3).
- Annex A region values and the 14–27° spill angle (R2 S3).
- T6b trapping / release as a distinct failure (R2 S5).
- T5c as a sub-type that emerged from a task (EIC S4), once reported per A5.
- §8 and the design note's "what this design still lacks" (all).

## Response letter

Respond item by item to A1–A7 and B1–B9 using `templates/revision_response_template.md`; for each DA CRITICAL, include the authors' position even where you disagree with the DA. Recommended deadline for the Part A revision: one working week; Part B: next cycle.
