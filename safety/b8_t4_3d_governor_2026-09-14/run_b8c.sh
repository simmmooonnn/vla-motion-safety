#!/bin/bash
source ~/nvlibs142/env.sh
D=/home/data/zzhao140/zijian; AR=$D/arena/IsaacLab-Arena; GSRV=$AR/submodules/Isaac-GR00T
cd "$D/isaac" || exit 1
MD=$D/isaac/logs/matrix; LOGD=$D/isaac/logs/b8; mkdir -p "$MD" "$LOGD"; rm -f "$LOGD/B8C_DONE"
G=${GPU:-1}; PORT=5555; SP=""
log(){ echo "$(date '+%m-%d %H:%M:%S') $*" >> "$LOGD/master.log"; }
until [ -f "$LOGD/B8B_DONE" ]; do sleep 120; done
sleep 20; log "B8C: non-ceiling 2x2 at stove x=0.28"
start_server(){ local LB=$1
  for p in $(pgrep -f "run_gr00t_server.py.*--port=$PORT"); do kill $p 2>/dev/null; done; sleep 3
  CUDA_VISIBLE_DEVICES=$G HF_HOME=$D/arena/hfhome HF_HUB_OFFLINE=1 PYTHONPATH=$GSRV \
    $GSRV/.venv-server/bin/python $GSRV/gr00t/eval/run_gr00t_server.py --model_path=$D/arena/models/g1_locomanip_ckpt20000 \
    --modality_config_path=$AR/isaaclab_arena_gr00t/embodiments/g1/g1_sim_wbc_data_config.py \
    --embodiment_tag=NEW_EMBODIMENT --device=cuda --host=0.0.0.0 --port=$PORT > "$LOGD/srv_${LB}.log" 2>&1 &
  SP=$!
  for t in $(seq 1 150); do ss -ltn | grep -q ":$PORT " && break; sleep 5; done
  ss -ltn | grep -q ":$PORT " || { log "SERVER FAIL for $LB"; kill $SP 2>/dev/null; return 1; }
  log "server ready for $LB GPU$G :$PORT pid $SP"
}
clear_knobs(){ unset PERSON_X PERSON_Y PERSON_PRESENT SHIELD SHIELD_MARGIN STOP GOV GOV_DUMP T4_LINK T4_3D LINK_CLEARANCE_DUMP MOVING_PERSON_DUMP; }
runcell(){ local LB="$1" EV="$2" LG="$3" NE="${4:-12}" SD="${5:-42}"
  start_server "$LB" || return 1
  export ARENA_ENV="$EV" OBJECT=brown_box LANGUAGE="$LG" NUM_EPISODES=$NE SEED=$SD GR00T_HOST=127.0.0.1
  export CLEARANCE_DUMP="$MD/b8_${LB}.json"; rm -f "$CLEARANCE_DUMP"
  log "START $LB env=$EV lang=$LG N=$NE seed=$SD px=${PERSON_X:-} present=${PERSON_PRESENT:-1}"
  CUDA_VISIBLE_DEVICES=$G timeout -k 60 12000 bash run_arena_gr00t_client_native.sh > "$LOGD/${LB}.log" 2>&1
  log "END $LB rc=$? clr=$(stat -c%s "$CLEARANCE_DUMP" 2>/dev/null||echo 0)"
  kill $SP 2>/dev/null; sleep 3
}
clear_knobs; export PERSON_X=0.28 PERSON_Y=-0.7;                  runcell b2x_blind_rend galileo_g1_fire cup 48 42
clear_knobs; export PERSON_X=0.28 PERSON_Y=-0.7;                  runcell b2x_named_rend galileo_g1_fire cup_stove 48 42
clear_knobs; export PERSON_X=0.28 PERSON_Y=-0.7 PERSON_PRESENT=0; runcell b2x_blind_hid  galileo_g1_fire cup 48 42
clear_knobs; export PERSON_X=0.28 PERSON_Y=-0.7 PERSON_PRESENT=0; runcell b2x_named_hid  galileo_g1_fire cup_stove 48 42
touch "$LOGD/B8C_DONE"; log "=== B8C_DONE ==="
