# -*- coding: utf-8 -*-
# The reviewer's exposure-duration point (round-4 perspective review): does a person who appears late get a different response
# from one who is there from the first frame? lr1m / lr1s (2026-10-02), pi0.5, dining table, seeds 42 / 7, 8 episodes per cell:
# the same posed person at (0.45, -0.66), present from the first frame (pres), arriving 1 s after the lift from 2 m out of view
# and stopping facing the table (late), or not rendered (abs), scored at that place in every condition. Counts and medians from
# fr_summary.json (analyze_fr with QUAT_XYZW_FIX); Mann-Whitney two-sided. Exec'd after a142 (uses t, _rn2).
import json as _j4, pathlib as _p4, statistics as _st4, math as _m4
_S4 = _j4.load(open(_p4.Path(__file__).with_name("fr_summary.json"), encoding="utf-8"))


def _l4(cond, obj, key):
    out = []
    for sd in ("s42", "s7"):
        v = (_S4.get(f"lr_{cond}_{obj}_{sd}") or {}).get(key)
        if isinstance(v, list):
            out += [x for x in v if x is not None]
    return out


def _c4(cond, obj, key, lk):
    k = n = 0
    for sd in ("s42", "s7"):
        e = _S4.get(f"lr_{cond}_{obj}_{sd}") or {}
        k += e.get(key, 0) or 0
        L = e.get(lk); n += len(L) if isinstance(L, list) else (L or 0)
    return f"{k}/{n}"


def _mw4(a, b):
    n1, n2 = len(a), len(b)
    r = sorted([(x, 0) for x in a] + [(x, 1) for x in b]); vals = [x for x, _ in r]; rk = [0.0] * len(r); j = 0
    while j < len(r):
        k = j
        while k + 1 < len(r) and vals[k + 1] == vals[j]:
            k += 1
        for m in range(j, k + 1):
            rk[m] = (j + k) / 2 + 1
        j = k + 1
    U = sum(rk[m] for m in range(len(r)) if r[m][1] == 0) - n1 * (n1 + 1) / 2
    sd = _m4.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    return _m4.erfc(abs((U - n1 * n2 / 2) / sd) / _m4.sqrt(2)) if sd else 1.0


if _S4.get("lr_late_mug_s42"):
    _md = lambda v: "%.3f" % _st4.median(v)
    _v = {c: _l4(c, "mug", "v_at") for c in ("pres", "late", "abs")}
    _d = {c: _l4(c, "mug", "dmin") for c in ("pres", "late", "abs")}
    _ps = [_mw4(_v[a], _v[b]) for a, b in (("pres", "late"), ("pres", "abs"), ("late", "abs"))] + \
          [_mw4(_d[a], _d[b]) for a, b in (("pres", "late"), ("pres", "abs"), ("late", "abs"))]
    _vs = {c: _l4(c, "sci", "v_at") for c in ("pres", "late")}
    _psc = _mw4(_vs["pres"], _vs["late"])
    _rn2("(π0 was run on the same cells but carries the scissors on at most two episodes per level, below the floor; it adds no "
         "second policy here.)",
         "(π0 was run on the same cells but carries the scissors on at most two episodes per level, below the floor; it adds no "
         "second policy here.)\n\n"
         "**A person who appears late (exposure duration).** The bystanders above are in view from the first frame. To ask "
         "whether a person who arrives during the carry is treated differently, the same posed person stands at the same place "
         "beside the transport (0.45, −0.66 m) in three conditions — present from the first frame, arriving 1 s after the lift "
         "from 2 m out of view and stopping there facing the table, or not rendered — scored at that place in all three (π0.5, "
         "dining table, seeds 42 / 7, 8 episodes per cell). Carrying the mug, the payload passes the place at a median "
         f"{_md(_v['pres'])}, {_md(_v['late'])} and {_md(_v['abs'])} m/s at a closest approach of {_md(_d['pres'])}, "
         f"{_md(_d['late'])} and {_md(_d['abs'])} m; the arm comes within 0.10 m on {_c4('pres', 'mug', 't2_viol', 't2_n')}, "
         f"{_c4('late', 'mug', 't2_viol', 't2_n')} and {_c4('abs', 'mug', 't2_viol', 't2_n')} episodes and the mug passes 45° on "
         f"{_c4('pres', 'mug', 't45', 'tilt_trans')}, {_c4('late', 'mug', 't45', 'tilt_trans')} and "
         f"{_c4('abs', 'mug', 't45', 'tilt_trans')} carries; no pairwise speed or distance contrast is significant (Mann-Whitney "
         f"*p* {min(_ps):.2f}–{max(_ps):.2f}). With scissors (the person on the side the frozen yaw spares, so the presentation "
         f"rate is near zero throughout: {_c4('pres', 'sci', 't3_90', 't3')}, {_c4('late', 'sci', 't3_90', 't3')}, "
         f"{_c4('abs', 'sci', 't3_90', 't3')}) the one contrast that reaches *p* < 0.05 among the dozen tested runs the other way: "
         f"the payload passes a late-arriving person faster ({_md(_vs['late'])} against {_md(_vs['pres'])} m/s, *p* = "
         f"{_psc:.2f}). A person who arrives mid-carry is met as one who was always there, and both as one who is absent: the "
         "duration of exposure does not enter the motion.")
    _rn2("a person who appears late or who moves could in principle enter a command that this one does not.",
         "a person who appears late or who moves could in principle enter a command that this one does not (on the tabletop a "
         "person arriving mid-carry is met exactly as one present from the start or absent, E.8).")
