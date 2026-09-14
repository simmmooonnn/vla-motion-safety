#!/bin/bash
source ~/nvlibs142/env.sh
D=/home/data/zzhao140/zijian; AR=$D/arena/IsaacLab-Arena; GSRV=$AR/submodules/Isaac-GR00T
cd "$D/isaac" || exit 1
MD=$D/isaac/logs/matrix; LOGD=$D/isaac/logs/b9; rm -f "$LOGD/B9B_DONE"
G=${GPU:-0}; PORT=5556; SP=""
log(){ echo "$(date '+%m-%d %H:%M:%S') $*" >> "$LOGD/master.log"; }
until [ -f "$LOGD/B9_DONE" ]; do sleep 120; done
sleep 20; log "B9B: contact cells with base logging, seed 7"
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
clear_knobs(){ unset T6_NO_COLLIDER STOP STOP_MARGIN STOP_HYST STOP_REF STOP_DUMP GOV SHIELD SHIELD_MARGIN MOVING_PERSON_DUMP; }
runcell(){ local LB="$1" NE="$2" SD="$3"; export GR00T_PORT=$PORT
  start_server "$LB" || return 1
  export ARENA_ENV=galileo_g1_moving OBJECT=brown_box LANGUAGE=benign NUM_EPISODES=$NE SEED=$SD GR00T_HOST=127.0.0.1
  export T6_START_X=-0.82 T6_START_Y=-0.95 T6_VEL_X=0.06 T6_VEL_Y=0.0 T6_CONTACT=1
  export CLEARANCE_DUMP="$MD/b9_${LB}.json" MOVING_PERSON_DUMP="$MD/b9_${LB}_moving.json"; rm -f "$CLEARANCE_DUMP" "$MOVING_PERSON_DUMP"
  if [ "${STOP:-0}" = 1 ]; then export STOP_DUMP="$MD/b9_${LB}_stop.jsonl"; rm -f "$STOP_DUMP"; fi
  log "START $LB env=galileo_g1_moving N=$NE seed=$SD contact=1 stop=${STOP:-0}/${STOP_MARGIN:-}"
  CUDA_VISIBLE_DEVICES=$G timeout -k 60 12000 bash run_arena_gr00t_client_native_p.sh > "$LOGD/${LB}.log" 2>&1
  log "END $LB rc=$? mov=$(stat -c%s "$MOVING_PERSON_DUMP" 2>/dev/null||echo 0)"
  kill $SP 2>/dev/null; sleep 3
}
clear_knobs; runcell t6_contact_s7 12 7
clear_knobs; export STOP=1 STOP_MARGIN=0.50 STOP_HYST=0.10 STOP_REF=min; runcell t6_stop050_contact_s7 12 7
touch "$LOGD/B9B_DONE"; log "=== B9B_DONE ==="
