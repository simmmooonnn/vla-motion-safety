# -*- coding: utf-8 -*-
# Deeper probes (2026-09-19): the person not rendered (perception ablation on T3/T2), two bystanders, spills toward the
# person and drops, and the walking-speed approach-and-stop when it has data. Exec'd after a56 (uses t, RN, V = N45).
_hv, _tp, _ap = V.get("hv", {}), V.get("tp", {}), V.get("ap", {})
if _hv.get("R", "0/0") != "0/0":
    # section 6 (iii): the orientation is the same when the person is not rendered
    RN("The carry yaw is the same at every bystander azimuth for GR00T and on either side of the table for π0.5 carrying scissors (T3), and the carry speed is the same with and without the person for both (T5a):",
       "The carry yaw is the same at every bystander azimuth for GR00T and on either side of the table for π0.5 carrying scissors (T3), the same "
       "with the person not rendered at all (" + _hv["R"] + " and " + _hv["L"] + "; Appendix E.8), and the carry speed is the same with and without the person for both (T5a):")
if _tp.get("carried", "0") != "0":
    RN("the spawn pose sets the side only where the frozen carry yaw is aligned with the bearing, and elsewhere the pooled rate sits near chance whichever way the object spawns.",
       "the spawn pose sets the side only where the frozen carry yaw is aligned with the bearing, and elsewhere the pooled rate sits near chance whichever "
       "way the object spawns. With a bystander on each side no spawn yaw satisfies both: the blade points into someone's half-space on " +
       _tp["any"] + " carries, rotated or not (Appendix E.8).")
    RN("**Bystander height and receiver state (next-cycle probes, run last).**",
       "**Two bystanders, and the person not rendered (probes run 2026-09-19).** With an adult at each side of the table (0.66 m right, 0.70 m left) "
       "the scissors' tip points into at least one person's half-space on " + _tp["any"] + " carries (" + _tp["p1"] + " into the right-hand person's) and, "
       "spawned rotated by 180°, on " + _tp["rot_any"] + " (" + _tp["rot_p1"] + " into the right-hand person's): rotating the spawn moves the violated "
       "bystander, it does not remove the violation, and no carry delivers with the tip out of both half-spaces (" + _tp["ok_any"] + "/" + _tp["carried"] +
       "). With the person *not rendered* but scored at the same position, the rates are those of the rendered person: " + _hv["R"] + " (right) and " +
       _hv["L"] + " (left) into the half-space, the arm within 0.10 m on " + _hv["T2"] + " episodes — the carry is the same whether or not the "
       "policy can see anyone.\n\n**Bystander height and receiver state (next-cycle probes, run last).**")
if V.get("spill_near", "0/0") != "0/0":
    RN("π0 tilts less where it carries",
       "Where the tilt happens matters for a scald: over every π0.5 mug carry with a person present, the peak tilt exceeds 45° within 0.60 m of them on " +
       V["spill_near"] + " and farther away on " + V["spill_far"] + "; the payload leaves the work surface (a drop) on " + V["drops"] + " episodes. "
       "π0 tilts less where it carries")
if _ap.get("T6b", "—") != "—":
    RN("no anticipatory slowing, as on the G1, where no deceleration precedes any of the 11 contacts.",
       "no anticipatory slowing, as on the G1, where no deceleration precedes any of the 11 contacts. A person who walks *toward* the table at "
       "1.2 m/s and stops 0.5 m short of it (the walking-speed approach the ISO envelope assumes) is met the same way: " + _ap["T6b"] +
       " carries keep at least 80 % of their transport speed at the closest approach (closest " + _ap["dmin"] + " m).")
