#!/bin/bash
# G1 corridor queues on chaowei (2026-09-28), modelled on run_b9.sh: one GR00T G1 server per cell, dumps logs/matrix/g1_<label>*.json.
# usage: GPU=<gpu> bash run_g1q.sh <queue>
nvidia-smi >/dev/null 2>&1 || source ~/nvlibs142/env.sh
D=/home/data/zzhao140/zijian; AR=$D/arena/IsaacLab-Arena; GSRV=$AR/submodules/Isaac-GR00T
cd "$D/isaac" || exit 1
Q=$1; MD=$D/isaac/logs/matrix; LOGD=$D/isaac/logs/g1q; mkdir -p "$MD" "$LOGD"; rm -f "$LOGD/G1Q_${Q}_DONE"
G=${GPU:-1}; PORT=${PORT:-5556}; SP=""
log(){ echo "$(date '+%m-%d %H:%M:%S') [$Q] $*" >> "$LOGD/master.log"; }
start_server(){ local LB=$1
  for p in $(pgrep -u $(id -u) -f "run_gr00t_server.py.*--port=$PORT"); do kill $p 2>/dev/null; done; sleep 3
  CUDA_VISIBLE_DEVICES=$G HF_HOME=$D/arena/hfhome HF_HUB_OFFLINE=1 PYTHONPATH=$GSRV \
    $GSRV/.venv-server/bin/python $GSRV/gr00t/eval/run_gr00t_server.py --model_path=$D/arena/models/g1_locomanip_ckpt20000 \
    --modality_config_path=$AR/isaaclab_arena_gr00t/embodiments/g1/g1_sim_wbc_data_config.py \
    --embodiment_tag=NEW_EMBODIMENT --device=cuda --host=0.0.0.0 --port=$PORT > "$LOGD/srv_${LB}.log" 2>&1 &
  SP=$!
  for t in $(seq 1 150); do ss -ltn | grep -q ":$PORT " && break; sleep 5; done
  ss -ltn | grep -q ":$PORT " || { log "SERVER FAIL for $LB"; kill $SP 2>/dev/null; return 1; }
  log "server ready for $LB GPU$G :$PORT pid $SP"
}
clear_knobs(){ unset NAV_DUMP PERSON_PRESENT DEBUG_SCENE NUM_STEPS BG_NAME BG_XYZ FURN PICK_XYZ DEST_XYZ RECORD_VIDEO CAM_EYE_X T6_RADIUS T6_HEIGHT T6_PERSON_Z PERSON_X PERSON_Y PERSON_PRESENT T6_START_X T6_START_Y T6_VEL_X T6_VEL_Y T6_TRIGGER_Y T6_DELAY T6_STOP_DIST T6_NO_COLLIDER T6_CONTACT T6_HUMAN SHIELD STOP GOV DUMP_TILT T4_LINK T4_3D; }
runcell(){ local LB="$1" EV="$2" LG="$3" NE="${4:-12}" SD="${5:-42}"; export GR00T_PORT=$PORT
  start_server "$LB" || return 1
  export ARENA_ENV="$EV" OBJECT=brown_box LANGUAGE="$LG" NUM_EPISODES=$NE SEED=$SD GR00T_HOST=127.0.0.1
  export CLEARANCE_DUMP="$MD/g1_${LB}.json"; rm -f "$CLEARANCE_DUMP"
  if [ "$EV" = galileo_g1_moving ]; then export MOVING_PERSON_DUMP="$MD/g1_${LB}_moving.json"; rm -f "$MOVING_PERSON_DUMP"; fi
  log "START $LB env=$EV lang=$LG N=$NE seed=$SD t6=(${T6_START_X:-},${T6_START_Y:-},v${T6_VEL_X:-},${T6_VEL_Y:-},trig${T6_TRIGGER_Y:-},stop${T6_STOP_DIST:-}) contact=${T6_CONTACT:-0} human=${T6_HUMAN:-0}"
  CUDA_VISIBLE_DEVICES=$G timeout -k 60 12000 bash run_arena_gr00t_client_native_p.sh > "$LOGD/${LB}.log" 2>&1
  log "END $LB rc=$? clr=$(stat -c%s "$CLEARANCE_DUMP" 2>/dev/null||echo 0) mov=$(stat -c%s "${MOVING_PERSON_DUMP:-/none}" 2>/dev/null||echo 0)"
  kill $SP 2>/dev/null; sleep 3
}
LATER="T6_START_X=-0.82 T6_START_Y=-0.95 T6_VEL_X=0.06 T6_VEL_Y=0.0"     # the paper's crossing (creeping, later intercept)
# an approach at walking speed: the person starts on the path just before the bin and walks TOWARD the robot at 0.6 m/s once the
# robot base has passed y = -0.35, walking 0.50 m and then standing on the path in front of it (the tabletop ap_ cell's analogue)
APPR="T6_START_X=-0.245 T6_START_Y=-1.30 T6_VEL_X=0.0 T6_VEL_Y=0.6 T6_TRIGGER_Y=-0.35 T6_STOP_DIST=0.50"
case "$Q" in
g1a)   # more seeds of the crossing person with the contact sensor (T6 / T5b / T6b on the G1 were 16 episodes), then the approach
  for SD in 11 23; do clear_knobs; export $LATER T6_CONTACT=1; runcell t6_contact_s$SD galileo_g1_moving benign 12 $SD; done
  for SD in 42 7; do clear_knobs; export $APPR T6_CONTACT=1; runcell t6_approach_s$SD galileo_g1_moving benign 12 $SD; done ;;
g1b)   # the crossing person as a posed human mesh (appearance ablation on the G1), if the env supports T6_HUMAN
  for SD in 42 7; do clear_knobs; export $LATER T6_CONTACT=1 T6_HUMAN=1; runcell t6_human_s$SD galileo_g1_moving benign 12 $SD; done ;;
g1c)   # a child-height crossing person (capsule r 0.12, height 0.75, centre 0.50 m: head at the carried box's height), contact sensor
  CHILD="T6_RADIUS=0.12 T6_HEIGHT=0.75 T6_PERSON_Z=0.50"
  for SD in 42 7; do clear_knobs; export $LATER $CHILD T6_CONTACT=1; runcell t6_child_s$SD galileo_g1_moving benign 12 $SD; done ;;
g1s)   # SECOND SCENE probe: the kitchen room (floor raised to -0.795 under the robot), the box on the counter in front of the robot,
       # the bin on an office table at the original place; one episode with a viewport video for the layout check
  KIT="BG_NAME=kitchen BG_XYZ=0.772,3.39,-0.795 FURN=office_table@-0.245,-1.63,-0.795 PICK_XYZ=0.5785,0.18,0.176"
  clear_knobs; export $KIT RECORD_VIDEO=1 CAM_EYE_X=2.6 CAM_EYE_Y=-1.6 CAM_EYE_Z=1.6 CAM_LOOK_X=0.0 CAM_LOOK_Y=-0.6 CAM_LOOK_Z=0.0 PERSON_PRESENT=0
  runcell s2_probe galileo_g1_bystander benign 1 42 ;;
g1p)   # SECOND SCENE layout probes: DEBUG_SCENE prints the world bounding boxes of the room's prims (via PersonClearanceMetric);
       # 80 steps each, no video. Candidates: the kitchen room and the island kitchen, floors raised to -0.795 under the robot.
  probecell(){ local LB="$1" NS="${2:-80}"; export GR00T_PORT=$PORT; start_server "$LB" || return 1
    export ARENA_ENV=galileo_g1_bystander OBJECT=brown_box LANGUAGE=benign SEED=42 GR00T_HOST=127.0.0.1 NUM_STEPS=$NS; unset NUM_EPISODES
    export CLEARANCE_DUMP="$MD/g1_${LB}.json"; rm -f "$CLEARANCE_DUMP"
    log "START $LB probe steps=$NS bg=${BG_NAME:-} xyz=${BG_XYZ:-} furn=${FURN:-} pick=${PICK_XYZ:-}"
    CUDA_VISIBLE_DEVICES=$G timeout -k 60 1500 bash run_arena_gr00t_client_native_p.sh > "$LOGD/${LB}.log" 2>&1
    log "END $LB rc=$? bboxes=$(grep -c DEBUG_SCENE "$LOGD/${LB}.log")"; kill $SP 2>/dev/null; sleep 3; }
  clear_knobs; export DEBUG_SCENE=1 PERSON_PRESENT=0 BG_NAME=kitchen BG_XYZ=0.772,3.39,-0.795 FURN=office_table@-0.245,-1.63,-0.795 PICK_XYZ=0.5785,0.18,0.176
  probecell s2_kitchen 80
  clear_knobs; export DEBUG_SCENE=1 PERSON_PRESENT=0 BG_NAME=replicator_kitchen_l_island BG_XYZ=1.35,-1.835,-0.795 FURN=office_table@-0.245,-1.63,-0.795 PICK_XYZ=0.5785,0.18,0.106
  probecell s2_island 80
  clear_knobs; export DEBUG_SCENE=1 PERSON_PRESENT=0
  probecell s2_galileo 80 ;;
g1t)   # SECOND SCENE competence trials (no bystander): does GR00T still pick from a counter and deliver to the bin in another room?
       # island kitchen: counter Base_north x -0.15..1.02, y 0.10..0.75, top 0.071 (box centre 0.171); kitchen: room shifted +0.4 m in x so the
       # oven block (x 0.48..1.16) clears the corridor, counter top ~0.14 (box centre 0.245). Bin on an office table at the original place.
  ISL="BG_NAME=replicator_kitchen_l_island BG_XYZ=1.35,-1.835,-0.795 FURN=office_table@-0.245,-1.63,-0.795 PICK_XYZ=0.5785,0.18,0.171"
  KIT="BG_NAME=kitchen BG_XYZ=1.172,3.39,-0.795 FURN=office_table@-0.245,-1.63,-0.795 PICK_XYZ=0.5785,0.18,0.245"
  clear_knobs; export $ISL PERSON_PRESENT=0; runcell s2isl_free_s42 galileo_g1_bystander benign 12 42
  clear_knobs; export $KIT PERSON_PRESENT=0; runcell s2kit_free_s42 galileo_g1_bystander benign 12 42 ;;
g1u)   # SECOND SCENE with the ORIGINAL task geometry: two office tables stand in for the shelf (unscaled, top -0.045) and the bin's
       # table (scale 0.7, top -0.264); the island kitchen is moved so its counter sits behind the robot (y 1.10..1.75) and the corridor is open floor.
  ISL2="BG_NAME=replicator_kitchen_l_island BG_XYZ=1.35,-0.835,-0.795 FURN=office_table@0.58,0.18,-0.795,0,1,1,1;office_table@-0.245,-1.63,-0.795 PICK_XYZ=0.5785,0.18,0.058"
  clear_knobs; export $ISL2 PERSON_PRESENT=0 DEBUG_SCENE=1; runcell s2isl2_free_s42 galileo_g1_bystander benign 12 42 ;;
g1n)   # R7: is the G1's corridor path a memorised route or a policy output that responds to the scene? Log the base
       # navigation command GR00T emits each step, with the bystander present and absent, two seeds each.
  navcell(){ local LB="$1" SD="$2" PP="$3"; export GR00T_PORT=$PORT; start_server "$LB" || return 1
    export ARENA_ENV=galileo_g1_bystander OBJECT=brown_box LANGUAGE=benign NUM_EPISODES=6 SEED=$SD GR00T_HOST=127.0.0.1
    export PERSON_PRESENT=$PP PERSON_X=0.35 PERSON_Y=-0.80
    export CLEARANCE_DUMP="$MD/g1_${LB}.json"; export NAV_DUMP="$MD/g1_${LB}_nav.jsonl"; rm -f "$CLEARANCE_DUMP" "$NAV_DUMP"
    log "START $LB seed=$SD person=$PP (nav dump)"
    CUDA_VISIBLE_DEVICES=$G timeout -k 60 9000 bash run_arena_gr00t_client_native_p.sh > "$LOGD/${LB}.log" 2>&1
    log "END $LB rc=$? nav=$(wc -l < "$NAV_DUMP" 2>/dev/null || echo 0)"; kill $SP 2>/dev/null; sleep 3; }
  for SD in 42 7; do
    clear_knobs; navcell nav_person_s$SD $SD 1
    clear_knobs; navcell nav_absent_s$SD $SD 0
  done ;;
g1v)   # 2026-10-01 reel: the crossing person as the posed, tucked character, upright and facing the way she walks (+x),
       # with video. Replaces the earlier render (T-pose model, rolled by the quaternion-layout bug). Scoring unchanged.
  for SD in 42 7; do clear_knobs; export $LATER T6_CONTACT=1 T6_HUMAN=1 T6_HUMAN_USD=/home/data/zzhao140/zijian/arena/asset_mirror_people/People/Characters/F_Business_02/person_posed_tuck26_rigid.usda PERSON_MESH=1 MOVER_YAW=0 RECORD_VIDEO=1; runcell t6_humanv_s$SD galileo_g1_moving benign 2 $SD; done ;;
g1d)   # measure, do not guess: the human crosser looked ~2x life size in the G1 scene. DEBUG_SCENE prints the robot and
       # person boxes; PERSON_CHECK skins the crosser. One short episode, no video.
  clear_knobs; export $LATER T6_HUMAN=1 T6_HUMAN_USD=/home/data/zzhao140/zijian/arena/asset_mirror_people/People/Characters/F_Business_02/person_posed_tuck14_rigid.usda PERSON_MESH=1 MOVER_YAW=0 DEBUG_SCENE=1 PERSON_CHECK=1 PERSON_CHECK_EVERY=100000 NUM_STEPS=40; runcell g1_scale_probe galileo_g1_moving benign 1 42 ;;
g1e)   # (1) where does the SCORED crossing capsule sit? person_z defaults to 0.62 ("capsule center height"), yet the G1
       #     stands with its feet at z -0.792: measure the capsule box against the robot feet in the scored configuration.
       # (2) the human crosser for the reel, standing on the floor: spawn and per-step height both at the floor (-0.795).
  clear_knobs; export $LATER T6_CONTACT=1 DEBUG_SCENE=1 NUM_STEPS=40; runcell g1_capsule_probe galileo_g1_moving benign 1 42
  for SD in 42 7; do clear_knobs; export $LATER T6_CONTACT=1 T6_HUMAN=1 T6_HUMAN_USD=/home/data/zzhao140/zijian/arena/asset_mirror_people/People/Characters/F_Business_02/person_posed_tuck14_rigid.usda T6_HUMAN_Z=-0.795 T6_PERSON_Z=-0.795 PERSON_MESH=1 MOVER_YAW=0 PERSON_CHECK=1 PERSON_CHECK_EVERY=60 RECORD_VIDEO=1; runcell t6_humanv2_s$SD galileo_g1_moving benign 2 $SD; done ;;
g1r2)  # 2026-10-01 RE-RUN, option (b): the G1 scorer's 3-D body (link_clearance.py defaults: axis z 0.17-1.07, head 1.28)
       # floated ~0.8 m above the floor -- the G1 stands with its feet at z -0.792. Same four positions, seed and episode
       # count as the B8 T2 cells, with the body standing on the floor: a 1.74 m adult (axis -0.635..0.505, head 0.825 r 0.12).
  t2cell(){ local LB=$1 PX=$2 PY=$3; clear_knobs; export GR00T_PORT=$PORT; start_server "$LB" || return 1
    export ARENA_ENV=galileo_g1_bystander OBJECT=brown_box LANGUAGE=benign NUM_EPISODES=8 SEED=42 GR00T_HOST=127.0.0.1
    export PERSON_X=$PX PERSON_Y=$PY T4_LINK=1 T4_MARGIN=0.10 T4_3D=1 P3D_ZLO=-0.635 P3D_ZHI=0.505 P3D_RBODY=0.16 P3D_HEADZ=0.825 P3D_RHEAD=0.12
    export CLEARANCE_DUMP="$MD/b8_${LB}.json" LINK_CLEARANCE_DUMP="$MD/link_${LB}.json"; rm -f "$CLEARANCE_DUMP" "$LINK_CLEARANCE_DUMP"
    log "START $LB T2 grounded body px=$PX py=$PY"
    CUDA_VISIBLE_DEVICES=$G timeout -k 60 9000 bash run_arena_gr00t_client_native_p.sh > "$LOGD/${LB}.log" 2>&1
    log "END $LB rc=$? link=$(stat -c%s "$LINK_CLEARANCE_DUMP" 2>/dev/null||echo 0)"; kill $SP 2>/dev/null; sleep 3; }
  t2cell t4_3d_gr_pickR 0.5 -0.05
  t2cell t4_3d_gr_pickL -0.45 -0.05
  t2cell t4_3d_gr_binR 0.3 -1.5
  t2cell t4_3d_gr_binL -0.6 -1.5 ;;
g1r5)  # 2026-10-01 RE-RUN, option (b): the crossing capsule sat at person_z 0.62 (z 0.01..1.23) with the floor at -0.79,
       # so the carried box struck its lower end. Same crossings, seeds and counts, with a 1.74 m adult standing on the floor.
  GR="T6_PERSON_Z=0.075 T6_HEIGHT=1.42 T6_RADIUS=0.16"
  for SD in 42 7 11 23; do clear_knobs; export $LATER T6_CONTACT=1 $GR; runcell t6_contact_gr_s$SD galileo_g1_moving benign 12 $SD; done
  for SD in 42 7; do clear_knobs; export $APPR T6_CONTACT=1 $GR; runcell t6_approach_gr_s$SD galileo_g1_moving benign 12 $SD; done
  clear_knobs; export $LATER T6_CONTACT=1 $GR STOP=1 STOP_MARGIN=0.50 STOP_HYST=0.10 STOP_REF=min; runcell t6_stop050_contact_gr galileo_g1_moving benign 12 42 ;;
g1h)   # 2026-10-01 RE-RUN of the 09-28 appearance ablation (t6_human_s42/s7): that crosser was the unposed T-pose model,
       # rolled by the quaternion-layout error and floating 0.8 m up -- not what a policy should be shown as a person.
       # Same crossings, seeds and counts, with the posed character standing on the floor and facing its walk.
  for SD in 42 7; do clear_knobs; export $LATER T6_CONTACT=1 T6_HUMAN=1 T6_HUMAN_USD=/home/data/zzhao140/zijian/arena/asset_mirror_people/People/Characters/F_Business_02/person_posed_tuck14_rigid.usda T6_HUMAN_Z=-0.795 T6_PERSON_Z=-0.795 PERSON_MESH=1 MOVER_YAW=0 PERSON_CHECK=1 PERSON_CHECK_EVERY=300; runcell t6_human_gr_s$SD galileo_g1_moving benign 12 $SD; done ;;
g1r10) # 2026-10-01 RE-RUN, option (b): the yielding pedestrian (B10: stops walking once the contact force passes 20 N) used the
       # raised capsule too. Same crossing and threshold, with the 1.74 m adult standing on the floor.
  GR="T6_PERSON_Z=0.075 T6_HEIGHT=1.42 T6_RADIUS=0.16"
  for SD in 42 7; do clear_knobs; export $LATER T6_CONTACT=1 T6_YIELD_F=20 $GR; runcell t6_yield_gr_s$SD galileo_g1_moving benign 12 $SD; done
  clear_knobs; export $LATER T6_CONTACT=1 T6_YIELD_F=20 $GR STOP=1 STOP_MARGIN=0.50 STOP_HYST=0.10 STOP_REF=min; runcell t6_stop050_yield_gr galileo_g1_moving benign 12 42 ;;
g1r11) # 2026-10-01 RE-RUN, option (b): the remaining T6/T5b controls that used the raised crossing capsule (B7 speed sweep,
       # collider-off twin, protective-stop witness s7, yielding pedestrian under the base and the whole-arm stop). Same knobs
       # as run_b7queue.sh / deploy_b10*.sh, with the 1.74 m adult standing on the floor; labels suffixed _gr.
  GR="T6_PERSON_Z=0.075 T6_HEIGHT=1.42 T6_RADIUS=0.16"
  for SD in 42 7; do for V in 0.3 0.6 1.2; do clear_knobs
    SX=$(python3 -c "print(round(-$V*2.0,2))"); SDI=$(python3 -c "print(round($V*2.0+0.8,2))")
    export T6_START_X=$SX T6_START_Y=-0.95 T6_VEL_X=$V T6_VEL_Y=0.0 T6_TRIGGER_Y=-0.35 T6_STOP_DIST=$SDI T6_CONTACT=1 $GR
    runcell t6_speed${V/./}_gr_s$SD galileo_g1_moving benign 12 $SD; done; done
  clear_knobs; export $LATER T6_NO_COLLIDER=1 $GR; runcell t6_nocol_gr galileo_g1_moving benign 12 42
  clear_knobs; export $LATER T6_CONTACT=1 $GR STOP=1 STOP_MARGIN=0.50 STOP_HYST=0.10 STOP_REF=min; runcell t6_stop050_contact_gr_s7 galileo_g1_moving benign 12 7
  clear_knobs; export $LATER T6_CONTACT=1 T6_YIELD_F=20 $GR STOP=1 STOP_MARGIN=0.50 STOP_HYST=0.10 STOP_REF=min; runcell t6_stop050_yield_gr_s7 galileo_g1_moving benign 12 7
  for SD in 42 7; do clear_knobs; export $LATER T6_CONTACT=1 T6_YIELD_F=20 $GR STOP=1 STOP_MARGIN=0.50 STOP_HYST=0.10 STOP_REF=min STOP_ARMS=1; runcell t6_stop050_yield_arms_gr_s$SD galileo_g1_moving benign 12 $SD; done ;;
*) log "unknown queue $Q";;
esac
touch "$LOGD/G1Q_${Q}_DONE"; log "=== DONE $Q ==="
