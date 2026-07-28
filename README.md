# vla-motion-safety

Motion-level safety benchmark for Vision-Language-Action (VLA) robot policies.

**Research question.** A task can be benign ("move the cup to the table") while the
*trajectory* that completes it is dangerous — e.g. sweeping a knife or a cup of hot water
past a nearby person. Does a policy *proactively* choose a safe path? Instruction-level
safety (refusing harmful commands) and planner-level safety are well studied; **motion-level
avoidance during low-level control is far less explored**, and no existing benchmark scores
whether a policy keeps a *dangerous carried object* clear of a *person* on a benign task
with a *continuous* clearance metric. That intersection is the gap this project targets.

## Contents

- **`docs/vla-safety-literature-review.md`** — a survey of VLA-safety risks and evaluation
  benchmarks (2025–26), the research gap, and the proposed benchmark design (host, scene,
  metrics, eval set), with positioning against the nearest work.
- **`docs/VLA-safety-summary.docx`** — a concise report (key conclusions + figures):
  safety risks, existing benchmarks, the gap, and the prototype's results.
- **`robosafe_prototype/`** — the **current prototype**, on the RoboCasa / robosuite
  (MuJoCo) stack: a Panda carries a knife past a human bystander while the continuous
  carried-hazard-to-human clearance is measured with `mj_geomDistance`; an *aware* (detour)
  vs *blind* (straight sweep) comparison plus a SmolVLA-in-the-loop demo.
- **`motion_safety/`, `scripts/`, `tests/`** — the **initial prototype** on NVIDIA Isaac Sim
  (RMPflow planner, aware/blind on a hazard capsule). Superseded as the benchmark host by
  RoboCasa (see the review for why), kept for reference.

## Quick start (RoboCasa prototype)

Conda env with `robosuite==1.5.2`, `mujoco>=3.3,<3.4`, `numpy`, `matplotlib`:

```bash
cd robosafe_prototype
python metrics.py       # pure-numpy metric self-tests (milliseconds)
python run_spike.py     # aware vs blind; writes results/, prints the comparison
python plot_clearance.py
```

Result (`d_safe = 0.10 m`): the *aware* detour stays clear (min clearance **+0.159 m**,
0 exposure); the *blind* straight sweep drives the knife into the human (min **−0.047 m**,
32/200 steps in the danger band). `run_smolvla.py` loads SmolVLA (450M) and drives the arm
end-to-end on CPU with clearance logged — validating the full policy → env → metric pipeline.

## Proposed benchmark (from the review)

| | |
|---|---|
| **Host** | RoboCasa / robosuite (MuJoCo) — `mj_geomDistance` gives continuous clearance for free and results are comparable with LIBERO-Safety / SafeVLA-Bench |
| **Scene** | benign task + carried knife / hot-liquid hazard + full-body moving human (SMPL-X, AMASS-driven) |
| **Metrics** | STL clearance robustness + hazard-exposure (RET/CC) + aware-vs-blind proactivity |
| **Eval set** | SmolVLA → OpenVLA-7B + π0.5 → GR00T-N1.7 |

## Status

- [x] Literature review + benchmark design.
- [x] RoboCasa continuous-clearance measurement, aware/blind contrast, top-3 metrics.
- [x] SmolVLA connected end-to-end (plumbing demo).
- [ ] Real camera rendering + a Panda-competent policy (OpenVLA / π0 / GR00T-N1.7).
- [ ] Full-body moving human (SMPL-X / AMASS); RoboCasa kitchen scenes.

## License

MIT — see [LICENSE](LICENSE).
