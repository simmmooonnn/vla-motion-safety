# Peer Review Report — Reviewer 3 (Presentation / Typesetting)

**Manuscript**: Execution-Phase Safety for Embodied VLA Agents: A Diagnostic Benchmark for How a Safe Task Gets Done (ICLR 2027 submission, `main.pdf`, 31 pp.)
**Review round**: 3 · **Date**: 2026-09-10
**Reviewer identity**: former ICLR/NeurIPS publication chair and scientific-figure designer; reviewed the compiled PDF page by page, consulting LaTeX/figure sources only to locate causes.

## Recommendation: Major Revision (presentation grounds) · Confidence: 5

## Summary
This review asks whether a reader can *see* the science. Currently: two figures have swapped graphics, in-text table numbers point at the wrong tables, two appendix sections are empty headings whose only content floated onto the previous page, subsections read "E.1 E.1", Fig. 1 is set in ~5 pt type, and the bibliography duplicates every year. All are mechanical (mostly `md2tex.py` artefacts) and fixable in a day, but together they signal "auto-generated" within 60 seconds, and the figure swap makes two results unverifiable from the PDF. The paper is anonymous and ends its main text on p. 10 (l. 535), but lacks Reproducibility and Ethics statements.

## Strengths
1. Clean template use: booktabs throughout, captions open with bold take-aways (Figs. 6–13).
2. Every prose number is traceable to Table 3 — the count table is the right idea.
3. Figs. 8, 9, 11, 13 are near publication quality once fonts and clipping are fixed.

## Weaknesses (headline)
Fig. 3 ↔ Fig. 12 swap; Roman-vs-Arabic table references; orphaned Appendices A/D; illegible Fig. 1; no Reproducibility/Ethics statements; bibliography artefacts.

---

## Layout and presentation issues

### Blocking
1. **Fig. 3 (p. 7) and Fig. 12 (p. 22) have swapped graphics.** Fig. 3's caption describes a two-panel T6 plot ("Left: carried-box speed … Right: box–person separation") but shows the single-panel T3a SSM envelope (`empirical_spine.tex` l. 20 includes `fig_ssm_envelope.pdf` under `\label{fig:t6contact}`); Fig. 12's caption describes the envelope but shows the two-panel T6 contact plot (`appendix_e…tex` l. 65). Every reference (p. 8 l. 388 "Fig. 12", l. 416 "Fig. 3"; p. 25 l. 1335; p. 27 l. 1417) therefore lands on the wrong plot. Fix: swap the two `\includegraphics` paths.
2. **Table references are hard-coded Roman numerals that no longer match.** "Table I" (p. 2 l. 056; p. 3 l. 161), "Table II" (p. 5 l. 266), "Table III, Appendix E" (p. 7 l. 357), "Table IV" (p. 7 l. 365; p. 20 l. 1078), "Tables III–IV" (p. 18 l. 951). Captions are Arabic and float order makes Table 3 = count table, Table 4 = standards mapping, so "Table IV" points at the wrong table (the intended ones are Tables 6–7). Fix: `\ref{tab:…}` everywhere.
3. **Appendices A (p. 15 l. 756) and D (p. 18 l. 947) are empty headings.** Their only content is a `[t]` float that landed on the *previous* page: Table 3 on p. 14, Tables 4–5 on pp. 17–18 (inside Appendix C, splitting a sentence at p. 16 l. 863 → p. 17 l. 901, leaving an 8-line hole at l. 895–900). Fix: one lead sentence per section plus `[htbp]`/`\clearpage` before the heading.
4. **Duplicated subsection numbers**: "E.1 E.1 Setup" … "E.8 E.8" (p. 18 l. 955; p. 20 l. 1058; p. 24 l. 1258; p. 25 l. 1300; p. 26 l. 1385; p. 27 l. 1404; p. 28 l. 1440) — numbers typed into `\subsection{}` titles. Fix: strip them.
5. **ICLR compliance.** No Reproducibility Statement or Ethics Statement (release info is buried in §7 l. 492–496); add both unnumbered after §9 (outside the limit) and check the 2027 CFP for LLM-usage disclosure. Main text ends p. 10 l. 535 — legal, zero slack.

### Major
6. **Fig. 1 (p. 6) is illegible at print size**: measured from the PDF, median text is 4.9 pt (min 4.7 pt) at `\linewidth`; the red/orange scene labels are ~5 pt. First cited p. 2 l. 072, appears four pages later. Fix: regenerate at `figsize=(5.5, 2.4)`, `fontsize≥8`, panels (a)/(b), place on p. 2.
7. **Clipped text**: Fig. 8 right title "T4 body-sweep: one margin, two geometri" (p. 20 l. 1042); Fig. 6 "11/11 stop only on contac" (p. 19 l. 984); Fig. 12/T6 legend "off-path: separation to the virtual cross…" and the annotation "…box half-extent ≈ 0.1" running off the axes (p. 22 l. 1160, 1166). Fix: `bbox_inches='tight'`, shorter strings, legends below axes.
8. **Fig. 6 (p. 19)**: label "100% (10/8)" should read 10/10 (`charts.py` l. 17); "25% pooled; 100% worst" is struck through by the T4 whisker (l. 986). Offset the annotation.
9. **Spaghetti plots**: the SSM envelope (now Fig. 3) has min font 3.8 pt / median 5.5 pt, ~40 traces and the "SSM requires a stop" label on the dashed bound; the T6 plot (now Fig. 12) overlays 20+ near-identical reds with a misaligned legend. Fix: per-condition median ± band, two colours, 7 pt.
10. **Fig. 9 (p. 21)**: "axis margin"/"capsule radius" labels collide with the guides and the y = 100 line; right-panel annotations sit on the curves; five-series rainbow legend at 5 pt. Red/green pairs here and in Figs. 10, 11, 13 are not colour-blind safe. Fix: Okabe–Ito palette, distinct markers, legend outside.
11. **Fig. 10 (p. 21)** legend sits inside the data region; **Fig. 11 (p. 22)** median tick text 4.7 pt.
12. **Table 1 (p. 4)**: `\scriptsize`, seven columns, citations inside cells ("SafeVLA / Safety-CHORES (Zhang et al., 2025a)" wraps to five lines), six-line caption. Fix: citations in the first column only, ✓/✗/≈ glyphs with a legend, "Policies evaluated…" into prose.
13. **Table 2 (p. 5)**: eight `\scriptsize` columns with 2–3-line wraps in every cell; "Status" mixes bold and prose. Drop Phase/Fixability (already in Appendix B) or use `sidewaystable`.
14. **Uncaptioned schema table (p. 5 l. 216–222)**: a floating table with `\label{tab:t1}` but no `\caption` (so any `\ref` resolves wrongly) that drifted away from its colon lead-in (p. 4 l. 215). Make it an inline `tabular` or caption it.
15. **Table 3 (p. 14)**: 45 rows; group rows ("T1 electric, keep-out 0.20 m — blind") indistinguishable from sub-rows ("blind, 3 seeds"); cells such as "contact (0 mm): 1 / 8" wrap. Fix: `\cmidrule` group headers, indented sub-rows, split by channel.
16. **Frame strips**: Fig. 2 (p. 6) top row at `\linewidth`, bottom at `0.9\linewidth` → misaligned; no "blind/shield" labels or keep-out overlay in the image. Fig. 4 (p. 18) squeezes eight stills into ~1.7 cm each. Fix: equal widths, overlay zone circle and path, row labels.
17. **§4 (p. 5 l. 264–269)** is a two-paragraph stub pointing to Appendix B; fold into §3.
18. **Citation form** "(International Organization for Standardization, 2025a;b)" occurs 19 times (e.g. p. 2 l. 090–093; p. 10 l. 512–516), usually right after the standard's own name. Fix: `author = {{ISO}}` → "(ISO, 2016)".
19. **Bibliography artefacts** (pp. 10–13): every entry repeats the year because venue strings with years sit in `howpublished` ("…2018, pp. 2669–2678, doi:…, 2018." l. 540–542; Kulić "2006 … 2005" l. 621–622); editorial notes leak in ("Concurrent work.", "(Spotlight)" l. 569, 578–580, 691); "NVIDIA. Isaac GR00T N1.6-3B. base model…" l. 655; inconsistent "et al." (l. 570, 680). Fix: proper `booktitle/journal/year` fields, delete notes.

### Minor
20. Abstract is 310 words with ~25 fractions; target ≤200 words and 3–4 numbers.
21. Extra blank lines between enumerate items (p. 2 l. 063–088) and above headings (l. 109–111; p. 5 l. 247–248, 261–263; p. 9 l. 476–478); tighten `\itemsep`.
22. Small-caps headings mangle identifiers: "T3A" (p. 8 l. 381; p. 25 l. 1300) vs "T3a" in text; "GR00T-ON-G1" (p. 28 l. 1441). Wrap in `\textnormal{}`.
23. ASCII tildes "~7 %", "~40 %", "~1.0 m" (p. 25 l. 1320; p. 29 l. 1530; p. 20 l. 1070) vs "≈" elsewhere; "θ°" (Table 2; p. 15 l. 777) mixes symbol and unit; "100 %" (spaced) vs "3%" (Fig. 8 caption l. 1054) and "100%/0%" (p. 23 l. 1200).
24. Main text cites appendix Figs. 9–13 eight times (p. 7 l. 360, 362; p. 8 l. 389, 400, 416, 429; p. 9 l. 433, 474) while carrying only three figures.
25. Near-verbatim duplicate paragraph "What is, and is not, new here." (§2 p. 3 l. 140–161 vs Appendix G p. 30 l. 1599 ff.); §8 (l. 502–521) and Appendix G are single 20–50-line paragraphs.
26. Fig. 1 caption (l. 286–291) and Table 1/3/4 captions run 5–7 lines; move method detail to text.

---

## Missing figures
1. **Scenario gallery (main text)**: one panel per T1–T6, rendered scene with the measured quantity drawn on it (keep-out circle, hazardous axis, SSM envelope, body capsule, tilt, crossing path). Replaces Figs. 2, 4, 5 and half of Fig. 1.
2. **Leaderboard-style results table in §5**: rows T1–T6 × policy, columns violation rate [Wilson CI], N, fixability verdict. The headline currently lives only in prose.
3. **Protocol/pipeline figure for §7**: scene → policy server → recorders → predicates → ablations → shield → feasibility witness.
4. **Redraw Fig. 1** as (a) three-axes diagram and (b) annotated scene, 8-pt text, consistent palette.
5. **Promote Fig. 7 (fixability) to §6 and Fig. 11 (shield overlay) to §5.2** — they are the visual proof of the two central claims.
6. **Unified chart style**: one `rcParams` block (≥7 pt at print, `figsize=(5.5, 2)`, Okabe–Ito palette, legends outside) shared by `charts.py`, `charts2.py`, `t6chart.py`, `overview_fig.py`.
