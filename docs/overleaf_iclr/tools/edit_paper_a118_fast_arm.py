# -*- coding: utf-8 -*-
# pi0-FAST on the forearm keep-out (labels f0_t1a20_/f0_t1a28_), appended to the a113 sentence, guarded on the floor and on the
# anchor being present. Exec'd after a117 (uses t, RN, V).
_ar = V.get("t1_arm", {})


def _n(x):
    try:
        return int(str(x).split("/")[1])
    except Exception:
        return 0


_f20 = _ar.get("d20", {}).get("f0", {}).get("rate", "—")
_f28 = _ar.get("d28", {}).get("f0", {}).get("rate", "—")
_old = "; π0 enters the hand's keep-out on " + _ar.get("d20", {}).get("pi0", {}).get("rate", "12/13") + " at 0.20 m and " + \
       _ar.get("d28", {}).get("pi0", {}).get("rate", "2/18") + " at 0.28 m."
if _n(_f20) >= 8 and _n(_f28) >= 8 and _old in t:
    RN(_old, _old[:-1] + ", π0-FAST on " + _f20 + " and " + _f28 + ".")

# pi0-FAST at the 0.20 m level of the off-path series (counter and desk), appended to the a103 clause
_ob = V.get("t1_off_by", {}).get("f0", {}).get("d20", {})
_old20 = "π0 enters on 26/33 of its carries over the four surfaces (median clearance 0.14 m)."
if _n(_ob.get("rate", "—")) >= 8 and _old20 in t:
    RN(_old20, _old20[:-1] + ", and π0-FAST on " + _ob["rate"] + " at the counter and the desk (median " + _ob["dmed"] + " m).")
