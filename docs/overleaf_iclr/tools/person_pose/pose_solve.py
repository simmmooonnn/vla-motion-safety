# -*- coding: utf-8 -*-
"""Solve a leaning-reach pose: the right wrist at a target in the character's own frame (facing -y, root on the floor),
then author it as a .usda. Imports the probe tool for the skeleton handling. Usage:
    pose_solve.py <reach_d> <wrist_height> <out.usda>
Bend is split equally over Waist / Spine01 / Spine02 about local +x (forward); shoulder and elbow flex about local +x.
"""
import sys, math, itertools, json
import numpy as np
sys.path.insert(0, "/tmp")
from pose_probe import Character, J, axis_rot   # noqa: E402
from pxr import Gf, UsdSkel, Usd, UsdGeom, Vt   # noqa: E402

reach_d = float(sys.argv[1]) if len(sys.argv) > 1 else 0.45
wrist_h = float(sys.argv[2]) if len(sys.argv) > 2 else 0.827
out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/person_reach.usda"

C = Character()
C.set_pose({})
W0 = C.joint_world()
lat = float(W0[J["rh"]][0])                       # keep the wrist on the right side where it hangs
target = np.array([lat, -reach_d, wrist_h])
q0 = {k: (C.rot_of(J[k]) if J[k] in C.base_joints else Gf.Quatf(C.rest[J[k]].ExtractRotationQuat()))
      for k in ("waist", "sp1", "sp2", "rua", "rfa")}


def pose_of(tb, ts, te):
    return {J["waist"]: axis_rot(q0["waist"], (1, 0, 0), tb / 3.0),
            J["sp1"]: axis_rot(q0["sp1"], (1, 0, 0), tb / 3.0),
            J["sp2"]: axis_rot(q0["sp2"], (1, 0, 0), tb / 3.0),
            J["rua"]: axis_rot(q0["rua"], (1, 0, 0), ts),
            J["rfa"]: axis_rot(q0["rfa"], (1, 0, 0), te)}


def evaluate(tb, ts, te):
    C.set_pose(pose_of(tb, ts, te))
    W = C.joint_world()
    w = W[J["rh"]]
    err = float(np.linalg.norm(w - target))
    return err, W


best = None
for tb, ts, te in itertools.product(range(0, 61, 6), range(0, 121, 10), range(0, 91, 10)):
    err, _ = evaluate(tb, ts, te)
    cost = err + 0.0004 * (tb + 0.3 * ts + 0.3 * te)      # prefer the least bend that reaches
    if best is None or cost < best[0]:
        best = (cost, err, tb, ts, te)
_, _, tb0, ts0, te0 = best
for tb, ts, te in itertools.product(np.arange(tb0 - 6, tb0 + 6.1, 1.5), np.arange(ts0 - 10, ts0 + 10.1, 2.5),
                                    np.arange(te0 - 10, te0 + 10.1, 2.5)):
    if tb < 0 or ts < 0 or te < 0:
        continue
    err, _ = evaluate(tb, ts, te)
    cost = err + 0.0004 * (tb + 0.3 * ts + 0.3 * te)
    if cost < best[0]:
        best = (cost, err, float(tb), float(ts), float(te))
_, err, tb, ts, te = best
err, W = evaluate(tb, ts, te)
res = {"bend_deg": round(tb, 1), "shoulder_deg": round(ts, 1), "elbow_deg": round(te, 1), "wrist_err_m": round(err, 4),
       "wrist": np.round(W[J["rh"]], 3).tolist(), "target": np.round(target, 3).tolist(),
       "head": np.round(W[J["head"]], 3).tolist(), "shoulder": np.round(W[J["rua"]], 3).tolist(),
       "hip": np.round(W[J["hip"]], 3).tolist(), "rtoe": np.round(W[J["rtoe"]], 3).tolist()}
mid = [k for k in C.all_joints if k.endswith("R_Hand/R_Mid1")]
if mid:
    res["fingertip_base"] = np.round(W[mid[0]], 3).tolist()
print(json.dumps(res))

# author the pose: the tucked file's four arm joints plus the bend and the right-arm reach
P = pose_of(tb, ts, te)
joints = list(C.base_joints)
rots = list(C.base_rot)
trs = list(C.base_tr)
for jp, q in P.items():
    if jp in joints:
        rots[joints.index(jp)] = q
    else:
        joints.append(jp); rots.append(q); trs.append(Gf.Vec3f(C.rest[jp].ExtractTranslation()))
src = open("/home/data/zzhao140/zijian/arena/asset_mirror_people/People/Characters/F_Business_02/person_posed_tuck26.usda").read()
head = src[:src.index("    def SkelAnimation")]


def fq(q):
    i = q.GetImaginary()
    return "(%.7g, %.7g, %.7g, %.7g)" % (q.GetReal(), i[0], i[1], i[2])


body = ("    def SkelAnimation \"Anim\"\n    {\n"
        "        uniform token[] joints = [" + ", ".join('"%s"' % j for j in joints) + "]\n"
        "        quatf[] rotations = [" + ", ".join(fq(q) for q in rots) + "]\n"
        "        half3[] scales = [" + ", ".join("(1, 1, 1)" for _ in joints) + "]\n"
        "        float3[] translations = [" + ", ".join("(%.7g, %.7g, %.7g)" % (t[0], t[1], t[2]) for t in trs) + "]\n"
        "    }\n}\n")
open(out, "w").write(head + body)
print("wrote", out)
