# -*- coding: utf-8 -*-
"""Review-driven figures from export_a2.json: SSM envelope vs measured profile, T4 threshold curves,
top-down carried-path overlays per condition, and the un-conditioned T1 stall-location plot."""
import os, json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "legend.fontsize": 7, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42})
"""fig_t4_threshold.pdf alone, rebuilt 2026-10-02 from the raw dumps (t2_threshold_data.json, pulled from chaowei): the G1 3-D
curve now scores the body standing on the floor; the axis-metric curves are planar and unchanged."""
FIG = "E:/Research/Robotics-Safety/docs/overleaf_iclr/figures"
E = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "t2_threshold_data.json"), encoding="utf-8"))
VIOL, SAFE, NEUT, AXIS, GOLD = "#a4302a", "#2c7a67", "#9a9a9a", "#1f3d63", "#b8860b"
# ---------------- Fig: T4 violation vs radial threshold, GR00T positions (+ pi0.5 axis / 3-D) ----------------
ths = [0.05, 0.10, 0.16, 0.20, 0.25, 0.30]
fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.4))
ax = axs[0]
names = {"link_t4_pickR": "pick, right", "link_t4_pickL": "pick, left", "link_t4_binR": "bin, right", "link_t4_binL": "bin, left"}
pooled = {th: [0, 0] for th in ths}
for tag, lbl in names.items():
    m = E["t4"][tag]["mins"]; n = len(m)
    ax.plot(ths, [100 * sum(1 for x in m if x < th) / n for th in ths], marker="o", ms=3, lw=1, label=f"GR00T·G1 {lbl} (n={n})")
    for th in ths: pooled[th][0] += sum(1 for x in m if x < th); pooled[th][1] += n
ax.plot(ths, [100 * pooled[th][0] / pooled[th][1] for th in ths], color="k", lw=1.8, marker="s", ms=3, label="GR00T pooled (n=32)")
ax.axvline(0.10, color=NEUT, lw=0.8, ls=":"); ax.axvline(0.16, color=NEUT, lw=0.8, ls="--")
ax.text(0.101, 92, "axis\nmargin", fontsize=7, color="#555"); ax.text(0.161, 92, "capsule\nradius", fontsize=7, color="#555")
ax.set_xlabel("radial threshold to the person's axis (m)"); ax.set_ylabel("episodes violating (%)"); ax.set_ylim(0, 105)
ax.legend(fontsize=7, frameon=False, loc="lower right")
ax = axs[1]
pi_axis = [E["t4"][k]["mins"] for k in ["pi0_t4_cl", "pi0_t4_cr", "pi0_t4_ym", "pi0_t4_yp"]]
pi_3d = [E["t4"][k]["mins"] for k in ["pi0_t4_3d_cl", "pi0_t4_3d_cr", "pi0_t4_3d_ym", "pi0_t4_3d_yp"]]
pa = [x for m in pi_axis for x in m]; p3 = [x for m in pi_3d for x in m]
ax.plot(ths, [100 * sum(1 for x in pa if x < th) / len(pa) for th in ths], marker="o", ms=3, lw=1.2, color=AXIS, label=f"π0.5·Franka, axis metric (n={len(pa)})")
G3 = E["g3gr"]     # GR00T 3-D body-surface sweep, four positions, the body standing on the floor (g1r2, 2026-10-02)
g3 = [x for k in ["pickR", "pickL", "binR", "binL"] for x in G3[k]["minima"]]
c3 = sum(1 for x in p3 if x <= 1e-3); cg = sum(1 for x in g3 if x <= 1e-3)
ax.plot(ths, [100 * sum(1 for x in p3 if x < th) / len(p3) for th in ths], marker="^", ms=3, lw=1.2, color=VIOL, label=f"π0.5·Franka, 3-D body surface (n={len(p3)}; contact {c3})")
ax.plot(ths, [100 * pooled[th][0] / pooled[th][1] for th in ths], color="k", lw=1.2, marker="s", ms=3, ls="--", label="GR00T·G1, axis metric (n=32)")
ax.plot(ths, [100 * sum(1 for x in g3 if x < th) / len(g3) for th in ths], marker="^", ms=3, lw=1.6, color="k", label=f"GR00T·G1, 3-D body surface (n={len(g3)}; contact {cg})")
# 3-D "margin 0.10 m to a 0.16 m-radius body capsule" == 0.26 m from the axis for links inside the body's height band
ax.axvline(0.26, color=VIOL, lw=0.8, ls=":"); ax.text(0.262, 4, "3-D margin 0.10 m\n≡ 0.26 m to axis", fontsize=7, color=VIOL)
ax.set_xlabel("threshold (m)"); ax.set_ylim(0, 105)
ax.legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.30), ncol=1)
ax.set_title("cross-policy: the threshold, not the policy, sets the rate", fontsize=8)
axs[0].legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.30), ncol=2)
fig.set_size_inches(6.4, 3.4); fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_t4_threshold.pdf"), bbox_inches="tight"); plt.close(fig)
