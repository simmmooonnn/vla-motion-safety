# Distance from the carried payload (and the gripper just above it) to the rendered coworker's head, torso and arms, per step,
# for the crossing-hand reel clips. The coworker is a kinematic mesh following the scored capsule (REACH_OFF, ROOT_XMIN); her
# joints in the character frame come from the pose solve (pose_solve_p.py output). usage: body_clear.py <mpfull.jsonl>...
import json, sys, math
import numpy as np

OX, OY, XMIN, FLOOR = 0.330, -0.146, 1.00, -0.697
J = {"head": (0.001, -0.308, 1.319), "sh_r": (-0.139, -0.208, 1.28), "sh_l": (0.139, -0.208, 1.28), "hip": (0.0, 0.0, 0.881),
     "el_r": (-0.148, -0.252, 1.024), "wr_r": (-0.144, -0.373, 0.836), "fb_r": (-0.141, -0.423, 0.777), "lh": (0.127, 0.173, 0.983)}
PARTS = [("head", ("head", "head"), 0.11), ("torso", ("hip", "shm"), 0.15), ("upper arm R", ("sh_r", "el_r"), 0.05),
         ("forearm R", ("el_r", "wr_r"), 0.04), ("hand R", ("wr_r", "fb_r"), 0.04), ("arm L", ("sh_l", "lh"), 0.05)]


def world(c, root):
    cx, cy, cz = c
    return np.array([root[0] + cy, root[1] - cx, cz + FLOOR])


def seg_d(p, a, b):
    ab = b - a; t = 0.0 if not ab.any() else max(0.0, min(1.0, float(np.dot(p - a, ab) / np.dot(ab, ab))))
    return float(np.linalg.norm(p - (a + t * ab)))


for f in sys.argv[1:]:
    rows = [json.loads(x) for x in open(f, encoding="utf-8") if x.strip()]
    lay = rows[0]["layout"]; ix = {k: i for i, k in enumerate(lay)}
    best = {}
    for r in rows[1:]:
        if not isinstance(r, list):
            continue
        mx, my = r[ix["mover_x"]], r[ix["mover_y"]]
        root = (max(mx + OX, XMIN), my + OY)
        W = {k: world(v, root) for k, v in J.items()}
        W["shm"] = (W["sh_r"] + W["sh_l"]) / 2
        obj = np.array([r[ix["obj_x"]], r[ix["obj_y"]], r[ix["obj_z"]]])
        for nm, (a, b), rad in PARTS:
            for lab, p, pr in (("payload", obj, 0.05), ("gripper", obj + np.array([0, 0, 0.15]), 0.06)):
                d = seg_d(p, W[a], W[b]) - rad - pr
                k = (nm, lab)
                if k not in best or d < best[k][0]:
                    best[k] = (d, r[ix["t"]], obj.round(3).tolist())
    print("==", f.split("/")[-1].split("\\")[-1])
    for (nm, lab), (d, t, o) in sorted(best.items(), key=lambda kv: kv[1][0])[:6]:
        print(f"   {nm:12s} {lab:8s} min surface gap {d:+.3f} m at t={t:.2f}s payload {o}")
