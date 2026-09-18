# -*- coding: utf-8 -*-
# B9: the rotated-spawn manipulation at other placements and on the fork. Exec'd after a48 (uses RN, t, V = N45).
_b9 = V.get("b9", {})
if _b9 and _b9.get("acr_rot", "0/0") != "0/0":
    RN("the object's pose sets it, not the person's, and 4 carries then deliver them blade-away.",
       "the object's pose sets it, not the person's, and 4 carries then deliver them blade-away; the manipulation does not travel, though — "
       "with the person across the far edge or at the far-right corner, and for the fork on either side, a 180° spawn leaves the rate near "
       "where it was (" + _b9["acr_rot"] + " vs " + _b9["acr"] + ", " + _b9["fr_rot"] + " vs " + _b9["fr"] + ", " + _b9["forkR_rot"] +
       " vs " + _b9["forkR"] + ", " + _b9["forkL_rot"] + " vs " + _b9["forkL"] + "; Appendix E.8): the spawn pose sets the side only where "
       "the frozen carry yaw is aligned with the bearing, and elsewhere the pooled rate sits near chance whichever way the object spawns.")
    RN("**Bystander height and receiver state (next-cycle probes, run last).**",
       "**Rotated spawn at other placements and on the fork (next-cycle probe).** The 180° spawn rotation that moves the scissors' violated "
       "side at the left and right placements (5/13 against 10/10; 12/15 against 1/10) was repeated with the person across the far edge and "
       "at the far-right corner, and with the fork on either side: " + _b9["acr_rot"] + " against " + _b9["acr"] + " (across), " +
       _b9["fr_rot"] + " against " + _b9["fr"] + " (far right), " + _b9["forkR_rot"] + " against " + _b9["forkR"] + " (fork, right), " +
       _b9["forkL_rot"] + " against " + _b9["forkL"] + " (fork, left). Where the carry yaw is roughly perpendicular to the bearing (the far "
       "placements; the fork, carried tines-back), rotating the spawn does not move the side, and the rate stays near chance: the causal spine "
       "is the alignment between a frozen carry yaw and the bearing to the person, not the spawn as such.\n\n"
       "**Bystander height and receiver state (next-cycle probes, run last).**")
