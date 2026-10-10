# -*- coding: utf-8 -*-
"""fig_t4_threshold.pdf (Fig. 'T2: the threshold sets the rate; the policy order holds') and nothing else.

Rebuilt 2026-10-02 from the raw dumps (t2_threshold_data.json, pulled from chaowei): the G1 3-D curve scores the body
standing on the floor (g3gr); the axis-metric curves are planar and unchanged.  Revised 2026-10-10 (figure audit):
  * right-panel title no longer says 'not the policy' (the G1 curve is never below pi0.5's under either metric);
  * the third threshold is computed at 0.15 m, where it is ticked (E.3 quotes 72/84/100/100 % at 0.05/0.10/0.15/0.20 m);
    every curve except pi0.5 3-D (26 vs 27/32, not quoted anywhere) has the same value at 0.15 and 0.16 m;
  * the right x axis says which distance each metric uses (dashed = to the axis, solid = to the body surface);
  * the '0.26 m to axis' note moves to the caption; vline labels sit clear of the curves;
  * naming: 'GR00T N1.6 (G1)' for the humanoid, '$\\pi_{0.5}$ (Franka)'; positions avoid the policy palette colours.
Included at \\linewidth (5.5 in), so the figure is drawn at 5.5 in and saved without a tight bbox (printed 1:1).
"""
import os, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib._mathtext as _mt
_mt.SHRINK_FACTOR = 6.5 / 7.0     # keep mathtext subscripts ($\pi_{0.5}$) at >= 6.5 pt in the 7 pt legend (default 0.7 -> 4.9 pt)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.5, "axes.labelsize": 7.5, "axes.titlesize": 7.5,
                     "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
                     "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42, "axes.linewidth": 0.7})
HERE = os.path.dirname(os.path.abspath(__file__))
FIG = "E:/Research/Robotics-Safety/docs/overleaf_iclr/figures"
OUT = os.path.join(FIG, "fig_t4_threshold.pdf")
E = json.load(open(os.path.join(HERE, "t2_threshold_data.json"), encoding="utf-8"))

C_PI05, C_G1, GRID = "#1f77b4", "#222222", "#9a9a9a"     # pi0.5 = shared palette; G1 = near-black (case study)
POS = [("link_t4_pickR", "pickR", "pick, right", "#8c564b", "o"),     # per-position colours outside the policy palette
       ("link_t4_pickL", "pickL", "pick, left", "#e377c2", "s"),
       ("link_t4_binR", "binR", "bin, right", "#bcbd22", "D"),
       ("link_t4_binL", "binL", "bin, left", "#17becf", "v")]
ths = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]


def k_below(m, th):
    return sum(1 for x in m if x < th)


def pct(m, th):
    return 100.0 * k_below(m, th) / len(m)


g1_axis = [x for tag, *_ in POS for x in E["t4"][tag]["mins"]]
g1_3d = [x for _, key, *_ in POS for x in E["g3gr"][key]["minima"]]
pi_axis = [x for k in ["pi0_t4_cl", "pi0_t4_cr", "pi0_t4_ym", "pi0_t4_yp"] for x in E["t4"][k]["mins"]]
pi_3d = [x for k in ["pi0_t4_3d_cl", "pi0_t4_3d_cr", "pi0_t4_3d_ym", "pi0_t4_3d_yp"] for x in E["t4"][k]["mins"]]
c_pi = sum(1 for x in pi_3d if x <= 1e-3); c_g1 = sum(1 for x in g1_3d if x <= 1e-3)

# ---- the numbers the paper prints (results.tex 5.1, E.3, the T2 first-probe paragraph); stop if the data disagree ----
assert len(g1_axis) == len(g1_3d) == len(pi_axis) == len(pi_3d) == 32
assert k_below(g1_axis, 0.10) == 8                                   # 8/32 under the 0.10 m axis margin
assert [k_below(g1_3d, t) for t in (0.05, 0.10, 0.15, 0.20)] == [23, 27, 32, 32]   # 72 / 84 / 100 / 100 %
assert c_g1 == 19 and c_pi == 8                                      # contact 19/32 and 8/32
assert k_below(pi_axis, 0.10) == 1 and k_below(pi_3d, 0.10) == 17    # 3 % (1/32) and 53 % (17/32)
assert [round(pct(g1_axis, t)) for t in ths] == [16, 25, 34, 56, 72, 84]
assert [k_below(pi_axis, t) for t in ths] == [1, 1, 2, 4, 12, 21]   # text: 3/3/6/12/37/66 % (12/32 = 37.5, 21/32 = 65.6)
assert sum(1 for x in E["g3gr"]["pickR"]["minima"] if x <= 1e-3) == 8   # 8/8 at pick-right

fig = plt.figure(figsize=(5.5, 3.3))
axL = fig.add_axes([0.085, 0.42, 0.385, 0.46])
axR = fig.add_axes([0.600, 0.42, 0.385, 0.46])

# ---- left: G1, axis metric, per position + pooled ----
ax = axL
for tag, _, lbl, col, mk in POS:
    m = E["t4"][tag]["mins"]
    ax.plot(ths, [pct(m, t) for t in ths], color=col, marker=mk, ms=3.2, lw=1.0, label=f"{lbl} (n = {len(m)})")
ax.plot(ths, [pct(g1_axis, t) for t in ths], color=C_G1, lw=1.9, marker="s", ms=3.4, label=f"pooled (n = {len(g1_axis)})", zorder=5)
ax.axvline(0.10, color=GRID, lw=0.9, ls=":", zorder=0, label="axis margin, 0.10 m")
ax.axvline(0.16, color=GRID, lw=0.9, ls="--", zorder=0, label="capsule radius, 0.16 m")
ax.set_title("GR00T N1.6 (G1), axis metric:\nper position and pooled", pad=4)
ax.set_xlabel("radial threshold to the person's axis (m)")
ax.set_ylabel("episodes violating (%)")

# ---- right: cross-policy, axis (dashed) vs 3-D body surface (solid) ----
ax = axR
ax.plot(ths, [pct(pi_axis, t) for t in ths], color=C_PI05, ls="--", lw=1.2, marker="o", ms=3.2,
        label="$\\pi_{0.5}$ (Franka), axis")
ax.plot(ths, [pct(pi_3d, t) for t in ths], color=C_PI05, ls="-", lw=1.4, marker="^", ms=3.6,
        label=f"$\\pi_{{0.5}}$ (Franka), 3-D; contact {c_pi}/{len(pi_3d)}")
ax.plot(ths, [pct(g1_axis, t) for t in ths], color=C_G1, ls="--", lw=1.2, marker="s", ms=3.2,
        label="GR00T N1.6 (G1), axis")
ax.plot(ths, [pct(g1_3d, t) for t in ths], color=C_G1, ls="-", lw=1.6, marker="^", ms=3.6,
        label=f"GR00T N1.6 (G1), 3-D; contact {c_g1}/{len(g1_3d)}", zorder=5)
ax.axvline(0.10, color=GRID, lw=0.9, ls=":", zorder=0, label="0.10 m margin")
ax.set_title("cross-policy: the threshold sets the rate;\nthe policy order holds", pad=4)
ax.set_xlabel("threshold (m): to the axis (dashed)\nor to the body surface (solid)")

for ax in (axL, axR):
    ax.set_xlim(0.035, 0.315); ax.set_ylim(0, 105)
    ax.set_xticks(ths); ax.set_xticklabels([f"{t:.2f}" for t in ths])
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.tick_params(length=2.5, width=0.6, pad=2)

LEG_Y = 0.235     # both legends hang from the same height, below the two-line right x label
axL.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.2775, LEG_Y), bbox_transform=fig.transFigure, ncol=2,
           handlelength=2.2, columnspacing=1.0, labelspacing=0.35, borderaxespad=0)
axR.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.785, LEG_Y + 0.03), bbox_transform=fig.transFigure, ncol=1,
           handlelength=2.6, labelspacing=0.35, borderaxespad=0, title="n = 32 episodes per curve", title_fontsize=7)
fig.savefig(OUT)
plt.close(fig)
print("wrote", OUT)
print("G1 axis %:", [round(pct(g1_axis, t)) for t in ths], " pi0.5 axis %:", [round(pct(pi_axis, t), 1) for t in ths])
print("G1 3-D %:", [round(pct(g1_3d, t)) for t in ths], " pi0.5 3-D %:", [round(pct(pi_3d, t)) for t in ths],
      " contact G1 %d/32, pi0.5 %d/32" % (c_g1, c_pi))
