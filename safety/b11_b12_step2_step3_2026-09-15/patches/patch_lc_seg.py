"""T2 on the tabletop: LinkClearanceRecorder also scores the bystander's forearm resting on the table, a capsule segment
T4_SEG="x0,y0,z0,x1,y1,z1,r" (world); per-link distance = min(body capsule, head, forearm). Default unchanged."""
import os, shutil, sys
p = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena/isaaclab_arena/metrics/link_clearance.py"
t = open(p).read()
if "T4_SEG" in t:
    print("already patched (seg)"); sys.exit(0)
old = """        minv, mini = torch.min(dxy, dim=1)           # (num_envs,), (num_envs,)"""
new = """        if os.environ.get("T4_SEG"):                  # step 3: forearm resting on the table (capsule segment)
            try:
                v = [float(s) for s in os.environ["T4_SEG"].split(",")]
                a = torch.tensor(v[0:3], device=bp.device, dtype=bp.dtype); b = torch.tensor(v[3:6], device=bp.device, dtype=bp.dtype)
                ab = b - a; l2 = (ab * ab).sum().clamp(min=1e-9)
                tt = (((bp - a) * ab).sum(-1) / l2).clamp(0.0, 1.0)            # (num_envs, num_bodies)
                cp = a + tt.unsqueeze(-1) * ab
                dseg = torch.sqrt(((bp - cp) ** 2).sum(-1)) - v[6]
                dxy = torch.minimum(dxy, dseg.clamp(min=0.0))
            except Exception:  # noqa: BLE001
                pass
        minv, mini = torch.min(dxy, dim=1)           # (num_envs,), (num_envs,)"""
assert t.count(old) == 1, "anchor mismatch"
t = t.replace(old, new)
shutil.copy(p, p + ".preB12seg")
tmp = p + ".tmp"; open(tmp, "w").write(t); os.replace(tmp, p)
print("patched T4_SEG")
