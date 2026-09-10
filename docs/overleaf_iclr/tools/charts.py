# -*- coding: utf-8 -*-
"""Regenerate the paper's chart figures as PDFs (matplotlib, no TeX rendering)."""
import os, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "pdf.fonttype": 42})
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
VIOL, SAFE, NEUT, AXIS = "#a4302a", "#2c7a67", "#9a9a9a", "#1f3d63"

# ---------- Fig: violation rate by channel (GR00T, G1) ----------
fig, ax = plt.subplots(figsize=(4.6, 2.2))
chan = ["T1 keep-out", "T3a SSM", "T6 dynamic", "T4 body-sweep", "T2 orient.", "T5 load"]
val  = [100, 100, 91, 25, 100, 0]
col  = [VIOL, VIOL, VIOL, VIOL, VIOL, SAFE]
lab  = ["100% (10/10)", "6/6 outside SSM envelope", "91% (10/11)", "25% pooled; 100% worst", "0 reorient (8 azimuths)", "null (level carry)"]
y = list(range(len(chan)))[::-1]
ax.barh(y, val, color=col, height=0.62)
ax.plot([25, 100], [y[3], y[3]], color=VIOL, lw=1.2)  # T4 whisker to worst position
for yi, v, l in zip(y, val, lab):
    ax.text(max(v, 3) + 1.5, yi, l, va="center", fontsize=7.5, color="#333")
ax.set_yticks(y); ax.set_yticklabels(chan); ax.set_xlim(0, 150); ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xlabel("violation rate (%), success-conditioned")
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_rates.pdf")); plt.close(fig)

# ---------- Fig: fixability (prompt null | shield fixes T1 | shield fails T6) ----------
fig, axs = plt.subplots(1, 3, figsize=(6.4, 2.0))
ax = axs[0]
x = [0, 1, 2]; base = [33, 33, 30]; cmd = [29, 46, 25]
ax.bar([i - 0.18 for i in x], base, 0.34, color=NEUT, label="neutral")
ax.bar([i + 0.18 for i in x], cmd, 0.34, color=VIOL, label="+ explicit command")
ax.set_xticks(x); ax.set_xticklabels(["T1", "T2", "T6"]); ax.set_ylim(0, 60); ax.set_ylabel("violation (%)")
ax.set_title("Explicit safety command\n(McNemar p = 1.0 / 0.58 / 1.0)", fontsize=8); ax.legend(fontsize=6.5, frameon=False)
ax = axs[1]
ax.bar([0, 1], [100, 0], 0.55, color=[VIOL, SAFE]); ax.set_xticks([0, 1]); ax.set_xticklabels(["blind", "+ shield"])
ax.set_ylim(0, 110); ax.set_title("T1 keep-out — shield\n8/8 → 0/10, Fisher p < 1e-4", fontsize=8)
ax.text(0, 102, "8/8", ha="center", fontsize=7.5); ax.text(1, 4, "0/10", ha="center", fontsize=7.5, color=SAFE)
ax = axs[2]
ax.bar([0, 1], [100, 86], 0.55, color=[VIOL, VIOL]); ax.set_xticks([0, 1]); ax.set_xticklabels(["blind", "+ live shield"])
ax.set_ylim(0, 110); ax.set_title("T6 dynamic — same shield\nstill ≈86% near-miss", fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_fixability.pdf")); plt.close(fig)

# ---------- Fig: cross-policy T1 and T4 ----------
fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.0))
ax = axs[0]
names = ["GR00T · G1", "π0.5 · Franka", "π0.5 · rendered"]; v = [100, 100, 100]; l = ["100%", "22/22", "16/16"]
yy = [2, 1, 0]; ax.barh(yy, v, color=VIOL, height=0.6)
for yi, li in zip(yy, l): ax.text(101, yi, li, va="center", fontsize=7.5, color=VIOL)
ax.set_yticks(yy); ax.set_yticklabels(names); ax.set_xlim(0, 130); ax.set_xticks([0, 50, 100])
ax.set_title("T1 keep-out: on-path violation", fontsize=8); ax.set_xlabel("%")
ax = axs[1]
names = ["GR00T · axis", "π0.5 · axis", "π0.5 · 3-D body"]; v = [25, 3, 53]; c = [NEUT, NEUT, VIOL]; l = ["25%", "3%", "53% (17/32)"]
ax.barh(yy, v, color=c, height=0.6)
for yi, vi, li in zip(yy, v, l): ax.text(vi + 1.5, yi, li, va="center", fontsize=7.5, color="#333")
ax.set_yticks(yy); ax.set_yticklabels(names); ax.set_xlim(0, 80); ax.set_xticks([0, 25, 50, 75])
ax.set_title("T4 body-sweep: one margin, two geometries", fontsize=8); ax.set_xlabel("%")
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_crosspolicy.pdf")); plt.close(fig)

# ---------- Fig: bimodal clearance (real per-carry values if available) ----------
bj = os.path.join(FIG, "bimodal.json")
if os.path.exists(bj):
    d = json.load(open(bj)); on, off = d["on"], d["off"]
    fig, ax = plt.subplots(figsize=(4.6, 1.7))
    import random; random.seed(3)
    ax.scatter(on,  [0.55 + random.uniform(-0.12, 0.12) for _ in on],  s=16, color=VIOL, alpha=.85, label="on-path (hazard at carry midpoint)")
    ax.scatter(off, [0.35 + random.uniform(-0.12, 0.12) for _ in off], s=16, color=SAFE, alpha=.85, label="off-path (perpendicular 0.35 m)")
    ax.axvspan(max(on), min(off), color="#bbb", alpha=.25); ax.text((max(on) + min(off)) / 2, 0.86, "empty band", ha="center", fontsize=7.5, color="#555")
    ax.set_yticks([]); ax.set_ylim(0.15, 0.95); ax.set_xlim(0, 0.5); ax.set_xlabel("minimum carried-object clearance to hazard (m)")
    ax.legend(fontsize=6.5, frameon=False, loc="upper right")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_bimodal.pdf")); plt.close(fig)
    print("bimodal figure written")
else:
    print("bimodal.json missing — skipped fig_bimodal.pdf")
print("charts written to", FIG)
