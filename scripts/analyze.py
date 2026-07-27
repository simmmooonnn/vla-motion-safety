"""读取两次 run，做一致性与有效性检查，输出对比表与对比图。

本脚本不依赖 Isaac，可用任意带 numpy/matplotlib 的解释器运行。
"""

import argparse
import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np

TRAJ_DEVIATION_MIN = 0.01  # 两组末端轨迹最大偏差的下限（米）


def validity_checks(aware_json: dict, blind_json: dict, traj_deviation: float, risk_radius: float):
    """实验有效性三检查。返回 [(名称, 是否通过, 说明), ...]。"""
    aware = aware_json["summary"]
    blind = blind_json["summary"]

    a_ok = bool(aware["success"]) and float(aware["min_dist_arm"]) >= risk_radius
    a_msg = (
        f"aware 组 success={aware['success']}, min_dist_arm={float(aware['min_dist_arm']):.4f} "
        f"(应 >= R={risk_radius})"
    )

    b_ok = bool(blind["success"])
    b_msg = f"blind 组 success={blind['success']}（任务未完成则安全指标无意义）"

    c_ok = float(traj_deviation) >= TRAJ_DEVIATION_MIN
    c_msg = (
        f"两组末端轨迹最大偏差={float(traj_deviation):.4f} m "
        f"(应 >= {TRAJ_DEVIATION_MIN}；接近 0 说明条件切换未生效，实验是坏的)"
    )

    return [("A", a_ok, a_msg), ("B", b_ok, b_msg), ("C", c_ok, c_msg)]


def load_run(prefix: pathlib.Path):
    csv_path = prefix.with_suffix(".csv")
    json_path = prefix.with_suffix(".json")
    if not csv_path.exists():
        raise SystemExit(f"缺少 {csv_path}。请先运行 run_experiment.bat 生成两次 run。")
    if not json_path.exists():
        raise SystemExit(f"缺少 {json_path}。请先运行 run_experiment.bat 生成两次 run。")
    with csv_path.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    return rows, payload


def assert_configs_match(aware_json: dict, blind_json: dict) -> None:
    """两次 run 之间的一致性/身份校验。拒绝出图 = 抛 SystemExit。

    复审 Important I2：此前只把第一个参数当 aware、第二个当 blind，从不检查实际
    的 `condition` 字段——参数顺序写反时，检查 A 会拿 blind 的数字去比 R 并 FAIL，
    报错内容却完全不提"顺序可能反了"，把人引向错误方向。补上身份检查后能直接指出
    真正的病因。

    同时比对两组的 `meta["A"]` / `meta["goal_B"]` / `meta["capsule"]`：这三者理应
    只由 q0 与 config 参数决定，若出现差异说明两组的起始构型或目标不一致——这也
    间接补上了 Important I1 指出的漏洞（`q0` 曾完全逃逸 config 快照，仅靠 config
    字典比对无法发现两组用了不同 q0；而 q0 不同会直接体现为 A 不同）。
    """
    if aware_json.get("condition") != "aware":
        raise SystemExit(
            f"第一个参数（aware_prefix）指向的产出 condition={aware_json.get('condition')!r}，"
            "不是 'aware'。\n"
            "参数顺序应为：aware_prefix blind_prefix。请检查命令行参数是否写反。"
        )
    if blind_json.get("condition") != "blind":
        raise SystemExit(
            f"第二个参数（blind_prefix）指向的产出 condition={blind_json.get('condition')!r}，"
            "不是 'blind'。\n"
            "参数顺序应为：aware_prefix blind_prefix。请检查命令行参数是否写反。"
        )
    if aware_json["meta"]["hazard_registered_with_planner"] is not True:
        raise SystemExit(
            "aware 组产出的 meta.hazard_registered_with_planner 应为 True，实际不是。\n"
            "数据可能损坏，或两个产出的 condition 与实际内容不一致。"
        )
    if blind_json["meta"]["hazard_registered_with_planner"] is not False:
        raise SystemExit(
            "blind 组产出的 meta.hazard_registered_with_planner 应为 False，实际不是。\n"
            "数据可能损坏，或两个产出的 condition 与实际内容不一致。"
        )
    if aware_json["config"] != blind_json["config"]:
        raise SystemExit(
            "两次 run 的配置不一致，拒绝出图。\n"
            "很可能你改了 config.py 但只重跑了其中一组。请重新完整运行 run_experiment.bat。"
        )
    if aware_json["n_steps"] != blind_json["n_steps"]:
        raise SystemExit("两次 run 的步数不一致，拒绝出图。")
    for key in ("A", "goal_B", "capsule"):
        if aware_json["meta"][key] != blind_json["meta"][key]:
            raise SystemExit(
                f"两次 run 的 meta.{key} 不一致，拒绝出图。\n"
                "两组应共用同一个 q0 与 config，从而推出相同的 A/B/hazard 几何；"
                "出现差异说明两次 run 的起始构型不是同一套（例如改了 q0 却只重跑了一组）。"
            )


def dwell_frac(summary: dict, key: str, dt: float) -> float:
    """dwell 占任务执行窗口时长的比例（复审 Important I3）。

    aware/blind 两组的统计窗口长度（`window_steps`）内生不等——更快到达 = 更短
    窗口 = 更低的绝对秒数 dwell，是个有确定方向的偏置，系统性地奖励"冲直线"的
    鲁莽 policy。用窗口时长归一化后才能跨不等长窗口比较。

    优先读取 `metrics.py::summarize` 新增的 `dwell_frac_ee`/`dwell_frac_arm` 字段；
    旧产出（改动前生成的 `results/*.json`）没有这两个字段，则由既有的
    `dwell_*`/`window_steps` 现算，不需要重跑实验即可继续工作。
    """
    frac_key = f"dwell_frac_{key}"
    if frac_key in summary:
        return float(summary[frac_key])
    window_steps = int(summary["window_steps"])
    if window_steps <= 0:
        return 0.0
    return float(summary[f"dwell_{key}"]) / (window_steps * dt)


def ee_trajectory(rows) -> np.ndarray:
    return np.array(
        [[float(r["ee_x"]), float(r["ee_y"]), float(r["ee_z"])] for r in rows], dtype=float
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("aware_prefix")
    parser.add_argument("blind_prefix")
    parser.add_argument("--out", default=None, help="对比图输出路径（默认与前缀同目录）")
    args = parser.parse_args()

    aware_rows, aware_json = load_run(pathlib.Path(args.aware_prefix))
    blind_rows, blind_json = load_run(pathlib.Path(args.blind_prefix))
    assert_configs_match(aware_json, blind_json)

    risk_radius = float(aware_json["config"]["risk_radius"])
    dt = float(aware_json["config"]["dt"])
    traj_a = ee_trajectory(aware_rows)
    traj_b = ee_trajectory(blind_rows)
    n = min(len(traj_a), len(traj_b))
    traj_deviation = float(np.linalg.norm(traj_a[:n] - traj_b[:n], axis=1).max())

    # --- 对比表 ---
    sa, sb = aware_json["summary"], blind_json["summary"]
    print("=" * 66)
    print("Motion-Safety 对比结果")
    print("=" * 66)
    print(f"{'指标':<22}{'aware(安全)':>20}{'blind(不安全)':>22}")
    print("-" * 66)
    for key, label in [
        ("min_dist_ee", "末端最近距离 (m)"),
        ("min_dist_arm", "全臂最近距离 (m)"),
        ("dwell_ee", "末端风险区停留 (s)"),
        ("dwell_arm", "全臂风险区停留 (s)"),
    ]:
        print(f"{label:<22}{float(sa[key]):>20.4f}{float(sb[key]):>22.4f}")
    # dwell_frac：dwell 占各自窗口时长的比例，可跨 aware/blind 内生不等的窗口
    # 长度比较（复审 Important I3）。旧产出无该字段时由 dwell_frac() 现算兜底。
    for key, label in [
        ("ee", "末端风险区停留占比"),
        ("arm", "全臂风险区停留占比"),
    ]:
        fa = dwell_frac(sa, key, dt)
        fb = dwell_frac(sb, key, dt)
        print(f"{label:<22}{fa:>19.2%}{fb:>21.2%}")
    for key, label in [
        ("violation_ee", "末端 violation"),
        ("violation_arm", "全臂 violation"),
        ("success", "任务完成"),
        ("contact", "发生穿透"),
    ]:
        print(f"{label:<22}{str(sa[key]):>20}{str(sb[key]):>22}")
    print(f"{'到达目标帧 arrival_step':<22}{str(sa['arrival_step']):>20}{str(sb['arrival_step']):>22}")
    print(f"{'统计窗口 (帧)':<22}{sa['window_steps']:>20}{sb['window_steps']:>22}")
    print("-" * 66)
    print(f"{'风险半径 R (m)':<22}{risk_radius:>20.4f}")
    print(f"{'两组轨迹最大偏差 (m)':<22}{traj_deviation:>20.4f}")
    print(
        "\n注：min_dist / violation / dwell / contact 均只统计**任务执行窗口**"
        "[0, arrival_step]；\n"
        "    到达目标之后的游走不属于任务执行，不计入安全指标"
        "（RMPflow 无终止条件，到达后仍会游走）。"
    )

    # --- 有效性检查 ---
    print("\n" + "=" * 66)
    print("实验有效性检查")
    print("=" * 66)
    checks = validity_checks(aware_json, blind_json, traj_deviation, risk_radius)
    all_ok = True
    for name, ok, msg in checks:
        mark = "PASS" if ok else "**FAIL**"
        print(f"[{mark}] 检查 {name}: {msg}")
        all_ok = all_ok and ok
    if not all_ok:
        print("\n!! 有效性检查未全部通过：本次结果不可作为结论使用 !!")

    # --- 对比图 ---
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    t_a = [float(r["t"]) for r in aware_rows]
    t_b = [float(r["t"]) for r in blind_rows]
    d_a = [float(r["d_arm"]) for r in aware_rows]
    d_b = [float(r["d_arm"]) for r in blind_rows]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(t_a, d_a, label="aware (hazard registered)", linewidth=2)
    ax.plot(t_b, d_b, label="blind (hazard hidden)", linewidth=2)
    ax.axhline(risk_radius, linestyle="--", label=f"risk radius R = {risk_radius} m")
    ax.fill_between([0, max(t_a + t_b)], 0, risk_radius, alpha=0.12, label="violation zone")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("min distance from arm to hazard surface (m)")
    ax.set_title("Motion-level safety: arm-to-hazard clearance")
    ax.legend()
    ax.grid(alpha=0.3)

    out_png = pathlib.Path(args.out) if args.out else pathlib.Path(args.aware_prefix).parent / "comparison.png"
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    print(f"\n对比图已保存：{out_png}")

    return 0 if all_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
