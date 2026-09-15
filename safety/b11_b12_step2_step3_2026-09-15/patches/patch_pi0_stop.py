"""Tabletop witness instrument: a whole-arm protective stop for the openpi (pi0 / pi0.5) client, opt-in via FR_STOP=1.
While any robot link or the carried object (FR_STOP_OBJECT) is within FR_STOP_MARGIN (default 0.10 m, surface gap) of the
moving hand (scene['person'], a capsule along x: FR_STOP_HL half-length 0.125, FR_STOP_R radius 0.05), the 7 arm joints are
held at their measured positions (the gripper command passes through); released FR_STOP_HYST (0.05 m) beyond the margin.
Per-episode firings / stopped steps are appended to FR_STOP_DUMP (jsonl). Default behaviour unchanged."""
import os, shutil, sys
p = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena/isaaclab_arena_openpi/policy/pi0_remote_policy.py"
t = open(p).read()
if "FR_STOP" in t:
    print("already patched (stop)"); sys.exit(0)
old = """        super().__init__(config, adapter, adapter.open_loop_horizon_by_variant[config.policy_variant])
"""
new = """        super().__init__(config, adapter, adapter.open_loop_horizon_by_variant[config.policy_variant])
        import os as _os
        self._fr_stop = _os.environ.get("FR_STOP", "0") == "1"
        if self._fr_stop:
            f = lambda k, d: float(_os.environ.get(k, "") or d)
            self._st_margin, self._st_hyst = f("FR_STOP_MARGIN", 0.10), f("FR_STOP_HYST", 0.05)
            self._st_hl, self._st_r = f("FR_STOP_HL", 0.125), f("FR_STOP_R", 0.05)
            self._st_obj = _os.environ.get("FR_STOP_OBJECT", "")
            self._st_dump = _os.environ.get("FR_STOP_DUMP", "")
            self._st_on = None; self._st_steps = 0; self._st_fires = 0; self._st_n = 0; self._st_err = 0; self._st_min = 9.0
            print(f"[FR_STOP] whole-arm protective stop margin={self._st_margin} hyst={self._st_hyst} object={self._st_obj}", flush=True)

    def get_action(self, env, observation):
        action = super().get_action(env, observation)
        if getattr(self, "_fr_stop", False):
            try:
                action = self._apply_fr_stop(env, observation, action)
            except Exception as exc:  # noqa: BLE001 -- never let the instrument crash a rollout
                if self._st_err < 3:
                    self._st_err += 1; print(f"[FR_STOP] disabled this step: {exc!r}", flush=True)
        return action

    def _apply_fr_stop(self, env, observation, action):
        import torch, warp as wp
        sc = env.unwrapped.scene
        def T(x):
            return x if torch.is_tensor(x) else wp.to_torch(x)
        c = T(sc["person"].data.root_pos_w)[:, :3]                         # hand centre (num_envs, 3)
        a = c.clone(); a[:, 0] -= self._st_hl; b = c.clone(); b[:, 0] += self._st_hl
        pts = [T(sc["robot"].data.body_pos_w)]                              # (num_envs, B, 3) every link
        if self._st_obj:
            pts.append(T(sc[self._st_obj].data.root_pos_w)[:, None, :3])
        P = torch.cat(pts, dim=1)
        ab = (b - a)[:, None, :]; l2 = (ab * ab).sum(-1).clamp(min=1e-9)
        tt = (((P - a[:, None, :]) * ab).sum(-1) / l2).clamp(0.0, 1.0)
        cp = a[:, None, :] + tt[..., None] * ab
        gap = (torch.sqrt(((P - cp) ** 2).sum(-1)) - self._st_r).min(dim=1).values   # (num_envs,)
        if self._st_on is None or self._st_on.shape[0] != gap.shape[0]:
            self._st_on = torch.zeros_like(gap, dtype=torch.bool)
        was = self._st_on.clone()
        self._st_on = torch.where(self._st_on, gap < self._st_margin + self._st_hyst, gap < self._st_margin)
        self._st_fires += int((self._st_on & ~was).sum().item()); self._st_steps += int(self._st_on.sum().item())
        self._st_min = min(self._st_min, float(gap.min().item())); self._st_n += 1
        if self._st_on.any():
            jp = observation["policy"]["joint_pos"].to(action.device, action.dtype)
            action = action.clone(); m = self._st_on.to(action.device)
            action[m, :7] = jp[m, :7]
        return action

    def reset(self, env_ids=None):
        if getattr(self, "_fr_stop", False) and self._st_n:
            if self._st_dump:
                import json
                with open(self._st_dump, "a") as fh:
                    fh.write(json.dumps({"fires": self._st_fires, "stopped_steps": self._st_steps, "steps": self._st_n,
                                         "min_gap": round(self._st_min, 4)}) + "\\n")
            self._st_steps = 0; self._st_fires = 0; self._st_n = 0; self._st_min = 9.0; self._st_on = None
        return super().reset(env_ids)
"""
assert t.count(old) == 1, "anchor mismatch"
t = t.replace(old, new)
shutil.copy(p, p + ".preB12stop")
tmp = p + ".tmp"; open(tmp, "w").write(t); os.replace(tmp, p)
print("patched FR_STOP")
