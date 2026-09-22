# -*- coding: utf-8 -*-
# Page budget, final: the off-path T1 series moves to E.8 with one clause left in §5.1 (it is already quoted in §6 (ii)).
# Exec'd after a88 (uses t, RN, V).
_t1 = V.get("t1_off", {})
if _t1.get("d28", {}).get("rate", "0/0") != "0/0":
    _old = ("**T1 off the path.** The scored marker sits on the transport, so entry is forced. Moved off it the cell discriminates: " +
            _t1["on"]["rate"] + " at the midpoint, " + _t1["d12"]["rate"] + " at 0.12 m (median clearance " + _t1["d12"]["dmed"] +
            " m, inside the offset) and " + _t1["d28"]["rate"] + " at 0.28 m, which a direct carry clears — the series with headroom.")
    _i = t.find(_old)
    if _i >= 0:
        # drop it from §5.1 and put the full series in Appendix E.8, before the appearance paragraph
        t = t[:_i] + t[_i + len(_old):].lstrip("\n")
        _anchor = "**What the policy sees of the person (appearance ablation).**"
        _j = t.find(_anchor)
        _new = ("**A keep-out off the path (trajectory with headroom).** The scored tabletop marker sits at the midpoint of a "
                "collinear transport with a 0.20 m keep-out, so entering it is forced and " + _t1["on"]["rate"] + " is a ceiling. "
                "Moving the same marker perpendicular to the transport makes the cell discriminating: " + _t1["d12"]["rate"] +
                " at 0.12 m, with a median clearance of " + _t1["d12"]["dmed"] + " m — inside the offset, so the path bends toward "
                "the marker rather than around it — and " + _t1["d28"]["rate"] + " at 0.28 m (median " + _t1["d28"]["dmed"] +
                " m, minimum " + _t1["d28"]["dmin"] + " m), an offset a direct carry clears by construction. We report the "
                "off-path series as the trajectory measurement with headroom and keep the midpoint cell as exposure.\n\n")
        if _j >= 0:
            t = t[:_j] + _new + t[_j:]
