# -*- coding: utf-8 -*-
# Review round 3, the three results that landed: a non-ceiling T1 series (C4), a three-level appearance ablation (C2), and
# the small bystanders re-rendered to match what is scored (C6). Exec'd after a85 (uses t, RN, V).
_t1 = V.get("t1_off", {})
_ap = V.get("appear", {})
_sv = V.get("small_vis", {})

# --- C4: the trajectory dimension gains headroom. Main text carries the one number that matters.
if _t1.get("d28", {}).get("rate", "0/0") != "0/0":
    RN("and on π0.5 a rendered marker is crossed as often as an unrendered point (16/16).",
       "and on π0.5 a rendered marker is crossed as often as an unrendered point (16/16), while a marker moved " + "0.28" +
       " m off the transport — which a straight carry clears — is still entered on " + _t1["d28"]["rate"] + " carries.")
    RN("**T1: completing carries pass through the keep-out.**", "**T1 off the path (review probe).** The scored tabletop marker sits on the transport, so entering it is forced and the rate is a "
       "ceiling; moving the same marker off the path makes the cell discriminating: " + _t1["on"]["rate"] + " at the midpoint, " +
       _t1["d12"]["rate"] + " at " + "0.12" + " m off it (median clearance " + _t1["d12"]["dmed"] + " m, i.e. inside the offset: "
       "the path bends toward the marker) and " + _t1["d28"]["rate"] + " at " + "0.28" + " m off it (median " + _t1["d28"]["dmed"] +
       " m, minimum " + _t1["d28"]["dmin"] + " m), where a direct carry would not violate at all. We report the off-path series as "
       "the trajectory measurement with headroom and keep the midpoint cell as exposure.\n\n"
       "**T1: completing carries pass through the keep-out.**")

# --- C2: appearance, three levels, same cells and seeds
if _ap.get("mesh", {}).get("T3_R", "—") != "—":
    RN("the same with the person not rendered at all (" + V.get("hv", {}).get("R", "8/8") + " and " + V.get("hv", {}).get("L", "0/10") +
       "; Appendix E.8), and the carry speed is the same with and without the person for both (T5a):",
       "the same whether that person is rendered as a capsule proxy, as a photorealistic articulated human, or not at all "
       "(Appendix E.8), and the carry speed is the same with and without the person for both (T5a):")
    RN("**Two bystanders, and the person not rendered (probes run 2026-09-19).**",
       "**What the policy sees of the person (appearance ablation).** The scored bystander is a capsule with a head sphere; the "
       "photorealistic articulated human of the demonstration figures is a rendering choice, not a different scored body. Over "
       "the same cells and seeds the presentation rate does not distinguish the three: into the person's half-space on " +
       _ap["capsule"]["T3_R"] + " (capsule), " + _ap["mesh"]["T3_R"] + " (human mesh) and " + _ap["hidden"]["T3_R"] +
       " (nothing rendered at the scored position) on the right, and " + _ap["capsule"]["T3_L"] + ", " + _ap["mesh"]["T3_L"] +
       ", " + _ap["hidden"]["T3_L"] + " on the left; the arm comes within 0.10 m on " + _ap["capsule"]["T2"] + ", " +
       _ap["mesh"]["T2"] + " and " + _ap["hidden"]["T2"] + ". Person-blindness is therefore blindness to a person at any "
       "appearance we can render, not an artefact of an impoverished proxy.\n\n"
       "**Two bystanders, and the person not rendered (probes run 2026-09-19).**")

# --- C6: the small bystanders, re-rendered to match the scored band
if _sv.get("child", {}).get("new_T3", "—") != "—":
    RN("the hazardous end is not lowered for a smaller person.",
       "the hazardous end is not lowered for a smaller person. Those cells scored a smaller capsule while still rendering the "
       "standing adult, so they measured a counterfactual exposure rather than a response to a smaller person. Re-run with the "
       "rendered body matching the scored band (a " + "1.10" + " m child, a seated proxy with its head at " + "1.27" + " m), they "
       "give the same answer: the arm comes within 0.10 m on " + _sv["child"]["new_T2"] + " and " + _sv["seated"]["new_T2"] +
       " episodes (previously " + _sv["child"]["old_T2"] + " and " + _sv["seated"]["old_T2"] + "), the blade points into their "
       "half-space on " + _sv["child"]["new_T3"] + " and " + _sv["seated"]["new_T3"] + " carries (previously " +
       _sv["child"]["old_T3"] + " and " + _sv["seated"]["old_T3"] + "), and the served mug passes 45° on " +
       _sv["child"]["new_T4"] + " and " + _sv["seated"]["new_T4"] + " (previously " + _sv["child"]["old_T4"] + " and " +
       _sv["seated"]["old_T4"] + ").")
