# Response to the 2026-09-09 panel — what changed in v0.25 → v0.26

Manuscript: `docs/execution_phase_safety_position_paper_draft.md` (v0.26, 2026-09-10); LaTeX build `docs/overleaf_iclr/main.pdf` (28 pp, main text 19 pp). Roadmap item numbers refer to `editorial_decision.md`.

## A. Offline items
| Item | Author's claim | Location |
|---|---|---|
| A1 unified count table | Added Appendix A, Table V: attempted / completing / violating with Wilson 95 % CIs for every GR00T T1 cell (incl. seeds, sweeps, shields, YCB, multi-hazard), T4 GR00T and π0.5 (axis + 3-D, with contact counts), T6 paired by episode. | Appendix A |
| A2 un-conditioned T1 | New paragraph "Un-conditioned view (every episode)" + Fig. 9 (progress of every episode) + Fig. 10 (top-down overlays). Result: hidden > blind completion (20/36 vs 10/35, p = 0.03) but all 37 non-completers stall at the shelf; none stops in the corridor. Abstract sentence added. | §5.2, Figs. 9–10, abstract |
| A3 GR00T T4 on the matched capsule | Confirmed in code that the 3-D "violation" equals 0.26 m to the axis; threshold curves for GR00T (all 32 episodes) and π0.5 (axis and 3-D) in Fig. 8; contact counts (π0.5 8/32, GR00T 8/8 at right-pick). §5.8 T4 paragraph rewritten to say the geometry, not the policy, sets the rate; abstract and §8 corrected; the "3 % vs 25 % / 53 %" reading withdrawn. GR00T 3-D at the other three positions still needs the GPU (B4). | §5.8, Fig. 8, abstract, §8 |
| A4 threshold sensitivity | T4: Fig. 8 (0.05–0.30 m). T6: all on-path minima 0.263–0.307 m; 0.25 m → 0/13, 0.35 m → 13/13; stated in §5.7 and §8; separations/TTCs reported in Appendix A. T2 θ and T5 tilt curves not added. | §5.7, §8, Fig. 8 |
| A5 SSM envelope figure | Fig. 11: six speed–separation traces vs v_allow(d) (three parameterizations) and the 250 mm/s line. | §5.4, Fig. 11 |
| A6 success-vs-safety scatter | Not added (the count table gives both rates per cell; a scatter is trivial to derive but not yet drawn). | — |
| A7 Fig. 1 overview / pipeline / overlays | Overlays added (Fig. 10). Overview and pipeline figures not yet drawn. | Fig. 10 |
| A8 standards table + crosswalk | Appendix D: Table VI (T1–T6 ↔ ISO 12100 / 10218-2 / TS 15066 / 13482, SSM-only vs PFL-eligible, our proxy) and Table VII (crosswalk vs ForesightSafety, SafeVLA-Bench, LIBERO-Safety, SafeManip, HazardArena). Pointer added at the end of §3.3. | Appendix D, §3.3 |
| A9 bibliography | 34 → 55 references, web-verified: real authors for [32]–[34]; ISO 13855:2024; ISO 10218-1/-2:2025, ISO 13482:2014, ISO/IEC TR 5469:2024, ISO 12100:2010; VLSA [22] now cited with the VLA filter cluster [40]–[44]; classical HRI safety [46]–[52]; handover lineage [53]–[55]; Habitat 3.0 [45]. ISO/TS 15066 described as "carried into ISO 10218-1/-2:2025" (formal withdrawal could not be confirmed). | §1, §2, §8, references |
| A10 restructure | Title → "A Diagnostic Benchmark for How a Safe Task Gets Done"; abstract 272 words; §1 opens with the two-sentence pitch and the diagnostic-benchmark identity; new §1 paragraph "What the policy should own" (demand-rate reframing); §4 per-type blocks → Appendix B; §5.8 reproducibility → Appendix C; §5 reordered T1 → T6; §6 "Alternative views"; §7 adds feasibility witness + protective-stop layer + release statement, drops the position-vs-benchmark question. Main text is 19 pages (limit 10): the §5 prose compression and moving most figures to the appendix are NOT done. | title, abstract, §1, §4–§7 |

## Corrections of earlier claims (found during A1/A2)
- T6: reproducible pairing gives 10/11 completing carries within 0.30 m over three seeds (12/13 with a mid-corridor start); earlier 13/14 and completion 14/24 could not be reproduced → replaced everywhere (91 %, 11/24).
- Electric-strip shield: earlier text said the run "did not yield enough completing carries"; the dumps show 12 completing carries of which 6 still violate at the 0.50 m margin (0/3 at ≥ 0.60 m). §5.2 now reports margin dependence (stove 0/28 at ≥ 0.60 m vs 22/25 at ≤ 0.50 m; person 2/10; YCB 1/13; multi 0/6).

## B. GPU items — all pending (chaowei driver mismatch since 2026-09-08; admin reboot required)
B1 person-cell N ≥ 20 · B2 non-ceiling 2×2 ablation · B3 language-following control · B4 GR00T T4 3-D sweep · B5 G1 stop-distance test · B6 feasibility witnesses · B7 protective-stop layer · B8 navigate_cmd logs + hazard-free baseline · B9 same-embodiment pair / OpenVLA-OFT · B10 fine-tune on detour demos. Scripts for B7-adjacent anticipatory shield are staged.

## C. Figures
Present: T1 frames, T4/T6 frames, generality gallery, shield frames, rates bar, fixability panels, cross-policy bars, bimodal scatter, T4 threshold curves (new), T1 every-episode (new), top-down overlays (new), SSM envelope (new). Missing: Fig. 1 overview, pipeline/scene-construction figure, taxonomy diagram, success-vs-safety scatter, T2 polar plot, per-cell dot plots with CIs.
