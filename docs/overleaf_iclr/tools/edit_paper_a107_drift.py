# -*- coding: utf-8 -*-
# A4b/A4c: attraction to a hazard, or a base-relative drift a hazard may lie in? Two guarded branches on the near-side
# marker and the unrendered far-side keep-out. Exec'd after a106 (uses t, RN, V).
_tn, _tu, _sf = V.get("t1_near", {}), V.get("t1_unseen", {}), V.get("t1_off_surf", {})


def _kn(x):
    try:
        k, n = str(x).split("/"); return int(k), int(n)
    except Exception:
        return 0, 0


_nk, _nn = _kn(_tn.get("pi", {}).get("rate", "—"))
_uk, _un = _kn(_tu.get("pi", {}).get("desk", "—"))
_rk, _rn = _kn(_sf.get("desk", {}).get("pi", "—"))
if _nn >= 16 and _un >= 8 and _rn >= 8:
    _near_rate = _nk / _nn
    _drift = (_uk / _un) >= 0.5 * (_rk / _rn) and _near_rate <= 0.15
    _attr = (_uk / _un) <= 0.2 * (_rk / _rn) and _rk / _rn >= 0.3
    if _drift:
        RN("is entered on " + V["t1_off"]["d28"]["rate"] + " by π0.5 and " + V.get("t1_off_pi0", {}).get("d28", {}).get("rate", "3/12") + " by π0.",
           "is entered on " + V["t1_off"]["d28"]["rate"] + " by π0.5 and " + V.get("t1_off_pi0", {}).get("d28", {}).get("rate", "3/12") +
           " by π0 — but only on the far side of the transport: the same marker on the near side is entered on " + _tn["pi"]["rate"] +
           ", and an *unrendered* far-side keep-out on " + _tu["pi"]["rate"] + " (desk " + _tu["pi"]["desk"] + " against " +
           _sf["desk"]["pi"] + " rendered). On the tabletop the bend is a base-relative drift that a hazard may lie in, not a "
           "pull toward what is seen; the attraction finding rests on the G1's rendered-against-hidden stove.")
        RN("with a median clearance of " + V["t1_off"]["d12"]["dmed"] + " m — inside the offset, so the path bends toward the "
           "marker rather than around it — and",
           "with a median clearance of " + V["t1_off"]["d12"]["dmed"] + " m — inside the offset, so the path bends to the far side "
           "of the transport, marker or no marker (the near-side and unrendered cells below) — and")
    elif _attr:
        RN("is entered on " + V["t1_off"]["d28"]["rate"] + " by π0.5 and " + V.get("t1_off_pi0", {}).get("d28", {}).get("rate", "3/12") + " by π0.",
           "is entered on " + V["t1_off"]["d28"]["rate"] + " by π0.5 and " + V.get("t1_off_pi0", {}).get("d28", {}).get("rate", "3/12") +
           " by π0; the same keep-out *unrendered* is entered on " + _tu["pi"]["rate"] + " (desk " + _tu["pi"]["desk"] + " against " +
           _sf["desk"]["pi"] + " rendered), so the bend needs the marker to be seen, and on the near side of the transport it is "
           "entered on " + _tn["pi"]["rate"] + ".")
    else:
        RN("is entered on " + V["t1_off"]["d28"]["rate"] + " by π0.5 and " + V.get("t1_off_pi0", {}).get("d28", {}).get("rate", "3/12") + " by π0.",
           "is entered on " + V["t1_off"]["d28"]["rate"] + " by π0.5 and " + V.get("t1_off_pi0", {}).get("d28", {}).get("rate", "3/12") +
           " by π0; unrendered, the far-side keep-out is entered on " + _tu["pi"]["rate"] + " (desk " + _tu["pi"]["desk"] + " against " +
           _sf["desk"]["pi"] + " rendered) and the near-side marker on " + _tn["pi"]["rate"] + ": part of the bend is a base-relative "
           "drift and part answers to the marker (Appendix E.8).")
