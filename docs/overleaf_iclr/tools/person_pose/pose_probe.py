# -*- coding: utf-8 -*-
"""Offline pose tool for the F_Business_02 character (runs with the Arena venv's pxr on chaowei, no simulator).

Stage 1 (this file, mode 'axes'): find which way the character faces at yaw 0, where its right hand sits in the tucked
pose, and which local axis of Waist / Spine01 / Spine02 / R_Upperarm / R_Forearm bends the body forward or swings the arm
forward -- by applying +30 deg about each local axis and watching the right hand move.
"""
import sys, math, json
import numpy as np
from pxr import Usd, UsdSkel, UsdGeom, Gf, Sdf, Vt

BASE = "/home/data/zzhao140/zijian/arena/asset_mirror_people/People/Characters/F_Business_02/person_posed_tuck26.usda"
J = {
    "waist": "RL_BoneRoot/Hip/Waist",
    "sp1": "RL_BoneRoot/Hip/Waist/Spine01",
    "sp2": "RL_BoneRoot/Hip/Waist/Spine01/Spine02",
    "rcl": "RL_BoneRoot/Hip/Waist/Spine01/Spine02/R_Clavicle",
    "rua": "RL_BoneRoot/Hip/Waist/Spine01/Spine02/R_Clavicle/R_Upperarm",
    "rfa": "RL_BoneRoot/Hip/Waist/Spine01/Spine02/R_Clavicle/R_Upperarm/R_Forearm",
    "rh": "RL_BoneRoot/Hip/Waist/Spine01/Spine02/R_Clavicle/R_Upperarm/R_Forearm/R_Hand",
    "lua": "RL_BoneRoot/Hip/Waist/Spine01/Spine02/L_Clavicle/L_Upperarm",
    "lfa": "RL_BoneRoot/Hip/Waist/Spine01/Spine02/L_Clavicle/L_Upperarm/L_Forearm",
    "head": "RL_BoneRoot/Hip/Waist/Spine01/Spine02/NeckTwist01/NeckTwist02/Head",
    "hip": "RL_BoneRoot/Hip",
    "rfoot": "RL_BoneRoot/Hip/Pelvis/R_Thigh/R_Calf/R_Foot",
    "rtoe": "RL_BoneRoot/Hip/Pelvis/R_Thigh/R_Calf/R_Foot/R_ToeBase",
}


class Character:
    def __init__(self):
        self.stage = Usd.Stage.Open(BASE)
        self.anim = UsdSkel.Animation(self.stage.GetPrimAtPath("/person/Anim"))
        self.base_joints = list(self.anim.GetJointsAttr().Get())
        self.base_rot = [Gf.Quatf(q) for q in self.anim.GetRotationsAttr().Get()]
        self.base_tr = list(self.anim.GetTranslationsAttr().Get())
        self.cache = UsdSkel.Cache()
        self.skel = None
        for p in self.stage.Traverse():
            if p.IsA(UsdSkel.Skeleton):
                self.skel = UsdSkel.Skeleton(p)
                break
        self.all_joints = list(self.skel.GetJointsAttr().Get())
        rest = self.skel.GetRestTransformsAttr().Get()
        self.rest = {self.all_joints[i]: rest[i] for i in range(len(self.all_joints))}
        root = None
        for p in self.stage.Traverse():
            if p.IsA(UsdSkel.Root):
                root = UsdSkel.Root(p)
                break
        self.root = root
        self.l2w = np.array(UsdGeom.Xformable(self.skel.GetPrim()).ComputeLocalToWorldTransform(Usd.TimeCode.Default()))

    def set_pose(self, extra):
        """extra: dict joint_path -> Gf.Quatf local rotation (overrides / adds to the tucked pose). Joints not in the base
        animation take their rest translation, so adding a joint does not move it."""
        joints = list(self.base_joints)
        rots = list(self.base_rot)
        trs = list(self.base_tr)
        for jp, q in extra.items():
            if jp in joints:
                rots[joints.index(jp)] = q
            else:
                joints.append(jp)
                rots.append(q)
                trs.append(Gf.Vec3f(self.rest[jp].ExtractTranslation()))
        self.anim.GetJointsAttr().Set(Vt.TokenArray(joints))
        self.anim.GetRotationsAttr().Set(Vt.QuatfArray(rots))
        self.anim.GetTranslationsAttr().Set(Vt.Vec3fArray(trs))
        self.anim.GetScalesAttr().Set(Vt.Vec3hArray([Gf.Vec3h(1, 1, 1)] * len(joints)))
        self.cache = UsdSkel.Cache()
        self.cache.Populate(self.root, Usd.TraverseInstanceProxies())

    def joint_world(self):
        sq = self.cache.GetSkelQuery(self.skel)
        xfs = sq.ComputeJointSkelTransforms(Usd.TimeCode.Default())
        out = {}
        order = list(sq.GetJointOrder())
        for i, jp in enumerate(order):
            m = np.array(xfs[i]) @ self.l2w
            out[jp] = m[3, :3].copy()
        return out

    def rot_of(self, jp):
        joints = list(self.anim.GetJointsAttr().Get())
        rots = self.anim.GetRotationsAttr().Get()
        if jp in joints:
            return Gf.Quatf(rots[joints.index(jp)])
        r = self.rest[jp].ExtractRotationQuat()
        return Gf.Quatf(r)


def axis_rot(base_q, axis, deg):
    """Post-multiply a rotation about a LOCAL axis onto the joint's current local rotation."""
    q = Gf.Quatf(float(math.cos(math.radians(deg) / 2)), Gf.Vec3f(*[float(a * math.sin(math.radians(deg) / 2)) for a in axis]))
    return base_q * q


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "axes"
    C = Character()
    C.set_pose({})
    W = C.joint_world()
    fwd = W[J["rtoe"]] - W[J["rfoot"]]
    fwd[2] = 0
    fwd /= np.linalg.norm(fwd)
    print("facing (toe - foot, horizontal):", np.round(fwd, 3).tolist())
    for k in ("hip", "head", "rua", "rh", "rfoot"):
        print("  %-6s %s" % (k, np.round(W[J[k]], 3).tolist()))
    base_hand = W[J["rh"]]
    print("right hand height above the feet: %.3f m" % (base_hand[2] - W[J["rfoot"]][2]))
    if mode == "axes":
        for k in ("waist", "sp1", "sp2", "rua", "rfa"):
            for ax, nm in (((1, 0, 0), "x"), ((0, 1, 0), "y"), ((0, 0, 1), "z")):
                C.set_pose({J[k]: axis_rot(C.rot_of(J[k]) if J[k] in C.base_joints else Gf.Quatf(C.rest[J[k]].ExtractRotationQuat()), ax, 30)})
                W2 = C.joint_world()
                d = W2[J["rh"]] - base_hand
                print("  %-5s +30 about local %s -> right hand moves %s  (forward %.3f, up %.3f)" % (
                    k, nm, np.round(d, 3).tolist(), float(d @ fwd), float(d[2])))
                C.set_pose({})
