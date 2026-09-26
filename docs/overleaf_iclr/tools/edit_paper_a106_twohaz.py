# -*- coding: utf-8 -*-
# A4: two hazards flanking the path, and (A4b, guarded) the single marker on the near side alone. Exec'd after a105.
_tw, _tn = V.get("t1_two", {}), V.get("t1_near", {})


def _n(x):
    try:
        return int(str(x).split("/")[1])
    except Exception:
        return 0


if _n(_tw.get("pi", {}).get("any", "—")) >= 8 and _n(_tw.get("ik", {}).get("any", "—")) >= 8:
    _near = ""
    if _n(_tn.get("pi", {}).get("rate", "—")) >= 8 and _n(_tn.get("ik", {}).get("rate", "—")) >= 8:
        _near = (" The near-side marker alone settles which: at 0.28 m on the robot's side of the path it is entered on " +
                 _tn["pi"]["rate"] + " carries (median clearance " + _tn["pi"]["dmed"] + " m; the control " + _tn["ik"]["rate"] +
                 "), against " + V.get("t1_off", {}).get("d28", {}).get("rate", "12/64") + " for the far-side marker.")
    RN("A person who visibly prepares to move is met exactly as one who does not.",
       "A person who visibly prepares to move is met exactly as one who does not. Two markers instead of one, flanking the "
       "transport at 0.28 m on either side so that a straight carry clears both, separate attraction from drift: the policy "
       "enters the far-side keep-out on " + _tw["pi"]["one"] + " carries (desk " + _tw["pi"]["desk"] + ", counter " +
       _tw["pi"]["counter"] + ") and the near-side one, toward the robot's base, on " + _tw["pi"]["two"] + ", passing it farther "
       "than a straight line would; the blind carrier enters either on " + _tw["ik"]["any"] + ". The bend is one-sided — away "
       "from the base — so a second hazard neither cancels it nor draws its own." + _near)
