"""Plot aware-vs-blind carried-hazard-to-human clearance over the trajectory."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D_SAFE = 0.10
RES = os.path.join(os.path.dirname(__file__), "results")


def load(cond):
    xs, ys = [], []
    with open(os.path.join(RES, cond + ".csv")) as f:
        for row in csv.DictReader(f):
            xs.append(int(row["step"]))
            ys.append(float(row["clearance"]))
    return xs, ys


fig, ax = plt.subplots(figsize=(7.5, 4.2))
for cond, color in (("aware", "#1a7f37"), ("blind", "#c1121f")):
    xs, ys = load(cond)
    ax.plot(xs, ys, color=color, lw=2, label=cond)

ax.axhline(D_SAFE, color="#555", ls="--", lw=1)
ax.axhline(0.0, color="#000", lw=0.8)
ax.fill_between([0, 200], -0.2, D_SAFE, color="#c1121f", alpha=0.06)
ax.text(4, D_SAFE + 0.005, f"d_safe = {D_SAFE} m", color="#555", fontsize=9)
ax.text(4, -0.045, "human penetrated (clearance < 0)", color="#c1121f", fontsize=8)

ax.set_xlabel("timestep")
ax.set_ylabel("carried-knife  to  human  clearance  (m)")
ax.set_title("Carried-hazard clearance: aware detour vs blind sweep (robosuite/MuJoCo)")
ax.set_xlim(0, 200)
ax.legend(loc="upper right")
fig.tight_layout()
out = os.path.join(RES, "clearance_comparison.png")
fig.savefig(out, dpi=130)
print("wrote", out)
