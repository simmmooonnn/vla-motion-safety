# -*- coding: utf-8 -*-
"""B7 patches (2026-09-13). Each edit is anchor-asserted; originals are kept as *.preB7."""
import os, shutil, sys
AR = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena"
def patch(rel, edits):
    p = os.path.join(AR, rel); t = open(p, encoding="utf-8").read(); n0 = len(t)
    if not os.path.exists(p + ".preB7"): shutil.copy(p, p + ".preB7")
    for old, new in edits:
        k = t.count(old)
        if k == 0 and new in t: print("  already applied:", rel, old[:50].replace("\n", " ")); continue
        assert k == 1, f"anchor x{k} in {rel}: {old[:80]!r}"
        t = t.replace(old, new)
    open(p, "w", encoding="utf-8").write(t); print("patched", rel, "delta", len(t) - n0)

# ---------------------------------------------------------------- 1. moving_person.py: trigger / delay / stop distance + richer dump
patch("isaaclab_arena/metrics/moving_person.py", [
("""_DEFAULT_DUMP = "/weka/scratch/aszalay1/zijian/isaac/logs/moving_person_dump.json"
""",
"""_DEFAULT_DUMP = "/weka/scratch/aszalay1/zijian/isaac/logs/moving_person_dump.json"


def _envf_opt(name):
    v = os.environ.get(name, "")
    try:
        return float(v) if v != "" else None
    except ValueError:
        return None
"""),
("""        self._dt = float(getattr(self._env, "step_dt", 0.02) or 0.02)
""",
"""        self._dt = float(getattr(self._env, "step_dt", 0.02) or 0.02)
        # B7 knobs: the person can WAIT at its start point until the robot base passes T6_TRIGGER_Y (robot-triggered
        # crossing, needed for realistic crossing speeds), or until T6_DELAY seconds; T6_STOP_DIST stops it after that
        # path length (it reaches the far side and stands). Defaults (all unset) reproduce the original p = start + v t.
        self._trig_y = _envf_opt("T6_TRIGGER_Y")
        self._delay = _envf_opt("T6_DELAY")
        self._stop_dist = _envf_opt("T6_STOP_DIST")
        self._t0 = None; self._last_t = None; self._robot_key = None; self._trig_log = 0
        if self._trig_y is not None or self._delay is not None or self._stop_dist is not None:
            print(f"[T6] crossing knobs trigger_y={self._trig_y} delay={self._delay} stop_dist={self._stop_dist}", flush=True)

    def _robot_y(self):
        scene = self._env.scene
        if self._robot_key is None:
            arts = getattr(scene, "articulations", {})
            self._robot_key = "robot" if "robot" in arts else max(arts, key=lambda k: int(arts[k].data.joint_pos.shape[-1]))
        org = scene.env_origins if torch.is_tensor(scene.env_origins) else wp.to_torch(scene.env_origins)
        return scene[self._robot_key].data.root_pos_w[:, 1] - org[:, 1]

    def _motion_time(self, t):
        \"\"\"Seconds the person has been walking: t (default); t - T6_DELAY; or time since the robot base first
        crossed T6_TRIGGER_Y (the person waits at its start point until then). Per env; re-armed with the episode clock.\"\"\"
        if self._trig_y is None and self._delay is None:
            return t
        if self._t0 is None or self._t0.shape[0] != t.shape[0]:
            self._t0 = torch.full_like(t, float("nan")); self._last_t = t.clone()
        reset = t < self._last_t                        # episode clock went backwards -> new episode
        self._t0[reset] = float("nan"); self._last_t = t.clone()
        if self._delay is not None:
            return (t - self._delay).clamp(min=0.0)
        try:
            ry = self._robot_y()
        except Exception:  # noqa: BLE001
            return t
        arm = torch.isnan(self._t0) & (ry < self._trig_y)
        if arm.any():
            self._t0[arm] = t[arm]
            if self._trig_log < 30:
                self._trig_log += 1
                print(f"[T6] person triggered t={t[arm][0].item():.2f}s robot_y={ry[arm][0].item():.2f}", flush=True)
        return torch.where(torch.isnan(self._t0), torch.zeros_like(t), (t - self._t0).clamp(min=0.0))
"""),
("""        t = self._episode_time()                       # (num_envs,)
        px = self.sx + self.vx * t                     # (num_envs,)
        py = self.sy + self.vy * t
""",
"""        t = self._episode_time()                       # (num_envs,)
        tau = self._motion_time(t)                     # walking time (trigger / delay aware)
        if self._stop_dist is not None:
            spd = float((self.vx ** 2 + self.vy ** 2) ** 0.5)
            if spd > 1e-9:
                tau = tau.clamp(max=self._stop_dist / spd)
        px = self.sx + self.vx * tau                   # (num_envs,)
        py = self.sy + self.vy * tau
"""),
("""            "sep_traj": sep.tolist(),
        })
""",
"""            "sep_traj": sep.tolist(),
            "person_xy": pxy[::5].round(3).tolist(),   # every 5th step, for encounter / crossing-timing analysis
            "box_xy": bxy[::5].round(3).tolist(),
        })
"""),
])

# ---------------------------------------------------------------- 2. moving env: collider-off twin
patch("isaaclab_arena_environments/galileo_g1_moving_environment.py", [
("""                    collision_props=sim_utils.CollisionPropertiesCfg(),
""",
"""                    collision_props=sim_utils.CollisionPropertiesCfg(
                        collision_enabled=(os.environ.get("T6_NO_COLLIDER", "0") != "1")),   # B7: collider-off twin
"""),
])

# ---------------------------------------------------------------- 3. policy: protective-stop reference layer
pol = "isaaclab_arena_gr00t/policy/gr00t_remote_closedloop_policy.py"
src = open(os.path.join(AR, pol), encoding="utf-8").read()
imp = [] if "\nimport json\n" in src else [("import os\n", "import json\nimport os\n")]
patch(pol, imp + [
("""    # ---------------------- Policy interface -------------------
""",
"""        # --- B7 protective-stop reference layer (env-gated): zero the navigation command while the person is closer
        # than STOP_MARGIN (hysteresis STOP_HYST), count demands per episode, dump per-episode stats to STOP_DUMP ---
        self._stop_on = os.environ.get("STOP", "0") == "1"
        if self._stop_on:
            def _sf(name, default):
                try:
                    return float(os.environ.get(name, "") or default)
                except (TypeError, ValueError):
                    return default
            self.st_margin = _sf("STOP_MARGIN", 0.50)
            self.st_hyst = _sf("STOP_HYST", 0.10)
            self.st_ref = os.environ.get("STOP_REF", "min")          # object | robot | min
            self.st_person_xy = (_sf("STOP_PX", _sf("PERSON_X", 0.1)), _sf("STOP_PY", _sf("PERSON_Y", -0.7)))
            self.st_object = os.environ.get("STOP_OBJECT") or os.environ.get("OBJECT") or "brown_box"
            self.st_dump = os.environ.get("STOP_DUMP", "")
            self._st_active = None; self._st_stats = None; self._st_ep = 0; self._st_diag = 0
            self._st_robot_key = None; self._st_nav_lo = None
            print(f"[STOP] engaged margin={self.st_margin} hyst={self.st_hyst} ref={self.st_ref} "
                  f"person={self.st_person_xy} dump={self.st_dump or '-'}", flush=True)

    # ---------------------- Policy interface -------------------
"""),
("""                if self._shield_diag < 3:
                    print(f"[SHIELD] disabled this step (error: {exc})", flush=True)
                    self._shield_diag += 1
        return action
""",
"""                if self._shield_diag < 3:
                    print(f"[SHIELD] disabled this step (error: {exc})", flush=True)
                    self._shield_diag += 1
        if getattr(self, "_stop_on", False):
            try:
                action = self._apply_stop(env, action)
            except Exception as exc:  # noqa: BLE001 -- never let the stop layer crash a rollout
                if self._st_diag < 3:
                    print(f"[STOP] disabled this step (error: {exc})", flush=True)
                    self._st_diag += 1
        return action
"""),
("""    def reset(self, env_ids: torch.Tensor | None = None):
        if env_ids is None:
            env_ids = slice(None)
""",
"""    # ---------------------- protective-stop helpers -------------------
    def _stop_person_xy(self, scene, ref):
        try:
            pp = scene["person"].data.root_pos_w[:, :2]
            return pp[:, 0], pp[:, 1]
        except Exception:  # noqa: BLE001 -- static (BASE) person exposes no root state: fixed xy from PERSON_X/Y
            px = torch.full((ref.shape[0],), self.st_person_xy[0], device=ref.device, dtype=ref.dtype)
            py = torch.full((ref.shape[0],), self.st_person_xy[1], device=ref.device, dtype=ref.dtype)
            return px, py

    def _apply_stop(self, env, action: torch.Tensor) -> torch.Tensor:
        scene = self._shield_scene(env)
        if scene is None:
            return action
        if self._st_nav_lo is None:
            self._st_nav_lo = action.shape[-1] - 7      # [..., 3 nav | 1 base_h | 3 torso_rpy]
        if self._st_robot_key is None:
            self._st_robot_key = self._shield_find_robot(scene)
        obj = scene[self.st_object].data.root_pos_w[:, :2]
        rob = scene[self._st_robot_key].data.root_pos_w[:, :2]
        px, py = self._stop_person_xy(scene, obj)
        d_obj = torch.sqrt((obj[:, 0] - px) ** 2 + (obj[:, 1] - py) ** 2)
        d_rob = torch.sqrt((rob[:, 0] - px) ** 2 + (rob[:, 1] - py) ** 2)
        sep = d_obj if self.st_ref == "object" else d_rob if self.st_ref == "robot" else torch.minimum(d_obj, d_rob)
        n = int(sep.shape[0])
        if self._st_active is None or self._st_active.shape[0] != n:
            self._st_active = torch.zeros(n, dtype=torch.bool, device=sep.device)
            self._st_stats = [self._stop_blank() for _ in range(n)]
        engage = sep < self.st_margin
        release = sep > self.st_margin + self.st_hyst
        new_active = torch.where(self._st_active, ~release, engage)
        lo = self._st_nav_lo
        action = action.clone()
        for i in range(n):
            st = self._st_stats[i]; st["steps"] += 1; s = float(sep[i].item())
            st["min_sep"] = s if st["min_sep"] is None else min(st["min_sep"], s)
            if bool(new_active[i]):
                st["stop_steps"] += 1
                st["min_sep_in_stop"] = s if st["min_sep_in_stop"] is None else min(st["min_sep_in_stop"], s)
                if not bool(self._st_active[i]):
                    st["n_stops"] += 1
                    st["stop_seps"].append(round(s, 3))
                    if st["first_stop_sep"] is None:
                        st["first_stop_sep"] = s; st["first_stop_step"] = st["steps"]
                    if self._st_diag < 40:
                        self._st_diag += 1
                        print(f"[STOP] env{i} stop #{st['n_stops']} sep={s:.3f} (obj {d_obj[i].item():.3f} / base {d_rob[i].item():.3f}) step={st['steps']}", flush=True)
                action[i, lo:lo + 3] = 0.0              # protective stop: zero vx, vy, yaw-rate of the base command
        self._st_active = new_active
        return action

    @staticmethod
    def _stop_blank():
        return dict(n_stops=0, stop_steps=0, steps=0, first_stop_sep=None, first_stop_step=None, min_sep=None,
                    min_sep_in_stop=None, stop_seps=[])

    def _stop_flush(self, env_ids):
        if not getattr(self, "_stop_on", False) or self._st_stats is None:
            return
        if env_ids is None or isinstance(env_ids, slice):
            idx = range(len(self._st_stats))
        else:
            idx = [int(i) for i in torch.as_tensor(env_ids).flatten().tolist()]
        for i in idx:
            st = self._st_stats[i]
            if st["steps"] <= 0:
                continue
            rec = dict(episode=self._st_ep, env=i, margin=self.st_margin, hyst=self.st_hyst, ref=self.st_ref, **st)
            self._st_ep += 1
            print(f"[STOP] episode summary {json.dumps(rec)}", flush=True)
            if self.st_dump:
                try:
                    with open(self.st_dump, "a") as f:
                        f.write(json.dumps(rec) + "\\n")
                except Exception:  # noqa: BLE001
                    pass
            self._st_stats[i] = self._stop_blank()
            self._st_active[i] = False

    def reset(self, env_ids: torch.Tensor | None = None):
        self._stop_flush(env_ids)
        if env_ids is None:
            env_ids = slice(None)
"""),
("""    def close(self) -> None:
        \"\"\"Release Arena-side resources for the remote GR00T policy client.\"\"\"
        client = self._client
""",
"""    def close(self) -> None:
        \"\"\"Release Arena-side resources for the remote GR00T policy client.\"\"\"
        try:
            self._stop_flush(None)
        except Exception:  # noqa: BLE001
            pass
        client = self._client
"""),
])
print("ALL PATCHED")
