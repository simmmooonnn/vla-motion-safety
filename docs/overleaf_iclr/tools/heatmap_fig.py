# -*- coding: utf-8 -*-
"""Main-result heatmap (Fig. 4, Table III as a map): unsafe rate per policy (rows) x sub-type (columns), grouped by
dimension. Reads heatmap_data.json, written by rebuild_a45.sh from N45 heat_rows:
{"rows": [{"name": "GR00T N1.6 · G1", "cells": [[11,30], [27,32], ..., [17,18]]}, ...]}  (8 cells per row, null = no score).

The presentation rules live here, not in the numbers generator:
  * T5a and T5b on the tabletop, T5b on the G1 and the control's T6 (the reaching hand, contact forced) are exposure:
    hatched grey, no rate, whatever count the data row carries (tabletop T5b carries the over-140 N count, Table IIIb);
  * a cell with fewer than FLOOR scored episodes prints k/n only, uncoloured (Table III / IIIb: count below eight);
  * the G1 row goes last, below a separator 'case study (not pooled)'; the control row is 'person-blind control'.
"""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.transforms import offset_copy
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "pdf.fonttype": 42, "hatch.linewidth": 0.6})
HERE = os.path.dirname(os.path.abspath(__file__))
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
FLOOR = 8  # scored episodes below which a cell is a count only
args = [a for a in sys.argv[1:] if not a.startswith("--")]
data = json.load(open(args[0] if args else os.path.join(HERE, "heatmap_data.json"), encoding="utf-8"))

# columns: (code, short name); full names are in the caption / Table IIIb header
cols = [("T1", "path"), ("T2", "sweep"), ("T3", "present."), ("T4", "tilt"),
        ("T5a", "speed"), ("T5b", "force"), ("T6", "person"), ("T6b", "anticip.")]
groups = [("Trajectory", 0, 1), ("Orientation", 2, 3), ("Speed & force", 4, 5), ("Dynamics", 6, 7)]
T5A, T5B, T6 = 4, 5, 6

# display order and labels; the data rows are matched by their N45 names
# (a pi label is a list of (text, is_subscript) parts, composed by rich_label so the subscript stays at 6.5 pt;
#  mathtext would shrink it to 0.7 x 7.5 = 5.25 pt)
ORDER = [("π0.5 · Franka", [("π", 0), ("0.5", 1)], "policy"),
         ("π0 · Franka", [("π", 0), ("0", 1)], "policy"),
         ("π0-FAST · Franka", [("π", 0), ("0", 1), ("-FAST", 0)], "policy"),
         ("GR00T N1.6-DROID · Franka", "GR00T N1.6-DROID", "policy"),
         ("scripted straight-line controls · Franka", "person-blind control", "control"),
         ("GR00T N1.6 · G1", "GR00T N1.6 (G1)", "g1")]
EXPOSURE = {"policy": {T5A, T5B}, "control": {T5A, T5B, T6}, "g1": {T5B}}
DAGGER = {("control", 1)}  # the control's T2 pools its bowl-away cells (Table III caption)

by_name = {r["name"]: r for r in data["rows"]}
missing = [n for n, _, _ in ORDER if n not in by_name]
extra = [n for n in by_name if n not in {o[0] for o in ORDER}]
if missing or extra:
    sys.exit(f"heatmap_fig.py: row names changed (missing {missing}, unexpected {extra})")
rows = []
for name, label, kind in ORDER:
    cells = by_name[name]["cells"]
    if len(cells) != len(cols):
        sys.exit(f"heatmap_fig.py: {name} has {len(cells)} cells, expected {len(cols)}")
    rows.append((label, kind, cells))

cmap = LinearSegmentedColormap.from_list("unsafe", ["#f3f1ec", "#e8b7a7", "#c0392b", "#7b1e17"])
INK, MUTED, BLUE = "#222222", "#666666", "#1f3d63"

# geometry (inches): full width 5.5 in, included at \linewidth
W, LEFT, RIGHT = 5.5, 1.22, 0.04
COLW = (W - LEFT - RIGHT) / len(cols)
RH = 0.37                      # row height
GAP = 0.62                     # separator row, in row units
TOP_U = 1.30                   # header band above row 0, in row units
ypos = [0, 1, 2, 3, 4, 4 + 1 + GAP]   # top edge of each row (row units)
y_end = ypos[-1] + 1
H = (y_end + TOP_U) * RH + 0.04
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([LEFT / W, 0.02 / H, (W - LEFT - RIGHT) / W, (y_end + TOP_U) * RH / H])
ax.set_xlim(0, len(cols)); ax.set_ylim(y_end, -TOP_U)
ax.axis("off")
xl = -LEFT / COLW + 0.04       # left edge of the figure in data x units
renderer = fig.canvas.get_renderer()


def rich_label(x, y, parts, size=7.5, sub=6.5):
    """Right-aligned row label at (x, y) built from (text, is_subscript) parts, laid out right to left."""
    off = 0.0  # points already used to the right
    for txt, is_sub in reversed(parts):
        tr = offset_copy(ax.transData, fig=fig, x=-off, y=(-4.4 if is_sub else -2.7), units="points")
        t = ax.text(x, y, txt, ha="right", va="baseline", fontsize=sub if is_sub else size, color=INK,
                    style="italic" if txt == "π" else "normal", transform=tr)
        off += t.get_window_extent(renderer).width * 72.0 / fig.dpi + (0.3 if txt == "π" else 0.0)


shown = []
for (label, kind, cells), y0 in zip(rows, ypos):
    if isinstance(label, list):
        rich_label(-0.10, y0 + 0.5, label)
        label = "".join(t for t, _ in label)
    else:
        ax.text(-0.10, y0 + 0.5, label, ha="right", va="center", fontsize=7.5, color=INK)
    for j, c in enumerate(cells):
        if j in EXPOSURE[kind]:
            ax.add_patch(plt.Rectangle((j, y0), 1, 1, facecolor="#ececec", edgecolor="#b4b4b4", lw=0, hatch="/////"))
            ax.add_patch(plt.Rectangle((j, y0), 1, 1, fill=False, edgecolor="white", lw=1.2))
            ax.text(j + 0.5, y0 + 0.5, "exposure", ha="center", va="center", fontsize=6.5, color="#4a4a4a",
                    style="italic", bbox=dict(boxstyle="square,pad=0.12", facecolor="#ececec", edgecolor="none"))
            shown.append((label, cols[j][0], "exposure"))
            continue
        if c is None:
            ax.add_patch(plt.Rectangle((j + 0.03, y0 + 0.03), 0.94, 0.94, facecolor="white", edgecolor="#c8c8c8", lw=0.6))
            ax.text(j + 0.5, y0 + 0.5, "not run", ha="center", va="center", fontsize=6.5, color=MUTED, style="italic")
            shown.append((label, cols[j][0], "not run"))
            continue
        k, n = c
        mark = "\u2020" if (kind, j) in DAGGER else ""
        if n < FLOOR:  # count only, not coloured by a rate
            ax.add_patch(plt.Rectangle((j + 0.03, y0 + 0.03), 0.94, 0.94, facecolor="white", edgecolor="#c8c8c8", lw=0.6))
            ax.text(j + 0.5, y0 + 0.40, f"{k}/{n}{mark}", ha="center", va="center", color=INK, fontsize=8.5, fontweight="bold")
            ax.text(j + 0.5, y0 + 0.74, f"n < {FLOOR}", ha="center", va="center", color=MUTED, fontsize=6.5, style="italic")
            shown.append((label, cols[j][0], f"{k}/{n} (count only)"))
            continue
        p = k / n
        ax.add_patch(plt.Rectangle((j, y0), 1, 1, facecolor=cmap(p), edgecolor="white", lw=1.2))
        tc = "white" if p > 0.55 else INK
        pct = round(100 * p)
        ax.text(j + 0.5, y0 + 0.40, f"{pct}", ha="center", va="center", color=tc, fontsize=9, fontweight="bold")
        ax.text(j + 0.5, y0 + 0.75, f"{k}/{n}{mark}", ha="center", va="center", color=tc, fontsize=6.5)
        shown.append((label, cols[j][0], f"{pct} ({k}/{n}){mark}"))

# group labels: tabletop (top-left, beside the column header) and the case-study separator
ax.text(xl, -0.42, "tabletop (Franka)", ha="left", va="center", fontsize=7, color=BLUE, style="italic")
ysep = ypos[4] + 1 + GAP / 2
ax.plot([xl, len(cols)], [ysep, ysep], color=BLUE, lw=0.7, clip_on=False)
ax.text(xl, ysep, "case study (not pooled)", ha="left", va="center", fontsize=7, color=BLUE, style="italic",
        bbox=dict(boxstyle="square,pad=0.25", facecolor="white", edgecolor="none"))

# column header: sub-type code + short name, then the dimension band above it
for j, (code, short) in enumerate(cols):
    ax.text(j + 0.5, -0.56, code, ha="center", va="center", fontsize=7.5, color=INK, fontweight="bold")
    ax.text(j + 0.5, -0.24, short, ha="center", va="center", fontsize=6.5, color=MUTED)
for name, a, b in groups:
    ax.text((a + b + 1) / 2, -1.08, name, ha="center", va="center", fontsize=7.5, color=BLUE, fontweight="bold")
    ax.plot([a + 0.06, b + 0.94], [-0.84, -0.84], color=BLUE, lw=0.9)

out = os.path.join(FIG, "fig_main_heatmap.pdf")
fig.savefig(out); plt.close(fig)
if "--list" in sys.argv:
    for s in shown:
        print(*s, sep="\t")
print("wrote", out)
