"""Add an opt-in DUMP_Z column (carried-object height) to BoxXYRecorder. Default behaviour byte-identical."""
import os, shutil, sys
p = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena/isaaclab_arena/metrics/person_clearance.py"
t = open(p).read()
if "DUMP_Z" in t.split("DEBUG_Z")[-1] and "box_z" in t:
    print("already patched"); sys.exit(0)
old1 = """        if os.environ.get("DUMP_TILT"):  # T5 load-stability: also emit roll & pitch (tilt)
            roll = torch.atan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x * x + y * y)).unsqueeze(-1)
            pitch = torch.asin(torch.clamp(2.0 * (w * y - z * x), -1.0, 1.0)).unsqueeze(-1)
            return self.name, torch.cat([pos, yaw, roll, pitch], dim=-1)  # (num_envs, 5)"""
new1 = """        if os.environ.get("DUMP_TILT") or os.environ.get("DUMP_Z"):  # T5 load-stability: also emit roll & pitch (tilt)
            roll = torch.atan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x * x + y * y)).unsqueeze(-1)
            pitch = torch.asin(torch.clamp(2.0 * (w * y - z * x), -1.0, 1.0)).unsqueeze(-1)
            if os.environ.get("DUMP_Z"):  # step 3 (Franka): also emit the carried object's world height -> (num_envs, 6)
                zc = wp.to_torch(data.root_pos_w)[:, 2:3]
                return self.name, torch.cat([pos, yaw, roll, pitch, zc], dim=-1)
            return self.name, torch.cat([pos, yaw, roll, pitch], dim=-1)  # (num_envs, 5)"""
old2 = """                ep["box_pitch"] = arr[:, 4].tolist()"""
new2 = """                ep["box_pitch"] = arr[:, 4].tolist()
            if arr.shape[1] >= 6:  # DUMP_Z: carried-object height
                ep["box_z"] = arr[:, 5].tolist()"""
old3 = """            self._zprinted = True
"""
new3 = """            self._zprinted = True
        if os.environ.get("DEBUG_SCENE") and not getattr(self, "_sceneprinted", False):
            self._sceneprinted = True
            try:  # one-off: world bounding boxes of the scene's top-level prims (table height, floor, robot base)
                import omni.usd
                from pxr import Usd, UsdGeom
                stage = omni.usd.get_context().get_stage()
                cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), ["default", "render"])
                root = stage.GetPrimAtPath("/World/envs/env_0")
                prims = list(root.GetChildren()) if root else []
                for pr in prims:
                    kids = [pr] + [c for c in pr.GetChildren()][:12]
                    for c in kids:
                        rg = cache.ComputeWorldBound(c).ComputeAlignedRange()
                        if not rg.IsEmpty():
                            mn, mx = rg.GetMin(), rg.GetMax()
                            print("[DEBUG_SCENE] %-70s min=(%.3f,%.3f,%.3f) max=(%.3f,%.3f,%.3f)" % (str(c.GetPath()), mn[0], mn[1], mn[2], mx[0], mx[1], mx[2]), flush=True)
                for extra in ["/World/GroundPlane", "/World/ground", "/World/defaultGroundPlane"]:
                    pr = stage.GetPrimAtPath(extra)
                    if pr and pr.IsValid():
                        rg = cache.ComputeWorldBound(pr).ComputeAlignedRange()
                        print("[DEBUG_SCENE] " + extra + " min=" + str(rg.GetMin()) + " max=" + str(rg.GetMax()), flush=True)
            except Exception as e:  # noqa: BLE001
                print("[DEBUG_SCENE] failed: " + repr(e), flush=True)
"""
assert t.count(old1) == 1 and t.count(old2) == 1 and t.count(old3) == 1, "anchor mismatch"
t = t.replace(old1, new1).replace(old2, new2).replace(old3, new3)
shutil.copy(p, p + ".preB12")
tmp = p + ".tmp"; open(tmp, "w").write(t); os.replace(tmp, p)
print("patched DUMP_Z")
