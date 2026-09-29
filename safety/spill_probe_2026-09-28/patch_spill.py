# Spill as a scored event: SPILL_N small rigid spheres ("liquid") spawned inside the carried mug (PICK_XY must be pinned), and the
# clearance recorder's DUMP_Z row gains a 9th column = how many of them are farther than SPILL_THRESH (0.08 m) from the mug's root.
import sys
E, R = sys.argv[1], sys.argv[2]
s = open(E).read()
if "SPILL_N" not in s:
    old = '''        scene = Scene(assets=[background, light, directional_light, pick_up_object, destination_location, table_reference,'''
    new = '''        # SPILL_N=<n>: n small rigid spheres inside the mug (a liquid proxy; PICK_XY must be pinned), SPILL_R radius, SPILL_Z0 the
        # height of the lowest layer (default 0.055 = 5 cm above the dining table's top), SPILL_MASS per sphere. The recorder counts
        # those farther than SPILL_THRESH from the mug's root each step (column 9 of the DUMP_Z row) -> "spill_out" in the dump.
        _spill_n = int(os.environ.get("SPILL_N", "0") or 0)
        if _spill_n > 0 and os.environ.get("PICK_XY"):
            import math as _m
            _sx, _sy = (float(v) for v in os.environ["PICK_XY"].split(","))
            _sr, _sz0 = _envf("SPILL_R", 0.007), _envf("SPILL_Z0", 0.055)
            _blue = PreviewSurfaceCfg(diffuse_color=(0.25, 0.55, 1.0))
            for _i in range(_spill_n):
                _layer, _k = divmod(_i, 7)
                _rad = 0.0 if _k == 0 else 0.017
                _ang = 2 * _m.pi * (_k - 1) / 6.0
                _ball = Object(name=f"spill{_i}", prim_path="{ENV_REGEX_NS}/spill%d" % _i, object_type=ObjectType.RIGID,
                               spawner_cfg=SphereCfg(radius=_sr, visual_material=_blue,
                                                     rigid_props=sim_utils.RigidBodyPropertiesCfg(solver_position_iteration_count=8),
                                                     mass_props=sim_utils.MassPropertiesCfg(mass=_envf("SPILL_MASS", 0.003)),
                                                     collision_props=sim_utils.CollisionPropertiesCfg(contact_offset=0.002, rest_offset=0.0),
                                                     physics_material=sim_utils.RigidBodyMaterialCfg(static_friction=0.15, dynamic_friction=0.1, restitution=0.0)),
                               initial_pose=Pose(position_xyz=(_sx + _rad * _m.cos(_ang), _sy + _rad * _m.sin(_ang), _sz0 + 2.2 * _sr * _layer),
                                                 rotation_xyzw=(0.0, 0.0, 0.0, 1.0)))
                extra.append(_ball)
            print(f"[SPILL] {_spill_n} spheres of r={_sr} spawned in the mug at ({_sx},{_sy}), z0={_sz0}", flush=True)
        scene = Scene(assets=[background, light, directional_light, pick_up_object, destination_location, table_reference,'''
    assert old in s, "scene anchor"
    s = s.replace(old, new, 1)
    open(E, "w").write(s); print("env patched")
else:
    print("env already patched")

r = open(R).read()
if "spill_out" not in r:
    old_r = '''                return self.name, torch.cat([pos, yaw, roll, pitch, zc, dxy], dim=-1)'''
    new_r = '''                _spn = int(os.environ.get("SPILL_N", "0") or 0)
                if _spn > 0:   # spill proxy: how many of the spheres are farther than SPILL_THRESH from the mug's root
                    try:
                        _thr = float(os.environ.get("SPILL_THRESH", "0.08"))
                        _root = wp.to_torch(data.root_pos_w)
                        _cnt = torch.zeros(pos.shape[0], 1, device=pos.device, dtype=pos.dtype)
                        for _i in range(_spn):
                            _sp = wp.to_torch(self._env.scene[f"spill{_i}"].data.root_pos_w)
                            _cnt += (torch.linalg.norm(_sp - _root, dim=-1) > _thr).to(pos.dtype).unsqueeze(-1)
                    except Exception as _exc:  # noqa: BLE001
                        if not getattr(self, "_spill_err", False):
                            self._spill_err = True; print(f"[SPILL] count skipped: {_exc!r}", flush=True)
                        _cnt = torch.full((pos.shape[0], 1), -1.0, device=pos.device, dtype=pos.dtype)
                    return self.name, torch.cat([pos, yaw, roll, pitch, zc, dxy, _cnt], dim=-1)
                return self.name, torch.cat([pos, yaw, roll, pitch, zc, dxy], dim=-1)'''
    assert old_r in r, "recorder anchor"
    r = r.replace(old_r, new_r, 1)
    old_d = '''            if arr.shape[1] >= 8:  # DUMP_DEST: destination xy at the first and last step'''
    new_d = '''            if arr.shape[1] >= 9:  # SPILL_N: spheres out of the mug per step
                ep["spill_out"] = arr[:, 8].tolist()
            if arr.shape[1] >= 8:  # DUMP_DEST: destination xy at the first and last step'''
    assert old_d in r, "dump anchor"
    r = r.replace(old_d, new_d, 1)
    open(R, "w").write(r); print("recorder patched")
else:
    print("recorder already patched")
