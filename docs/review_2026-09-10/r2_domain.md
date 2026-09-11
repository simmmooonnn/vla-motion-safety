# Peer Review Report

## Manuscript Information
- **Title**: Execution-Phase Safety for Embodied VLA Agents: A Diagnostic Benchmark for How a Safe Task Gets Done
- **Manuscript ID**: ICLR 2027 submission, `main.pdf` (31 pp.)
- **Review Date**: 2026-09-10
- **Review Round**: Round 3

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 (Domain)

### Reviewer Identity
Author of a 2026 VLA-safety benchmark, reviewing an adjacent benchmark submission.

### Review Focus
Benchmark completeness (figures, leaderboard, thresholds, artefact); fairness of Table 1, §2 and Appendix D to peers and ISO clauses; taxonomy legibility; credibility of the T6 contact reading.

---

## Overall Assessment

### Recommendation
- [x] **Major Revision**

### Confidence Score
4

### Summary Assessment
The paper defines execution-phase safety as a third axis, gives a six-type taxonomy, and instantiates it on GR00T N1.6/G1 carrying a hazard past a bystander, porting T1/T4 to π0.5/Franka. The intersection claim (p.3 L154–159) survives my check, and Table 4 cites the right clauses (SSM 5.5.4, PFL 5.5.5, ISO 13855 K = 1.6/2.0 m/s, ISO 10218-1 250 mm/s). As a *benchmark* it is below the 2026 cluster's bar: two policies, 6–35 episodes per cell, three main-text figures — Fig. 3 is the wrong graphic — no main-text leaderboard, no success–safety plot, no published thresholds, no repository URL anywhere in the PDF. Table 1 mis-scores SafeManip (its §6 prompt ablation is this paper's "name the hazard" axis with the same null) and inflates ForesightSafety's policy count; claim (iv) "every predicate with fixability ablations" is contradicted by §5.4–5.6. The T6 headline ("stops only on contact, 11/11") overstates §E.7 (6/11 stall, 5/11 brush past); its "off-path" control is person-absent. The ideas merit publication; the packaging does not yet.

---

## Strengths

### S1: The intersection is real
p.3 L154–159. My search found no humanoid-locomotion + bystander execution suite; the nearest uncited work (ROBOSHACKLES 2606.18632, TouchSafeBench 2605.31196) is VLM/video-level.

### S2: Standards mapping is competent
Table 4 (p.17): clauses check out; the SSM-only vs PFL-eligible regime column is something no peer offers.

### S3: Threshold-curve discipline
Fig. 9 (p.21), §5.8 (p.9 L432–435): full curve plus contact count properly answers SafeVLA-Bench's threshold-sensitivity table.

---

## Weaknesses

### W1: Table 1 / §2 / Table 5 mischaracterize peers
**Problem**: SafeManip "Fixability ablation: No" (p.4 L179–180) — SafeManip §6 runs regular / short-conservative / long-constraint prompts on GR00T-tpt: SR 43.9→26.4→6.9 %, violation 71.8→69.4→65.1 %, the same design and result as p.9 L454–456 (π0.5: success 100→62 %, violation 94→88 %); Appendix G "which none of the above does" (p.31 L1630–1631) is false. ForesightSafety "≈10" policies (p.4 L167): leaderboard has 4, seven scatter-only. Table 5 maps ForesightSafety "Collaborative (proximity)" to T3a (p.18 L930), but that category is dual-arm separation — as Table 5's own T4 cell says. LIBERO-Safety's chunk-level CBF mitigation earns "No" (p.4 L173) while HazardArena's SOL earns "defense baseline".
**Why it matters**: the promptability null is not new.
**Suggestion**: correct the cells; cite SafeManip §6 as corroboration in §6; restrict claim (iv) to T1.
**Severity**: Major

### W2: Claim (iv) contradicted by the paper's own evidence
**Problem**: "pairs every predicate with fixability ablations" (p.3 L158–159; Table 1 p.4 L188–190). T3a, T4, T5 carry none (§5.4–5.6); render/hide is T1-only (Table 7).
**Suggestion**: "pairs the headline predicate (T1)…"; run T4 ablations.
**Severity**: Major

### W3: Not yet a benchmark by the field's own bar
**Problem**: Norm evidence (survey of six 2026 suites, verified from arXiv): overview figure and per-category breakdown 6/6; ≥50 episodes/cell, pipeline figure, success–safety analysis 5/6; ≥6 policies 4/6. Here: 2 policies (+1), 6–35 episodes/cell (Table 3), leaderboard and per-channel figures appendix-only (Figs. 6–8), no success–safety plot although p.9 L450–452 invites one, no repository URL (release asserted p.10 L493–494), thresholds "illustrative" (p.16 L855–856), canonical values only promised (p.31 L1652–1658).
**Suggestion**: see final section.
**Severity**: Major

### W4: T6 headline overstates §E.7
**Problem**: "stops only on contact … 11/11" (p.1 L031–032) vs §E.7: stall 6/11, brush past 5/11 (p.27 L1417–1419). The stall is against an immovable kinematic collider, which physics alone produces (conceded p.27 L1423–1426). "0/3 off-path" is a person-absent virtual-crosser control (p.27 L1420–1421; Fig. 12 legend). The crosser moves at 0.06 m/s (p.8 L413), one-twentieth of walking speed.
**Suggestion**: "reaches contact distance without slowing (11/11); stalls at contact 6/11"; relabel the control. Settling controls: collider-off twin (unchanged speed through the capsule = physics stall), speed sweep 0.3–1.2 m/s, a person who stops 0.5 m short.
**Severity**: Major

### W5: Taxonomy lost its intuition
**Problem**: §4 is two sentences (p.5 L265–269); Appendix B's harm-channel prose (p.15 L773–775) is gone; Table 2 at ≈6 pt is the sole carrier.
**Suggestion**: six-panel gallery, one still per type with the scored quantity drawn.
**Severity**: Minor

---

## Detailed Comments

### Literature Review
Add ROBOSHACKLES and TouchSafeBench. HazardArena's ISO 13482 grounding is correct (p.31 L1643) and its scenes hold static person assets, so "semantic category only" (p.4 L183) should read "static person asset, no contact scored".

### Standards (Appendix D)
Table 5 "ISO 200 N" (p.18 L931–932) is not an ISO/TS 15066 Annex A value (chest 140 N, back 210 N); attribute it to SafeVLA-Bench. d0 = 0.94 m uses C = 0.2 m (p.25 L1333); ISO 13855's body-detection C is ≥0.85 m, so even the "walking-human" line is lenient.

### Results
"109/109" (p.1 L024) sums Table 3 blind rows only if the "3 seeds" rows include the primary cells (40+36+5+6+22); the caption (p.14 L707) suggests otherwise.

---

## Questions for Authors
1. Is an anonymized repository accessible? URL?
2. With the crossing person's collider removed, does the box still stall?
3. Which Table 3 rows nest, so that 109 is reproducible?

---

## Dimension Scores

| Dimension | Score | Descriptor |
|---|---|---|
| Originality (20%) | 66 | Adequate+ |
| Methodological Rigor (25%) | 55 | Adequate |
| Evidence Sufficiency (25%) | 46 | Weak |
| Argument Coherence (15%) | 62 | Adequate |
| Writing Quality (15%) | 55 | Adequate |
| Literature Integration | 66 | Adequate+ |
| **Weighted Average** | **56** | **Major Revision** |

---

## Layout and presentation issues

1. p.7 L324–349, Fig. 3 — **Critical**. Graphic is the T3a SSM envelope (`fig_ssm_envelope.pdf`) under the T6 caption; p.22 Fig. 12 is the T6 contact plot under the T3a caption. Swap the `\includegraphics`.
2. p.7 L356, L364; p.18 L951 — **Major**. "Table III/IV" cited; tables are numbered 1–7, intended are Tables 6–7. Use `\ref`.
3. p.14 Table 3 precedes its section; p.15 L756 and p.18 L947 are empty headings — **Major**. Add body text, `[H]`.
4. p.6 L270–285, Fig. 1 — **Major**. Left panel ≈5 pt text box; right panel no rendered scene.
5. p.6 L292–305, Fig. 2 — **Major**. Eight ≈2 cm thumbnails, keep-out zone not drawn; pass vs detour invisible. Four per row, zone and path overlaid.
6. p.18 L938–945, Fig. 4 — **Minor**. ≈1.6 cm stills, bystander barely visible, stranded in Appendix D.
7. p.18 L955, p.20 L1058, p.24 L1258, p.25 L1300, p.26 L1385, p.27 L1404/L1440 — **Minor**. Duplicated labels "E.1 E.1 Setup".
8. p.22 Fig. 12 right — **Minor**. Legend clipped and overlapping.
9. p.19 Fig. 6 — **Minor**. Right-edge label clipped; inherits W4 wording.
10. p.5 Table 2 — **Minor**. ≈6 pt, eight columns; move "Status" to its own strip.

---

## Missing figures and experiments

**No-GPU**
- MUST: fix items 1–3 (hours).
- MUST: main-text leaderboard — condensed Table 3 (type × policy: n, rate, Wilson CI) in §5 (hours).
- MUST: six-panel scenario gallery with scored quantity drawn (1 day, existing renders).
- MUST: repository link plus canonical-thresholds table (keep-out per hazard class, θ, SSM parameters, T4 margin, tilt, TTC) (hours).
- SHOULD: success-vs-safety plot per cell with 2×2 safe/unsafe × success/fail decomposition (SafeManip Fig. 2b) (hours).
- SHOULD: pipeline figure (hazard placement → recorders → predicates → CI) (1 day).
- SHOULD: cite SafeManip §6, ROBOSHACKLES, TouchSafeBench (hours).

**GPU (when the node returns)**
- MUST: T6 collider-off twin + speed sweep {0.06, 0.3, 0.6, 1.2 m/s} + stops-short control, 24 episodes each (~120).
- MUST: ≥50 completing carries in the T1 and T6 headline cells (~150 attempted per cell).
- SHOULD: third policy at full power (π0, GR00T N1.5, or OpenVLA-OFT) for a three-row leaderboard (~200).
- SHOULD: name/hide/shield ablations on T4 and T3a (~150).
- NICE: GR00T 3-D sweep at all four T4 positions; PhysX contact-force logging; filled-cup T5.
