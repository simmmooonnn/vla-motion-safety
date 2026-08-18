#!/usr/bin/env python3
"""Fold the motion-safety shield into the BASE remote policy (env-gated via SHIELD),
sidestepping the @register_policy 'must directly inherit PolicyBase[Cfg]' assertion
that broke the subclass approach. Idempotent-ish: asserts each anchor is present once."""
import io, sys

F = "/weka/scratch/aszalay1/zijian/arena/IsaacLab-Arena/isaaclab_arena_gr00t/policy/gr00t_remote_closedloop_policy.py"
src = open(F, encoding="utf-8").read()

if "[SHIELD] engaged" in src:
    print("already patched; nothing to do"); sys.exit(0)

# 1. imports
a1 = "import gymnasium as gym\nimport torch\n"
assert src.count(a1) == 1, "import anchor not found"
src = src.replace(a1, "import gymnasium as gym\nimport os\nimport torch\n")

# 2. __init__ shield setup
a2 = "        self.task_description: str | None = None\n"
assert src.count(a2) == 1, "init anchor not found"
init_block = a2 + '''
        # --- motion-level safety shield (env-gated; folded in to avoid subclass/registry issues) ---
        self._shield_on = os.environ.get("SHIELD", "0") == "1"
        self._shield_diag = 0
        self._shield_robot_key = None
        self._shield_nav_lo = None
        if self._shield_on:
            def _f(name, default):
                try:
                    return float(os.environ.get(name, "") or default)
                except (TypeError, ValueError):
                    return default
            self.sh_margin = _f("SHIELD_MARGIN", 0.35)
            self.sh_gain = _f("SHIELD_GAIN", 2.0)
            self.sh_vmax = _f("SHIELD_VMAX", 0.4)
            self.shield_person_xy = (_f("PERSON_X", 0.1), _f("PERSON_Y", -0.7))
            self.shield_object = os.environ.get("SHIELD_OBJECT") or os.environ.get("OBJECT") or "brown_box"
            print(f"[SHIELD] engaged margin={self.sh_margin} gain={self.sh_gain} "
                  f"vmax={self.sh_vmax} person={self.shield_person_xy} object={self.shield_object}", flush=True)
'''
src = src.replace(a2, init_block)

# 3. get_action -> apply shield
a3 = ("        return self._chunking_state.get_action(\n"
      "            fetch_chunk,\n"
      "            hold_action=self._extract_hold_action(observation),\n"
      "        )\n")
assert src.count(a3) == 1, "get_action anchor not found"
a3_new = ('''        action = self._chunking_state.get_action(
            fetch_chunk,
            hold_action=self._extract_hold_action(observation),
        )
        if self._shield_on:
            try:
                action = self._apply_shield(env, action)
            except Exception as exc:  # noqa: BLE001 -- never let the shield crash a rollout
                if self._shield_diag < 3:
                    print(f"[SHIELD] disabled this step (error: {exc})", flush=True)
                    self._shield_diag += 1
        return action
''')
src = src.replace(a3, a3_new)

# 4. helper methods before reset()
a4 = "    def reset(self, env_ids: torch.Tensor | None = None):\n"
assert src.count(a4) == 1, "reset anchor not found"
helpers = '''    # ---------------------- safety shield helpers -------------------
    @staticmethod
    def _shield_scene(env):
        s = getattr(env, "scene", None)
        if s is None:
            s = getattr(getattr(env, "unwrapped", env), "scene", None)
        return s

    def _shield_find_robot(self, scene):
        arts = getattr(scene, "articulations", None)
        if arts is None:
            return None
        if "robot" in arts:
            return "robot"
        best, best_n = None, -1
        for k, a in arts.items():
            n = int(a.data.joint_pos.shape[-1]) if hasattr(a, "data") else -1
            if n > best_n:
                best, best_n = k, n
        return best

    @staticmethod
    def _shield_yaw(q):
        w, x, y, z = q[:, 0], q[:, 1], q[:, 2], q[:, 3]
        return torch.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))

    def _apply_shield(self, env, action: torch.Tensor) -> torch.Tensor:
        scene = self._shield_scene(env)
        if scene is None:
            return action
        if self._shield_nav_lo is None:
            self._shield_nav_lo = action.shape[-1] - 7  # [..., 3 nav | 1 base_h | 3 torso_rpy]
        if self._shield_robot_key is None:
            self._shield_robot_key = self._shield_find_robot(scene)
        obj = scene[self.shield_object].data.root_pos_w[:, :2]
        robot = scene[self._shield_robot_key]
        yaw = self._shield_yaw(robot.data.root_quat_w)
        px = torch.as_tensor(self.shield_person_xy[0], device=obj.device, dtype=obj.dtype)
        py = torch.as_tensor(self.shield_person_xy[1], device=obj.device, dtype=obj.dtype)
        dx = obj[:, 0] - px
        dy = obj[:, 1] - py
        clr = torch.sqrt(dx * dx + dy * dy) + 1e-6
        intr = (self.sh_margin - clr).clamp(min=0.0)
        spd = (self.sh_gain * intr).clamp(max=self.sh_vmax)
        ux, uy = dx / clr, dy / clr
        wvx, wvy = spd * ux, spd * uy
        c, s = torch.cos(yaw), torch.sin(yaw)
        vx_b = c * wvx + s * wvy
        vy_b = -s * wvx + c * wvy
        lo = self._shield_nav_lo
        action = action.clone()
        action[:, lo + 0] = (action[:, lo + 0] + vx_b).clamp(-1.0, 1.0)
        action[:, lo + 1] = (action[:, lo + 1] + vy_b).clamp(-1.0, 1.0)
        if self._shield_diag < 8:
            self._shield_diag += 1
            print(f"[SHIELD] robot={self._shield_robot_key} nav_lo={lo} dim={action.shape[-1]} "
                  f"clr={clr[0].item():.3f} intr={intr[0].item():.3f} "
                  f"add=({vx_b[0].item():+.3f},{vy_b[0].item():+.3f}) "
                  f"obj=({obj[0,0].item():.2f},{obj[0,1].item():.2f})", flush=True)
        return action

'''
src = src.replace(a4, helpers + a4)

open(F, "w", encoding="utf-8").write(src)
print("PATCHED", F)
