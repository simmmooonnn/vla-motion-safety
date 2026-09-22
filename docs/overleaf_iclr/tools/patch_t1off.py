# -*- coding: utf-8 -*-
"""Keep the off-path T1 cells out of the canonical (on-path) T1 pool and report them as their own quantity."""
import io

p = "gen_a45_numbers.py"
s = io.open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)


# the canonical T1 stays the on-path marker; the offset cells are a separate, non-ceiling measurement
rep('out["T1"] = pool([l for l in ls if g(l, "n_t1") and "_t1" in base(l) and base(l).startswith(("sc_", "kit_"))], "viol_t1", "n_t1")   # rendered marker',
    'out["T1"] = pool([l for l in ls if g(l, "n_t1") and "_t1" in base(l) and "_t1o" not in base(l) and base(l).startswith(("sc_", "kit_"))], "viol_t1", "n_t1")   # rendered marker, on the path')

# the off-path series, by offset
rep('N["matched"] = _matched()', '''N["matched"] = _matched()
# ---- the non-ceiling T1 series: the same marker offset perpendicular to the transport (review round 3, C4)
N["t1_off"] = {}
for _tag, _pat in (("on", "_t1_"), ("d12", "_t1o12"), ("d28", "_t1o28")):
    _ls = [l for l in S if policy(l) == "pi05" and g(l, "n_t1") and _pat in base(l) and base(l).startswith("sc_")]
    _k, _n = pool(_ls, "viol_t1", "n_t1")
    _cl = [v for l in _ls for v in (g(l, "t1_clear") or [])]
    N["t1_off"][_tag] = {"rate": f"{_k}/{_n}", "pct": (f"{100 * _k / _n:.0f}" if _n else "0"),
                         "dmin": (f"{min(_cl):.2f}" if _cl else "—"), "dmed": (f"{st.median(_cl):.2f}" if _cl else "—"),
                         "cells": str(len(_ls))}''')

io.open(p, "w", encoding="utf-8").write(s)
print("patched")
