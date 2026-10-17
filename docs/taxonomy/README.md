# Taxonomy draft v0.1 (2026-10-15)

Sources for the shared taxonomy document "Motion Safety Benchmark on Isaac Sim: Taxonomy Draft v0.1 and Next-Step Plan", written after the 10-13 discussion with the two seniors. The Word file itself (`docs/Motion_Safety_Taxonomy_Draft_v0.1_2026-10-15.docx`) is not tracked; rebuild it from these files.

| File | What it is |
|---|---|
| `build_docx.py` | Builds the Word document (English text, tables, figures, next-step plan). Needs `python-docx`. |
| `make_figs.py` | Renders the five figures into `figures/`. |
| `e0_speed.py` | E0: Speed-vector readout on the existing payload logs of the pre-registered serving cell (CPU only). |
| `e0_speed_report.txt` | Output of `e0_speed.py` (radii 0.4 / 0.5 / 0.6 m). |
| `figures/` | fig1 taxonomy layers, fig2 coverage matrix, fig3 the three readouts in the existing POC, fig4 E0 speed, fig5 plan. |

Rebuild (from the repository root):

```
python docs/taxonomy/make_figs.py
python docs/taxonomy/build_docx.py
```

`e0_speed.py` and figure 4 read the payload logs pulled from the server into `_scratch/tmp/tax/spike/dumps/` (not tracked); the cell list comes from `docs/paper_v2/supp/prereg_followup_cells.csv`.

Contents of the document: target capability (Level, Awareness, Instruction readouts); four layers (Attack Surface = embodiment x task family, Attack Vector = trajectory / orientation / speed with Dynamic as an add-on, Hazard type grouped as in ISO 12100, Vulnerability cards); six predicate templates; dimension-wise evaluation with a few composite tasks; coverage matrix; 21 candidate cards; what Isaac Lab-Arena supports today; scene generation; the E0 result (no slowing near a visible person detected; the serving cell's near-person zone is also the place point, so Speed cards need a person beside the path); the plan to mid-November; open questions.
