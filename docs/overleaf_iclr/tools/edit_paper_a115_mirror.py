# -*- coding: utf-8 -*-
# Drift mechanism: base-relative or travel-relative? The mirrored transport decides. Guarded on n >= 8 per surface. Exec'd after a114.
_dr = V.get("drift_rev", {})
def _ok(sf):
    try: return int(_dr[sf]["rev"][1]) >= 8 and _dr[sf]["rev"][0] != "—"
    except Exception: return False
if _ok("desk") and _ok("counter"):
    _bx = [float(_dr[sf]["rev"][0]) for sf in ("desk", "counter")]
    _fw = [float(_dr[sf]["fwd"][0]) for sf in ("desk", "counter")]
    _lf = []
    for sf in ("desk", "counter"):
        try: _lf.append(abs(float(_dr[sf]["rev_left"])))
        except Exception: _lf.append(0.0)
    # base-relative if, with the travel reversed, the bow toward +x is still clearly there (> 2 cm at both surfaces) and larger
    # than any excursion to the left of the new travel direction
    _base_rel = all(b > 0.02 and b > lf for b, lf in zip(_bx, _lf))
    _verdict = ("the bow stays on the same side of the world, away from the base, when the transport is reversed: it is "
                "base-relative, a property of where the arm is mounted, not of the direction of travel"
                if _base_rel else
                "the bow changes sides with the direction of travel: it is travel-relative, a lean to one side of whatever "
                "line the arm is following, not a pull away from the base")
    RN("What the trajectory dimension measures on the tabletop is therefore a bow the policy carries into every transport, "
       "large enough at some surfaces to enter a keep-out that a straight carry clears.",
       "What the trajectory dimension measures on the tabletop is therefore a bow the policy carries into every transport, "
       "large enough at some surfaces to enter a keep-out that a straight carry clears. Reversing the transport (pick and place "
       "swapped, so the arm travels toward +y instead of −y) puts the bow toward +x at " + _dr["desk"]["rev"][0] + " m at "
       "the desk and " + _dr["counter"]["rev"][0] + " m at the counter (forward: " + _dr["desk"]["fwd"][0] + " and " +
       _dr["counter"]["fwd"][0] + "; the blind control " + _dr["desk"]["rev_ik"][0] + " and " + _dr["counter"]["rev_ik"][0] +
       "; the excursion to the left of the reversed travel is " + _dr["desk"]["rev_left"] + " and " + _dr["counter"]["rev_left"] + " m): " + _verdict + ".")
