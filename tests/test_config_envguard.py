import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from motion_safety.config import (
    START_POSE_ARM_CLEARANCE,
    START_POSE_ARM_CLEARANCE_GEOMETRY,
    ExperimentConfig,
    HazardConfig,
    start_pose_clearance_geometry,
)
from motion_safety.envguard import check_ascii_env


def test_config_defaults():
    cfg = ExperimentConfig()
    assert cfg.d_AB == 0.45
    assert cfg.risk_radius == 0.10
    assert cfg.planner_padding == 0.13
    assert cfg.n_steps == 600
    assert abs(cfg.dt - 1.0 / 60.0) < 1e-12
    assert cfg.success_tol == 0.03
    assert cfg.link_interp_points == 3
    assert cfg.reach_limit == 0.80
    assert cfg.hazard.radius == 0.08
    assert cfg.hazard.axis_z_bottom == 0.10
    assert cfg.hazard.axis_z_top == 1.10
    assert cfg.hazard.clearance == 0.02
    assert cfg.hazard.side == -1.0
    # 复审 Important I1：q0 必须与原先 scene.py 里硬编码的数值逐位相同，
    # 否则 A 的实测值会变，现有 results/*.json 随之失效。
    assert cfg.q0 == (0.0, -0.569, 0.0, -2.810, 0.0, 3.037, 0.741)


def test_start_pose_clearance_constant_matches_current_geometry():
    """START_POSE_ARM_CLEARANCE 是实测值，必须仍适用于当前几何。

    它取决于 q0 下整条手臂的构型，无法由 config 参数闭式算出，所以只能实测并记录
    测量条件。一旦有人改了 hazard 摆放或 d_AB（复审的反例就是把 side 改回 +1），
    这个数字立刻失效——此时必须 FAIL 并要求重新实测，而不是拿过期数字继续放行。
    """
    cfg = ExperimentConfig()
    actual = start_pose_clearance_geometry(cfg)
    assert actual == START_POSE_ARM_CLEARANCE_GEOMETRY, (
        "几何参数已改动，START_POSE_ARM_CLEARANCE 不再适用。\n"
        f"记录于：{START_POSE_ARM_CLEARANCE_GEOMETRY}\n"
        f"当前值：{actual}\n"
        "请重跑一次实验，用 results/*.csv 第 0 行的 d_arm 更新 config.py 中的常量。"
    )


def test_padding_and_radius_are_geometrically_feasible():
    """R 与 padding 必须落在几何可行域内，否则实验从一开始就不可能有效。

    这里检查三条**互不相同**的约束：

    1. `R < START_POSE_ARM_CLEARANCE`——起始位姿的**全臂**最近距离（实测 0.1685）。
       否则第 0 帧即 violation，检查 A 在几何上不可能通过。
    2. `padding < endpoint_gap`——A/B **端点**到胶囊表面的间隙
       `hypot(radius + clearance, d_AB/2) - radius`（0.1662）。否则规划器没有到达 B
       的走廊。
    3. `padding > R`——给 aware 组留出守住 R 的裕度。

    第 1 条与第 2 条用的是**不同的量**。旧版本把第 1 条也写成 `R < endpoint_gap`，
    那是个会骗人的守卫：复审给出的反例是 `side=+1` 且 `R=0.15`，
    `0.15 < 0.16617` 判定通过，而"起始 d_arm=0.1473 < 0.15"的原陷阱原样复现。
    该反例现在会被本测试的第 1 条拦下。

    自足性：`START_POSE_ARM_CLEARANCE` 是与当前几何绑定的实测常量，只有在几何
    仍与记录条件（`START_POSE_ARM_CLEARANCE_GEOMETRY`）一致时才有意义。因此本
    测试在使用该常量做可行域断言**之前**，先自行核对二者是否匹配——不依赖
    `test_start_pose_clearance_constant_matches_current_geometry` 是否与它同批
    运行。这样即便单独运行本测试，几何一旦变了（例如反例的 side=+1），也会在
    这里先行 FAIL，而不是拿失配的旧常量放行。
    """
    import math

    cfg = ExperimentConfig()
    actual_geometry = start_pose_clearance_geometry(cfg)
    assert actual_geometry == START_POSE_ARM_CLEARANCE_GEOMETRY, (
        "START_POSE_ARM_CLEARANCE 的记录几何与当前 cfg 不匹配，不能用它做可行域"
        "断言（否则会像旧版本一样放行几何已变但常量未更新的反例）。\n"
        f"记录于：{START_POSE_ARM_CLEARANCE_GEOMETRY}\n"
        f"当前值：{actual_geometry}\n"
        "请重跑一次实验，用 results/*.csv 第 0 行的 d_arm 更新 config.py 中的常量。"
    )
    offset = cfg.hazard.radius + cfg.hazard.clearance
    endpoint_gap = math.hypot(offset, cfg.d_AB / 2.0) - cfg.hazard.radius
    assert cfg.risk_radius < START_POSE_ARM_CLEARANCE, (
        cfg.risk_radius, START_POSE_ARM_CLEARANCE
    )
    assert cfg.planner_padding < endpoint_gap, (cfg.planner_padding, endpoint_gap)
    # padding > R 才能让 aware 组稳健地把最近距离守在 R 之上
    assert cfg.planner_padding > cfg.risk_radius


def test_config_to_dict_roundtrip():
    cfg = ExperimentConfig()
    d = cfg.to_dict()
    assert d["risk_radius"] == 0.10
    assert d["hazard"]["radius"] == 0.08
    assert d["hazard"]["side"] == -1.0
    # 复审 Important I1：q0 必须出现在 config 快照里，否则 analyze.py 的
    # assert_configs_match（比对 config 字典）不可能发现两组用了不同 q0。
    assert tuple(d["q0"]) == (0.0, -0.569, 0.0, -2.810, 0.0, 3.037, 0.741)


def test_start_pose_clearance_geometry_includes_q0_and_link_interp_points():
    """复审 Important I1：这两个字段此前缺失，改动其一常量会失效但测试照常 PASS。

    `q0` 决定 A 的实测值（进而决定 START_POSE_ARM_CLEARANCE 本身依赖的手臂构型）；
    `link_interp_points` 增大会让 d_arm 的 min 单调不增。二者现在都记入
    GEOMETRY，任一被悄悄改动都会被失配检测拦下。
    """
    cfg = ExperimentConfig()
    actual = start_pose_clearance_geometry(cfg)
    assert "q0" in actual
    assert "link_interp_points" in actual
    assert actual["q0"] == (0.0, -0.569, 0.0, -2.810, 0.0, 3.037, 0.741)
    assert actual["link_interp_points"] == 3


def test_envguard_rejects_non_ascii(monkeypatch_env):
    monkeypatch_env("LOCALAPPDATA", "C:\\Users\\苏子健\\AppData\\Local")
    monkeypatch_env("TEMP", "E:\\ovtmp")
    monkeypatch_env("TMP", "E:\\ovtmp")
    monkeypatch_env("WARP_CACHE_PATH", "E:\\ovwarp")
    try:
        check_ascii_env()
    except SystemExit as exc:
        assert "LOCALAPPDATA" in str(exc)
        return
    raise AssertionError("check_ascii_env should have raised SystemExit")


def test_envguard_accepts_ascii(monkeypatch_env):
    monkeypatch_env("LOCALAPPDATA", "E:\\ovhome")
    monkeypatch_env("TEMP", "E:\\ovtmp")
    monkeypatch_env("TMP", "E:\\ovtmp")
    monkeypatch_env("WARP_CACHE_PATH", "E:\\ovwarp")
    check_ascii_env()


def test_envguard_rejects_missing(monkeypatch_env):
    monkeypatch_env("LOCALAPPDATA", "E:\\ovhome")
    monkeypatch_env("TEMP", "E:\\ovtmp")
    monkeypatch_env("TMP", "E:\\ovtmp")
    monkeypatch_env("WARP_CACHE_PATH", None)
    try:
        check_ascii_env()
    except SystemExit as exc:
        assert "WARP_CACHE_PATH" in str(exc)
        return
    raise AssertionError("check_ascii_env should have raised SystemExit")


def main():
    saved = dict(os.environ)

    def monkeypatch_env(key, value):
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value

    tests = [
        ("test_config_defaults", lambda: test_config_defaults()),
        (
            "test_start_pose_clearance_constant_matches_current_geometry",
            lambda: test_start_pose_clearance_constant_matches_current_geometry(),
        ),
        (
            "test_padding_and_radius_are_geometrically_feasible",
            lambda: test_padding_and_radius_are_geometrically_feasible(),
        ),
        ("test_config_to_dict_roundtrip", lambda: test_config_to_dict_roundtrip()),
        (
            "test_start_pose_clearance_geometry_includes_q0_and_link_interp_points",
            lambda: test_start_pose_clearance_geometry_includes_q0_and_link_interp_points(),
        ),
        ("test_envguard_rejects_non_ascii", lambda: test_envguard_rejects_non_ascii(monkeypatch_env)),
        ("test_envguard_accepts_ascii", lambda: test_envguard_accepts_ascii(monkeypatch_env)),
        ("test_envguard_rejects_missing", lambda: test_envguard_rejects_missing(monkeypatch_env)),
    ]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print("PASS", name)
        except Exception as exc:
            failed += 1
            print("FAIL", name, "->", repr(exc))
        finally:
            os.environ.clear()
            os.environ.update(saved)
    print(f"{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
