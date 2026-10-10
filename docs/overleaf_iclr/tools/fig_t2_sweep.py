# -*- coding: utf-8 -*-
"""Pre-registered T2 body sweep (appendix figure, label fig:t2sweep; figure audit 2026-10-10, item R2).

Per-episode minimum distance from any Franka arm-link origin to the bystander's body (3-D surface model) on the
pre-registered serving mug cell (seeds 67-101; PREREG_T2 / _T2B / _T2C), one strip per arm:
Cartesian (person-blind) control 64, pi0.5 60, pi0-FAST 64, GR00T N1.6-DROID 54 (90 s) and 58 (35 s rerun), pi0 57.
Filled = delivered, hollow = not delivered. Panel (b): mug-to-bowl distance at the step of that minimum, for the
episodes inside the 0.10 m band (bowl = the nearer of its start and end positions, as in the paper's 26/26, 33/34).

Data (all local, read only):
  tmp/now/t2_cond/rows.json                 min_link, delivered (per episode)
  tmp/now/t2_cond_skeptic/indep_rows.json   independent recompute; db_at_min (two-bowl minimum)
  fr_summary.json                           t2_mins of the 48 cf_* cells (golden)
  a45_numbers.py                            N45 t2conf / t2conf_b / t2conf_e35
Every printed count is asserted against the paper's numbers (results.tex 5.1, Appendix C, Table XVI) before plotting.
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.transforms import blended_transform_factory

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "pdf.fonttype": 42, "ps.fonttype": 42,
                     "mathtext.fontset": "dejavusans"})
HERE = os.path.dirname(os.path.abspath(__file__))
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
OUT = os.path.join(FIG, "fig_t2_sweep.pdf")

TH = 0.10        # T2 band (link origin to body surface)
NEAR = 0.15      # "mug within 0.15 m of the bowl" (paper, Appendix C / E)

# ---------------------------------------------------------------- data
rows = json.load(open(os.path.join(HERE, "tmp", "now", "t2_cond", "rows.json"), encoding="utf-8"))["rows"]
indep = json.load(open(os.path.join(HERE, "tmp", "now", "t2_cond_skeptic", "indep_rows.json"), encoding="utf-8"))["rows"]
summ = json.load(open(os.path.join(HERE, "fr_summary.json"), encoding="utf-8"))
ns = {}
exec(open(os.path.join(HERE, "a45_numbers.py"), encoding="utf-8").read(), ns)
N45 = ns["N45"]

# arm key in rows.json, key in indep_rows.json, row label, colour, marker
ARMS = [
    ("ctl", "ctl", "Cartesian control", None, "#555555", "s"),
    ("pi05", "pi05", r"$\pi_{0.5}$", None, "#1f77b4", "o"),
    ("pi0fast", "pi0fast", r"$\pi_0$-FAST", None, "#ff7f0e", "^"),
    ("gr00t_droid_90s", "g90", "GR00T N1.6-DROID", "90 s episodes", "#d62728", "D"),
    ("gr00t_droid_35s", "g35", "GR00T N1.6-DROID", "35 s rerun", "#d62728", "d"),
    ("pi0", "pi0", r"$\pi_0$", None, "#2ca02c", "v"),
]
# the paper's counts (Table XVI; results.tex 5.1; Appendix C/E): within 0.10 m, all and among delivered
PAPER = {
    "ctl": ("0/64", "0/24"), "pi05": ("26/60", "26/56"), "pi0fast": ("34/64", "32/56"),
    "gr00t_droid_90s": ("51/54", "14/14"), "gr00t_droid_35s": ("43/58", "5/6"), "pi0": ("0/57", "0/2"),
}
PAPER_NEAR = {"pi05": "26/26", "pi0fast": "33/34"}          # mug within 0.15 m of the bowl at the closest step
PAPER_CTL_PLACE = (0.131, 0.185)                             # control's delivered placements (Appendix C/E, F)
# N45 cross-check of the all-episode counts and the delivered/attempted counts
assert N45["t2conf"]["ctl"]["kn"] == "0/64" and N45["t2conf"]["ctl"]["delivered"] == "24/64"
assert N45["t2conf"]["pi05"]["kn"] == "26/60" and N45["t2conf"]["pi05"]["delivered"] == "56/60"
assert N45["t2conf"]["pi0fast"]["kn"] == "34/64" and N45["t2conf"]["pi0fast"]["delivered"] == "56/64"
assert N45["t2conf_b"]["gr00t_droid"]["kn"] == "51/54" and N45["t2conf_b"]["gr00t_droid"]["delivered"] == "14/54"
assert N45["t2conf_b"]["pi0"]["kn"] == "0/57" and N45["t2conf_b"]["pi0"]["delivered"] == "2/57"
assert N45["t2conf_e35"]["kn"] == "43/58" and N45["t2conf_e35"]["delivered"] == "6/58"

ind = {(r["label"], r["ep"]): r for r in indep}
DATA = {}
for arm, iarm, *_ in ARMS:
    R = sorted((r for r in rows if r["arm"] == arm), key=lambda r: (r["label"], r["ep"]))
    for r in R:                                              # three sources agree episode by episode
        q = ind[(r["label"], r["ep"])]
        assert q["arm"] == iarm and abs(q["mn"] - r["min_link"]) < 1e-9 and q["delivered"] == r["delivered"]
        assert abs(summ[r["label"]]["t2_mins"][r["ep"]] - r["min_link"]) < 1e-9
    for lb in {r["label"] for r in R}:
        assert len(summ[lb]["t2_mins"]) == sum(1 for r in R if r["label"] == lb)
    x = [r["min_link"] for r in R]
    dl = [bool(r["delivered"]) for r in R]
    db = [ind[(r["label"], r["ep"])]["db_at_min"] for r in R]
    k_all = f"{sum(v < TH for v in x)}/{len(x)}"
    k_del = f"{sum(v < TH for v, d in zip(x, dl) if d)}/{sum(dl)}"
    assert (k_all, k_del) == PAPER[arm], (arm, k_all, k_del, PAPER[arm])
    vio = [(b, d) for v, b, d in zip(x, db, dl) if v < TH]
    if arm in PAPER_NEAR:
        k_near = f"{sum(b <= NEAR for b, _ in vio)}/{len(vio)}"
        assert k_near == PAPER_NEAR[arm], (arm, k_near)
    DATA[arm] = dict(x=x, dl=dl, vio=vio)
cp = [v for v, d in zip(DATA["ctl"]["x"], DATA["ctl"]["dl"]) if d]
assert (round(min(cp), 3), round(max(cp), 3)) == PAPER_CTL_PLACE, (min(cp), max(cp))


# ---------------------------------------------------------------- beeswarm (in points, so markers do not overlap)
def swarm(xs, x0, x1, w_pt, d_pt, half_pt):
    """Vertical offsets (points) for markers of diameter d_pt at data x, axis [x0, x1] drawn w_pt wide."""
    sx = w_pt / (x1 - x0)
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    step = d_pt * 0.92
    levels = [0.0]
    j = 1
    while j * step <= half_pt + 1e-9:
        levels += [j * step, -j * step]
        j += 1
    placed, off = [], [0.0] * len(xs)
    for i in order:
        px = (xs[i] - x0) * sx
        best, bestd = None, -1.0
        for lv in levels:
            dmin = min((((px - qx) ** 2 + (lv - qy) ** 2) ** 0.5 for qx, qy in placed if abs(px - qx) < d_pt * 1.5),
                       default=1e9)
            if dmin >= d_pt * 0.98:
                best = lv
                break
            if dmin > bestd:
                best, bestd = lv, dmin
        off[i] = best
        placed.append((px, best))
    return off


# ---------------------------------------------------------------- layout
W, H = 5.5, 2.3
L_A, R_A = 1.13, 3.45          # inches: panel (a)
L_B, R_B = 4.22, 5.44          # panel (b); counts column between R_A and L_B
B, T = 0.47, 1.93              # axes bottom / top (inches)
fig = plt.figure(figsize=(W, H))
axA = fig.add_axes([L_A / W, B / H, (R_A - L_A) / W, (T - B) / H])
axB = fig.add_axes([L_B / W, B / H, (R_B - L_B) / W, (T - B) / H], sharey=axA)
n = len(ARMS)
row_pt = (T - B) * 72 / n
MS = 3.0                       # marker size (points)
XA = (-0.012, 0.55)
XB = (-0.02, 0.85)

for ax in (axA, axB):
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", labelsize=6.5, length=2.5, pad=1.5)
    for i in range(n):
        ax.axhline(i, color="#eeeeee", lw=0.5, zorder=0)
axA.set_ylim(n - 0.5, -0.5)
axA.set_yticks(range(n))
axA.set_yticklabels([])
for i, (_, _, nm, sub, *_r) in enumerate(ARMS):
    if sub:
        axA.text(-0.035, i - 0.17, nm, transform=blended_transform_factory(axA.transAxes, axA.transData),
                 ha="right", va="center", fontsize=7)
        axA.text(-0.035, i + 0.2, sub, transform=blended_transform_factory(axA.transAxes, axA.transData),
                 ha="right", va="center", fontsize=6.5, color="#444444")
    else:
        axA.text(-0.035, i, nm, transform=blended_transform_factory(axA.transAxes, axA.transData),
                 ha="right", va="center", fontsize=7)
plt.setp(axB.get_yticklabels(), visible=False)

# (a) closest link to the body
axA.set_xlim(*XA)
axA.axvspan(*PAPER_CTL_PLACE, color="#e4e4e4", lw=0, zorder=0.5)
axA.axvline(TH, color="#222222", lw=0.8, zorder=1)
wA = (R_A - L_A) * 72
for i, (arm, _, _, _, col, mk) in enumerate(ARMS):
    x, dl = DATA[arm]["x"], DATA[arm]["dl"]
    off = swarm(x, *XA, wA, MS, row_pt * 0.45)
    y = [i + o / row_pt for o in off]
    xf = [(a, b) for a, b, d in zip(x, y, dl) if d]
    xh = [(a, b) for a, b, d in zip(x, y, dl) if not d]
    if xh:
        axA.plot(*zip(*xh), ls="none", marker=mk, ms=MS, mfc="white", mec=col, mew=0.7, zorder=3)
    if xf:          # delivered on top: the control's delivered placements are the matched reference
        axA.plot(*zip(*xf), ls="none", marker=mk, ms=MS, mfc=col, mec=col, mew=0.6, zorder=4)
axA.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
axA.set_xticklabels(["0", "0.10", "0.20", "0.30", "0.40", "0.50"])
axA.set_xlabel("(a) closest arm-link origin to the body (m)", fontsize=7, labelpad=2)

# annotations above (a): band label, the control's placements and the ~3 cm margin
tA = axA.get_xaxis_transform()
axA.text(TH - 0.004, 1.035, "0.10 m band", transform=tA, ha="right", va="bottom", fontsize=6.5)
axA.annotate("", xy=(TH, 1.115), xytext=(PAPER_CTL_PLACE[0], 1.115), xycoords=tA, textcoords=tA,
             arrowprops=dict(arrowstyle="<->", lw=0.6, color="#222222", shrinkA=0, shrinkB=0))
axA.text(PAPER_CTL_PLACE[0] + 0.006, 1.115, "3 cm", transform=tA, ha="left", va="center", fontsize=6.5)
axA.text(PAPER_CTL_PLACE[0] + 0.002, 1.035, "control's placements, 0.131\u20130.185 m", transform=tA,
         ha="left", va="bottom", fontsize=6.5, color="#333333")

# counts column (between the panels)
tC = blended_transform_factory(axA.transAxes, axA.transData)
xc = 1.0 + (L_B - R_A) / 2 / (R_A - L_A)
axA.text(xc, -0.5 - 0.06 * n, "within 0.10 m\nall \u00b7 delivered", transform=tC, ha="center", va="bottom",
         fontsize=6.5, linespacing=1.05)
for i, (arm, *_r) in enumerate(ARMS):
    a, d = PAPER[arm]
    axA.text(xc, i, f"{a} \u00b7 {d}", transform=tC, ha="center", va="center", fontsize=7)

# (b) where the arm enters: mug-to-bowl distance at the closest step, episodes inside the band
axB.set_xlim(*XB)
axB.axvline(NEAR, color="#777777", lw=0.7, ls=(0, (3, 2)), zorder=1)
axB.text(NEAR + 0.012, 1.035, "0.15 m", transform=axB.get_xaxis_transform(), ha="left", va="bottom",
         fontsize=6.5, color="#444444")
wB = (R_B - L_B) * 72
for i, (arm, _, _, _, col, mk) in enumerate(ARMS):
    vio = DATA[arm]["vio"]
    if not vio:
        axB.text(0.50, i, "none in the band", ha="center", va="center", fontsize=6.5, color="#777777")
        continue
    xb = [b for b, _ in vio]
    off = swarm(xb, *XB, wB, MS, row_pt * 0.45)
    for (b, d), o in zip(vio, off):
        axB.plot([b], [i + o / row_pt], ls="none", marker=mk, ms=MS, mfc=col if d else "white", mec=col,
                 mew=0.6 if d else 0.7, zorder=3)
    if arm in PAPER_NEAR:
        axB.text(0.83, i, f"{PAPER_NEAR[arm]} within\n0.15 m of the bowl", ha="right", va="center", fontsize=6.5,
                 linespacing=1.0)
axB.set_xticks([0, 0.15, 0.4, 0.8])
axB.set_xticklabels(["0", "0.15", "0.40", "0.80"])
axB.set_xlabel("(b) mug\u2013bowl distance\nat that step (m)", fontsize=7, labelpad=2, linespacing=1.0)

# legend: delivered filled, not delivered hollow
hd = [Line2D([], [], ls="none", marker="o", ms=MS + 0.4, mfc="#555555", mec="#555555", label="delivered"),
      Line2D([], [], ls="none", marker="o", ms=MS + 0.4, mfc="white", mec="#555555", mew=0.7, label="not delivered")]
axA.legend(handles=hd, loc="center right", bbox_to_anchor=(1.0, 1.0 - 4.5 / n), ncol=2, frameon=False, fontsize=6.5,
           handletextpad=0.2, columnspacing=0.8, borderaxespad=0.0)

os.makedirs(FIG, exist_ok=True)
fig.savefig(OUT)
print("fig_t2_sweep.pdf written;", {a: PAPER[a] for a, *_ in ARMS}, "near", PAPER_NEAR)
