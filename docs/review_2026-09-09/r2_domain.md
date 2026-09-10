# Peer Review Report

## Manuscript Information
- **Title**: Execution-Phase Safety for Embodied VLA Agents: A Taxonomy and a Case for Behavioral Safety Competence (v0.24)
- **Review Date**: 2026-09-09 · **Round**: 1 (ICLR 2027)

## Reviewer Information
- **Role**: Peer Reviewer 2 (Domain)
- **Identity**: VLA-safety researcher (author on a 2026 LIBERO-Safety/SafeVLA-Bench-generation benchmark); knows HRI handover work and ISO/TS 15066.
- **Focus**: accuracy of Table I and the five "first" claims (§2); whether T1–T6 adds to existing taxonomies; whether one humanoid task supports field-level claims. ✓ = verified today against arXiv/ISO sources.

## Overall Assessment
- **Recommendation**: **Major Revision** · **Confidence**: 4

**Summary.** The paper proposes a third VLA-safety axis, a six-type taxonomy with a six-field tuple, and measures GR00T N1.6/G1 on a box carry plus π0.5/Franka on two channels. Its reading of the 2026 benchmark cluster is careful and largely accurate ✓. The genuinely new elements are the *fixability* and *phase* fields, human-referenced SSM scoring (T3a), and the axis-vs-capsule lesson (T4). But the flagship first claim — a *carried hazard past a passive bystander* — rests on one completing carry (Table III); the channel list is largely inherited without a crosswalk; the standard cited is superseded; and the HRI-safety and VLA-safety-filter literatures that supply the paper's own remedies are absent. Fixable, but not in a minor pass.

## Strengths
**S1 — Verifiable positioning (§2, Table I).** SafeVLA-Bench (STL, SBU, ISO/TS 15066 force proxy, "bystanders" = objects), SafeManip (LTLf), Safety-CHORES (mobile, no humans), HazardArena (ISO 13482, semantic human) and R2HandoverSim (UR5e, static hand) are all fairly described ✓.
**S2 — Standards-grounded T3a (§5.3).** Inverting protective distance to v_allow(d) is the first VLA-benchmark use of SSM *relative to a human* I can find; SafeVLA-Bench uses only object-force ceilings ✓.
**S3 — The T4 metric lesson (§5.9)** — axis distance inverts a policy comparison versus body-capsule contact — is reusable benchmark design.
**S4 — Fixability as a field (§3.2, §6).** No peer pairs each predicate with prompt/perception/shield ablations ✓ (HazardArena has one defense; LIBERO-Safety an L2 paraphrase tier).

## Weaknesses
**W1 — First-claim (ii) is a scene design, not a measurement (§2, §5.2, Table III).** The person cell has 1/11 completing carries; T2, T5, T6 carry a *box*. "Carries a hazardous object past a passive bystander" is instantiated but unmeasured, yet it is Table I's headline differentiator. *Fix:* re-run person-on-path with a hazard-class payload (fire setup gives 33 % completion) to n≥20; meanwhile reword (ii) as "we instantiate". **Critical.**
**W2 — Taxonomy delta not shown (§4).** ForesightSafety's Safe-Core already lists Force/Torque, Thermal, Spatial Boundary, Collaborative, Temporal ✓; SafeVLA-Bench's eight clauses cover tilt, self-collision, contact force ✓; ISO 13482 and Lasota, Fong & Shah (*Found. Trends Robotics* 2017) give hazard/method taxonomies. T1–T6 adds the human referent, phase and fixability — the reader must infer this. *Fix:* crosswalk table plus "channels inherited, fields new". **Major.**
**W3 — Superseded, mis-scoped standard (§2, §5.3, §8).** ISO/TS 15066:2016 was withdrawn into ISO 10218-2:2025 (in force Apr 2025 ✓). Both are *industrial*; a domestic humanoid falls under ISO 13482:2014 (named in §2, absent from the bibliography). *Fix:* cite ISO 10218-1/2:2025, keep TS 15066 as formula source, add ISO 13482. **Major.**
**W4 — Remedy literature missing (§2, §6, §7).** "Fixable by an external layer" already has non-oracle instantiations: VLSA [22] (in bibliography, never cited), attention-guided CBF filters (2606.09749 ✓), barrier-enhanced/constrained flow matching (2607.29569, 2607.01378 ✓), SPARK — safe control on the Unitree G1 itself (Sun et al., IFAC 2025 ✓), ISO 10218 SSM-in-CBF (Parma et al., 2606.13203 ✓). Classical HRI safety is absent: Kulić & Croft danger index (*RAS* 2006), Haddadin et al. (*T-RO* 2017; *IJRR* 2012) for T3b, Sisbot & Alami human-aware manipulation (*T-RO* 2012), Marvel & Norcross SSM (*RCIM* 2017), Mainprice & Berenson anticipation (IROS 2013) for T6, Habitat 3.0's human-collision rate (Puig et al., ICLR 2024 ✓). *Fix:* one paragraph plus a shield baseline from this list. **Major.**
**W5 — T2 lineage under-credited; T6 fixability over-generalized (§5.4, §5.7).** Handle-first presentation is a decade-old convention (Cakmak et al., IROS 2011; Aleotti et al., *IJSR* 2014; Chan et al., *IJSR* 2020), not a 2026 result; [32]–[34] have placeholder titles (real: Biagi et al. ×2; Zhang, Dhafer, Dong & Hao ✓). "Reactive repulsion cannot fix T6" tests one design; the ISO-canonical reactive response is a *protective stop*, untested. *Fix:* cite the lineage; add a stop-on-TTC baseline before claiming anticipation is required. **Major.**

## Detailed Comments
- **§2 firsts.** (i) no counterexample found ✓ — keep "to our knowledge". (ii) W1; cite HazardArena's "knife toward a crawling baby" as the semantic cousin. (iv) LIBERO-Safety's margin is a mesh-level check, already all links ✓; your delta is the *full-body bystander*, not link count. (v) "none of the above does" → "none pairs all three".
- **Table I.** LIBERO-Safety's proxy is a MANO *hand* ✓ — say so (strengthens your case, weakens ≈T6). SafeManip also scores collision/contact ✓. HazardArena is multi-room MuJoCo, not tabletop ✓. SafeVLA-Bench: 9 entries, 8 distinct policies ✓.
- **§5.9.** 53 % body contact "beside the workspace" of a tabletop arm suggests the proxy sits inside nominal reach; justify placement or report violation-vs-distance.
- **§6.** On π0.5 the command drops success 100→62 %: the prompt is not ignored, it is unhelpful.

## Questions for Authors
1. Can the fire-run configuration deliver n≥20 completing person-on-path carries with a hazardous payload?
2. Does ForesightSafety's "Collaborative" category overlap T4/T6? What distinguishes yours beyond the human being physical?
3. Would a protective-stop baseline prevent the 13/14 T6 near-misses? If so, withdraw "anticipatory".

## Minor Issues
- [22] uncited; replace [32]–[34] placeholders; add ISO 13482:2014 and ISO 10218-1/2:2025.
- Abstract (~900 words) and 中文摘要 exceed ICLR norms; cut to ≤250 words.
- Table II: add n per cell.

## Dimension Scores
| Dimension | Score | Descriptor |
|---|---|---|
| Originality (20%) | 68 | Adequate — fields new, channels inherited |
| Methodological Rigor (25%) | 62 | Adequate — one task, oracle shield |
| Evidence Sufficiency (25%) | 56 | Weak — key cell n=1, box proxies |
| Argument Coherence (15%) | 74 | Adequate — §2 overstates |
| Writing Quality (15%) | 66 | Adequate — over-hedged |
| Literature Integration | 64 | Adequate — classics/standards/filters missing |
| **Weighted** | **64** | **Major Revision** |

## Missing experiments and figures
*What a LIBERO-Safety / SafeVLA-Bench reader expects and does not find.*

**MUST**
1. **Figure 1 overview** — three axes, six types, the tuple. Every peer opens this way; your eight figures are all results. *1–2 days.*
2. **Taxonomy crosswalk table** (W2). *1 day.*
3. **Fill the carried-hazard-past-person cell** (W1), n≥20. *1–2 H100-days.*
4. **Success-vs-safety scatter** (SBU-style, one point per policy×channel×condition); peers lead with it, and it answers your success-confound worry. *Half a day.*
5. **Standards update** (W3). *None.*

**SHOULD**
6. **Multi-policy leaderboard on T1/T4**, ≥3–4 policies (finish π0; add OpenVLA-OFT or GR00T N1.5 via your server swap). Peers report 6–12. *2–3 GPU-days per policy.*
7. **Non-oracle mitigation comparison**: protective-stop SSM plus one perception-fed filter (VLSA / attention-guided CBF / SPARK on G1). Turns the shield into a baseline and tests the T6 claim. *1–2 weeks.*
8. **Head-to-head on a shared scene**: LIBERO-Safety's HRI suite (Franka; GR00T N1.6 and π0.5 already scored there ✓) with your capsule metric and ablations. *~1 week if assets public.*
9. **Scenario gallery**, **polar T2 plot**, **SSM envelope plot** (speed vs separation with v_allow(d)). *1–2 days.*

**NICE**
10. Real hazardous objects for T2 — needs a cup-competent checkpoint. *Weeks.*
11. Human-trajectory crosser (e.g., THÖR) for T6. *2–3 days.*
12. Proxemics-grounded bystander distances, violation-vs-distance curve. *1 GPU-day.*
13. Any hardware frame or sim-to-real note (SafeVLA has one). *High; optional.*
