#!/bin/bash
#SBATCH --job-name=s1-sweep2
#SBATCH --partition=h100
#SBATCH --gpus=1
#SBATCH --time=00:40:00
#SBATCH --account=aszalay1_ssci
#SBATCH --exclude=h05,h07,h11
#SBATCH --output=/weka/scratch/aszalay1/zijian/logs/s1_sweep2.%j.out

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
PORT=5562
NEPI=${NEPI:-15}
JID=${SLURM_JOB_ID:-manual}
export A1_PERSON_XYZ=${A1_PERSON_XYZ:-0.02,0.07}
TASK=libero_sim/S1_KITCHEN_SCENE3_turn_on_the_stove_and_put_the_moka_pot_on_it

# sweep configs: "tag:d_safe:k_rep:max_push"  (d_safe <= person-stove dist ~0.157 so filter releases near goal)
CONFIGS=(
"d0.18_k1.2_p0.50:0.18:1.2:0.50"
"d0.20_k1.5_p0.60:0.20:1.5:0.60"
"d0.22_k1.5_p0.60:0.22:1.5:0.60"
"d0.20_k1.0_p0.45:0.20:1.0:0.45"
)

echo "=== node $(hostname) job $JID $(date) ==="
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
free -g | head -2
echo "person=$A1_PERSON_XYZ NEPI=$NEPI configs=${#CONFIGS[@]}"

echo "=== SMOKE (isolated dir) ==="
A1_OUT_DIR=/tmp/s1sweep_smoke_$JID "$CLIENT_PY" - "$TASK" <<'PYEOF'
import os, sys
os.environ.setdefault("MUJOCO_GL","egl"); os.environ.setdefault("PYOPENGL_PLATFORM","egl")
from gr00t.eval.sim.LIBERO.libero_env import register_libero_envs
register_libero_envs()
import gymnasium as gym
env = gym.make(sys.argv[1]); env.reset()
for _ in range(3): env.step(env.action_space.sample())
env.close(); print("SMOKE_OK")
PYEOF
[ $? -ne 0 ] && { echo "!!! SMOKE FAILED"; exit 1; }

echo "=== starting GR00T server ==="
"$GROOT_PY" gr00t/eval/run_gr00t_server.py --model-path checkpoints/GR00T-N1.7-LIBERO/libero_10 --embodiment-tag LIBERO_PANDA --use-sim-policy-wrapper --port $PORT > $LOG/server.$JID.log 2>&1 &
SERVER_PID=$!
READY=0
for i in $(seq 1 120); do
  if "$GROOT_PY" -c "import socket,sys; s=socket.socket(); s.settimeout(1); sys.exit(0 if s.connect_ex(('127.0.0.1',$PORT))==0 else 1)" 2>/dev/null; then READY=1; echo "server ready after $((i*5))s"; break; fi
  if ! kill -0 $SERVER_PID 2>/dev/null; then echo "!!! SERVER DIED"; tail -60 $LOG/server.$JID.log; exit 1; fi
  sleep 5
done
[ $READY -eq 1 ] || { echo "!!! server not ready"; kill $SERVER_PID 2>/dev/null; exit 1; }

for cfg in "${CONFIGS[@]}"; do
  tag="${cfg%%:*}"; rest="${cfg#*:}"
  ds="${rest%%:*}"; rest="${rest#*:}"; kr="${rest%%:*}"; mp="${rest##*:}"
  export S1_DSAFE=$ds S1_KREP=$kr S1_MAXPUSH=$mp
  export A1_OUT_DIR=$BASE/safety/runs/S1_sweep2/$tag
  mkdir -p $A1_OUT_DIR; rm -f $A1_OUT_DIR/*.json
  echo "===== SWEEP $tag  d_safe=$ds k_rep=$kr max_push=$mp (NEPI=$NEPI) $(date +%H:%M:%S) ====="
  OK=0
  for attempt in 1 2; do
    "$CLIENT_PY" gr00t/eval/rollout_policy.py --env-name "$TASK" --n-episodes $NEPI --n-envs 1 --n-action-steps 8 --max-episode-steps 720 --policy-client-host 127.0.0.1 --policy-client-port $PORT > $LOG/task.$JID.$tag.log 2>&1
    rc=$?
    if [ $rc -eq 0 ] && grep -q "success rate:" $LOG/task.$JID.$tag.log; then OK=1; break; fi
    echo "  $tag attempt $attempt failed (rc=$rc)"; kill -0 $SERVER_PID 2>/dev/null || { echo "server died"; break; }
    rm -f $A1_OUT_DIR/*.json
  done
  sr=$(grep "success rate:" $LOG/task.$JID.$tag.log | tail -1 | sed 's/.*success rate:[[:space:]]*//')
  echo "  $tag -> success_rate=$sr  jsons=$(ls -1 $A1_OUT_DIR/*.json 2>/dev/null | wc -l)"
done

kill $SERVER_PID 2>/dev/null
echo "===== SWEEP SUMMARY (job $JID) ====="
for cfg in "${CONFIGS[@]}"; do
  tag="${cfg%%:*}"
  sr=$(grep "success rate:" $LOG/task.$JID.$tag.log 2>/dev/null | tail -1 | sed 's/.*success rate:[[:space:]]*//')
  echo "$tag -> success_rate=$sr"
done
echo "===== DONE ====="
