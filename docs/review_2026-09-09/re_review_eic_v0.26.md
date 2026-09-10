# Verification Review Report — v0.26 (EIC re-review, 2026-09-10)

## Decision
**Major Revision** (trajectory strongly positive; see rationale).

## Revision Response Checklist

### Priority 1 — Required Revisions (consensus K1–K11)

| # | Original Review Comment | Author's Claim | Response Status | Revision Location | Verified? | Quality Assessment |
|---|---|---|---|---|---|---|
| K1 | Person cell n=1; T2/T5/T6 carry a benign box | B1 pending (GPU down) | NOT_ADDRESSED | Table III; App. A | ✅ pending confirmed | Table III still 1/1 "illustrative", yet Table V lists a second blind person run (16 attempted, 4/4 violating): pooled 5/5 [57–100 %] is never surfaced in §5.2 or the abstract. |
| K2 | T4 cross-policy comparison metric-unmatched | Fig. 8 threshold curves, contact counts, "3 % vs 25 %/53 %" withdrawn; GR00T 3-D elsewhere pending B4 | PARTIALLY_ADDRESSED | §5.8, Fig. 8, abstract, §8 | ✅ | §5.8 now says the threshold sets the rate; abstract uses contact (π0.5 8/32; GR00T 8/8). Residual: §1 item 3 and App. B T4 still lead with the axis 25 %/75 %. |
| K3 | Hidden > blind completion hidden by conditioning | New §5.2 paragraph, Figs. 9–10, "all 37 non-completers stall at shelf", abstract sentence | PARTIALLY_ADDRESSED | §5.2 "Un-conditioned view", Figs. 9–10 | ⚠️ Partial | Paragraph and figures exist; Fig. 9 supports "stall at shelf". But Table IV implies 25+16 = **41**, not 37; **no abstract sentence exists**; Fig. 9 shows a *named* non-completer at progress ≈0.66, past the hazard, excluded by the blind+hidden scoping — say so. |
| K4 | Promptability probe cannot move its metric | B2 pending | NOT_ADDRESSED | §6, abstract | ✅ | §6 still calls the paired probe "adequately powered … a firm null" while Table V shows 8/8 → 7/7: the 33 → 29 % *is* the completion rate; the abstract headlines it. |
| K5 | No feasibility witness | §7 protocol item; §6 Alt-view (iii) withholds attribution for T4/T6 | PARTIALLY_ADDRESSED | §6 (iii), §7 | ✅ | Correct hedge; B6 pending. |
| K6 | Protective stop untested | §7 adds protective-stop layer; Table VI T6 names it | PARTIALLY_ADDRESSED | §7, App. D | ✅ | §5.7 hedged; App. B T6 still says avoidance "must be computed ahead" — soften. B7 pending. |
| K7 | Denominators switch silently; no CI on 10/10 | Appendix A Table V | PARTIALLY_ADDRESSED | App. A; §5.2; §6 | ⚠️ Partial | Table V sound for GR00T T1/T4/T6. Missing: §6 probe cells (T2, T6), all π0.5 T1 cells (22/22, 0/22, 16/16, 14/16 vs 15/16), stove margin-sweep cells (0/28, 22/25). §6 never states its rates are unconditioned; 10/10 has no CI in the main text. |
| K8 | TS 15066 status; 13482 uncited; SSM parameters asserted | Refs added; "carried into 10218-1/-2:2025"; Fig. 11 three parameterizations; T_r+T_s flagged assumed | PARTIALLY_ADDRESSED | §2, §5.4, Fig. 11, Table VI | ✅ | Bibliography, hedge and Fig. 11 verified; biped stop-time (B5) pending, flagged. |
| K9 | Identity; ~12k words; 700-word abstract | Title, 272-word abstract, §1 identity, §7 drops the question; 19 pp not cut | PARTIALLY_ADDRESSED | title, abstract, §1, §7 | ✅ (272 counted) | Identity resolved. Leftovers: §8 "undercuts the position"; §9 is still a position-paper conclusion (no benchmark, π0.5 or release). **19 pp vs 10 is a hard format block.** |
| K10 | No Fig. 1 / pipeline / scatter | Figs. 8–11 added; rest not | PARTIALLY_ADDRESSED | figures/ | ✅ four PDFs read | New figures match the text except the shield count (NEW-2). Fig. 1 missing — offline, cheap. |
| K11 | Missing literature; [32]–[34] placeholders | 34 → 55 refs | FULLY_ADDRESSED | §2, refs | ✅ | [22], [40]–[44], [45], [46]–[52], [53]–[55] present with real authors; ISO set complete. |

### Priority 2 — Suggested Revisions

| # | Original Review Comment | Response Status | Notes |
|---|---|---|---|
| S1 | A4 threshold curves T4/T6/T2 θ/T5 tilt | PARTIALLY_ADDRESSED | T4, T6 done; T2 θ, T5 tilt not. |
| S2 | A6 success-vs-safety scatter | NOT_ADDRESSED | Author: derivable, not drawn. |
| S3 | A7 pipeline figure; Franka overlays | NOT_ADDRESSED | G1 overlays only. |
| S4 | r0 MUST-3 leaderboard policies × T1–T6 | PARTIALLY_ADDRESSED | Table V lacks π0.5 T1 rows. |
| S5 | r0 MUST-8 release | PARTIALLY_ADDRESSED | Statement only; no link or scope. |
| S6 | r0 W3 headline powered runs | PARTIALLY_ADDRESSED | Abstract still leads with 10/10; Table V holds >100 completing blind carries, all violating, never pooled. |
| S7 | B1–B10 (GPU) | NOT_ADDRESSED | Author: chaowei driver mismatch since 09-08. Accepted. |

### Priority 3 — Nice to Fix

| # | Original Review Comment | Response Status |
|---|---|---|
| N1 | Fig. 1 overview, taxonomy diagram | NOT_ADDRESSED |
| N2 | T2 polar plot; dot plots with CIs | NOT_ADDRESSED |
| N3 | Scenario gallery | FULLY_ADDRESSED |

## New Issues (Discovered During Revision)

| # | Type | Location | Description |
|---|---|---|---|
| NEW-1 | Arithmetic | §5.2 | "37 non-completing blind and hidden episodes"; Table IV implies 41. |
| NEW-2 | Inconsistency | §5.2/abstract vs Table V vs Fig. 10 | Fire shield N=24: 0/10 and 33 → 42 % completion vs 0/8 and 33 % vs 0/7. One run, three counts. |
| NEW-3 | Under-reporting | Table III vs Table V | Person cell 5/5 pooled in the appendix, 1/1 in the text. |
| NEW-4 | Denominator | §1 pitch | "arm into a bystander on 25–100 % of *completing* episodes" — T4 is all-episodes (§5.5) and 25 % is the axis figure §5.8 retracts. |
| NEW-5 | Stale cross-refs | App. B T2 "(§5.4)"→§5.3; App. B T3 "§5.3"→§5.4; §5.6 "§4"→App. B | Reorder left dangling pointers. |
| NEW-6 | Conflation | Abstract | "π0.5 22/22, even with the hazard rendered visible" — 22/22 is geometric; rendered is 16/16. |
| NEW-7 | Asserted, not supported | §1 "What the policy should own" | No demand metric exists in §5; the 6/6 SSM-envelope violation (§5.4) is a 100 % stop-demand and should be named as such. "Protective stop is a fall hazard for a biped" is uncited and unmeasured (B5). |
| NEW-8 | Commitment | §7 Release, abstract | "Released" with no link, licence or scope; the letter reports earlier T6 and shield numbers could not be reproduced from dumps — scope the release to the Table V runs and attach an anonymized repository. |
| NEW-9 | Omission | §6 Alternative views | Omits the strongest objection on record (K4). |
| NEW-10 | Figure/text | §5.8 vs Fig. 8 | π0.5 axis rate at 0.20 m: text 6 %, figure ≈12 %. Verify. |

## Decision Rationale
The offline programme was executed with care and is verifiable: Table V, Figs. 8–11, Appendix D, the 55-reference bibliography, the T6 correction to 10/11 (no 13/14 residue anywhere), the benchmark identity and the Alternative-views paragraph all check against the manuscript. K11 is closed; K2, K3, K7, K8, K10 are substantively advanced.

Accept is excluded because two Critical items remain open in the text, not only in the GPU queue: K1 (the defining cell rests on n=1 while the appendix holds n=5) and K4 (§6 and the abstract present a saturated completion-rate comparison as a "firm null"). Minor Revision is excluded because the main text is at 190 % of the ICLR limit — a structural rewrite, not a trim — and the new material introduced ten inconsistencies, three in headline numbers. None of this needs the GPU.

## Residual Issues (prioritized by acceptance gain per hour)

1. **Headline the evidence already in Table V (1 day).** Every completing blind carry across three hazards, three seeds, two sweeps, YCB and the two-hazard scene violates (>100/100). Put that, not 10/35, in the abstract, §1 and §5.2; promote the person cell to 5/5; move Tables III–IV to the appendix. Answers r0 W3 and half of K1.
2. **Reframe the promptability probe (2 h).** State in §6 and the abstract that the T1/T6 paired null is a completion null; keep T2 (33→46 %) and π0.5 (14/16 vs 15/16) as the non-saturated cells; add K4 to Alternative views; reserve "firm null" for B2.
3. **Cut to 10 pages (2–3 days).** §2's novelty paragraph → Table I plus three sentences; shield-margin detail, the §5.4 derivation and §5.8 infrastructure notes → appendices; rewrite §9 as a benchmark conclusion.
4. **Fix NEW-1 to NEW-6, NEW-10; add π0.5 T1 rows and §6 cells to Table V (half a day).**
5. **Fig. 1 overview and the success-vs-safety scatter (1 day).**
6. **Release link with scope (1 day).**
7. **GPU, by yield once chaowei is up:** B1 (K1), B2 (K4), B4 (K2), B7 (K6), B5 (K8, NEW-7), B6 (K5).

Items 1–6 alone would, in my judgment, bring the paper to Minor Revision; B1 and B2 added would make it competitive.
