# -*- coding: utf-8 -*-
"""Main result as a forest plot (review round 2026-10-06): for each sub-type with a person-blind control (T1-T4), each policy's
matched difference from the control (Mantel-Haenszel, points) with its 95 % interval (cluster-robust, t with fewer-cells-1 df);
filled red when the cell-level permutation test survives Holm correction over the 16 rows. Reads a45_numbers.py (N45["null_rel"])."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.5, "pdf.fonttype": 42})
HERE = os.path.dirname(os.path.abspath(__file__))
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
ns = {}
exec(open(os.path.join(HERE, "a45_numbers.py"), encoding="utf-8").read(), ns)
NR = ns["N45"]["null_rel"]
POL = [("pi05", "π0.5"), ("pi0", "π0"), ("pi0fast", "π0-FAST"), ("gr00t_droid", "GR00T-DROID")]
SUB = [("T1", "T1 keep-out"), ("T2", "T2 body sweep"), ("T3", "T3 presentation"), ("T4", "T4 load tilt")]
fig, axes = plt.subplots(1, 4, figsize=(6.6, 1.75), sharey=True)
for ax, (sid, title) in zip(axes, SUB):
    for i, (p, nm) in enumerate(POL):
        v = (NR.get(p) or {}).get(sid)
        y = len(POL) - 1 - i
        if not v:
            ax.text(0, y, "not run", ha="center", va="center", color="#999", fontsize=6.5)
            continue
        lo, hi = v.get("ci") or (v["rd"], v["rd"])
        sig = v.get("sig") == "above" or v.get("sig") == "below"
        col = "#b03a2e" if sig else "#5f6b7a"
        ax.plot([lo, hi], [y, y], color=col, lw=1.6, solid_capstyle="butt")
        ax.plot([v["rd"]], [y], marker="o", ms=4.2, color=col, mfc=col if sig else "white", mew=1.2)
    ax.axvline(0, color="#222", lw=0.7)
    ax.set_xlim(-100, 100)
    ax.set_xticks([-100, -50, 0, 50, 100])
    ax.tick_params(axis="x", labelsize=6)
    ax.set_title(title, fontsize=7.5, pad=3)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)
axes[0].set_yticks(range(len(POL)))
axes[0].set_yticklabels([nm for _, nm in reversed(POL)])
fig.text(0.5, 0.01, "policy minus person-blind control, matched placements (percentage points; 95 % interval)", ha="center", fontsize=6.5)
fig.subplots_adjust(left=0.135, right=0.985, bottom=0.22, top=0.86, wspace=0.22)
os.makedirs(FIG, exist_ok=True)
fig.savefig(os.path.join(FIG, "fig_forest.pdf"))
print("fig_forest.pdf written")
