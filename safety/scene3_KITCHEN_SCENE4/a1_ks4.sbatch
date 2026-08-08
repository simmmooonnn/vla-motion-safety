#!/bin/bash
#SBATCH --job-name=a1-ks4
#SBATCH --partition=h100
#SBATCH --gpus=1
#SBATCH --time=00:15:00
#SBATCH --account=aszalay1_ssci
#SBATCH --exclude=h05,h07,h11
#SBATCH --output=/weka/scratch/aszalay1/zijian/logs/a1_ks4.%j.out

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
PORT=5566
NEPI=${NEPI:-20}
JID=${SLURM_JOB_ID:-manual}
export A1_OUT_DIR=$BASE/safety/runs/A1_ks4
mkdir -p $A1_OUT_DIR
TASK=libero_sim/A1_KITCHEN_SCENE4_put_the_black_bowl_in_the_bottom_drawer_of_the_cabinet_and_close_it

echo "=== node $(hostname) job $JID $(date) ==="; nvidia-smi --query-gpu=name --format=csv,noheader
echo "=== SMOKE (verify bowl hazard discovery) ==="
A1_OUT_DIR=/tmp/a1ks4smoke_$JID "$CLIENT_PY" - "$TASK" <<'PYEOF'
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

short=$(echo "$TASK" | sed 's#.*/##')
OK=0
for attempt in 1 2; do
  echo "===== A1-KS4 RUN attempt $attempt (NEPI=$NEPI) $(date +%H:%M:%S) ====="
  rm -f $A1_OUT_DIR/*.json
  "$CLIENT_PY" gr00t/eval/rollout_policy.py --env-name "$TASK" --n-episodes $NEPI --n-envs 1 --n-action-steps 8 --max-episode-steps 720 --policy-client-host 127.0.0.1 --policy-client-port $PORT > $LOG/task.$JID.$short.log 2>&1
  rc=$?
  grep -E "success rate:|A1-probe\] (nbody|hazard cand|ep000 hazard)" $LOG/task.$JID.$short.log | head -6
  if [ $rc -eq 0 ] && grep -q "success rate:" $LOG/task.$JID.$short.log; then OK=1; break; fi
  echo "  attempt $attempt failed (rc=$rc)"; tail -6 $LOG/task.$JID.$short.log; kill -0 $SERVER_PID 2>/dev/null || break
done
kill $SERVER_PID 2>/dev/null
echo "===== A1-KS4 SUMMARY (job $JID) ====="
sr=$(grep "success rate:" $LOG/task.$JID.$short.log | tail -1 | sed 's/.*success rate:[[:space:]]*//')
echo "$short  ->  success_rate=$sr  jsons=$(ls -1 $A1_OUT_DIR/*.json 2>/dev/null | wc -l)"
echo "===== DONE ====="
