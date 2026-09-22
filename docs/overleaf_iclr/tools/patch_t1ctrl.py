# -*- coding: utf-8 -*-
"""Round 3, C4: the scripted control's own off-path T1 series -- the geometric witness."""
import io

p = "gen_a45_numbers.py"
s = io.open(p, encoding="utf-8").read()
a = 'N["t1_off"] = {}'
assert s.count(a) == 1

blk = '''N["t1_off"] = {}
N["t1_off_ctrl"] = {}
for _tag, _pat in (("on", "_t1_"), ("d12", "_t1o12"), ("d28", "_t1o28")):
    _lc = [l for l in S if policy(l) == "scripted" and g(l, "n_t1") and _pat in base(l)]
    _kc, _nc = pool(_lc, "viol_t1", "n_t1")
    _cc = [v for l in _lc for v in (g(l, "t1_clear") or [])]
    N["t1_off_ctrl"][_tag] = {"rate": f"{_kc}/{_nc}", "pct": (f"{100 * _kc / _nc:.0f}" if _nc else "0"),
                              "dmin": (f"{min(_cc):.2f}" if _cc else "—"), "dmed": (f"{st.median(_cc):.2f}" if _cc else "—")}'''

s = s.replace(a, blk)
io.open(p, "w", encoding="utf-8").write(s)
print("patched")
