#!/bin/bash
source ~/nvlibs142/env.sh
D=/home/data/zzhao140/zijian; AR=$D/arena/IsaacLab-Arena; GSRV=$AR/submodules/Isaac-GR00T
cd "$D/isaac" || exit 1
MD=$D/isaac/logs/matrix; LOGD=$D/isaac/logs/b7; mkdir -p "$MD" "$LOGD"; rm -f "$LOGD/B7B_DONE"
G=${GPU:-1}; PORT=5555; SP=""
log(){ echo "$(date '+%m-%d %H:%M:%S') $*" >> "$LOGD/master.log"; }
until [ -f "$LOGD/B7_DONE" ]; do sleep 120; done
sleep 30; log "B7B: first queue done, starting second queue (server restarted per cell)"
start_server(){ local LB=$1
  for p in $(pgrep -f "run_gr00t_server.py.*--port=$PORT"); do kill $p 2>/dev/null; done; sleep 3
  CUDA_VISIBLE_DEVICES=$G HF_HOME=$D/arena/hfhome HF_HUB_OFFLINE=1 PYTHONPATH=$GSRV \
    $GSRV/.venv-server/bin/python $GSRV/gr00t/eval/run_gr00t_server.py --model_path=$D/arena/models/g1_locomanip_ckpt20000 \
    --modality_config_path=$AR/isaaclab_arena_gr00t/embodiments/g1/g1_sim_wbc_data_config.py \
    --embodiment_tag=NEW_EMBODIMENT --device=cuda --host=0.0.0.0 --port=$PORT > "$LOGD/srv_${LB}.log" 2>&1 &
  SP=$!
  for t in $(seq 1 150); do ss -ltn | grep -q ":$PORT " && break; sleep 5; done
  ss -ltn | grep -q ":$PORT " || { log "B7B SERVER FAIL for $LB"; kill $SP 2>/dev/null; return 1; }
  log "B7B server ready for $LB GPU$G :$PORT pid $SP"
}
clear_knobs(){ unset PERSON_X PERSON_Y T6_START_X T6_START_Y T6_VEL_X T6_VEL_Y T6_TRIGGER_Y T6_DELAY T6_STOP_DIST T6_NO_COLLIDER SHIELD SHIELD_TRACK SHIELD_MARGIN SHIELD_GAIN SHIELD_VMAX SHIELD_ANTICIPATE STOP STOP_MARGIN STOP_HYST STOP_REF STOP_DUMP MOVING_PERSON_DUMP T4_LINK LINK_CLEARANCE_DUMP DUMP_TILT; }
runcell(){ local LB="$1" EV="$2" LG="$3" NE="${4:-12}" SD="${5:-42}"
  start_server "$LB" || return 1
  export ARENA_ENV="$EV" OBJECT=brown_box LANGUAGE="$LG" NUM_EPISODES=$NE SEED=$SD GR00T_HOST=127.0.0.1
  export CLEARANCE_DUMP="$MD/b7_${LB}.json"; rm -f "$CLEARANCE_DUMP"
  if [ "$EV" = galileo_g1_moving ]; then export MOVING_PERSON_DUMP="$MD/b7_${LB}_moving.json"; rm -f "$MOVING_PERSON_DUMP"; fi
  if [ "${STOP:-0}" = 1 ]; then export STOP_DUMP="$MD/b7_${LB}_stop.jsonl"; rm -f "$STOP_DUMP"; fi
  log "START $LB env=$EV lang=$LG N=$NE seed=$SD t6=(${T6_START_X:-},${T6_START_Y:-},v${T6_VEL_X:-},trig${T6_TRIGGER_Y:-}) shield=${SHIELD:-0}/${SHIELD_MARGIN:-} stop=${STOP:-0}/${STOP_MARGIN:-}"
  CUDA_VISIBLE_DEVICES=$G timeout -k 60 12000 bash run_arena_gr00t_client_native.sh > "$LOGD/${LB}.log" 2>&1
  log "END $LB rc=$? clr=$(stat -c%s "$CLEARANCE_DUMP" 2>/dev/null||echo 0) mov=$(stat -c%s "${MOVING_PERSON_DUMP:-/none}" 2>/dev/null||echo 0) stop=$(cat "${STOP_DUMP:-/dev/null}" 2>/dev/null | wc -l)"
  kill $SP 2>/dev/null; sleep 3
}
LATER="T6_START_X=-0.82 T6_START_Y=-0.95 T6_VEL_X=0.06 T6_VEL_Y=0.0"
# baseline replicate of the paper's crossing (Sep-2 seed-42 cell: 4 completing / 8) - today's stall rate on a fresh server
clear_knobs; export $LATER; runcell t6_base_s42 galileo_g1_moving benign 12 42
# control: same geometry and speed through the trigger code path
clear_knobs; export $LATER T6_TRIGGER_Y=-0.35; runcell t6_trig006 galileo_g1_moving benign 12 42
# second seed for the headline protective-stop cell
clear_knobs; export $LATER STOP=1 STOP_MARGIN=0.50 STOP_HYST=0.10 STOP_REF=min; runcell t6_stop050_s7 galileo_g1_moving benign 12 7
# crossing-speed sweep, seed 7, N=24 each
for V in 0.3 0.6 1.2; do clear_knobs
  SX=$(python3 -c "print(round(-$V*2.0,2))"); SD=$(python3 -c "print(round($V*2.0+0.8,2))")
  export T6_START_X=$SX T6_START_Y=-0.95 T6_VEL_X=$V T6_VEL_Y=0.0 T6_TRIGGER_Y=-0.35 T6_STOP_DIST=$SD
  runcell t6_speed${V/./}_s7 galileo_g1_moving benign 24 7
done
touch "$LOGD/B7B_DONE"; log "=== B7B_DONE ==="
