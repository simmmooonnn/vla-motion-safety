# -*- coding: utf-8 -*-
# Pouring as a second goal for T1 and T6 (queues pourx, f0pourx; the pour crossing cells rerun in hx9b with the hand that
# withdraws out of reach; 2026-10-04). A keep-out marker beside the jug's transport at the kitchen counter, and the crossing
# hand at the dining table. Extended the same day (queues g2a, g2b): pouring into, and stirring, a bowl on the serving
# placement beside the person (T2), and pouring while a person walks past (T6b). Written when the cells exist; every number
# from the generator; below the eight-episode floor the count is given and no rate is read. Exec'd after a153 (uses t, _rn2, V).
_po = (V.get("pour2") or {}).get("pi")
if _po:
    _f0p = (V.get("pour2") or {}).get("f0")
    _n = lambda s_: int(s_.split("/")[1]) if s_ and "/" in s_ else 0
    _kh, _nh = (int(v) for v in _po["hx"].split("/")) if "/" in _po["hx"] else (0, 0)
    _sp = V.get("sv2_pour_pi05"); _ss = V.get("sv2_stir_pi05"); _pw = V.get("pour_T6b_pi05")
    _GN = V.get("goals_n_by_sub", {})
    _gn = lambda sid, goal: _GN.get(sid, {}).get("pi", {}).get(goal, 0)
    _pour_in = [sid for sid in ("T1", "T2", "T6", "T6b") if _gn(sid, "pour") >= 8]
    _pour_low = [sid for sid in ("T1", "T2", "T6", "T6b") if 0 < _gn(sid, "pour") < 8]
    _stir_in = _gn("T2", "tool use: stir") >= 8
    _lst = lambda xs: xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]
    _head = "**Pouring and stirring, further goals.**" if (_sp or _ss or _pw) else "**Pouring, a second goal.**"
    _par = (_head + " The trajectory and dynamics predicates do not depend on the instruction, so they are "
            "also run while π0.5 pours milk from a jug into the bowl (" + _po["carried"] + "/" + _po["att"] + " attempts carried at "
            "the keep-out and crossing-hand cells). "
            "A marker 0.20 m beside the jug's transport at the kitchen counter is entered on " + _po["t1_20"] + " carries and one "
            "0.28 m beside it on " + _po["t1_28"] + "; at the dining table the crossing hand is reached on " + _po["hx"]
            + (" (below the eight-episode floor, a count)" if _nh < 8 else "") + " and waited for on " + _po["hx_wait"] + ".")
    if _sp or _ss:
        _bits = []
        if _sp:
            _bits.append(_sp["t2"] + " pouring episodes" + (" (a count)" if _n(_sp["t2"]) < 8 else ""))
        if _ss:
            _bits.append(_ss["t2"] + " stirring ones" + (" (a count)" if _n(_ss["t2"]) < 8 else ""))
        _par += (" With the bowl on the serving placement beside the person, a link enters the 0.10 m band on "
                 + " and on ".join(_bits)
                 + ((", against " + V["sv2_pnp_pi05"] + " for pick-and-place onto that placement") if V.get("sv2_pnp_pi05") else "")
                 + ".")
    if _pw:
        _pwk = V.get("pour_wk_pi05") or {}
        _par += (" While a person walks past the pour" + ((" (" + _pwk["carried"] + "/" + _pwk["att"] + " attempts carried)")
                                                          if _pwk.get("att") else "")
                 + ", the jug keeps at least 0.8 of its transport speed at the closest approach "
                 "on " + _pw + (" (a count)" if _n(_pw) < 8 else "")
                 + ((" (pick-and-place, the same passer-by: " + V["wk_pnp_pi05"] + ")") if V.get("wk_pnp_pi05") else "") + ".")
    _par += (" π0-FAST does not carry the jug (" + _f0p["carried"] + "/" + _f0p["att"] + ")." if _f0p and _f0p["carried"] == "0" else "")
    _par += (" Table IVe counts pouring as a further goal of " + (_lst(_pour_in) if _pour_in else "no sub-type")
             + (", and of " + _lst(_pour_low) + " after its plus sign" if _pour_low else "")
             + (", and stirring as one of T2" if _stir_in else "") + ".")
    _i = t.find("**A hand that withdraws when touched (reactive proxy).**")
    if _i > 0:
        t = t[:_i] + _par + "\n\n" + t[_i:]
    else:
        print("  [a154 MISS] anchor for the pouring paragraph")
# the pour positive control's main-text count, generated (it had been a literal since a129)
if V.get("pour", {}).get("away"):
    _rn2("a pour tilts away from the bowl on 2/26 carries,", "a pour tilts away from the bowl on " + V["pour"]["away"] + " carries,")
