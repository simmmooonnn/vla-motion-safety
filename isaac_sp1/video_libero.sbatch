#!/bin/bash
#SBATCH --job-name=lib-video
#SBATCH --partition=nvl
#SBATCH --gpus=1
#SBATCH --time=00:25:00
#SBATCH --account=aszalay1_ssci
#SBATCH --output=/weka/scratch/aszalay1/zijian/isaac/logs/video.%j.out
set -uo pipefail
BASE=/weka/scratch/aszalay1/zijian
ROOT=$BASE/code/Isaac-GR00T
LOG=$BASE/isaac/logs
source $BASE/env.sh 2>/dev/null
# nvl nodes have no `module` and groot torch sees CUDA without it (verified job 2034283).
export PYTHONFAULTHANDLER=1 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl
# video recording wrapper shells out to `ffmpeg`; supply it from the conda-forge tools env
export PATH=$BASE/isaac/tools/bin:$PATH
cd $ROOT
GROOT_PY=$BASE/envs/groot/bin/python
CLIENT_PY=$ROOT/gr00t/eval/sim/LIBERO/libero_uv/.venv/bin/python
PORT=5591
JID=${SLURM_JOB_ID:-manual}
TASK=KITCHEN_SCENE3_turn_on_the_stove_and_put_the_moka_pot_on_it
VIDDIR=$BASE/safety/ISAAC_SP1/libero_videos
mkdir -p $VIDDIR $LOG

echo "=== node $(hostname) job $JID $(date) ==="
nvidia-smi --query-gpu=name --format=csv,noheader
echo "=== start GR00T server ==="
$GROOT_PY gr00t/eval/run_gr00t_server.py --model-path checkpoints/GR00T-N1.7-LIBERO/libero_10 \
  --embodiment-tag LIBERO_PANDA --use-sim-policy-wrapper --port $PORT > $LOG/server.$JID.log 2>&1 &
SERVER_PID=$!
READY=0
for i in $(seq 1 120); do
  if $GROOT_PY -c "import socket,sys; s=socket.socket(); s.settimeout(1); sys.exit(0 if s.connect_ex(('127.0.0.1',$PORT))==0 else 1)" 2>/dev/null; then
    READY=1; echo "server ready after $((i*5))s"; break; fi
  kill -0 $SERVER_PID 2>/dev/null || { echo "SERVER DIED"; tail -40 $LOG/server.$JID.log; exit 1; }
  sleep 5
done
[ $READY -eq 1 ] || { echo "server not ready"; kill $SERVER_PID 2>/dev/null; exit 1; }

echo "=== rollout WITH video (moka pot, 4 episodes) ==="
$CLIENT_PY gr00t/eval/rollout_policy.py --env-name "libero_sim/$TASK" --n-episodes 4 --n-envs 1 \
  --n-action-steps 8 --max-episode-steps 720 --policy-client-host 127.0.0.1 --policy-client-port $PORT \
  --video-dir $VIDDIR > $LOG/rollout.$JID.log 2>&1
echo "rollout_exit=$?"
grep -iE "success rate|Video saved" $LOG/rollout.$JID.log | tail
kill $SERVER_PID 2>/dev/null
echo "=== videos ==="; ls -la $VIDDIR
echo "=== DONE ==="
