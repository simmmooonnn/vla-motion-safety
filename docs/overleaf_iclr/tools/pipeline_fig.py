# -*- coding: utf-8 -*-
"""§7 protocol / pipeline figure: scene family -> policy server -> recorders -> predicates -> report, with the three
items that make a cell a benchmark cell (ablations, reference layer, feasibility witness)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "pdf.fonttype": 42})
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
S = r"C:\Users\苏子健\AppData\Local\Temp\claude\E--Research-Robotics-Safety\0f8a80ac-06d8-48e8-b25c-61ee2e370d30\scratchpad"
VIOL, SAFE, NEUT, AXIS, GOLD, INK = "#a4302a", "#2c7a67", "#9a9a9a", "#1f3d63", "#b8860b", "#222"
fig, ax = plt.subplots(figsize=(7.0, 2.7)); ax.set_xlim(0, 100); ax.set_ylim(0, 40); ax.axis("off")
def node(x, y, w, h, title, body, ec, fc="#f7f7f7"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=1.2", fc=fc, ec=ec, lw=1.0))
    ax.text(x + w / 2, y + h - 2.8, title, ha="center", va="center", fontsize=7.2, fontweight="bold", color=INK)
    ax.text(x + w / 2, y + (h - 3.2) / 2 - 0.4, body, ha="center", va="center", fontsize=6.1, color="#333", linespacing=1.2)
def arrow(x0, y0, x1, y1, color=NEUT):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=color, lw=1.0))
node(1, 21, 17.5, 18, "1  Scene family", "hazard class ×\nperson state ×\nsafe move demanded", AXIS)
node(21, 21, 17.5, 18, "2  Policy server", "GR00T N1.6, π0.5, …\nunmodified, remote;\nnew policy = a swap", AXIS)
node(41, 21, 17.5, 18, "3  Recorders", "object pose (clearance,\nyaw, tilt); link poses (3-D\nbody); moving person", AXIS)
node(61, 21, 17.5, 18, "4  Predicates T1–T6", "per-episode violation,\ncontact, threshold curve;\nsuccess-conditioning", VIOL, fc="#fbeeed")
node(81, 21, 18, 18, "5  Report", "attempted / completing /\nviolating, Wilson CI,\nexact tests, curves", INK, fc="#f0f0f0")
for x0, x1 in [(18.5, 21), (38.5, 41), (58.5, 61), (78.5, 81)]: arrow(x0, 30, x1, 30)
node(1, 1, 30.5, 15, "6  Fixability ablations", "name the hazard · hide it · safety command\n(paired seeds; minimal detectable effect)", GOLD, fc="#fbf5e6")
node(34.5, 1, 30.5, 15, "7  Reference safety layer", "repulsion shield · protective stop · orientation\ncontrol — efficacy and failure modes", SAFE, fc="#eaf3f0")
node(68, 1, 31, 15, "8  Feasibility witness", "scripted violation-free trajectory, so a rate\nis attributable to the policy, not the scene", NEUT, fc="#f4f4f4")
for x in [16.25, 49.75, 83.5]: arrow(x, 16, x, 21)
fig.savefig(os.path.join(FIG, "fig_pipeline.pdf"), bbox_inches="tight"); plt.close(fig)
import fitz
fitz.open(os.path.join(FIG, "fig_pipeline.pdf"))[0].get_pixmap(dpi=110).save(os.path.join(S, "pdfpages", "fig_pipeline.png"))
print("wrote fig_pipeline.pdf")
