# -*- coding: utf-8 -*-
"""Main-result heatmap: unsafe rate per policy (rows) x sub-type (columns), grouped by dimension. Reads heatmap_data.json:
{"rows": [{"name": "GR00T N1.6 · G1", "cells": [[121,125], [26,32], null, ...]}, ...]}  (null = not run)."""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "pdf.fonttype": 42})
HERE = os.path.dirname(os.path.abspath(__file__))
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
data = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "heatmap_data.json"), encoding="utf-8"))
cols = ["T1\npayload path", "T2\nbody sweep", "T3\npresentation", "T4\nload tilt", "T5a\nspeed", "T5b\nforce", "T6\nmoving person"]
groups = [("Trajectory", 0, 1), ("Orientation", 2, 3), ("Speed & force", 4, 5), ("Dynamics", 6, 6)]
cmap = LinearSegmentedColormap.from_list("unsafe", ["#f3f1ec", "#e8b7a7", "#c0392b", "#7b1e17"])
rows = data["rows"]
fig, ax = plt.subplots(figsize=(6.4, 0.5 + 0.42 * len(rows)))
for i, r in enumerate(rows):
    for j, c in enumerate(r["cells"]):
        if c is None:
            ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor="white", edgecolor="#d0d0d0", lw=0.6, hatch="////"))
            ax.text(j + 0.5, i + 0.5, "—", ha="center", va="center", color="#9a9a9a", fontsize=8)
            continue
        k, n = c
        p = k / n if n else 0.0
        ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor=cmap(p), edgecolor="white", lw=1.2))
        tc = "white" if p > 0.55 else "#222"
        ax.text(j + 0.5, i + 0.40, f"{round(100 * p)}", ha="center", va="center", color=tc, fontsize=9, fontweight="bold")
        ax.text(j + 0.5, i + 0.74, f"{k}/{n}", ha="center", va="center", color=tc, fontsize=6.5)
ax.set_xlim(0, len(cols)); ax.set_ylim(len(rows), -0.62)
ax.set_xticks([j + 0.5 for j in range(len(cols))]); ax.set_xticklabels(cols, fontsize=7)
ax.xaxis.tick_bottom()
ax.set_yticks([i + 0.5 for i in range(len(rows))]); ax.set_yticklabels([r["name"] for r in rows], fontsize=7.5)
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)
for name, a, b in groups:  # dimension header band
    ax.text((a + b + 1) / 2, -0.33, name, ha="center", va="center", fontsize=7.5, color="#1f3d63", fontweight="bold")
    ax.plot([a + 0.06, b + 0.94], [-0.1, -0.1], color="#1f3d63", lw=0.9)
fig.tight_layout()
out = os.path.join(FIG, "fig_main_heatmap.pdf")
fig.savefig(out, bbox_inches="tight"); plt.close(fig)
print("wrote", out)
