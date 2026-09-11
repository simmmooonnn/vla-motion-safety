# -*- coding: utf-8 -*-
"""Gallery at 1:1 print width (5.5 in): (a)-(f) one schematic per type with the scored quantity drawn (the predicate
text lives in Table II), (g)-(j) rendered top-down stills."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Wedge
from matplotlib import gridspec
from PIL import Image
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "pdf.fonttype": 42})
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
S = r"C:\Users\苏子健\AppData\Local\Temp\claude\E--Research-Robotics-Safety\0f8a80ac-06d8-48e8-b25c-61ee2e370d30\scratchpad"
VIOL, SAFE, NEUT, AXIS, GOLD, INK, SKIN, BLUE = "#a4302a", "#2c7a67", "#9a9a9a", "#1f3d63", "#b8860b", "#222", "#e6c9b0", "#5f7fb0"
fig = plt.figure(figsize=(5.5, 4.75))
gs = gridspec.GridSpec(3, 12, figure=fig, height_ratios=[1.0, 1.0, 0.68], hspace=0.12, wspace=0.25)
axs = [[fig.add_subplot(gs[r, c * 4:(c + 1) * 4]) for c in range(3)] for r in range(2)]
def base(ax, title):
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.45, 0.62); ax.set_aspect("equal"); ax.axis("off")
    ax.text(-1.28, 0.6, title, fontsize=7.5, fontweight="bold", color=INK, va="top")
def scene(ax, path=True):
    ax.add_patch(Rectangle((-0.5, 0.1), 1.0, 0.18, fc="#d9c7a3", ec="#8a7350", lw=0.6)); ax.text(0.0, 0.19, "shelf", ha="center", va="center", fontsize=6, color="#5a4a2a")
    ax.add_patch(Rectangle((-0.45, -1.3), 0.4, 0.26, fc="#c9d4e6", ec=AXIS, lw=0.6)); ax.text(-0.25, -1.17, "bin", ha="center", va="center", fontsize=6, color=AXIS)
    if path:
        xs = [0.15, 0.05, -0.05, -0.15, -0.22, -0.25]; ys = [0.02, -0.3, -0.6, -0.85, -0.98, -1.02]
        ax.plot(xs, ys, color=VIOL, lw=1.3, alpha=0.8); ax.annotate("", xy=(-0.25, -1.04), xytext=(-0.22, -0.96), arrowprops=dict(arrowstyle="-|>", color=VIOL, lw=1.2))
def person(ax, x, y, r=0.16):
    ax.add_patch(Circle((x, y), r, fc=BLUE, ec=AXIS, lw=0.6)); ax.add_patch(Circle((x, y), r * 0.55, fc=SKIN, ec="none"))
def box(ax, x, y, ang=0):
    ax.add_patch(Rectangle((x - 0.09, y - 0.06), 0.18, 0.12, angle=ang, rotation_point="center", fc="#b08968", ec=INK, lw=0.5))
ax = axs[0][0]; base(ax, "(a) T1  path / keep-out"); scene(ax)
ax.add_patch(Rectangle((-0.14, -0.66), 0.14, 0.14, fc="#e0762a", ec="none")); ax.add_patch(Circle((-0.07, -0.59), 0.3, fill=False, ls="--", lw=0.8, color=VIOL))
box(ax, -0.06, -0.45); ax.annotate("", xy=(-0.07, -0.59), xytext=(0.45, -0.25), arrowprops=dict(arrowstyle="<->", color=INK, lw=0.7)); ax.text(0.5, -0.22, "clearance", fontsize=6, color=INK)
ax.text(0.28, -0.85, "keep-out\n0.20 / 0.30 m", fontsize=6, color=VIOL, va="top")
ax = axs[0][1]; base(ax, "(b) T2  presentation orientation"); scene(ax)
person(ax, 0.8, -0.55); box(ax, -0.05, -0.55, ang=-25)
ax.annotate("", xy=(0.3, -0.72), xytext=(-0.05, -0.55), arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.3)); ax.text(0.08, -1.05, "hazardous axis", fontsize=6, color=GOLD)
ax.plot([-0.05, 0.64], [-0.55, -0.55], color=NEUT, lw=0.7, ls=":"); ax.text(0.3, -0.45, "bearing", fontsize=6, color="#555")
ax.add_patch(Wedge((-0.05, -0.55), 0.22, -25, 0, fc="none", ec=GOLD, lw=0.8)); ax.text(0.2, -0.66, "θ", fontsize=7, color=GOLD)
ax = axs[0][2]; base(ax, "(c) T3  speed vs separation"); scene(ax)
person(ax, 0.0, -0.9); box(ax, -0.02, -0.3)
ax.add_patch(Circle((0.0, -0.9), 0.5, fill=False, ls="--", lw=0.8, color=VIOL)); ax.text(0.55, -1.05, "d₀: must stop", fontsize=6, color=VIOL)
ax.annotate("", xy=(-0.02, -0.52), xytext=(-0.02, -0.3), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2)); ax.text(0.04, -0.42, "v", fontsize=7, color=INK)
ax.annotate("", xy=(0.62, -0.9), xytext=(0.62, -0.36), arrowprops=dict(arrowstyle="<->", color=INK, lw=0.7)); ax.text(0.67, -0.63, "d", fontsize=7, color=INK)
ax = axs[1][0]; base(ax, "(d) T4  body swept-volume"); scene(ax, path=False)
person(ax, 0.75, -0.25); ax.add_patch(Circle((0.75, -0.25), 0.26, fill=False, ls="--", lw=0.8, color=VIOL))
ax.add_patch(Circle((-0.15, -0.55), 0.13, fc="#ddd", ec=INK, lw=0.6)); ax.text(-0.15, -0.8, "robot", fontsize=6, ha="center", color=INK)
ax.plot([-0.15, 0.25, 0.53], [-0.55, -0.35, -0.22], color=INK, lw=2.0); ax.plot([0.53], [-0.22], "o", color=INK, ms=3)
ax.text(-0.05, -1.0, "arm enters the\nbystander's body", fontsize=6, color=VIOL, va="top")
ax = axs[1][1]; base(ax, "(e) T5  load stability (side view)")
ax.add_patch(Rectangle((-1.2, -1.15), 2.4, 0.07, fc="#ccc", ec="none")); ax.text(0.0, -1.05, "floor", ha="center", fontsize=6, color="#666")
ax.add_patch(Rectangle((-0.3, -0.35), 0.6, 0.4, angle=22, rotation_point="center", fc="#b08968", ec=INK, lw=0.6))
ax.plot([-0.55, 0.55], [-0.35, -0.35], color=NEUT, lw=0.7, ls=":"); ax.add_patch(Wedge((0.0, -0.35), 0.4, 0, 22, fc="none", ec=GOLD, lw=0.8)); ax.text(0.45, -0.27, "tilt", fontsize=7, color=GOLD)
ax.plot([-0.05, 0.12, 0.22], [0.12, 0.3, 0.18], color=AXIS, lw=1.0); ax.text(0.3, 0.3, "contents", fontsize=6, color=AXIS)
ax.annotate("", xy=(0.0, -1.0), xytext=(0.0, -0.6), arrowprops=dict(arrowstyle="-|>", color=VIOL, lw=1.0, ls="--")); ax.text(0.06, -0.8, "drop", fontsize=6, color=VIOL)
ax = axs[1][2]; base(ax, "(f) T6  dynamic reactivity"); scene(ax)
person(ax, -0.85, -0.75); ax.annotate("", xy=(-0.3, -0.75), xytext=(-0.67, -0.75), arrowprops=dict(arrowstyle="-|>", color=AXIS, lw=1.2)); ax.text(-1.25, -1.02, "crossing\n0.06 m/s", fontsize=6, color=AXIS, va="top")
box(ax, -0.08, -0.45); ax.add_patch(Circle((-0.08, -0.45), 0.26, fill=False, ls=":", lw=0.8, color=VIOL)); ax.text(0.25, -0.3, "contact\ndistance", fontsize=6, color=VIOL)
ax.text(0.2, -0.85, "TTC = d / closing speed", fontsize=6, color=INK)
stills = [("td_t1_plow.png", "(g) T1: through the strip's keep-out"), ("td_t4_body.png", "(h) T4: arm sweeps the bystander"),
          ("td_t6_cross.png", "(i) T6: crossing person, no slowing"), ("gen_drill.png", "(j) same carry past a real object")]
for k, (f, cap) in enumerate(stills):
    ax = fig.add_subplot(gs[2, k * 3:(k + 1) * 3]); ax.imshow(Image.open(os.path.join(FIG, f)).convert("RGB")); ax.axis("off")
    ax.set_title(cap, fontsize=6.2, loc="left", pad=2)
fig.savefig(os.path.join(FIG, "fig_gallery.pdf"), bbox_inches="tight"); plt.close(fig)
import fitz
fitz.open(os.path.join(FIG, "fig_gallery.pdf"))[0].get_pixmap(dpi=110).save(os.path.join(S, "pdfpages", "fig_gallery.png"))
print("wrote fig_gallery.pdf")
