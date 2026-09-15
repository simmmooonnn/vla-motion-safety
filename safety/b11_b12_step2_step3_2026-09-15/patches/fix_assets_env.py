"""(1) object_library: scissors back to the Nucleus path (chaowei has internet); other ARCH-mirror paths -> chaowei mirror.
(2) franka env: attach the payload recorder whenever DUMP_TILT / DUMP_Z is set (T4 cells have no bystander)."""
import os, shutil
lib = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena/isaaclab_arena/assets/object_library.py"
t = open(lib).read()
old = 'usd_path = f"/weka/scratch/aszalay1/zijian/arena/asset_mirror/Arena/assets/object_library/srl_robolab_assets/objects/ycb/scissors.usd"'
new = 'usd_path = f"{ARENA_NUCLEUS_DIR}/Arena/assets/object_library/srl_robolab_assets/objects/ycb/scissors.usd"'
n1 = t.count(old)
t = t.replace(old, new)
n2 = t.count("/weka/scratch/aszalay1/zijian/arena/asset_mirror")
t = t.replace("/weka/scratch/aszalay1/zijian/arena/asset_mirror", "/home/data/zzhao140/zijian/arena/asset_mirror")
shutil.copy(lib, lib + ".preB12")
tmp = lib + ".tmp"; open(tmp, "w").write(t); os.replace(tmp, lib)
print(f"object_library: scissors->nucleus {n1}, mirror paths fixed {n2}")
env = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena/isaaclab_arena_environments/franka_safety_table_environment.py"
e = open(env).read()
o2 = 'if os.environ.get("T1_HAZARD") or os.environ.get("BYSTANDER"):'
n2_ = 'if os.environ.get("T1_HAZARD") or os.environ.get("BYSTANDER") or os.environ.get("DUMP_TILT") or os.environ.get("DUMP_Z"):'
assert e.count(o2) == 1
e = e.replace(o2, n2_)
tmp = env + ".tmp"; open(tmp, "w").write(e); os.replace(tmp, env)
print("env: recorder attached for DUMP_TILT/DUMP_Z")
