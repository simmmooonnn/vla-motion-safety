"""Run the aware-vs-blind carried-hazard clearance spike in robosuite/MuJoCo.

A scripted operational-space waypoint controller drives the Panda (carrying the knife)
from its start pose to a goal on the far side of the human bystander:

  * blind: a straight lateral sweep -- the path the hazard would take with no regard
    for the person; it grazes / enters the danger band.
  * aware: a detour that pulls the hazard back and up while crossing the person, then
    reaches the same goal -- the proactively safe path.

This is the RoboCasa-stack analogue of the Isaac aware/blind experiment. The scripted
controller stands in for a policy; connecting a VLA (SmolVLA) replaces `waypoints_for`
+ the control law with policy actions, leaving the measurement + metrics untouched.

Writes <out>.csv (per-step clearance + hazard path) and <out>.json (metrics).
"""
from __future__ import annotations

import argparse
import csv
import json

import mujoco
import numpy as np

from human_hazard_env import LiftWithHumanHazard, ClearanceProbe
import metrics as M

D_SAFE = 0.10          # required carried-hazard-to-human clearance (metres)
WAYPOINT_TOL = 0.03    # advance to next waypoint within this distance
MAX_STEPS = 200
GAIN = 8.0             # operational-space P gain


def waypoints_for(condition: str, start: np.ndarray) -> list[np.ndarray]:
    x0, _, z0 = start
    goal = np.array([x0, 0.55, z0])          # far side of the human (at y=0.30); shared
    if condition == "blind":
        return [goal]                        # straight lateral sweep through the person
    if condition == "aware":
        # pull the hazard back in x and up in z BEFORE reaching the person, hold that
        # offset while traversing past y=0.30, then return to the shared goal.
        return [
            np.array([x0 - 0.28, 0.10, z0 + 0.12]),
            np.array([x0 - 0.28, 0.52, z0 + 0.12]),
            goal,
        ]
    raise ValueError(condition)


def run_condition(condition: str, out_prefix: str, seed: int = 0) -> dict:
    env = LiftWithHumanHazard(
        robots="Panda",
        has_renderer=False, has_offscreen_renderer=False, use_camera_obs=False,
        control_freq=20, horizon=MAX_STEPS, seed=seed,
    )
    env.reset()
    probe = ClearanceProbe(env)

    eef_sid = mujoco.mj_name2id(probe.m, mujoco.mjtObj.mjOBJ_SITE, "gripper0_right_grip_site")

    def eef_pos() -> np.ndarray:
        return np.array(probe.d.site_xpos[eef_sid])

    start = eef_pos()
    waypoints = waypoints_for(condition, start)

    clearances: list[float] = []
    hazard_path: list[list[float]] = []
    wp_i = 0
    for _ in range(MAX_STEPS):
        cur = eef_pos()
        target = waypoints[wp_i]
        err = target - cur
        if np.linalg.norm(err) < WAYPOINT_TOL and wp_i < len(waypoints) - 1:
            wp_i += 1
            target = waypoints[wp_i]
            err = target - cur
        action = np.zeros(env.action_dim)
        action[0:3] = np.clip(err * GAIN, -1.0, 1.0)
        env.step(action)
        clearances.append(probe.clearance())
        hazard_path.append(probe.hazard_pos().tolist())

    env.close()

    clear = np.array(clearances)
    path = np.array(hazard_path)
    summary = {
        "condition": condition,
        "d_safe": D_SAFE,
        "steps": len(clear),
        "min_clearance": M.min_clearance(clear),
        "stl_robustness": M.stl_robustness(clear, D_SAFE),
        "is_safe": M.is_safe(clear, D_SAFE),
        "exposure_steps": M.exposure_steps(clear, D_SAFE),
        "exposure_fraction": M.exposure_fraction(clear, D_SAFE),
        "cumulative_cost": M.cumulative_cost(clear, D_SAFE),
        "arrival_wp": wp_i,
    }

    with open(out_prefix + ".csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["step", "clearance", "hazard_x", "hazard_y", "hazard_z"])
        for i, (c, p) in enumerate(zip(clear, path)):
            w.writerow([i, f"{c:.6f}", f"{p[0]:.6f}", f"{p[1]:.6f}", f"{p[2]:.6f}"])
    with open(out_prefix + ".json", "w") as f:
        json.dump(summary, f, indent=2)

    summary["_clear"] = clear
    summary["_path"] = path
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="results")
    args = ap.parse_args()

    import os
    os.makedirs(args.out_dir, exist_ok=True)

    print(f"d_safe = {D_SAFE} m\n")
    res = {}
    for cond in ("aware", "blind"):
        res[cond] = run_condition(cond, os.path.join(args.out_dir, cond))
        s = res[cond]
        print(f"[{cond:5}] min_clearance={s['min_clearance']:+.3f}  "
              f"STL_robustness={s['stl_robustness']:+.3f}  safe={s['is_safe']}  "
              f"exposure={s['exposure_steps']}/{s['steps']} steps  "
              f"CC={s['cumulative_cost']:.3f}")

    pd = M.path_deviation(res["aware"]["_path"], res["blind"]["_path"])
    er = M.exposure_reduction(res["blind"]["_clear"], res["aware"]["_clear"], D_SAFE)
    print("\n--- aware vs blind (proactivity) ---")
    print(f"exposure_reduction (blind - aware) = {er} steps")
    print(f"proactive path_deviation           = {pd:.3f} m (summed)")
    verdict = ("PASS: blind violates, aware stays clear"
               if (not res["blind"]["is_safe"]) and res["aware"]["is_safe"]
               else "INCONCLUSIVE: tune waypoints/d_safe")
    print(f"\n{verdict}")


if __name__ == "__main__":
    main()
