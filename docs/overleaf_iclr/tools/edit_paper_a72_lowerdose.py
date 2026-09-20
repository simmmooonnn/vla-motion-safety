# -*- coding: utf-8 -*-
# The bowl-offset fall-off for the seated and the child-height bystander. Exec'd after a71 (uses t, RN, V).
_ld = V.get("svh_d45", {})
if _ld.get("seated", {}).get("att", "0") not in ("0", "") and _ld.get("child", {}).get("att", "0") not in ("0", ""):
    RN("a lower head is swept less because it is lower, not because the carry changes.",
       "a lower head is swept less because it is lower, not because the carry changes; with the bowl 0.45 m from them the sweep is " +
       _ld["seated"]["T2"] + " (seated) and " + _ld["child"]["T2"] + " (child), the same fall-off as for the adult.")
