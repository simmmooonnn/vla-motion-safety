set -u
A=/home/data/zzhao140/zijian/arena/IsaacLab-Arena
python3 - <<'PYEOF'
import os
A = "/home/data/zzhao140/zijian/arena/IsaacLab-Arena"

# 1. R7 was patched into the pink (IK) action term, but the client runs --embodiment g1_wbc_joint, so the joint term is
#    the one that turns GR00T's action chunk into a base command. Patch that one.
p = A + "/isaaclab_arena_g1/g1_env/mdp/actions/g1_decoupled_wbc_joint_action.py"
s = open(p, encoding="utf-8").read()
if "NAV_DUMP" in s:
    print("joint action already patched")
else:
    anchor = "        navigate_cmd = self.get_navigation_cmd_from_actions(actions_clone)\n"
    assert anchor in s, "joint navigate_cmd anchor"
    NL = chr(10)
    add = (anchor
           + '        if __import__("os").environ.get("NAV_DUMP"):      # R7: the base command GR00T asks for, per step' + NL
           + "            try:" + NL
           + "                import json as _json" + NL
           + '                self._nav_t = getattr(self, "_nav_t", 0) + 1' + NL
           + '                with open(__import__("os").environ["NAV_DUMP"], "a") as _f:' + NL
           + '                    _f.write(_json.dumps({"t": self._nav_t, "nav": navigate_cmd[0].detach().cpu().tolist()}) + chr(10))' + NL
           + "            except Exception as _e:" + NL
           + '                if not getattr(self, "_nav_err", False):' + NL
           + "                    self._nav_err = True" + NL
           + '                    print("[NAV_DUMP] skipped: " + repr(_e), flush=True)' + NL)
    open(p + ".tmp", "w", encoding="utf-8").write(s.replace(anchor, add, 1))
    os.replace(p + ".tmp", p)
    print("patched joint action term")

# 2. The recorder's dataset filename is timestamped to the second, so two runs that start in the same second race for
#    the same HDF5 and one dies with BlockingIOError. Add the pid.
q = A + "/isaaclab_arena/environments/arena_env_builder.py"
s = open(q, encoding="utf-8").read()
if "os.getpid()" in s:
    print("builder already patched")
else:
    a = "f\"{base}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_rank{get_local_rank()}\""
    assert a in s, "dataset filename anchor"
    b = "f\"{base}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_rank{get_local_rank()}_{__import__('os').getpid()}\""
    open(q + ".tmp", "w", encoding="utf-8").write(s.replace(a, b, 1))
    os.replace(q + ".tmp", q)
    print("patched dataset filename with the pid")
PYEOF
python3 -c "import ast,sys; ast.parse(open('$A/isaaclab_arena_g1/g1_env/mdp/actions/g1_decoupled_wbc_joint_action.py',encoding='utf-8').read()); ast.parse(open('$A/isaaclab_arena/environments/arena_env_builder.py',encoding='utf-8').read()); print('both files parse')"
grep -n "NAV_DUMP" $A/isaaclab_arena_g1/g1_env/mdp/actions/g1_decoupled_wbc_joint_action.py | head -4
grep -n "getpid" $A/isaaclab_arena/environments/arena_env_builder.py | head -2
