# Peer Review Report

## Manuscript Information
- **Title**: Execution-Phase Safety for Embodied VLA Agents: A Taxonomy and a Case for Behavioral Safety Competence
- **Manuscript ID**: draft v0.24 (ICLR 2027)
- **Review Date**: 2026-09-09 · **Round**: 1

## Reviewer Information
### Reviewer Role
Peer Reviewer 3 (Perspective — cross-disciplinary / practical)
### Reviewer Identity
Industrial functional-safety engineer / pHRI practitioner certifying collaborative and service robots to ISO 10218-1/-2, ISO 13482, ISO/TS 15066; has deployed mobile manipulators around untrained people. ML outsider.
### Review Focus
Standards realism of SSM/PFL usage and thresholds; whether "behavioral safety competence" survives the certifier's external-layer view; the human model and ISO 13482 implications.

## Overall Assessment
### Recommendation
- [x] **Major Revision**
### Confidence Score
4
### Summary Assessment
The paper defines an execution-phase axis of VLA safety, a six-type taxonomy, and measures GR00T/G1 and π0.5/Franka: every completing carry crosses an on-path keep-out, the arm enters a bystander's body, no speed-and-separation behavior, no reaction to a crossing person. The phenomena are real and the hazard framing is unusually careful for an ML venue. Two things stop me handing it to a safety team. It never separates the certified external *safety function* — where SSM/PFL live — from *policy behavior*, so a certifier reads "the policy implements no SSM" as "correct, it must not". And it reports exposure (zone entry, 0.000 m) as harm, with no body region, force or stopping time. Both are fixable from existing logs.

## Strengths
### S1: Payload counted as part of the machine
§3.3/§5.1 treat the carried hazard as part of the robot system, exactly as ISO 10218-2 treats the workpiece.
### S2: SSM used as an envelope
§5.3 inverts S_p into v_allow(d)/d_0 with lenient parameters; §5.8's radius sweep is the sensitivity a certifier asks for first.
### S3: Metric choice shown to flip verdicts
§5.9's axis-vs-capsule flip (3 % → 53 %) is the classic zone-monitoring error; publishing it stops others certifying the wrong surface.

## Weaknesses
### W1: Safety function and policy behavior conflated
**Problem**: Title, §1, §5.3 ("the policy implements no SSM") and §9 ("safe to stand next to") ask the task policy for properties certification assigns to a safety-rated layer (ISO 13849-1); a learned policy earns zero risk-reduction credit.
**Why it matters**: practitioners will dismiss the position as naïve, though the data support a stronger claim.
**Suggestion**: a §1/§6 paragraph and table: (a) the external layer is non-negotiable; (b) policy behavior sets its *demand rate* — for a biped each protective stop is a fall hazard and lost availability; (c) a geometric stop cannot cover T2/T5/T6 (it leaves the blade pointed, does not level a cup), so that competence must live in the policy or a dedicated controller. Anchor in IEC TR 5469:2024.
**Severity**: Critical.

### W2: Exposure reported as harm; no severity term
**Problem**: T1 counts zone entry, T4/T6 count 0.000 m or < 0.30 m; §5.3 uses payload speed magnitude, not directed closing speed, and ignores the closest link of a walking ~35 kg body. No body region, force or energy is reported.
**Why it matters**: risk graphs need severity per body region; PFL is region-specific (skull: no transient contact). At 0.34 m/s a blunt box into an adult chest is near the TS 15066 transient limit, into a child's head well beyond it.
**Suggestion**: MUST-2.
**Severity**: Major.

### W3: SSM parameters asserted, not measured
**Problem**: §5.3 assumes T_r+T_s = 0.4 s, C = 0.2 m; a biped cannot stop in 0.4 s without a step, and ISO 13855 gives C ≈ 0.85–1.2 m for floor scanners. The 2016 TS is cited although ISO 10218-1/-2:2025 absorbed and revised it.
**Why it matters**: "scored against the standard" needs the machine's own stop test (ISO 10218-1 Annex B).
**Suggestion**: MUST-1; cite the 2025 editions; note hot/sharp payloads are excluded from PFL, so T1/T2 are SSM-only, T3b/T4 PFL-eligible — a clarifying Table II column.
**Severity**: Major.

### W4: Human model is the easiest case
**Problem**: adult, standing, non-reacting capsule; T6 crossing speed unstated; no child, seated or reaching human, although ISO 13482 makes vulnerable bystanders the design case and its "incorrect autonomous decisions and actions" hazard class is what this taxonomy refines.
**Why it matters**: box-carry height is child-head height; reach-in is how contacts happen.
**Suggestion**: SHOULD-6; state crossing speed against ISO 13855's 1.6/2.0 m/s.
**Severity**: Major.

## Detailed Comments
- **§5.7**: position-repulsion is not SSM — SSM is anticipatory by construction (v_h term). Test a compliant stop-based governor before concluding T6 needs new control theory; report completion vs d_0, the availability cost.
- **§5.5/§5.9, §8**: 0.000 m against a capsule is *penetration* — say whether the proxy collides; add loss-of-balance/toppling to §8.

## Questions for Authors
1. T6 crossing speed, and does the person proxy carry collision geometry?
2. Masses of G1, box, hand; payload height vs a six-year-old's head?
3. Would you reframe policy competence as lowering *demand on*, not replacing, a certified layer — and retitle accordingly?

## Minor Issues
- §5.3: 0.34 m/s also exceeds ISO 10218-1's 250 mm/s reduced speed — cite it. Rename "shield" → "reference filter" (not safety-rated); label the 0.30 m near-miss margin study-defined.

## Dimension Scores
| Dimension | Score | Descriptor |
|---|---|---|
| Originality (20%) | 72 | Adequate |
| Methodological Rigor (25%) | 58 | Weak/Adequate |
| Evidence Sufficiency (25%) | 62 | Adequate |
| Argument Coherence (15%) | 62 | Adequate |
| Writing Quality (15%) | 74 | Adequate |
| Significance & Impact | 78 | Strong |
| **Weighted Average** | **65** | **Major** (Critical W1 overrides) |

## Missing experiments and figures
**MUST**
1. **G1 stop-time/stop-distance test** under its WBC (ISO 10218-1 Annex B analogue): stop from 0.34 m/s, measure T_s, S_s; recompute d_0, v_allow. Buys: §5.3 becomes machine-specific. Cost: hours, sim.
2. **PFL-referenced severity from existing logs**: per T1/T4/T6 event, record body region, closing speed, PhysX contact impulse; compare with TS 15066 Annex A limits (v_max = F_max/√(μk)). Buys: "0.000 m" becomes "exceeds skull limit by X×"; T3b for free. Cost: days.
3. **Figure: SSM envelope vs measured profile** — v_allow(d) (nominal, lenient) over the six speed-vs-separation traces, plus the 250 mm/s line. Buys: the picture a certifier reads in five seconds. Cost: hours.
4. **Standards-mapping table** T1–T6 ↔ ISO 12100 hazard type ↔ ISO 10218-2:2025 / ISO 13482 clause ↔ SSM-only vs PFL-eligible. Cost: writing.

**SHOULD**
5. **Stop-based SSM governor as reference layer** on T1-person, T3a, T6; report violation *and* completion vs d_0. Buys: whether T6 needs anticipation or merely compliance; the availability cost. Cost: days.
6. **Human-model variants**: child (~1.15 m), seated adult, reaching arm; T6 at 0.5/1.0/1.6 m/s. Buys: ISO 13482 relevance, head-height exposure. Cost: days.
7. **T4 3-D margin sweep** (0, 0.05, 0.10 m, S_p), both policies. Buys: §5.8-style sensitivity for T4. Cost: offline.

**NICE**
8. **Balance/topple readout** (CoM excursion, falls) during governed stops. Cost: small.
9. **Hardware-in-the-loop check**: replay 5–10 trajectories on a G1 with a mannequin, or validate sim stop distance against manufacturer data. Buys: sim-to-real credibility. Cost: high.
