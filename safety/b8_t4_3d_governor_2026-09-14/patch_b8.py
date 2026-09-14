# -*- coding: utf-8 -*-
"""B8 patch: SSM speed governor in gr00t_remote_closedloop_policy.py (anchor-asserted; original kept as *.preB8)."""
import os, shutil
AR = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena"
p = os.path.join(AR, "isaaclab_arena_gr00t/policy/gr00t_remote_closedloop_policy.py")
t = open(p, encoding="utf-8").read()
if "_gov_on" in t:
    print("already applied"); raise SystemExit
if not os.path.exists(p + ".preB8"): shutil.copy(p, p + ".preB8")
def rep(old, new):
    global t
    assert t.count(old) == 1, old[:70]
    t = t.replace(old, new)
rep("""    # ---------------------- Policy interface -------------------
""",
"""        # --- B8 speed-and-separation GOVERNOR reference layer (env-gated): scale the base velocity command so the measured
        # base speed stays under v_allow(d) = max(0, (d - v_h (T_r+T_s) - C - Z) / (T_r + T_s/2)) (ISO/TS 15066 SSM inverted) ---
        self._gov_on = os.environ.get("GOV", "0") == "1"
        if self._gov_on:
            def _gf(name, default):
                try:
                    return float(os.environ.get(name, "") or default)
                except (TypeError, ValueError):
                    return default
            self.gv_vh = _gf("GOV_VH", 0.0); self.gv_tr = _gf("GOV_TR", 0.10); self.gv_ts = _gf("GOV_TS", 0.30)
            self.gv_c = _gf("GOV_C", 0.20); self.gv_z = _gf("GOV_Z", 0.10)
            self.gv_ref = os.environ.get("GOV_REF", "min")          # object | robot | min
            self.gv_person_xy = (_gf("GOV_PX", _gf("PERSON_X", 0.1)), _gf("GOV_PY", _gf("PERSON_Y", -0.7)))
            self.gv_object = os.environ.get("GOV_OBJECT") or os.environ.get("OBJECT") or "brown_box"
            self.gv_dump = os.environ.get("GOV_DUMP", "")
            self._gv_stats = None; self._gv_ep = 0; self._gv_diag = 0; self._gv_robot_key = None; self._gv_nav_lo = None
            print(f"[GOV] engaged v_h={self.gv_vh} T_r={self.gv_tr} T_s={self.gv_ts} C={self.gv_c} Z={self.gv_z} "
                  f"ref={self.gv_ref} person={self.gv_person_xy} dump={self.gv_dump or '-'}", flush=True)

    # ---------------------- Policy interface -------------------
""")
rep("""        if getattr(self, "_stop_on", False):
            try:
                action = self._apply_stop(env, action)
            except Exception as exc:  # noqa: BLE001 -- never let the stop layer crash a rollout
                if self._st_diag < 3:
                    print(f"[STOP] disabled this step (error: {exc})", flush=True)
                    self._st_diag += 1
        return action
""",
"""        if getattr(self, "_stop_on", False):
            try:
                action = self._apply_stop(env, action)
            except Exception as exc:  # noqa: BLE001 -- never let the stop layer crash a rollout
                if self._st_diag < 3:
                    print(f"[STOP] disabled this step (error: {exc})", flush=True)
                    self._st_diag += 1
        if getattr(self, "_gov_on", False):
            try:
                action = self._apply_gov(env, action)
            except Exception as exc:  # noqa: BLE001 -- never let the governor crash a rollout
                if self._gv_diag < 3:
                    print(f"[GOV] disabled this step (error: {exc})", flush=True)
                    self._gv_diag += 1
        return action
""")
rep("""    def reset(self, env_ids: torch.Tensor | None = None):
        self._stop_flush(env_ids)
""",
"""    # ---------------------- speed governor helpers -------------------
    def _gov_v_allow(self, d):
        num = d - self.gv_vh * (self.gv_tr + self.gv_ts) - self.gv_c - self.gv_z
        return (num / (self.gv_tr + 0.5 * self.gv_ts)).clamp(min=0.0)

    def _apply_gov(self, env, action: torch.Tensor) -> torch.Tensor:
        scene = self._shield_scene(env)
        if scene is None:
            return action
        if self._gv_nav_lo is None:
            self._gv_nav_lo = action.shape[-1] - 7
        if self._gv_robot_key is None:
            self._gv_robot_key = self._shield_find_robot(scene)
        obj = scene[self.gv_object].data.root_pos_w[:, :2]
        robot = scene[self._gv_robot_key]
        rob = robot.data.root_pos_w[:, :2]
        try:
            pp = scene["person"].data.root_pos_w[:, :2]; px, py = pp[:, 0], pp[:, 1]
        except Exception:  # noqa: BLE001 -- static (BASE) person: fixed xy
            px = torch.full((obj.shape[0],), self.gv_person_xy[0], device=obj.device, dtype=obj.dtype)
            py = torch.full((obj.shape[0],), self.gv_person_xy[1], device=obj.device, dtype=obj.dtype)
        d_obj = torch.sqrt((obj[:, 0] - px) ** 2 + (obj[:, 1] - py) ** 2)
        d_rob = torch.sqrt((rob[:, 0] - px) ** 2 + (rob[:, 1] - py) ** 2)
        d = d_obj if self.gv_ref == "object" else d_rob if self.gv_ref == "robot" else torch.minimum(d_obj, d_rob)
        v_allow = self._gov_v_allow(d)
        vel = robot.data.root_lin_vel_w[:, :2]
        speed = torch.sqrt(vel[:, 0] ** 2 + vel[:, 1] ** 2)
        factor = torch.where(speed > v_allow, v_allow / speed.clamp(min=1e-3), torch.ones_like(speed)).clamp(0.0, 1.0)
        n = int(d.shape[0])
        if self._gv_stats is None or len(self._gv_stats) != n:
            self._gv_stats = [self._gov_blank() for _ in range(n)]
        lo = self._gv_nav_lo
        action = action.clone()
        for i in range(n):
            st = self._gv_stats[i]; st["steps"] += 1
            f = float(factor[i].item()); s = float(speed[i].item()); va = float(v_allow[i].item()); dd = float(d[i].item())
            st["min_d"] = dd if st["min_d"] is None else min(st["min_d"], dd)
            exc = s - va
            st["max_excess"] = exc if st["max_excess"] is None else max(st["max_excess"], exc)
            if f < 1.0:
                st["governed_steps"] += 1; st["min_factor"] = min(st["min_factor"], f)
                if va <= 0.0: st["stop_steps"] += 1
                if self._gv_diag < 20 and st["governed_steps"] in (1, 50, 200):
                    self._gv_diag += 1
                    print(f"[GOV] env{i} d={dd:.3f} v_allow={va:.3f} speed={s:.3f} factor={f:.2f} step={st['steps']}", flush=True)
                action[i, lo + 0] = action[i, lo + 0] * f
                action[i, lo + 1] = action[i, lo + 1] * f
        return action

    @staticmethod
    def _gov_blank():
        return dict(steps=0, governed_steps=0, stop_steps=0, min_factor=1.0, min_d=None, max_excess=None)

    def _gov_flush(self, env_ids):
        if not getattr(self, "_gov_on", False) or self._gv_stats is None:
            return
        idx = range(len(self._gv_stats)) if env_ids is None or isinstance(env_ids, slice) else [int(i) for i in torch.as_tensor(env_ids).flatten().tolist()]
        for i in idx:
            st = self._gv_stats[i]
            if st["steps"] <= 0:
                continue
            rec = dict(episode=self._gv_ep, env=i, vh=self.gv_vh, T=self.gv_tr + self.gv_ts, C=self.gv_c, Z=self.gv_z, ref=self.gv_ref, **st)
            self._gv_ep += 1
            print(f"[GOV] episode summary {json.dumps(rec)}", flush=True)
            if self.gv_dump:
                try:
                    with open(self.gv_dump, "a") as f:
                        f.write(json.dumps(rec) + "\\n")
                except Exception:  # noqa: BLE001
                    pass
            self._gv_stats[i] = self._gov_blank()

    def reset(self, env_ids: torch.Tensor | None = None):
        self._stop_flush(env_ids)
        self._gov_flush(env_ids)
""")
rep("""        try:
            self._stop_flush(None)
        except Exception:  # noqa: BLE001
            pass
        client = self._client
""",
"""        try:
            self._stop_flush(None); self._gov_flush(None)
        except Exception:  # noqa: BLE001
            pass
        client = self._client
""")
open(p, "w", encoding="utf-8").write(t); print("patched governor")
