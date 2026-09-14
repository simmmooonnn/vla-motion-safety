#!/bin/bash
source ~/nvlibs142/env.sh
D=/home/data/zzhao140/zijian; AR=$D/arena/IsaacLab-Arena; GSRV=$AR/submodules/Isaac-GR00T
cd "$D/isaac" || exit 1
MD=$D/isaac/logs/matrix; LOGD=$D/isaac/logs/b9; mkdir -p "$MD" "$LOGD"; rm -f "$LOGD/B9_DONE"; : > "$LOGD/master.log"
G=${GPU:-0}; PORT=5556; SP=""
log(){ echo "$(date '+%m-%d %H:%M:%S') $*" >> "$LOGD/master.log"; }
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
clear_knobs(){ unset PERSON_X PERSON_Y PERSON_PRESENT T6_START_X T6_START_Y T6_VEL_X T6_VEL_Y T6_TRIGGER_Y T6_STOP_DIST T6_NO_COLLIDER T6_CONTACT SHIELD SHIELD_TRACK SHIELD_MARGIN SHIELD_GAIN SHIELD_VMAX STOP STOP_MARGIN STOP_HYST STOP_REF STOP_DUMP GOV GOV_VH GOV_TR GOV_TS GOV_C GOV_Z GOV_REF GOV_SPEED GOV_MARGIN GOV_DUMP MOVING_PERSON_DUMP T4_LINK T4_3D LINK_CLEARANCE_DUMP; }
runcell(){ local LB="$1" EV="$2" LG="$3" NE="${4:-12}" SD="${5:-42}"; export GR00T_PORT=$PORT
  start_server "$LB" || return 1
  export ARENA_ENV="$EV" OBJECT=brown_box LANGUAGE="$LG" NUM_EPISODES=$NE SEED=$SD GR00T_HOST=127.0.0.1
  export CLEARANCE_DUMP="$MD/b9_${LB}.json"; rm -f "$CLEARANCE_DUMP"
  if [ "$EV" = galileo_g1_moving ]; then export MOVING_PERSON_DUMP="$MD/b9_${LB}_moving.json"; rm -f "$MOVING_PERSON_DUMP"; fi
  if [ "${STOP:-0}" = 1 ]; then export STOP_DUMP="$MD/b9_${LB}_stop.jsonl"; rm -f "$STOP_DUMP"; fi
  if [ "${GOV:-0}" = 1 ]; then export GOV_DUMP="$MD/b9_${LB}_gov.jsonl"; rm -f "$GOV_DUMP"; fi
  log "START $LB env=$EV lang=$LG N=$NE seed=$SD contact=${T6_CONTACT:-0} stop=${STOP:-0}/${STOP_MARGIN:-} gov=${GOV:-0}/${GOV_SPEED:-}/${GOV_MARGIN:-} shield=${SHIELD:-0}/${SHIELD_MARGIN:-}"
  CUDA_VISIBLE_DEVICES=$G timeout -k 60 12000 bash run_arena_gr00t_client_native_p.sh > "$LOGD/${LB}.log" 2>&1
  log "END $LB rc=$? clr=$(stat -c%s "$CLEARANCE_DUMP" 2>/dev/null||echo 0) mov=$(stat -c%s "${MOVING_PERSON_DUMP:-/none}" 2>/dev/null||echo 0)"
  kill $SP 2>/dev/null; sleep 3
}
LATER="T6_START_X=-0.82 T6_START_Y=-0.95 T6_VEL_X=0.06 T6_VEL_Y=0.0"
clear_knobs; export $LATER T6_CONTACT=1; runcell t6_contact_smoke galileo_g1_moving benign 2 42
clear_knobs; export $LATER T6_CONTACT=1; runcell t6_contact galileo_g1_moving benign 12 42
clear_knobs; export $LATER T6_CONTACT=1 STOP=1 STOP_MARGIN=0.50 STOP_HYST=0.10 STOP_REF=min; runcell t6_stop050_contact galileo_g1_moving benign 12 42
GOVS="GOV=1 GOV_VH=0 GOV_TR=0.10 GOV_TS=0.30 GOV_C=0.20 GOV_Z=0.10 GOV_REF=min GOV_SPEED=max GOV_MARGIN=0.05"
clear_knobs; export $GOVS SHIELD=1 SHIELD_MARGIN=0.60 SHIELD_GAIN=2.0 SHIELD_VMAX=0.4; runcell t3a_gov_shield_strict galileo_g1_bystander cup 12 42
clear_knobs; export $GOVS SHIELD=1 SHIELD_MARGIN=0.70 SHIELD_GAIN=2.0 SHIELD_VMAX=0.4; runcell t3a_gov_shield070 galileo_g1_bystander cup 12 42
touch "$LOGD/B9_DONE"; log "=== B9_DONE ==="
