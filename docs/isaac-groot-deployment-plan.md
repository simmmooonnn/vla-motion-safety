# Plan: Deploy GR00T on Isaac Sim, measure ASR, then build safety scenarios

**Goal (advisor-directed, 2026-07-28):** deploy a mainstream, Isaac-native VLA policy
(NVIDIA **GR00T**) inside Isaac Sim, put a robot arm in a ready environment, drive it with
different instructions, and **measure task success rate (ASR)** on simple tasks. Then, on the
tasks it does reliably, **construct safety scenarios** and test its zero-shot safe-motion
behavior.

**Why Isaac + GR00T** (vs. the RoboCasa/SmolVLA spike): GR00T is *Isaac-native*, which fixes
the cross-embodiment mismatch that made our SmolVLA-on-robosuite run non-task-competent —
i.e. GR00T should actually complete tasks. Isaac gives higher DOF, more realism, and richer
scenes than RoboCasa's kitchen focus. And `IsaacLab-Arena` ports RoboCasa + LIBERO tasks
*into* Isaac, so we keep comparability with the benchmark literature too.

---

## Decisions to pin first

1. **Model = GR00T N1.7** (not N1.6). N1.7 (Apr 2026, GA) is the latest, is the **first
   commercially-licensed** release (N1.6/earlier are non-commercial, 3B), and ships ready
   checkpoints — including a **Franka** one, `nvidia/GR00T-N1.7-LIBERO` (130 language-conditioned
   pick/place tasks in sim, works out-of-box). Base model: `nvidia/GR00T-N1.7-3B`. (Confirm with
   advisor whether there's a reason to stay on 1.6.)
2. **Stack = Isaac Lab 3.0 Beta 2 + your Isaac Sim 6.0.1 + IsaacLab-Arena 0.2.x.** This keeps
   you on 6.0.1 — **no downgrade**. ⚠️ *Avoid* `IsaacLabEvalTasks` and Arena 0.1.x: they pin
   Isaac Sim 5.0 / Lab 2.2 (the GR1-T2 humanoid "nut pouring" example).
3. **Compute = a ≥16 GB GPU is mandatory** (Isaac Sim rendering needs ≥16 GB *and* GR00T
   inference needs ≥16 GB); ≥24 GB preferred to co-locate both; fine-tuning (if needed) ≥40 GB.
   **The 4 GB laptop cannot run the GR00T-in-Isaac loop** — this is what the server is for.

### Where each thing runs

| Laptop (4 GB, now) | Server (≥16 GB, when ready) |
|---|---|
| author scene/task configs; write obs→action adapters; iterate on the plan; read code | GR00T inference + Isaac Sim rendering; ASR eval runs; safety-scenario runs; any fine-tuning |

---

## Phase 0 — Environment bring-up (server)

- Install **Isaac Lab 3.0 Beta 2** (the release matching Isaac Sim 6.0.1) + **IsaacLab-Arena 0.2.x**
  + the `isaaclab_arena_gr00t` integration package.
- Pull GR00T: `nvidia/GR00T-N1.7-3B` and `nvidia/GR00T-N1.7-LIBERO`. Request access to the gated
  backbone repo `nvidia/Cosmos-Reason2-2B`.
- **Smoke test (no robot yet):** start GR00T's inference server
  (`gr00t/eval/run_gr00t_server.py --model-path nvidia/GR00T-N1.7-3B --port 5555`) and hit it with
  the standalone/replay example to confirm it loads and returns an action chunk on the server GPU.

*Expect setup friction:* Isaac Lab 3.0 is still Beta (known open dependency conflicts). Budget a
day or two for the install.

## Phase 1 — Deploy on a known task and measure ASR (advisor's step 1)

The fast path avoids fine-tuning by using an embodiment GR00T already knows:

- **Option A (fastest):** the LIBERO-Franka checkpoint `GR00T-N1.7-LIBERO` on LIBERO tasks inside
  Arena — pick/place, already language-conditioned, Franka arm.
- **Option B:** Arena's pre-wired **Panda-Omron** embodiment on RoboCasa tasks (GR00T is
  benchmarked here, ~70% average SR).

Then:
- Run closed-loop eval with Arena's `policy_runner.py` (GPU-parallel envs), or robomimic
  `play.py --num_rollouts N` for stock Isaac Lab Franka tasks (`Isaac-Lift-Cube-Franka-v0`,
  `Isaac-Stack-Cube-Franka-v0`, `Isaac-Open-Drawer-Franka-v0`).
- **Try different instructions**, run N episodes per task, record **success rate**.
- **Deliverable:** a table of *task × ASR* → the list of tasks GR00T completes reliably. These
  become the substrate for Phase 2 (we only test safety on tasks it can already do).

The observation GR00T needs each step: `{RGB camera(s), joint proprioception, language string}`;
its output is a **16-step joint-target action chunk** applied to the arm before re-querying.

## Phase 2 — Construct safety scenarios on the reliable tasks (advisor's step 2)

On a high-ASR task, use Arena to inject:
- a **hazard** — a carried dangerous object (knife / hot item) attached to the gripper;
- a **human bystander** — a kinematic/animated USD placed in the scene.

Add a **safety metric** term: the continuous **carried-hazard-to-person clearance** (a PhysX
distance query — the Isaac analog of the `mj_geomDistance` clearance we already prototyped on
RoboCasa), plus hazard-exposure and the aware-vs-blind proactivity comparison.

Run GR00T **zero-shot** and measure whether it keeps the hazard clear of the person while still
completing the benign task. This is exactly the carried-hazard-to-person benchmark idea from the
literature review — now on Isaac.

## Phase 3 — Richer, more realistic scenarios

Leverage Isaac's flexibility (the advisor's main reason for choosing it): expand beyond kitchen
tasks to more diverse, realistic hazard scenarios (workshop, tools, multiple bystanders, dynamic
humans).

---

## What carries over from the existing work

- **Clearance metric + aware/blind design + metrics** (STL clearance robustness, exposure, aware-vs-blind
  proactivity) from `robosafe_prototype/` port directly — swap `mj_geomDistance` for a PhysX/USD
  distance query in Isaac.
- The **literature review** (`docs/vla-safety-literature-review.md`) frames Phase 2's contribution
  and its positioning.
- The **first Isaac prototype** (`motion_safety/`) already established the Isaac bring-up and the
  aware/blind measurement on a hazard capsule.

## Open questions for the advisor

- **Model:** OK to use N1.7 (latest, commercial, ready Franka checkpoint) rather than N1.6?
- **Server:** ≥16 GB is enough for *inference + rendering*; do we also want ≥40 GB so we can
  post-train GR00T on a custom Franka rig later, or start entirely with Arena's pre-wired
  embodiments (no fine-tuning)?
- **First milestone:** reproduce a GR00T Arena eval as-is (Phase 1) before authoring any custom
  scene — agree?

## Risks / watch-items

- Isaac Lab 3.0 is **Beta** — setup friction (open dependency conflicts, issue #6200).
- GR00T is **not zero-shot on an arbitrary Franka** — use Arena's pre-wired embodiments, or budget
  a small post-training (10–30K steps, one ≥40 GB GPU).
- **Version pinning:** some Lightwheel/Arena badges show Isaac Sim 5.0 (that's the *legacy* 0.1.x
  line) — pin to an Arena **0.2.x / Isaac Lab 3.0** branch for Isaac Sim 6.0.1.
