# -*- coding: utf-8 -*-
"""Main result as a forest plot (review round 2026-10-06; figure audit 2026-10-10).
For each tabletop sub-type with a person-blind reference, each policy's matched difference (Mantel-Haenszel, points) with
its cluster-robust 95 % interval, UNADJUSTED for multiplicity; a filled marker means the cell-level permutation test survives
Holm correction within its own family:
  circles  - vs the Cartesian (straight-line) control, Table tab:IIIf, Holm over its 12 rows      (N45["null_rel"])
  diamonds - vs the pre-registered joint-space control, T1 only, Table tab:XVIII, Holm over 4   (N45["a2js"]["vs_policies"])
  squares  - pre-registered serving tests vs the control, T2 only, Table tab:XVI, Holm per pair (N45["t2conf"], N45["t2conf_b"])
Every number is read from a45_numbers.py; nothing is recomputed here."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "pdf.fonttype": 42, "mathtext.fontset": "dejavusans",
                     "axes.linewidth": 0.6, "xtick.major.width": 0.6, "xtick.minor.width": 0.5})
HERE = os.path.dirname(os.path.abspath(__file__))
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
ns = {}
exec(open(os.path.join(HERE, "a45_numbers.py"), encoding="utf-8").read(), ns)
N45 = ns["N45"]
NR = N45["null_rel"]                       # vs Cartesian control (tab:IIIf)
JS = N45["a2js"]["vs_policies"]            # vs joint-space control (tab:XVIII)
T2 = {"pi05": N45["t2conf"]["pi05"], "pi0fast": N45["t2conf"]["pi0fast"],                 # pre-registered H1-H2
      "gr00t_droid": N45["t2conf_b"]["gr00t_droid"], "pi0": N45["t2conf_b"]["pi0"]}       # pre-registered H3-H4
POL = [("pi05", r"$\pi_{0.5}$"), ("pi0", r"$\pi_0$"), ("pi0fast", r"$\pi_0$-FAST"), ("gr00t_droid", "GR00T N1.6-DROID")]
SUB = [("T1", "T1 keep-out"), ("T2", "T2 body sweep"), ("T3", "T3 presentation"), ("T4", "T4 load tilt")]
C_CART, C_JS, INK, MUTED = "#555555", "#8e44ad", "#222222", "#555555"
MK = {"cart": ("o", 3.9), "js": ("D", 3.5), "t2": ("s", 3.7)}

# Layout in inches: full width 5.5 in (included at \linewidth), height kept below the old 1.458 in printed height.
W, H = 5.5, 1.45
L, R, T, B, GAP = 1.08, 0.06, 0.17, 0.42, 0.16
pw = (W - L - R - 3 * GAP) / 4
fig = plt.figure(figsize=(W, H))
axes = [fig.add_axes([(L + k * (pw + GAP)) / W, B / H, pw / W, (H - T - B) / H]) for k in range(4)]


def interval(ax, y, rd, ci, col, kind, filled):
    lo, hi = ci
    if hi > lo:
        ax.plot([lo, hi], [y, y], color=col, lw=1.15, solid_capstyle="butt", zorder=2)
    m, ms = MK[kind]
    ax.plot([rd], [y], linestyle="none", marker=m, ms=ms, color=col, mfc=col if filled else "white", mew=0.9, zorder=3)


DY = 0.19   # T1: Cartesian reference above the row centre, joint-space below
for ax, (sid, title) in zip(axes, SUB):
    ax.axvline(0, color=INK, lw=0.6, zorder=1)
    for i, (p, nm) in enumerate(POL):
        y = len(POL) - 1 - i
        if sid == "T2":
            v = T2[p]
            if v["ci"][0] == v["ci"][1] == 0 and v["kn"].startswith("0/"):     # pi0: 0/57 vs 0/64, no event in either arm
                interval(ax, y, 0, (0, 0), C_CART, "t2", False)
                ax.text(11, y, "no event", ha="left", va="center", fontsize=6.5, color=MUTED)
            else:
                interval(ax, y, v["rd"], v["ci"], C_CART, "t2", bool(v.get("confirmed")))
            continue
        v = (NR.get(p) or {}).get(sid)
        if not v:
            ax.text(0, y, "not run", ha="center", va="center", fontsize=6.5, color=MUTED)
            continue
        sig = v.get("sig") in ("above", "below")
        yc = y + DY if sid == "T1" else y
        interval(ax, yc, v["rd"], v.get("ci") or (v["rd"], v["rd"]), C_CART, "cart", sig)
        if sid == "T1":
            j = JS[p]
            interval(ax, y - DY, j["rd"], j["ci"], C_JS, "js", j["p_holm"] < 0.05)
    ax.set_xlim(-106, 106)
    ax.set_ylim(-0.55, len(POL) - 0.45)
    ax.xaxis.set_major_locator(FixedLocator([-50, 0, 50]))
    ax.xaxis.set_minor_locator(FixedLocator([-100, 100]))
    ax.set_xticklabels(["\u221250", "0", "50"])
    ax.tick_params(axis="x", which="major", labelsize=6.5, length=2.5, pad=1.5)
    ax.tick_params(axis="x", which="minor", length=2.5)
    ax.set_title(title, fontsize=7.5, pad=2.5)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_yticks([])
axes[0].set_yticks(range(len(POL)))
axes[0].set_yticklabels([nm for _, nm in reversed(POL)], fontsize=7.5)
fig.text(0.5, 0.205 / H, "policy minus control on matched placements, percentage points "
         "(95 % interval, unadjusted; filled: survives Holm)", ha="center", va="center", fontsize=6.5)
hand = [Line2D([], [], color=C_CART, marker="o", ms=3.9, lw=1.15, label="vs Cartesian control"),
        Line2D([], [], color=C_JS, marker="D", ms=3.5, lw=1.15, label="vs joint-space control"),
        Line2D([], [], color=C_CART, marker="s", ms=3.7, lw=1.15, label="vs Cartesian control, pre-registered, own Holm family")]
fig.legend(handles=hand, loc="center", bbox_to_anchor=(0.5, 0.075 / H), ncol=3, frameon=False, fontsize=6.5,
           handlelength=1.6, handletextpad=0.4, columnspacing=1.3, borderaxespad=0, borderpad=0)
os.makedirs(FIG, exist_ok=True)
fig.savefig(os.path.join(FIG, "fig_forest.pdf"))
print("fig_forest.pdf written")
