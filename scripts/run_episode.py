"""单条件实验入口。用法见 run_experiment.bat。"""

import argparse
import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from motion_safety.envguard import check_ascii_env

check_ascii_env()

parser = argparse.ArgumentParser()
parser.add_argument("--condition", required=True, choices=["aware", "blind"])
parser.add_argument("--out", required=True, help="输出前缀，不含扩展名")
parser.add_argument("--gui", action="store_true", help="开窗观察（默认 headless）")
parser.add_argument("--steps", type=int, default=None, help="覆盖步数（冒烟测试用）")
args = parser.parse_args()

from isaacsim import SimulationApp  # noqa: E402

simulation_app = SimulationApp({"headless": not args.gui})

import omni.kit.app  # noqa: E402

omni.kit.app.get_app().get_extension_manager().set_extension_enabled_immediate(
    "isaacsim.robot.experimental.manipulators.examples", True
)

from motion_safety.config import ExperimentConfig  # noqa: E402
from motion_safety.episode import run_episode  # noqa: E402

CSV_FIELDS = ["step", "t", "ee_x", "ee_y", "ee_z", "d_ee", "d_arm", "contact"]


def main() -> int:
    cfg = ExperimentConfig()
    n_steps = args.steps if args.steps is not None else cfg.n_steps

    records, summary, meta = run_episode(cfg, args.condition, n_steps, simulation_app)

    out_prefix = pathlib.Path(args.out)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)

    csv_path = out_prefix.with_suffix(".csv")
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(records)

    json_path = out_prefix.with_suffix(".json")
    payload = {
        "condition": args.condition,
        "config": cfg.to_dict(),
        "n_steps": n_steps,
        "meta": meta,
        "summary": summary.to_dict(),
    }
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"[{args.condition}] 写出 {csv_path.name} ({len(records)} 帧) 与 {json_path.name}")
    print(f"  min_dist_ee ={summary.min_dist_ee:.4f}  min_dist_arm={summary.min_dist_arm:.4f}")
    print(f"  violation_ee={summary.violation_ee}  violation_arm={summary.violation_arm}")
    print(f"  success     ={summary.success}  contact={summary.contact}")
    print(
        f"  arrival_step={summary.arrival_step}  "
        f"统计窗口={summary.window_steps}/{n_steps} 帧"
        f"（安全指标只在 [0, arrival_step] 的任务执行窗口内统计）"
    )
    return 0


try:
    exit_code = main()
finally:
    simulation_app.close()

raise SystemExit(exit_code)
