# Peer Review Report

## Manuscript Information
- **Title**: Execution-Phase Safety for Embodied VLA Agents: A Diagnostic Benchmark for How a Safe Task Gets Done
- **Manuscript ID**: overleaf_iclr/main.pdf (31 pp.; main text pp. 1–10, lines 000–535)
- **Review Date**: 2026-09-10
- **Review Round**: Round 3 (compiled PDF)

## Reviewer Information
### Reviewer Role
EIC / ICLR 2027 Area Chair (robot learning, embodied agents, benchmarks)
### Review Focus
Does the 10-page main text stand alone; ICLR benchmark-paper expectations; page-level presentation.

---

## Overall Assessment
### Recommendation
- [x] **Major Revision** — the science has stabilised, but the compiled PDF has compile-level defects (swapped figures, broken table references, uncited floats, empty appendix sections) and lacks standard ICLR benchmark scaffolding. All fixes are no-GPU.

### Confidence Score
4

### Summary Assessment
The paper defines execution-phase safety as a third VLA-safety axis, gives a six-type schema (Table 2, p. 5), and instantiates it on GR00T-N1.6/G1 with two channels ported to π0.5/Franka. At the argument level the cut works: abstract → §1 → §5 → §6 → §9 is coherent and the attribution-pending labelling (p. 10, lines 505–508) is exemplary. At the artefact level it fails: Fig. 3 (p. 7) and Fig. 12 (p. 22) have swapped graphics; "Table III/IV" point at tables numbered 6/7; Figs. 4–8 are never cited; Appendices A and D are bodiless headings; there is no main-text results table, no Reproducibility or Ethics Statement, no artefact URL. The PDF reads as unproofed after compression.

---

## Strengths
### S1: The first two pages sell the framing
Abstract (p. 1, lines 014–035), contribution list (p. 2, lines 065–087) and "demonstrated versus proposed" (lines 104–107) separate measured from proposed.

### S2: Concrete benchmark positioning
Table 1 (p. 4) compares six 2026 suites on six axes, with policy counts in the caption (lines 166–167).

### S3: Quantified limitations
§8 (p. 10, lines 502–521) names every small cell, the 5/5 person cell, the oracle-fed shield, the collider-free proxies.

---

## Weaknesses
### W1: Swapped figures and broken cross-references
**Problem**: `fig:t6contact` embeds `fig_ssm_envelope.pdf` (Fig. 3, p. 7, lines 324–349: a "Left/Right" T6 caption over a single-panel plot with an "SSM requires a stop" band); Fig. 12 (p. 22, lines 1134–1174) shows the two-panel T6 plot under the T3a caption, so §5.4 (p. 8, line 389) and §5.7 (line 416) cite the wrong figure. "Table III" (p. 7, line 357) and "Table IV" (p. 7, line 364; p. 18, line 951; p. 20, line 1078) are hard-coded literals; the tables are 6 and 7 (pp. 23–24).
**Why it matters**: a reviewer checking the headline T6 claim finds a figure contradicting its caption.
**Suggestion**: swap the `\includegraphics`; replace literals with `\ref`.
**Severity**: Critical

### W2: No compact results table in the main text
**Problem**: §5 (pp. 6–9) is prose carrying ~45 inline ratios; the only tabular result is Table 2's Status column; the count table (Table 3) sits on p. 14.
**Why it matters**: without a channel × policy × {N, rate, CI, ablation Δ, shield Δ} table the paper reads as a compressed position paper.
**Suggestion**: promote a 6-row × 2-policy summary of Table 3 into §5.1.
**Severity**: Major

### W3: Missing ICLR benchmark scaffolding
**Problem**: no Reproducibility Statement, Ethics Statement or LLM-usage line; no repository URL (p. 10, line 493 only promises one); no versioned thresholds file.
**Why it matters**: page-budget-free items an AC checks first.
**Suggestion**: add both statements after §9; anonymous 4open/Zenodo URL in abstract and §7.
**Severity**: Major

### W4: Section balance after compression
**Problem**: §4 is four lines (p. 5, lines 266–269); §8 is one 20-line paragraph; Fig. 1 is cited on p. 2 (line 072) but appears on p. 6.
**Why it matters**: the abstract → Fig. 1 path breaks; the overview arrives after both tables.
**Suggestion**: Fig. 1 to p. 2 (`[t]`), fold §4 into §3.2, bullet §8.
**Severity**: Major

---

## Detailed Comments
- **Abstract** (p. 1, lines 014–035): 22 lines of statistics; keep four headline rates.
- **§5**: every number traces to Table 3 — commendable. **§6 "Alternative views"** (p. 9, lines 465–475) and **§9** match the claims.
- **§2** (p. 3, lines 139–161): 23-line citation block duplicated in Appendix G (p. 30, lines 1598–1619).

## Questions for Authors
1. Which graphic was intended for Fig. 3, and does §5.7 (p. 8, lines 413–422) describe the two-panel plot now on p. 22?
2. At which URL will the repository and Appendix A logs be reachable during discussion?
3. Is Table 2's Status column the intended "leaderboard cell", or will a channel × policy table be added?

## Dimension Scores
| Dimension | Score | Descriptor |
|---|---|---|
| Originality (20%) | 72 | Strong |
| Methodological Rigor (25%) | 62 | Adequate |
| Evidence Sufficiency (25%) | 55 | Adequate |
| Argument Coherence (15%) | 70 | Strong |
| Writing Quality (15%) | 45 | Weak |
| **Weighted Average** | **61** | **Major Revision** |

---

## Layout and presentation issues
1. p. 7, lines 324–349 / p. 22, lines 1134–1174 — **Critical** — Fig. 3 and Fig. 12 graphics swapped. Fix: exchange files (`empirical_spine.tex` line 20 and Appendix E).
2. p. 7, lines 357, 364; p. 18, line 951; p. 20, line 1078 — **Critical** — "Table III/IV" literals; actual numbers 6/7. Fix: `\ref`.
3. pp. 18–20, Figs. 4–8 — **Major** — never cited. Fix: cite from §5 / §6 or delete.
4. p. 15, line 756 (App. A); p. 18, line 947 (App. D) — **Major** — heading-only sections; their tables floated to pp. 14 and 17–18. Fix: lead sentence + `\FloatBarrier`.
5. Tables 1–3 (pp. 4, 5, 14) — **Major** — overfull 29.6/35.6/24.0 pt (log); rules enter the margin; ~7 pt type. Fix: `tabularx`; drop Table 2's Status column (duplicates §5).
6. p. 6, Fig. 1 — **Major** — four pages after first citation; in-figure text ~5 pt. Fix: p. 2, redraw ≥ 8 pt.
7. p. 19, Fig. 6 — **Major** — T6 label truncated ("…on contac"); T4 whisker text overprinted; T2 drawn as 100 % although §5.3 reports 52 %. Fix: widen axis, plot 52 % with "no reorientation" note.
8. p. 18, line 954; p. 20, line 1058; p. 24, line 1258; p. 25, lines 1299, 1346; p. 27, lines 1404, 1439 — **Minor** — duplicated numbers ("E.1 E.1 SETUP"). Fix: strip manual numbers.
9. p. 20, Fig. 8 right — **Minor** — title clipped ("…two geometri"); p. 22, Fig. 12 — legend overprinted, right annotation clipped.
10. p. 6, Fig. 2 — **Minor** — bottom strip narrower (0.9 vs 1.0 linewidth); no keep-out circle. Fix: equal widths, overlay the zone.
11. p. 5, lines 216–222 — **Minor** — uncaptioned, unnumbered schema table.
12. p. 5 (lines 223–225, 239–241, 247–249, 261–264), p. 14 (747–755), p. 17 (895–900) — **Minor** — float whitespace; Table 4 splits a sentence (p. 16 line 863 → p. 17 line 901).
13. p. 1, lines 000–006 — **Minor** — title breaks with the colon isolated; force `\\` before "A Diagnostic Benchmark".
14. Log — **Minor** — `T1/ptm/m/scit` undefined; Appendix B headings silently lose small caps.

## Missing figures and experiments
**MUST (no GPU)**
- Main-text results table: channel × policy with N, rate, CI, ablation and shield Δ (from Table 3). Buys the benchmark identity. ~half a day.
- Reproducibility + Ethics Statements + LLM-usage line; anonymous URL with Appendix A logs and `thresholds.yaml`. ~one day.
- Fix items 1–5; re-run latexmk; read the PDF end-to-end.

**SHOULD (no GPU)**
- Fig. 1 on p. 2, legible; corrected Fig. 6 promoted to §5.
- Completion-rate vs violation-rate scatter per cell (from Table 3): makes the transport-conditioning caveat visible. ~2 h.
- Fig. 2 with keep-out overlay.

**SHOULD (GPU, when the node returns)**
- Hazardous-payload-past-person cell at N ≥ 20 (now 5/5, p. 10 line 504): the title's cell is unpowered.
- Feasibility witnesses for T3a/T4/T6 (p. 10, lines 489–491) to lift "attribution-pending".

**NICE (GPU)**
- Non-flow third policy on T1 (π0 is 3/3, p. 9 lines 436–437).
- T6 shield at ≥ 0.60 m (p. 8, line 421).
