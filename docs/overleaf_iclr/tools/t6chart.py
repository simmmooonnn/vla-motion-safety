# -*- coding: utf-8 -*-
"""fig_t6_contact.pdf (GR00T N1.6 on the G1): carried-box speed and box-person separation vs time around the closest
approach, on-path (11 completing carries, three seeds) vs the person-absent control (3), plus the 0.50 m live-tracking
shield runs (7).

Data: export_t6.json, exported 2026-09-10 from clearance_t6_s42/s7/s123, clearance_t6_offpath and e1b_t6_shield_track
(the September cells, in which the crossing capsule stood 0.79 m above the floor; the caption says so).  The file lives in
the 2026-09 session scratchpad, archived under E:/ClaudeTempArchive/...; the loader tries both.

2026-10-10 (figure audit): one shared legend below both panels, each entry once; the overprinted 'old 0.30 m label'
line is gone; drawn at the inclusion width (0.82 x 5.5 in) and saved without a tight bbox, so 7 pt text prints at 7 pt;
the person-absent control has its own line style (dash-dot) as well as its own colour; 'person-absent' throughout.
"""
import os, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.5, "axes.labelsize": 7.5, "legend.fontsize": 7,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.linewidth": 0.7,
                     "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42})
SESSION = "0f8a80ac-06d8-48e8-b25c-61ee2e370d30"
DATA_DIRS = [r"C:\Users\苏子健\AppData\Local\Temp\claude\E--Research-Robotics-Safety\%s\scratchpad" % SESSION,
             r"E:\ClaudeTempArchive\E--Research-Robotics-Safety\%s\scratchpad" % SESSION]
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
PREVIEW = r"E:\Research\Robotics-Safety\_scratch\tmp\figfix"          # PNG preview (write only under E:)
OUT = os.path.join(FIG, "fig_t6_contact.pdf")
E = None
for d in DATA_DIRS:
    if os.path.exists(os.path.join(d, "export_t6.json")):
        E = json.load(open(os.path.join(d, "export_t6.json"), encoding="utf-8")); break
if E is None:
    raise FileNotFoundError("export_t6.json not found in " + " | ".join(DATA_DIRS))

C_ON, C_ABS, C_SH = "#a4302a", "#2c7a67", "#1f3d63"
LS_ON, LS_ABS, LS_SH = "-", (0, (5, 1.5, 1, 1.5)), (0, (3, 1.5))
CONTACT = 0.16 + 0.10                     # capsule radius + box half-extent

# ---- the numbers the paper prints (E.7, results 5.1, the caption); stop if the export disagrees ----
on, off, tr = E["onpath"], E["offpath"], E["track"]
assert (len(on), len(off), len(tr)) == (11, 3, 7)
m_on = [min(t["sep"]) for t in on]; m_tr = [min(t["sep"]) for t in tr]; m_off = [min(t["sep"]) for t in off]
assert 0.255 <= min(m_on) and max(m_on) < 0.315                     # on-path minima 0.26--0.31 m (contact)
assert 0.265 <= min(m_tr) and max(m_tr) < 0.315                     # live-tracking 0.27--0.31 m
assert 0.055 <= min(m_off) and max(m_off) < 0.195                   # person-absent virtual separation 0.06--0.19 m


def first_below(t, th):
    return next(s for s, d, ti in zip(t["sp"], t["sep"], t["t"]) if d < th and ti <= 0.1)


sp35 = [first_below(t, 0.35) for t in on]
assert 0.245 <= min(sp35) and max(sp35) < 0.375                     # 0.25--0.37 m/s one step before contact


def hold_s(t):        # longest run below 0.08 m/s overlapping |t| <= 3 s, excluding the release run that ends the trace
    runs, st = [], None
    for i, v in enumerate(t["sp"]):
        if v < 0.08 and st is None: st = i
        if st is not None and (v >= 0.08 or i == len(t["sp"]) - 1):
            en = i if v >= 0.08 else i + 1
            runs.append((t["t"][st], t["t"][en - 1], en == len(t["sp"]))); st = None
    c = [b - a + 0.06 for a, b, end in runs if not end and b >= -3 and a <= 3]
    return max(c) if c else 0.0


holds = sorted(hold_s(t) for t in on)
held = [h for h in holds if h >= 1.95]   # 0.06 s sampling of a smoothed trace: 1.98 s reads as 2.0 s
assert len(held) == 6 and max(held) < 3.6, holds                    # 6/11 held 2--3.5 s, 5/11 brush past

W = 0.82 * 5.5                            # included at 0.82\linewidth
fig = plt.figure(figsize=(W, 2.75))
axL = fig.add_axes([0.095, 0.37, 0.385, 0.6])
axR = fig.add_axes([0.600, 0.37, 0.385, 0.6])

ax = axL
for t in on:
    ax.plot(t["t"], t["sp"], color=C_ON, ls=LS_ON, lw=0.7, alpha=0.75)
for t in off:
    ax.plot(t["t"], t["sp"], color=C_ABS, ls=LS_ABS, lw=1.0, alpha=0.95)
ax.text(-3.85, 0.665, "at contact: 6/11 held 2–3.5 s,\n5/11 brush past", fontsize=7, color=C_ON, va="top",
        linespacing=1.2)
ax.set_xlim(-4, 7); ax.set_ylim(0, 0.68)
ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
ax.set_ylabel("carried-box speed (m/s)")

ax = axR
for t in on:
    ax.plot(t["t"], t["sep"], color=C_ON, ls=LS_ON, lw=0.7, alpha=0.75)
for t in off:
    ax.plot(t["t"], t["sep"], color=C_ABS, ls=LS_ABS, lw=1.0, alpha=0.95)
for t in tr:
    ax.plot(t["t"], t["sep"], color=C_SH, ls=LS_SH, lw=0.8, alpha=0.8)
ax.axhline(CONTACT, color="k", lw=0.9, ls=":", zorder=5)
ax.text(6.9, CONTACT - 0.025, "contact distance\n(0.26 m)", fontsize=7, color="#222222", ha="right", va="top",
        linespacing=1.15)
ax.set_xlim(-4, 7); ax.set_ylim(0, 1.0)
ax.set_ylabel("box → person separation (m)")

for ax in (axL, axR):
    ax.set_xlabel("time from closest approach (s)")
    ax.set_xticks([-4, -2, 0, 2, 4, 6])
    ax.tick_params(length=2.5, width=0.6, pad=2)

handles = [Line2D([], [], color=C_ON, ls=LS_ON, lw=1.0, label="on-path carries (n = 11)"),
           Line2D([], [], color=C_ABS, ls=LS_ABS, lw=1.0, label="person-absent control (n = 3; right: to the virtual crossing)"),
           Line2D([], [], color=C_SH, ls=LS_SH, lw=1.0, label="+ live-tracking shield, 0.50 m (n = 7; right only)"),
           Line2D([], [], color="k", ls=":", lw=0.9, label="contact distance: capsule radius 0.16 m + box half-extent")]
fig.legend(handles=handles, frameon=False, loc="upper left", bbox_to_anchor=(0.075, 0.2), ncol=1,
           handlelength=2.8, labelspacing=0.3, borderaxespad=0)
fig.savefig(OUT)
plt.close(fig)
try:
    import fitz
    os.makedirs(PREVIEW, exist_ok=True)
    fitz.open(OUT)[0].get_pixmap(dpi=200).save(os.path.join(PREVIEW, "t6chart_fig_t6_contact.png"))
except Exception as e:
    print("preview skipped:", e)
print("wrote", OUT, "| on-path minima %.3f-%.3f, holds" % (min(m_on), max(m_on)), [round(h, 2) for h in holds])
