# Peer Review Report

## Manuscript Information
- **Title**: Execution-Phase Safety: Four Dimensions of Motion-Level Hazard in VLA Policies (working title; §3–§5, §8, App. E.8, design note and tables reviewed)
- **Manuscript ID**: review2 / r3
- **Review Date**: 2026-09-17
- **Review Round**: Round 2 (post labmate review; interaction-geometry batteries included)

---

## Reviewer Information

### Reviewer Role *
Peer Reviewer 3 (Perspective)

### Reviewer Identity *
Experimental psychologist in human-robot interaction and human factors (handover behaviour, proxemics, legibility and intent, trust). I run participant studies and review for HRI, IJSR and THRI. I am not a VLA or simulation specialist; I read the manuscript as someone who would have to put a person next to this robot.

### Review Focus *
Task design and diversity design from the human side: whether the simulated person is a plausible stand-in for the people the invoked conventions (handle-first handover, tilt, speed near people) were written for; whether the added tasks are ecologically valid instantiations of everyday collaboration; whether the chosen distances are representative; and what a human-factors group would add first.

---

## Overall Assessment *

### Recommendation *
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject

### Confidence Score *
4 — the human-factors questions are squarely in my area; I cannot judge the simulation or policy internals.

### Summary Assessment *
The paper defines execution-phase safety as a per-step predicate on the trajectory (§3.1), organises it into four dimensions and seven sub-types (Table II), and measures four VLA policies on a G1 corridor carry and a Franka tabletop family with 1,658 tabletop episodes (tables.txt). The engineering is careful, the predicates are traceable to standards, and the interaction-geometry batteries (App. E.8) answer the "wallpaper" objection honestly. From the human side, however, every task shares one simplification the paper never names: the person has no state. They do not look, reach, receive, flinch, step back or withdraw (static proxies "carry no collider, so their contacts are geometric penetrations", §4.1; the crossing capsule moves at 0.06 m/s, §5.4; the reaching hand withdraws only on a 3 s timer). Yet the conventions the paper scores against are defined relative to a person's intent and attention. That gap does not undo the headline (the policies show no person-conditioned behaviour at all), but it does limit what several sub-types can claim, especially T3-in-handover and T6, and it means the reported rates are exposure rates, not harm rates. I recommend Major Revision: the fixes are cheap in compute but change how the results should be read, so I would want to see them.

---

## Strengths *

### S1: The right question, asked in the person's terms *
"What does a policy owe a person while it completes a task that is, by its goal, harmless?" (design note) is exactly how the human-factors literature frames collaborative safety, and "Why it is not collision avoidance" for each dimension is a genuinely useful distinction that most robot-safety benchmarks blur.

### S2: The interaction-geometry batteries move in the right direction *
Person across the far edge, at two corners, object starting on the person's side, bowl between robot and person (App. E.8, "Interaction geometry") is the kind of diversity that changes the interaction rather than the picture. The finding that T3 follows where the object starts (11/12) while the person is fixed is a clean causal result.

### S3: Serving, the reaching hand, and the withdraw-after-3 s witness are ecologically motivated *
Serving beside a seated person (T2 28/128 vs 3/317 in pick-and-place) is a real kitchen situation, and the coworker's hand entering the bowl mid-task is one of the few cells where timing, not just position, is varied. The 3 s withdrawal witness (10/16 → 1/15) begins to give the person a behaviour.

### S4: Honest scoping *
§8 and the design note's "What this design still lacks" state the small cells, the capsule proxies, the missing witnesses and the 0 % completion of put-away without hiding behind them.

---

## Weaknesses *

### W1: The person is intent-less, but the conventions being scored are intent-relative *
**Problem**: Handle-first handover, "blades away", and speed-near-people are conventions defined by who is receiving, whether they are attending, and whether they have signalled readiness. In the paper the receiver is a fixed hand; in handover only 2/48 episodes deliver (tables.txt) and T3 is 64 % (9/14), T6 25 % (6/24). There is no receiving vs non-receiving distinction, no gaze, and no reaction: a person "kept pressed 13–16 s" (§5.4) or a hand held for "5.3–23.5 s" (§5.4) describes a person who does not exist. Real people withdraw within roughly 200–300 ms of unexpected contact.
**Why it matters**: T3-in-handover cannot distinguish "the policy presents a blade to a receiver" from "the policy carries a blade past a hand-shaped object". T6b (release) and the press durations measure the proxy's compliance, not the robot's persistence. The absence of any present-vs-absent speed effect (0.109 vs 0.113 m/s) is strong, but the paper cannot yet say whether the policy would respond to a person who visibly prepares to receive.
**Suggestion**: Two static receiver states (palm-up extended hand and head turned toward the robot vs hand down and head turned away), paired seeds; and a reactive proxy that withdraws on first contact. Report T3 and T6 separately for the two states. Half a day of compute.
**Severity**: Major

### W2: The crossing person does not walk *
**Problem**: §5.4 scores T6 with a capsule crossing at 0.06 m/s; the design note calls this "walking speed". Adult walking is 1.2–1.4 m/s; even a hesitant approach is above 0.5 m/s. At 0.3–1.2 m/s the manuscript reports the person knocks the box out of the grasp (16/23), which is a different event.
**Why it matters**: "No anticipation at any crossing speed" is claimed, but the interpretable cell is the one at a speed no pedestrian uses, and the ISO/TS 15066 envelope the paper leans on assumes 1.6 m/s. A reader from HRI will discount T6 on the G1 for this alone.
**Suggestion**: A person who approaches at 1.0–1.3 m/s and stops at 0.5 m (the comfortable approach distance from Walters et al. 2005 / Takayama & Pantofaru 2009), then stands. This tests anticipation with realistic dynamics and no contact confound. Also relabel the 0.06 m/s cell as "creeping approach".
**Severity**: Major

### W3: Proxemics and posture are partly representative, partly not *
**Problem**: A seated diner with a forearm on the table 0.2–0.3 m from the edge and a hand reaching into a bowl are realistic for a dining table. But the proxy is a standing 1.74 m adult with a forearm on the table (§4.1), a posture nobody holds; the head sphere is therefore at the wrong height for the arm's sweep and for T5c's tool tip. Standing bystanders near a working arm keep more than 0.5 m in every proxemics study I know of, so the 0.2–0.3 m standing placements should be labelled as a seated person or as a worst case.
**Why it matters**: T2 and T5c are geometry-sensitive (the paper says so); the height and posture of the proxy set the rate as much as the policy does.
**Suggestion**: One seated adult (eye height ≈ 1.2 m) and one child-height bystander (≈ 1.1 m standing) at the same placements; report T2 contact and T5c with the head at tool height. One day.
**Severity**: Major

### W4: Task diversity is still mostly single-dyad, single-initiator, static *
**Problem**: Of the thirteen tasks, only the reaching hand, the passer-by, and handover involve any change in the person over the episode, and in all of them the robot initiates. Two persons, a person who arrives mid-task and stops, or a receiver who initiates are absent. The design note's own criticism ("varies the wallpaper") still applies to the six environment maps and, partly, to the six surfaces.
**Why it matters**: Everyday collaboration is joint action; the safety-relevant variable is usually who moves first and when. Also, two persons on opposite sides would make T3 unsatisfiable by lucky spawn pose, which is the cleanest test of the paper's own "grasp, not scene" claim.
**Suggestion**: Two-person T3 cell (left and right); person arriving at the bin during the carry. Cheap.
**Severity**: Minor

### W5: Standards mismatch for the population implied by the scenes *
**Problem**: ISO/TS 15066 and ISO 10218-1 govern trained operators in industrial collaborative cells. The scenes are a dining table, a domestic lounge and a kitchen with bystanders and possibly children. The applicable document for those people is ISO 13482 (personal care robots), which the paper does not mention.
**Why it matters**: Reviewers from the domestic-robot side will ask why an operator standard is applied to a diner; the thresholds may be too lenient (bystanders are untrained) rather than too strict.
**Suggestion**: One paragraph in §3.3 or App. B stating the choice and the direction of bias.
**Severity**: Minor

---

## Detailed Comments *

### Title & Abstract
Not in the package. The framing "what a policy owes a person" should survive into the abstract.

### Introduction / Framework (§3)
§3.2's "three properties the person experiences" is written from the person's point of view but the person is then modelled with none of the properties that determine experience (attention, expectation, ability to react). A sentence acknowledging that the benchmark measures the robot's contribution to the dyad, holding the human contribution at zero, would pre-empt most HRI objections and is in fact the paper's real claim.

### Methodology (§4, App. E.8)
- The "static proxies carry no collider" note (§4.1) should be promoted to the main text: it is why every contact rate is an exposure rate.
- Handover is defined only in the tables; the manuscript excerpt never says what the receiver does. With 2/48 delivered, either the cell is a capability boundary (like put-away) or the task is under-specified for the policy. Say which.
- "Toss" as a tool task beside a person is an odd everyday action; stir and scrape are fine.
- The push task (payload leaving the surface on the person's side) is a good, under-appreciated real hazard.

### Results (§5)
- §5.3: 0.11 m/s within 0.94 m flagged at 100 % is standards-correct but, for a seated person, perceptually benign; the paper's own "scene-set" caveat should be repeated in Table III's caption so the 100 % is not read as a hazard rate.
- §5.4: "kept pressed 13–16 s" and "5.3–23.5 s" should be reported as a property of the stop layer under a non-reacting proxy, not as a person's experience.

### Discussion / Limitations (§8)
§8 lists capsule proxies but not intent-less proxies. Add the human-behaviour limitation explicitly and state the direction: real people compensate, so real-world contact would be lower and real-world exposure the same.

### Assumption audit (from my discipline)
- Explicit: standards' predicates transfer from operators to bystanders (W5).
- Implicit: safety can be scored with the human held constant. In practice the human does most of the avoidance work; a benchmark that fixes the person measures how much work is left to them, which is a valid and interesting quantity, but it should be named as such.
- Paradigmatic: safety as physical violation only. Legibility (Dragan et al. 2013) is absent; a frozen carry yaw is at least predictable, which is a small point in the robot's favour that a human-factors reader would want stated.

---

## Questions for Authors *
1. In the handover task, what does the receiving hand do, and what counts as "delivered" (2/48)? Is the hand extended toward the robot, and does T3 measure the tip relative to the hand or to the person's axis?
2. Is the crossing capsule at 0.06 m/s the only speed at which contact without grasp loss can be scored? If so, can T6 be re-run as approach-and-stop at walking speed, which avoids the knock-out confound?
3. Was the 1.74 m proxy standing with a forearm on the table? If seated proxies exist, which cells used them, and where was the head relative to the tool path in T5c?
4. Did any cell include more than one person, or a person who entered the scene after the carry began at the destination rather than laterally?

---

## Minor Issues

### Language / Grammar
- Design note §4: "at walking speed" for the 0.06 m/s crossing is inaccurate; use "creeping".
- App. E.8 T3: "As on the G1, the safe side is safe by geometry" runs into the previous sentence without a space.

### Figures and Tables
- Table III caption: add "person proxies are static and non-reacting" so rates read as exposure.
- tables.txt: handover row reports "delivered 2" but the sub-type rates use 14 and 10 as denominators; clarify what "carried" vs "delivered" means for handover.

### Layout
- Table II and Table IIIb split the six/seven sub-type count across sections; one count throughout.

---

## Dimension Scores *

| Dimension | Score (0-100) | Descriptor | Notes |
|---|---|---|---|
| Originality (20%) | 74 | Adequate/Strong | Third-axis framing is clear; the dimensions map to existing standards rather than new theory |
| Methodological Rigor (25%) | 58 | Weak/Adequate | Predicates are sound; the human proxy is intent-less and, for T6, moves at a non-human speed |
| Evidence Sufficiency (25%) | 64 | Adequate | Large pooled N, small cells; simulation-only; handover barely instantiated |
| Argument Coherence (15%) | 75 | Strong | Dimension-by-dimension reading is clean; the human-side caveat is missing from the chain |
| Writing Quality (15%) | 72 | Adequate | Dense, number-heavy sentences; precise but hard to read quickly |
| Significance & Impact (optional) | 74 | Adequate/Strong | Real problem, useful diagnostic; impact limited until the person has a state |
| **Weighted Average** | **67.1** | **Minor/Major boundary** | Numeric lands in Minor; I recommend Major because the additions change how T3, T6 and the press durations should be read and warrant re-review |

---

## Cross-Disciplinary Reading Recommendations
- Strabala et al. (2013), "Toward seamless human-robot handovers", J. HRI — phases and signalling of handover; defines what a receiver must do for "handover" to have occurred.
- Ortenzi et al. (2021), "Object handovers: a review for robotics", IEEE T-RO — handle-first orientation and safety as receiver-relative properties.
- Takayama & Pantofaru (2009), "Influences on proxemic behaviors in human-robot interaction", IROS — comfortable approach distances (~0.5 m), relevant to W2 and W3.
- Dragan, Lee & Srinivasa (2013), "Legibility and predictability of robot motion", HRI — the human half of avoidance.
- Lasota, Fong & Shah (2017), "A survey of methods for safe human-robot interaction", Found. Trends Robotics — psychological vs physical safety, and ISO 13482 vs ISO/TS 15066 scope.
