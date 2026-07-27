import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from analyze import assert_configs_match, validity_checks

R = 0.15


def _summary(success=True, min_arm=0.20):
    return {"summary": {"success": success, "min_dist_arm": min_arm}}


# --- assert_configs_match（复审 Important I1 / I2）---

_CONFIG = {"risk_radius": 0.10, "dt": 1.0 / 60.0, "q0": [0.0, -0.569, 0.0, -2.810, 0.0, 3.037, 0.741]}
_A = [0.463, 0.0, 0.385]
_B = [0.463, 0.450, 0.385]
_CAPSULE = {"seg_a": [0.563, 0.225, 0.1], "seg_b": [0.563, 0.225, 1.1], "radius": 0.08}


def _run_json(condition, hazard_registered, config=None, n_steps=600, A=None, goal_B=None, capsule=None):
    return {
        "condition": condition,
        "config": config if config is not None else dict(_CONFIG),
        "n_steps": n_steps,
        "meta": {
            "A": A if A is not None else list(_A),
            "goal_B": goal_B if goal_B is not None else list(_B),
            "capsule": capsule if capsule is not None else dict(_CAPSULE),
            "hazard_registered_with_planner": hazard_registered,
        },
        "summary": {"success": True, "min_dist_arm": 0.15},
    }


def test_assert_configs_match_passes_on_matching_valid_data():
    aware = _run_json("aware", True)
    blind = _run_json("blind", False)
    assert_configs_match(aware, blind)  # 不应抛异常


def test_assert_configs_match_fails_when_arguments_are_swapped():
    """复审 Important I2：参数顺序写反时必须被直接拦下，而不是让检查 A 用错误的

    数字去比 R 并 FAIL、把人引向错误方向。"""
    aware = _run_json("aware", True)
    blind = _run_json("blind", False)
    try:
        assert_configs_match(blind, aware)  # 顺序反了
    except SystemExit as exc:
        assert "aware" in str(exc)
        return
    raise AssertionError("参数顺序反了应该抛 SystemExit")


def test_assert_configs_match_fails_when_hazard_flag_inconsistent():
    aware_bad = _run_json("aware", False)  # condition 说是 aware，但 flag 是 False
    blind = _run_json("blind", False)
    try:
        assert_configs_match(aware_bad, blind)
    except SystemExit as exc:
        assert "hazard_registered_with_planner" in str(exc)
        return
    raise AssertionError("hazard_registered_with_planner 与 condition 不符时应抛 SystemExit")


def test_assert_configs_match_fails_when_meta_a_differs():
    """复审 Important I1：q0 若在两组之间不同，会体现为 meta.A 不同——

    即使 config 字典本身相同（q0 曾完全逃逸 config 快照），这里也必须拦下。"""
    aware = _run_json("aware", True, A=[0.999, 0.0, 0.385])
    blind = _run_json("blind", False)
    try:
        assert_configs_match(aware, blind)
    except SystemExit as exc:
        assert "meta.A" in str(exc)
        return
    raise AssertionError("meta.A 不一致时应抛 SystemExit")


def test_assert_configs_match_fails_when_config_differs():
    aware = _run_json("aware", True, config={**_CONFIG, "risk_radius": 0.20})
    blind = _run_json("blind", False)
    try:
        assert_configs_match(aware, blind)
    except SystemExit as exc:
        assert "配置不一致" in str(exc)
        return
    raise AssertionError("config 不一致时应抛 SystemExit")


def test_assert_configs_match_fails_when_n_steps_differs():
    aware = _run_json("aware", True, n_steps=600)
    blind = _run_json("blind", False, n_steps=300)
    try:
        assert_configs_match(aware, blind)
    except SystemExit as exc:
        assert "步数不一致" in str(exc)
        return
    raise AssertionError("n_steps 不一致时应抛 SystemExit")


def test_all_checks_pass_on_good_data():
    checks = validity_checks(_summary(True, 0.20), _summary(True, 0.02), 0.18, R)
    assert all(ok for _, ok, _ in checks), checks


def test_check_a_fails_when_aware_violates():
    checks = validity_checks(_summary(True, 0.05), _summary(True, 0.02), 0.18, R)
    names = {n: ok for n, ok, _ in checks}
    assert names["A"] is False


def test_check_b_fails_when_blind_task_incomplete():
    checks = validity_checks(_summary(True, 0.20), _summary(False, 0.02), 0.18, R)
    names = {n: ok for n, ok, _ in checks}
    assert names["B"] is False


def test_check_c_fails_when_trajectories_identical():
    checks = validity_checks(_summary(True, 0.20), _summary(True, 0.02), 0.0005, R)
    names = {n: ok for n, ok, _ in checks}
    assert names["C"] is False


def test_check_a_fails_when_aware_task_incomplete():
    checks = validity_checks(_summary(False, 0.20), _summary(True, 0.02), 0.18, R)
    names = {n: ok for n, ok, _ in checks}
    assert names["A"] is False


def main():
    tests = [
        test_all_checks_pass_on_good_data,
        test_check_a_fails_when_aware_violates,
        test_check_b_fails_when_blind_task_incomplete,
        test_check_c_fails_when_trajectories_identical,
        test_check_a_fails_when_aware_task_incomplete,
        test_assert_configs_match_passes_on_matching_valid_data,
        test_assert_configs_match_fails_when_arguments_are_swapped,
        test_assert_configs_match_fails_when_hazard_flag_inconsistent,
        test_assert_configs_match_fails_when_meta_a_differs,
        test_assert_configs_match_fails_when_config_differs,
        test_assert_configs_match_fails_when_n_steps_differs,
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
