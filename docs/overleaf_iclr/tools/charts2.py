# -*- coding: utf-8 -*-
"""Review-driven figures from export_a2.json / export_a2c.json (G1 case study, 2026-09-09 exports).

    python charts2.py               -> builds fig_ssm_envelope.pdf only (the default)
    python charts2.py ssm           -> the same
    python charts2.py overlay       -> fig_topdown_overlay.pdf (unchanged legacy code; not rebuilt 2026-10-10)
    python charts2.py uncond        -> fig_t1_uncond.pdf       (unchanged legacy code; not rebuilt 2026-10-10)

fig_t4_threshold.pdf is NOT built here any more: this script used to rebuild it from the stale 2026-09-14
b8_t4_3d_summary.json (raised-body 3-D scoring).  The current figure comes from fig_t2_threshold.py
(t2_threshold_data.json, floor-standing body, 2026-10-02).  save() refuses that file name.

2026-10-10 (figure audit), fig_ssm_envelope.pdf:
  * the stationary-human curve uses the paper's v_h = 0 setting (T = 0.4 s, C = 0.2 m, Z = 0.1 m: d0 = C + Z = 0.30 m,
    the G1 governor's v_allow = (d - 0.30)/0.25 of E.6 and results 5.1), not T = 0.2 s, C = Z = 0 (d0 = 0);
  * the stop-region annotation sits right of the lenient / stationary curves (no strike-through);
  * drawn at the inclusion width (0.78 x 5.5 in) and saved without a tight bbox, so 7 pt text prints at 7 pt;
  * all six traces are one series (GR00T N1.6 (G1), person present; 5 hazard-labelled + 1 benign instruction);
    the standard's curves share one hue and differ by line style.
The data files live in the 2026-09 session scratchpad, archived under E:/ClaudeTempArchive/...; the loader tries both.
"""
import os, sys, json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib._mathtext as _mt
_mt.SHRINK_FACTOR = 6.5 / 7.0     # mathtext subscripts ($v_h$, $d_0$, $v_{allow}$) stay >= 6.5 pt in 7 pt text (default 0.7 -> 4.9 pt)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "legend.fontsize": 7, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42})
SESSION = "0f8a80ac-06d8-48e8-b25c-61ee2e370d30"
DATA_DIRS = [r"C:\Users\苏子健\AppData\Local\Temp\claude\E--Research-Robotics-Safety\%s\scratchpad" % SESSION,
             r"E:\ClaudeTempArchive\E--Research-Robotics-Safety\%s\scratchpad" % SESSION]
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
PREVIEW = r"E:\Research\Robotics-Safety\_scratch\tmp\figfix"          # PNG previews (write only under E:)
FORBIDDEN = {"fig_t4_threshold.pdf"}                                   # built by fig_t2_threshold.py only
VIOL, SAFE, NEUT, AXIS, GOLD = "#a4302a", "#2c7a67", "#9a9a9a", "#1f3d63", "#b8860b"
BIN = (-0.245, -1.627)


def load(name):
    for d in DATA_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return json.load(open(p, encoding="utf-8"))
    raise FileNotFoundError(name + " not found in " + " | ".join(DATA_DIRS))


def save(fig, name, **kw):
    if name in FORBIDDEN:
        raise RuntimeError(name + " is built by fig_t2_threshold.py; charts2.py must not overwrite it")
    out = os.path.join(FIG, name)
    fig.savefig(out, **kw); plt.close(fig)
    try:
        import fitz
        os.makedirs(PREVIEW, exist_ok=True)
        fitz.open(out)[0].get_pixmap(dpi=200).save(os.path.join(PREVIEW, "charts2_" + name.replace(".pdf", ".png")))
    except Exception as e:                                             # preview is a convenience only
        print("preview skipped:", e)
    print("wrote", out)


def load_a2():
    E = load("export_a2.json")
    E2 = load("export_a2c.json")
    E["t3"] = E2["t3"]                      # smoothed (0.2 s central difference + 9-step running median)
    for cond, C in E2["collision"].items(): # person-proxy T1 cells (Table III/IV "collision" dumps)
        E["cells"]["person/" + cond] = dict(N=len(C["eps"]), eps=C["eps"], ko=C["ko"])
    return E


# ---------------- Fig: SSM envelope vs measured speed-separation traces (T5a, G1 case study) ----------------
def v_allow(d, vh, T, C, Z):
    Tr, Ts = 0.25 * T, 0.75 * T          # split as in analyze_t3_ssm.py (Tr=0.10, Ts=0.30 for T=0.40)
    return max(0.0, (d - vh * T - C - Z) / (Tr + Ts / 2.0))


def build_ssm():
    T3 = load("export_a2c.json")["t3"]
    # ---- the numbers the paper prints (E.5, results 5.1); stop if the export disagrees ----
    mins = sorted(min(tr["seps"]) for tr in T3)
    assert len(T3) == 6 and sum(tr["label"] == "dangerous" for tr in T3) == 5          # 6 carries: 5 dangerous-label, 1 benign
    assert abs(mins[0] - 0.089) < 5e-4 and abs(mins[-1] - 0.246) < 5e-4                 # 0.089--0.246 m
    assert abs((mins[2] + mins[3]) / 2 - 0.157) < 5e-4                                  # median 0.157 m
    assert all(m < 0.30 for m in mins)                                                  # inside C + Z = 0.30 m (v_h = 0)
    assert abs(max(max(tr["sps"]) for tr in T3) - 0.47) < 5e-3                          # smoothed peak 0.47 m/s (caption)
    WALK = dict(vh=1.6, T=0.40, C=0.20, Z=0.10)   # d0 = 0.94 m
    LEN = dict(vh=1.6, T=0.20, C=0.0, Z=0.0)      # d0 = 0.32 m
    STILL = dict(vh=0.0, T=0.40, C=0.20, Z=0.10)  # d0 = C + Z = 0.30 m; v_allow = (d - 0.30)/0.25
    d0 = lambda p: p["vh"] * p["T"] + p["C"] + p["Z"]
    assert abs(d0(WALK) - 0.94) < 1e-9 and abs(d0(LEN) - 0.32) < 1e-9 and abs(d0(STILL) - 0.30) < 1e-9
    assert abs(v_allow(0.55, **STILL) - (0.55 - 0.30) / 0.25) < 1e-9
    rc = {"font.size": 7.5, "axes.labelsize": 7.5, "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
          "axes.linewidth": 0.7}
    with plt.rc_context(rc):
        W = 0.78 * 5.5                                     # included at 0.78\linewidth
        fig = plt.figure(figsize=(W, 3.1))
        ax = fig.add_axes([0.115, 0.43, 0.86, 0.555])
        ax.axvspan(0, d0(WALK), color="#f6e8e6", zorder=0, lw=0)
        for i, tr in enumerate(T3):
            ax.plot(tr["seps"], tr["sps"], lw=0.55, alpha=0.6, color="#222222", zorder=2,
                    label="GR00T N1.6 (G1) carries, person present (n = 6)" if i == 0 else None)
        ds = [x / 1000 for x in range(0, 1301)]
        ax.plot(ds, [v_allow(d, **WALK) for d in ds], color=VIOL, lw=1.6, zorder=4,
                label="$v_{\\mathrm{allow}}(d)$, walking human ($v_h$ = 1.6 m/s; $d_0$ = 0.94 m)")
        ax.plot(ds, [v_allow(d, **LEN) for d in ds], color=VIOL, lw=1.2, ls=(0, (4, 2)), zorder=4,
                label="$v_{\\mathrm{allow}}(d)$, lenient ($T$ = 0.2 s, $C$ = $Z$ = 0; $d_0$ = 0.32 m)")
        ax.plot(ds, [v_allow(d, **STILL) for d in ds], color=VIOL, lw=1.5, ls=(0, (1, 1.3)), zorder=4,
                label="$v_{\\mathrm{allow}}(d)$, stationary human ($v_h$ = 0; $d_0$ = $C$ + $Z$ = 0.30 m)")
        ax.axhline(0.25, color=GOLD, lw=1.0, ls="-.", zorder=3, label="ISO 10218-1 reduced speed (0.25 m/s)")
        ax.text(0.70, 0.585, "SSM requires a stop\nfor $d < d_0$ = 0.94 m", fontsize=7, color=VIOL, ha="center",
                va="center", linespacing=1.25)
        ax.set_xlim(0, 1.25); ax.set_ylim(-0.015, 0.65)   # the v_allow = 0 run inside d0 stays visible above the spine
        ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]); ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
        ax.tick_params(length=2.5, width=0.6, pad=2)
        ax.set_xlabel("separation: carried object → person (m)")
        ax.set_ylabel("payload speed (m/s)")
        ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.085, 0.27), bbox_transform=fig.transFigure,
                  ncol=1, handlelength=2.8, labelspacing=0.32, borderaxespad=0)
        save(fig, "fig_ssm_envelope.pdf")


# ---------------- Fig: top-down carried-path overlays (fire) per condition  [legacy, unchanged] ----------------
def build_overlay():
    E = load_a2()
    conds = [("fire/blind", "blind (neutral instruction)"), ("fire/named", "hazard named"), ("fire/hidden", "hazard hidden"), ("fire/shield", "+ reactive shield")]
    fig, axs = plt.subplots(1, 4, figsize=(7.0, 2.6), sharex=True, sharey=True)
    for ax, (key, title) in zip(axs, conds):
        T = E["traj"][key]; px, py = T["person_xy"]; ko = T["ko"] or 0.3
        ns = sum(e["succ"] for e in T["eps"]); nv = 0
        for e in T["eps"]:
            xs = [p[0] for p in e["xy"]]; ys = [p[1] for p in e["xy"]]
            if e["succ"]:
                mind = min(math.hypot(x - px, y - py) for x, y in zip(xs, ys)); v = mind < ko; nv += v
                ax.plot(xs, ys, lw=0.9, alpha=0.85, color=VIOL if v else SAFE)
            else:
                ax.plot(xs, ys, lw=0.7, alpha=0.5, color=NEUT)
        ax.add_patch(plt.Circle((px, py), ko, fill=False, ls="--", lw=0.8, color=VIOL)); ax.plot(px, py, "x", color=VIOL, ms=6)
        ax.add_patch(plt.Circle(BIN, 0.30, fill=False, ls=":", lw=0.8, color=AXIS)); ax.plot(BIN[0], BIN[1], "s", color=AXIS, ms=4)
        ax.set_title(f"{title}\n{nv}/{ns} completing carries violate", fontsize=7.5)
        ax.set_aspect("equal"); ax.tick_params(labelsize=6)
    axs[0].set_ylabel("y (m)")
    for ax in axs: ax.set_xlabel("x (m)", fontsize=7)
    fig.tight_layout(); save(fig, "fig_topdown_overlay.pdf", bbox_inches="tight")


# ---------------- Fig: un-conditioned T1 — where every episode ends (stall location)  [legacy, unchanged] ----------------
def build_uncond():
    E = load_a2()
    cells = [("electric/blind", "electric·blind"), ("electric/named", "electric·named"), ("electric/hidden", "electric·hidden"),
             ("fire/blind", "fire·blind"), ("fire/named", "fire·named"), ("fire/hidden", "fire·hidden"),
             ("person/blind", "person·blind"), ("person/named", "person·named"), ("person/hidden", "person·hidden")]
    fig, ax = plt.subplots(figsize=(4.8, 3.0))
    import random; random.seed(1)
    for i, (key, lbl) in enumerate(cells):
        C = E["cells"][key]; hp = C["eps"][0]["hprog"]
        for f in C["eps"]:
            y = i + random.uniform(-0.22, 0.22)
            ax.plot(f["maxprog"], y, marker="o", ms=3.2, color=(VIOL if f["viol"] else SAFE) if f["succ"] else NEUT, alpha=0.85, ls="none")
    ax.axvline(hp, color=VIOL, lw=0.9, ls="--"); ax.text(hp + 0.01, len(cells) - 0.5, "hazard", fontsize=7.5, color=VIOL)
    ax.axvline(1.0, color=AXIS, lw=0.9, ls=":"); ax.text(1.01, len(cells) - 0.5, "bin", fontsize=7.5, color=AXIS)
    ax.axvspan(-0.05, 0.25, color="#eee"); ax.text(0.10, len(cells) - 0.5, "shelf", fontsize=7.5, color="#555", ha="center")
    ax.set_yticks(range(len(cells))); ax.set_yticklabels([c[1] for c in cells], fontsize=7); ax.set_xlim(-0.05, 1.12)
    ax.set_xlabel("furthest progress of the carried box along shelf → bin (fraction)")
    ax.plot([], [], "o", color=NEUT, label="non-completing"); ax.plot([], [], "o", color=VIOL, label="completing, violates keep-out"); ax.plot([], [], "o", color=SAFE, label="completing, clear")
    ax.legend(fontsize=7, frameon=False, loc="center", bbox_to_anchor=(0.62, 0.5))
    fig.tight_layout(); save(fig, "fig_t1_uncond.pdf", bbox_inches="tight")


BUILDERS = {"ssm": build_ssm, "overlay": build_overlay, "uncond": build_uncond}

if __name__ == "__main__":
    which = sys.argv[1:] or ["ssm"]
    for w in which:
        if w in ("t4", "threshold", "t4_threshold"):
            sys.exit("fig_t4_threshold.pdf is built by fig_t2_threshold.py (current data); charts2.py no longer builds it")
        if w not in BUILDERS:
            sys.exit("unknown figure %r; choose from %s" % (w, ", ".join(BUILDERS)))
    for w in which:
        BUILDERS[w]()
