#!/bin/bash
#SBATCH --job-name=d1-kitchen3
#SBATCH --partition=h100
#SBATCH --gpus=1
#SBATCH --time=00:50:00
#SBATCH --account=aszalay1_ssci
#SBATCH --output=/weka/scratch/aszalay1/zijian/logs/d1_kitchen3.%j.out

set -uo pipefail
BASE=/weka/scratch/aszalay1/zijian
ROOT=$BASE/code/Isaac-GR00T
LOG=$BASE/logs
source $BASE/env.sh 2>/dev/null
module load GCC/13.2.0
export PYTHONFAULTHANDLER=1
export GR00T_NO_VIDEO=1
export MUJOCO_GL=egl PYOPENGL_PLATFORM=egl
cd $ROOT
GROOT_PY=$BASE/envs/groot/bin/python
CLIENT_PY=$ROOT/gr00t/eval/sim/LIBERO/libero_uv/.venv/bin/python
PORT=5556
NEPI=${NEPI:-20}
JID=${SLURM_JOB_ID:-manual}

# NOTE: deliberately do NOT export A1_TASK_TAG -> each env uses its own task_tag
# (D1_neutral / D1_caution / D1_danger) so per-condition jsons stay separate.
export A1_OUT_DIR=$BASE/safety/runs/D1_kitchen3
mkdir -p $A1_OUT_DIR

TASKS=(
libero_sim/D1_neutral_KITCHEN_SCENE3_turn_on_the_stove_and_put_the_moka_pot_on_it
libero_sim/D1_caution_KITCHEN_SCENE3_turn_on_the_stove_and_put_the_moka_pot_on_it
libero_sim/D1_danger_KITCHEN_SCENE3_turn_on_the_stove_and_put_the_moka_pot_on_it
)

echo "=== node $(hostname) job $JID $(date) ==="
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
echo "A1_OUT_DIR=$A1_OUT_DIR  NEPI=$NEPI  conditions=${#TASKS[@]}"

echo "=== SMOKE: build one D1 probe env on GPU (fail fast before model load) ==="
A1_OUT_DIR=/tmp/d1_smoke_$JID "$CLIENT_PY" - "${TASKS[0]}" <<'PYEOF'
import os, sys
os.environ.setdefault("MUJOCO_GL", "egl"); os.environ.setdefault("PYOPENGL_PLATFORM", "egl")
from gr00t.eval.sim.LIBERO.libero_env import register_libero_envs
register_libero_envs()
import gymnasium as gym
env = gym.make(sys.argv[1])
obs, _ = env.reset()
print("instruction seen by policy:", repr(obs["annotation.human.action.task_description"])[:160])
for _ in range(3):
    env.step(env.action_space.sample())
env.close()
print("SMOKE_OK")
PYEOF
if [ $? -ne 0 ]; then echo "!!! SMOKE FAILED (D1 probe env broke); aborting before model load"; exit 1; fi

echo "=== starting GR00T server ==="
"$GROOT_PY" gr00t/eval/run_gr00t_server.py --model-path checkpoints/GR00T-N1.7-LIBERO/libero_10 --embodiment-tag LIBERO_PANDA --use-sim-policy-wrapper --port $PORT > $LOG/server.$JID.log 2>&1 &
SERVER_PID=$!
echo "=== waiting for server on port $PORT ==="
READY=0
for i in $(seq 1 120); do
  if "$GROOT_PY" -c "import socket,sys; s=socket.socket(); s.settimeout(1); sys.exit(0 if s.connect_ex(('127.0.0.1',$PORT))==0 else 1)" 2>/dev/null; then
    READY=1; echo "server ready after $((i*5))s"; break
  fi
  if ! kill -0 $SERVER_PID 2>/dev/null; then echo "!!! SERVER DIED"; tail -80 $LOG/server.$JID.log; exit 1; fi
  sleep 5
done
[ $READY -eq 1 ] || { echo "!!! server not ready in 600s"; tail -80 $LOG/server.$JID.log; kill $SERVER_PID 2>/dev/null; exit 1; }

for T in "${TASKS[@]}"; do
  short=$(echo "$T" | sed 's#.*/##')
  echo "===== D1 RUN $short (NEPI=$NEPI) $(date +%H:%M:%S) ====="
  "$CLIENT_PY" gr00t/eval/rollout_policy.py --env-name "$T" --n-episodes $NEPI --n-envs 1 --n-action-steps 8 --max-episode-steps 720 --policy-client-host 127.0.0.1 --policy-client-port $PORT 2>&1 | tee $LOG/task.$JID.$short.log | grep -E "success rate:|Running collecting|instruction seen|Error|Traceback|Exception"
done

kill $SERVER_PID 2>/dev/null
echo "===== D1 SUMMARY (job $JID) ====="
for f in $LOG/task.$JID.*.log; do
  [ -e "$f" ] || continue
  sr=$(grep "success rate:" "$f" | tail -1 | sed 's/.*success rate:[[:space:]]*//')
  echo "$(basename "$f" | sed 's/^task\.[0-9]*\.//; s/\.log$//')  ->  success_rate=$sr"
done
echo -n "trajectory files: "; ls -1 $A1_OUT_DIR/*.json 2>/dev/null | wc -l
echo "===== DONE ====="
