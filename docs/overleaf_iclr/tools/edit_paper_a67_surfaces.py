# -*- coding: utf-8 -*-
# The keep-upright command and the passer-by at two more surfaces. Exec'd after a66 (uses t, RN, V).
_hs, _ws = V.get("hot_surf", {}), V.get("wk_surf", {})
if _hs.get("counter", {}).get("car", "0") not in ("0", "") and _hs.get("office", {}).get("car", "0") not in ("0", ""):
    RN("(the task battery's tilt rates are in Table IV). Told to keep hot coffee upright, it still tilts the mug past 45° on " + V.get("pi_t4_hot", "16/24") +
       " (27°: " + V.get("pi_t4_hot27", "21/24") + "): the command does not change the carry.",
       "(the task battery's tilt rates are in Table IV). Told to keep hot coffee upright, it still tilts the mug past 45° on " + V.get("pi_t4_hot", "16/24") +
       " (27°: " + V.get("pi_t4_hot27", "21/24") + "): the command does not change the carry, nor at the kitchen counter (" + _hs["counter"]["T4"] +
       " past 45°) or the office desk (" + _hs["office"]["T4"] + ").")
if _ws.get("office", {}).get("car", "0") not in ("0", "") and _ws.get("counter", {}).get("car", "0") not in ("0", ""):
    RN("walking past at 0.55 m/s is passed at 80 % or more of the transport speed on " + V.get("wkch", {}).get("T6b", "17/27") + " carries (closest " +
       V.get("wkch", {}).get("dmin", "0.44") + " m; touched on " + V.get("wkch", {}).get("touch", "0/35") + ").",
       "walking past at 0.55 m/s is passed at 80 % or more of the transport speed on " + V.get("wkch", {}).get("T6b", "17/27") + " carries (closest " +
       V.get("wkch", {}).get("dmin", "0.44") + " m; touched on " + V.get("wkch", {}).get("touch", "0/35") + "). The same adult walker launched at the office desk and the "
       "kitchen counter arrives while the payload is already being set down (the closest approach falls within 1 s of the place on " + _ws["office"]["late"] + " and " +
       _ws["counter"]["late"] + " of the transports), which leaves " + _ws["office"]["T6b"].split("/")[1] + " and " + _ws["counter"]["T6b"].split("/")[1] +
       " mid-transport passes (" + _ws["office"]["T6b"] + ", " + _ws["counter"]["T6b"] + " fast): a timing mismatch of the scene, reported, not scored (Table IV).")
