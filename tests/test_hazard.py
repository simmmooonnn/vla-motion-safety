import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from motion_safety.config import HazardConfig
from motion_safety.hazard import Capsule, build_hazard

SEG_A = np.array([0.0, 0.0, 0.0])
SEG_B = np.array([0.0, 0.0, 1.0])
R = 0.1


def test_point_at_radius_gives_zero():
    cap = Capsule(SEG_A, SEG_B, R)
    pts = np.array([[R, 0.0, 0.5]])
    assert abs(cap.distance_to_surface(pts)[0] - 0.0) < 1e-12


def test_point_at_two_radius_gives_radius():
    cap = Capsule(SEG_A, SEG_B, R)
    pts = np.array([[2 * R, 0.0, 0.5]])
    assert abs(cap.distance_to_surface(pts)[0] - R) < 1e-12


def test_point_inside_clamped_to_zero():
    cap = Capsule(SEG_A, SEG_B, R)
    pts = np.array([[0.5 * R, 0.0, 0.5]])
    assert cap.distance_to_surface(pts)[0] == 0.0


def test_point_beyond_end_cap():
    # 端帽外侧最易写错：轴线段外的点须投影到端点
    cap = Capsule(SEG_A, SEG_B, R)
    pts = np.array([[0.0, 0.0, 1.5]])
    assert abs(cap.distance_to_surface(pts)[0] - (0.5 - R)) < 1e-12


def test_point_beyond_end_cap_diagonal():
    cap = Capsule(SEG_A, SEG_B, R)
    pts = np.array([[0.3, 0.0, 1.4]])  # 到 (0,0,1) 距离 = 0.5
    assert abs(cap.distance_to_surface(pts)[0] - (0.5 - R)) < 1e-12


def test_vectorized_matches_scalar():
    cap = Capsule(SEG_A, SEG_B, R)
    pts = np.array([[R, 0.0, 0.5], [2 * R, 0.0, 0.5], [0.0, 0.0, 1.5]])
    out = cap.distance_to_surface(pts)
    assert out.shape == (3,)
    assert abs(out[0] - 0.0) < 1e-12
    assert abs(out[1] - R) < 1e-12
    assert abs(out[2] - (0.5 - R)) < 1e-12


def test_build_hazard_clearance_is_exact():
    """核心不变量：A->B 直线到胶囊表面的最近距离 == clearance"""
    cfg = HazardConfig()
    A = np.array([0.31, -0.225, 0.49])
    B = np.array([0.31, 0.225, 0.49])
    cap = build_hazard(A, B, cfg)

    ts = np.linspace(0.0, 1.0, 2001)
    line_pts = A + ts[:, None] * (B - A)
    dmin = cap.distance_to_surface(line_pts).min()
    assert abs(dmin - cfg.clearance) < 1e-6, dmin


def test_build_hazard_axis_is_vertical_and_grounded():
    cfg = HazardConfig()
    A = np.array([0.31, -0.225, 0.49])
    B = np.array([0.31, 0.225, 0.49])
    cap = build_hazard(A, B, cfg)
    assert abs(cap.seg_a[0] - cap.seg_b[0]) < 1e-12
    assert abs(cap.seg_a[1] - cap.seg_b[1]) < 1e-12
    assert abs(cap.seg_a[2] - cfg.axis_z_bottom) < 1e-12
    assert abs(cap.seg_b[2] - cfg.axis_z_top) < 1e-12


def test_build_hazard_side_flips_placement_and_preserves_clearance():
    """side 只换边，不改"A->B 直线到表面距离 == clearance"这一不变量。"""
    import dataclasses

    A = np.array([0.31, -0.225, 0.49])
    B = np.array([0.31, 0.225, 0.49])
    inner = build_hazard(A, B, dataclasses.replace(HazardConfig(), side=+1.0))
    outer = build_hazard(A, B, dataclasses.replace(HazardConfig(), side=-1.0))

    mid_x = 0.5 * (A[0] + B[0])
    # 两侧关于 A->B 路径对称
    assert abs((inner.seg_a[0] - mid_x) + (outer.seg_a[0] - mid_x)) < 1e-12
    assert abs(inner.seg_a[0] - outer.seg_a[0]) > 1e-6

    ts = np.linspace(0.0, 1.0, 2001)
    line_pts = A + ts[:, None] * (B - A)
    for cap in (inner, outer):
        dmin = cap.distance_to_surface(line_pts).min()
        assert abs(dmin - HazardConfig().clearance) < 1e-6, dmin


def main():
    tests = [
        test_point_at_radius_gives_zero,
        test_point_at_two_radius_gives_radius,
        test_point_inside_clamped_to_zero,
        test_point_beyond_end_cap,
        test_point_beyond_end_cap_diagonal,
        test_vectorized_matches_scalar,
        test_build_hazard_clearance_is_exact,
        test_build_hazard_axis_is_vertical_and_grounded,
        test_build_hazard_side_flips_placement_and_preserves_clearance,
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
