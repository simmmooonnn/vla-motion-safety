"""场景搭建：Franka + hazard 代理 + RMPflow 控制器。依赖 Isaac。

Isaac API 名称与调用顺序均已对照 `docs/api-findings.md` 及本机已安装的
Isaac Sim 6.0.1 源码 / 官方参考 demo 核实，格外注意 API 名称、参数名、
调用顺序的准确性。
"""

from dataclasses import dataclass

import numpy as np

from .config import ExperimentConfig
from .hazard import Capsule, build_hazard
from .sampling import ArmSampler

ROBOT_PRIM_PATH = "/World/robot"
TARGET_PATH = "/World/TargetCube"
HAZARD_PRIM_PATH = "/World/hazard"

CONDITIONS = ("aware", "blind")


@dataclass
class SceneHandles:
    articulation: object
    controller: object
    cumotion_robot: object
    world_binding: object
    sampler: ArmSampler
    capsule: Capsule
    A: np.ndarray
    B: np.ndarray
    tool_frame: str
    site_space: list
    hazard_prim_path: str
    geometry_note: str


def build_scene(cfg: ExperimentConfig, condition: str) -> SceneHandles:
    """搭建场景。condition 决定 hazard 是否注册进规划器世界。

    condition == "aware"：hazard 被加入 world_binding 的 tracked_prims，规划器会避开它。
    condition == "blind"：hazard 仍在场景中、仍被 metrics 度量，但不加入 tracked_prims，
    规划器看不见它。两个条件之间的实现差异**仅此一处**。
    """
    if condition not in CONDITIONS:
        raise ValueError(f"condition 必须是 {CONDITIONS} 之一，收到 {condition!r}")

    import isaacsim.robot_motion.experimental.motion_generation as mg
    from isaacsim.core.experimental.objects import Capsule as IsaacCapsule
    from isaacsim.core.experimental.prims import Articulation, GeomPrim
    from isaacsim.robot.experimental.manipulators.examples.franka import (
        FrankaFollowTarget,
    )
    from isaacsim.robot_motion.cumotion import (
        CumotionWorldInterface,
        RmpFlowController,
        load_cumotion_supported_robot,
    )

    # --- 机器人 ---
    follow = FrankaFollowTarget()
    follow.setup_scene(target_position=[0.4, 0.0, 0.4])  # API-VERIFIED
    articulation = Articulation(ROBOT_PRIM_PATH)  # API-VERIFIED

    cumotion_robot = load_cumotion_supported_robot("franka")  # API-VERIFIED
    site_space = cumotion_robot.robot_description.tool_frame_names()  # API-VERIFIED
    tool_frame = site_space[0]

    ee_link_name, ee_local_offset = _resolve_tool_frame(articulation, tool_frame)
    sampler = ArmSampler(
        articulation=articulation,
        robot_path=ROBOT_PRIM_PATH,
        ee_link_name=ee_link_name,
        n_per_segment=cfg.link_interp_points,
        ee_local_offset=ee_local_offset,
    )

    # --- 复位到 q0，测得 A ---
    reset_to_home(articulation, cfg.q0)
    A, _ = sampler.sample()
    A = np.asarray(A, dtype=float)

    # --- 由 A 推算 B，并做可达性检查 ---
    u = np.asarray(cfg.travel_dir, dtype=float)
    u = u / np.linalg.norm(u)
    B = A + cfg.d_AB * u

    robot_pos, robot_ori = articulation.get_world_poses()  # API-VERIFIED
    base = np.asarray(robot_pos.numpy(), dtype=float).reshape(-1, 3)[0]
    reach = float(np.linalg.norm(B - base))
    if reach > cfg.reach_limit:
        raise SystemExit(
            f"目标 B 距基座 {reach:.3f} m，超过可达上限 {cfg.reach_limit:.3f} m。\n"
            f"请在 motion_safety/config.py 中下调 d_AB（当前 {cfg.d_AB} m）。"
        )

    # --- Hazard：静态碰撞体，两个条件下都存在 ---
    capsule = build_hazard(A, B, cfg.hazard)

    # Capsule.heights 语义 = 圆柱段长度（不含两端半球），已实测确认
    # （见 task-6-report.md）：heights=1.0 时局部 extent 沿轴总跨度为
    # 1.16 = heights + 2*radius。故此处直接传 seg_b.z - seg_a.z（不再
    # 像 Cylinder 方案那样额外 + 2*radius），几何图元与 build_hazard()
    # 的胶囊数学定义完全吻合。
    cylinder_length = float(capsule.seg_b[2] - capsule.seg_a[2])  # = axis_z_top - axis_z_bottom
    center = [
        float(capsule.seg_a[0]),
        float(capsule.seg_a[1]),
        float(0.5 * (capsule.seg_a[2] + capsule.seg_b[2])),
    ]
    IsaacCapsule(
        HAZARD_PRIM_PATH,
        radii=capsule.radius,
        heights=cylinder_length,
        axes="Z",
        positions=center,
    )  # API-VERIFIED
    GeomPrim(HAZARD_PRIM_PATH, apply_collision_apis=True)  # API-VERIFIED

    # hazard 必须带 UsdPhysics.CollisionAPI —— WorldBinding.initialize() 会检查
    # tracked_prims 是否具备该 API，否则 aware 组注册不上。但"人"的代理不应是一堵
    # 让机械臂物理顶住的墙：实测（见 task-9-report.md）blind 组机械臂会直接撞上胶囊
    # 并被卡死，关节指令与实际值稳态偏差达 0.99 rad，任务永远无法完成，min_dist 记录
    # 的是"卡住时的距离"而非"扫过时的最近距离"，度量口径被破坏。
    # 因此用 UsdPhysics.FilteredPairsAPI 过滤 hazard 与机器人之间的接触：
    # 规划器世界模型照常看到它（aware 组据此避障），物理引擎则不产生接触力。
    # 该过滤在两个条件下**无条件**施加，故不引入新的条件分叉。
    #
    # 注（Task 9 复审重跑实测）：在**当前**外侧摆放（hazard.side = -1）下这行其实是
    # 空操作——手臂全程最近只到胶囊表面外 0.0427 m，从不发生接触，去掉它两组轨迹
    # 几乎逐帧重合。它是在把 hazard 移到外侧**之前**必需的。保留作为廉价的度量卫生：
    # 若将来调整 hazard 摆放 / q0 / d_AB 使手臂重新可能接触，缺了它会再次出现
    # "min_dist 记录的是卡住时的距离"这种隐晦的口径破坏。
    # 判别证据：scripts/diagnose_contact_jam.py --both --steps 300（默认 --side 1）。
    #
    # filter target 取的是 articulation 根路径，依赖 PhysX 把根 prim 上的过滤关系
    # 传播到全部子连杆 collider。实测有效，但这是未记录的隐含 API 语义，
    # 风险与更保守的写法见 docs/api-findings.md「Task 9 补充」。
    _filter_collision_pair(HAZARD_PRIM_PATH, ROBOT_PRIM_PATH)

    geometry_note = (
        "视觉/碰撞图元使用 isaacsim.core.experimental.objects.Capsule，"
        "轴线段与半径同 build_hazard() 返回的 Capsule 数学定义完全一致"
        "（heights 语义为圆柱段长度、不含两端半球，已实测确认）；"
        "ObstacleStrategy 对 Capsule 类型的默认 representation 就是 "
        "ObstacleRepresentation.CAPSULE（非 OBB 近似，见 obstacle_strategy.py "
        "源码），本函数只调用 set_default_safety_tolerance 追加安全余量、"
        "未覆盖 representation，故 aware 组规划器看到的是与真实几何一致的"
        "精确胶囊 + planner_padding 安全缓冲，不存在图元近似误差。"
    )

    # --- 规划器世界：仅 aware 条件注册 hazard ---
    obstacle_strategy = mg.ObstacleStrategy()  # API-VERIFIED
    obstacle_strategy.set_default_safety_tolerance(cfg.planner_padding)  # API-VERIFIED

    tracked_prims = [HAZARD_PRIM_PATH] if condition == "aware" else []

    world_binding = mg.WorldBinding(  # API-VERIFIED
        world_interface=CumotionWorldInterface(),
        obstacle_strategy=obstacle_strategy,
        tracked_prims=tracked_prims,
        tracked_collision_api=mg.TrackableApi.PHYSICS_COLLISION,
    )
    world_binding.initialize()  # API-VERIFIED
    world_binding.get_world_interface().update_world_to_robot_root_transforms(
        poses=(robot_pos, robot_ori)
    )  # API-VERIFIED
    world_binding.synchronize_transforms()  # API-VERIFIED

    controller = RmpFlowController(  # API-VERIFIED
        cumotion_robot=cumotion_robot,
        cumotion_world_interface=world_binding.get_world_interface(),
        robot_joint_space=articulation.dof_names,
        robot_site_space=site_space,
        tool_frame=tool_frame,
    )

    return SceneHandles(
        articulation=articulation,
        controller=controller,
        cumotion_robot=cumotion_robot,
        world_binding=world_binding,
        sampler=sampler,
        capsule=capsule,
        A=A,
        B=B,
        tool_frame=tool_frame,
        site_space=site_space,
        hazard_prim_path=HAZARD_PRIM_PATH,
        geometry_note=geometry_note,
    )


def _filter_collision_pair(prim_path: str, other_path: str) -> None:
    """在 prim_path 上施加 UsdPhysics.FilteredPairsAPI，过滤掉与 other_path 的接触。

    FilteredPairsAPI 的语义是"这两者之间不产生碰撞响应"，但 CollisionAPI 仍然存在，
    故 WorldBinding 对 tracked_prims 的 collision API 检查照常通过。
    """
    import isaacsim.core.experimental.utils.stage as stage_utils
    from pxr import UsdPhysics

    stage = stage_utils.get_current_stage()
    prim = stage.GetPrimAtPath(prim_path)
    if not prim.IsValid():
        raise RuntimeError(f"施加碰撞过滤失败：{prim_path} 不是有效 prim")
    filtered = UsdPhysics.FilteredPairsAPI.Apply(prim)
    filtered.CreateFilteredPairsRel().AddTarget(other_path)


def reset_to_home(articulation, q0) -> None:
    """把关节设为固定初始构型 q0（取自 `ExperimentConfig.q0`，Franka 默认 home 附近）。

    `q0` 由调用方传入（来自 `cfg.q0`），本函数不再自行硬编码数值——否则该常量会
    同时逃逸 config 快照（`run_episode.py` 写出的 JSON）与 `analyze.py` 的失配
    检测（复审 Important I1）。

    `set_dof_positions()` 要求时间线已 play()，否则抛 AssertionError（见
    docs/api-findings.md）。这里按已实测验证的顺序：若时间线尚未播放，
    先 play() 再 update_app() 一次使物理张量视图就绪；设置完关节角后
    再 update_app() 一次，使后续读取（连杆位姿、dof 位置）能看到新值。
    """
    import isaacsim.core.experimental.utils.app as app_utils

    if not app_utils.is_playing():  # API-VERIFIED
        app_utils.play()  # API-VERIFIED
        app_utils.update_app()  # API-VERIFIED

    q0 = np.asarray(q0, dtype=float)
    n_dof = len(articulation.dof_names)
    if n_dof > len(q0):  # 含夹爪自由度时补 0
        q0 = np.concatenate([q0, np.zeros(n_dof - len(q0))])
    articulation.set_dof_positions(q0[:n_dof].reshape(1, -1))  # API-VERIFIED
    app_utils.update_app()  # API-VERIFIED：需 update 才能读到新值


# cumotion 的 tool_frame 未必是刚体连杆。Franka 的 tool_frame 为
# `panda_leftfingertip`，在 robot_configurations/franka/robot.urdf 中是挂在刚体
# `panda_leftfinger` 上的 fixed joint，origin xyz = (0, 0, 0.045)、无平移以外的
# 偏置。此表把"cumotion 控制的 tool_frame"映射到"(可用 RigidPrim 读到的刚体连杆,
# 局部偏移)"，使度量端与控制端指向同一个物理点。
_TOOL_FRAME_TO_LINK = {
    "panda_leftfingertip": ("panda_leftfinger", (0.0, 0.0, 0.045)),
    "panda_rightfingertip": ("panda_rightfinger", (0.0, 0.0, 0.045)),
}


def _resolve_tool_frame(articulation, tool_frame: str):
    """把 cumotion tool_frame 映射为 (刚体连杆名, 局部偏移)。

    返回的连杆必须存在于 `articulation.link_names` 中（RigidPrim 才读得到）。
    若 tool_frame 本身就是刚体连杆则偏移为零。
    """
    link_names = list(articulation.link_names)  # API-VERIFIED
    if tool_frame in link_names:
        return tool_frame, (0.0, 0.0, 0.0)
    if tool_frame in _TOOL_FRAME_TO_LINK:
        link, offset = _TOOL_FRAME_TO_LINK[tool_frame]
        if link in link_names:
            return link, offset
    raise RuntimeError(
        f"无法把 cumotion tool_frame {tool_frame!r} 映射到刚体连杆。"
        f"可用连杆：{link_names}。请在 _TOOL_FRAME_TO_LINK 中补充映射——"
        f"绝不能退化到任意连杆，否则目标 B 与实测末端不是同一个点。"
    )
