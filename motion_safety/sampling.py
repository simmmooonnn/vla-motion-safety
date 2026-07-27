"""从机械臂提取用于安全度量的采样点。

纯几何插值与 Isaac 位姿读取分离，前者可独立单测。
"""

import numpy as np


def interpolate_polyline(link_positions: np.ndarray, n_per_segment: int) -> np.ndarray:
    """沿相邻连杆连成的折线插值，近似手臂扫过的体积。

    Args:
        link_positions: 形状 (L, 3)，各连杆原点位置。
        n_per_segment: 每段内部插入的点数（不含端点）。
    Returns:
        形状 (L + (L-1)*n_per_segment, 3) 的点集。
    """
    pts = np.asarray(link_positions, dtype=float).reshape(-1, 3)
    if len(pts) <= 1 or n_per_segment <= 0:
        return pts

    out = [pts[0]]
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        for k in range(1, n_per_segment + 1):
            frac = k / (n_per_segment + 1)
            out.append(a + frac * (b - a))
        out.append(b)
    return np.asarray(out, dtype=float)


def assemble_arm_points(
    link_positions: np.ndarray, ee_pos: np.ndarray, n_per_segment: int
) -> np.ndarray:
    """组装"全臂"采样点集：连杆折线插值点 + tool frame 点。

    把 tool 点并入 `arm_pts` 是有意为之——它是手臂最远端的实体点，理应参与
    "手臂到 hazard 最近距离"的取 min。**其直接后果是 `d_arm <= d_ee` 成为恒等式**
    （arm 点集是 ee 点的超集，取 min 只会更小或相等），这不是巧合或 bug。
    抽成纯函数是为了让这条不变量能脱离 Isaac 单测。
    """
    pts = interpolate_polyline(link_positions, n_per_segment)
    ee_pos = np.asarray(ee_pos, dtype=float).reshape(1, 3)
    return np.vstack([pts, ee_pos])


def rotate_by_quat(quat_wxyz: np.ndarray, vec: np.ndarray) -> np.ndarray:
    """用四元数（wxyz，见 docs/api-findings.md）旋转向量。

    v' = v + 2w(u x v) + 2(u x (u x v))，其中 u = (x, y, z)。
    """
    q = np.asarray(quat_wxyz, dtype=float).reshape(4)
    v = np.asarray(vec, dtype=float).reshape(3)
    w, u = q[0], q[1:]
    t = np.cross(u, v)
    return v + 2.0 * w * t + 2.0 * np.cross(u, t)


class ArmSampler:
    """读取机械臂当前位姿并生成采样点。依赖 Isaac。

    连杆世界位姿读取方式见 docs/api-findings.md："连杆位姿读取方式"一节：
    `Articulation` 没有 `get_link_poses`；须用
    `isaacsim.core.experimental.prims.RigidPrim(paths).get_world_poses()`，
    其中 paths 是各连杆的完整 USD 路径列表，返回顺序与 `articulation.link_names` 一致。
    """

    def __init__(
        self,
        articulation,
        robot_path: str,
        ee_link_name: str,
        n_per_segment: int,
        ee_local_offset=(0.0, 0.0, 0.0),
    ):
        """
        Args:
            articulation: 已初始化的 Articulation 实例。
            robot_path: 机器人在 USD stage 中的根路径（如 "/World/robot"），
                用于拼接各连杆的完整路径 f"{robot_path}/{link_name}"。
            ee_link_name: 末端参考连杆名。**必须与 RMPflow 实际控制的 tool_frame
                对应**，否则"目标 B"与"实测末端"不是同一个点，success 判据会带上
                一个恒定偏置（实测曾因此产生 0.106 m 的系统误差，见 task-9-report.md）。
            n_per_segment: 每段插值点数，来自 ExperimentConfig.link_interp_points。
            ee_local_offset: 在 ee_link 局部坐标系下、从该连杆原点到真正 tool_frame
                的固定平移。Franka 的 cumotion tool_frame 是 `panda_leftfingertip`，
                它在 URDF 中是挂在 `panda_leftfinger` 上的 fixed joint，
                origin xyz = (0, 0, 0.045)（robot_configurations/franka/robot.urdf）。
        """
        # 延迟导入：ArmSampler 依赖 Isaac，避免让纯几何测试间接引入 Isaac 依赖。
        from isaacsim.core.experimental.prims import RigidPrim

        self._art = articulation
        self._n_per_segment = n_per_segment
        self._link_names = list(articulation.link_names)
        if ee_link_name not in self._link_names:
            raise ValueError(
                f"末端连杆 {ee_link_name!r} 不在 link_names 中：{self._link_names}"
            )
        self._ee_index = self._link_names.index(ee_link_name)
        self._ee_local_offset = np.asarray(ee_local_offset, dtype=float).reshape(3)
        link_paths = [f"{robot_path}/{name}" for name in self._link_names]
        self._link_rigid_prim = RigidPrim(link_paths)

    def sample(self):
        """返回 (tool_frame 位置 (3,), 全臂采样点 (M,3))。

        tool_frame 位置 = ee_link 世界位置 + R(ee_link 世界朝向) · ee_local_offset。
        该点同时被追加进 arm_pts —— 它是手臂上最远端的实体点，理应参与
        "手臂到 hazard 最近距离"的取 min。
        """
        positions, orientations = self._link_world_poses()
        ee_pos = positions[self._ee_index] + rotate_by_quat(
            orientations[self._ee_index], self._ee_local_offset
        )
        arm_pts = assemble_arm_points(positions, ee_pos, self._n_per_segment)
        return ee_pos, arm_pts

    def _link_world_poses(self):
        """各连杆世界位姿，返回 (positions (L,3), orientations (L,4) wxyz)。

        使用 RigidPrim.get_world_poses()（见 docs/api-findings.md）。
        """
        positions, orientations = self._link_rigid_prim.get_world_poses()
        if hasattr(positions, "numpy"):
            positions = positions.numpy()
        if hasattr(orientations, "numpy"):
            orientations = orientations.numpy()
        return (
            np.asarray(positions, dtype=float).reshape(-1, 3),
            np.asarray(orientations, dtype=float).reshape(-1, 4),
        )
