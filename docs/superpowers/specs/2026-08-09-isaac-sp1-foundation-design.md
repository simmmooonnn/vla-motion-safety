# SP1 — Foundation: Isaac on ARCH + GR00T-in-Isaac ASR

**Date:** 2026-08-09 · **Status:** design approved, pending spec review · **Author:** Zijian Su

## 1. Context

The VLA carried-hazard-to-person motion-safety benchmark currently runs on
**LIBERO / MuJoCo** via GR00T's built-in LIBERO eval on the JHU ARCH HPC. That
route produced a publishable first slice (A1 clearance probe, D1 danger-language
twin, S1 action-shield filter, replicated across three scenes). But two of the
proposal's core aims cannot be met on that stack:

- the "person" is an **offline coordinate**, not an entity the policy perceives
  (a static-capsule injection test confirmed a bystander *can* be rendered into
  the LIBERO agentview, but placing a clean, non-occluding, realistic — let alone
  **dynamic** — human is fiddly hand-work); and
- **dynamic / unaware humans (Tier C)** and **realistic scenes (Phase 3)** are
  the project's stated core, and they want Isaac's scene flexibility (arbitrary
  USD assets, animated humans, PhysX contact/distance queries).

The advisor ("学长") directed the project onto **NVIDIA Isaac** (Isaac Lab 3.0 +
IsaacLab-Arena + GR00T N1.7) for exactly these reasons. This spec is the first
sub-project of that migration. Priority is **correctness and realism, not speed**.

### Decisions locked before this spec

- **Compute:** everything runs on **ARCH HPC** ("硬啃 ARCH"). No lab workstation
  or cloud for now.
- **Task substrate:** **Arena's LIBERO port** — run the *same* LIBERO-10 tasks
  inside Isaac so results stay apples-to-apples comparable with the existing
  LIBERO A1/D1/S1 numbers.
- **Bring-up route:** **approach A — pip `isaacsim` + Isaac Lab into a venv**
  (no root, no container), with a spike-first GO/NO-GO gate; **approach B**
  (Apptainer + NGC Isaac Lab container, via cluster admin) is the fallback if
  headless rendering can't be brought up self-service.

### The migration arc (context only — later sub-projects each get their own spec)

| | Sub-project | Success criterion | Depends on |
|---|---|---|---|
| **SP1** (this spec) | Isaac on ARCH + GR00T-in-Isaac ASR | GR00T completes the 3 validated LIBERO tasks inside Isaac/Arena, closed-loop, headless, ASR reproduced | — |
| SP2 | Perceivable static human + PhysX clearance | real human USD in agentview FOV; continuous carried-hazard→person clearance; A1/D1 re-run with a *seen* person | SP1 |
| SP3 | Dynamic human (Tier C) + reaction lead time | animated human (SMPL-X/AMASS or scripted); C1 walk-into-path, C2 back-turned; reaction-lead-time metric | SP2 |
| SP4 | Orientation (Tier B) + richer scenes (Phase 3) | danger-vector angle metric; workshop / multiple bystanders; filter v3 | SP3 |

## 2. Scope

### In scope (SP1)

- Bring up Isaac Sim + Isaac Lab 3.0 + IsaacLab-Arena on ARCH, headless, on Slurm.
- Integrate the existing GR00T-N1.7-LIBERO policy server with the Arena LIBERO
  environment as a **client-server** pair (same shape as the current LIBERO eval).
- Reproduce **task success rate (ASR)** on the three tasks already validated on
  LIBERO: KITCHEN_SCENE3 moka pot, LIVING_ROOM_SCENE6 mug, KITCHEN_SCENE4 bowl.
- Produce a `task × ASR` table (Isaac) placed next to the LIBERO numbers.

### Out of scope (SP1 — YAGNI, deferred to SP2+)

- No human of any kind (static or dynamic).
- No clearance / exposure / safety metric.
- No A1 / D1 / S1 probe re-host.
- No custom USD scenes, no orientation, no dynamics.
- No fine-tuning of GR00T (use the ready checkpoint as-is).

## 3. Success criteria ("done")

SP1 is done when **all** hold:

1. A Slurm batch job, on a GPU compute node, headless, starts the GR00T server,
   instantiates an Arena LIBERO task, and runs GR00T closed-loop to completion.
2. `success rate:` is reported for each of the 3 tasks over N ≥ 15 episodes.
3. The Isaac ASR is **within a defensible band of the LIBERO ASR** for the same
   tasks (target: same order, i.e. high-success tasks stay high). Any large gap
   is *explained* (embodiment/action-convention difference), not hidden.
4. The recipe is captured (env spec, sbatch, exact commands) so it re-runs.

Non-goal: matching LIBERO ASR to the decimal. Isaac physics/rendering differ; the
bar is "GR00T is task-competent in Isaac on these tasks," which is the substrate
SP2 needs.

## 4. Architecture — process isolation (key decision)

Reuse the **client-server** structure already working in the LIBERO eval:

- **GR00T policy server** — the existing `run_gr00t_server.py`, **unchanged**:
  `groot` env, checkpoint `GR00T-N1.7-LIBERO/libero_10`, embodiment tag
  `LIBERO_PANDA`, `--use-sim-policy-wrapper`, ZMQ port. Needs `HF_TOKEN` for the
  gated Cosmos-Reason2-2B backbone (passed via `sbatch --export`, never written
  to a file).
- **Isaac/Arena client** — a **new** venv (`isaaclab`) holding only isaacsim +
  Isaac Lab + Arena + ZMQ client. It builds the scene, emits observations,
  applies GR00T's action chunk, checks success.

**Why this shape:** GR00T runs in its own environment, so the Isaac client env
only needs Isaac/Arena/ZMQ dependencies. GR00T's torch/numpy/transformers stack
never has to co-resolve with Isaac Lab 3.0 Beta's — which sidesteps the
beta-dependency-conflict risk the advisor's plan flagged. Only the "env side"
changes from LIBERO to Isaac; the GR00T side is zero-diff.

## 5. Data flow

```
Isaac/Arena scene
  → observation { agentview RGB, wrist RGB, joint proprioception, language }
  → (ZMQ) → GR00T server
  → 16-step action chunk
  → (ZMQ) → Arena applies to the Franka
  → step sim → repeat
per-episode success check → aggregate → ASR
```

Identical in shape to the LIBERO eval; only the environment implementation differs.

## 6. Staged bring-up + test gates (each is a GO/NO-GO)

| Gate | What runs | Pass = | On fail |
|---|---|---|---|
| **T0 — render spike** | fresh venv on a GPU node; `pip install isaacsim`; launch headless `SimulationApp`; create a stage; render one frame → PNG | a non-empty rendered frame comes back | escalate to **approach B** (admin + Apptainer + NGC container) before downloading the full stack |
| **T1 — Isaac Lab** | install Isaac Lab; run a stock task (`Isaac-Lift-Cube-Franka-v0`) a few steps with a random/scripted policy, headless | env steps and renders without crashing on Slurm | pin versions / consult Isaac Lab 3.0 beta issues |
| **T2 — Arena env** | install Arena; instantiate one LIBERO-ported task; step with random actions | obs contains the RGB + joint state + language GR00T needs | check Arena 0.2.x / isaaclab_arena_gr00t wiring |
| **T3 — closed loop** | wire GR00T server ↔ Arena client; 1 episode, 1 task | episode runs; success check returns; action convention accepted | write action-space adapter (see §7) |
| **T4 — ASR** | 3 tasks × N≥15 episodes | ASR table produced, compared to LIBERO | investigate per-task gaps |

**T0 is the hard gate:** prove headless rendering works on an ARCH compute node
(ten minutes of spike) *before* downloading tens of GB — so a missing Vulkan
stack is discovered cheaply, not after a long install.

## 7. Risks & mitigations

- **Headless rendering needs Vulkan** (Isaac Sim uses Vulkan, not just MuJoCo's
  EGL). The compute node must have a Vulkan ICD + usable GPU. → **T0** verifies
  this first; fallback is approach B.
- **Driver compatibility** — isaacsim wheels have a minimum NVIDIA driver. → T0
  records `nvidia-smi` driver version and checks it against the wheel's minimum.
- **Action-convention mismatch** — GR00T-N1.7-LIBERO emits the LIBERO_PANDA
  convention (7-dim ΔEEF pose + gripper, with LIBERO's gripper
  normalize/invert). Arena's LIBERO-Franka must accept the same convention or an
  adapter is needed. The local `isaac_groot/` scaffold was created for exactly
  this. → verified at **T3**; adapter is the mitigation.
- **Disk pressure** — `/weka/scratch` is ~94% full; isaacsim + Isaac Lab is
  ~15–25 GB. → check `df` before install; clean LIBERO intermediates; request
  quota if needed. Install under `/weka/scratch/aszalay1/zijian/`.
- **Isaac Lab 3.0 is Beta** — known open dependency conflicts. → the client-server
  isolation (§4) keeps GR00T's stack out of it; pin the Arena 0.2.x / Isaac Lab
  3.0 branch matching the isaacsim wheel version.

## 8. Deliverables

- `envs/isaaclab/` (or equivalent) — the Isaac client venv, with a recorded
  install recipe (`setup_isaac.sh`).
- An Arena↔GR00T eval entry point (reuse/mirror `rollout_policy.py`'s role).
- Slurm sbatch(es) following the existing pattern: start GR00T server, wait for
  port, run the Arena eval headless, print `success rate:`.
- `safety/ISAAC_SP1/results.md` — the Isaac `task × ASR` table beside the LIBERO
  numbers, plus the exact recipe.

## 9. Constraints (standing)

- **ARCH rules:** work only in `/weka/scratch/aszalay1/zijian/`; always Slurm
  account `aszalay1_ssci`; never run heavy compute on the login node; clean up
  large intermediates. Congested queue → prefer the **nvl** partition (access
  confirmed) and short `--time` for backfill.
- **Security:** commit only as `simmmooonnn <2516984443@qq.com>` with **no Claude
  traces** (no Co-Authored-By, no session trailer). HF token via
  `sbatch --export` only; never written to any file. GitHub token inline in the
  push URL only; never stored in `.git/config` or any file.

## 10. Assumptions to verify during implementation

- isaacsim ships pip wheels compatible with ARCH's GPU driver (checked at T0).
- IsaacLab-Arena 0.2.x provides a LIBERO task port usable with GR00T (checked at
  T2/T3); if the GR00T integration package is unavailable, we build a thin
  adapter using Arena's generic policy runner.
- The GR00T-N1.7-LIBERO checkpoint drives the Arena LIBERO-Franka with at most a
  small action-convention adapter (checked at T3).
