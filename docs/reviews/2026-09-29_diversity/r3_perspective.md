# Perspective Review Report (Peer Reviewer 3)

**Manuscript:** *Execution-Phase Safety for VLA Agents* (v0.45). **Focus:** is the diversity and scene design sufficient?

### Reviewer Identity
HRI researcher with functional-safety assessment experience (ISO 12100 / 13849 risk graphs, unfenced
installations). Outsider to VLA training; I read this as someone who must sign a risk assessment.

### Recommendation
**Major Revision.** Confidence **4/5**. **Score 68/100.**

Sub-scores /100 — assumption transparency & honesty 85; ecological validity of the scene set 55; bystander
modelling 50; do the four dimensions carve the problem 70; practical impact for a deployment reader 60;
cross-disciplinary grounding (HRI, safety practice) 60.

### Summary
The empirical effort is large and willing to disconfirm itself (6159 tabletop episodes; witnesses; appearance
ablations; a finite-mass hand; a yielding pedestrian), and the core claim — four motion properties are never
conditioned on the person — survives the weakest part of the design. But the diversity is narrower than the prose
implies, and two absences are inferential, not cosmetic. (1) Every person is visible from spawn: no doorway,
corner, threshold or occluder appears in six surfaces or four maps, so "not perception, therefore architecture"
is established only for the easy case. (2) Every scored bystander is inert, which by the paper's own analysis
makes the tabletop force number a proxy artefact — yet that number *is* the tabletop speed-and-force score.
Separately, the four dimensions exhaust what the motion does *to* a person but omit what it *communicates*
(legibility) and how *long* exposure lasts. Both are addable from existing logs.

### Strengths
**The orientation finding is human-model-independent** — a world-fixed yaw (+3° ± 11° over eight azimuths; a side
effect and no stature effect; unrendered person 8/8 right, 0/10 left) does not depend on how the person is
modelled. **Instrument/witness discipline is honest**, and self-refuting controls are reported: the finite-mass
hand, the yielding pedestrian, the 0/31 second-room rebuild, the T2 threshold concession.

---

## Numbered issues

**CRITICAL 1 — The tabletop speed-and-force score is built from a quantity the paper itself shows is not a harm
measure.** Table III prints π0.5 **7**, π0 **0**, π0-FAST **0**, GR00T-DROID **0**, each equal to T5b alone.
E.8 then states the Annex A prediction for a *free* hand is 7 N median, 94 N max, **0/202 above 140 N**; a
finite-mass hand gives 2 N median against 47 N on the immovable capsule; "the 140 N exceedances of Table III are
the capsule's, not the hand's." A practitioner will read a four-policy force ranking off constraint forces on an
inert capsule. *Fix:* print no tabletop force score; substitute the measured exposure triple (reached 78/83,
touched 65/83, pressed ≥ 5 s 16/83) plus the Annex A prediction, and label the G1's 95–428 N as unyielding-body
exposure inside Table III, not only in §8.

**CRITICAL 2 — The bolded dimension mean invites the ranking the paper disclaims, and in the trajectory column
carries no information.** All three Franka policies read exactly **50** = mean(T1 100, T2 0). E.8 calls the
tabletop T1 cell a ceiling (entry "forced") and T2 sits at floor; a mean of a forced ceiling and a floor is not
a score. The discriminating cell exists — the 0.28 m off-path keep-out (π0.5 12/64, π0-FAST 2/32, π0 5/28,
GR00T-DROID 15/15, blind control 0/64). *Fix:* score trajectory from the off-path level, or drop the bold mean
and print the vector.

**MAJOR 3 — Occluded or late-revealed people are structurally absent, and that absence licenses the fixability
taxonomy.** The perception ablation is a render/hide toggle at fixed geometry (10/10, 12/12, 8/8 right); the four
"environment maps" are backdrops on the same dining table. Late detection is the dominant real-world
execution-phase failure and is untested. *Fix:* one cell per family where an occluder (counter end, door frame)
reveals the person mid-transport, reporting time from visibility to closest approach. Until then, say
"architecture, not perception" holds for an always-visible person.

**MAJOR 4 — A missing axis: legibility / avoidability — and the data are already logged.** Risk in practice is
severity × frequency × *possibility of avoidance* (ISO 12100 / 13849 S-F-P). The suite asks whether the robot
reads the human, never whether a human could read the robot. The bow tables (π0.5 0.089 m at the desk against
0.001 m for the blind control; base-relative under transport reversal; 0.099 → 0.018 m across the radius probe)
are a *predictability* result presented only as a keep-out cause. *Fix:* compute a predictability statistic from
existing trajectories; map the dimensions onto S-F-P; and extend "the demand on the safety layer" to "…and on
the human" — with no proxy able to yield, the suite cannot separate "the policy is unsafe" from "the policy
relies on human avoidance."

**MAJOR 5 — Exposure duration is unowned.** All nine predicates are occurrence or extremal; two policies with
identical booleans can differ tenfold in dwell. The data exist but sit in secondary rows (pressed ≥ 5 s 16/83;
1.7 s median contact; 13–16 s pressing; 5.3–6.8 s stop dwell). *Fix:* seconds-inside-keep-out,
seconds-above-45°, seconds-inside-*d₀*, seconds-in-contact beside every rate. No new runs.

**MAJOR 6 — The humanoid family, the claimed novel cell, is one non-portable room.** E.7's rebuild gives 6/31
lifted, 0/31 delivered in two other rooms, and the corridor is an empty 1.9 m lane. *Fix:* state this rather
than only concede scope; if a second room is out of reach, vary the layout inside it (width, a furniture
occluder, a threshold) so one geometric factor moves.

**MAJOR 7 — T3 × T6 is empty: orientation is never scored against a moving person.** T3 is taken at closest
approach to a static bearing; T6b scores speed only; handover — where presentation matters most — is a
capability boundary (2/48 delivered). The two-bystander cell shows the half-space predicate degenerating (37/39;
1/47 compliant directions). *Fix:* score presentation against the existing passer-by and crossing person, and add
a continuous angle-to-nearest-bearing alternative beside the half-space predicate.

**MINOR 8 —** "Six work surfaces / four environment maps" oversells one topology: three heights, one open drawer,
backdrop swaps, 3089 of 6159 episodes at the dining table. Prefer "one tabletop topology at three heights under
four backdrops."

**MINOR 9 —** Regime is resolved per sub-type (Table VI) but not per scene: a packing-station coworker at 0.45 m
and a dining-table family member fall under different regimes (industrial series vs ISO 13482). One column in
Table IVb fixes it.

**MINOR 10 —** The most actionable result is buried: a base-referenced stop misses the arms (8/11 empty-handed
contacts persist at 0.50 m; a full joint hold still 17/17). Promote to §5.4 or §6.

## Assumption audit
**Implicit:** *harm is a property of the robot's motion alone.* Unfenced safety is a joint achievement of robot
legibility and human anticipation; inert humans measure one term of a two-body system, overstating hazard where
people yield and understating it where legibility fails. Put this in §3 as the frame of every rate, not only in
§8 as a proxy caveat. **Implicit:** *an occurrence is the unit of risk* (MAJOR 4, 5).

## What the people cost each dimension
**Trajectory:** survives (the path is unchanged with the person unrendered, 0/39 within 0.10 m), but T2's rate
would fall against a person who steps back and T2 has no witness — Table III's most human-model-sensitive number.
**Orientation:** survives best; a frozen world-frame yaw is indifferent to how the bearing arises. **Speed &
force:** most damaged — the SSM human-velocity term is zero and the forces are an immovable body's (CRITICAL 1).
**Dynamics:** the *absence of deceleration* survives (0.06–1.2 m/s; the collider-off twin passes through the
body); the contact rates and "pressed 13–16 s" do not. The withdrawing-hand control (39/91 against 106/210,
*p* = 0.26; payload follows the hand back on 20/25) is the only evidence this is not a proxy artefact — move it
from E.8 into §5.4.

## What a deployment engineer would ask for that is missing
Demand rate per operating *hour* — the central claim is a rate with time units, reported as a per-episode
proportion. The availability cost of each mitigation as a curve, not points (0.50 m stop → 8/24; 0.94 m → 0/12;
governor alone → 0/12). Dwell inside the keep-out. One occluded-approach cell. A whole-body versus
base-referenced envelope recommendation (present, buried). A per-scene regime label. A mapping onto severity /
frequency / avoidability. And how much demand is absorbed today by a human who yields rather than by any layer.

## Verdict on the author's question
Sufficient for the qualitative claim (the profile recurs on every dimension); **insufficient for the
scene-generality and policy-comparison claims the tables invite**. The cheapest high-value fixes are re-analyses
of existing logs — dwell, predictability, off-path trajectory scoring — plus one occluded cell per family.
