#!/bin/bash
# usage: run_gr00t_droid_server.sh <gpu> <port>   GR00T N1.6-DROID (nvidia/GR00T-N1.6-DROID, OXE_DROID tag), offline from the HF cache
G=${1:-1}; PORT=${2:-5557}
D=/home/data/zzhao140/zijian; GSRV=$D/arena/IsaacLab-Arena/submodules/Isaac-GR00T
mkdir -p $D/isaac/logs/fr
for p in $(pgrep -u $(id -u) -f "run_gr00t_server.py.*--port=$PORT"); do kill $p 2>/dev/null; done; sleep 2
cd $GSRV
CUDA_VISIBLE_DEVICES=$G HF_HOME=$D/arena/hfhome HF_HUB_OFFLINE=1 PYTHONPATH=$GSRV \
  nohup setsid $GSRV/.venv-server/bin/python $GSRV/gr00t/eval/run_gr00t_server.py --model_path=nvidia/GR00T-N1.6-DROID \
  --embodiment_tag=OXE_DROID --device=cuda --host=0.0.0.0 --port=$PORT </dev/null > $D/isaac/logs/fr/gr00t_droid_server_$PORT.log 2>&1 &
disown
echo "GR00T-N1.6-DROID server launching on GPU$G :$PORT"
