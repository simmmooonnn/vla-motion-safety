# -*- coding: utf-8 -*-
"""Fig. 1 overview: the three axes of VLA safety (left) and the benchmark scene with the six types called out (right)."""
import os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch, Polygon
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "pdf.fonttype": 42})
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
S = r"C:\Users\苏子健\AppData\Local\Temp\claude\E--Research-Robotics-Safety\0f8a80ac-06d8-48e8-b25c-61ee2e370d30\scratchpad"
VIOL, SAFE, NEUT, AXIS, GOLD, INK = "#a4302a", "#2c7a67", "#9a9a9a", "#1f3d63", "#b8860b", "#222"
fig = plt.figure(figsize=(7.0, 3.6))
# ---------------- left: three axes
ax = fig.add_axes([0.01, 0.02, 0.44, 0.96]); ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
def box(x, y, w, h, title, sub, fc, ec, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.25", fc=fc, ec=ec, lw=1.4 if bold else 0.9))
    ax.text(x + w / 2, y + h - 0.55, title, ha="center", va="center", fontsize=9, fontweight="bold" if bold else "normal", color=INK)
    ax.text(x + w / 2, y + 0.55, sub, ha="center", va="center", fontsize=7.6, color="#444")
ax.text(0.1, 9.75, "(a)", fontsize=8, fontweight="bold")
box(0.3, 7.3, 4.3, 2.0, "Instruction safety", "should the task be done?\n(refusal, jailbreaks)", "#eef1f5", AXIS)
box(5.4, 7.3, 4.3, 2.0, "Outcome safety", "is the end state acceptable?\n(goal predicates)", "#eef1f5", AXIS)
box(0.3, 3.6, 9.4, 2.7, "Execution-phase safety  (this paper)", "how is a safe task carried out?", "#fbeeed", VIOL, bold=True)
ax.annotate("", xy=(2.45, 6.3), xytext=(2.45, 7.3), arrowprops=dict(arrowstyle="-|>", color=NEUT, lw=1))
ax.annotate("", xy=(7.55, 7.3), xytext=(7.55, 6.3), arrowprops=dict(arrowstyle="-|>", color=NEUT, lw=1))
ax.text(5.0, 6.85, "instruction ── trajectory τ = (s₀, a₀, …, s_T) ── end state", ha="center", va="center", fontsize=7.4, color="#555")
ax.text(5.0, 4.75, "T1 path / keep-out  ·  T2 presentation orientation\nT3 force & speed  ·  T4 body swept-volume\nT5 load stability  ·  T6 dynamic reactivity", ha="center", va="center", fontsize=7.0, color=INK)
ax.add_patch(FancyBboxPatch((0.3, 0.4), 9.4, 2.6, boxstyle="round,pad=0.02,rounding_size=0.25", fc="#f6f6f6", ec=NEUT, lw=0.8))
ax.text(5.0, 2.45, "type = ⟨harm channel, task phase, measured quantity,", ha="center", fontsize=7.2, color=INK)
ax.text(5.0, 1.85, "violation predicate, metric with CI, fixability class⟩", ha="center", fontsize=7.2, color=INK)
ax.text(5.0, 1.05, "fixability: prompt it? · perceive it? · architecture? · external layer?", ha="center", fontsize=7.2, color=VIOL)
# ---------------- right: top-down scene
bx = fig.add_axes([0.50, 0.02, 0.49, 0.96]); bx.set_xlim(-1.4, 1.9); bx.set_ylim(-2.35, 0.75); bx.set_aspect("equal"); bx.axis("off")
bx.add_patch(Rectangle((-0.1, 0.25), 1.3, 0.3, fc="#d9c7a3", ec="#8a7350", lw=0.8)); bx.text(0.55, 0.64, "(b)  shelf (pick)", ha="center", fontsize=7.5, color="#5a4a2a")
bx.add_patch(Rectangle((-0.5, -1.95), 0.5, 0.45, fc="#c9d4e6", ec=AXIS, lw=0.8)); bx.text(-0.25, -2.15, "bin (place)", ha="center", fontsize=7.5, color=AXIS)
# corridor path
xs = [0.55, 0.3, 0.0, -0.05, -0.1, -0.2, -0.25]; ys = [0.2, 0.0, -0.35, -0.7, -1.05, -1.45, -1.7]
bx.plot(xs, ys, color=VIOL, lw=1.6, alpha=0.85); bx.annotate("", xy=(-0.25, -1.72), xytext=(-0.2, -1.45), arrowprops=dict(arrowstyle="-|>", color=VIOL, lw=1.4))
bx.text(0.33, -0.28, "carry\n≈1.9 m", fontsize=7.2, color=VIOL, ha="center")
# T1 hazard on the path
bx.add_patch(Circle((-0.05, -0.7), 0.3, fill=False, ls="--", lw=0.9, color=VIOL)); bx.add_patch(Rectangle((-0.13, -0.78), 0.16, 0.16, fc="#e0762a", ec="none"))
bx.text(0.32, -1.02, "T1 hazard on the path\n(strip / stove / person)", fontsize=7.2, color=VIOL, va="center")
# carried box with orientation arrow (T2) and speed (T3)
bx.add_patch(Rectangle((-0.13, -0.42), 0.14, 0.09, angle=15, fc="#b08968", ec=INK, lw=0.6))
bx.annotate("", xy=(0.16, -0.36), xytext=(0.0, -0.39), arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.1))
bx.text(-1.35, -0.32, "T2 hazardous axis\npoints where?", fontsize=7.2, color=GOLD, va="center")
bx.text(-1.35, -0.62, "T3 speed vs\nseparation (SSM)", fontsize=7.2, color=INK, va="center")
bx.text(-1.35, -0.95, "T5 load tilt\n/ spill", fontsize=7.2, color=INK, va="center")
# T4 bystander beside the workspace
bx.add_patch(Circle((1.4, -0.15), 0.16, fc="#5f7fb0", ec=AXIS, lw=0.8)); bx.add_patch(Circle((1.4, -0.15), 0.09, fc="#e6c9b0", ec="none"))
bx.text(1.4, -0.4, "T4 bystander\nbeside the\nworkspace:\nthe robot's\nown arm", fontsize=7.2, color=AXIS, va="top", ha="center")
# T6 crossing person
bx.add_patch(Circle((-0.9, -1.1), 0.16, fc="#5f7fb0", ec=AXIS, lw=0.8)); bx.add_patch(Circle((-0.9, -1.1), 0.09, fc="#e6c9b0", ec="none"))
bx.annotate("", xy=(-0.35, -1.1), xytext=(-0.72, -1.1), arrowprops=dict(arrowstyle="-|>", color=AXIS, lw=1.2))
bx.text(-1.35, -1.42, "T6 person crossing\nthe corridor (0.06 m/s)", fontsize=7.2, color=AXIS, va="center")
# robot glyph
bx.add_patch(Circle((0.55, 0.05), 0.11, fc="#ddd", ec=INK, lw=0.8)); bx.text(-0.15, 0.05, "G1 + GR00T\n(or Franka + π0.5)", fontsize=7.2, color=INK, va="center", ha="right")
fig.savefig(os.path.join(FIG, "fig_overview.pdf"), bbox_inches="tight"); plt.close(fig)
import fitz
doc = fitz.open(os.path.join(FIG, "fig_overview.pdf")); doc[0].get_pixmap(dpi=120).save(os.path.join(S, "pdfpages", "fig_overview.png"))
print("wrote fig_overview.pdf")
