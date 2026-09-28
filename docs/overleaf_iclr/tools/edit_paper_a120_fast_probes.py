# -*- coding: utf-8 -*-
# pi0-FAST on the remaining probes, one compact E.8 paragraph (every clause guarded on the floor), and GR00T-DROID's carry count at
# the 0.20 m level stated when it stays under the floor. Exec'd after a119 (uses t, RN, V).
_fp = V.get("f0_probes", {})
_g20 = V.get("t1_off_by", {}).get("g0", {}).get("d20", {})


def _n(x):
    try:
        return int(str(x).split("/")[1])
    except Exception:
        return 0


def _fl(x):
    try:
        return float(x)
    except Exception:
        return None


_cl = []
# appearance: the three renderings on the right-hand placement
_ap = _fp.get("appear", {})
if all(_n(_ap.get(k, {}).get("R", "—")) >= 8 for k in ("capsule", "mesh", "hidden")):
    _cl.append("into the person's half-space on " + _ap["capsule"]["R"] + " (capsule), " + _ap["mesh"]["R"] + " (human mesh) and " +
               _ap["hidden"]["R"] + " (not rendered) on the right, " + _ap["capsule"]["L"] + ", " + _ap["mesh"]["L"] + " and " +
               _ap["hidden"]["L"] + " on the left — the same person-blindness at every appearance")
# hurry
_hu = _fp.get("hurry", {})
_hm = _hu.get("v_mug", {}).get("hurry", ("—", "0"))
if isinstance(_hm, tuple) and _hm[0] != "—" and int(_hm[1]) >= 8:
    _cl.append("told to hurry, the mug moves at " + _hm[0] + " m/s against " + _hu["v_mug"]["neutral"][0] + " and the passer-by is met at "
               "80 % or more on " + _hu["t6b"]["hurry"][0] + " (neutral " + _hu["t6b"]["neutral"][0] + ")")
# cue walker
_cu = _fp.get("cue", {})
if int(_cu.get("n_cue", "0")) >= 8 and int(_cu.get("n_nocue", "0")) >= 8:
    _cl.append("the walker who visibly prepares to move is met at " + _cu["cue_med"] + " m/s against " + _cu["nocue_med"] + " without the cue")
# finite-mass hand
_dy = _fp.get("dyn", {})
if _n(_dy.get("touch", "—")) >= 8:
    _cl.append("the finite-mass hand is touched on " + _dy["touch"] + " (immovable " + _dy["touch_static"] + ") at a peak median of " +
               _dy["f_med"] + " N against " + _dy["f_med_static"] + " N")
# mirrored transport
_rv = _fp.get("rev", {})
_rc, _rd = _rv.get("counter", {}), _rv.get("desk", {})
if _rc and _rd and int(_rc.get("rev", ("—", "0"))[1]) >= 8 and int(_rd.get("rev", ("—", "0"))[1]) >= 8:
    _cl.append("with the transport reversed the bow toward +x is " + _rd["rev"][0] + " m at the desk and " + _rc["rev"][0] +
               " m at the counter (forward " + _rd["fwd"][0] + " and " + _rc["fwd"][0] + ")")

_anchor = ("The keep-out entries of the trajectory dimension are therefore the benchmark's transports sitting inside the "
           "demonstrations' workspace, and a scene laid out farther from the base would see the bow reverse.")
_add = ""
if _cl and _anchor in t:
    _add += " π0-FAST on the remaining probes: " + "; ".join(_cl) + "."
# GR00T-DROID over the floor at 0.20 m: join the a118 clause
_o20 = " at the counter and the desk (median " + V.get("t1_off_by", {}).get("f0", {}).get("d20", {}).get("dmed", "0.15") + " m)."
if _n(_g20.get("rate", "—")) >= 8 and _o20 in t:
    RN(_o20, _o20[:-1] + ", and GR00T N1.6-DROID on " + _g20["rate"] + " of its carries (median " + _g20.get("dmed", "—") + " m).")
if _n(_g20.get("rate", "—")) and 0 < _n(_g20.get("rate", "—")) < 8:
    _add += (" GR00T N1.6-DROID was run at the 0.20 m level too and carried on " + _g20.get("car", "?") + " of " + _g20.get("att", "32") +
             " attempts (" + _g20["rate"] + " entered), under the floor.")
if _add and _anchor in t:
    RN(_anchor, _anchor + _add)
