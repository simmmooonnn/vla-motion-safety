"""侦察 Isaac API：把后续任务需要的真实方法名打印出来。"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from motion_safety.envguard import check_ascii_env

check_ascii_env()

from isaacsim import SimulationApp  # noqa: E402

simulation_app = SimulationApp({"headless": True})

import omni.kit.app  # noqa: E402

omni.kit.app.get_app().get_extension_manager().set_extension_enabled_immediate(
    "isaacsim.robot.experimental.manipulators.examples", True
)

import isaacsim.core.experimental.objects as objects_mod  # noqa: E402
import isaacsim.robot_motion.experimental.motion_generation as mg  # noqa: E402
import isaacsim.core.experimental.utils.app as app_utils  # noqa: E402
from isaacsim.core.experimental.prims import Articulation, RigidPrim  # noqa: E402
from isaacsim.robot.experimental.manipulators.examples.franka import (  # noqa: E402
    FrankaFollowTarget,
)


def show(label, names):
    print(f"PROBE {label}: {sorted(names)}")


print("PROBE === objects module: 是否有 Capsule ===")
show("objects_exports", [n for n in dir(objects_mod) if not n.startswith("_")])

print("PROBE === Articulation: 关节与连杆相关方法 ===")
art_methods = [m for m in dir(Articulation) if not m.startswith("_")]
show("articulation_dof", [m for m in art_methods if "dof" in m.lower()])
show("articulation_link", [m for m in art_methods if "link" in m.lower() or "body" in m.lower()])
show("articulation_pose", [m for m in art_methods if "pose" in m.lower()])

print("PROBE === ObstacleStrategy / ObstacleConfiguration ===")
mg_all_exports = [n for n in dir(mg) if not n.startswith("_")]
show("mg_exports", mg_all_exports)
show(
    "mg_exports_obstacle_related",
    [n for n in mg_all_exports if "obstacle" in n.lower()],
)

print("PROBE === 建一个真实场景，读取实际值 ===")
follow = FrankaFollowTarget()
follow.setup_scene(target_position=[0.4, 0.0, 0.4])
art = Articulation("/World/robot")
simulation_app.update()

print("PROBE dof_names:", art.dof_names)
try:
    print("PROBE link_names:", art.link_names)
except Exception as exc:
    print("PROBE link_names FAILED:", repr(exc))

try:
    pos = art.get_dof_positions()
    print("PROBE get_dof_positions shape:", getattr(pos, "shape", None), "value:", pos)
except Exception as exc:
    print("PROBE get_dof_positions FAILED:", repr(exc))

for cand in (
    "set_dof_positions",
    "set_dof_state",
    "set_joint_positions",
    "set_dof_position_targets",
):
    print(f"PROBE Articulation has {cand}:", hasattr(art, cand))

for cand in ("get_link_poses", "get_link_transforms", "get_world_poses"):
    print(f"PROBE Articulation has {cand}:", hasattr(art, cand))

try:
    lp = art.get_link_poses()
    print("PROBE get_link_poses ->", type(lp), getattr(lp, "__len__", lambda: "?")())
except Exception as exc:
    print("PROBE get_link_poses FAILED:", repr(exc))

print("PROBE === 实测调用 Articulation.get_world_poses()（区分是否只返回根节点）===")
try:
    art_pos, art_ori = art.get_world_poses()
    print(
        "PROBE Articulation.get_world_poses() shapes:",
        art_pos.shape,
        art_ori.shape,
        "pos:",
        art_pos.numpy(),
        "ori:",
        art_ori.numpy(),
    )
except Exception as exc:
    print("PROBE Articulation.get_world_poses() FAILED:", repr(exc))

print("PROBE === 用 RigidPrim 读取单个连杆世界位姿（未 play） ===")
try:
    hand = RigidPrim("/World/robot/panda_hand")
    pos, ori = hand.get_world_poses()
    print("PROBE RigidPrim(panda_hand).get_world_poses() shapes:", pos.shape, ori.shape, "pos:", pos.numpy())
except Exception as exc:
    print("PROBE RigidPrim single-link get_world_poses FAILED:", repr(exc))

print("PROBE === 用 RigidPrim 批量读取所有连杆世界位姿（未 play） ===")
try:
    link_paths = [f"/World/robot/{name}" for name in art.link_names]
    all_links = RigidPrim(link_paths)
    positions, orientations = all_links.get_world_poses()
    print(
        "PROBE RigidPrim(all links).get_world_poses() shapes:",
        positions.shape,
        orientations.shape,
        "order matches link_names:",
        art.link_names,
    )
    print(
        "PROBE === 四元数分量顺序核验：逐连杆打印原始朝向，寻找单位四元数 ===\n"
        "PROBE wxyz 约定下单位四元数应为 [1,0,0,0]；xyzw 约定下应为 [0,0,0,1]"
    )
    ori_np = orientations.numpy()
    for name, quat in zip(art.link_names, ori_np):
        print(f"PROBE link {name} raw orientation:", quat.tolist())
except Exception as exc:
    print("PROBE RigidPrim all-links get_world_poses FAILED:", repr(exc))

print("PROBE === 播放仿真时间线后再读取/设置关节位置 ===")
try:
    app_utils.play()
    simulation_app.update()
    print("PROBE app_utils.is_playing():", app_utils.is_playing())
    pos_after_play = art.get_dof_positions()
    print(
        "PROBE get_dof_positions AFTER play shape:",
        getattr(pos_after_play, "shape", None),
        "value:",
        pos_after_play,
    )
    art.set_dof_positions([0.1, -0.5, 0.0, -2.5, 0.0, 3.0, 0.7, 0.03, 0.03])
    simulation_app.update()
    pos_set = art.get_dof_positions()
    print("PROBE get_dof_positions AFTER set_dof_positions:", pos_set)
except Exception as exc:
    print("PROBE play + set/get_dof_positions FAILED:", repr(exc))

print("PROBE === 播放后再用 RigidPrim 读取连杆世界位姿 ===")
try:
    pos2, ori2 = hand.get_world_poses()
    print("PROBE RigidPrim(panda_hand).get_world_poses() AFTER play:", pos2.numpy(), ori2.numpy())
except Exception as exc:
    print("PROBE RigidPrim get_world_poses AFTER play FAILED:", repr(exc))

simulation_app.close()
