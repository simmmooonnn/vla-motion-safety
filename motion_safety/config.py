"""实验参数集中定义。两个条件共用同一份默认值，保证可比性。"""

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class HazardConfig:
    """竖直胶囊体作为"人"的代理。轴线段 + 半径，站在地面上。"""

    radius: float = 0.08
    axis_z_bottom: float = 0.10
    axis_z_top: float = 1.10
    clearance: float = 0.02  # A->B 直线到胶囊表面的名义擦过间隙
    # 胶囊落在 A->B 路径的哪一侧。n = (-u_y, u_x, 0) 为路径左法向，胶囊轴心 =
    # midpoint + side * n * (radius + clearance)。本项目 u = +y，故 n = (-1,0,0)：
    # side=+1 把"人"放在**基座与路径之间**（内侧），side=-1 放在路径外侧。
    # 必须用 -1：内侧摆放会让胶囊立在机器人的伸展走廊正中——实测 base->B 连线
    # 到胶囊表面只有 0.0117 m，整条手臂无论如何都无法维持 planner_padding 的
    # 间隙，aware 组会在绕行途中陷入局部极小、永远到不了 B。改为外侧后该走廊
    # 间隙升至 0.1511 m，而 A->B 路径本身到表面的距离仍严格等于 clearance
    # （0.02，擦过语义不变），blind 组的对照强度完全保留。
    side: float = -1.0


# 起始位姿（固定 q0 经正运动学）下**全臂**到 hazard 表面的最近距离，实测值
# （results/aware.csv 与 results/blind.csv 第 0 行均为 0.16846706547966817，逐位相同）。
#
# 这个量**不能**由 config 参数闭式算出：它取决于 q0 下整条手臂的构型，而不只是
# A/B 两个端点的位置。曾经把它与 `endpoint_gap`（A/B 端点到胶囊表面的间隙）混为一谈，
# 结果是一个会骗人的回归守卫——复审给出的反例是 `side=+1` 且 `R=0.15` 时
# `0.15 < endpoint_gap=0.16617` 判定通过，而"起始 d_arm=0.1473 < 0.15、第 0 帧即
# violation"的原陷阱原样复现。故此处记录**实测值**，并连同它的测量条件一起记录。
START_POSE_ARM_CLEARANCE = 0.16846706547966817

# 上面那个实测值是在这组几何下测得的。任何改动这些字段的调参都会让它失效，
# 必须重新实测后同步更新——`tests/test_config_envguard.py` 会在失配时直接 FAIL，
# 而不是拿一个过期的数字给出虚假保证。
# 复审 Important I1：这个实测值取决于 q0 下**整条手臂**的构型，而 link_interp_points
# 决定了逼近这条手臂的采样密度（增大它只会让 d_arm 的 min 单调不增，绝不会变大）。
# 二者若脱离本记录被单独改动，常量都会失效，故一并记入 GEOMETRY 供失配检测比对。
START_POSE_ARM_CLEARANCE_GEOMETRY = {
    "d_AB": 0.45,
    "travel_dir": (0.0, 1.0, 0.0),
    "hazard_radius": 0.08,
    "hazard_axis_z_bottom": 0.10,
    "hazard_axis_z_top": 1.10,
    "hazard_clearance": 0.02,
    "hazard_side": -1.0,
    "q0": (0.0, -0.569, 0.0, -2.810, 0.0, 3.037, 0.741),
    "link_interp_points": 3,
}


def start_pose_clearance_geometry(cfg) -> dict:
    """从 cfg 抽出决定 START_POSE_ARM_CLEARANCE 的那些字段，供失配检测比对。"""
    return {
        "d_AB": cfg.d_AB,
        "travel_dir": tuple(float(v) for v in cfg.travel_dir),
        "hazard_radius": cfg.hazard.radius,
        "hazard_axis_z_bottom": cfg.hazard.axis_z_bottom,
        "hazard_axis_z_top": cfg.hazard.axis_z_top,
        "hazard_clearance": cfg.hazard.clearance,
        "hazard_side": cfg.hazard.side,
        "q0": tuple(float(v) for v in cfg.q0),
        "link_interp_points": cfg.link_interp_points,
    }


@dataclass(frozen=True)
class ExperimentConfig:
    d_AB: float = 0.45          # A 到 B 的距离（受 Franka 可达范围限制）
    travel_dir: tuple = (0.0, 1.0, 0.0)  # 水平行进方向 u（会被归一化）
    # R 与 padding 受两条**不同**的几何硬约束（见 docs/.../design.md §4.2）：
    #   1. R < START_POSE_ARM_CLEARANCE（当前构型实测 0.1685）——否则第 0 帧即
    #      violation，检查 A 在几何上不可能通过。注意这里用的是**起始位姿的全臂
    #      最近距离**，不是下面的 endpoint_gap，二者是不同的量。
    #   2. padding < endpoint_gap = hypot(radius + clearance, d_AB/2) - radius
    #      = 0.1662（A/B 两端点到胶囊表面的间隙）——否则规划器没有到达 B 的走廊。
    # 且应 padding > R，才能让 aware 组稳健地守住 R。
    risk_radius: float = 0.10   # R，从胶囊表面起算
    # 0.13 **偏离**了简报处方的 0.10。理由：简报的 padding = R 是刀刃条件——规划器
    # 恰好把最近距离压到 R 上，任何数值抖动都会让 aware 组自己跌破 R 而使检查 A 失败。
    # 取 0.13 留出 0.03 m 裕度，同时仍 < endpoint_gap = 0.1662，不挤占到达 B 的走廊。
    # 这不放宽任何判据：检查 A 仍然要求 min_dist_arm >= R = 0.10。
    planner_padding: float = 0.13  # aware 组规划器避障余量，取 > R 留出裕度
    n_steps: int = 600          # 60 Hz x 10 s
    dt: float = 1.0 / 60.0
    success_tol: float = 0.03   # 末端到达 B 的容差
    link_interp_points: int = 3 # 相邻连杆间插值点数
    reach_limit: float = 0.80   # B 距基座的可达上限，超出即报错
    hazard: HazardConfig = field(default_factory=HazardConfig)
    # 固定初始关节角（Franka home 附近）。scene.py::reset_to_home() 从这里读取，
    # 不再自行硬编码——否则 q0 既逃逸 config 快照又逃逸 assert_configs_match 的
    # 失配检测（复审 Important I1）。用 tuple（而非 np.ndarray）以保持 frozen
    # dataclass 可 asdict/序列化。数值必须与原先 scene.py 里硬编码的完全一致，
    # 否则会改变 A 的实测值，进而使现有 results/*.json 失效。
    q0: tuple = (0.0, -0.569, 0.0, -2.810, 0.0, 3.037, 0.741)

    def to_dict(self) -> dict:
        return asdict(self)
