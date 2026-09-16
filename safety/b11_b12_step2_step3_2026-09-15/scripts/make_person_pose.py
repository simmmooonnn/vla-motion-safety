# -*- coding: utf-8 -*-
"""Author a resting pose for the Isaac People character.

The mirrored F_Business_02 character carries a skeleton but no animation, so it renders in its bind (T) pose, which looks
wrong in a figure. This writes person_posed.usda: it references the character and adds a one-sample SkelAnimation that
swings the upper arms down (and bends the elbows slightly), leaving every other joint at its rest transform.

Run with the Arena venv python on chaowei.
"""
import math
from pxr import Usd, UsdGeom, UsdSkel, Gf, Sdf

SRC = "/home/data/zzhao140/zijian/arena/asset_mirror_people/People/Characters/F_Business_02/F_Business_02.usd"
OUT = "/home/data/zzhao140/zijian/arena/asset_mirror_people/People/Characters/F_Business_02/person_posed.usda"

stage = Usd.Stage.Open(SRC)
skel_prim = next(p for p in stage.Traverse() if p.GetTypeName() == "Skeleton")
skel = UsdSkel.Skeleton(skel_prim)
joints = list(skel.GetJointsAttr().Get())
rest = list(skel.GetRestTransformsAttr().Get())          # local matrices, joint order
print("skeleton:", skel_prim.GetPath(), len(joints), "joints")

idx = {j: i for i, j in enumerate(joints)}
parent = {}
for j in joints:
    head = j.rsplit("/", 1)[0] if "/" in j else None
    parent[j] = idx[head] if head in idx else -1

def world(i):
    """Rest world matrix of joint i (compose local matrices up the chain)."""
    m = Gf.Matrix4d(rest[i])
    p = parent[joints[i]]
    while p >= 0:
        m = m * Gf.Matrix4d(rest[p])
        p = parent[joints[p]]
    return m

def find(suffix):
    return next(i for i, j in enumerate(joints) if j.endswith(suffix))

pose = {}   # joint index -> new local matrix
for side, down_deg, out_deg in (("L", 72.0, 8.0), ("R", 72.0, 8.0)):
    up_i = find("/%s_Upperarm" % side)
    hand_i = find("/%s_Hand" % side)
    fore_i = find("/%s_Forearm" % side)
    w_up, w_hand = world(up_i), world(hand_i)
    a = w_up.ExtractTranslation(); b = w_hand.ExtractTranslation()
    cur = (b - a).GetNormalized()                        # arm direction in the bind pose (points outwards)
    sgn = 1.0 if side == "L" else -1.0
    # target: mostly down, tilted slightly away from the body and a little forward
    tgt = Gf.Vec3d(sgn * math.sin(math.radians(out_deg)), 0.12, -math.cos(math.radians(out_deg))).GetNormalized()
    # rotate 'cur' onto 'tgt' by down_deg/90 of the full swing (down_deg=72 keeps a natural, slightly open stance)
    full = Gf.Rotation(Gf.Vec3d(cur), Gf.Vec3d(tgt))
    swing = Gf.Rotation(full.GetAxis(), full.GetAngle() * (down_deg / 90.0))
    w_new = Gf.Matrix4d(1.0).SetRotate(swing) * Gf.Matrix4d(1.0).SetTranslate(a)   # keep the shoulder where it is
    # new world rotation for the joint = swing applied to its current world rotation
    w_cur_rot = Gf.Matrix4d(1.0).SetRotate(w_up.ExtractRotation())
    w_new_rot = w_cur_rot * Gf.Matrix4d(1.0).SetRotate(swing)
    w_new = w_new_rot * Gf.Matrix4d(1.0).SetTranslate(a)
    p_i = parent[joints[up_i]]
    local_new = w_new * world(p_i).GetInverse() if p_i >= 0 else w_new
    pose[up_i] = local_new
    # a slight elbow bend
    bend = Gf.Rotation(Gf.Vec3d(0, 1, 0), sgn * 12.0)
    m_f = Gf.Matrix4d(rest[fore_i])
    pose[fore_i] = Gf.Matrix4d(1.0).SetRotate(bend) * m_f

import os
if os.path.exists(OUT):
    os.remove(OUT)
out = Usd.Stage.CreateNew(OUT)
UsdGeom.SetStageUpAxis(out, UsdGeom.Tokens.z)
UsdGeom.SetStageMetersPerUnit(out, 1.0)
root = out.DefinePrim("/person", "Xform")
out.SetDefaultPrim(root)
ref = out.DefinePrim("/person/mesh")
ref.GetReferences().AddReference(SRC)

anim_path = "/person/Anim"
anim = UsdSkel.Animation.Define(out, anim_path)
drive = sorted(pose)
anim.CreateJointsAttr([joints[i] for i in drive])
tr, ro, sc = [], [], []
for i in drive:
    m = pose[i]
    t = m.ExtractTranslation()
    q = m.ExtractRotationQuat()
    tr.append(Gf.Vec3f(t))
    ro.append(Gf.Quatf(float(q.GetReal()), Gf.Vec3f(*[float(v) for v in q.GetImaginary()])))
    sc.append(Gf.Vec3h(1.0, 1.0, 1.0))
anim.CreateTranslationsAttr(tr)
anim.CreateRotationsAttr(ro)
anim.CreateScalesAttr(sc)

# bind the animation on the referenced SkelRoot
skel_root = None
for p in out.Traverse():
    if p.GetTypeName() == "SkelRoot":
        skel_root = p
        break
assert skel_root is not None, "no SkelRoot under the reference"
binding = UsdSkel.BindingAPI.Apply(skel_root)
binding.CreateAnimationSourceRel().SetTargets([Sdf.Path(anim_path)])
out.GetRootLayer().Save()
print("wrote", OUT, "driving", [joints[i].rsplit('/', 1)[-1] for i in drive])
