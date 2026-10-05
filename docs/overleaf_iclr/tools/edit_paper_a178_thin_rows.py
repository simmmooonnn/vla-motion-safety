# -*- coding: utf-8 -*-
# Thin rows (queues q0xa-c, g0xa-c, 2026-10-05): pi0 and GR00T N1.6-DROID meet the crossing hand (dining with the hidden-hand twin,
# counter, desk). E.8, after the policy rates of the crossing-hand paragraph; Tables III and IIIb follow from the generator.
# Exec'd after a177 (uses t, _rn2, V).
_x0 = V.get("hx_pi0") or {}; _xg = V.get("hx_gr00t_droid") or {}
_h0 = V.get("hx_pi0_hidden") or {}; _hg = V.get("hx_gr00t_droid_hidden") or {}


def _n_of(s_):
    try:
        return int(s_.split("/")[1])
    except Exception:  # noqa: BLE001
        return 0


_parts = []
for _nm, _x, _h in (("π0", _x0, _h0), ("GR00T N1.6-DROID", _xg, _hg)):
    if _x.get("reach") and _n_of(_x["reach"]) > 0:
        _parts.append(_nm + " reaches it on " + _x["reach"] + " and waits on " + _x.get("wait", "—")
                      + (" (hand neither rendered nor colliding: " + _h["reach"] + ")" if _h.get("reach") and _n_of(_h["reach"]) else ""))
_i8 = t.find("π0-FAST reaches it on ")
_j8 = t.find(".", t.find("waits on", _i8)) if _i8 > 0 else -1
if _parts and _i8 > 0 and _j8 > _i8 and "π0 reaches it on" not in t:
    t = t[:_j8 + 1] + " " + "; ".join(_parts) + " (at the dining table, the counter and the desk)." + t[_j8 + 1:]
elif not _parts:
    print("  [a178] no pi0 / GR00T-DROID crossing cells yet")
else:
    print("  [a178 MISS] E.8 crossing paragraph")
