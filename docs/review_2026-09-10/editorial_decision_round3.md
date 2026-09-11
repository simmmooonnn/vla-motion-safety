# Editorial Decision — round 3 (compiled PDF v0.28 → v0.29), 2026-09-10

Panel: EIC (`r0_eic.md`), R1 methodology (`r1_methodology.md`), R2 domain/benchmark norms (`r2_domain.md`), R3 presentation/typesetting (`r3_presentation.md`), Devil's Advocate (`r4_devils_advocate.md`). All five reviewed `docs/overleaf_iclr/main.pdf` (v0.28) page by page. Every point below traces to one of those reports.

## Decision: MAJOR REVISION on presentation and completeness; science stable
Weighted scores 56–62; all five: Major Revision. Consensus: the argument (abstract → Fig. 1 → Tables I–II → §5 → §6–§9) holds and the reporting discipline is above the norm (EIC S1–S3, R1 S1–S4, R2 S1–S3, R3 strengths 1–3); the compiled artefact had compile-level defects and lacked ICLR benchmark scaffolding.

## Consensus findings (≥3 reviewers) and what v0.29 did
| # | Finding | Raised by | v0.29 |
|---|---|---|---|
| K1 | Fig. 3 (T6) and Fig. 12 (T3a) graphics swapped | EIC W1, R2 L1, R3 B1, DA M1 | fixed (`md2tex.py` FIGS) |
| K2 | "Table III/IV" hard-coded literals point at the wrong tables | EIC W1, R1 minor, R2 L2, R3 B2 | fixed: tables labelled by roman numeral, text uses `\ref`; Appendix E tables renumbered VIII/IX |
| K3 | Appendices A and D empty headings (tables floated to the previous page); "E.1 E.1" duplicated numbers | EIC L4/L8, R2 L3/L7, R3 B3/B4 | fixed: `[H]` tables in appendices, `\FloatBarrier`, lead sentences, heading numbers stripped |
| K4 | No main-text results table / leaderboard | EIC W2, R1 NICE-11, R2 MUST, R3 missing-2 | added Table III (channel × policy, N, rate, CI, command, shield) in §5.1 |
| K5 | No Reproducibility / Ethics / LLM-use statements; no repository URL | EIC W3, R3 B5, DA M6 | statements added after §9 (unnumbered); URL still pending (anonymized repo to be created) |
| K6 | Fig. 1 illegible (~5 pt) and four pages from its citation | EIC L6, R2 L4, R3 M6 | redrawn at 7–9 pt, panels (a)/(b), placed in §1 (page 2) |
| K7 | Fisher p for 8/8 → 0/8 is 1.6 × 10⁻⁴ two-sided, not < 10⁻⁴ | R1 W1 | fixed everywhere (text, captions, chart) |
| K8 | Appendix A incomplete; 109/109 nesting unstated | R1 W2, R2 detailed, DA M3 | rows added (off-path controls, shield-margin pools, T2, T5, T6 shield cells, probes, π0); ⊂ marks nested rows; composition of 109 in the caption |
| K9 | T6 "stops only on contact 11/11" overstates (6/11 stall, 5/11 brush past); crosser at 0.06 m/s; contact inferred, TTC unreported; "off-path" is person-absent | R1 W5, R2 W4, DA M2/m4 | abstract/§1/§5.7 reworded; TTC and the 0.06 m/s caveat added; control renamed "person-absent"; box half-extent range and the missing contact log stated |
| K10 | Table I mischaracterizes peers (SafeManip has a prompt ablation with the same null; ForesightSafety 4 + 7 partial; LIBERO-Safety has a CBF mitigation; HazardArena has static person assets); claim (iv) over-broad | R2 W1/W2 | fixed; SafeManip's null cited in §2 and §6; claim (iv) narrowed |
| K11 | §6 "powered for a moderate effect" is wrong (McNemar needs ≥ 6 discordant pairs) | R1 W4, DA M5 | replaced by the minimal-detectable-effect statement |
| K12 | Title cell (hazardous payload past a person) never instantiated — every payload is a box | DA C1, R1 detailed, R2 W3 | §2(ii) and Table I now say "proxy payload, 5 completing carries, not yet powered"; §9 sentence unfused |
| K13 | Chart defects: "10/8" label, T2 drawn as 100 %, clipped titles/legends, 5 pt fonts | EIC L7/L9, R2 L8/L9, R3 M7–M11 | fixed; fonts ≥ 7 pt; tight bounding boxes |
| K14 | Bibliography artefacts (years repeated, notes leaking, ISO as a 40-character author) | R3 M18/M19 | fixed in the bib generator (ISO short author; year regex; notes dropped) |

## Still open after v0.29 (offline)
- Anonymized repository URL + licence + `thresholds.yaml` (K5; DA MUST-4).
- Scenario gallery (one still per type with the scored quantity drawn) and a protocol/pipeline figure (EIC/R2/R3).
- Success-vs-safety scatter per cell (R1, R2, R3).
- Table I / Table III still `\scriptsize`; Table V long (R3 M12–M15): split by channel, indent sub-rows.
- Fig. 2 frame strips: equal widths, keep-out overlay (R3 M16, EIC L10).
- Abstract 255 words (target ≤ 200 per R3).

## Still open (GPU)
T6 controls — collider-off twin, crossing-speed sweep 0.3–1.2 m/s, PhysX contact logging, ≥ 0.60 m shield (R2/DA MUST); hazardous-payload-past-person cell N ≥ 20 (K12); feasibility witnesses for T3a/T4/T6 and a scripted detour on the Franka (DA SHOULD-8); non-ceiling T1 ablation (R1 MUST-7); GR00T 3-D T4 sweep; third policy at full N; language-following control + navigate_cmd logs.
