# Adds scene knobs to a galileo_g1_* environment: BG_NAME (background asset), BG_XYZ (background position, rotation kept),
# PICK_XYZ / DEST_XYZ (object poses), FURN ("asset@x,y,z[,yaw_deg];..." extra furniture spawned as library objects).
import sys
p = sys.argv[1]; s = open(p).read()
if "BG_NAME" in s:
    print("already patched", p); sys.exit()
old_bg = '        background = self.asset_registry.get_asset_by_name("galileo_locomanip")()\n'
new_bg = '''        background = self.asset_registry.get_asset_by_name(os.environ.get("BG_NAME", "galileo_locomanip"))()
        if os.environ.get("BG_XYZ"):      # 2026-09-28 second scene: move the room so its floor sits under the robot (rotation kept)
            _bx, _by, _bz = [float(v) for v in os.environ["BG_XYZ"].split(",")]
            _brot = getattr(getattr(background, "initial_pose", None), "rotation_xyzw", None) or (0.0, 0.0, 0.0, 1.0)
            background.set_initial_pose(Pose(position_xyz=(_bx, _by, _bz), rotation_xyzw=tuple(_brot)))
'''
assert old_bg in s, "bg anchor"; s = s.replace(old_bg, new_bg)
old_pick = '''        pick_up_object.set_initial_pose(
            PoseRange(
                position_xyz_min=(0.5785 - XY_RANGE_M, 0.18 - XY_RANGE_M, 0.0707),
                position_xyz_max=(0.5785 + XY_RANGE_M, 0.18 + XY_RANGE_M, 0.0707),
'''
new_pick = '''        _px, _py, _pz = ([float(v) for v in os.environ["PICK_XYZ"].split(",")] if os.environ.get("PICK_XYZ") else (0.5785, 0.18, 0.0707))
        pick_up_object.set_initial_pose(
            PoseRange(
                position_xyz_min=(_px - XY_RANGE_M, _py - XY_RANGE_M, _pz),
                position_xyz_max=(_px + XY_RANGE_M, _py + XY_RANGE_M, _pz),
'''
assert old_pick in s, "pick anchor"; s = s.replace(old_pick, new_pick)
old_dest = '        destination.set_initial_pose(Pose(position_xyz=(-0.2450, -1.6272, -0.2641), rotation_xyzw=(0.0, 0.0, 1.0, 0.0)))\n'
new_dest = '''        _dxyz = tuple(float(v) for v in os.environ["DEST_XYZ"].split(",")) if os.environ.get("DEST_XYZ") else (-0.2450, -1.6272, -0.2641)
        destination.set_initial_pose(Pose(position_xyz=_dxyz, rotation_xyzw=(0.0, 0.0, 1.0, 0.0)))
'''
assert old_dest in s, "dest anchor"; s = s.replace(old_dest, new_dest)
old_assets = '        assets = [background, pick_up_object, destination]\n'
new_assets = '''        assets = [background, pick_up_object, destination]
        for _i, _spec in enumerate([x for x in os.environ.get("FURN", "").split(";") if x.strip()]):   # extra furniture
            _an, _pose = _spec.split("@"); _vals = [float(v) for v in _pose.split(",")]
            _yaw = math.radians(_vals[3]) if len(_vals) > 3 else 0.0
            _f = self.asset_registry.get_asset_by_name(_an.strip())(instance_name=f"furn{_i}", prim_path="{ENV_REGEX_NS}/furn%d" % _i)
            _f.set_initial_pose(Pose(position_xyz=tuple(_vals[:3]), rotation_xyzw=(0.0, 0.0, math.sin(_yaw / 2), math.cos(_yaw / 2))))
            assets.append(_f)
'''
assert old_assets in s, "assets anchor"; s = s.replace(old_assets, new_assets)
open(p, "w").write(s); print("patched", p)
