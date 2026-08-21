#!/usr/bin/env python3
"""Tier B orientation figure: (A) carried-hazard yaw is fixed regardless of bystander side
→ no orientation-level avoidance; (B) the geometric consequence — the +x-side bystander gets
the blade pointed nearly at them, uncorrected."""
import json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = json.load(open("tierb_reduced.json"))
CONDS = ["absent", "left", "right"]
LAB = {"absent": "absent\n(no person)", "left": "person LEFT\n(x=-0.25, on-path)",
       "right": "person RIGHT\n(x=+0.45, off-path)"}
COL = {"absent": "#8a8f98", "left": "#d1495b", "right": "#2f7ec4"}

def circ_mean(vs):
    s = sum(math.sin(math.radians(v)) for v in vs); c = sum(math.cos(math.radians(v)) for v in vs)
    return math.degrees(math.atan2(s, c))
def circ_sd(vs):
    s = sum(math.sin(math.radians(v)) for v in vs)/len(vs); c = sum(math.cos(math.radians(v)) for v in vs)/len(vs)
    R = math.hypot(s, c); return math.degrees(math.sqrt(max(0.0, -2*math.log(max(R, 1e-9)))))

fig, (axA, axB) = plt.subplots(1, 2, figsize=(12.4, 5.4))
rng = np.random.default_rng(7)

# ---------- Panel A: box_yaw@closest ----------
for i, c in enumerate(CONDS):
    eps = d[c]
    succ = [e["yaw"] for e in eps if e["succ"]]
    fail = [e["yaw"] for e in eps if not e["succ"]]
    xs_s = i + (rng.random(len(succ)) - 0.5) * 0.16
    xs_f = i + (rng.random(len(fail)) - 0.5) * 0.16
    axA.scatter(xs_f, fail, s=42, facecolors="none", edgecolors="#b8bcc4", linewidths=1.2, zorder=2)
    axA.scatter(xs_s, succ, s=80, color=COL[c], edgecolors="white", linewidths=1.0, zorder=3)
    if succ:
        cm, cs = circ_mean(succ), circ_sd(succ)
        axA.hlines(cm, i-0.26, i+0.26, color=COL[c], lw=2.6, zorder=4)
        yoff = {0: -32, 1: 40, 2: 28}[i]
        axA.annotate(f"{cm:+.1f}°±{cs:.0f}°\n(succ n={len(succ)})", (i, cm),
                     xytext=(i, cm+yoff), fontsize=9.5, color=COL[c], va="center", ha="center",
                     fontweight="bold")
axA.axhspan(-8, 8, color="#e8f0d8", alpha=0.7, zorder=0)
axA.axhline(0, color="#5a7d2a", lw=1.0, ls="--", zorder=1)
axA.text(-0.45, 10, "fixed-carry band (±8°)", fontsize=8.2, color="#5a7d2a", va="bottom", ha="left")
axA.set_xticks(range(3)); axA.set_xticklabels([LAB[c] for c in CONDS], fontsize=9.5)
axA.set_ylabel("carried-hazard yaw at closest approach  (deg)", fontsize=10.5)
axA.set_ylim(-195, 155); axA.set_xlim(-0.5, 3.05)
axA.set_title("A · Orientation mechanism: yaw is FIXED (~0°) whether the bystander\nis absent, left, or right → GR00T never turns the hazard away",
              fontsize=10.5, loc="left")
axA.scatter([], [], s=80, color="#555", label="successful carry (yaw counted)")
axA.scatter([], [], s=42, facecolors="none", edgecolors="#b8bcc4", label="failed grasp (box knocked; excluded)")
axA.legend(loc="lower left", fontsize=8.3, framealpha=0.9)

# ---------- Panel B: blade->person angle (consequence) ----------
for i, c in enumerate(CONDS):
    eps = d[c]
    succ = [e["blade"] for e in eps if e["succ"]]
    xs = i + (rng.random(len(succ)) - 0.5) * 0.16
    axB.scatter(xs, succ, s=80, color=COL[c], edgecolors="white", linewidths=1.0, zorder=3)
    if succ:
        m = sum(succ)/len(succ)
        axB.hlines(m, i-0.26, i+0.26, color=COL[c], lw=2.6, zorder=4)
        axB.annotate(f"{m:.0f}°", (i, m), xytext=(i+0.30, m), fontsize=10.5,
                     color=COL[c], va="center", fontweight="bold")
axB.axhspan(0, 45, color="#f6d9dd", alpha=0.8, zorder=0)
axB.text(2.46, 22, "blade points\nAT the person\n(hazard)", fontsize=8.5, color="#a33", va="center", ha="left")
axB.axhspan(135, 180, color="#d8ecf6", alpha=0.8, zorder=0)
axB.text(2.46, 158, "blade points\nAWAY\n(incidental)", fontsize=8.5, color="#256", va="center", ha="left")
axB.set_xticks(range(3)); axB.set_xticklabels([LAB[c] for c in CONDS], fontsize=9.5)
axB.set_ylabel("angle between hazard blade-axis and the bystander  (deg)", fontsize=10.5)
axB.set_ylim(-8, 190); axB.set_xlim(-0.5, 3.05)
axB.set_yticks([0, 45, 90, 135, 180])
axB.set_title("B · Consequence: because orientation is fixed, the +x-side (right)\nbystander gets the blade aimed nearly AT them (26°), uncorrected",
              fontsize=10.5, loc="left")

fig.suptitle("Tier B — carried-hazard orientation on the constrained G1 humanoid (GR00T, knife instruction, success-conditioned)",
             fontsize=12, fontweight="bold", y=0.995)
fig.tight_layout(rect=[0, 0, 1, 0.96])
out = r"E:\Research\Robotics-Safety\safety\isaac_matrix_2026-08-11\run7_orientation\orientation_result.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
print("saved", out)
