# -*- coding: utf-8 -*-
# The scripted carry as a T3 / T4 witness (ik2, blade turned away), the crossed surface x map design (b5), and the control's
# unscored T6b. Exec'd after a47 (uses RN, t, V = N45).
_w = V.get("ik_t3w", {})
if _w and _w.get("R", {}).get("carried") not in (None, "0"):
    _ok = int(_w["R"]["ok_done"]) + int(_w["L"]["ok_done"]); _car = int(_w["R"]["carried"]) + int(_w["L"]["carried"])
    RN("the object's pose sets it, not the person's, and 4 carries then deliver them blade-away — the scene's witness (Appendix E.4, E.8).",
       "the object's pose sets it, not the person's, and 4 carries then deliver them blade-away. A scripted carry that turns the scissors so "
       "the blade points away from the person delivers them that way on " + str(_ok) + "/" + str(_car) + " carries (into the person's "
       "half-space on " + _w["R"]["t3"] + " with the person on the right, " + _w["L"]["t3"] + " on the left): the tabletop T3 witness, and "
       "with its level carry (T4 " + V["ik_T4_pct"] + " %) the T4 witness (Appendix E.4, E.8).")
    RN("| Witness in scene | yes (G1: T1) | yes (tabletop: T3) | yes (G1: T5a; both: T5b) | yes (both: T6) |",
       "| Witness in scene | yes (G1: T1) | yes (tabletop: T3, T4, scripted carry) | yes (G1: T5a; both: T5b) | yes (both: T6) |")
    RN("T2 and T4 have **no witness**, and T3 has one only on the tabletop.",
       "T2 has **no witness**; T3 and T4 have one on the tabletop only (the scripted carry), T1 on the G1 only.")
    RN("Where control and policies agree (T1, T2, T6) the column is set by scene or task; where they differ (T4, and the mechanism behind T3) the policy owns the rate.",
       "Where control and policies agree (T1, T2, T6) the column is set by scene or task; where they differ (T4, and the mechanism behind T3) "
       "the policy owns the rate. The control's carry is too short to meet the passer-by mid-transport (one scored episode), so its T6b stays unscored.")
if V.get("b5_rows"):
    RN("**Bystander height and receiver state (next-cycle probes, run last).**",
       "**A crossed surface × map design (next-cycle probe).** Two work surfaces under three environment maps, one seed, eight episodes per "
       "cell (Table IVd): every mug carry completes under every map, and the map is not always inert — at the counter the mug leaves upright "
       "by more than 45° on 8/8 carries under the lounge map and 3/8 under the outdoor courtyard map, at the packing station on 4/8–6/8; the "
       "scissors' presentation is too sparse per cell to compare (9/28 pooled). A surface × map effect on tilt is therefore a live "
       "hypothesis for the next cycle, not a result.\n\n"
       "**Table IVd. Crossed design: work surface × environment map, π0.5, seed 42.** Carried / attempted, delivered; the mug's T4 and the "
       "scissors' T3 (counts, below the floor); T2 is not scored on these cells (no person term in the map cells' T2 pool).\n\n"
       "| Surface | Map | Mug | Scissors |\n|---|---|---|---|\n" + V["b5_rows"] + "\n\n"
       "**Bystander height and receiver state (next-cycle probes, run last).**")
