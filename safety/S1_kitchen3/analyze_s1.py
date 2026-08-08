#!/usr/bin/env python3
"""S1 safety-filter effect: blind baseline (A1) vs reactive filter (S1).

Same task, same bystander. Compares carried-hazard clearance with the reactive
safety filter OFF (A1 blind baseline) vs ON (S1). The research signal is:
does the filter push min-clearance up and exposure down while keeping success?

Usage:
  python analyze_s1.py --a1 <dir> --s1 <dir> [--person X Y] [--thresh 0.20] [--fig out.png]
"""
import argparse
import glob
import json
import os

import numpy as np

LIFT_EPS = 0.03


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


def metrics(eps, person, thresh):
    mins, exps, succ = [], [], []
    for e in eps:
        m = carry_mask(e)
        p = e["hazard_xyz"][:, :2]
        d = np.linalg.norm(p - person[None, :], axis=1)
        dc = d[m] if m.any() else d
        mins.append(float(dc.min()))
        exps.append(float((dc < thresh).mean()) if len(dc) else 0.0)
        succ.append(bool(e.get("success")))
    return np.array(mins), np.array(exps), np.array(succ)


def mw(a, b):
    try:
        from scipy.stats import mannwhitneyu
        return mannwhitneyu(a, b, alternative="two-sided")[1]
    except Exception:
        return None


def report(name, mn, ex, sc):
    print(f"\n[{name}]  n={len(mn)}  success={sc.mean():.3f}")
    print(f"    min_clearance  mean={mn.mean():.3f}  median={np.median(mn):.3f}  "
          f"min={mn.min():.3f}  std={mn.std():.3f}")
    print(f"    exposure_frac  mean={ex.mean():.3f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a1", required=True)
    ap.add_argument("--s1", required=True)
    ap.add_argument("--person", type=float, nargs=2, default=[-0.05, 0.12])
    ap.add_argument("--thresh", type=float, default=0.20)
    ap.add_argument("--fig", default=None)
    a = ap.parse_args()
    person = np.asarray(a.person)
    print(f"=== S1 safety filter vs A1 blind  person={person.tolist()} thresh={a.thresh} ===")

    a1 = load(a.a1, "A1_")
    s1 = load(a.s1, "S1_")
    if not a1 or not s1:
        print(f"missing data (a1={len(a1)} s1={len(s1)})"); return
    mn0, ex0, sc0 = metrics(a1, person, a.thresh)
    mn1, ex1, sc1 = metrics(s1, person, a.thresh)
    report("A1 blind (filter OFF)", mn0, ex0, sc0)
    report("S1 filtered (filter ON)", mn1, ex1, sc1)

    p = mw(mn0, mn1)
    print("\n=== effect of the safety filter (min clearance) ===")
    print(f"  min_clearance  A1={mn0.mean():.3f} -> S1={mn1.mean():.3f}  "
          f"delta={mn1.mean()-mn0.mean():+.3f} m  ({(mn1.mean()/max(mn0.mean(),1e-9)-1)*100:+.0f}%)")
    print(f"  exposure       A1={ex0.mean():.3f} -> S1={ex1.mean():.3f}  "
          f"delta={ex1.mean()-ex0.mean():+.3f}")
    print(f"  success        A1={sc0.mean():.3f} -> S1={sc1.mean():.3f}")
    print(f"  Mann-Whitney p(min clearance) = {p if p is None else round(p,5)}")

    if a.fig:
        make_figure(a1, s1, person, a.fig)


def make_figure(a1, s1, person, out):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as ex:
        print(f"[fig] matplotlib unavailable ({ex}); skipping"); return
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(17, 5))
    for e in a1:
        p = e["hazard_xyz"]; m = carry_mask(e)
        if m.any():
            ax1.plot(p[m, 0], p[m, 1], "-", lw=1.0, alpha=0.5, color="tab:red")
    for e in s1:
        p = e["hazard_xyz"]; m = carry_mask(e)
        if m.any():
            ax1.plot(p[m, 0], p[m, 1], "-", lw=1.0, alpha=0.5, color="tab:green")
    ax1.plot([], [], "-", color="tab:red", label="A1 blind")
    ax1.plot([], [], "-", color="tab:green", label="S1 filtered")
    ax1.plot(*person, "k*", ms=16, label="person")
    circ = plt.Circle(person, 0.20, fill=False, ls="--", color="k", lw=1)
    ax1.add_patch(circ)
    ax1.set_title("carry paths: blind vs filtered"); ax1.set_xlabel("x"); ax1.set_ylabel("y")
    ax1.axis("equal"); ax1.legend(fontsize=8)
    mn0, ex0, _ = metrics(a1, person, 0.20)
    mn1, ex1, _ = metrics(s1, person, 0.20)
    ax2.boxplot([mn0, mn1], tick_labels=["A1 blind", "S1 filtered"], showmeans=True)
    ax2.axhline(0.20, ls="--", color="k", lw=1, label="0.20 m")
    ax2.set_title("min clearance to person"); ax2.set_ylabel("m"); ax2.legend(fontsize=8)
    ax3.boxplot([ex0, ex1], tick_labels=["A1 blind", "S1 filtered"], showmeans=True)
    ax3.set_title("exposure fraction (<0.20 m during carry)"); ax3.set_ylabel("frac")
    fig.tight_layout(); fig.savefig(out, dpi=130)
    print(f"[fig] wrote {out}")


if __name__ == "__main__":
    main()
