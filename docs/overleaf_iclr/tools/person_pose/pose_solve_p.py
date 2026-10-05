# -*- coding: utf-8 -*-
"""Solve a reach whose FOREARM passes through a target point (the capsule centre where it crosses the line), with as little
lean as possible and a straight wrist. Was: a leaning reach with a LEVEL forearm and a straight hand: the coworker whose forearm crosses the transport line at
the payload's height (the crossing-hand clip). The right wrist goes to a target in the character's own frame (facing -y,
root on the floor) while the elbow and the base of the middle finger stay at the wrist's height. Imports the probe tool
for the skeleton handling. Usage:
    pose_solve_h.py <reach_d> <wrist_height> <out.usda>
Bend is split equally over Waist / Spine01 / Spine02 about local +x (forward); shoulder, elbow and wrist flex about local +x.
"""
import sys, itertools, json
import numpy as np
sys.path.insert(0, "/home/data/zzhao140/zijian/isaac/_deploy_tmp")
from pose_probe import Character, J, axis_rot   # noqa: E402
from pxr import Gf   # noqa: E402

reach_d = float(sys.argv[1]) if len(sys.argv) > 1 else 0.40          # horizontal root -> forearm-point distance
wrist_h = float(sys.argv[2]) if len(sys.argv) > 2 else 0.897         # height of that point above the floor
BACK = float(__import__("os").environ.get("BACK", "0.085")); FLOOR_Z = float(__import__("os").environ.get("HAND_ZMIN", "0.72"))
out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/person_cross.usda"

C = Character()
C.set_pose({})
W0 = C.joint_world()
lat = float(W0[J["rh"]][0])
target = np.array([lat, -reach_d, wrist_h])
MID = next(k for k in C.all_joints if k.endswith("R_Hand/R_Mid1"))
q0 = {k: (C.rot_of(J[k]) if J[k] in C.base_joints else Gf.Quatf(C.rest[J[k]].ExtractRotationQuat()))
      for k in ("waist", "sp1", "sp2", "rua", "rfa", "rh")}


def pose_of(tb, ts, te, tw):
    return {J["waist"]: axis_rot(q0["waist"], (1, 0, 0), tb / 3.0),
            J["sp1"]: axis_rot(q0["sp1"], (1, 0, 0), tb / 3.0),
            J["sp2"]: axis_rot(q0["sp2"], (1, 0, 0), tb / 3.0),
            J["rua"]: axis_rot(q0["rua"], (1, 0, 0), ts),
            J["rfa"]: axis_rot(q0["rfa"], (1, 0, 0), te),
            J["rh"]: axis_rot(q0["rh"], (1, 0, 0), tw)}


def evaluate(tb, ts, te, tw):
    C.set_pose(pose_of(tb, ts, te, tw))
    W = C.joint_world()
    w, el, m = W[J["rh"]], W[J["rfa"]], W[MID]
    d = (el - w) / max(float(np.linalg.norm(el - w)), 1e-9)
    P = w + BACK * d                                                    # the forearm point BACK m behind the wrist
    err = float(np.linalg.norm(P - target))
    low = max(0.0, FLOOR_Z - float(m[2])) + max(0.0, FLOOR_Z - float(w[2]))   # hand above the table top
    ahead = max(0.0, float(m[1] - w[1]) + 0.03)                          # fingers ahead (-y) of the wrist
    bend_w = float(__import__("os").environ.get("BEND_W", "0.002"))
    return err + 3.0 * low + 2.0 * ahead + bend_w * tb + 0.0003 * (0.3 * ts + 0.3 * te + 0.5 * abs(tw)), err, low, W


best = None
for tb, ts, te, tw in itertools.product(range(0, 61, 3), range(-10, 91, 4), range(-20, 61, 5), (0,)):
    c, err, lv, _ = evaluate(tb, ts, te, tw)
    if best is None or c < best[0]:
        best = (c, tb, ts, te, tw)
for step in (4.0, 2.0, 1.0):
    _, tb0, ts0, te0, tw0 = best
    for tb, ts, te, tw in itertools.product(*[np.arange(v - 2 * step, v + 2.01 * step, step) for v in (tb0, ts0, te0, tw0)]):
        if tb < 0:
            continue
        c, err, lv, _ = evaluate(tb, ts, te, tw)
        if c < best[0]:
            best = (c, float(tb), float(ts), float(te), float(tw))
_, tb, ts, te, tw = best
c, err, lv, W = evaluate(tb, ts, te, tw)
res = {"bend_deg": round(tb, 1), "shoulder_deg": round(ts, 1), "elbow_deg": round(te, 1), "wrist_deg": round(tw, 1),
       "point_err_m": round(err, 4), "low_m": round(lv, 4), "target": np.round(target, 3).tolist(),
       "wrist": np.round(W[J["rh"]], 3).tolist(), "elbow": np.round(W[J["rfa"]], 3).tolist(),
       "finger_base": np.round(W[MID], 3).tolist(), "head": np.round(W[J["head"]], 3).tolist(),
       "shoulder": np.round(W[J["rua"]], 3).tolist(), "hip": np.round(W[J["hip"]], 3).tolist(),
       "rtoe": np.round(W[J["rtoe"]], 3).tolist()}
print(json.dumps(res))

P = pose_of(tb, ts, te, tw)
joints = list(C.base_joints); rots = list(C.base_rot); trs = list(C.base_tr)
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
