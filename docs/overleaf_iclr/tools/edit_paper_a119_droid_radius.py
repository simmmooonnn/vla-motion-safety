# -*- coding: utf-8 -*-
# Where the drift comes from. (a) The human demonstrations: the droid_100 sample's grasp-to-release transports, measured with the
# paper's drift field (outward vs inward bow from the straight chord). (b) The radius probe: the same transport pinned at five
# distances from the base; if the outward bow shrinks or turns inward as the transport moves out toward the demonstrations'
# radius, the drift is a pull toward where the demonstrations live. Guarded; the verdict is decided from the numbers.
# Exec'd after a118 (uses t, RN, V).
_dd, _rd = V.get("droid", {}), V.get("drift_rad", {})


def _fl(x):
    try:
        return float(x)
    except Exception:
        return None


_anchor_end = ("the bow stays on the same side of the world, away from the base, when the transport is reversed: it is base-relative, "
               "a property of where the arm is mounted, not of the direction of travel.")

_add = ""
# (a) the demonstrations
if _dd.get("n") and int(_dd["n"]) >= 30:
    _add += (" The demonstrations themselves do not carry the bow: over " + _dd["n"] + " grasp-to-release transports in the public "
             "DROID sample (" + _dd["eps"] + " episodes, chord median " + _dd["chord"] + " m), the human path's largest excursion from "
             "the straight chord is " + _dd["out"] + " m outward (away from the base) against " + _dd["in"] + " m inward, outward "
             "larger on " + _dd["frac_out"] + " % — no side is preferred, where π0.5 bows 0.04–0.09 m outward and ≈ 0 inward. What the "
             "demonstrations do carry is a *place*: their transports sit at a median " + _dd["rmid"] + " m from the base (quartiles " +
             _dd["rq1"] + "–" + _dd["rq3"] + "), and the inner ones (below 0.58 m, n = " + _dd["inner_n"] + ") bow outward " +
             _dd["inner_out"] + " m against " + _dd["inner_in"] + " m inward while the outer ones (n = " + _dd["outer_n"] + ") bow inward " +
             _dd["outer_in"] + " m against " + _dd["outer_out"] + " m outward — a mild pull toward the middle of the workspace. The "
             "benchmark's transports run at 0.45–0.54 m, at the inner edge of that range.")

# (b) the radius probe, verdict from the data: does the outward bow fall (or flip) as the transport moves out?
_far = {x: _fl(_rd.get(x, {}).get("pi", {}).get("far", "—")) for x in ("35", "45", "55", "65", "75")}
_n = {x: int(_rd.get(x, {}).get("pi", {}).get("n", "0") or 0) for x in _far}
_ok = [x for x in ("35", "45", "55", "65", "75") if _far[x] is not None and _n[x] >= 8]
if len(_ok) >= 4 and "35" in _ok and "75" in _ok:
    _near = {x: _fl(_rd.get(x, {}).get("pi", {}).get("near", "—")) for x in _ok}
    _f0ok = [x for x in _ok if _fl(_rd.get(x, {}).get("f0", {}).get("far", "—")) is not None and int(_rd[x]["f0"]["n"]) >= 8]
    _tab = ("\n\n| Transport at | π0.5 far / near bow (m) | π0-FAST far / near bow (m) |\n|---|---|---|\n" + V.get("drift_rad_rows", "") + "\n\n")
    if _far["75"] <= 0.5 * _far["35"] and _far["35"] >= 0.02:
        _flip = [x for x in _ok if _near[x] is not None and _near[x] <= -0.02 and _far[x] < 0.02]
        _verdict = ("The outward bow falls from " + f"{_far['35']:.3f}" + " m at 0.35 m to " + f"{_far['75']:.3f}" + " m at 0.75 m" +
                    (" and turns inward at " + " and ".join("0." + x + " m" for x in _flip) if _flip else "") +
                    ": the drift is a pull toward the radius at which the demonstrations were given, not a fixed bend of the arm. "
                    "The keep-out entries of the trajectory dimension are therefore the benchmark's transports sitting inside the "
                    "demonstrations' workspace, and a scene laid out farther from the base would see the bow reverse.")
    elif _far["75"] >= 0.8 * _far["35"]:
        _verdict = ("The outward bow is the same at every distance (" + f"{_far['35']:.3f}" + " m at 0.35 m, " + f"{_far['75']:.3f}" +
                    " m at 0.75 m): the drift is not a pull toward the demonstrations' radius but a fixed outward bend the policy "
                    "adds to every transport.")
    else:
        _verdict = ("The outward bow shrinks with distance (" + f"{_far['35']:.3f}" + " m at 0.35 m, " + f"{_far['75']:.3f}" +
                    " m at 0.75 m) without reversing: part of it is a pull toward the demonstrations' radius, part a fixed bend.")
    _add += (" **The radius probe.** The same transport pinned at five distances from the base (the dining table, the adult across; "
             "median largest excursion outward / inward, carries in parentheses):" + _tab + _verdict)

if _add:
    RN(_anchor_end, _anchor_end + _add)

# section 6 (ii): the mechanism in one clause, only in the falls branch (the bow drops by half or more from 0.35 m to 0.75 m)
if len(_ok) >= 4 and "35" in _ok and "75" in _ok and _far["75"] <= 0.5 * _far["35"] and _far["35"] >= 0.02:
    RN("The arm's bend is a base-relative drift a hazard may lie in, not a pull toward what is seen;",
       "The arm's bend is a pull toward its demonstrations' radius (Appendix E.8) that a hazard may lie in, not toward what is seen;")
    if "on 9/32 (a FAST-token decoder alike; Appendix E.8)." in t:
        RN("on 9/32 (a FAST-token decoder alike; Appendix E.8).", "on 9/32 (a FAST-token decoder alike).")
