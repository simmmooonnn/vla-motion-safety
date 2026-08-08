#!/bin/bash
#SBATCH --job-name=s1-kitchen3
#SBATCH --partition=h100
#SBATCH --gpus=1
#SBATCH --time=00:40:00
#SBATCH --account=aszalay1_ssci
#SBATCH --output=/weka/scratch/aszalay1/zijian/logs/s1_kitchen3.%j.out

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
PORT=5557
NEPI=${NEPI:-20}
JID=${SLURM_JOB_ID:-manual}

# person the safety filter actively avoids (same as the A1 headline bystander)
export A1_PERSON_XYZ=${A1_PERSON_XYZ:--0.05,0.12}
# reactive-filter gains (tunable)
export S1_DSAFE=${S1_DSAFE:-0.30}
export S1_KREP=${S1_KREP:-2.0}
export S1_MAXPUSH=${S1_MAXPUSH:-0.8}
# NOTE: do NOT export A1_TASK_TAG -> env uses its own task_tag "S1"
export A1_OUT_DIR=$BASE/safety/runs/S1_kitchen3
mkdir -p $A1_OUT_DIR

TASK=libero_sim/S1_KITCHEN_SCENE3_turn_on_the_stove_and_put_the_moka_pot_on_it

echo "=== node $(hostname) job $JID $(date) ==="
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
echo "A1_OUT_DIR=$A1_OUT_DIR NEPI=$NEPI person=$A1_PERSON_XYZ d_safe=$S1_DSAFE k_rep=$S1_KREP max_push=$S1_MAXPUSH"

echo "=== SMOKE: build S1 (filter+probe) env on GPU before model load ==="
A1_OUT_DIR=/tmp/s1_smoke_$JID "$CLIENT_PY" - "$TASK" <<'PYEOF'
import os, sys
os.environ.setdefault("MUJOCO_GL", "egl"); os.environ.setdefault("PYOPENGL_PLATFORM", "egl")
from gr00t.eval.sim.LIBERO.libero_env import register_libero_envs
register_libero_envs()
import gymnasium as gym
env = gym.make(sys.argv[1])
obs, _ = env.reset()
for _ in range(3):
    env.step(env.action_space.sample())
env.close()
print("SMOKE_OK")
PYEOF
if [ $? -ne 0 ]; then echo "!!! SMOKE FAILED (S1 env broke); aborting before model load"; exit 1; fi

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

short=$(echo "$TASK" | sed 's#.*/##')
OK=0
for attempt in 1 2 3; do
  echo "===== S1 RUN $short attempt $attempt (NEPI=$NEPI) $(date +%H:%M:%S) ====="
  rm -f $A1_OUT_DIR/*.json   # avoid mixing partial data from a crashed attempt
  "$CLIENT_PY" gr00t/eval/rollout_policy.py --env-name "$TASK" --n-episodes $NEPI --n-envs 1 --n-action-steps 8 --max-episode-steps 720 --policy-client-host 127.0.0.1 --policy-client-port $PORT > $LOG/task.$JID.$short.log 2>&1
  rc=$?
  grep -E "success rate:|S1-filter" $LOG/task.$JID.$short.log | tail -3
  if [ $rc -eq 0 ] && grep -q "success rate:" $LOG/task.$JID.$short.log; then OK=1; break; fi
  echo "  attempt $attempt FAILED (rc=$rc); tail:"; tail -8 $LOG/task.$JID.$short.log
  if ! kill -0 $SERVER_PID 2>/dev/null; then echo "!!! server died; aborting retries"; break; fi
done
[ $OK -eq 1 ] || echo "!!! all S1 rollout attempts failed"

kill $SERVER_PID 2>/dev/null
echo "===== S1 SUMMARY (job $JID) ====="
sr=$(grep "success rate:" $LOG/task.$JID.$short.log | tail -1 | sed 's/.*success rate:[[:space:]]*//')
echo "$short  ->  success_rate=$sr"
echo -n "trajectory files: "; ls -1 $A1_OUT_DIR/*.json 2>/dev/null | wc -l
echo "===== DONE ====="
