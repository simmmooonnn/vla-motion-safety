# -*- coding: utf-8 -*-
# The re-timed walker at the office desk and the kitchen counter; the keep-upright command at the packing station and the drawer kitchen. Exec'd after a68 (uses t, RN, V).
_hs, _ws = V.get("hot_surf", {}), V.get("wk_surf", {})
if _hs.get("packing", {}).get("car", "0") not in ("0", "") and _hs.get("drawer", {}).get("car", "0") not in ("0", ""):
    RN("nor at the kitchen counter (" + _hs["counter"]["T4"] + " past 45°) or the office desk (" + _hs["office"]["T4"] + ").",
       "nor at the kitchen counter (" + _hs["counter"]["T4"] + " past 45°), the office desk (" + _hs["office"]["T4"] + "), the packing station (" +
       _hs["packing"]["T4"] + ") or the drawer kitchen (" + _hs["drawer"]["T4"] + ").")
if _ws.get("office2", {}).get("car", "0") not in ("0", "") and _ws.get("counter2", {}).get("car", "0") not in ("0", ""):
    _o, _c = _ws["office2"], _ws["counter2"]
    RN("a timing mismatch of the scene, reported, not scored (Table IV).",
       "a timing mismatch of the scene, reported, not scored (Table IV). Started 0.60 m nearer, the walker still meets the place phase on " + _o["late"] + " and " +
       _c["late"] + " of the transports; the mid-transport passes are met at 80 % or more of the transport speed on " + _o["T6b"] + " (desk) and " + _c["T6b"] + " (counter); these re-timed cells are pooled into Table III.")
