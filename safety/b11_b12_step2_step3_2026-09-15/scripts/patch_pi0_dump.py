import io, sys
p = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena/isaaclab_arena_openpi/policy/pi0_remote_policy.py"
s = io.open(p, encoding="utf-8").read()
if "FR_ACTION_DUMP" in s:
    print("already patched"); sys.exit(0)
old = '''    def get_action(self, env, observation):
        action = super().get_action(env, observation)
'''
NL = chr(92) + "n"      # the two characters backslash + n, written into the patched source
new = '''    def get_action(self, env, observation):
        action = super().get_action(env, observation)
        if getattr(self, "_fr_dump", None) is None:
            import os as _o
            self._fr_dump = _o.environ.get("FR_ACTION_DUMP", "") or False
            if self._fr_dump:
                open(self._fr_dump, "w").close()
        if self._fr_dump:
            try:
                import json as _j
                _t = int(env.unwrapped.episode_length_buf[0].item())
                with open(self._fr_dump, "a") as _fh:
                    _fh.write(_j.dumps({"t": _t, "a": [round(float(v), 6) for v in action[0].tolist()]}) + "''' + NL + '''")
            except Exception as _exc:  # noqa: BLE001
                print(f"[FR_ACTION_DUMP] {_exc!r}", flush=True)
'''
assert s.count(old) == 1, "anchor"
io.open(p, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))
print("pi0 policy patched for FR_ACTION_DUMP")
