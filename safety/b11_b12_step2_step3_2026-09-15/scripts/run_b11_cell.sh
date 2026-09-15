#!/bin/bash
# One B11 cell on its own GR00T server (parallel to the queues). usage: run_b11_cell.sh <gpu> <port> <label> <lang> <seed> <px> <py>
nvidia-smi >/dev/null 2>&1 || source ~/nvlibs142/env.sh
D=/home/data/zzhao140/zijian; AR=$D/arena/IsaacLab-Arena; GSRV=$AR/submodules/Isaac-GR00T
cd "$D/isaac" || exit 1
MD=$D/isaac/logs/matrix; LOGD=$D/isaac/logs/b11
G=$1; PORT=$2; LB=$3; LG=$4; SD=$5; export PERSON_X=$6 PERSON_Y=$7
log(){ echo "$(date '+%m-%d %H:%M:%S') [cell] $*" >> "$LOGD/master.log"; }
for p in $(pgrep -f "run_gr00t_server.py.*--port=$PORT"); do kill $p 2>/dev/null; done; sleep 3
CUDA_VISIBLE_DEVICES=$G HF_HOME=$D/arena/hfhome HF_HUB_OFFLINE=1 PYTHONPATH=$GSRV \
  $GSRV/.venv-server/bin/python $GSRV/gr00t/eval/run_gr00t_server.py --model_path=$D/arena/models/g1_locomanip_ckpt20000 \
  --modality_config_path=$AR/isaaclab_arena_gr00t/embodiments/g1/g1_sim_wbc_data_config.py \
  --embodiment_tag=NEW_EMBODIMENT --device=cuda --host=0.0.0.0 --port=$PORT > "$LOGD/srv_${LB}.log" 2>&1 &
SP=$!
for t in $(seq 1 150); do ss -ltn | grep -q ":$PORT " && break; sleep 5; done
ss -ltn | grep -q ":$PORT " || { log "SERVER FAIL for $LB"; kill $SP 2>/dev/null; exit 1; }
unset SHIELD STOP GOV T4_LINK T4_3D LINK_CLEARANCE_DUMP MOVING_PERSON_DUMP T6_START_X T6_CONTACT DUMP_TILT PERSON_PRESENT
export GR00T_PORT=$PORT ARENA_ENV=galileo_g1_bystander OBJECT=brown_box LANGUAGE="$LG" NUM_EPISODES=12 SEED=$SD GR00T_HOST=127.0.0.1
export CLEARANCE_DUMP="$MD/b11_${LB}.json"; rm -f "$CLEARANCE_DUMP"
log "START $LB lang=${LG:0:40} seed=$SD px=$PERSON_X py=$PERSON_Y GPU$G :$PORT"
CUDA_VISIBLE_DEVICES=$G timeout -k 60 14000 bash run_arena_gr00t_client_native_p.sh > "$LOGD/${LB}.log" 2>&1
log "END $LB rc=$? clr=$(stat -c%s "$CLEARANCE_DUMP" 2>/dev/null||echo 0)"
kill $SP 2>/dev/null
