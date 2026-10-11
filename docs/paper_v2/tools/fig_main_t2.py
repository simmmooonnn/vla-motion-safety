# -*- coding: utf-8 -*-
"""Main-text T2 body sweep (paper v2, label fig:t2): compact version of fig_t2_sweep.py.

Per-episode minimum distance from any Franka arm-link origin to the bystander's body (3-D surface model) on the
pre-registered serving mug cell, one strip per arm: person-blind control 64, pi0.5 60, pi0-FAST 64,
GR00T N1.6-DROID 54 (90 s episodes), pi0 57. Filled = delivered, hollow = not delivered. Vertical line: the 0.10 m band;
grey: the person-blind control's range over all 64 episodes (0.1306-0.1882 m, printed as v1's "0.13-0.19 m"; the
delivered ones span 0.131-0.185 m). Counts at right = episodes inside the band. No panel (b), no 35 s rerun row (both
stay in the appendix version). The control's markers are drawn at 0.8x size because 64 episodes share 0.058 m.

Data (all local, read only; identical loading and asserts to fig_t2_sweep.py):
  tmp/now/t2_cond/rows.json                 min_link, delivered (per episode)
  tmp/now/t2_cond_skeptic/indep_rows.json   independent recompute
  fr_summary.json                           t2_mins of the cf_* cells (golden)
  a45_numbers.py                            N45 t2conf / t2conf_b
Writes docs/paper_v2/figures/fig_main_t2.pdf and a 250 dpi PNG preview in tmp/v2/mainfigs/.
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.transforms import blended_transform_factory

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "pdf.fonttype": 42, "ps.fonttype": 42,
                     "mathtext.fontset": "dejavusans", "axes.linewidth": 0.6, "xtick.major.width": 0.6,
                     "xtick.major.size": 2.5})
HERE = os.path.dirname(os.path.abspath(__file__))
FIG = r"E:\Research\Robotics-Safety\docs\paper_v2\figures"
PREV = os.path.join(HERE, "tmp", "v2", "mainfigs")
OUT = os.path.join(FIG, "fig_main_t2.pdf")

TH = 0.10        # T2 band (link origin to body surface)

# ---------------------------------------------------------------- data
rows = json.load(open(os.path.join(HERE, "tmp", "now", "t2_cond", "rows.json"), encoding="utf-8"))["rows"]
indep = json.load(open(os.path.join(HERE, "tmp", "now", "t2_cond_skeptic", "indep_rows.json"), encoding="utf-8"))["rows"]
summ = json.load(open(os.path.join(HERE, "fr_summary.json"), encoding="utf-8"))
ns = {}
exec(open(os.path.join(HERE, "a45_numbers.py"), encoding="utf-8").read(), ns)
N45 = ns["N45"]

# arm key in rows.json, key in indep_rows.json, row label, colour, marker
ARMS = [
    ("ctl", "ctl", "person-blind control", "#555555", "s"),
    ("pi05", "pi05", r"$\pi_{0.5}$", "#1f77b4", "o"),
    ("pi0", "pi0", r"$\pi_0$", "#2ca02c", "v"),
    ("pi0fast", "pi0fast", r"$\pi_0$-FAST", "#ff7f0e", "^"),
    ("gr00t_droid_90s", "g90", "GR00T N1.6-DROID (90 s)", "#d62728", "D"),
]
# the paper's counts (v1 Table XVI; results 5.1; Appendix C/E): within 0.10 m, all episodes and among delivered
PAPER = {"ctl": ("0/64", "0/24"), "pi05": ("26/60", "26/56"), "pi0fast": ("34/64", "32/56"),
         "gr00t_droid_90s": ("51/54", "14/14"), "pi0": ("0/57", "0/2")}
PAPER_CTL_PLACE = (0.131, 0.185)       # the control's delivered placements (v1 Appendix C/E/F)
CTL_LABEL = "0.13\u20130.19 m"         # v1: "links 0.13-0.19 m from the body on every episode"
assert N45["t2conf"]["ctl"]["kn"] == "0/64" and N45["t2conf"]["ctl"]["delivered"] == "24/64"
assert N45["t2conf"]["pi05"]["kn"] == "26/60" and N45["t2conf"]["pi05"]["delivered"] == "56/60"
assert N45["t2conf"]["pi0fast"]["kn"] == "34/64" and N45["t2conf"]["pi0fast"]["delivered"] == "56/64"
assert N45["t2conf_b"]["gr00t_droid"]["kn"] == "51/54" and N45["t2conf_b"]["gr00t_droid"]["delivered"] == "14/54"
assert N45["t2conf_b"]["pi0"]["kn"] == "0/57" and N45["t2conf_b"]["pi0"]["delivered"] == "2/57"

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
    k_all = f"{sum(v < TH for v in x)}/{len(x)}"
    k_del = f"{sum(v < TH for v, d in zip(x, dl) if d)}/{sum(dl)}"
    assert (k_all, k_del) == PAPER[arm], (arm, k_all, k_del, PAPER[arm])
    DATA[arm] = dict(x=x, dl=dl, k=k_all)
cp = [v for v, d in zip(DATA["ctl"]["x"], DATA["ctl"]["dl"]) if d]
assert (round(min(cp), 3), round(max(cp), 3)) == PAPER_CTL_PLACE, (min(cp), max(cp))
ca = DATA["ctl"]["x"]                                        # v1: "0.13-0.19 m from the body on every episode"
CTL_RANGE = (min(ca), max(ca))                               # shaded: every control episode (0.1306-0.1882 m)
assert f"{CTL_RANGE[0]:.2f}–{CTL_RANGE[1]:.2f} m" == CTL_LABEL, CTL_RANGE
XMAX = max(max(DATA[a]["x"]) for a in DATA)


# ---------------------------------------------------------------- beeswarm (in points, so markers do not overlap)
def swarm(xs, x0, x1, w_pt, d_pt, half_pt, up_pt=None):
    """Vertical offsets (points; negative = up on the inverted axis) for markers of diameter d_pt at data x, axis
    [x0, x1] drawn w_pt wide; offsets stay within [-up_pt, +half_pt] (up_pt defaults to half_pt)."""
    up_pt = half_pt if up_pt is None else up_pt
    sx = w_pt / (x1 - x0)
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    step = d_pt * 0.92
    levels = [0.0]
    j = 1
    while j * step <= max(half_pt, up_pt) + 1e-9:
        if j * step <= half_pt + 1e-9:
            levels.append(j * step)
        if j * step <= up_pt + 1e-9:
            levels.append(-j * step)
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


# ---------------------------------------------------------------- layout (inches)
W, H = 5.5, 1.55
L_A, R_A = 1.40, 4.80          # strip axes
B, T = 0.33, 1.36              # axes bottom / top
XC = 5.13                      # centre of the counts column
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([L_A / W, B / H, (R_A - L_A) / W, (T - B) / H])
n = len(ARMS)
TOPX = 0.34                    # extra room above the top row: the control's 64 episodes sit in a 0.054 m range
row_pt = (T - B) * 72 / (n + TOPX)
MS = 3.0
MS_CTL = 0.8                   # the control's markers are a little smaller (64 episodes in 0.058 m)
XA = (-0.012, 0.545)
assert XMAX < XA[1] - 0.005, XMAX

for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.tick_params(axis="x", labelsize=7, pad=1.5)
for i in range(n):
    ax.axhline(i, color="#eeeeee", lw=0.5, zorder=0)
ax.set_ylim(n - 0.5, -0.5 - TOPX)
ax.set_yticks([])
tY = blended_transform_factory(ax.transAxes, ax.transData)
for i, (_, _, nm, col, _) in enumerate(ARMS):
    ax.text(-0.012, i, nm, transform=tY, ha="right", va="center", fontsize=7)

ax.set_xlim(*XA)
ax.axvspan(*CTL_RANGE, color="#e2e2e2", lw=0, zorder=0.5)
ax.axvline(TH, color="#222222", lw=0.8, zorder=1)
wA = (R_A - L_A) * 72
for i, (arm, _, _, col, mk) in enumerate(ARMS):
    x, dl = DATA[arm]["x"], DATA[arm]["dl"]
    msz = MS * (0.9 if mk == "D" else 1.0) * (MS_CTL if arm == "ctl" else 1.0)
    off = swarm(x, *XA, wA, msz, row_pt * 0.45, row_pt * (0.45 + (TOPX if i == 0 else 0.0)))
    y = [i + o / row_pt for o in off]
    xf = [(a, b) for a, b, d in zip(x, y, dl) if d]
    xh = [(a, b) for a, b, d in zip(x, y, dl) if not d]
    if xh:
        ax.plot(*zip(*xh), ls="none", marker=mk, ms=msz, mfc="white", mec=col, mew=0.7, zorder=3)
    if xf:
        ax.plot(*zip(*xf), ls="none", marker=mk, ms=msz, mfc=col, mec=col, mew=0.6, zorder=4)
ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
ax.set_xticklabels(["0", "0.10", "0.20", "0.30", "0.40", "0.50"])
ax.set_xlabel("closest arm-link origin to the bystander's body, per episode (m)", fontsize=7, labelpad=2)

# labels above the axes: the band and the control's range
tA = ax.get_xaxis_transform()
ax.text(TH - 0.004, 1.03, "0.10 m band", transform=tA, ha="right", va="bottom", fontsize=7)
ax.text(CTL_RANGE[0] + 0.003, 1.03, f"control's range, {CTL_LABEL}", transform=tA, ha="left", va="bottom",
        fontsize=7, color="#555555")

# counts column
tC = blended_transform_factory(fig.transFigure, ax.transData)
fig.text(XC / W, (T + 0.03) / H, "within 0.10 m", ha="center", va="bottom", fontsize=7)
for i, (arm, *_r) in enumerate(ARMS):
    ax.text(XC / W, i, DATA[arm]["k"], transform=tC, ha="center", va="center", fontsize=7)

# legend: delivered filled, not delivered hollow (in the empty right part of the control's row)
hd = [Line2D([], [], ls="none", marker="o", ms=MS + 0.3, mfc="#555555", mec="#555555", label="delivered"),
      Line2D([], [], ls="none", marker="o", ms=MS + 0.3, mfc="white", mec="#555555", mew=0.7, label="not delivered")]
ax.legend(handles=hd, loc="center right", bbox_to_anchor=(1.0, 1.0 - (0.5 + TOPX) / (n + TOPX)), ncol=2, frameon=False, fontsize=7,
          handletextpad=0.15, columnspacing=0.9, borderaxespad=0.0, borderpad=0.0)

os.makedirs(FIG, exist_ok=True)
os.makedirs(PREV, exist_ok=True)
fig.savefig(OUT)
import fitz  # noqa: E402  (preview of the PDF exactly as written)
doc = fitz.open(OUT)
doc[0].get_pixmap(dpi=250).save(os.path.join(PREV, "fig_main_t2.png"))
fonts = {f[3] for f in doc[0].get_fonts()}
assert all("DejaVu" in f for f in fonts), fonts
print("fig_main_t2.pdf written;", {a: DATA[a]["k"] for a, *_ in ARMS}, "fonts", fonts, "xmax", round(XMAX, 3))
