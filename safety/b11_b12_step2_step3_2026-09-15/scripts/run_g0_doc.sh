#!/bin/bash
# GR00T N1.6-DROID on Arena's documented example, unmodified environment (pick_and_place_maple_table, home_office light), one
# recorded episode, then a few frames as PNG so we can see whether the arm moves. Video stays on chaowei.
D=/home/data/zzhao140/zijian; AR=$D/arena/IsaacLab-Arena; LOGD=$D/isaac/logs/fr; OUT=$LOGD/video_g0doc
G=${1:-1}; PORT=${2:-5557}
cd $AR || exit 1
export ACCEPT_EULA=Y OMNI_KIT_ACCEPT_EULA=YES PYTHONPATH=$AR:$AR/submodules/Isaac-GR00T
export VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json VK_DRIVER_FILES=/usr/share/vulkan/icd.d/nvidia_icd.json
rm -rf $OUT; mkdir -p $OUT
echo "$(date '+%m-%d %H:%M:%S') START g0_doc (documented env, video) gpu=$G port=$PORT" >> $LOGD/master.log
CUDA_VISIBLE_DEVICES=$G timeout -k 60 1500 .venv/bin/python isaaclab_arena/evaluation/policy_runner.py \
  --policy_type isaaclab_arena_gr00t.policy.gr00t_remote_closedloop_policy.Gr00tRemoteClosedloopPolicy \
  --policy_config_yaml_path isaaclab_arena_gr00t/policy/config/droid_manip_gr00t_closedloop_config.yaml \
  --remote_host 127.0.0.1 --remote_port $PORT --record_viewport_video --output_base_dir $OUT \
  --seed 42 --language_instruction "Pick up the Rubik's cube and place it in the bowl." --num_episodes 1 --num_envs 1 --headless --enable_cameras \
  pick_and_place_maple_table --embodiment droid_abs_joint_pos --pick_up_object rubiks_cube_hot3d_robolab --destination_location bowl_ycb_robolab \
  --hdr home_office_robolab > $LOGD/g0_doc.log 2>&1
RC=$?
echo "$(date '+%m-%d %H:%M:%S') END g0_doc rc=$RC met=[$(grep -E 'Metrics' $LOGD/g0_doc.log | tail -1 | cut -c1-200)]" >> $LOGD/master.log
V=$(find $OUT -name "*.mp4" | head -1); echo "video: $V"
[ -n "$V" ] && $AR/.venv/bin/python - "$V" "$OUT" <<'EOF'
import sys, imageio.v2 as iio, os
v, out = sys.argv[1], sys.argv[2]
r = iio.get_reader(v); n = r.count_frames(); fps = r.get_meta_data().get("fps", 30)
print("frames", n, "fps", fps)
for t in (0.02, 0.25, 0.5, 0.75, 0.98):
    k = min(n - 1, int(t * n)); im = r.get_data(k)
    h, w = im.shape[:2]; im = im[::2, ::2]
    iio.imwrite(os.path.join(out, f"frame_{int(t*100):02d}.png"), im)
print("frames written")
EOF
exit 0
