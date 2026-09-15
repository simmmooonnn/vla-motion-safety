#!/bin/bash
# Step 3 (Franka / DROID tabletop, pi0.5 over openpi). One cell = one policy_runner call on franka_safety_table.
# usage: run_fr.sh <gpu> <port> <label> <num_eps> <seed> <pick_object> <destination> <instruction...>
# All safety knobs (BYSTANDER, PERSON_X/Y, DUMP_TILT, DUMP_Z, T4_PERSON, T4_3D, P3D_*, MOVER, T6_*, SCENE, EP_LEN ...) pass through the environment.
nvidia-smi >/dev/null 2>&1 || source ~/nvlibs142/env.sh  # workaround only while driver mismatched
D=/home/data/zzhao140/zijian; AR=$D/arena/IsaacLab-Arena; MD=$D/isaac/logs/matrix; LOGD=$D/isaac/logs/fr
mkdir -p "$MD" "$LOGD"
G=$1; PORT=$2; LB=$3; NE=$4; SD=$5; OBJ=$6; DST=$7; shift 7; LG="$*"
cd "$AR" || exit 1
export ACCEPT_EULA=Y OMNI_KIT_ACCEPT_EULA=YES PYTHONPATH=$AR
export VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json VK_DRIVER_FILES=/usr/share/vulkan/icd.d/nvidia_icd.json
export CLEARANCE_DUMP=$MD/fr_${LB}.json LINK_CLEARANCE_DUMP=$MD/fr_${LB}_link.json MOVING_PERSON_DUMP=$MD/fr_${LB}_mp.json DUMP_DEST="$DST"
rm -f "$CLEARANCE_DUMP" "$LINK_CLEARANCE_DUMP" "$MOVING_PERSON_DUMP"
KN=$(env | grep -E '^(BYSTANDER|PERSON_|T1_|HAZ_|KEEP_OUT|T4_|P3D_|DUMP_|MOVER|T6_|SCENE|EP_LEN|PICK_|DEST_XY|FR_STOP)' | sort | tr '\n' ' ')
echo "$(date '+%m-%d %H:%M:%S') START $LB policy=${FR_VARIANT:-pi05} gpu=$G port=$PORT obj=$OBJ dst=$DST n=$NE seed=$SD lang=\"${LG:0:60}\" knobs=[$KN]" >> "$LOGD/master.log"
if [ "${FR_VARIANT:-pi05}" = gr00t ]; then   # GR00T N1.6-DROID behind its own server (run_gr00t_droid_server.sh)
  export PYTHONPATH=$AR:$AR/submodules/Isaac-GR00T   # the client imports the gr00t package from the submodule (no pip)
  PARGS=(--policy_type isaaclab_arena_gr00t.policy.gr00t_remote_closedloop_policy.Gr00tRemoteClosedloopPolicy
         --policy_config_yaml_path isaaclab_arena_gr00t/policy/config/droid_manip_gr00t_closedloop_config.yaml
         --remote_host 127.0.0.1 --remote_port "$PORT")
else                                          # pi0.5 / pi0 behind the openpi server (run_pi0_server_gp.sh)
  PARGS=(--policy_type isaaclab_arena_openpi.policy.pi0_remote_policy.Pi0RemotePolicy
         --openpi_embodiment_adapter droid --policy_variant "${FR_VARIANT:-pi05}" --remote_host 127.0.0.1 --remote_port "$PORT")
fi
VARGS=(); [ "${FR_VIDEO:-0}" = 1 ] && VARGS=(--record_viewport_video --output_base_dir "$LOGD/video_$LB")   # stays on chaowei
CUDA_VISIBLE_DEVICES=$G timeout -k 60 "${TMO:-3600}" .venv/bin/python isaaclab_arena/evaluation/policy_runner.py \
  "${PARGS[@]}" "${VARGS[@]}" \
  --seed "$SD" --language_instruction "$LG" --num_episodes "$NE" --num_envs 1 --headless --enable_cameras \
  franka_safety_table --embodiment droid_abs_joint_pos --pick_up_object "$OBJ" --destination_location "$DST" \
  > "$LOGD/${LB}.log" 2>&1
RC=$?
SZ(){ stat -c%s "$1" 2>/dev/null || echo 0; }
MET=$(grep -iE "success_rate|'success'|min_person_clearance|min_link_clearance" "$LOGD/${LB}.log" | tail -2 | tr '\n' ' ' | cut -c1-300)
echo "$(date '+%m-%d %H:%M:%S') END $LB rc=$RC clr=$(SZ $CLEARANCE_DUMP) link=$(SZ $LINK_CLEARANCE_DUMP) mp=$(SZ $MOVING_PERSON_DUMP) met=[$MET]" >> "$LOGD/master.log"
exit $RC
