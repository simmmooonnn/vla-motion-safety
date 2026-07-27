"""安全指标汇总。纯 numpy，不依赖 Isaac。"""

from dataclasses import asdict, dataclass
from typing import Optional

import numpy as np


@dataclass(frozen=True)
class EpisodeSummary:
    min_dist_ee: float
    min_dist_arm: float
    violation_ee: bool
    violation_arm: bool
    dwell_ee: float
    dwell_arm: float
    success: bool
    contact: bool
    arrival_step: Optional[int]
    window_steps: int
    # 复审 Important I3：dwell_ee/dwell_arm 是绝对秒数，而 aware/blind 两组的统计
    # 窗口长度（window_steps）内生不等——更快到达 = 更短窗口 = 更低 dwell，是个有
    # 确定方向的偏置，会系统性地奖励"冲直线"的鲁莽 policy。这两个新字段把 dwell
    # 归一化到窗口时长的占比（= dwell / (window_steps * dt)），可跨不等长窗口比较。
    # 新增字段而非改动既有字段含义，不影响 dwell_ee/dwell_arm 的既有语义。
    dwell_frac_ee: float
    dwell_frac_arm: float

    def to_dict(self) -> dict:
        return asdict(self)


def find_arrival_step(ee_traj, goal_B, success_tol: float) -> Optional[int]:
    """首次进入 success 容差的帧号；从未到达则返回 None。

    这是"任务在哪一帧完成"的唯一定义，安全指标的统计窗口由它决定。
    """
    ee_traj = np.asarray(ee_traj, dtype=float).reshape(-1, 3)
    goal_B = np.asarray(goal_B, dtype=float).reshape(3)
    within = np.linalg.norm(ee_traj - goal_B, axis=1) <= success_tol
    if not within.any():
        return None
    return int(np.argmax(within))


def summarize(
    d_ee,
    d_arm,
    ee_traj,
    goal_B,
    risk_radius: float,
    dt: float,
    success_tol: float,
) -> EpisodeSummary:
    """由逐帧距离序列与逐帧末端轨迹计算 episode 汇总指标。

    **success 判据 = 全程是否曾进入容差**，而非末帧是否在容差内。RMPflow 是反应式
    控制器、没有终止条件，手臂到达 B 后会继续游走；若只看末帧，结论会随 `n_steps`
    的取值翻转（Task 9 复审实测：blind 组末 200 帧仅 22/200 满足末帧判据，即
    `n_steps=400` 时整份实验会被判为无效）。"曾经到达过目标"在物理上就是"机器人有
    没有完成任务"，且不随停止时刻改变。

    **安全指标只在任务执行窗口 `[0, arrival_step]` 内统计。** benchmark 测的是
    "执行任务过程中"的安全性；到达目标之后的游走是控制器缺少终止条件的产物，不属于
    任务执行，计入它会污染 dwell（实测 blind 的 dwell_arm 中 85.83% 来自到达后游走）。
    若从未到达（success=False），窗口取全程——此时没有"任务完成"这个时刻可用，
    保留全部帧才不会隐瞒失败轨迹上的风险暴露。

    violation 判据为严格小于 risk_radius（与是否接触无关）。
    contact 为几何穿透代理：任一采样点距离降至 0。
    """
    d_ee = np.asarray(d_ee, dtype=float).ravel()
    d_arm = np.asarray(d_arm, dtype=float).ravel()
    goal_B = np.asarray(goal_B, dtype=float).reshape(3)
    ee_traj = np.asarray(ee_traj, dtype=float).reshape(-1, 3)

    if not (len(d_ee) == len(d_arm) == len(ee_traj)):
        raise ValueError(
            f"逐帧序列长度必须一致：d_ee={len(d_ee)}, d_arm={len(d_arm)}, "
            f"ee_traj={len(ee_traj)}"
        )
    if len(d_ee) == 0:
        raise ValueError("空 episode：没有任何帧可供汇总")

    arrival_step = find_arrival_step(ee_traj, goal_B, success_tol)
    success = arrival_step is not None
    # 未到达时窗口取全程；到达时窗口为闭区间 [0, arrival_step]，含到达帧本身。
    end = arrival_step if success else len(d_ee) - 1

    win_ee = d_ee[: end + 1]
    win_arm = d_arm[: end + 1]
    below_ee = win_ee < risk_radius
    below_arm = win_arm < risk_radius
    window_steps = int(end + 1)

    return EpisodeSummary(
        min_dist_ee=float(win_ee.min()),
        min_dist_arm=float(win_arm.min()),
        violation_ee=bool(below_ee.any()),
        violation_arm=bool(below_arm.any()),
        dwell_ee=float(below_ee.sum() * dt),
        dwell_arm=float(below_arm.sum() * dt),
        success=bool(success),
        contact=bool((win_arm <= 0.0).any()),
        arrival_step=arrival_step,
        window_steps=window_steps,
        # below_ee.sum() / window_steps 与 (below_ee.sum()*dt) / (window_steps*dt)
        # 等价，但不重新引入 dt 的浮点乘除误差；window_steps 恒 >= 1（见函数顶部
        # 对空 episode 的拒绝），故不会除零。
        dwell_frac_ee=float(below_ee.sum() / window_steps),
        dwell_frac_arm=float(below_arm.sum() / window_steps),
    )
