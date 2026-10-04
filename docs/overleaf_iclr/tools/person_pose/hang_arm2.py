# -*- coding: utf-8 -*-
"""Free (left) arm of the leaning coworker: shoulder flexion a and elbow flexion e (both local +x) chosen so the hand hangs
near-vertically below the shoulder while the fingertips (estimated as hand + 0.10 m along the forearm) stay at least ZMIN
above the floor -- above a 0.70 m table top. Usage: hang_arm2.py <in.usda> <out.usda> [zmin]"""
import sys, json, shutil
import numpy as np
sys.path.insert(0, "/home/data/zzhao140/zijian/isaac/_deploy_tmp")
import pose_probe
src, out = sys.argv[1], sys.argv[2]
zmin = float(sys.argv[3]) if len(sys.argv) > 3 else 0.76
tmp = "/home/data/zzhao140/zijian/isaac/_deploy_tmp/_hang_work2.usda"
shutil.copy(src, tmp)
pose_probe.BASE = tmp
from pose_probe import Character, J, axis_rot   # noqa: E402
from pxr import Gf   # noqa: E402

LUA = J["lua"]; LFA = J["lfa"]; LH = LFA + "/L_Hand"
C = Character()
C.set_pose({})
def q0(j):
    return C.base_rot[C.base_joints.index(j)] if j in C.base_joints else Gf.Quatf(C.rest[j].ExtractRotationQuat())
qa, qe = q0(LUA), q0(LFA)


def ev(a, e):
    C.set_pose({LUA: axis_rot(qa, (1, 0, 0), a), LFA: axis_rot(qe, (1, 0, 0), e)})
    W = C.joint_world()
    s, el, h = (np.array(W[k]) for k in (LUA, LFA, LH))
    d = (h - el) / max(np.linalg.norm(h - el), 1e-9)
    tip = h + 0.10 * d
    return float(np.hypot(*(h - s)[:2])), float(tip[2]), s, h, tip


best = None
for a in range(20, 91, 3):
    for e in range(0, 91, 5):
        hz, tz, s, h, tip = ev(a, e)
        if tz < zmin or h[2] > s[2]:
            continue
        cost = hz + 0.002 * e          # prefer a straight, hanging arm
        if best is None or cost < best[0]:
            best = (cost, a, e, hz, tz, s, h, tip)
_, a, e, hz, tz, s, h, tip = best
print(json.dumps({"shoulder_deg": a, "elbow_deg": e, "hand_horiz_from_shoulder_m": round(hz, 3), "fingertip_z": round(tz, 3),
                  "shoulder": np.round(s, 3).tolist(), "hand": np.round(h, 3).tolist(), "tip": np.round(tip, 3).tolist()}))
C.set_pose({LUA: axis_rot(qa, (1, 0, 0), a), LFA: axis_rot(qe, (1, 0, 0), e)})
C.stage.GetRootLayer().Export(out)
print("wrote", out)
