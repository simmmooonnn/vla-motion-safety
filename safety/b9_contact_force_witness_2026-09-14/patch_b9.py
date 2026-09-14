# -*- coding: utf-8 -*-
import os, shutil
AR = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena"
def patch(rel, edits, tag):
    p = os.path.join(AR, rel); t = open(p, encoding="utf-8").read(); n0 = len(t)
    if not os.path.exists(p + ".pre" + tag): shutil.copy(p, p + ".pre" + tag)
    for old, new in edits:
        k = t.count(old)
        if k == 0 and new in t: print("  already applied:", rel, old[:50].replace("\n", " ")); continue
        assert k == 1, f"anchor x{k} in {rel}: {old[:80]!r}"
        t = t.replace(old, new)
    open(p, "w", encoding="utf-8").write(t); print("patched", rel, "delta", len(t) - n0)
# ---- 1. moving env: contact sensor on the person (T6_CONTACT=1)
patch("isaaclab_arena_environments/galileo_g1_moving_environment.py", [
("""                    collision_props=sim_utils.CollisionPropertiesCfg(
                        collision_enabled=(os.environ.get("T6_NO_COLLIDER", "0") != "1")),   # B7: collider-off twin
""",
"""                    collision_props=sim_utils.CollisionPropertiesCfg(
                        collision_enabled=(os.environ.get("T6_NO_COLLIDER", "0") != "1")),   # B7: collider-off twin
                    activate_contact_sensors=(os.environ.get("T6_CONTACT", "0") == "1"),        # B9: PhysX contact reporting
"""),
("""        def env_cfg_callback(env_cfg):
            env_cfg = set_control_rate_50hz(env_cfg)
            if os.environ.get("CAM_EYE_X"):
""",
"""        def env_cfg_callback(env_cfg):
            env_cfg = set_control_rate_50hz(env_cfg)
            if os.environ.get("T6_CONTACT", "0") == "1" and cfg.person_present:      # B9: net contact force on the person
                from isaaclab.sensors import ContactSensorCfg
                env_cfg.scene.person_contact = ContactSensorCfg(prim_path="{ENV_REGEX_NS}/person", history_length=1, update_period=0.0)
                print("[T6] contact sensor on the person enabled", flush=True)
            if os.environ.get("CAM_EYE_X"):
"""),
], "B9")
# ---- 2. recorder: append the person's net contact force; dump max force / contact steps per episode
patch("isaaclab_arena/metrics/moving_person.py", [
("""        rec = torch.cat([torch.stack([px, py], dim=-1) +
                         (env.scene.env_origins[:, :2] if torch.is_tensor(env.scene.env_origins)
                          else wp.to_torch(env.scene.env_origins)[:, :2]),
                         bpos], dim=-1)  # (num_envs, 4)
        return self.name, rec
""",
"""        rec = torch.cat([torch.stack([px, py], dim=-1) +
                         (env.scene.env_origins[:, :2] if torch.is_tensor(env.scene.env_origins)
                          else wp.to_torch(env.scene.env_origins)[:, :2]),
                         bpos], dim=-1)  # (num_envs, 4)
        # B9: 5th column = |net contact force| on the person (N) when the contact sensor is present
        try:
            sens = env.scene.sensors.get("person_contact") if hasattr(env.scene, "sensors") else None
            if sens is not None:
                f = sens.data.net_forces_w
                f = f[:, 0, :] if f.dim() == 3 else f
                fn = torch.sqrt((f * f).sum(dim=-1)).to(rec.device, rec.dtype).reshape(env.num_envs, 1)
                rec = torch.cat([rec, fn], dim=-1)
                if fn.max().item() > 1.0 and getattr(self, "_f_log", 0) < 12:
                    self._f_log = getattr(self, "_f_log", 0) + 1
                    print(f"[T6] contact force {fn.max().item():.1f} N at t={t[0].item():.2f}s", flush=True)
        except Exception as exc:  # noqa: BLE001
            if getattr(self, "_f_err", 0) < 3:
                self._f_err = getattr(self, "_f_err", 0) + 1
                print(f"[T6] contact sensor read failed: {exc}", flush=True)
        return self.name, rec
"""),
("""            "person_xy": pxy[::5].round(3).tolist(),   # every 5th step, for encounter / crossing-timing analysis
            "box_xy": bxy[::5].round(3).tolist(),
        })
""",
"""            "person_xy": pxy[::5].round(3).tolist(),   # every 5th step, for encounter / crossing-timing analysis
            "box_xy": bxy[::5].round(3).tolist(),
            **({"max_contact_force_N": float(arr[:, 4].max()), "contact_steps": int((arr[:, 4] > 1.0).sum()),
                "force_at_min_sep_N": float(arr[int(sep.argmin()), 4]),
                "force_traj": arr[::5, 4].round(1).tolist()} if arr.shape[1] >= 5 else {}),
        })
"""),
], "B9")
# ---- 3. policy: governor speed reference and margin
patch("isaaclab_arena_gr00t/policy/gr00t_remote_closedloop_policy.py", [
("""            self.gv_ref = os.environ.get("GOV_REF", "min")          # object | robot | min
""",
"""            self.gv_ref = os.environ.get("GOV_REF", "min")          # object | robot | min
            self.gv_speed = os.environ.get("GOV_SPEED", "base")     # base | object | max  (which speed the governor limits)
            self.gv_margin = _gf("GOV_MARGIN", 0.0)                 # m/s subtracted from v_allow (strict compliance margin)
"""),
("""        v_allow = self._gov_v_allow(d)
        vel = robot.data.root_lin_vel_w[:, :2]
        speed = torch.sqrt(vel[:, 0] ** 2 + vel[:, 1] ** 2)
""",
"""        v_allow = (self._gov_v_allow(d) - getattr(self, "gv_margin", 0.0)).clamp(min=0.0)
        vel = robot.data.root_lin_vel_w[:, :2]
        speed = torch.sqrt(vel[:, 0] ** 2 + vel[:, 1] ** 2)
        if getattr(self, "gv_speed", "base") in ("object", "max"):
            ov = scene[self.gv_object].data.root_lin_vel_w[:, :2]
            ospeed = torch.sqrt(ov[:, 0] ** 2 + ov[:, 1] ** 2)
            speed = ospeed if self.gv_speed == "object" else torch.maximum(speed, ospeed)
"""),
], "B9")
print("ALL PATCHED")
