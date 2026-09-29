# Devil's Advocate Review — Round 4 (diversity and scene design)

**R4, Devil's Advocate.** Manuscript v0.45, read-only; no other Round-4 report consulted. **Score: 58 / 100**
(adversarial floor; Round 3 was 68.3). **Answer:** the diversity is *accumulated*, not *crossed*; on three of four
dimensions it is narrower than one policy and one geometry. *Credit first:* the taxonomy is useful, and the group
repeatedly ran controls that contradicted its own draft and then changed the draft — the radius probe being the paper's
best experiment, and the most damaging to it.

### Strongest Counter-Argument

The paper claims a *policy × dimension* matrix. It has built a *scene-geometry × dataset* matrix, and its own control row
proves it. A scripted straight-line carrier that reads simulator state and is blind to the person scores **Trajectory 50
(T1 100, T2 1) | T3 47 | Speed & force 6 | T6 100** (Table III), against π0.5's **50 | 43 | 7 | 94**. If a straight line
with no policy, no language and no vision reproduces the profile, the profile belongs to the scenes. The one separating
sub-type is T4 (77 % vs 13 %), and that 13 % comes from a pinch grasp that succeeded on 31 of 112 attempts, the authors
conceding the witness "holds where the pinch holds" — carries selected for being firm grasps are exactly the carries that
stay level. The discriminating content of a four-dimension, 7497-episode suite is one sub-type on a survivorship-selected
witness.

Second, "recurs across policies" is a claim about one corpus. §4.1: π0.5, π0 and π0-FAST are "openpi; one backbone, two
action decoders"; GR00T N1.6-DROID is DROID too. E.8 states the mechanism: "The decoders trained on one dataset agree with
each other and with GR00T N1.6-DROID… the drift is learned from the demonstrations." Granted — then §2's hypothesis
("absent from the imitation training distribution") is confirmed by a design that never varies the distribution. The fifth
row, GR00T on the G1, is one room in which it delivers ~50 % and outside which it delivers **0/31** (§8, E.7). Five
policies, one dataset plus one room.

## CRITICAL

**C1 · One dataset, not four policies.** *Evidence:* §4.1 "one backbone, two action decoders"; E.8 "A third DROID policy";
E.8's mechanism sentence above. *Counter:* §5.5's "Across four policies and two embodiments the profile recurs" is, by the
authors' own causal account, "across three decoders on one corpus", and §2's hypothesis needs a second corpus the arm
family lacks. *Rebuttal:* GR00T-DROID's backbone and decoder both differ. *Holds?* **No** — the corpus is the constant.
Restate as dataset-level recurrence; §1's contribution 3 weakens accordingly.

**C2 · The blind control reproduces the profile on three of four dimensions** (the counter-argument above, as a finding;
E.8's matched pool: "T2 3/208 against 2/205 and T3 46/112 against 32/75"). *Rebuttal:* the control is a witness, not a
comparison. *Holds?* **Partly, and that is worse** — then three dimensions have no demonstrated headroom at all.

**C3 · The scored tabletop T1 is the cell the paper itself calls forced; Round-3 C4 was discharged in the appendix only.**
*Evidence:* §5.1 — "56/56 carries (the scored tabletop T1); a keep-out at each carry's midpoint… is exposure, not a score";
E.8 — "The scored tabletop marker sits at the midpoint of a collinear transport… entering it is forced and 56/56 is a
ceiling"; E.8's on-path column sums 8+16+16+16 = **56**; `gen_a45_numbers.py:59` pools T1 "on the path only".
*Counter:* §5.1's disclaimer is false on the paper's own arithmetic — the scored T1 *is* the midpoint cell, so Trajectory =
mean(forced 100, floor 0) = **50** to the unit for π0.5, π0 and π0-FAST. The discriminating cells (12/64 at 0.28 m; 62/63
against the line's 15/64 at 0.20 m) exist and are not the score. *Holds* — promote the off-path cells or drop the column.

**C4 · Two "parallel dimensions" are the same episodes of one task, and the floor of 8 lets 0/9 print as a bold score.**
*Evidence:* `gen_a45_numbers.py:74-77` builds T5b and T6 from the identical cell list and denominator; Table IIIb π0.5
**T5b 6/83, T6 78/83**; π0, π0-FAST, GR00T-DROID **T5b 0/9**; Table III prints bold **Speed & force 0** on three rows.
*Counter:* the advisor's "each dimension resting on several tasks" is false here — one task, nine episodes, the same nine
that score Dynamics; a bold 0 meaning "no force above 140 N in nine carries of one cell" (Wilson upper bound 30 %) is the
paper's most misleading number. *Rebuttal:* §3.2 pre-empts it — "separate by what they measure, not by which episodes they
use". *Holds?* **No** — that concedes the fact and leaves the scores non-independent.

**C5 · Route memorisation fits the G1 data better and is not among the four alternatives answered.** *Evidence:* §8 "one
corridor (0/31 delivered in two other rooms)"; E.7 "bound to the room it was fine-tuned in"; Appendix F answers only
collision-avoidance-renamed, external-layer, unavoidable-scenes, completion-null. *Counter:* a checkpoint executing one
memorised route produces every G1 signature — yaw fixed at +3° across eight azimuths, path invariant to naming and
rendering, no slowing, no avoidance, a 2–3 cm shift when pixels change. "Absent from the training distribution" and "this
checkpoint can only do this trajectory" are observationally equivalent, and 0/31 favours the second. *Rebuttal:* the same
profile appears on the Franka. *Holds?* **No** — those rows are C1's confound and C3's forced geometry. E.1 names the clean
test (`navigate_cmd` logging) and does not run it.

## MAJOR

**M1 · The force numbers are known proxy artefacts, and the fix was applied only where it was harmless.** E.8: a
finite-mass hand moves the median peak from **47 N to 2 N**, and "T5b therefore counts contacts, not injuries… the 140 N
exceedances of Table III are the capsule's, not the hand's." The G1 crosser stays "a kinematic capsule (60 kg)… not
displaced by the impact", and the abstract still sells "median 200 N" with Table III **Speed & force 86 (T5b 71)**. An
exposure label does not license an ISO-limit comparison. *Holds.*

**M2 · The abstract overgeneralizes.** Abstract: "rendering it draws the path closer"; §6(ii): "the arm's path drifts
whether or not one is there… not toward what is seen" — a 2–3 cm, one-room, one-policy effect, stated as general.

**M3 · The six surfaces hold constant the variable that produces the trajectory result.** E.8: DROID transports sit at "a
median 0.61 m from the base"; "The benchmark's transports run at 0.45–0.54 m, at the inner edge of that range"; the bow
falls 0.099 → 0.018 m from 0.35 m to 0.75 m; "a scene laid out farther from the base would see the bow reverse." Six
surfaces differ in height, lighting and clutter and share one radius band; the causal axis is varied in one probe on one
table. *Holds* — the sharpest answer to the question put: no.

**M4 · Scope is set by policy capability, not hazard importance.** Boundaries: handover 2/48 delivered, drawer 0/32, door
0/8, push 0/16, pitcher 0/16, drill 0/32 — removing presentation to a receiver (Appendix H: "the most intuitive instance of
the thesis"), the liquid vessel, the powered tool and every pinch hazard (§8: "pinch and head-height absent"). The claimed
novelty, "a passive, non-receiving bystander", coincides with what the policies can complete; the scored hazard set is a
mug, scissors and a fork at table height.

**M5 · Orientation still averages a chance-level predicate (Round-3 C4 resolved by decree, not repair).** Table III: "T3
pooled over bearings (chance 50 %)"; scored T3 = 52, 43, 42, 46, 20, 47 — every row at or below chance, blind control
included. GR00T-DROID's **Orientation 53** = mean(T3 **2/10**, below chance, one over the floor; T4 86).

**M6 · A conclusion drawn from a null test.** E.8: "43 % against 50 %, **Fisher p = 0.2587** — so part of the static hand's
exposure is the proxy's immobility." Round 3 had this at p ≈ 0.004; re-pooling removed the effect, the inference stayed.

## MINOR

**m1** (E.8/IVd) "one seed, eight episodes per cell" against the same table's "seeds 42 and 7 pooled" and 16/16 cells; "four
environment maps" (§4.1) against three named. **m2** (IV/IVb) "six work surfaces": the island kitchen is a capability
boundary (3/32) and the dining table is 3089 of π0.5's 4161 episodes. **m3** (§5.1) T2's G1 rate is a metric choice —
26/32 by body surface, 8/32 by axis — with no witness, yet half of Trajectory 89.

### Ignored Alternatives

(1) Route memorisation (C5). (2) A workspace-radius prior, granted for the bow but not for tabletop T1, the T3 side effect
or T6 reach. (3) Predicate geometry — T1 forced, T3 at chance, T2 threshold-set: three of nine predicates may report their
own construction.

### Missing Stakeholders

No non-DROID policy and no second corpus — the party who could adjudicate C1 is absent. No human-factors input on what a
bystander does (§8: "the people have no state"). Standards bodies: operator limits applied to bystanders.

### Unexamined Premise

The paper assumes the four dimensions are properties **of policies**. Nothing separates policy from scene geometry and
training corpus, because neither is crossed with anything: one arm, one gripper, one corpus, one radius band, one corridor.
A benchmark that cannot vary the two factors its own mechanism section calls causal measures its own scenes.

### The single strongest sentence a hostile reviewer would write

> Your own person-blind straight-line carrier scores 50 on Trajectory, 47 on T3, 6 on Speed-and-force and 100 on T6 —
> indistinguishable from your four DROID checkpoints on three of your four dimensions — so this matrix demonstrates that
> your scenes force these numbers, and the one sub-type separating a policy from a straight line rests on a pinch grasp
> that succeeded 31 times in 112.
