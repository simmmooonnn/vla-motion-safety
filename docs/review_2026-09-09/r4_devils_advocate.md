## Devil's Advocate Review — "Execution-Phase Safety for Embodied VLA Agents" (draft v0.24)

**Credit where due.** The reporting is unusually candid (§5.2, §8); the π0.5 on-path/off-path split (§5.9) is clean and powered; and a live-pose reactive shield still failing against a crossing person (§5.7) is non-obvious.

### Strongest Counter-Argument

This paper re-packages obstacle avoidance as a "third axis" and then supplies evidence that mostly measures its own scene construction. The formal definition (§3.1, ∀t ψ_h(φ_h(s_t))) is the ordinary safe-set / state-constraint specification that CBFs [9], shields [10] and SafeVLA-Bench's STL clauses [27] already use; §2 concedes that trajectory-level VLA safety, humans in scene, moving humans, handover orientation and load stability are all taken. What remains is a five-conjunct "intersection", and its load-bearing conjunct — a *carried hazard past a passive bystander* — rests on one completing trajectory (Table III, person cell 1/1). Every headline defect is guaranteed by design: the T1 keep-out sits on the straight-line path (§5.9, "geometric midpoint"); the T6 crossing is "tuned to intersect" (§5.7); the T4 bystander stands within reach of the pick (§5.5); and the T3a envelope gives d₀ = 0.94 m in a 1.9 m corridor with the person mid-path, so SSM compliance requires the robot to *stop* — "6/6 violate" restates "6/6 completed the task" (§5.3). Any policy that executes the demonstrated motion then violates; a flawless teleoperator would too. The paper therefore shows that imitation-trained VLAs follow the demonstrated path and do not replan — known, and already reported for GR00T, π0 and π0.5 by [24], [27]. The "behavioral safety competence" hypothesis adds nothing falsifiable: its prediction ("needs an external layer") is what every certified robot already does and what VLSA [22] — in the bibliography but never cited in the text — already ships for VLAs. §8 concedes every link (one task-tuned policy, underpowered ablations, oracle shield, proxy metrics), leaving no positive claim beyond "our checkpoint walks straight."

### Issue List

#### CRITICAL
| # | Dimension | Issue Description | Location | Field-Norm Boundary | Evidence-Crossing Rationale |
|---|---|---|---|---|---|
| C1 | Data–conclusion mismatch | Abstract/§6 claim rendering the hazard produces "no detectable change in behavior", yet Table IV shows it does: pooled completion 10/35 blind vs 20/36 hidden (p≈0.02); person cell 1/11 vs 6/12. Aborting when a hazard is visible is the policy's one observable reaction, and success-conditioning discards those episodes; "non-traversal, not detour" does not exclude a freeze. | Abstract; §5.2 Table IV; §6 | — (logic) | — |
| C2 | Foundation collapse | The novelty claim's core cell — hazardous payload past a passive bystander (§2 (ii), §3.3) — has n=1 completing carry. The pooled 10/10 is stove/strip (plain obstacle avoidance); T2/T4/T6 carry a benign box. The paper's unique cell is unmeasured. | §2, §3.3, Table III | — | — |
| C3 | Stronger counter-narrative | The T4 "3-D lesson" is a threshold change: horizontal violation = link origin < 0.10 m from the axis; capsule "contact" = origin < 0.16 m. Loosening 0.10→0.16 m flips π0.5 3%→53%; GR00T's pooled 25% was never re-scored at 0.16 m. The metric changed after π0.5 looked safe; the cross-policy comparison is now metric-unmatched. | §5.5, §5.9, §8 | — | — |

#### MAJOR
| # | Dimension | Issue Description | Location | Field-Norm Boundary | Evidence-Crossing Rationale |
|---|---|---|---|---|---|
| M1 | Logic chain | "Not promptable" (§6) needs a language-following control. The checkpoint is a task-specific fine-tune [13] at 29% success; if it cannot follow *any* novel spatial instruction ("place it on the left"), the safety-prompt null is a language null. | §5.2, §6, [13] | — | — |
| M2 | Evidence gap | Path attribution to GR00T's `navigate_cmd` is asserted from code reading; commands are not logged (§5.1 admits). A vision-blind decoupled WBC is itself an architectural limit, so the "competence" may be unlearnable here by construction — a different claim. | §5.1 | — | — |
| M3 | Cherry-picking | T3a: after the modulation test returned null, scoring switched to an envelope with walking-human parameters (v_h = 1.6 m/s) applied to a *stationary* proxy, guaranteeing violation. T5's "measured null" is a rigid box (§8: "nearly trivial"); the real test did not run (0/4). Table II overstates both. | §5.3, §5.6, Table II | — | — |
| M4 | So what | If all claims hold, the prescription is "add an external safety layer" — current practice under ISO 10218/TS 15066 and already published for VLAs [17], [18], [22]. No suite, code or canonical thresholds are released (§7: "roadmap, not a promise"). | §6, §7 | — | — |

#### MINOR
| # | Dimension | Issue Description | Location |
|---|---|---|---|
| m1 | Overgeneralization | "VLA agents" rests on one task-tuned GR00T plus one π0.5 tabletop run (π0: 3/3). "First on a locomoting humanoid" hair-splits Safety-CHORES [21], which §2 calls "genuinely mobile". | §2, §8 |
| m2 | Consistency | §5.3 calls T3a "standards-grounded"; §8 says the full ISO separation distance is not computed. T_r+T_s = 0.4 s is assumed for a walking humanoid. | §5.3, §8 |
| m3 | Evidence | The shield is fire-only; the electric run "did not yield enough completing carries" — an unreported null. | §5.2 |

### Ignored Alternative Explanations/Paths
1. **Freeze-as-reaction.** A visible hazard halves completion (Table IV). "Stop when something unexpected appears" is a safety behavior; conditioning on completion erases it, then declares no reaction.
2. **Unavoidable-by-construction.** No oracle/planner baseline shows a contact-free solution exists for the T4 pick or T6 crossing at the chosen geometry; without it, rates measure placement, not policy.
3. **Replay, not competence.** A 29%-success fine-tune may emit near-constant navigation regardless of scene; "no avoidance" then means "no closed-loop navigation at all" — testable by moving the bin.

### Missing Stakeholder Perspectives
- Functional-safety engineers/certifiers, for whom "the policy should own safety" is a non-starter.
- Training-data curators: the hypothesis blames the demonstration corpus, yet no corpus is inspected.

### Unexamined Premise
That an in-policy "behavioral competence" is a separable, testable target. With a decoupled WBC and a working shield, the paper never states what evidence would show the competence is *present* rather than merely shielded.

### Observations (Non-Defects)
- **What survives:** (a) π0.5 routes through a *rendered* on-path marker 16/16 while clearing an off-path one 0/22; (b) the paired McNemar promptability null at N = 20–24 on two policies (§6); (c) reactive repulsion failing against a fast crosser (§5.7). These support a modest paper: "current VLAs have no closed-loop obstacle avoidance and cannot be talked into it."
- ICLR has no position track; this reads as a benchmark paper without a released benchmark.

### Missing experiments and figures
**MUST** (defeat C1, C2, M1):
1. *Language-following control* — same checkpoint, neutral spatial instructions ("go around the right"); if unfollowed, retract "not promptable". ~1 GPU-day.
2. *Un-condition T1* — all 35 episodes with a freeze/abort classification; figure: per-episode displacement vs hazard visibility. No new runs.
3. *Powered carried-hazard-past-person cell* — N ≥ 20 completing carries in the claimed novel cell. 1–2 GPU-days.

**SHOULD** (defeat C3, M3):
4. Re-score GR00T T4 at the same 0.16 m capsule; one figure, both policies × both metrics. Hours.
5. Feasibility oracle — a planner/teleop path completing T4 and T6 without contact, proving violation is avoidable. ~1 day.

**NICE:** `navigate_cmd` logs across conditions (M2); a second shielded hazard (m3); one RL-trained policy so the training-distribution hypothesis can actually fail.
