# -*- coding: utf-8 -*-
# Second and third policies on the queue-A probes, all guarded on the floor: pi0 on the forearm keep-out, the hurry
# instruction and the cue walker; GR00T-DROID on the near-side marker and the unrendered far-side keep-out. Exec'd after a112.
_ar, _hu0, _cu0 = V.get("t1_arm", {}), V.get("hurry_pi0", {}), V.get("cue_pi0", {})
_tn, _tu = V.get("t1_near", {}), V.get("t1_unseen", {})


def _n(x):
    try:
        return int(str(x).split("/")[1])
    except Exception:
        return 0


# pi0 on the forearm keep-out
if _n(_ar.get("d20", {}).get("pi0", {}).get("rate", "—")) >= 8:
    RN("the keep-out a body part defines is treated as the marker was, which is what makes the tabletop T1 the same measurement as the G1's.",
       "the keep-out a body part defines is treated as the marker was, which is what makes the tabletop T1 the same measurement as "
       "the G1's; π0 enters the hand's keep-out on " + _ar["d20"]["pi0"]["rate"] + " at 0.20 m and " + _ar["d28"]["pi0"]["rate"] + " at 0.28 m.")

# pi0 told to hurry
_hm0 = _hu0.get("v_mug", {}).get("hurry", ("—", "0"))
if isinstance(_hm0, tuple) and _hm0[0] != "—" and int(_hm0[1]) >= 8:
    RN("Whatever a command does to speed, it does it without regard to the person on either side of the instruction.",
       "π0 answers the same command with " + _hm0[0] + " m/s against " + _hu0["v_mug"]["neutral"][0] + " with the mug and the "
       "passer-by met at 80 % or more on " + _hu0["t6b"]["hurry"][0] + " (neutral " + _hu0["t6b"]["neutral"][0] + "). Whatever a "
       "command does to speed, it does it without regard to the person on either side of the instruction.")

# pi0 and the cue-bearing walker
if int(_cu0.get("n_cue", "0")) >= 8 and int(_cu0.get("n_nocue", "0")) >= 8:
    RN("A person who visibly prepares to move is met exactly as one who does not.",
       "A person who visibly prepares to move is met exactly as one who does not (π0: " + _cu0["cue_med"] + " m/s with the cue "
       "against " + _cu0["nocue_med"] + " without, " + _cu0["n_cue"] + " and " + _cu0["n_nocue"] + " carries).")

# GR00T-DROID on the near side and the unrendered far side
if _n(_tn.get("g0", {}).get("rate", "—")) >= 8 and _n(_tu.get("g0", {}).get("rate", "—")) >= 8:
    RN("The near-side marker alone settles which:",
       "GR00T N1.6-DROID, whose far-side entries were " + V.get("t1_off_gr00t", {}).get("rate", "15/15") + ", enters the near-side "
       "marker on " + _tn["g0"]["rate"] + " and the unrendered far-side keep-out on " + _tu["g0"]["rate"] + ": the same base-relative "
       "bend. The near-side marker alone settles which:")
