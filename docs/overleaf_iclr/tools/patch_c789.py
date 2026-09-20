# -*- coding: utf-8 -*-
"""Review round 3, blocking items C7/C8/C9 in the number generator."""
import io

p = "gen_a45_numbers.py"
s = io.open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)


# C8: the control gets its own coverage column, so the caption total matches the rows
rep('                            for p in ("pi05", "pi0", "gr00t_droid")) + " |" for s in SURF)',
    '                            for p in TAB4B_POL) + " |" for s in SURF)')
rep('SURF = ["dining table", "kitchen counter", "packing station", "drawer kitchen", "office desk", "island kitchen"]',
    'SURF = ["dining table", "kitchen counter", "packing station", "drawer kitchen", "office desk", "island kitchen"]\n'
    'TAB4B_POL = ("pi05", "pi0", "gr00t_droid", "scripted")')
rep('N["episodes_total"] = str(sum(v[0] for v in cov.values())); N["carried_total"] = str(sum(v[1] for v in cov.values()))\n'
    'N["delivered_total"] = str(sum(v[2] for v in cov.values()))',
    'N["episodes_total"] = str(sum(v[0] for k, v in cov.items() if k[1] in TAB4B_POL))\n'
    'N["carried_total"] = str(sum(v[1] for k, v in cov.items() if k[1] in TAB4B_POL))\n'
    'N["delivered_total"] = str(sum(v[2] for k, v in cov.items() if k[1] in TAB4B_POL))')

# C7: the T6b secondary has no distance gate, so it is not a subset of T6b
rep('"| T6b, of which the payload is faster at the closest approach than over the transport | "',
    '"| Payload faster at the closest approach than its transport mean (no distance gate, so not a subset of T6b) | "')

# C8: the capability-boundary count, from the table instead of a literal
rep('N["n_tasks_exercised"] =',
    'N["n_tasks_boundary"] = str(sum(1 for nm in ORDER_T if nm in groups and "capability boundary" in task_row(nm, groups[nm]).split("|")[3]))\n'
    'N["n_tasks_exercised"] =')

# C9: does a hand that can move away get touched less? static reaching hand vs the withdrawing proxy
rep('N["matched"] = _matched()', '''N["matched"] = _matched()


def _fisher(a, b, c, d):
    from math import comb
    n = a + b + c + d; r1 = a + b; c1 = a + c
    if min(n, r1, c1) <= 0:
        return 1.0
    pr = lambda x: comb(r1, x) * comb(n - r1, c1 - x) / comb(n, c1)
    p0 = pr(a)
    return min(1.0, sum(pr(x) for x in range(max(0, c1 - (n - r1)), min(r1, c1) + 1) if pr(x) <= p0 + 1e-12))


_st_h = [l for l in S if policy(l) == "pi05" and ("t6_hand" in l or "t6hand" in l) and g(l, "t6_n") and not any(x in l for x in SKIP)]
_wd_h = [l for l in S if l.startswith("hw_") and g(l, "t6_n")]
_ta, _tn1 = sum(g(l, "t5b_touch", 0) or 0 for l in _st_h), sum(g(l, "t6_n", 0) or 0 for l in _st_h)
_tc, _tn2 = sum(g(l, "t5b_touch", 0) or 0 for l in _wd_h), sum(g(l, "t6_n", 0) or 0 for l in _wd_h)
N["hand_state"] = {"static": f"{_ta}/{_tn1}", "withdraw": f"{_tc}/{_tn2}",
                   "static_pct": (f"{100 * _ta / _tn1:.0f}" if _tn1 else "0"),
                   "withdraw_pct": (f"{100 * _tc / _tn2:.0f}" if _tn2 else "0"),
                   "p": f"{_fisher(_ta, _tn1 - _ta, _tc, _tn2 - _tc):.4f}"}''')

io.open(p, "w", encoding="utf-8").write(s)
print("patched")
