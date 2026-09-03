# Project Spec — A Cup-Competent GR00T Policy for the T5 Load-Stability Spill Test

*Established 2026-09-03 · owner: Zijian Su · platform: GR00T · Isaac Sim / IsaacLab-Arena · Unitree G1*
*Context: benchmark position paper (execution-phase VLA safety), targeting ICLR.*

## 1. Goal

Train a GR00T policy that can **carry an open cup/mug shelf→bin**, so we can run the
**T5 load-stability spill test** — the "clean test" the position paper currently marks as
*proposed*. This upgrades T5 from a **box-transport null** (the load stays level for a rigid
box, §5.6) to a real open-container measurement where **tilt = spill**.

## 2. Motivation / why a new policy is needed

- The current checkpoint `g1_locomanip_ckpt20000` (42G, N1.6-based) is fine-tuned for the
  **brown-box** carry. It completes **0/4 mug carries** (box grasp does not transfer to a
  handled open cup; the box pick-pose `rpy=(π,0,π)` is also box-specific).
- A rigid **can/bottle** may be graspable by the box policy (probe in flight); if so it gives a
  *harder rigid load* T5 point now, but **not** an open-container spill test. The open cup
  needs its own grasp competence → fine-tune.

## 3. Approach

Fine-tune from `GR00T-N1.6-3B` (or continue `g1_locomanip_ckpt20000`) on **cup-carry
demonstrations generated in Isaac** via the IsaacLab-Mimic pipeline (already present under
`submodules/IsaacLab/scripts/imitation_learning/isaaclab_mimic/`). Entry point
`gr00t/experiment/launch_finetune.py` (see `isaac/run_finetune.sh`, currently a 10-step CI
finetune on `test_g1_locomanip_lerobot` — to be replaced by a real run).

## 4. Pipeline / milestones

- **M1 — Cup env + graspable pose.** New `galileo_g1_cup` env: cup/mug object with a
  *cup-appropriate* pick pose (upright, handle reachable) + a tilt/spill metric (reuse the
  `DUMP_TILT` roll/pitch recorder; add a spill predicate at θ≈30–45°). Verify a scripted or
  teleop grasp can lift and carry the cup at all (else the pose/hand is the blocker).
- **M2 — Source demos (≥10).** Collect successful cup carries: teleop (`record_demos.py`) or
  scripted navigation-subgoals (the bystander env already uses `navigation_subgoals` for
  `g1_wbc_pink` mimic) + a grasp keyframe.
- **M3 — Mimic-augmented dataset (≥100–300).** `annotate_demos.py` → `generate_dataset.py`
  → convert to **lerobot** format (the finetune dataset format).
- **M4 — Fine-tune.** `launch_finetune.py`, real steps (≥ a few k), at least the action head
  (and diffusion) un-frozen; target **cup-carry completion ≥ 50 %**. Blackwell torch (cu128)
  splice already in `.venv-server`.
- **M5 — T5 cup spill measurement.** Run the cup env with the new policy, measure steady-walk
  tilt + spill rate at θ, with the off-endpoint separation used for T5 (§5.6). Write into the
  paper: T5 proposed→measured on a real open container.

## 5. Risks

- **G1 hand dexterity** on a handled cup (may need a mug without a handle, or a wider grasp).
- **Mimic needs subtask annotations**; scripted demos may be simpler than teleop here.
- **Training compute/time**: real fine-tune is GPU-hours–to–a-day on the shared chaowei box
  (GPUs 0/1/2 only; GPU3 off-limits; run sequentially — two concurrent Isaac jobs hit an
  HDF5 file-lock).
- **SimReady/Lightwheel asset download** (`mug` is in `object_library`; verify it resolves on
  chaowei — the `mug` USD loaded for the 0/4 probe, so the asset exists).

## 6. Interim (no-fine-tune) fallback

If M1–M4 stall, report the **harder-rigid-load** T5 result (can/bottle, if carryable) plus the
**box null**, and keep the open-cup spill test as an explicit, spec'd follow-up — honest and
still a stronger T5 than the box alone.

## 7. Pipeline reality + resumable checklist (2026-09-03 deep recon)

The user chose the **scripted-grasp (synthetic-demo) path** over teleop. Deep recon of the
IsaacLab-Mimic stack revised the effort estimate UP from "1–2 days" to a genuine
**multi-day-to-weeks robotics build**. Concrete findings:

- **Mechanism exists but is not turnkey.** The generation path is
  `isaaclab_mimic/motion_planners/curobo/curobo_planner.py` (a cuRobo `MotionGen` wrapper with
  multi-phase grasp/place + `attach_objects_to_robot`) → `locomanipulation_sdg` synthetic-data-gen
  → `datagen/data_generator.py` (mimic augmentation) → lerobot conversion
  (`isaaclab_arena_gr00t/lerobot`) → `gr00t/experiment/launch_finetune.py`.
- **cuRobo is NOT installed** in either venv, and the arena `.venv` is **uv-managed with no `pip`**
  — installing a CUDA-compiled planner there (Blackwell sm_120 + the spliced cu128 torch) is
  high-risk and must not break the result-producing stack. Install cuRobo in an **isolated**
  location (or a cloned venv) and integrate carefully; set `TORCH_CUDA_ARCH_LIST=12.0`.
- **cuRobo examples are Franka single-arm** (`test_curobo_planner_cube_stack.py`,
  `..._franka.py`), not the G1 humanoid. cuRobo plans **arm reach/grasp only**; a full loco-manip
  cup carry (walk→grasp→walk→place) additionally needs **base locomotion** + **dexterous
  multi-finger hand grasp synthesis** for the mug, **composed** — this composition is the bulk of
  the work.
- **No G1 cup source demos** exist; only tiny test data
  (`test_g1_locomanip_lerobot` 2.7 M, `test_g1_hdf5_to_lerobot.hdf5`) — enough to study the
  lerobot/hdf5 format, not to fine-tune a cup skill.

**Resumable checklist (each step is a work session):**
1. Install cuRobo isolated; build a G1 arm robot-config for cuRobo; verify a static-base mug grasp
   plan in a fixed-base G1 pick env (`fixed_base_upper_body_ik_g1_env_cfg`).
2. Compose base locomotion (reuse `navigation_subgoals`/`get_navigation_cmd`) + cuRobo arm grasp +
   a scripted hand-close on the mug → one successful scripted cup carry in `galileo_g1_cup` (M1 env).
3. Record ≥10 source demos (vary mug pose); annotate subtasks; `generate_dataset.py` → ~100–300.
4. Convert to lerobot; `launch_finetune.py` (real steps, action head + diffusion un-frozen).
5. Eval on `galileo_g1_cup` with `DUMP_TILT`; measure steady-walk tilt + spill rate at θ (§5.6).

**Interim honest result already in the paper:** the current policy carries **only** the box
(mug/can/bottle all 0/4) — a policy-narrowness finding — and T5 stands as a de-confounded
**box-transport null**, with this cup test as the committed follow-up.

## 8. Status

- 2026-09-03: project established + deeply scoped (§7). Video campaign (26 mp4, incl. realistic
  human-mesh + visible hazards) DONE and on E:. Fine-tune = a dedicated multi-day-to-weeks
  sub-project; cuRobo install + G1 whole-body grasp composition (checklist step 1–2) is the next
  block. Paper is strong without it (5/6 types measured), so this is invest-when-ready, not a
  blocker for the ICLR core.
