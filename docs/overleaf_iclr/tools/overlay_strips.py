# -*- coding: utf-8 -*-
"""Draw the keep-out zone (and the 0.30 m delivery circle) on the existing top-down T1 frame strips.
Calibration: a similarity transform (scale, rotation, translation) fitted from two static landmarks whose world
positions are known — the stove centre (hazard point, (-0.01, -0.70)) and the bin centre (-0.245, -1.627) — detected
by colour (yellow / blue). CPU-only; no new renders."""
import os, math
import numpy as np
from PIL import Image, ImageDraw
FIG = r"E:\Research\Robotics-Safety\docs\overleaf_iclr\figures"
S = r"C:\Users\苏子健\AppData\Local\Temp\claude\E--Research-Robotics-Safety\0f8a80ac-06d8-48e8-b25c-61ee2e370d30\scratchpad"
STOVE_W = np.array([-0.01, -0.70]); BIN_W = np.array([-0.245, -1.627]); KEEP_OUT = 0.30; DELIVER = 0.30
UP = 3

def centroid(mask):
    ys, xs = np.nonzero(mask)
    return (np.array([xs.mean(), ys.mean()]), len(xs)) if len(xs) > 50 else (None, 0)

def landmarks(frame):
    a = np.asarray(frame).astype(int); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    yellow = (r > 180) & (g > 150) & (b < 110)                      # stove top plate
    blue = (b > 120) & (b > r + 50) & (b > g + 30)                   # bin
    return centroid(yellow), centroid(blue)

def similarity(p_stove, p_bin):
    """world -> pixel: p = s*R*w + t, from two correspondences."""
    dw = BIN_W - STOVE_W; dp = p_bin - p_stove
    s = np.linalg.norm(dp) / np.linalg.norm(dw)
    ang = math.atan2(dp[1], dp[0]) - math.atan2(dw[1], dw[0])
    R = np.array([[math.cos(ang), -math.sin(ang)], [math.sin(ang), math.cos(ang)]])
    t = p_stove - s * R @ STOVE_W
    return s, R, t

def overlay(strip_path, out_path, label):
    im = Image.open(strip_path).convert("RGB"); W, H = im.size; n = 4; fw = W // n
    out = Image.new("RGB", (W * UP, H * UP))
    scales = []
    # the camera is static: calibrate once, on the frame where the stove plate is least occluded (most yellow pixels)
    best = None
    for k in range(n):
        (ps, ny), (pb, nb) = landmarks(im.crop((k * fw, 0, (k + 1) * fw, H)))
        if ps is not None and pb is not None and (best is None or ny > best[0]): best = (ny, ps, pb)
    calib = similarity(best[1], best[2]) if best else None
    for k in range(n):
        fr = im.crop((k * fw, 0, (k + 1) * fw, H))
        big = fr.resize((fw * UP, H * UP), Image.LANCZOS); d = ImageDraw.Draw(big)
        if calib:
            s, R, t = calib; scales.append(s)
            c = (s * R @ STOVE_W + t) * UP; rk = KEEP_OUT * s * UP
            # dashed red keep-out circle around the hazard point
            for i in range(36):
                a0 = i * 10; a1 = a0 + 6
                d.arc([c[0] - rk, c[1] - rk, c[0] + rk, c[1] + rk], a0, a1, fill=(190, 40, 40), width=3)
            d.ellipse([c[0] - 4, c[1] - 4, c[0] + 4, c[1] + 4], fill=(190, 40, 40))
            cb = (s * R @ BIN_W + t) * UP; rb = DELIVER * s * UP
            for i in range(36):
                a0 = i * 10; a1 = a0 + 4
                d.arc([cb[0] - rb, cb[1] - rb, cb[0] + rb, cb[1] + rb], a0, a1, fill=(40, 70, 140), width=2)
        d.text((6, 6), f"{label}  ·  t{k+1}", fill=(20, 20, 20))
        out.paste(big, (k * fw * UP, 0))
    out.save(out_path)
    print(os.path.basename(out_path), "scale px/m (per frame):", [round(x, 1) for x in scales])

overlay(os.path.join(FIG, "fig_t1_fire_defect.png"), os.path.join(FIG, "fig_t1_fire_defect_ov.png"), "blind")
overlay(os.path.join(FIG, "fig_t1_fire_shield.png"), os.path.join(FIG, "fig_t1_fire_shield_ov.png"), "+ shield")
Image.open(os.path.join(FIG, "fig_t1_fire_defect_ov.png")).save(os.path.join(S, "pdfpages", "ov_defect.png"))
Image.open(os.path.join(FIG, "fig_t1_fire_shield_ov.png")).save(os.path.join(S, "pdfpages", "ov_shield.png"))
