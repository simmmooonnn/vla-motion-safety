#!/bin/bash
#SBATCH --job-name=s2-d1s1
#SBATCH --partition=h100
#SBATCH --gpus=1
#SBATCH --time=00:30:00
#SBATCH --account=aszalay1_ssci
#SBATCH --exclude=h05,h07,h11
#SBATCH --output=/weka/scratch/aszalay1/zijian/logs/scene2_d1s1.%j.out

set -uo pipefail
BASE=/weka/scratch/aszalay1/zijian
ROOT=$BASE/code/Isaac-GR00T
LOG=$BASE/logs
source $BASE/env.sh 2>/dev/null
module load GCC/13.2.0
export PYTHONFAULTHANDLER=1 GR00T_NO_VIDEO=1 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl
cd $ROOT
GROOT_PY=$BASE/envs/groot/bin/python
CLIENT_PY=$ROOT/gr00t/eval/sim/LIBERO/libero_uv/.venv/bin/python
PORT=5564
JID=${SLURM_JOB_ID:-manual}
TB=LIVING_ROOM_SCENE6_put_the_white_mug_on_the_plate_and_put_the_chocolate_pudding_to_the_right_of_the_plate

run_rollout () {  # $1=env-name  $2=logtag
  local T="$1" tag="$2" OK=0 attempt
  for attempt in 1 2; do
    "$CLIENT_PY" gr00t/eval/rollout_policy.py --env-name "$T" --n-episodes $NEPI --n-envs 1 \
      --n-action-steps 8 --max-episode-steps 720 --policy-client-host 127.0.0.1 --policy-client-port $PORT \
      > $LOG/task.$JID.$tag.log 2>&1
    local rc=$?
    if [ $rc -eq 0 ] && grep -q "success rate:" $LOG/task.$JID.$tag.log; then OK=1; break; fi
    echo "  $tag attempt $attempt failed (rc=$rc)"; kill -0 $SERVER_PID 2>/dev/null || break
  done
  local sr=$(grep "success rate:" $LOG/task.$JID.$tag.log | tail -1 | sed 's/.*success rate:[[:space:]]*//')
  echo "  $tag -> success_rate=$sr  jsons=$(ls -1 $A1_OUT_DIR/*.json 2>/dev/null | wc -l)"
}

echo "=== node $(hostname) job $JID $(date) ==="; nvidia-smi --query-gpu=name --format=csv,noheader

echo "=== SMOKE ==="
A1_OUT_DIR=/tmp/s2smoke_$JID "$CLIENT_PY" - "libero_sim/S1_$TB" <<'PYEOF'
import os,sys
os.environ.setdefault("MUJOCO_GL","egl"); os.environ.setdefault("PYOPENGL_PLATFORM","egl")
from gr00t.eval.sim.LIBERO.libero_env import register_libero_envs
register_libero_envs()
import gymnasium as gym
env=gym.make(sys.argv[1]); env.reset()
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
  kill -0 $SERVER_PID 2>/dev/null || { echo "SERVER DIED"; tail -40 $LOG/server.$JID.log; exit 1; }
  sleep 5
done
[ $READY -eq 1 ] || { echo "server not ready"; kill $SERVER_PID 2>/dev/null; exit 1; }

# ---- D1b: 3 language conditions (NEPI=20) ----
NEPI=20
export A1_OUT_DIR=$BASE/safety/runs/D1_lr6; mkdir -p $A1_OUT_DIR; rm -f $A1_OUT_DIR/*.json
for cond in neutral caution danger; do
  echo "===== D1b $cond $(date +%H:%M:%S) ====="
  run_rollout "libero_sim/D1_${cond}_${TB}" "D1_${cond}"
done

# ---- S1b: safety filter sweep at person=(0.0,-0.05) (NEPI=15) ----
NEPI=15
export A1_PERSON_XYZ=0.0,-0.05
S1CONFIGS=("d0.13_k1.0_p0.40:0.13:1.0:0.40" "d0.15_k1.0_p0.45:0.15:1.0:0.45" "d0.15_k1.2_p0.50:0.15:1.2:0.50")
for cfg in "${S1CONFIGS[@]}"; do
  tag="${cfg%%:*}"; rest="${cfg#*:}"; ds="${rest%%:*}"; rest="${rest#*:}"; kr="${rest%%:*}"; mp="${rest##*:}"
  export S1_DSAFE=$ds S1_KREP=$kr S1_MAXPUSH=$mp
  export A1_OUT_DIR=$BASE/safety/runs/S1_lr6_sweep/$tag; mkdir -p $A1_OUT_DIR; rm -f $A1_OUT_DIR/*.json
  echo "===== S1b $tag d_safe=$ds k_rep=$kr max_push=$mp person=$A1_PERSON_XYZ $(date +%H:%M:%S) ====="
  run_rollout "libero_sim/S1_${TB}" "S1_${tag}"
done

kill $SERVER_PID 2>/dev/null
echo "===== SCENE2 SUMMARY (job $JID) ====="
for f in $LOG/task.$JID.D1_*.log $LOG/task.$JID.S1_*.log; do
  [ -e "$f" ] || continue
  sr=$(grep "success rate:" "$f" | tail -1 | sed 's/.*success rate:[[:space:]]*//')
  echo "$(basename "$f" | sed 's/^task\.[0-9]*\.//; s/\.log$//')  ->  success_rate=$sr"
done
echo "===== DONE ====="
