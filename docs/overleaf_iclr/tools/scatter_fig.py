# -*- coding: utf-8 -*-
"""Success-vs-safety scatter: one point per cell (completion rate vs success-conditioned violation rate), from the
count table (Appendix A). Marker = channel, colour = condition."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "legend.fontsize": 6.5, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42})
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
S = r"C:\Users\苏子健\AppData\Local\Temp\claude\E--Research-Robotics-Safety\0f8a80ac-06d8-48e8-b25c-61ee2e370d30\scratchpad"
VIOL, SAFE, NEUT, AXIS, GOLD = "#a4302a", "#2c7a67", "#9a9a9a", "#1f3d63", "#b8860b"
# (label, attempted, completing, violating, channel, condition)
cells = [
 ("electric blind ×3", 36, 16, 16, "T1", "blind"), ("electric named", 12, 6, 6, "T1", "named"), ("electric hidden", 12, 7, 7, "T1", "hidden"),
 ("electric off-path", 35, 11, 0, "T1", "control"), ("electric sweep", 36, 24, 24, "T1", "blind"), ("electric shield 0.50", 36, 12, 6, "T1", "shield"),
 ("stove blind ×3", 36, 16, 16, "T1", "blind"), ("stove named", 12, 4, 4, "T1", "named"), ("stove hidden", 12, 7, 7, "T1", "hidden"),
 ("stove sweep", 36, 12, 12, "T1", "blind"), ("stove shield ≥0.60", 95, 28, 0, "T1", "shield"), ("stove shield ≤0.50", 60, 25, 22, "T1", "shield"),
 ("stove N=24", 24, 8, 8, "T1", "blind"), ("stove command", 24, 7, 7, "T1", "command"), ("stove off-path", 23, 12, 0, "T1", "control"),
 ("person blind", 27, 5, 5, "T1", "blind"), ("person named", 12, 1, 1, "T1", "named"), ("person hidden", 12, 6, 6, "T1", "hidden"), ("person shield", 39, 10, 2, "T1", "shield"),
 ("two hazards", 24, 6, 6, "T1", "blind"), ("two hazards shield", 24, 6, 0, "T1", "shield"), ("YCB blind", 42, 22, 22, "T1", "blind"), ("YCB shield", 34, 13, 1, "T1", "shield"),
 ("π0.5 on-path", 22, 22, 22, "T1 π0.5", "blind"), ("π0.5 off-path", 22, 22, 0, "T1 π0.5", "control"), ("π0.5 rendered", 22, 16, 16, "T1 π0.5", "hidden"),
 ("T6 on-path", 24, 11, 11, "T6", "blind"), ("T6 person-absent", 8, 3, 0, "T6", "control"), ("T6 shield fixed", 24, 4, 4, "T6", "shield"), ("T6 shield live", 24, 7, 6, "T6", "shield"),
 ("T2 axis<90°", 64, 27, 14, "T2", "blind"), ("T5 tilt>45°", 32, 17, 0, "T5", "blind"),
]
marker = {"T1": "o", "T1 π0.5": "D", "T6": "^", "T2": "s", "T5": "v"}
color = {"blind": VIOL, "named": GOLD, "hidden": "#7b4ea3", "shield": SAFE, "command": "#c46a1f", "control": NEUT}
fig, ax = plt.subplots(figsize=(4.9, 3.2))
import random; random.seed(7)
for lbl, N, C, V, ch, cond in cells:
    x = 100 * C / N + random.uniform(-1.2, 1.2); y = 100 * V / C + random.uniform(-1.2, 1.2)
    ax.scatter(x, y, s=18 + 0.6 * C, marker=marker[ch], color=color[cond], alpha=0.85, edgecolor="k", linewidth=0.3)
ax.set_xlim(0, 105); ax.set_ylim(-4, 106); ax.set_xlabel("completion rate (%)"); ax.set_ylabel("violation rate among completing carries (%)")
ax.axhline(50, color="#ddd", lw=0.6); ax.axvline(50, color="#ddd", lw=0.6)
ax.text(2, 96, "unsafe how", fontsize=7, color=VIOL); ax.text(2, 2, "safe how", fontsize=7, color=SAFE)
for ch, mk in marker.items(): ax.scatter([], [], marker=mk, color="w", edgecolor="k", label=ch)
for cond, c in color.items(): ax.scatter([], [], marker="o", color=c, label=cond)
ax.legend(frameon=False, ncol=2, loc="center right", bbox_to_anchor=(1.0, 0.5), handletextpad=0.3, columnspacing=0.8)
fig.savefig(os.path.join(FIG, "fig_success_safety.pdf"), bbox_inches="tight"); plt.close(fig)
import fitz
fitz.open(os.path.join(FIG, "fig_success_safety.pdf"))[0].get_pixmap(dpi=110).save(os.path.join(S, "pdfpages", "fig_success_safety.png"))
print("wrote fig_success_safety.pdf")
