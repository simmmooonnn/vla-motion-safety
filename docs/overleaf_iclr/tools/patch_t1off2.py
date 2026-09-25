# -*- coding: utf-8 -*-
"""Off-path T1 as a cross-policy, four-surface, four-level series: N["t1_off"] gains a 0.20 m level and a per-surface split,
and N["t1_off_pi0"] is the same series for pi0."""
import io

p = "gen_a45_numbers.py"
s = io.open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)


rep('for _tag, _pat in (("on", "_t1_"), ("d12", "_t1o12"), ("d28", "_t1o28")):\n    _ls = [l for l in S if policy(l) == "pi05" and g(l, "n_t1") and _pat in base(l) and base(l).startswith("sc_")]',
    'for _tag, _pat in (("on", "_t1_"), ("d12", "_t1o12"), ("d20", "_t1o20"), ("d28", "_t1o28")):\n    _ls = [l for l in S if policy(l) == "pi05" and g(l, "n_t1") and _pat in base(l) and base(l).startswith("sc_")]')
rep('N["t1_off_ctrl"] = {}\nfor _tag, _pat in (("on", "_t1_"), ("d12", "_t1o12"), ("d28", "_t1o28")):',
    'N["t1_off_ctrl"] = {}\nfor _tag, _pat in (("on", "_t1_"), ("d12", "_t1o12"), ("d20", "_t1o20"), ("d28", "_t1o28")):')
# pi0 on the same cells, and the 0.28 m level per surface for pi0.5 and the control
rep('N["n_tasks_exercised"] =', '''N["t1_off_pi0"] = {}
for _tag, _pat in (("on", "_t1_"), ("d28", "_t1o28")):
    _lp = [l for l in S if policy(l) == "pi0" and g(l, "n_t1") and _pat in base(l) and base(l).startswith("sc_")]
    _kp, _np = pool(_lp, "viol_t1", "n_t1"); _cp = [v for l in _lp for v in (g(l, "t1_clear") or [])]
    N["t1_off_pi0"][_tag] = {"rate": f"{_kp}/{_np}", "pct": (f"{100 * _kp / _np:.0f}" if _np else "0"),
                             "dmed": (f"{st.median(_cp):.2f}" if _cp else "—"), "car": str(sum(g(l, "carried", 0) or 0 for l in _lp)),
                             "att": str(sum(g(l, "N", 0) for l in _lp))}
N["t1_off_surf"] = {}
for _sf, _pre in (("counter", "sc_kit_"), ("desk", "sc_off_"), ("packing", "sc_pack_"), ("drawer", "sc_drw_")):
    _o = {}
    for _who, _pol in (("pi", "pi05"), ("ik", "scripted")):
        _lq = [l for l in S if policy(l) == _pol and g(l, "n_t1") and "_t1o28" in base(l) and base(l).startswith(_pre)]
        _kq, _nq = pool(_lq, "viol_t1", "n_t1"); _o[_who] = f"{_kq}/{_nq}" if _nq else "—"
    N["t1_off_surf"][_sf] = _o
N["n_tasks_exercised"] =''')
io.open(p, "w", encoding="utf-8").write(s)
print("patched")
