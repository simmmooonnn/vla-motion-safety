"""Step 3 (Franka T6/T5b 'reaching hand'): two opt-in knobs for MovingPersonRecorder; defaults unchanged.
  T6_TRIGGER_LIFT=<dz>  the mover waits until the carried object rises dz above its episode-start height
  T6_AIM_DEST=1         T6_START_X/Y are an OFFSET from the destination object (DUMP_DEST); the start follows the destination
                        until the trigger fires, then the mover advances with T6_VEL_X/Y (T6_STOP_DIST caps the path)
The trigger moment is visible in the dumped person_xy path (the mover starts to move)."""
import os, shutil, sys
p = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena/isaaclab_arena/metrics/moving_person.py"
t = open(p).read()
if "T6_TRIGGER_LIFT" in t:
    print("already patched (aim)"); sys.exit(0)
rep = []
rep.append(("""        self._yield_f = _envf_opt("T6_YIELD_F")""",
"""        self._yield_f = _envf_opt("T6_YIELD_F")
        # step 3 (Franka): lift trigger + destination-relative start (a hand reaching into the destination)
        self._lift = _envf_opt("T6_TRIGGER_LIFT"); self._z0 = None
        self._aim = os.environ.get("T6_AIM_DEST", "0") == "1"; self._dest = os.environ.get("DUMP_DEST", ""); self._start = None
        if self._lift is not None or self._aim:
            print(f"[T6] lift trigger={self._lift} aim_dest={self._aim} dest={self._dest} offset=({self.sx},{self.sy}) vel=({self.vx},{self.vy})", flush=True)"""))
rep.append(("""        if self._trig_y is None and self._delay is None:
            return t""",
"""        if self._trig_y is None and self._delay is None and self._lift is None:
            return t"""))
rep.append(("""        if self._delay is not None:
            return (t - self._delay).clamp(min=0.0)
        try:""",
"""        if self._delay is not None:
            return (t - self._delay).clamp(min=0.0)
        if self._lift is not None:                      # step 3: start when the carried object is lifted
            zc = wp.to_torch(self._env.scene[self.object_name].data.root_pos_w)[:, 2]
            if self._z0 is None or self._z0.shape[0] != zc.shape[0]:
                self._z0 = zc.clone()
            self._z0[reset] = zc[reset]
            arm = torch.isnan(self._t0) & (zc > self._z0 + self._lift)
            if arm.any():
                self._t0[arm] = t[arm]
                if self._trig_log < 30:
                    self._trig_log += 1
                    print(f"[T6] mover triggered by lift t={t[arm][0].item():.2f}s z={zc[arm][0].item():.3f}", flush=True)
            return torch.where(torch.isnan(self._t0), torch.zeros_like(t), (t - self._t0).clamp(min=0.0))
        try:"""))
rep.append(("""        px = self.sx + self.vx * tau                   # (num_envs,)
        py = self.sy + self.vy * tau""",
"""        if self._aim and self._dest:                   # step 3: start = destination + offset, frozen once walking
            org = env.scene.env_origins if torch.is_tensor(env.scene.env_origins) else wp.to_torch(env.scene.env_origins)
            dxy = wp.to_torch(env.scene[self._dest].data.root_pos_w)[:, :2] - org[:, :2]
            if self._start is None or self._start.shape[0] != dxy.shape[0]:
                self._start = torch.stack([dxy[:, 0] + self.sx, dxy[:, 1] + self.sy], dim=-1)
            waiting = (tau <= 0.0)
            if waiting.any():
                self._start[waiting] = torch.stack([dxy[waiting, 0] + self.sx, dxy[waiting, 1] + self.sy], dim=-1)
            px = self._start[:, 0] + self.vx * tau
            py = self._start[:, 1] + self.vy * tau
        else:
            px = self.sx + self.vx * tau               # (num_envs,)
            py = self.sy + self.vy * tau"""))
for a, b in rep:
    assert t.count(a) == 1, "anchor mismatch: " + a[:60]
    t = t.replace(a, b)
shutil.copy(p, p + ".preB12aim")
tmp = p + ".tmp"; open(tmp, "w").write(t); os.replace(tmp, p)
print("patched T6 lift/aim")
