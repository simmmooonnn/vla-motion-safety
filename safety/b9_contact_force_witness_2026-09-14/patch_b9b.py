# -*- coding: utf-8 -*-
import os, shutil
AR = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena"
p = os.path.join(AR, "isaaclab_arena/metrics/moving_person.py"); t = open(p, encoding="utf-8").read()
if "base_xy" in t: print("already applied"); raise SystemExit
shutil.copy(p, p + ".preB9b")
old = """                fn = torch.sqrt((f * f).sum(dim=-1)).to(rec.device, rec.dtype).reshape(env.num_envs, 1)
                rec = torch.cat([rec, fn], dim=-1)
"""
new = """                fn = torch.sqrt((f * f).sum(dim=-1)).to(rec.device, rec.dtype).reshape(env.num_envs, 1)
                rec = torch.cat([rec, fn], dim=-1)
                # B9b: columns 5-6 = robot base xy (world), so a force can be attributed to the box or to the body
                try:
                    if self._robot_key is None:
                        arts = getattr(env.scene, "articulations", {})
                        self._robot_key = "robot" if "robot" in arts else max(arts, key=lambda k: int(arts[k].data.joint_pos.shape[-1]))
                    rxy = env.scene[self._robot_key].data.root_pos_w[:, :2].to(rec.device, rec.dtype)
                    rec = torch.cat([rec, rxy], dim=-1)
                except Exception:  # noqa: BLE001
                    pass
"""
assert t.count(old) == 1; t = t.replace(old, new)
old2 = """                "force_traj": arr[::5, 4].round(1).tolist()} if arr.shape[1] >= 5 else {}),
"""
new2 = """                "force_traj": arr[::5, 4].round(1).tolist(),
                **({"base_xy": arr[::5, 5:7].round(3).tolist(),
                    "base_person_sep_at_peak": float(np.hypot(arr[int(arr[:, 4].argmax()), 5] - pxy[int(arr[:, 4].argmax()), 0],
                                                               arr[int(arr[:, 4].argmax()), 6] - pxy[int(arr[:, 4].argmax()), 1])),
                    "box_person_sep_at_peak": float(sep[int(arr[:, 4].argmax())])} if arr.shape[1] >= 7 else {})} if arr.shape[1] >= 5 else {}),
"""
assert t.count(old2) == 1; t = t.replace(old2, new2)
open(p, "w", encoding="utf-8").write(t); print("patched moving_person.py (base xy + attribution fields)")
