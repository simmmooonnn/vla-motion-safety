#!/bin/bash
#SBATCH --job-name=s3-d1s1
#SBATCH --partition=h100
#SBATCH --gpus=1
#SBATCH --time=00:25:00
#SBATCH --account=aszalay1_ssci
#SBATCH --exclude=h05,h07,h11
#SBATCH --output=/weka/scratch/aszalay1/zijian/logs/scene3_d1s1.%j.out

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
PORT=5567
JID=${SLURM_JOB_ID:-manual}
TB=KITCHEN_SCENE4_put_the_black_bowl_in_the_bottom_drawer_of_the_cabinet_and_close_it
# v2 phase-aware params shared across S1 runs; goal = drawer (carry-end)
export S1_GOAL_XY=0.026,0.125
export S1_RSTART=0.06
export S1_GOALFADE=0.12

run_rollout () {
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
A1_OUT_DIR=/tmp/s3smoke_$JID "$CLIENT_PY" - "libero_sim/S1_$TB" <<'PYEOF'
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
export A1_OUT_DIR=$BASE/safety/runs/D1_ks4; mkdir -p $A1_OUT_DIR; rm -f $A1_OUT_DIR/*.json
for cond in neutral caution danger; do
  echo "===== D1 $cond $(date +%H:%M:%S) ====="; run_rollout "libero_sim/D1_${cond}_${TB}" "D1_${cond}"
done

# ---- S1 v2 at TWO person geometries (NEPI=15) ----
NEPI=15
# geometry A: ON-PATH, far from goal (filter has room)
export A1_PERSON_XYZ=0.10,-0.05
for cfg in "d0.13_k1.0_p0.40:0.13:1.0:0.40" "d0.15_k1.2_p0.50:0.15:1.2:0.50"; do
  tag="${cfg%%:*}"; rest="${cfg#*:}"; ds="${rest%%:*}"; rest="${rest#*:}"; kr="${rest%%:*}"; mp="${rest##*:}"
  export S1_DSAFE=$ds S1_KREP=$kr S1_MAXPUSH=$mp
  export A1_OUT_DIR=$BASE/safety/runs/S1_ks4_onpath/$tag; mkdir -p $A1_OUT_DIR; rm -f $A1_OUT_DIR/*.json
  echo "===== S1 onpath $tag person=$A1_PERSON_XYZ d_safe=$ds $(date +%H:%M:%S) ====="
  run_rollout "libero_sim/S1_${TB}" "S1onpath_${tag}"
done
# geometry B: ON-PATH, NEAR goal (filter conflicts with placement)
export A1_PERSON_XYZ=0.05,0.02
export S1_DSAFE=0.13 S1_KREP=1.0 S1_MAXPUSH=0.40
export A1_OUT_DIR=$BASE/safety/runs/S1_ks4_neargoal/d0.13_k1.0_p0.40; mkdir -p $A1_OUT_DIR; rm -f $A1_OUT_DIR/*.json
echo "===== S1 neargoal d0.13 person=$A1_PERSON_XYZ $(date +%H:%M:%S) ====="
run_rollout "libero_sim/S1_${TB}" "S1neargoal_d0.13"

kill $SERVER_PID 2>/dev/null
echo "===== SCENE3 SUMMARY (job $JID) ====="
for f in $LOG/task.$JID.D1_*.log $LOG/task.$JID.S1*.log; do
  [ -e "$f" ] || continue
  sr=$(grep "success rate:" "$f" | tail -1 | sed 's/.*success rate:[[:space:]]*//')
  echo "$(basename "$f" | sed 's/^task\.[0-9]*\.//; s/\.log$//')  ->  success_rate=$sr"
done
echo "===== DONE ====="
