# Peer Review Report

## Manuscript Information
- **Title**: Execution-Phase Safety of VLA Policies: Four Dimensions, Seven Sub-types (working title; package: §3–§5, §8, App. E.8, design note 2026-09-16/18, coverage tables 2026-09-18)
- **Manuscript ID**: review2 / round 1
- **Review Date**: 2026-09-17
- **Review Round**: Round 1

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 (Domain)

### Reviewer Identity
Industrial physical-HRI safety engineer; certifies collaborative and service robots to ISO 10218-1/-2:2025, ISO/TS 15066 and ISO 13482; has deployed mobile manipulators around untrained people.

### Review Focus
Do the seven predicates name the right hazards and cite the right clauses? Does the task set cover what an ISO 12100 / ISO 13482 risk assessment for a kitchen, serving or workshop robot lists first? Do the human proxies support the standards they are scored against?

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject

### Confidence Score
4 — standards, hazard taxonomy and pHRI biomechanics are my daily work; VLA and simulator internals are not.

### Summary Assessment
The manuscript defines execution-phase safety as a per-step trajectory predicate (§3.1) and scores four dimensions / seven sub-types (Table II) on a G1 corridor carry and a Franka tabletop family across three VLA policies (Tables III, IIIb). The headline — no detour, frozen hazard axis, no slowing, no anticipation — is credible, and the authors are unusually candid about proxies and witnesses (§8; design note "What this design still lacks"). But the standards are decorative in three places where they carry the argument: T2's 0.10 m is not "the Z of ISO/TS 15066"; T5a applies speed-and-separation monitoring to a table-side cobot where power-and-force limiting is the applicable mode, so its 100 % is a category error; T5c cites a teach-mode speed for a moving blade that the PFL framework excludes, and its assets (ladle, spatula, tongs) have no edge. T5b forces are measured against an infinite-mass kinematic capsule, so they are not the Annex A quantity. The hazard list omits what a kitchen assessment lists first (scald, pinch in drawers/doors, dropped load, head-height exposure of seated persons and children). Major revision: fix citations, re-mode the tabletop speed criterion, re-derive force, and narrow the coverage claim or add the missing classes.

---

## Strengths

### S1: Dimensions map to the right safety functions
§3.2 maps trajectory → protective separation, orientation → handover/load-handling practice, speed/force → SSM and PFL, dynamics → the human-velocity term and the protective stop. Framing the policy as setting "how often the layer must intervene" (§3.2; §5.4: stop fires 22/24) is a standards-compatible metric — the demand rate on a safety function (ISO 13849-1 high-demand mode).

### S2: Threshold sensitivity is reported where the threshold is invented
T1 is flat for 0.15–0.80 m (Table II; E.8 empty band 0.10–0.245 m). T2 reports the full threshold curve and contact count and retracts an earlier 3 % → 53 % "discovery" as a threshold change (E.8 "first probe"). That is certification-file discipline.

### S3: Body-region limits and spill geometry are correct
Hand 140 N / abdomen 110 N / chest 140 N quasi-static and 220 N / 280 N transient (§5.3) match ISO/TS 15066:2016 Table A.2; 14–27° for 1–2 cm freeboard on an ~8 cm mug is right and correctly reported beside the permissive 45°.

### S4: Interaction-geometry battery is real exposure variation
Five placements (design note; E.8) move T2 closest approach 0.03–0.27 m and T3 2/8–11/12 while T4 persists everywhere. This — not the six environment maps — is the diversity a safety engineer asks for.

### S5: Trapping after contact is noticed
"Kept pressed 13–16 s" (§5.4) and "keeps pressing 5.3–23.5 s in 17/138" (E.8) are the clamping case ISO/TS 15066 §5.5.5 cares most about; T6b is the right addition.

---

## Weaknesses

### W1: T5a applies the wrong collaborative mode to the tabletop
**Problem**: §5.3 / E.8 score every Franka transport unsafe for passing inside d₀ = 0.94 m at 0.11 m/s (326/326, 100/101, 29/29). With v_h = 1.6 m/s and T_r+T_s = 0.4 s, SSM requires the robot *stopped* whenever anyone is within 0.94 m — i.e., "never move while a person is at the table". No integrator certifies a table-side Panda under SSM; the applicable mode is PFL (ISO/TS 15066 §5.5.5; ISO 10218-2:2025 collaborative-application clauses), under which a 0.11 m/s carry is compliant by construction and the criterion is Annex A force/pressure (your T5b) plus the transient relative-speed bound v_rel,max = F_max/√(μ·k) (Annex A.3.3).
**Why it matters**: The "43 / 50 / 50" speed-and-force scores in Table III are mostly this scene-set 100 %. The surviving finding — no modulation (0.109 vs 0.113 m/s, p = 0.79) — is behavioural, not a standards violation.
**Suggestion**: Score SSM only on the mobile G1 (base logic per ISO 3691-4:2023 / ISO 13482); on the tabletop replace T5a with Annex A.3.3's per-region relative speed; report no-modulation as a separate unscored row.
**Severity**: Critical (norm: ISO/TS 15066 §5.5.4 vs §5.5.5).

### W2: T5b forces are not the Annex A quantity
**Problem**: The crossing person is "a kinematic capsule with a collider" (§4.1) — an infinite-mass rigid wall. The 95–428 N (§5.3) are solver penalty/constraint artefacts, not the force a compliant human receives. Annex A limits derive from a spring–mass model with region-specific effective mass (abdomen 40 kg, hand 0.6 kg) and stiffness (abdomen 10 N/mm, hand 75 N/mm; Table A.3). The hand case is a clamp (mug rim on hand against bowl) whose binding limit is pressure (Table A.2, hand/finger 190 N/cm²); a capsule has no contact area. "~1 s sustained" (design note) is not the standard's 0.5 s transient/quasi-static boundary (§5.5.5.2).
**Why it matters**: T5b is the only region-specific force claim ("10/13 pass 110 N").
**Suggestion**: Give the struck region Table A.3 mass/stiffness, or post-process penetration/velocity through the A.3.3 energy model; report hand pressure from the rim contact area; use the 0.5 s boundary.
**Severity**: Major.

### W3: T5c cites the wrong standard and its assets are not blades
**Problem**: Table II / §5.3 ground 0.25 m/s inside 0.5 m in "ISO 10218-1 reduced speed for collaborative operation". 250 mm/s is the reduced-speed-control TCP limit for manual mode and hand guiding (ISO 10218-1:2011 §5.6.3, §5.10.3; retained in the 2025 edition) — a retreat assumption for a trained operator, not a laceration criterion. PFL presupposes blunt geometry: sharp edges and points are to be eliminated by design (ISO 10218-2 collaborative-application design requirements; ISO/TS 15066 §5.5.5), so no clause licenses a speed threshold for an edge. The design note says there is no knife asset; T5c is measured on a ladle, spatula and tongs (10/41), none edged.
**Why it matters**: T5c is averaged into Table III and is the paper's only "energy transfer" claim.
**Suggestion**: Rename "tool-tip speed within reach"; ground the threshold in Haddadin et al., "Soft-tissue injury in robotics", ICRA 2010 (penetration vs. speed for knives/scissors) or Annex A.3.3 v_rel,max for blunt tools; state that sharp tools fall under hazard elimination (ISO 12100 §6.2).
**Severity**: Major.

### W4: T2's 0.10 m is mis-attributed
**Problem**: Table II: 0.10 m "is the position-uncertainty allowance Z of the ISO/TS 15066 separation". §5.5.4.2.3 Eq. (2) defines Z_d (operator, from sensor tolerance) and Z_r (robot) but fixes no value; the 0.1 m is the authors' own T5a parameter (§5.3), so T2 is grounded in T5a's choice.
**Why it matters**: T2 separates the G1 (81 %) from the arm (1 %) and is the row the authors show is threshold-set.
**Suggestion**: Cite as "a 0.10 m margin of the order of typical Z_d + Z_r for scanner SSM (ISO 13855:2024; ISO/TS 15066 §5.5.4.2.3)"; keep contact as the threshold-free statement; add ISO 13854:2019 minimum gaps (hand 100 mm, body 500 mm) for the pressed-against-table trap.
**Severity**: Minor.

### W5: Coverage stops at "carry past a bystander"
**Problem**: An ISO 12100 Annex B / ISO 13482 Annex A assessment for a serving robot lists first: pinch/crush in drawers and doors (drawer 0 % completion; door 0/8 carried, "nothing to score"); scald (T4 is an angle — no spill model, no ISO 13732-1 threshold, no tilt-*over*-person cell); dropped/projected load ("knocks it from the grasp 16/23" and the push task's payload leaving the surface are observed, not scored); head/face exposure of a seated diner or child (only a standing 1.74 m adult, so Annex A face 65 N / neck 150 N are never exercised and T2 never sweeps the head band); humanoid fall onto a person (ISO 13482 instability). T1's "live strip" and stove harm no *person* when a box passes them.
**Why it matters**: The paper claims execution-phase safety, not transport-past-bystander safety; Table 2's dynamics row is populated for three of thirteen tasks.
**Suggestion**: Scope the title/abstract to transport, presentation and approach hazards, or add a seated person, a child/5th-percentile proxy, a scored drop event, a scored spill-within-reach event (T4 ∧ reach), and a drawer/door pinch cell with a hand in the gap.
**Severity**: Major (norm: ISO 12100:2010 Annex B; ISO 13482:2014 Annex A).

---

## Detailed Comments

### Title & Abstract
Table II caption and §3.3 say "six sub-types"; the table lists seven. Table IIIb has no T5c column though Table III includes it.

### Literature Review / Theoretical Framework
No handover or injury-biomechanics literature is visible in the excerpt; T3's "handover practice presents a hazard away" and "handle-first convention" need sources (below). The 2025 editions of ISO 10218-1/-2 absorbed most of ISO/TS 15066 and revised Annex A values; state which editions are used.

### Methodology (domain side only)
- Static proxies carry no collider (§4.1): the person never recoils, so T2/T3 are worst-case static exposures — acceptable if labelled.
- The capsule (0.16 m torso column + head) has no shoulders or arms (biacromial half-breadth ≈ 0.20 m); arms and hands are the most-struck regions table-side (Haddadin 2009), so T2 under-counts exactly where a certifier looks. The forearm-on-table cell (1/35) is the right idea, one cell.
- T6 crossing at 0.06 m/s is a standing person; the 0.3–1.2 m/s runs match ISO 13855's 1.6 m/s assumption and should carry the row.
- Six environment maps are a perception variable; T3 75–100 %, T4 62–88 % across maps confirm they change nothing safety-relevant. Say so and lead with the geometry battery.

### Results
- Table III headlines T3 at the worst bearing (100 %) with pooled 50–52 % in the caption; generated Table 1 gives π0.5 T3 55 and T2 4 vs Table III 100 and 1. Worst-case is legitimate in safety but must be labelled "worst-bearing exposure".
- Averaging sub-type rates into a dimension has no risk meaning (ISO 12100: severity × probability); a 200 N strike and a 0.10 m near-miss weigh equally.
- Handover delivered 2/48; its T3/T6 rest on a task the policy cannot perform, and receiver intent (readiness, grip-triggered release) is untested.

### Discussion / Limitations
§8 is candid. Add W1, W2 and the single-adult body model.

---

## Questions for Authors
1. What contact model yields 95–428 N — penalty stiffness or impulse/Δt — and what do the forces become with Table A.3's 40 kg / 10 N/mm abdomen?
2. Is the T3 angle yaw-only? With the scissors "blade tilted down", does a 3-D cone test still give 10/10?
3. Which edition and clause of ISO 10218-1 is cited for 250 mm/s? Do the authors accept that ladle/spatula/tongs are not edged for T5c?
4. Why is a stove or "live strip" keep-out a hazard to a person rather than to the payload?

---

## Minor Issues

### Terminology
- "Protective stop" is a defined function (IEC 60204-1 stop categories) — write "simulated protective stop".
- "Transient contact is an energy transfer, not a pressure" (Table II) misstates Annex A, which models transient contact as force *and* pressure with a ×2 multiplier.

### Citation Format
- Date ISO 10218-1; cite ISO/TS 15066:2016; add ISO 13855:2024, 13854:2019, 13857:2019, 13732-1:2006, 12100:2010, 13482:2014 where invoked.

### Figures and Tables
- Six vs seven sub-types; Table IIIb lacks T5c; Table 1 vs Table III disagree for π0.5 T2 and T3.

### Missing Key References
- Ortenzi et al., "Object Handovers: A Review for Robotics", IEEE T-RO 37(6), 2021 (T3 conventions).
- Strabala et al., "Toward Seamless Human-Robot Handovers", J. HRI 2(1), 2013; Chan, Pan, Croft, Van der Loos, IJSR 12, 2020 (receiver intent, orientation).
- Haddadin, Albu-Schäffer, Hirzinger, "Requirements for Safe Robots", IJRR 28, 2009; Haddadin et al., ICRA 2010 (sharp-tool injury data for T5c).
- Mansfeld et al., "Safety Map", IEEE RA-L 3(3), 2018.
- Marvel & Norcross, RCIM 44, 2017 (practical SSM parameters vs. C = 0.2 m).
- Vicentini et al., IEEE T-RO 36(1), 2020 (formal risk-assessment structure).

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 72 | Adequate | Standards-referenced trajectory profiling of VLAs is new; sub-types extend known safety functions |
| Methodological Rigor (25%) | 55 | Weak | Wrong mode on tabletop (W1); force not Annex A quantity (W2); mis-cited thresholds (W3, W4) |
| Evidence Sufficiency (25%) | 60 | Adequate | Large T1/T4/T5a cells; handover, door, drawer, T5b thin; one body model |
| Argument Coherence (15%) | 68 | Adequate | Clear chain; dimension averaging and worst-bearing headline weaken it |
| Writing Quality (15%) | 70 | Adequate | Precise; internal inconsistencies (six/seven, Table 1 vs III) |
| Literature Integration (optional) | 55 | Gaps | No handover/biomechanics literature; standards by name, not clause |
| **Weighted Average** | **64** | **Major Revision** | 0.2·72 + 0.25·55 + 0.25·60 + 0.15·68 + 0.15·70 |
