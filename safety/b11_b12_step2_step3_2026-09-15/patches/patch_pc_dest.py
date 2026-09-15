"""Step 3: with DUMP_Z the recorder also logs the destination's xy (object named by DUMP_DEST) -> 8 columns; dump gets dest_xy0/1.
Default behaviour (no DUMP_Z) byte-identical."""
import os, shutil, sys
p = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena/isaaclab_arena/metrics/person_clearance.py"
t = open(p).read()
if "DUMP_DEST" in t:
    print("already patched (dest)"); sys.exit(0)
old1 = """            if os.environ.get("DUMP_Z"):  # step 3 (Franka): also emit the carried object's world height -> (num_envs, 6)
                zc = wp.to_torch(data.root_pos_w)[:, 2:3]
                return self.name, torch.cat([pos, yaw, roll, pitch, zc], dim=-1)"""
new1 = """            if os.environ.get("DUMP_Z"):  # step 3 (Franka): + carried-object height, + destination xy (DUMP_DEST) -> (num_envs, 8)
                zc = wp.to_torch(data.root_pos_w)[:, 2:3]
                dn = os.environ.get("DUMP_DEST", "")
                try:
                    dxy = wp.to_torch(self._env.scene[dn].data.root_pos_w)[:, :2] if dn else torch.zeros_like(pos)
                except Exception:  # noqa: BLE001
                    dxy = torch.zeros_like(pos)
                return self.name, torch.cat([pos, yaw, roll, pitch, zc, dxy], dim=-1)"""
old2 = """            if arr.shape[1] >= 6:  # DUMP_Z: carried-object height
                ep["box_z"] = arr[:, 5].tolist()"""
new2 = """            if arr.shape[1] >= 6:  # DUMP_Z: carried-object height
                ep["box_z"] = arr[:, 5].tolist()
            if arr.shape[1] >= 8:  # DUMP_DEST: destination xy at the first and last step
                ep["dest_xy0"] = arr[0, 6:8].tolist(); ep["dest_xy1"] = arr[-1, 6:8].tolist()"""
old3 = """        q = wp.to_torch(data.root_quat_w)          # (num_envs, 4) = (w, x, y, z)
"""
new3 = """        if os.environ.get("DEBUG_MESH") and not getattr(self, "_meshprinted", False):
            self._meshprinted = True
            try:  # one-off: width profile of the carried object's mesh along its long axis, in the object's root frame
                import omni.usd
                from pxr import Gf, Usd, UsdGeom
                stage = omni.usd.get_context().get_stage()
                root = stage.GetPrimAtPath("/World/envs/env_0/" + str(self.object_name))
                inv = UsdGeom.Xformable(root).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).GetInverse()
                allp = []
                for c in Usd.PrimRange(root):
                    if c.IsA(UsdGeom.Mesh):
                        pts = UsdGeom.Mesh(c).GetPointsAttr().Get() or []
                        m = UsdGeom.Xformable(c).ComputeLocalToWorldTransform(Usd.TimeCode.Default()) * inv
                        allp += [list(m.Transform(Gf.Vec3d(*p))) for p in pts]
                P = np.asarray(allp)
                lo, hi = P.min(0), P.max(0); ext = hi - lo; ax = int(np.argmax(ext)); oth = [i for i in range(3) if i != ax]
                print("[DEBUG_MESH] %s npts=%d extent=%s long_axis=%d centroid=%s bbox_center=%s" % (self.object_name, len(P), np.round(ext, 3).tolist(), ax, np.round(P.mean(0), 3).tolist(), np.round((lo + hi) / 2, 3).tolist()), flush=True)
                edges = np.linspace(lo[ax], hi[ax], 11)
                prof = []
                for b in range(10):
                    s = P[(P[:, ax] >= edges[b]) & (P[:, ax] <= edges[b + 1])]
                    prof.append((round(float(edges[b]), 3), len(s), round(float(np.ptp(s[:, oth[0]])) if len(s) else 0.0, 3), round(float(np.ptp(s[:, oth[1]])) if len(s) else 0.0, 3)))
                print("[DEBUG_MESH] profile (bin_start, npts, width_a, width_b): " + str(prof), flush=True)
            except Exception as e:  # noqa: BLE001
                print("[DEBUG_MESH] failed: " + repr(e), flush=True)
        q = wp.to_torch(data.root_quat_w)          # (num_envs, 4) = (w, x, y, z)
"""
assert t.count(old1) == 1 and t.count(old2) == 1 and t.count(old3) == 1, "anchor mismatch"
t = t.replace(old1, new1).replace(old2, new2).replace(old3, new3)
shutil.copy(p, p + ".preB12dest")
tmp = p + ".tmp"; open(tmp, "w").write(t); os.replace(tmp, p)
print("patched DUMP_DEST")
