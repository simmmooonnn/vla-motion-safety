# Scene 3 — KITCHEN_SCENE4 (black bowl → drawer) + hazard-person geometry study

**Date:** 2026-08-08 · **Model:** GR00T-N1.7-LIBERO · Hazard = `akita_black_bowl_1_main` ("bowl of hot soup"). Third object/geometry: bowl carried **+y** from table [0.03,-0.05] to the cabinet drawer [0.026, 0.125].

## A1 / D1 replicate
- **A1 (blind):** success **0.90** (= un-probed eval → probe transparent). The bowl grazes a corridor bystander with zero avoidance (blind min-clearance 0.01–0.03 m depending on where the person stands).
- **D1 (danger language):** neutral/caution/danger success 1.0 / 0.95 / 0.85. Clearance to the on-path person: neutral 0.035 → danger 0.045 m, **p = 0.06 (not significant at 0.05)**, Cohen's d = 0.68. Consistent with scenes 1–2 (no significant routing change), though the effect here is borderline — danger wording nudged the bowl slightly *farther* on average but not significantly. The policy still does not reliably route around the person from language alone.

## S1 — the hazard-person geometry study (the "different geometry" experiment)
Same scene/object, filter (v2 phase-aware) run against **bystanders in different positions relative to the carry**. `s3_geometry.png` plots success vs min-clearance:

| bystander geometry | filter config | min clearance (blind→S1) | success |
|---|---|---|---|
| **on-path, far from goal** (0.10,−0.05) | d0.13 | 0.031→0.036 (+17 %, p=0.22) | 0.87 |
| on-path, far from goal | d0.15 | 0.031→0.034 (+11 %, p=0.61) | **1.00** |
| **near goal** (0.05,0.02) | d0.13 | 0.023→0.021 (−7 %, ns) | 0.80 |
| **mid-transit** (0.08,0.04) | d0.15 | 0.014→0.053 (**+278 %**, p<0.001) | 0.13 |
| mid-transit | d0.18 | 0.014→0.054 (**+286 %**, p<0.001) | 0.00 |

**Finding — filter effectiveness is governed by *which carry phase* the closest approach falls in:**
- **near start / near goal:** the phase-aware protections (`r_start`, `goal_fade`) deliberately disable the push there, so the filter can't help → clearance barely moves (but success stays high, 0.8–1.0).
- **mid-transit:** the push is fully active → clearance jumps **+278 %** (highly significant) — but a push strong enough to do that disrupts the (short) bowl placement → success collapses.

## The consistent conclusion across all 3 scenes
The reactive/phase-aware safety filter is a **genuine success-vs-clearance trade-off**, not a free lunch. The achievable operating point depends on **(a)** the task's robustness to action perturbation (robust moka pot: clean +31 %/0.87; fragile mug/bowl: worse) and **(b)** where the bystander's closest approach falls in the carry (mid-transit is steerable; grasp/placement endpoints are not, by design). A clean win-win exists only for robust tasks with mid-transit bystanders; in general, safety and task success trade off — which is itself the honest, useful characterization of when a lightweight action-shield suffices and when a heavier remedy (replanning, or a safety-aware policy) is needed.

Figures: `d1_ks4.png` (D1 twin), `s3_geometry.png` (geometry study). Raw trajectories under `trajectories/`.
