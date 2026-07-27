"""判别实验：hazard 的刚性接触是否把机械臂物理卡死？

这是 Task 9 修复 2（`scene.py::_filter_collision_pair` 施加
`UsdPhysics.FilteredPairsAPI`）的**唯一支撑证据**。复审指出该结论当时只写在报告
里、脚本与日志均未提交，磁盘上无法复核，故把它重建为一个可一键重跑的脚本。

## 判别逻辑

RMPflow 的 `forward()` 完全忽略 `estimated_state`（只用自己的积分器
`_output_position`），所以"规划器以为自己到了、实际手臂没动"是可能的。判别量是
**关节指令值与实际值的稳态偏差 `|cmd - act|`**：

- `|cmd - act| ~ 1 rad`：驱动在拼命推、关节却不动 → 有外力顶住 → 手臂撞在 hazard 上。
- `|cmd - act| ~ 0.004 rad`：关节忠实跟踪指令 → 控制链路正常。

两次运行只差**一处**：hazard 与机器人之间的 `FilteredPairsAPI` 过滤是否生效。
其余（hazard 位置、几何、q0、目标 B、步数）完全相同，故 `|cmd - act|` 的差异只能
归因于物理接触。

本脚本固定跑 **blind** 条件：blind 组 hazard 不进规划器世界，规划器对它一无所知，
因此观察到的任何差异都是**纯物理**效应，不掺规划器避障行为。

## 历史数据（Task 9 首次诊断，当时用"把 hazard 挪走"作对照）

    有接触:  step 100 |B-ee|=0.3214  |cmd-act|=1.0232
             step 599 |B-ee|=0.3237  |cmd-act|=0.9852
    无接触:  step   0 |B-ee|=0.4500  |cmd-act|=0.0001
             step 150 |B-ee|=0.1062  |cmd-act|=0.0040
             step 599 |B-ee|=0.1061  |cmd-act|=0.0042

本脚本用"切换碰撞过滤"代替"挪走 hazard"：因果主张相同（接触 → 卡死），但它直接
对照的就是仓库里实际采用的那处修复，审计价值更高。

## 本脚本重跑复现的结果（`--both --side 1 --steps 300`）

    filter OFF: step 100 |B-ee|=0.3199  |cmd-act|=1.6260
                step 299 |B-ee|=0.3187  |cmd-act|=1.3197     <- 卡死，到不了 B
    filter ON : step 100 |B-ee|=0.0393  |cmd-act|=0.0274
                step 299 |B-ee|=0.0152  |cmd-act|=0.0506     <- 正常跟踪，到达 B

与历史数据同一现象（数值不逐位相同：历史那次是"挪走 hazard"且带着当时尚未修复的
其它三个缺陷）。**判别结论成立。**

## 重要：`--side` 的默认值为什么是 +1

**在仓库当前的最终构型（`side = −1`，外侧摆放）下，本判别实验必然测不出差异。**
实测：外侧摆放时手臂全程最近只到胶囊表面外 0.0427 m，**从不发生物理接触**，
因此碰撞过滤是**空操作**——两个变体的轨迹逐帧几乎重合
（step 100 时 |B-ee| 分别为 0.0393 / 0.0392）。

也就是说：修复 2（`FilteredPairsAPI`）对**当前基线结果不是承重的**。它是在修复 1
（把 hazard 从内侧改到外侧）之前必需的——那时手臂会一头撞进胶囊。两处修复是同一轮
诊断中并行做出的，最终构型下前者使后者变成了冗余的保险。保留它是因为它是廉价的
度量卫生：若将来调整 hazard 摆放、`q0` 或 `d_AB` 使手臂重新可能接触，没有它就会
再次出现"min_dist 记录的是卡住时的距离"这种口径破坏，且失败方式隐晦。

故默认 `--side 1`：那是唯一能让手臂真的撞上 hazard、从而使判别有意义的构型。

## 用法

    $env:LOCALAPPDATA="E:\\ovhome"; $env:TEMP="E:\\ovtmp"; $env:TMP="E:\\ovtmp"
    $env:WARP_CACHE_PATH="E:\\ovwarp"
    & "E:\\Isaac\\isaac\\python.bat" scripts\\diagnose_contact_jam.py --both --steps 300

`--both` 依次跑两个变体并打印对照表。单独跑某一侧用 `--filter on` / `--filter off`。
`--side -1` 可复核"当前构型下确实无接触、过滤确为空操作"这一结论。
"""

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from motion_safety.envguard import check_ascii_env

check_ascii_env()

parser = argparse.ArgumentParser()
parser.add_argument(
    "--filter",
    choices=["on", "off"],
    default=None,
    help="on = 保留碰撞过滤（仓库现状）；off = 清掉过滤，复现被顶死的原状态",
)
parser.add_argument("--both", action="store_true", help="依次跑两个变体并对照")
parser.add_argument(
    "--side",
    type=float,
    default=1.0,
    help=(
        "hazard 落在 A->B 路径的哪一侧。默认 +1（内侧），即修复 1 之前的摆放——"
        "这是原始判别证据产生的条件，也是唯一能让手臂真的撞上 hazard 的构型。"
        "传 -1 用仓库当前摆放（外侧），此时手臂最近只到表面外 0.0427 m，"
        "根本不发生接触，两个变体必然无差异。"
    ),
)
parser.add_argument("--steps", type=int, default=600)
parser.add_argument("--gui", action="store_true")
args = parser.parse_args()

if not args.both and args.filter is None:
    parser.error("请指定 --filter on|off，或用 --both 跑对照")

from isaacsim import SimulationApp  # noqa: E402

simulation_app = SimulationApp({"headless": not args.gui})

import omni.kit.app  # noqa: E402

omni.kit.app.get_app().get_extension_manager().set_extension_enabled_immediate(
    "isaacsim.robot.experimental.manipulators.examples", True
)

import dataclasses  # noqa: E402

import numpy as np  # noqa: E402

from motion_safety.config import ExperimentConfig, HazardConfig  # noqa: E402
from motion_safety.episode import _make_states  # noqa: E402
from motion_safety.scene import (  # noqa: E402
    HAZARD_PRIM_PATH,
    ROBOT_PRIM_PATH,
    build_scene,
    reset_to_home,
)

PROBE_STEPS = (0, 100, 150, 300, 599)


def _clear_collision_filter() -> None:
    """清掉 hazard 上的 FilteredPairsAPI 目标，让机器人重新能撞上它。

    只清 relationship 的 target，不移除 API 本身——CollisionAPI 与 prim 结构保持
    原样，确保两个变体之间除"是否过滤接触"外没有任何其他差异。
    """
    import isaacsim.core.experimental.utils.stage as stage_utils
    from pxr import UsdPhysics

    stage = stage_utils.get_current_stage()
    prim = stage.GetPrimAtPath(HAZARD_PRIM_PATH)
    rel = UsdPhysics.FilteredPairsAPI(prim).GetFilteredPairsRel()
    targets = list(rel.GetTargets())
    rel.ClearTargets(True)
    print(f"  [setup] 已清除碰撞过滤，原 targets = {targets}")


def _as_numpy(x):
    return np.asarray(x.numpy() if hasattr(x, "numpy") else x, dtype=float).ravel()


def run_variant(filter_on: bool, n_steps: int) -> dict:
    """跑一个变体，返回 {step: (|B-ee|, |cmd-act|)} 与末帧详情。"""
    import isaacsim.core.experimental.utils.app as app_utils
    import isaacsim.robot_motion.experimental.motion_generation as mg
    import warp as wp
    from isaacsim.core.simulation_manager import SimulationManager
    from isaacsim.core.experimental.utils import stage as stage_utils

    label = "filter ON (仓库现状)" if filter_on else "filter OFF (复现卡死)"
    print(f"\n===== 变体：{label} =====")

    stage_utils.create_new_stage()
    SimulationManager.setup_simulation(dt=cfg.dt, device="cuda")
    handles = build_scene(cfg, "blind")
    if not filter_on:
        _clear_collision_filter()
    simulation_app.update()

    app_utils.play()
    simulation_app.update()

    articulation = handles.articulation
    reset_to_home(articulation, cfg.q0)
    simulation_app.update()

    estimated, setpoint = _make_states(mg, handles, articulation, wp)
    if not handles.controller.reset(estimated, setpoint, t=0.0):
        raise RuntimeError("RmpFlowController reset 失败")

    probes = {}
    t = 0.0
    last = None
    for step in range(n_steps):
        simulation_app.update()

        handles.world_binding.get_world_interface().update_world_to_robot_root_transforms(
            articulation.get_world_poses()
        )
        handles.world_binding.synchronize_transforms()

        estimated, setpoint = _make_states(mg, handles, articulation, wp)
        desired = handles.controller.forward(estimated, setpoint, t)

        cmd_dev = float("nan")
        if desired is not None and desired.joints.positions is not None:
            articulation.set_dof_position_targets(
                positions=desired.joints.positions,
                dof_indices=desired.joints.position_indices,
            )
            cmd = _as_numpy(desired.joints.positions)
            idx = _as_numpy(desired.joints.position_indices).astype(int)
            act = _as_numpy(articulation.get_dof_positions())[idx]
            # 稳态偏差用 L-inf：关心的是"有没有某个关节被顶住"，不是平均误差。
            cmd_dev = float(np.abs(cmd - act).max())

        ee_pos, _ = handles.sampler.sample()
        err = float(np.linalg.norm(np.asarray(ee_pos, dtype=float) - handles.B))

        last = (err, cmd_dev)
        if step in PROBE_STEPS or step == n_steps - 1:
            probes[step] = (err, cmd_dev)
            print(f"  step {step:4d} |B-ee|={err:.4f}  |cmd-act|={cmd_dev:.4f}")
        t += cfg.dt

    return {"label": label, "probes": probes, "final": last}


cfg = dataclasses.replace(
    ExperimentConfig(),
    hazard=dataclasses.replace(HazardConfig(), side=args.side),
)


def main() -> int:
    print(
        f"\nhazard side = {args.side:+.0f} "
        f"（{'内侧，修复 1 之前的摆放' if args.side > 0 else '外侧，仓库当前摆放'}）"
    )
    variants = [True, False] if args.both else [args.filter == "on"]
    results = [run_variant(f, args.steps) for f in variants]

    print("\n" + "=" * 70)
    print("判别实验结论")
    print("=" * 70)
    print(f"{'变体':<26}{'末帧 |B-ee|':>16}{'末帧 |cmd-act|':>18}")
    print("-" * 70)
    for r in results:
        err, dev = r["final"]
        print(f"{r['label']:<26}{err:>16.4f}{dev:>18.4f}")
    print("-" * 70)

    if len(results) == 2:
        on_dev = results[0]["final"][1]
        off_dev = results[1]["final"][1]
        print(
            f"\n|cmd-act| 由 {off_dev:.4f}（无过滤）降至 {on_dev:.4f}（有过滤）。"
        )
        if off_dev > 10 * max(on_dev, 1e-6):
            print(
                "判定：**接触卡死成立**。无过滤时驱动在推、关节不动，说明手臂被 hazard "
                "顶住；施加 FilteredPairsAPI 后关节忠实跟踪指令。\n"
                "推论：若不过滤，min_dist 记录的是「卡住时的距离」而非「扫过时的最近"
                "距离」，度量口径被破坏——这正是该修复必要的理由。"
            )
        elif args.side < 0:
            print(
                "判定：**无差异，且这是预期的**。当前外侧摆放下手臂最近只到 hazard 表面外\n"
                "0.0427 m，从不发生接触，碰撞过滤自然是空操作。要复现原始判别证据，\n"
                "须用 `--side 1`（修复 1 之前的内侧摆放），那才是手臂真会撞上去的构型。"
            )
        else:
            print(
                "判定：**未复现出显著差异**。请勿据此引用修复 2 的理由，需重新诊断。"
            )
    return 0


try:
    exit_code = main()
finally:
    simulation_app.close()

raise SystemExit(exit_code)
