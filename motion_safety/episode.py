"""单 episode 主循环：复位 -> 驱动到 B -> 逐帧记录。依赖 Isaac。"""

import numpy as np

from .config import ExperimentConfig
from .metrics import summarize
from .scene import build_scene, reset_to_home


def _make_states(mg, handles, articulation, wp):
    """构造 RMPflow 需要的 (估计状态, 目标状态)。"""
    names = articulation.dof_names
    estimated = mg.RobotState(
        joints=mg.JointState.from_name(
            robot_joint_space=names,
            positions=(names, articulation.get_dof_positions()),
            velocities=(names, articulation.get_dof_velocities()),
        )
    )
    target_positions = wp.array(
        [handles.B.tolist()], dtype=wp.float32, device="cpu"
    )
    # 只给位置、不给朝向 —— 任务定义是"末端从 A 平移到 B"，朝向从来不是本
    # benchmark 的约束。若同时下达朝向 attractor，RMPflow 需同时满足位置与
    # 朝向，实测会收敛到"朝向满足、位置错误"的位姿而停滞（见 task-9-report.md
    # 的诊断记录）。RmpFlowController._tool_orientation_from_robot_state() 在
    # tool_frame 不在 sites.orientation_names 中时返回 None，forward() 便不会
    # 调用 set_end_effector_orientation_attractor；reset() 又会先
    # clear_end_effector_orientation_attractor()，故此处省略 orientations 即为
    # 纯位置约束（源码：isaacsim/robot_motion/cumotion/impl/rmp_flow_controller.py）。
    # 注：曾试过在 setpoint 里附带"当前关节角"以中和 reset() 钉在 q0 上的 cspace
    # attractor，假设它与避障斥力叠加造成局部极小。实测该假设不成立（aware 组终点
    # 距 B 由 0.1907 变为 0.1919，无改善），故不采用，保持 setpoint 只含位置。
    setpoint = mg.RobotState(
        sites=mg.SpatialState.from_name(
            spatial_space=handles.site_space,
            positions=([handles.tool_frame], target_positions),
        )
    )
    return estimated, setpoint


def run_episode(cfg: ExperimentConfig, condition: str, n_steps: int, simulation_app):
    """跑一个 episode，返回 (逐帧记录, 汇总, 元信息)。"""
    import isaacsim.core.experimental.utils.app as app_utils
    import isaacsim.robot_motion.experimental.motion_generation as mg
    import warp as wp
    from isaacsim.core.simulation_manager import SimulationManager

    SimulationManager.setup_simulation(dt=cfg.dt, device="cuda")
    handles = build_scene(cfg, condition)
    simulation_app.update()

    app_utils.play()
    simulation_app.update()

    articulation = handles.articulation
    reset_to_home(articulation, cfg.q0)
    simulation_app.update()

    estimated, setpoint = _make_states(mg, handles, articulation, wp)
    if not handles.controller.reset(estimated, setpoint, t=0.0):
        raise RuntimeError("RmpFlowController reset 失败")

    records = []
    t = 0.0
    for step in range(n_steps):
        simulation_app.update()

        handles.world_binding.get_world_interface().update_world_to_robot_root_transforms(
            articulation.get_world_poses()
        )
        handles.world_binding.synchronize_transforms()

        estimated, setpoint = _make_states(mg, handles, articulation, wp)
        desired = handles.controller.forward(estimated, setpoint, t)
        if desired is not None and desired.joints.positions is not None:
            articulation.set_dof_position_targets(
                positions=desired.joints.positions,
                dof_indices=desired.joints.position_indices,
            )

        ee_pos, arm_pts = handles.sampler.sample()
        d_ee = float(handles.capsule.distance_to_surface(ee_pos.reshape(1, 3))[0])
        d_arm = float(handles.capsule.distance_to_surface(arm_pts).min())

        records.append(
            {
                "step": step,
                "t": t,
                "ee_x": float(ee_pos[0]),
                "ee_y": float(ee_pos[1]),
                "ee_z": float(ee_pos[2]),
                "d_ee": d_ee,
                "d_arm": d_arm,
                "contact": int(d_arm <= 0.0),
            }
        )
        t += cfg.dt

    # 传入**逐帧**末端轨迹（而非只传末帧位置）：success 判据为"全程是否曾进入容差"，
    # 且安全指标只在 [0, arrival_step] 的任务执行窗口内统计，二者都需要完整轨迹。
    ee_traj = np.array(
        [[r["ee_x"], r["ee_y"], r["ee_z"]] for r in records], dtype=float
    )
    summary = summarize(
        d_ee=[r["d_ee"] for r in records],
        d_arm=[r["d_arm"] for r in records],
        ee_traj=ee_traj,
        goal_B=handles.B,
        risk_radius=cfg.risk_radius,
        dt=cfg.dt,
        success_tol=cfg.success_tol,
    )

    meta = {
        "A": handles.A.tolist(),
        "goal_B": handles.B.tolist(),
        "capsule": handles.capsule.to_dict(),
        "geometry_note": handles.geometry_note,
        "hazard_registered_with_planner": condition == "aware",
    }
    return records, summary, meta
