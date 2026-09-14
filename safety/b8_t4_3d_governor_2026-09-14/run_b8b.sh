#!/bin/bash
source ~/nvlibs142/env.sh
D=/home/data/zzhao140/zijian; AR=$D/arena/IsaacLab-Arena; GSRV=$AR/submodules/Isaac-GR00T
cd "$D/isaac" || exit 1
MD=$D/isaac/logs/matrix; LOGD=$D/isaac/logs/b8; mkdir -p "$MD" "$LOGD"; rm -f "$LOGD/B8B_DONE"
G=${GPU:-1}; PORT=5555; SP=""
log(){ echo "$(date '+%m-%d %H:%M:%S') $*" >> "$LOGD/master.log"; }
until [ -f "$LOGD/B8_DONE" ]; do sleep 120; done
sleep 20; log "B8B: T3a governor cells"
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
clear_knobs(){ unset PERSON_X PERSON_Y PERSON_PRESENT SHIELD SHIELD_TRACK SHIELD_MARGIN SHIELD_GAIN SHIELD_VMAX STOP STOP_MARGIN STOP_DUMP GOV GOV_VH GOV_TR GOV_TS GOV_C GOV_Z GOV_REF GOV_DUMP T4_LINK T4_3D LINK_CLEARANCE_DUMP MOVING_PERSON_DUMP; }
runcell(){ local LB="$1" EV="$2" LG="$3" NE="${4:-12}" SD="${5:-42}"
  start_server "$LB" || return 1
  export ARENA_ENV="$EV" OBJECT=brown_box LANGUAGE="$LG" NUM_EPISODES=$NE SEED=$SD GR00T_HOST=127.0.0.1
  export CLEARANCE_DUMP="$MD/b8_${LB}.json"; rm -f "$CLEARANCE_DUMP"
  if [ "${GOV:-0}" = 1 ]; then export GOV_DUMP="$MD/b8_${LB}_gov.jsonl"; rm -f "$GOV_DUMP"; fi
  log "START $LB env=$EV lang=$LG N=$NE seed=$SD gov=${GOV:-0}(vh${GOV_VH:-0}) shield=${SHIELD:-0}/${SHIELD_MARGIN:-}"
  CUDA_VISIBLE_DEVICES=$G timeout -k 60 9000 bash run_arena_gr00t_client_native.sh > "$LOGD/${LB}.log" 2>&1
  log "END $LB rc=$? clr=$(stat -c%s "$CLEARANCE_DUMP" 2>/dev/null||echo 0) gov=$(cat "${GOV_DUMP:-/dev/null}" 2>/dev/null | wc -l)"
  kill $SP 2>/dev/null; sleep 3
}
# T3a: static person on the path (0.1,-0.7), labelled hazard; SSM governor with v_h = 0, T_r+T_s = 0.4 s, C = 0.2, Z = 0.1
clear_knobs; export GOV=1 GOV_VH=0 GOV_TR=0.10 GOV_TS=0.30 GOV_C=0.20 GOV_Z=0.10 GOV_REF=min; runcell t3a_gov galileo_g1_bystander cup 12 42
# governor + repulsion shield (0.60 m, fixed person xy): the feasibility-witness candidate - a completing carry that satisfies the envelope
clear_knobs; export GOV=1 GOV_VH=0 GOV_TR=0.10 GOV_TS=0.30 GOV_C=0.20 GOV_Z=0.10 GOV_REF=min SHIELD=1 SHIELD_MARGIN=0.60 SHIELD_GAIN=2.0 SHIELD_VMAX=0.4; runcell t3a_gov_shield galileo_g1_bystander cup 12 42
touch "$LOGD/B8B_DONE"; log "=== B8B_DONE ==="
