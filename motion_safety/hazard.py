"""Hazard 几何：竖直胶囊体 + 点到表面的精确距离。纯 numpy，不依赖 Isaac。"""

from dataclasses import dataclass

import numpy as np

from .config import HazardConfig


@dataclass(frozen=True)
class Capsule:
    """由轴线段 (seg_a -> seg_b) 与半径定义的胶囊体。"""

    seg_a: np.ndarray
    seg_b: np.ndarray
    radius: float

    def distance_to_surface(self, points: np.ndarray) -> np.ndarray:
        """各点到胶囊表面的距离，内部点截断为 0。

        Args:
            points: 形状 (N, 3) 的点集。
        Returns:
            形状 (N,) 的距离数组，非负。
        """
        pts = np.asarray(points, dtype=float).reshape(-1, 3)
        seg_a = np.asarray(self.seg_a, dtype=float)
        seg_b = np.asarray(self.seg_b, dtype=float)

        ab = seg_b - seg_a
        ab_len2 = float(ab @ ab)
        if ab_len2 <= 0.0:
            t = np.zeros(len(pts))
        else:
            t = np.clip(((pts - seg_a) @ ab) / ab_len2, 0.0, 1.0)

        closest = seg_a + t[:, None] * ab
        d_axis = np.linalg.norm(pts - closest, axis=1)
        return np.maximum(d_axis - self.radius, 0.0)

    def to_dict(self) -> dict:
        return {
            "seg_a": np.asarray(self.seg_a, dtype=float).tolist(),
            "seg_b": np.asarray(self.seg_b, dtype=float).tolist(),
            "radius": float(self.radius),
        }


def build_hazard(A: np.ndarray, B: np.ndarray, hazard_cfg: HazardConfig) -> Capsule:
    """在 A->B 中点沿水平侧向偏移，构造竖直胶囊。

    偏移量 = radius + clearance，使 A->B 直线到胶囊表面的最近距离恰为 clearance。
    """
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)

    u = B - A
    u_horiz = np.array([u[0], u[1], 0.0])
    norm = np.linalg.norm(u_horiz)
    if norm < 1e-9:
        raise ValueError("A 与 B 的水平位移过小，无法确定行进方向")
    u_horiz = u_horiz / norm

    # 水平面内垂直于行进方向的单位向量（左法向），再按 side 选边。
    # side 只改变胶囊落在路径哪一侧，不影响"A->B 直线到表面距离 == clearance"
    # 这一核心不变量。
    n = np.array([-u_horiz[1], u_horiz[0], 0.0]) * float(hazard_cfg.side)

    midpoint = 0.5 * (A + B)
    offset = hazard_cfg.radius + hazard_cfg.clearance
    center_xy = midpoint + n * offset

    seg_a = np.array([center_xy[0], center_xy[1], hazard_cfg.axis_z_bottom])
    seg_b = np.array([center_xy[0], center_xy[1], hazard_cfg.axis_z_top])
    return Capsule(seg_a=seg_a, seg_b=seg_b, radius=hazard_cfg.radius)
