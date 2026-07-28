# isaac_groot — GR00T on Isaac Sim

Deploying NVIDIA **GR00T N1.7** in Isaac Sim / Isaac Lab, measuring task success rate,
then injecting safety scenarios. See the full plan in
[`../docs/isaac-groot-deployment-plan.md`](../docs/isaac-groot-deployment-plan.md).

## What runs where

- **Laptop (4 GB, now):** author configs, write/adapt glue code, unit-test the pure-Python
  parts (`python groot_adapter.py`). **Cannot** run Isaac rendering or GR00T inference.
- **Server (≥16 GB GPU):** GR00T inference + Isaac Sim rendering + eval. ≥24 GB to co-locate
  both; ≥40 GB if we later fine-tune. This is the compute the advisor is preparing.

## Contents

- `groot_adapter.py` — pure-Python glue: builds GR00T's observation dict `{video, state,
  language}` and feeds its 16-step action chunk out one step at a time. Works with either the
  local `Gr00tPolicy` or the ZMQ `PolicyClient`. Self-tested (`python groot_adapter.py`), no GPU.
- Safety metrics are **reused** from [`../robosafe_prototype/metrics.py`](../robosafe_prototype/metrics.py)
  (STL clearance robustness, exposure, aware-vs-blind proactivity — sim-agnostic).

## Server setup (Phase 0) — run when the GPU box is ready

Stack: **Isaac Lab 3.0 Beta 2 + Isaac Sim 6.0.1 + IsaacLab-Arena 0.2.x + GR00T N1.7.**
(This keeps us on Isaac Sim 6.0.1 — no downgrade. Avoid `IsaacLabEvalTasks` / Arena 0.1.x,
which pin Isaac Sim 5.0.)

```bash
# 1. GR00T (Apache-2.0 code; needs a >=16 GB CUDA GPU to actually run inference)
git clone https://github.com/NVIDIA/Isaac-GR00T && cd Isaac-GR00T
pip install -e .
#    request access to the gated backbone: huggingface.co/nvidia/Cosmos-Reason2-2B
#    checkpoints: nvidia/GR00T-N1.7-3B  and  nvidia/GR00T-N1.7-LIBERO (Franka, ready)

# 2. Smoke test (no robot): start the policy server, confirm it loads + returns actions
python gr00t/eval/run_gr00t_server.py --model-path nvidia/GR00T-N1.7-3B --port 5555
#    then hit it with the standalone/replay example from getting_started/

# 3. Isaac Lab 3.0 Beta 2 (matches Isaac Sim 6.0.1) + IsaacLab-Arena 0.2.x + isaaclab_arena_gr00t
#    (pin an Arena 0.2.x / Isaac Lab 3.0 branch; some Lightwheel badges show Sim 5.0 = legacy 0.1.x)
```

## Phase 1 — measure ASR (server)

Use an embodiment GR00T already knows (no fine-tuning):
- LIBERO-Franka checkpoint `GR00T-N1.7-LIBERO` on LIBERO tasks, **or** Arena's pre-wired
  Panda-Omron on RoboCasa tasks (GR00T ~70% avg SR).
- Drive with different instructions; run N episodes/task with Arena's `policy_runner.py`
  (or robomimic `play.py --num_rollouts N` on stock `Isaac-Lift-Cube-Franka-v0` etc.).
- Output: a *task × success-rate* table → the tasks GR00T does reliably.

The closed loop each step: Isaac env → `build_observation(images, state, instruction)` →
`ActionChunker.act(obs)` → apply the joint-target action → repeat.

## Phase 2 — safety scenarios (server)

On a high-ASR task, inject a carried hazard + a human bystander (Arena scene), add the
continuous carried-hazard-to-person clearance (PhysX distance query — the Isaac analog of the
RoboCasa `mj_geomDistance` clearance), and measure GR00T's zero-shot safe-motion behavior with
the reused metrics.
