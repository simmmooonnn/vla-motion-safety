"""启动守卫：中文用户名会让 Isaac 的多个组件在非 ASCII 路径上隐晦失败。"""

import os

REQUIRED_ENV = ("LOCALAPPDATA", "TEMP", "TMP", "WARP_CACHE_PATH")

_HINT = (
    "\n请勿直接运行本脚本，改用 run_experiment.bat / run-tests.bat 启动，"
    "它们会设置以下环境变量：\n"
    "  LOCALAPPDATA=E:\\ovhome\n"
    "  TEMP=E:\\ovtmp\n"
    "  TMP=E:\\ovtmp\n"
    "  WARP_CACHE_PATH=E:\\ovwarp\n"
)


def check_ascii_env() -> None:
    """确认关键路径环境变量已设置且为纯 ASCII，否则立即退出。"""
    for key in REQUIRED_ENV:
        value = os.environ.get(key)
        if not value:
            raise SystemExit(f"环境变量 {key} 未设置。{_HINT}")
        try:
            value.encode("ascii")
        except UnicodeEncodeError:
            raise SystemExit(
                f"环境变量 {key} 含非 ASCII 字符：{value}\n"
                f"中文用户名会导致 Isaac 素材下载与 Warp CUDA 编译失败。{_HINT}"
            )
