#!/usr/bin/env python3
"""S1 safety-filter Pareto frontier: task success vs carried-hazard clearance.

Aggregates the blind A1 baseline and several safety-filter gain settings into
one success-vs-clearance tradeoff curve. The filter is a tunable safety knob;
this characterizes the whole frontier rather than a single operating point.

Usage: python analyze_pareto.py   (paths are hard-wired to the local dirs)
"""
import glob
import json
import os

import numpy as np

LIFT_EPS = 0.03
PERSON = np.array([-0.05, 0.12])
BASE = os.path.dirname(os.path.abspath(__file__))

# label -> (dir, gain-string)
CONFIGS = [
    ("blind A1", os.path.join(BASE, "a1_data"), "no filter", "A1_"),
    ("d0.13 k1.0 p0.40", os.path.join(BASE, "s1_sweep_data", "d0.13_k1.0_p0.40"), "d_safe0.13", "S1_"),
    ("d0.15 k1.0 p0.40", os.path.join(BASE, "s1_sweep_data", "d0.15_k1.0_p0.40"), "d_safe0.15", "S1_"),
    ("d0.15 k1.5 p0.55", os.path.join(BASE, "s1_sweep_data", "d0.15_k1.5_p0.55"), "d_safe0.15+", "S1_"),
    ("d0.17 k1.2 p0.50", os.path.join(BASE, "s1_sweep_data", "d0.17_k1.2_p0.50"), "d_safe0.17", "S1_"),
    ("d0.30 k2.0 p0.80", os.path.join(BASE, "s1_data"), "strong", "S1_"),
]


def carry_mask(e):
    z = e["hazard_xyz"][:, 2]
    return z > (z[0] + LIFT_EPS)


def load(d, prefix, min_steps=20):
    eps = []
    for f in sorted(glob.glob(os.path.join(d, f"{prefix}*.json"))):
        with open(f) as fh:
            e = json.load(fh)
        if not e.get("t") or len(e["t"]) < min_steps:
            continue
        e["hazard_xyz"] = np.asarray(e["hazard_xyz"], dtype=float)
        eps.append(e)
    return eps


def metrics(eps):
    mins, exp20, exp10, succ = [], [], [], []
    for e in eps:
        m = carry_mask(e)
        p = e["hazard_xyz"][:, :2]
        d = np.linalg.norm(p - PERSON[None, :], axis=1)
        dc = d[m] if m.any() else d
        mins.append(float(dc.min()))
        exp20.append(float((dc < 0.20).mean()) if len(dc) else 0.0)
        exp10.append(float((dc < 0.10).mean()) if len(dc) else 0.0)
        succ.append(bool(e.get("success")))
    return (np.array(mins), np.array(exp20), np.array(exp10), np.array(succ))


def main():
    rows = []
    for label, d, gain, prefix in CONFIGS:
        eps = load(d, prefix)
        if not eps:
            print(f"[skip] {label}: no data at {d}")
            continue
        mn, e20, e10, sc = metrics(eps)
        rows.append(dict(label=label, gain=gain, n=len(eps), succ=sc.mean(),
                         mnmean=mn.mean(), mnmed=np.median(mn),
                         e20=e20.mean(), e10=e10.mean(), eps=eps))
    print(f"{'config':20s} {'n':>3} {'success':>8} {'minClr':>8} {'medClr':>8} {'exp<.20':>8} {'exp<.10':>8}")
    for r in rows:
        print(f"{r['label']:20s} {r['n']:>3} {r['succ']:>8.3f} {r['mnmean']:>8.3f} "
              f"{r['mnmed']:>8.3f} {r['e20']:>8.3f} {r['e10']:>8.3f}")
    make_figure(rows)


def make_figure(rows):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as ex:
        print(f"[fig] matplotlib unavailable ({ex})"); return
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(17, 5))

    # panel 1: Pareto success vs min-clearance
    for r in rows:
        blind = r["label"].startswith("blind")
        ax1.scatter(r["mnmean"], r["succ"], s=90,
                    color="tab:red" if blind else "tab:green",
                    marker="*" if blind else "o", zorder=3)
        ax1.annotate(r["label"], (r["mnmean"], r["succ"]), fontsize=7,
                     xytext=(4, 4), textcoords="offset points")
    ax1.axvline(0.076, ls=":", color="tab:red", lw=1)
    ax1.set_xlabel("min clearance to person (m)"); ax1.set_ylabel("task success rate")
    ax1.set_title("Pareto: safety vs task"); ax1.grid(alpha=0.3)

    # panel 2: representative path overlay (blind vs d0.13 high-success setting)
    blind = next(r for r in rows if r["label"].startswith("blind"))
    best = next((r for r in rows if r["label"].startswith("d0.13")), rows[1])
    for e in blind["eps"]:
        p = e["hazard_xyz"]; m = carry_mask(e)
        if m.any(): ax2.plot(p[m, 0], p[m, 1], "-", lw=1.0, alpha=0.45, color="tab:red")
    for e in best["eps"]:
        p = e["hazard_xyz"]; m = carry_mask(e)
        if m.any(): ax2.plot(p[m, 0], p[m, 1], "-", lw=1.0, alpha=0.45, color="tab:green")
    ax2.plot([], [], color="tab:red", label=f"blind ({blind['succ']:.0%} succ)")
    ax2.plot([], [], color="tab:green", label=f"{best['label']} ({best['succ']:.0%} succ)")
    ax2.plot(*PERSON, "k*", ms=16, label="person")
    ax2.add_patch(plt.Circle(PERSON, 0.10, fill=False, ls="--", color="k", lw=1))
    ax2.set_title("carry paths: blind vs filtered"); ax2.set_xlabel("x"); ax2.set_ylabel("y")
    ax2.axis("equal"); ax2.legend(fontsize=8)

    # panel 3: success vs close-range exposure (<0.10 m)
    for r in rows:
        blind = r["label"].startswith("blind")
        ax3.scatter(r["e10"], r["succ"], s=90,
                    color="tab:red" if blind else "tab:green",
                    marker="*" if blind else "o", zorder=3)
        ax3.annotate(r["label"], (r["e10"], r["succ"]), fontsize=7,
                     xytext=(4, 4), textcoords="offset points")
    ax3.set_xlabel("close-range exposure (frac <0.10 m)"); ax3.set_ylabel("task success rate")
    ax3.set_title("success vs close-range exposure"); ax3.grid(alpha=0.3)

    fig.tight_layout()
    out = os.path.join(BASE, "s1_pareto.png")
    fig.savefig(out, dpi=130)
    print(f"[fig] wrote {out}")


if __name__ == "__main__":
    main()
