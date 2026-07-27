import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from motion_safety.metrics import EpisodeSummary, find_arrival_step, summarize

DT = 1.0 / 60.0
R = 0.15
TOL = 0.03
GOAL = np.array([0.31, 0.225, 0.49])
FAR = GOAL + np.array([0.5, 0.0, 0.0])  # 远在容差之外


def traj(n, arrive_at=None):
    """构造 n 帧末端轨迹：arrive_at 之前都远离 GOAL，之后停在 GOAL。

    arrive_at=None 表示从未到达。默认让"到达"发生在最后一帧，使统计窗口等于全程，
    这样那些只关心距离序列的用例可以沿用直观的期望值。
    """
    pts = np.tile(FAR, (n, 1))
    if arrive_at is not None:
        pts[arrive_at:] = GOAL
    return pts


def test_dwell_counts_frames_below_radius():
    # 100 帧，其中恰好 6 帧低于 R -> dwell = 6/60 = 0.1 s
    d = np.full(100, 0.30)
    d[10:16] = 0.05
    s = summarize(d, d, traj(100, arrive_at=99), GOAL, R, DT, TOL)
    assert abs(s.dwell_ee - 0.1) < 1e-12, s.dwell_ee


# --- 复审 Important I3：dwell_frac 归一化，可跨不等长窗口比较 ---


def test_dwell_frac_is_dwell_divided_by_window_duration():
    """dwell_frac = dwell / (window_steps * dt)，即窗口内低于 R 的帧占比。"""
    d = np.full(100, 0.30)
    d[10:16] = 0.05  # 6/100 帧低于 R
    s = summarize(d, d, traj(100, arrive_at=99), GOAL, R, DT, TOL)
    assert s.window_steps == 100
    assert abs(s.dwell_frac_ee - 0.06) < 1e-12, s.dwell_frac_ee
    assert abs(s.dwell_frac_ee - s.dwell_ee / (s.window_steps * DT)) < 1e-9


def test_dwell_frac_is_zero_when_never_below_radius():
    d = np.full(4, 0.4)
    s = summarize(d, d, traj(4, arrive_at=3), GOAL, R, DT, TOL)
    assert s.dwell_frac_ee == 0.0
    assert s.dwell_frac_arm == 0.0


def test_dwell_frac_exposes_unequal_window_bias():
    """核心动机：同样的绝对 dwell，窗口越短 dwell_frac 越大——这正是复审指出的、

    绝对秒数 dwell 会系统性偏袒"冲直线"policy 的那条偏置，dwell_frac 把它显性化。
    """
    d_short = np.full(20, 0.4)
    d_short[0] = 0.05
    s_short = summarize(d_short, d_short, traj(20, arrive_at=19), GOAL, R, DT, TOL)

    d_long = np.full(200, 0.4)
    d_long[0] = 0.05
    s_long = summarize(d_long, d_long, traj(200, arrive_at=199), GOAL, R, DT, TOL)

    # 两条轨迹的绝对 dwell 相同（都只有 1 帧违规）
    assert s_short.dwell_ee == s_long.dwell_ee
    # 但归一化后，窗口更短的那条 dwell_frac 更大——暴露了绝对 dwell 的偏置方向
    assert s_short.dwell_frac_ee > s_long.dwell_frac_ee


def test_min_dist_and_violation_true():
    d = np.array([0.4, 0.2, 0.05, 0.3])
    s = summarize(d, d, traj(4, arrive_at=3), GOAL, R, DT, TOL)
    assert abs(s.min_dist_ee - 0.05) < 1e-12
    assert s.violation_ee is True


def test_no_violation_when_always_above_radius():
    d = np.array([0.4, 0.2, 0.16, 0.3])
    s = summarize(d, d, traj(4, arrive_at=3), GOAL, R, DT, TOL)
    assert s.violation_ee is False
    assert s.dwell_ee == 0.0


def test_boundary_exactly_at_radius_is_not_violation():
    # 判据为严格小于 R
    d = np.array([R, R, R])
    s = summarize(d, d, traj(3, arrive_at=2), GOAL, R, DT, TOL)
    assert s.violation_ee is False


def test_contact_when_arm_distance_reaches_zero():
    d_ee = np.array([0.4, 0.3])
    d_arm = np.array([0.4, 0.0])
    s = summarize(d_ee, d_arm, traj(2, arrive_at=1), GOAL, R, DT, TOL)
    assert s.contact is True


def test_no_contact_when_arm_stays_positive():
    d = np.array([0.4, 0.01])
    s = summarize(d, d, traj(2, arrive_at=1), GOAL, R, DT, TOL)
    assert s.contact is False


def test_ee_and_arm_tracked_separately():
    d_ee = np.array([0.40, 0.35])
    d_arm = np.array([0.40, 0.02])
    s = summarize(d_ee, d_arm, traj(2, arrive_at=1), GOAL, R, DT, TOL)
    assert s.violation_ee is False
    assert s.violation_arm is True
    assert abs(s.min_dist_arm - 0.02) < 1e-12


# --- success 判据：全程曾到达，而非末帧在容差内 ---


def test_success_when_within_tolerance_at_some_frame():
    d = np.full(5, 0.4)
    s = summarize(d, d, traj(5, arrive_at=2), GOAL, R, DT, TOL)
    assert s.success is True
    assert s.arrival_step == 2


def test_success_true_even_when_final_frame_drifts_away():
    """到达 B 之后又游走出容差，仍算完成任务。

    这正是复审发现的不稳健点：旧判据只看末帧，blind 组末 200 帧仅 22/200 满足，
    n_steps 取 400 或 500 会让同一条轨迹的 success 翻转。
    """
    d = np.full(6, 0.4)
    pts = np.tile(FAR, (6, 1))
    pts[2] = GOAL          # 曾经到达
    pts[3:] = FAR          # 之后游走走远，末帧不在容差内
    s = summarize(d, d, pts, GOAL, R, DT, TOL)
    assert s.success is True
    assert s.arrival_step == 2


def test_success_is_invariant_to_where_the_episode_is_cut():
    """同一条轨迹，截到不同步数，success 与窗口内安全指标必须完全一致。"""
    d = np.concatenate([np.full(3, 0.05), np.full(97, 0.4)])
    pts = np.tile(FAR, (100, 1))
    pts[10] = GOAL
    pts[11:] = FAR  # 到达后游走
    full = summarize(d, d, pts, GOAL, R, DT, TOL)
    cut = summarize(d[:40], d[:40], pts[:40], GOAL, R, DT, TOL)
    assert full.success == cut.success is True
    assert full.arrival_step == cut.arrival_step == 10
    assert full.min_dist_arm == cut.min_dist_arm
    assert full.dwell_arm == cut.dwell_arm
    assert full.violation_arm == cut.violation_arm


def test_arrival_step_is_first_entry_not_closest_frame():
    d = np.full(5, 0.4)
    pts = np.tile(FAR, (5, 1))
    pts[1] = GOAL + np.array([0.0, 0.0, 0.02])  # 进入容差但不是最近
    pts[3] = GOAL                               # 最近，但更晚
    s = summarize(d, d, pts, GOAL, R, DT, TOL)
    assert s.arrival_step == 1


def test_failure_when_never_within_tolerance():
    d = np.full(4, 0.4)
    s = summarize(d, d, traj(4, arrive_at=None), GOAL, R, DT, TOL)
    assert s.success is False
    assert s.arrival_step is None


# --- 安全指标只在任务执行窗口 [0, arrival_step] 内统计 ---


def test_metrics_ignore_frames_after_arrival():
    """到达之后的游走不计入任何安全指标。"""
    d = np.full(10, 0.40)
    d[2] = 0.05   # 到达前的闯入 -> 必须计入
    d[7] = 0.01   # 到达后的游走 -> 必须忽略
    d[8] = 0.0    # 到达后的穿透 -> 必须忽略
    s = summarize(d, d, traj(10, arrive_at=4), GOAL, R, DT, TOL)
    assert s.arrival_step == 4
    assert s.window_steps == 5
    assert abs(s.min_dist_arm - 0.05) < 1e-12
    assert abs(s.dwell_arm - DT) < 1e-12  # 只有 1 帧低于 R
    assert s.violation_arm is True
    assert s.contact is False


def test_window_includes_the_arrival_frame_itself():
    d = np.full(5, 0.40)
    d[3] = 0.02  # 恰好落在到达帧上
    s = summarize(d, d, traj(5, arrive_at=3), GOAL, R, DT, TOL)
    assert s.window_steps == 4
    assert abs(s.min_dist_arm - 0.02) < 1e-12


def test_window_is_full_episode_when_never_arrived():
    """从未到达时窗口取全程——不能因为任务失败就隐瞒风险暴露。"""
    d = np.full(10, 0.40)
    d[7] = 0.03
    d[9] = 0.0
    s = summarize(d, d, traj(10, arrive_at=None), GOAL, R, DT, TOL)
    assert s.success is False
    assert s.arrival_step is None
    assert s.window_steps == 10
    assert abs(s.min_dist_arm - 0.0) < 1e-12
    assert s.violation_arm is True
    assert s.contact is True
    assert abs(s.dwell_arm - 2 * DT) < 1e-12


def test_arrival_at_frame_zero_gives_single_frame_window():
    d = np.array([0.40, 0.01, 0.01])
    s = summarize(d, d, traj(3, arrive_at=0), GOAL, R, DT, TOL)
    assert s.arrival_step == 0
    assert s.window_steps == 1
    assert abs(s.min_dist_arm - 0.40) < 1e-12
    assert s.violation_arm is False


# --- find_arrival_step 直测 ---


def test_find_arrival_step_returns_none_when_never_within():
    assert find_arrival_step(traj(5, arrive_at=None), GOAL, TOL) is None


def test_find_arrival_step_boundary_is_inclusive():
    """恰好等于容差算作到达（判据为 <=）。

    目标取原点、偏移只落在一个轴上，使 `|p - goal|` 恰好是可精确表示的 TOL；
    若用 GOAL 加偏移，浮点舍入会让差值变成 0.030000000000000027 而越过边界，
    那测的就是浮点误差而不是判据的开闭。
    """
    origin = np.zeros(3)
    pts = np.tile(np.array([0.0, 0.0, 1.0]), (3, 1))
    pts[1] = np.array([0.0, 0.0, TOL])
    assert find_arrival_step(pts, origin, TOL) == 1
    # 略微超出容差则不算到达
    pts[1] = np.array([0.0, 0.0, TOL * 1.001])
    assert find_arrival_step(pts, origin, TOL) is None


# --- 其他 ---


def test_mismatched_lengths_are_rejected():
    try:
        summarize(np.full(5, 0.4), np.full(4, 0.4), traj(5, arrive_at=4), GOAL, R, DT, TOL)
    except ValueError:
        return
    raise AssertionError("长度不一致时应抛 ValueError")


def test_to_dict_has_all_fields():
    d = np.array([0.4])
    s = summarize(d, d, traj(1, arrive_at=0), GOAL, R, DT, TOL)
    out = s.to_dict()
    for key in (
        "min_dist_ee", "min_dist_arm", "violation_ee", "violation_arm",
        "dwell_ee", "dwell_arm", "dwell_frac_ee", "dwell_frac_arm",
        "success", "contact", "arrival_step", "window_steps",
    ):
        assert key in out, key
    assert isinstance(out["violation_ee"], bool)
    assert isinstance(out["min_dist_ee"], float)


def main():
    tests = [
        test_dwell_counts_frames_below_radius,
        test_dwell_frac_is_dwell_divided_by_window_duration,
        test_dwell_frac_is_zero_when_never_below_radius,
        test_dwell_frac_exposes_unequal_window_bias,
        test_min_dist_and_violation_true,
        test_no_violation_when_always_above_radius,
        test_boundary_exactly_at_radius_is_not_violation,
        test_contact_when_arm_distance_reaches_zero,
        test_no_contact_when_arm_stays_positive,
        test_ee_and_arm_tracked_separately,
        test_success_when_within_tolerance_at_some_frame,
        test_success_true_even_when_final_frame_drifts_away,
        test_success_is_invariant_to_where_the_episode_is_cut,
        test_arrival_step_is_first_entry_not_closest_frame,
        test_failure_when_never_within_tolerance,
        test_metrics_ignore_frames_after_arrival,
        test_window_includes_the_arrival_frame_itself,
        test_window_is_full_episode_when_never_arrived,
        test_arrival_at_frame_zero_gives_single_frame_window,
        test_find_arrival_step_returns_none_when_never_within,
        test_find_arrival_step_boundary_is_inclusive,
        test_mismatched_lengths_are_rejected,
        test_to_dict_has_all_fields,
    ]
    failed = 0
    for fn in tests:
        try:
            fn()
            print("PASS", fn.__name__)
        except Exception as exc:
            failed += 1
            print("FAIL", fn.__name__, "->", repr(exc))
    print(f"{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
