# -*- coding: utf-8 -*-
# Test-retest (queues rpa-rpd + rpx, 2026-10-05; review item 8): eight cells across the sub-types rerun twice with the current
# code, same configurations and seeds, side by side. Appendix C, after "What a seed fixes". Each cell's two reruns are tested
# against each other and its original against the pooled reruns (two-sided Fisher). Applied once both reruns of every cell
# are in. Exec'd after a169 (uses t, _rn2, V).
_rt = V.get("retest") or []
_rt_done = len(_rt) >= 8 and all(r.get("rep1") not in (None, "—") and r.get("rep2") not in (None, "—") for r in _rt)
_anchor = ("so the same configuration and seed give different episodes on a rerun. Every interval is therefore clustered by cell, "
           "and every comparison that matters runs its arms in one session, interleaved.")


def _kn(s_):
    k_, n_ = (int(x) for x in s_.split("/"))
    return k_, n_


def _fx2(a, n1, c, n2):
    from math import comb
    if not n1 or not n2:
        return 1.0
    r1, r2, c1 = n1, n2, a + c
    n = r1 + r2
    pr = lambda x: comb(r1, x) * comb(r2, c1 - x) / comb(n, c1)
    p0 = pr(a)
    return min(1.0, sum(pr(x) for x in range(max(0, c1 - r2), min(r1, c1) + 1) if pr(x) <= p0 * (1 + 1e-9)))


if _rt_done and _anchor in t and "**Table XII." not in t:
    _p12, _p0 = [], []
    for r in _rt:
        (k1, n1), (k2, n2), (k0, n0) = _kn(r["rep1"]), _kn(r["rep2"]), _kn(r["orig"])
        _p12.append(_fx2(k1, n1, k2, n2)); _p0.append(_fx2(k0, n0, k1 + k2, n1 + n2))
    _sub = {"T6": "T6 reaching hand (exposure)", "T6 crossing": "T6 crossing hand"}
    _rows = "\n".join(f"| {r['cell']} | {_sub.get(r['sub'], r['sub'])} | {r['orig']} ({r['orig_del']}) | {r['rep1']} ({r['rep1_del']}) | "
                      f"{r['rep2']} ({r['rep2_del']}) |" for r in _rt)
    _ns12 = all(p >= 0.05 for p in _p12); _ns0 = all(p >= 0.05 for p in _p0)
    _txt = (" Eight cells, one or two per sub-type, were rerun twice with the final code, side by side (Table XII). "
            + ("No cell's two reruns differ detectably" if _ns12 else "Some cells' reruns differ") + f" (smallest two-sided Fisher *p* = {min(_p12):.2f}), and "
            + ("no original differs detectably from its pooled reruns" if _ns0 else "some originals differ from their pooled reruns")
            + f" (smallest *p* = {min(_p0):.2f}): the spread between runs of a cell is the binomial spread of a few episodes, which the "
            "cell-clustered intervals carry.\n\n"
            "**Table XII. Test–retest: unsafe / scored episodes (delivered / attempted) for the original run and two reruns.**\n\n"
            "| Cell | Sub-type | Original | Rerun 1 | Rerun 2 |\n|---|---|---|---|---|\n" + _rows + "\n")
    t = t.replace(_anchor, _anchor + _txt, 1)
elif not _rt_done:
    print("  [a170] retest not complete yet")
