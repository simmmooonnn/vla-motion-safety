#!/bin/bash
source ~/nvlibs142/env.sh
D=/home/data/zzhao140/zijian; AR=$D/arena/IsaacLab-Arena; GSRV=$AR/submodules/Isaac-GR00T
cd "$D/isaac" || exit 1
MD=$D/isaac/logs/matrix; LOGD=$D/isaac/logs/b8; rm -f "$LOGD/B8E_DONE"
G=${GPU:-0}; PORT=5556; SP=""
log(){ echo "$(date '+%m-%d %H:%M:%S') $*" >> "$LOGD/master.log"; }
until [ -f "$LOGD/B8C_DONE" ]; do sleep 120; done
sleep 20; log "B8E: seed-7 top-ups of the 2x2 arms"
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
runcell(){ local LB="$1" LG="$2" NE="$3" SD="$4" PRES="$5"; export GR00T_PORT=$PORT
  start_server "$LB" || return 1
  export ARENA_ENV=galileo_g1_fire OBJECT=brown_box LANGUAGE="$LG" NUM_EPISODES=$NE SEED=$SD GR00T_HOST=127.0.0.1 PERSON_X=0.28 PERSON_Y=-0.7 PERSON_PRESENT=$PRES
  export CLEARANCE_DUMP="$MD/b8_${LB}.json"; rm -f "$CLEARANCE_DUMP"
  log "START $LB env=galileo_g1_fire lang=$LG N=$NE seed=$SD px=0.28 present=$PRES gpu=$G"
  CUDA_VISIBLE_DEVICES=$G timeout -k 60 24000 bash run_arena_gr00t_client_native_p.sh > "$LOGD/${LB}.log" 2>&1
  log "END $LB rc=$? clr=$(stat -c%s "$CLEARANCE_DUMP" 2>/dev/null||echo 0)"
  kill $SP 2>/dev/null; sleep 3
}
runcell b2x_named_rend_s7 cup_stove 24 7 1
runcell b2x_blind_hid_s7  cup       24 7 0
runcell b2x_named_hid_s7  cup_stove 24 7 0
touch "$LOGD/B8E_DONE"; log "=== B8E_DONE ==="
