# R7: log the base navigation command GR00T emits each step, so a memorised route can be told from a policy output that
# responds to the scene. NAV_DUMP=<path> appends one JSON line per step: {"t": step, "nav": [vx, vy, wz]}.
import sys

p = sys.argv[1]
s = open(p).read()
if "NAV_DUMP" in s:
    print("already patched", p)
    sys.exit()

anchor = "        navigate_cmd = self.get_navigation_cmd_from_actions(actions_clone).cpu()\n"
add = '''        navigate_cmd = self.get_navigation_cmd_from_actions(actions_clone).cpu()
        if __import__("os").environ.get("NAV_DUMP"):      # R7: the base heading GR00T asks for, per step
            try:
                import json as _json
                self._nav_t = getattr(self, "_nav_t", 0) + 1
                with open(__import__("os").environ["NAV_DUMP"], "a") as _f:
                    _f.write(_json.dumps({"t": self._nav_t, "nav": navigate_cmd[0].tolist()}) + "\\n")
            except Exception as _e:
                if not getattr(self, "_nav_err", False):
                    self._nav_err = True
                    print("[NAV_DUMP] skipped: " + repr(_e), flush=True)
'''
assert anchor in s, "navigate_cmd anchor"
s = s.replace(anchor, add, 1)
open(p, "w").write(s)
print("patched", p)
