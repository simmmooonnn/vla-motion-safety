# ICLR 2027 Overleaf seed

LaTeX project generated from `docs/execution_phase_safety_position_paper_draft.md` (v0.24) using the
official ICLR 2027 author kit (`iclr2027_conference.sty/.bst`, `math_commands.tex`, `natbib.sty`, `fancyhdr.sty`).

## Layout

```
main.tex                 preamble, title, abstract, \input of the sections, bibliography
sections/*.tex           one file per top-level section (in paper order, see main.tex)
refs.bib                 34 entries (ref1 ... ref34 = the [N] numbers in the markdown draft)
figures/                 rendered frames (png) + charts (pdf) + bimodal.json (raw clearance values)
tools/md2tex.py          markdown -> LaTeX converter that produced main.tex / sections / refs.bib
tools/charts.py          matplotlib script that produced figures/fig_*.pdf
```

## Build

Overleaf: upload `docs/overleaf_iclr_seed.zip` (New Project -> Upload Project), compiler pdfLaTeX, main file `main.tex`.

Local: `latexmk -pdf -interaction=nonstopmode main.tex` (TinyTeX needs `microtype courier` on top of the basic scheme).

## Regenerating from the markdown

`python tools/md2tex.py` **overwrites** `main.tex`, `sections/*.tex` and `refs.bib`. Use it only while the
markdown draft is still the source of truth; once editing moves to Overleaf, stop running it (or diff first).

## Submission-mode notes

* `\iclrfinalcopy` is commented out, so the PDF shows *Anonymous authors* and line numbers (double-blind).
* The author block in `main.tex` still has a `[email]` placeholder for the camera-ready.
* `ref32`–`ref34` (handover orientation papers) have no author field yet — they cite by arXiv id until verified.
* The seed is ~23 pages; ICLR's main-text limit is 10 pages (references/appendix unlimited), so the
  per-type schema (§4.1–4.6), the agenda, and parts of §5 are candidates for an appendix.
