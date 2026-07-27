import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from motion_safety.sampling import (
    assemble_arm_points,
    interpolate_polyline,
    rotate_by_quat,
)


def test_includes_all_original_points():
    links = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
    out = interpolate_polyline(links, n_per_segment=0)
    assert out.shape == (3, 3)
    assert np.allclose(out, links)


def test_interpolates_expected_count():
    # L 个连杆 -> L-1 段；每段插入 n 个内点
    links = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
    out = interpolate_polyline(links, n_per_segment=3)
    assert out.shape == (3 + 2 * 3, 3), out.shape


def test_interpolated_points_lie_on_segment():
    links = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
    out = interpolate_polyline(links, n_per_segment=1)
    # 应包含中点
    assert any(np.allclose(p, [0.5, 0.0, 0.0]) for p in out)


def test_single_link_returns_itself():
    links = np.array([[0.3, 0.1, 0.5]])
    out = interpolate_polyline(links, n_per_segment=5)
    assert out.shape == (1, 3)
    assert np.allclose(out[0], [0.3, 0.1, 0.5])


def test_rotate_by_identity_quat_is_noop():
    # wxyz 约定下单位四元数是 [1,0,0,0]（见 docs/api-findings.md）
    v = np.array([0.0, 0.0, 0.045])
    assert np.allclose(rotate_by_quat([1.0, 0.0, 0.0, 0.0], v), v)


def test_rotate_by_quat_180_about_x():
    # 绕 X 轴 180°：wxyz = [0,1,0,0]，把 +z 转成 -z
    out = rotate_by_quat([0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.045])
    assert np.allclose(out, [0.0, 0.0, -0.045], atol=1e-12), out


def test_rotate_by_quat_90_about_z():
    # 绕 Z 轴 90°：wxyz = [cos45, 0, 0, sin45]，把 +x 转成 +y
    s = np.sqrt(0.5)
    out = rotate_by_quat([s, 0.0, 0.0, s], [1.0, 0.0, 0.0])
    assert np.allclose(out, [0.0, 1.0, 0.0], atol=1e-12), out


def test_rotate_by_quat_preserves_length():
    q = np.array([0.5, 0.5, 0.5, 0.5])  # 单位四元数
    v = np.array([0.1, -0.2, 0.3])
    assert abs(np.linalg.norm(rotate_by_quat(q, v)) - np.linalg.norm(v)) < 1e-12


def test_assemble_arm_points_appends_tool_point():
    links = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
    ee = np.array([1.0, 0.0, 0.5])
    out = assemble_arm_points(links, ee, n_per_segment=0)
    assert out.shape == (3, 3)
    assert np.allclose(out[-1], ee)


def test_assemble_arm_points_is_superset_of_polyline():
    links = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]])
    ee = np.array([1.0, 1.0, 0.3])
    base = interpolate_polyline(links, n_per_segment=3)
    out = assemble_arm_points(links, ee, n_per_segment=3)
    assert out.shape[0] == base.shape[0] + 1
    assert np.allclose(out[:-1], base)


def test_arm_min_distance_never_exceeds_ee_distance():
    """d_arm <= d_ee 是恒等式：arm 点集包含 tool 点，取 min 只会更小或相等。

    这条不变量此前只隐含在 ArmSampler.sample() 里、需要 Isaac 才能验证。
    组装逻辑抽成纯函数后可以脱离 Isaac 直接固化。
    """
    rng = np.random.default_rng(0)
    for _ in range(50):
        links = rng.normal(size=(5, 3))
        ee = rng.normal(size=3)
        hazard = rng.normal(size=3)
        arm_pts = assemble_arm_points(links, ee, n_per_segment=3)
        d_arm = np.linalg.norm(arm_pts - hazard, axis=1).min()
        d_ee = np.linalg.norm(ee - hazard)
        assert d_arm <= d_ee + 1e-12, (d_arm, d_ee)


def main():
    tests = [
        test_includes_all_original_points,
        test_interpolates_expected_count,
        test_interpolated_points_lie_on_segment,
        test_single_link_returns_itself,
        test_rotate_by_identity_quat_is_noop,
        test_rotate_by_quat_180_about_x,
        test_rotate_by_quat_90_about_z,
        test_rotate_by_quat_preserves_length,
        test_assemble_arm_points_appends_tool_point,
        test_assemble_arm_points_is_superset_of_polyline,
        test_arm_min_distance_never_exceeds_ee_distance,
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
