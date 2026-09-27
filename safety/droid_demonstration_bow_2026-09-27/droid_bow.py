# The lateral bow of human teleoperation transports in DROID (droid_100 sample), measured exactly as the paper's drift field:
# for every grasp-to-release transport, the largest perpendicular excursion of the end effector from the straight grasp-to-release
# chord in the base XY plane, signed OUTWARD (away from the robot base) vs inward. Also the bow a constant-radius sweep about the
# base would produce (the chord's sagitta), so a measured bow can be read against the "rotate about the base" motion prior.
import glob, json, math, sys
import numpy as np
from tfrecord.reader import tfrecord_loader

D = "/home/data/zzhao140/zijian/droid_100"
desc = {"steps/observation/cartesian_position": "float", "steps/observation/gripper_position": "float",
        "steps/language_instruction": "byte"}
trans = []
n_ep = 0
for f in sorted(glob.glob(D + "/r2d2_faceblur-train.tfrecord-*")):
    for ex in tfrecord_loader(f, None, desc):
        n_ep += 1
        cp = np.asarray(ex["steps/observation/cartesian_position"], dtype=float).reshape(-1, 6)
        gp = np.asarray(ex["steps/observation/gripper_position"], dtype=float).reshape(-1)
        T = min(len(cp), len(gp))
        cp, gp = cp[:T], gp[:T]
        lang = ex["steps/language_instruction"]
        try:
            lang = (lang[0] if isinstance(lang, (list, np.ndarray)) else lang)
            lang = lang.decode() if isinstance(lang, (bytes, bytearray)) else str(lang)
        except Exception:
            lang = ""
        closed = gp > 0.5
        k = 0
        while k < T:
            if closed[k] and (k == 0 or not closed[k - 1]):
                j = k
                while j < T and closed[j]:
                    j += 1
                # transport = closed stretch k..j-1
                seg = cp[k:j, :2]
                if j - k >= 15:
                    p0, p1 = seg[0], seg[-1]
                    c = np.linalg.norm(p1 - p0)
                    if c >= 0.15:
                        u = (p1 - p0) / c
                        n = np.array([-u[1], u[0]])
                        mid = (p0 + p1) / 2
                        s_out = 1.0 if np.dot(n, mid) >= 0 else -1.0      # +n points away from the base at the chord midpoint
                        e = (seg - p0) @ n * s_out                         # outward-signed excursion per step
                        r0, r1 = np.linalg.norm(p0), np.linalg.norm(p1)
                        rm = (r0 + r1) / 2
                        sag = rm - math.sqrt(max(rm * rm - (c / 2) ** 2, 0.0))
                        trans.append({"ep": n_ep, "steps": int(j - k), "chord": float(c), "out_max": float(e.max()),
                                      "in_max": float(-e.min()), "sagitta": float(sag), "r0": float(r0), "r1": float(r1),
                                      "lang": lang[:60]})
                k = j
            else:
                k += 1

out = np.array([t["out_max"] for t in trans]); inn = np.array([t["in_max"] for t in trans]); sag = np.array([t["sagitta"] for t in trans])
res = {"episodes": n_ep, "transports": len(trans),
       "out_med": float(np.median(out)) if len(out) else None, "in_med": float(np.median(inn)) if len(inn) else None,
       "out_q1": float(np.percentile(out, 25)) if len(out) else None, "out_q3": float(np.percentile(out, 75)) if len(out) else None,
       "frac_out_gt_in": float(np.mean(out > inn)) if len(out) else None,
       "frac_out_gt_2cm": float(np.mean(out > 0.02)) if len(out) else None,
       "frac_in_gt_2cm": float(np.mean(inn > 0.02)) if len(out) else None,
       "sag_med": float(np.median(sag)) if len(sag) else None,
       "ratio_out_over_sag_med": float(np.median(out / np.maximum(sag, 1e-3))) if len(sag) else None,
       "chord_med": float(np.median([t["chord"] for t in trans])) if trans else None,
       "transports_list": trans}
json.dump(res, open(D + "/droid_bow.json", "w"), indent=1)
print({k: v for k, v in res.items() if k != "transports_list"})
