#!/usr/bin/env python3
"""Scene-2 (mug) safety-filter frontier: blind vs reactive (v1) vs phase-aware (v2).

Shows that the phase-aware filter (v2: push only in free transit — start-exclusion
+ goal-fade) shifts the success-vs-clearance frontier up relative to the plain
reactive filter (v1) on the perturbation-fragile mug task.
"""
import glob
import json
import os

import numpy as np

LIFT = 0.03
PERSON = np.array([0.0, -0.05])
BASE = os.path.dirname(os.path.abspath(__file__))


def carry_mask(e):
    z = e["hazard_xyz"][:, 2]
    return z > (z[0] + LIFT)


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
    mn, ex10, sc = [], [], []
    for e in eps:
        m = carry_mask(e)
        p = e["hazard_xyz"][:, :2]
        d = np.linalg.norm(p - PERSON[None, :], axis=1)
        dc = d[m] if m.any() else d
        mn.append(float(dc.min()))
        ex10.append(float((dc < 0.10).mean()) if len(dc) else 0.0)
        sc.append(bool(e.get("success")))
    return np.mean(mn), np.mean(ex10), np.mean(sc), eps


# (label, dir, prefix, group)
CONFIGS = [
    ("blind", os.path.join(BASE, "a1lr6_data"), "A1_", "blind"),
    ("v1 d0.13", os.path.join(BASE, "s1lr6_data", "d0.13_k1.0_p0.40"), "S1_", "v1"),
    ("v1 d0.15a", os.path.join(BASE, "s1lr6_data", "d0.15_k1.0_p0.45"), "S1_", "v1"),
    ("v1 d0.15b", os.path.join(BASE, "s1lr6_data", "d0.15_k1.2_p0.50"), "S1_", "v1"),
    ("v2 d0.12", os.path.join(BASE, "s1v2_data", "v2_d0.12_k0.8_p0.35"), "S1_", "v2"),
    ("v2 d0.13", os.path.join(BASE, "s1v2_data", "v2_d0.13_k1.0_p0.40"), "S1_", "v2"),
    ("v2 d0.15", os.path.join(BASE, "s1v2_data", "v2_d0.15_k1.0_p0.40"), "S1_", "v2"),
    ("v2 d0.18", os.path.join(BASE, "s1v2_data", "v2_d0.18_k1.5_p0.60"), "S1_", "v2"),
    ("v2 d0.20", os.path.join(BASE, "s1v2_data", "v2_d0.20_k1.5_p0.60"), "S1_", "v2"),
]


def main():
    rows = []
    blind_clr = None
    for label, d, pfx, grp in CONFIGS:
        eps = load(d, pfx)
        if not eps:
            print(f"[skip] {label} ({d})"); continue
        mn, ex, sc, ev = metrics(eps)
        if grp == "blind":
            blind_clr = mn
        rows.append(dict(label=label, grp=grp, clr=mn, ex10=ex, succ=sc, n=len(eps)))
    print(f"{'config':12s} {'grp':6s} {'n':>3} {'minClr':>7} {'d%':>6} {'exp<.10':>8} {'success':>8}")
    for r in rows:
        dpct = (r["clr"] / blind_clr - 1) * 100 if blind_clr else 0
        print(f"{r['label']:12s} {r['grp']:6s} {r['n']:>3} {r['clr']:>7.3f} {dpct:>5.0f}% "
              f"{r['ex10']:>8.3f} {r['succ']:>8.3f}")
    make_fig(rows, blind_clr)


def make_fig(rows, blind_clr):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as ex:
        print(f"[fig] no matplotlib ({ex})"); return
    color = {"blind": "tab:red", "v1": "tab:orange", "v2": "tab:green"}
    marker = {"blind": "*", "v1": "s", "v2": "o"}
    fig, ax = plt.subplots(figsize=(7.5, 6))
    seen = set()
    for r in rows:
        g = r["grp"]
        lbl = g if g not in seen else None
        seen.add(g)
        ax.scatter(r["clr"], r["succ"], s=140 if g == "blind" else 90,
                   color=color[g], marker=marker[g], zorder=3, label=lbl,
                   edgecolor="k", linewidth=0.5)
        ax.annotate(r["label"], (r["clr"], r["succ"]), fontsize=7,
                    xytext=(5, 3), textcoords="offset points")
    if blind_clr:
        ax.axvline(blind_clr, ls=":", color="tab:red", lw=1)
    ax.set_xlabel("min clearance to person (m)")
    ax.set_ylabel("task success rate")
    ax.set_title("Scene-2 (fragile mug task): phase-aware v2 shifts the frontier up")
    ax.grid(alpha=0.3); ax.legend()
    out = os.path.join(BASE, "s1_v1v2_scene2.png")
    fig.tight_layout(); fig.savefig(out, dpi=130)
    print(f"[fig] wrote {out}")


if __name__ == "__main__":
    main()
