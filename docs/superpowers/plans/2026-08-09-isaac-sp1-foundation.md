# Isaac SP1 Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring up Isaac Sim + Isaac Lab + IsaacLab-Arena headless on JHU ARCH HPC and reproduce GR00T-N1.7 task success rate (ASR) on the same three LIBERO tasks already validated on MuJoCo — establishing the platform SP2 (perceivable human) will build on.

**Architecture:** Client-server, mirroring the working LIBERO eval. The existing GR00T policy server runs unchanged in its own `groot` env; a new `isaaclab` venv holds only Isaac Sim + Isaac Lab + Arena + a ZMQ client. Only the environment side changes from LIBERO to Isaac/Arena; GR00T is zero-diff. Each task is gated by an empirical sbatch job (T0–T4) that must produce concrete pass evidence before the next task starts.

**Tech Stack:** Python 3.11 venv via `uv`; NVIDIA `isaacsim` pip wheels (`--extra-index-url https://pypi.nvidia.com`); Isaac Lab 3.x; IsaacLab-Arena 0.2.x; PyZMQ; Slurm; Vulkan headless rendering.

## Global Constraints

- Work ONLY under `/weka/scratch/aszalay1/zijian/` (alias `$BASE`). Never run heavy compute on the login node.
- Slurm account ALWAYS `aszalay1_ssci`. Prefer partition `nvl` (access confirmed, has backfill capacity); use short `--time` (≤ 20 min for spikes) for backfill. Do not use `--exclude` node lists on `nvl` (the h05/h07/h11 excludes were h100-only).
- `module` is NOT available on `nvl` compute nodes — do not rely on `module load` there; provision everything through the `uv` venv and check for system libs explicitly.
- Disk: `/weka/scratch` is ~94% full. Run `df -h /weka/scratch` before any multi-GB install; if free space < 30 GB, stop and clean intermediates or request quota before installing.
- SSH: `ssh zzhao140@dsailogin.arch.jhu.edu`. Author scripts locally in the repo, `scp` to the server, `sed -i 's/\r$//'` after copy (Windows CRLF), then run.
- Security: commit ONLY as `simmmooonnn <2516984443@qq.com>` with NO Claude traces (no `Co-Authored-By`, no session trailer). HF token passed ONLY via `sbatch --export=ALL,HF_TOKEN=...`, never written to a file. GitHub token inline in the push URL only, with `git -c credential.helper=`, never in `.git/config` or any file.
- GR00T server command (reuse verbatim, do not modify):
  `$BASE/envs/groot/bin/python gr00t/eval/run_gr00t_server.py --model-path checkpoints/GR00T-N1.7-LIBERO/libero_10 --embodiment-tag LIBERO_PANDA --use-sim-policy-wrapper --port $PORT`
- The three validated tasks (must match LIBERO exactly):
  `KITCHEN_SCENE3_turn_on_the_stove_and_put_the_moka_pot_on_it`,
  `LIVING_ROOM_SCENE6_put_the_white_mug_on_the_plate...` (mug),
  `KITCHEN_SCENE4_put_the_black_bowl_in_the_bottom_drawer_of_the_cabinet_and_close_it`.

---

## File Structure

Server (`$BASE = /weka/scratch/aszalay1/zijian`):
- `$BASE/envs/isaaclab/` — the new uv venv (Isaac client). Isolated from `envs/groot`.
- `$BASE/isaac/` — SP1 working dir: spike scripts, env wrapper, sbatch files, logs.
- `$BASE/isaac/logs/` — job logs.
- `$BASE/safety/ISAAC_SP1/` — results + rendered evidence pulled for the repo.

Repo (`E:\Research\Robotics-Safety`, mirror of what runs on server):
- `isaac_sp1/setup_isaac.sh` — reproducible install recipe (env creation + pins).
- `isaac_sp1/t0_render_spike.py` — headless Isaac Sim render smoke.
- `isaac_sp1/t1_isaaclab_smoke.py` — stock Franka task step smoke.
- `isaac_sp1/t2_arena_probe.py` — Arena LIBERO task instantiation + obs dump.
- `isaac_sp1/arena_groot_env.py` — gym wrapper exposing the GR00T LIBERO obs/action dict, backed by Arena. Registers `arena_sim/<task>`.
- `isaac_sp1/*.sbatch` — one per gate.
- `isaac_sp1/ISAAC_SP1_results.md` — the task×ASR table + recipe.

Reuse (do NOT modify): `code/Isaac-GR00T/gr00t/eval/run_gr00t_server.py`, `code/Isaac-GR00T/gr00t/eval/rollout_policy.py`, and the obs mapping in `code/Isaac-GR00T/gr00t/eval/sim/LIBERO/libero_env.py::LiberoEnv._process_observation` (copy its field names into the Arena wrapper).

---

## Task 0 (Gate T0): Isaac Sim headless render spike — HARD GO/NO-GO

**Files:**
- Create: `isaac_sp1/setup_isaac.sh`, `isaac_sp1/t0_render_spike.py`, `isaac_sp1/t0_spike.sbatch`

**Interfaces:**
- Produces: a working `$BASE/envs/isaaclab` venv with `isaacsim` importable; a rendered PNG proving headless Vulkan works; the pinned isaacsim version + node driver version recorded in `setup_isaac.sh`.

- [ ] **Step 1: Discover available isaacsim wheels + Python + driver (no install yet)**

On a `nvl` GPU node via a 5-min interactive/sbatch probe, record what's installable. Run:
```bash
ssh zzhao140@dsailogin.arch.jhu.edu 'srun -A aszalay1_ssci -p nvl --gpus=1 -t 00:05:00 bash -lc "
  nvidia-smi --query-gpu=driver_version,name --format=csv,noheader;
  ls /usr/lib/x86_64-linux-gnu/libvulkan.so* 2>/dev/null || echo NO_SYSTEM_VULKAN;
  ~/.local/bin/uv python list 2>/dev/null | head;
  ~/.local/bin/uv pip index versions isaacsim --extra-index-url https://pypi.nvidia.com 2>&1 | head"'
```
Decision rule: pick the latest `isaacsim` version whose CUDA build matches the driver (driver ≥ the wheel's minimum). Note the Python it requires (isaacsim 4.5/5.x → 3.10/3.11). If `NO_SYSTEM_VULKAN` and no vulkan loader ships in the wheel, that is a NO-GO signal for Step 4 (not yet — the wheel bundles its own loader for many versions; proceed and let the render test decide).

- [ ] **Step 2: Write `setup_isaac.sh` (env creation + pinned install)**

```bash
#!/bin/bash
# Reproducible Isaac client env. Pins filled in from Task 0 Step 1 discovery.
set -euo pipefail
BASE=/weka/scratch/aszalay1/zijian
UV=~/.local/bin/uv
ISAACSIM_VERSION="${ISAACSIM_VERSION:?set to the version chosen in T0 step1}"
PYVER="${PYVER:-3.11}"
df -h /weka/scratch | tail -1
$UV venv --python $PYVER $BASE/envs/isaaclab
$UV pip install --python $BASE/envs/isaaclab/bin/python \
  "isaacsim[all,extscache]==${ISAACSIM_VERSION}" \
  --extra-index-url https://pypi.nvidia.com
echo "isaacsim ${ISAACSIM_VERSION} installed into envs/isaaclab (py${PYVER})"
```

- [ ] **Step 3: Write `t0_render_spike.py` (headless render → PNG)**

```python
"""T0: prove Isaac Sim launches headless and renders a frame on an ARCH GPU node."""
import os, numpy as np, imageio.v2 as imageio
from isaacsim import SimulationApp
app = SimulationApp({"headless": True, "renderer": "RayTracedLighting"})
import omni.replicator.core as rep
from pxr import UsdGeom
import omni.usd
stage = omni.usd.get_context().get_stage()
UsdGeom.Cube.Define(stage, "/World/Cube")
cam = rep.create.camera(position=(3, 3, 3), look_at=(0, 0, 0))
rp = rep.create.render_product(cam, (256, 256))
rgb = rep.AnnotatorRegistry.get_annotator("rgb"); rgb.attach(rp)
for _ in range(30):
    rep.orchestrator.step()
frame = rgb.get_data()
out = os.environ.get("OUTDIR", "/tmp") + "/t0_frame.png"
imageio.imwrite(out, np.asarray(frame)[..., :3])
print("WROTE", out, np.asarray(frame).shape, "nonzero=", int(np.asarray(frame)[...,:3].sum()))
app.close()
print("T0_OK")
```
Note: if `omni.replicator` capture API differs in the chosen isaacsim version, replace the annotator block with the version's documented camera-capture call; the pass criterion (a non-black 256×256 PNG) is unchanged.

- [ ] **Step 4: Write `t0_spike.sbatch` and run it (the gate)**

```bash
#!/bin/bash
#SBATCH --job-name=t0-spike
#SBATCH --partition=nvl
#SBATCH --gpus=1
#SBATCH --time=00:15:00
#SBATCH --account=aszalay1_ssci
#SBATCH --output=/weka/scratch/aszalay1/zijian/isaac/logs/t0.%j.out
set -uo pipefail
BASE=/weka/scratch/aszalay1/zijian
export OUTDIR=$BASE/safety/ISAAC_SP1; mkdir -p $OUTDIR $BASE/isaac/logs
nvidia-smi --query-gpu=driver_version,name --format=csv,noheader
$BASE/envs/isaaclab/bin/python $BASE/isaac/t0_render_spike.py
echo "exit=$?"
```
Run: `scp` all three files to `$BASE/isaac/`, `sed -i 's/\r$//'`, run `setup_isaac.sh` (with `ISAACSIM_VERSION`/`PYVER` from Step 1) on a GPU node, then `sbatch t0_spike.sbatch`.
Expected PASS: log contains `T0_OK` and `nonzero>` a large number; `safety/ISAAC_SP1/t0_frame.png` is a non-black image.
Expected FAIL modes → action: Vulkan/GL error or black frame → **NO-GO on approach A; escalate to approach B (email cluster admin for Apptainer + NGC Isaac Lab container).** Record the exact error in `ISAAC_SP1_results.md` before switching.

- [ ] **Step 5: Pull evidence and commit**

```bash
scp "zzhao140@dsailogin.arch.jhu.edu:/weka/scratch/aszalay1/zijian/safety/ISAAC_SP1/t0_frame.png" isaac_sp1/
git add isaac_sp1/setup_isaac.sh isaac_sp1/t0_render_spike.py isaac_sp1/t0_spike.sbatch isaac_sp1/t0_frame.png
git -c user.name="simmmooonnn" -c user.email="2516984443@qq.com" commit -m "feat(isaac-sp1): T0 headless render spike passes on ARCH nvl"
```

---

## Task 1 (Gate T1): Isaac Lab installed + stock Franka task steps headless

**Files:**
- Modify: `isaac_sp1/setup_isaac.sh` (append Isaac Lab install)
- Create: `isaac_sp1/t1_isaaclab_smoke.py`, `isaac_sp1/t1_smoke.sbatch`

**Interfaces:**
- Consumes: `$BASE/envs/isaaclab` from Task 0.
- Produces: Isaac Lab importable in the same venv; proof a stock Franka task resets + steps + renders headless.

- [ ] **Step 1: Discover the Isaac Lab version matching the installed isaacsim**

```bash
ssh zzhao140@dsailogin.arch.jhu.edu '~/.local/bin/uv pip index versions isaaclab --extra-index-url https://pypi.nvidia.com 2>&1 | head'
```
Decision rule: choose the Isaac Lab release documented as compatible with the isaacsim version pinned in T0 (Isaac Lab 3.x line for isaacsim 5.x/6.x). If no pip wheel exists for the needed version, clone `github.com/isaac-sim/IsaacLab` at the matching tag and install with its `./isaaclab.sh -i` against the existing venv; record whichever path in `setup_isaac.sh`.

- [ ] **Step 2: Append Isaac Lab install to `setup_isaac.sh`**

```bash
ISAACLAB_VERSION="${ISAACLAB_VERSION:?set from T1 step1}"
$UV pip install --python $BASE/envs/isaaclab/bin/python \
  "isaaclab[isaacsim]==${ISAACLAB_VERSION}" --extra-index-url https://pypi.nvidia.com
$BASE/envs/isaaclab/bin/python -c "import isaaclab; print('isaaclab', isaaclab.__version__)"
```

- [ ] **Step 3: Write `t1_isaaclab_smoke.py`**

```python
"""T1: a stock Isaac Lab Franka task resets, steps, and renders headless."""
from isaaclab.app import AppLauncher
app_launcher = AppLauncher(headless=True, enable_cameras=True)
simulation_app = app_launcher.app
import gymnasium as gym
import isaaclab_tasks  # noqa: F401  (registers Isaac-* envs)
import torch
env = gym.make("Isaac-Lift-Cube-Franka-v0", num_envs=1)
obs, _ = env.reset()
print("obs keys:", list(obs.keys()) if isinstance(obs, dict) else type(obs))
for i in range(20):
    act = torch.zeros(env.action_space.shape, device=env.unwrapped.device)
    obs, rew, term, trunc, info = env.step(act)
env.close(); simulation_app.close()
print("T1_OK")
```
Note: if `Isaac-Lift-Cube-Franka-v0` is not registered in the installed version, list available ids with `[k for k in gym.envs.registry if k.startswith('Isaac-')]` and pick a Franka lift/stack task; record the id used.

- [ ] **Step 4: Write `t1_smoke.sbatch` (copy T0's sbatch, swap script to `t1_isaaclab_smoke.py`, job-name `t1-smoke`) and run it**

Expected PASS: log prints `obs keys:` then `T1_OK`, no crash. FAIL → capture the traceback; if it is a numpy/torch/gym version conflict, pin per Isaac Lab 3.x release notes (this stays inside the `isaaclab` venv, so GR00T is unaffected).

- [ ] **Step 5: Commit**

```bash
git add isaac_sp1/setup_isaac.sh isaac_sp1/t1_isaaclab_smoke.py isaac_sp1/t1_smoke.sbatch
git -c user.name="simmmooonnn" -c user.email="2516984443@qq.com" commit -m "feat(isaac-sp1): T1 Isaac Lab Franka task steps headless"
```

---

## Task 2 (Gate T2): Arena LIBERO task instantiates + exposes GR00T-needed obs

**Files:**
- Modify: `isaac_sp1/setup_isaac.sh` (append Arena install)
- Create: `isaac_sp1/t2_arena_probe.py`, `isaac_sp1/t2_probe.sbatch`

**Interfaces:**
- Consumes: `$BASE/envs/isaaclab` with Isaac Lab from Task 1.
- Produces: a documented way to build a LIBERO-ported Arena task and read, per step, `{agentview RGB, wrist RGB, eef pose, gripper, language}` — the exact fields Task 3's wrapper needs.

- [ ] **Step 1: Install IsaacLab-Arena 0.2.x + GR00T integration**

```bash
ssh zzhao140@dsailogin.arch.jhu.edu 'cd /weka/scratch/aszalay1/zijian/code
  git clone https://github.com/LightwheelAI/isaaclab-arena.git || (cd isaaclab-arena && git fetch)
  cd isaaclab-arena && git checkout 0.2.x 2>/dev/null || git branch -a | head'
```
Then `uv pip install` Arena (and `isaaclab_arena_gr00t` if present) into `envs/isaaclab` per Arena's README. Record the exact package/branch in `setup_isaac.sh`. If the repo URL/branch differs, find the current Arena repo from the Isaac Lab ecosystem docs and record the resolved source.

- [ ] **Step 2: Write `t2_arena_probe.py` (instantiate one LIBERO task, dump obs schema)**

```python
"""T2: build one Arena LIBERO task and print the observation schema + shapes."""
from isaaclab.app import AppLauncher
simulation_app = AppLauncher(headless=True, enable_cameras=True).app
import gymnasium as gym, numpy as np
import isaaclab_arena  # noqa: F401  (registers arena tasks)
# Discover the LIBERO-ported task id(s):
ids = [k for k in gym.envs.registry if "libero" in k.lower() or "LIBERO" in k]
print("ARENA LIBERO IDS:", ids[:20])
assert ids, "no Arena LIBERO task registered — inspect Arena task registry"
env = gym.make(ids[0], num_envs=1)
obs, _ = env.reset()
def describe(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items(): describe(v, p + "/" + k)
    else:
        import numpy as _np
        try: print(p, getattr(o, "shape", None), getattr(o, "dtype", type(o)))
        except Exception: print(p, type(o))
describe(obs)
env.close(); simulation_app.close(); print("T2_OK")
```

- [ ] **Step 3: Write `t2_probe.sbatch` (copy pattern, job-name `t2-probe`) and run it**

Expected PASS: log lists `ARENA LIBERO IDS:` with at least one id and prints an obs schema containing an RGB image tensor, an end-effector/proprioception field, and a task/language field, then `T2_OK`. Record the exact obs key paths + shapes in `ISAAC_SP1_results.md` — Task 3 depends on these names.
FAIL (no LIBERO ids) → Arena LIBERO port not available in this branch; fall back to Arena's RoboCasa Panda task OR the generic Arena manipulation task and record the deviation (this would revisit the spec's comparability assumption — flag to the user, do not silently switch).

- [ ] **Step 4: Commit**

```bash
git add isaac_sp1/setup_isaac.sh isaac_sp1/t2_arena_probe.py isaac_sp1/t2_probe.sbatch
git -c user.name="simmmooonnn" -c user.email="2516984443@qq.com" commit -m "feat(isaac-sp1): T2 Arena LIBERO task obs schema captured"
```

---

## Task 3 (Gate T3): GR00T server ↔ Arena client closed loop (1 episode)

**Files:**
- Create: `isaac_sp1/arena_groot_env.py`, `isaac_sp1/t3_closed_loop.sbatch`

**Interfaces:**
- Consumes: the Arena LIBERO task id + obs key paths from Task 2; the unchanged GR00T server (Global Constraints); the obs field names from `LiberoEnv._process_observation`.
- Produces: `arena_sim/<task>` gym envs whose `reset()/step()` return/accept the GR00T LIBERO modality dict, so the existing `rollout_policy.py` client drives them.

- [ ] **Step 1: Write `arena_groot_env.py` — the obs/action adapter**

Wrap the Arena task so its interface is byte-for-byte what `rollout_policy.py` already sends the GR00T server. Copy the field names from `LiberoEnv._process_observation` exactly:
```python
"""Adapter: Arena LIBERO task -> GR00T LIBERO modality dict (mirror of LiberoEnv)."""
import numpy as np, gymnasium as gym
from gymnasium.envs.registration import register
import isaaclab_arena  # noqa: F401

class ArenaLiberoEnv(gym.Env):
    def __init__(self, arena_task_id: str, task_description: str):
        self._env = gym.make(arena_task_id, num_envs=1)
        self._task_description = task_description
        # observation_space / action_space: identical dict to LiberoEnv
        # (video.image, video.wrist_image, state.x..yaw, state.gripper,
        #  annotation.human.action.task_description ; action.x..gripper).
        # Copy the two spaces verbatim from libero_env.py.

    def _process(self, obs):
        # Map Arena obs keys (from T2 schema) to the GR00T dict:
        agent = _get(obs, AGENT_RGB_KEY)      # 256x256x3 uint8
        wrist = _get(obs, WRIST_RGB_KEY)
        eef   = _get(obs, EEF_POS_KEY)        # xyz
        rpy   = _quat2axisangle(_get(obs, EEF_QUAT_KEY))
        grip  = _get(obs, GRIPPER_QPOS_KEY)
        return {
            "video.image": np.asarray(agent)[::-1, ::-1],
            "video.wrist_image": np.asarray(wrist)[::-1, ::-1],
            "state.x": [float(eef[0])], "state.y": [float(eef[1])], "state.z": [float(eef[2])],
            "state.roll": [float(rpy[0])], "state.pitch": [float(rpy[1])], "state.yaw": [float(rpy[2])],
            "state.gripper": np.asarray(grip, dtype=float),
            "annotation.human.action.task_description": self._task_description,
        }
    # reset()/step(): call self._env, run _process, map the GR00T action dict
    # back to the Arena action tensor (inverse of LiberoEnv.step's concat +
    # normalize_gripper_action + invert_gripper_action), check success via the
    # Arena task's success signal.

def register_arena_libero_envs():
    for task_id, desc in ARENA_TASKS:   # from T2 discovery, the 3 validated tasks
        register(id=f"arena_sim/{task_id}",
                 entry_point="arena_groot_env:ArenaLiberoEnv",
                 kwargs={"arena_task_id": task_id, "task_description": desc})
```
Fill `AGENT_RGB_KEY`/`WRIST_RGB_KEY`/`EEF_*`/`GRIPPER_QPOS_KEY` and `ARENA_TASKS` from the T2 schema. Copy `_quat2axisangle`, the two gym spaces, and the gripper normalize/invert helpers verbatim from `libero_env.py` (DRY — same GR00T contract).

- [ ] **Step 2: Write `t3_closed_loop.sbatch` (start server, wait for port, 1 episode)**

Mirror the working LIBERO sbatch: start the GR00T server (Global Constraints command), poll the port up to 120×5s, then run the client:
```bash
CLIENT_PY=$BASE/envs/isaaclab/bin/python
$CLIENT_PY $BASE/code/Isaac-GR00T/gr00t/eval/rollout_policy.py \
  --env-name "arena_sim/$TASK" --n-episodes 1 --n-envs 1 \
  --n-action-steps 8 --max-episode-steps 720 \
  --policy-client-host 127.0.0.1 --policy-client-port $PORT
```
sbatch header: `--partition=nvl --gpus=1 --time=00:20:00 --account=aszalay1_ssci`, `--export=ALL,HF_TOKEN=<passed at submit>`, `PYTHONPATH` including `$BASE/isaac`. Job-name `t3-loop`.

- [ ] **Step 3: Run the gate**

Submit: `sbatch --export=ALL,HF_TOKEN=$HF_TOKEN t3_closed_loop.sbatch` (HF token from the shell, never a file).
Expected PASS: server reaches ready, the episode runs to completion, `success rate:` prints (0.0 or 1.0 for 1 episode is fine — the gate is "closed loop runs + action convention accepted + success check returns"), no action-shape error.
FAIL (action shape/scale mismatch) → adjust the action mapping in `arena_groot_env.py` (the LIBERO_PANDA convention is 7-dim ΔEEF pose + gripper); re-run. Record the resolved mapping.

- [ ] **Step 4: Commit**

```bash
git add isaac_sp1/arena_groot_env.py isaac_sp1/t3_closed_loop.sbatch
git -c user.name="simmmooonnn" -c user.email="2516984443@qq.com" commit -m "feat(isaac-sp1): T3 GR00T<->Arena closed loop runs one episode"
```

---

## Task 4 (Gate T4): ASR on the three validated tasks + results table

**Files:**
- Create: `isaac_sp1/t4_asr.sbatch`, `isaac_sp1/ISAAC_SP1_results.md`

**Interfaces:**
- Consumes: `arena_sim/<task>` envs from Task 3.
- Produces: the Isaac `task × ASR` table beside LIBERO numbers; SP1 done.

- [ ] **Step 1: Write `t4_asr.sbatch` — 3 tasks × N=15 episodes**

Copy `t3_closed_loop.sbatch`; loop over the 3 validated task ids with `--n-episodes 15`; after each, grep `success rate:` from the task log into a summary block (mirror the LIBERO sbatch summary pattern). Keep `--time` modest and rely on `nvl` backfill; if 3×15 exceeds 20 min, split into one job per task.

- [ ] **Step 2: Run and collect**

Submit with `--export=ALL,HF_TOKEN=$HF_TOKEN`. Poll to completion (background poller pattern: re-ssh `sacct -j <id> --format=State`, pull logs on COMPLETED).
Expected: three `success_rate=` numbers.

- [ ] **Step 3: Write `ISAAC_SP1_results.md`**

Table with columns: task | LIBERO ASR (from `safety/*/results.md`) | Isaac/Arena ASR | note. Plus the full recipe: chosen isaacsim/Isaac Lab/Arena versions, node driver, the exact env-var/action mapping, and the sbatch commands. State plainly any per-task gap and its explanation (physics/render/embodiment). Success = §3 of the spec satisfied.

- [ ] **Step 4: Commit + push**

```bash
scp back logs/figures into safety/ISAAC_SP1/ ; git add isaac_sp1/ safety/ISAAC_SP1/
git -c user.name="simmmooonnn" -c user.email="2516984443@qq.com" commit -m "feat(isaac-sp1): T4 GR00T-in-Isaac ASR reproduced on 3 validated tasks"
git -c credential.helper= push "https://<TOKEN>@github.com/simmmooonnn/vla-motion-safety.git" main
```

---

## Self-Review

**Spec coverage:** §2 in-scope (bring-up, client-server integration, ASR on 3 tasks, table) → Tasks 0–4. §3 success criteria → Task 4 Step 3. §4 architecture (client-server isolation, GR00T unchanged) → Task 3 + Global Constraints. §6 gates T0–T4 → Tasks 0–4 one-to-one. §7 risks: Vulkan → T0 Step 4 fail-branch; driver → T0 Step 1; action convention → T3 Step 3; disk → Global Constraints + T0 pre-check; beta conflicts → T1 Step 4 (isolated venv). §2 out-of-scope (no human/clearance/probes) respected — no task adds them. All covered.

**Placeholder scan:** Version pins (`ISAACSIM_VERSION`, `ISAACLAB_VERSION`) and obs-key names (`AGENT_RGB_KEY` etc.) are intentionally resolved by an explicit discovery step (T0/T1/T2) with a stated decision rule and recorded output — not vague TODOs. All gate pass/fail criteria are concrete.

**Type consistency:** The obs/action dict field names in `arena_groot_env.py` (Task 3) are copied verbatim from `LiberoEnv._process_observation` (`video.image`, `video.wrist_image`, `state.x..yaw`, `state.gripper`, `annotation.human.action.task_description`) so the GR00T server contract matches. `register_arena_libero_envs()` / `arena_sim/<task>` naming is consistent between Task 3 definition and Task 4 use.
