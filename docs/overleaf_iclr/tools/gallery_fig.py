# -*- coding: utf-8 -*-
"""Gallery at 1:1 print width (5.5 in x 4.12 in, included at \\linewidth): (a)-(f) one schematic per type with the scored
quantity drawn (the predicate text lives in Table II), (g)-(j) rendered top-down stills.

2026-10-10 (figure audit): explicit axes in inches, no tight bbox, so every font prints at its nominal size (>= 6.8 pt);
(a) draws the Cartesian control's straight line grazing the keep-out and a bowed joint-space control entering it next to the
policy's bow; (b) is labelled as the 0.10 m proximity band, not penetration; label overlaps in (b), (c), (e), (f) removed;
(d) 'drop' -> 'spill'; the G1 stills (g), (j) are cropped on the robot so the hazard and the crossing person are visible."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle, Wedge, Polygon
from PIL import Image
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 6.8, "pdf.fonttype": 42, "mathtext.fontset": "dejavusans"})
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
PREV = r"E:\Research\Robotics-Safety\_scratch\tmp\figfix"
VIOL, SAFE, NEUT, AXIS, GOLD, INK, SKIN, BLUE = "#a4302a", "#2c7a67", "#9a9a9a", "#1f3d63", "#b8860b", "#222", "#e6c9b0", "#5f7fb0"
CART, JS = "#555555", "#8e44ad"                     # shared palette: Cartesian control, joint-space control
LAB, TIT, SYM = 6.8, 7.5, 7.5                       # label / panel-title / symbol sizes in pt (printed 1:1)
W, H = 5.5, 4.12
fig = plt.figure(figsize=(W, H))
CW = W / 3.0                                        # schematic column width (in)
RH = 1.595                                          # schematic row height (in)
XL = (-1.4, 1.4)
YSPAN = RH / (CW / (XL[1] - XL[0]))
YL = (0.696 - YSPAN, 0.696)
def sax(r, c):
    y0 = H - (r + 1) * RH
    return fig.add_axes([c * CW / W, y0 / H, CW / W, RH / H])
axs = [[sax(r, c) for c in range(3)] for r in range(2)]
def base(ax, title):
    ax.set_xlim(*XL); ax.set_ylim(*YL); ax.set_aspect("equal"); ax.axis("off")
    ax.text(XL[0] + 0.03, YL[1] - 0.02, title, fontsize=TIT, fontweight="bold", color=INK, va="top")
def scene(ax, path=True, dx=0.0):
    ax.add_patch(Rectangle((-0.5 + dx, 0.1), 1.0, 0.18, fc="#d9c7a3", ec="#8a7350", lw=0.6))
    ax.text(0.0 + dx, 0.19, "shelf", ha="center", va="center", fontsize=LAB, color="#5a4a2a")
    ax.add_patch(Rectangle((-0.45 + dx, -1.3), 0.4, 0.26, fc="#c9d4e6", ec=AXIS, lw=0.6))
    ax.text(-0.25 + dx, -1.17, "bin", ha="center", va="center", fontsize=LAB, color=AXIS)
    if path:
        xs = [0.15, 0.05, -0.05, -0.15, -0.22, -0.25]; ys = [0.02, -0.3, -0.6, -0.85, -0.98, -1.02]
        ax.plot(xs, ys, color=VIOL, lw=1.3, alpha=0.8)
        ax.annotate("", xy=(-0.25, -1.04), xytext=(-0.22, -0.96), arrowprops=dict(arrowstyle="-|>", color=VIOL, lw=1.2))
def person(ax, x, y, r=0.16):
    ax.add_patch(Circle((x, y), r, fc=BLUE, ec=AXIS, lw=0.6)); ax.add_patch(Circle((x, y), r * 0.55, fc=SKIN, ec="none"))
def box(ax, x, y, ang=0):
    ax.add_patch(Rectangle((x - 0.09, y - 0.06), 0.18, 0.12, angle=ang, rotation_point="center", fc="#b08968", ec=INK, lw=0.5))

# (a) T1: a keep-out BESIDE the transport. The Cartesian control's straight line grazes it (18/80 at 0.20 m), the
# joint-space control's bow enters it (every far 0.20 m keep-out), and so does the policy's bow.
ax = axs[0][0]; base(ax, "(a) T1 payload path"); dx = 0.0; scene(ax, path=False, dx=dx)
S0, E0 = np.array([0.15 + dx, 0.02]), np.array([-0.25 + dx, -1.02])
dvec = E0 - S0; L = np.hypot(*dvec); u = dvec / L; nrm = np.array([-u[1], u[0]])     # nrm points to the far side (right)
if nrm[0] < 0: nrm = -nrm
t = np.linspace(0, 1, 60)
def bow(A, p=1.0):
    off = A * np.sin(np.pi * t) ** p
    return S0[0] + dvec[0] * t + nrm[0] * off, S0[1] + dvec[1] * t + nrm[1] * off
c0 = S0 + 0.45 * dvec + 0.292 * nrm; R0 = 0.30                                        # tangent to the straight line
ax.add_patch(Circle(tuple(c0), R0, fill=False, ls="--", lw=0.8, color=VIOL))
ax.add_patch(Rectangle((c0[0] - 0.05, c0[1] - 0.05), 0.10, 0.10, fc="#e0762a", ec="none"))
ax.plot([S0[0], E0[0]], [S0[1], E0[1]], color=CART, lw=0.9, ls=(0, (3.2, 1.8)))
xj, yj = bow(0.20); ax.plot(xj, yj, color=JS, lw=1.2, ls=(0, (1.0, 1.4)))
xp, yp = bow(0.30, 0.85); ax.plot(xp[:-3], yp[:-3], color=VIOL, lw=1.3, alpha=0.9)
ax.annotate("", xy=(E0[0] - 0.01, E0[1] - 0.02), xytext=(xp[-5], yp[-5]), arrowprops=dict(arrowstyle="-|>", color=VIOL, lw=1.2))
ax.text(c0[0] + R0 + 0.07, c0[1], "keep-out\nbeside the\ntransport", fontsize=LAB, color=VIOL, va="center", ha="left", linespacing=1.05)
for yy, lab, col, ls, lw in [(0.02, "policy", VIOL, "-", 1.3), (-0.27, "joint-space\ncontrol", JS, (0, (1.0, 1.4)), 1.2),
                             (-0.62, "Cartesian\ncontrol", CART, (0, (3.2, 1.8)), 0.9)]:
    ax.plot([-1.36, -1.17], [yy + (0.07 if "\n" in lab else 0.0)] * 2, color=col, lw=lw, ls=ls)
    ax.text(-1.12, yy, lab, fontsize=LAB, color=col, va="center", ha="left", linespacing=1.05)

# (b) T2: the robot's links against the bystander's body; scored = a link origin within 0.10 m of the body surface.
ax = axs[0][1]; base(ax, "(b) T2 body sweep"); scene(ax, path=False)
person(ax, 0.75, -0.25); ax.add_patch(Circle((0.75, -0.25), 0.26, fill=False, ls="--", lw=0.8, color=VIOL))
ax.add_patch(Circle((-0.15, -0.55), 0.13, fc="#ddd", ec=INK, lw=0.6)); ax.text(-0.33, -0.55, "robot", fontsize=LAB, ha="right", va="center", color=INK)
ax.plot([-0.15, 0.25, 0.53], [-0.55, -0.35, -0.22], color=INK, lw=2.0); ax.plot([0.53], [-0.22], "o", color=INK, ms=3)
ax.text(0.72, -0.60, "link within 0.10 m\nof the body", fontsize=LAB, color=VIOL, va="top", ha="center", linespacing=1.1)

# (c) T3: angle between the hazardous axis and the bearing to the bystander.
ax = axs[0][2]; base(ax, "(c) T3 orientation"); scene(ax)
person(ax, 0.8, -0.55); bx, by = -0.05, -0.55; box(ax, bx, by, ang=-25)
ang = np.deg2rad(-25); Lax = 0.62
ax.annotate("", xy=(bx + Lax * np.cos(ang), by + Lax * np.sin(ang)), xytext=(bx, by), arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.3))
ax.text(0.14, -0.93, "hazardous axis", fontsize=LAB, color=GOLD, va="top")
ax.plot([bx, 0.63], [by, by], color=CART, lw=0.7, ls=":"); ax.text(0.37, -0.51, "bearing", fontsize=LAB, color="#555", ha="center", va="bottom")
ax.add_patch(Wedge((bx, by), 0.32, -25, 0, fc="none", ec=GOLD, lw=0.8))
a2 = np.deg2rad(-12.5); ax.text(bx + 0.47 * np.cos(a2), by + 0.47 * np.sin(a2), "θ", fontsize=SYM, color=GOLD, ha="center", va="center")

# (d) T4 (side view): the load's tilt; the contents reach the low lip.
ax = axs[1][0]; base(ax, "(d) T4 load tilt (side)")
ax.add_patch(Rectangle((-1.2, -1.15), 2.4, 0.07, fc="#ccc", ec="none")); ax.text(0.0, -1.27, "floor", ha="center", va="center", fontsize=LAB, color="#666")
B = np.array([0.0, -0.40]); th = np.deg2rad(22); Rm = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
corners = np.array([[-0.3, 0.0], [0.3, 0.0], [0.3, 0.42], [-0.3, 0.42]]) @ Rm.T + B
cont = Polygon(corners, closed=True, fc="#f3ece2", ec=INK, lw=0.7, zorder=2); ax.add_patch(cont)
lip = corners[3]
liq = Rectangle((-1.0, -1.0), 2.0, (lip[1] - 0.012) + 1.0, fc="#8fb3dc", ec="none", zorder=2.5); ax.add_patch(liq); liq.set_clip_path(cont)
ax.add_patch(Polygon(corners, closed=True, fill=False, ec=INK, lw=0.7, zorder=3))
for k, (ox, oy, rr) in enumerate([(-0.04, -0.12, 0.030), (-0.07, -0.27, 0.026), (-0.09, -0.42, 0.022)]):
    ax.add_patch(Circle((lip[0] + ox, lip[1] + oy), rr, fc="#8fb3dc", ec=AXIS, lw=0.4, zorder=3))
ax.text(lip[0] - 0.16, lip[1] - 0.12, "spill", fontsize=LAB, color=VIOL, ha="right", va="center")
ax.plot([B[0] - 0.05, 0.68], [B[1], B[1]], color=NEUT, lw=0.7, ls=":")
ax.add_patch(Wedge(tuple(B), 0.46, 0, 22, fc="none", ec=GOLD, lw=0.8))
a3 = np.deg2rad(9); ax.text(B[0] + 0.60 * np.cos(a3), B[1] + 0.60 * np.sin(a3), "tilt", fontsize=SYM, color=GOLD, ha="left", va="center")

# (e) T5: payload speed v against the separation d to a person on the path; inside d0 it must have stopped.
ax = axs[1][1]; base(ax, "(e) T5 speed & force"); scene(ax)
px_, py_ = -0.10, -0.70; person(ax, px_, py_); box(ax, 0.075, -0.20, ang=-17)
ax.add_patch(Circle((px_, py_), 0.42, fill=False, ls="--", lw=0.8, color=VIOL))
ax.text(0.02, -1.21, "d₀: must stop", fontsize=LAB, color=VIOL, ha="left", va="center")
ax.annotate("", xy=(0.135, -0.46), xytext=(0.205, -0.24), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1))
ax.text(0.25, -0.36, "v", fontsize=SYM, color=INK, ha="left", va="center")
ax.annotate("", xy=(0.52, py_), xytext=(0.52, -0.20), arrowprops=dict(arrowstyle="<->", color=INK, lw=0.7))
ax.plot([px_ + 0.18, 0.56], [py_, py_], color=NEUT, lw=0.5, ls=":"); ax.plot([0.17, 0.56], [-0.20, -0.20], color=NEUT, lw=0.5, ls=":")
ax.text(0.58, -0.45, "d", fontsize=SYM, color=INK, ha="left", va="center")

# (f) T6: the payload reaching a crossing person or hand while it is in the way.
ax = axs[1][2]; base(ax, "(f) T6 moving person or hand"); scene(ax)
person(ax, -0.85, -0.75); ax.annotate("", xy=(-0.36, -0.75), xytext=(-0.67, -0.75), arrowprops=dict(arrowstyle="-|>", color=AXIS, lw=1.2))
ax.text(-0.85, -0.97, "crossing\n0.06 m/s", fontsize=LAB, color=AXIS, va="top", ha="center", linespacing=1.05)
box(ax, 0.0, -0.45, ang=-17); ax.add_patch(Circle((0.0, -0.45), 0.26, fill=False, ls=":", lw=0.8, color=VIOL))
ax.text(0.31, -0.36, "contact\ndistance", fontsize=LAB, color=VIOL, va="center", ha="left", linespacing=1.05)
ax.text(0.02, -1.40, "reached: gap ≤ 0.02 m\nwhile it is in the way", fontsize=LAB, color=INK, va="top", ha="center", linespacing=1.1)

# (g)-(j) stills. The G1 frames (340x191) are cropped to the same 16:9 window on the robot, hazard and bin.
def g1crop(im):
    return im.crop((88, 50, 312, 176)).resize((896, 504), Image.LANCZOS)
stills = [("td_t1_plow.png", "(g) G1 · T1, exposure", True), ("td_tab_t2_serving.png", "(h) Franka · T2", False),
          ("td_tab_t6_cross.png", "(i) Franka · T6 hand", False), ("td_t6_cross.png", "(j) G1 · T6", True)]
GAP = 0.06; SW = (W - 3 * GAP) / 4; SH = SW * 9 / 16
for k, (f, cap, crop) in enumerate(stills):
    ax = fig.add_axes([k * (SW + GAP) / W, 0.0, SW / W, SH / H])
    im = Image.open(os.path.join(FIG, f)).convert("RGB")
    if crop: im = g1crop(im)
    ax.imshow(im, aspect="auto", interpolation="none"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title(cap, fontsize=7.0, loc="left", pad=2)
fig.savefig(os.path.join(FIG, "fig_gallery.pdf"))
os.makedirs(PREV, exist_ok=True)
fig.savefig(os.path.join(PREV, "fig_gallery_direct.png"), dpi=200)
plt.close(fig)
import fitz
fitz.open(os.path.join(FIG, "fig_gallery.pdf"))[0].get_pixmap(dpi=200).save(os.path.join(PREV, "fig_gallery.png"))
print("wrote fig_gallery.pdf")
