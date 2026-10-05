# -*- coding: utf-8 -*-
# Consistency audit wf_fe8809d8-343, range design: confirmed findings applied (exec at the end of the chain; uses t, _rn2, V).


def _a175d_t4(rows, label, fb):
    # delivered/attempted of one Table IV row ("| label | attempted / carried / delivered |"), from the generator string
    import re
    m = re.search(r"\|\s*" + re.escape(label) + r"\s*\|\s*(\d+)\s*/\s*(\d+)\s*/\s*(\d+)\s*\|", rows or "")
    return "%s/%s" % (m.group(3), m.group(1)) if m else fb


def _a175d_g1(heat, i, fb):
    # one G1 cell of the heat rows as a rounded percentage and a k/n count
    try:
        c = [r for r in heat if "G1" in r["name"]][0]["cells"][i]
        return "%d" % int(round(100.0 * c[0] / c[1])), "%d/%d" % (c[0], c[1])
    except Exception:
        return fb


_a175d_t4rows = V.get("tab4_rows", "")
_a175d_g1T2 = _a175d_g1(V.get("heat_rows", []), 1, ("84", "27/32"))

# F38 (l.62): T6b reads the carry's own transport speed, so the hazard functional takes trajectory context, phi_h(tau, t)
_rn2(r"hazard functional $\phi_h(s_t)$", r"hazard functional $\phi_h(\tau,t)$")
_rn2(r"\psi_h\big(\phi_h(s_t)\big)", r"\psi_h\big(\phi_h(\tau,t)\big)")

# F27 (l.64, follows the l.96 fix): the T2 sweep is not a pick-phase event on the tabletop (it happens at the serving destination)
_rn2("as for T2's pick-phase sweep", "as for T2's body sweep")

# F29 (l.68): the sub-types are scored on the pools where each predicate is available, not on the same episodes
_rn2("scored on the same episodes, so they are separate by what they measure, not by which episodes they use,",
     "each scored on the episodes where its predicate is available, so they are separate by what they measure,")

# F22 (l.68): the 97 % was the G1 on-path T1 (121/125, exposure); use a scored split from Table III (G1 T2 against a level load)
_rn2("GR00T enters the keep-out on 97 % of carries while its load stays level",
     "GR00T's body sweeps into bystanders on %s %% of episodes while its load stays level" % _a175d_g1T2[0])

# F28 (l.68): the tests behind (iii) are non-detections; say so instead of 'no quantity is conditioned'
_rn2("no quantity is conditioned on the person (§6 iii)", "no quantity detectably depends on the person (§6 iii)")

# F41 (l.68): a layer below the policy (governor, protective stop) does cover T5a/T6 in the witnesses; it intercepts, it does not prevent
_rn2("that no layer below the policy — collision checker, protective stop, force limit — covers (Appendix B)",
     "that layers below the policy — collision checker, protective stop, force limit — at best intercept (Appendix B)")

# F31 (l.72): the third fixability class is 'only by an external safety layer'; a missing competence is consistent with it, not shown by elimination (§6 iv)
_rn2("is, by elimination, a missing behavioral competence (§6).",
     "needs an external layer, consistent with a missing behavioral competence (§6).")

# F30 (l.72): T5c is met on 5/41, so the scene does not force it (not exposure), and the tools measured are not sharp: a labelled secondary quantity
_rn2("and a sharp tool may not touch a person at all, so its rate is an exposure (E.8).",
     "so it is a labelled secondary quantity (Table IIIc; E.8).")

# F43 (l.78): Table II states the tabletop T1 keep-out radius too (0.20 m, marker or resting hand; E.8)
_rn2("clearance < keep-out (0.20 m strip, person; 0.30 m stove)",
     "clearance < keep-out (0.20 m strip, person, marker, hand; 0.30 m stove)")

# F39 (l.85): the scored tabletop T6 is the crossing hand; the reaching hand is exposure
_rn2("min separation to a crossing person or a reaching hand",
     "min separation to a crossing person or hand (a reaching hand: exposure)")

# F37 (l.86): the G1 T6b rule is the absence of any deceleration (E.7), the tabletop's the 80 % rule; Table II now says so
_rn2("≥ 80 % of the transport speed inside the stop distance (no slowing)",
     "≥ 80 % of the transport speed inside the stop distance (G1: no deceleration)")

# F40 (l.92): GR00T N1.6-DROID runs in the tabletop family; the corridor family is the G1's
_rn2("All GR00T tasks share one scene family", "All G1 tasks share one scene family")

# F25 (l.92): on the tabletop only the crossing hand is scored T6; the reaching hand and the contact force T5b are exposure
_rn2("a hand reaching into the destination bowl or crossing the transport line (T5b, T6)",
     "a hand crossing the transport line (T6; one reaching into the bowl, and T5b, are exposure)")

# F24 (l.92): Table IV tiers handover and drawer 'carried, not delivered' (drawer 3/56, not pi0-FAST's 1/32); only the door is a capability boundary
_rn2("*carried, not delivered*; *capability boundary*: handover 2/48, drawer 1/32 delivered, door 0/8)",
     "*carried, not delivered*: handover %s and drawer %s delivered; *capability boundary*: door %s)" % (
         _a175d_t4(_a175d_t4rows, "handover", "2/48"),
         _a175d_t4(_a175d_t4rows, "put away in a drawer", "3/56"),
         _a175d_t4(_a175d_t4rows, "close a door", "0/8")))

# F33 (l.96): E.2 says 40 of the 41 stall at the shelf and one reaches a quarter of the way; none reaches the hazard
_rn2("all 41 non-completing blind and hidden T1 episodes stall at the shelf, before the hazard is on the path",
     "40 of the 41 non-completing blind and hidden T1 episodes stall at the shelf and none reaches the hazard")

# F42 (l.96): the serving bowl is 0.32 m from the person's axis (E.8), not from the body surface
_rn2("the destination bowl 0.32 m from the body", "the destination bowl 0.32 m from the person's axis")

# F27 (l.96): the tabletop sweep happens at the serving destination, not at the pick; the reason for scoring over episodes is that it needs no carry
_rn2("since the sweep happens at the pick", "since the arm can sweep without carrying")

# F26 (l.96): no serving or handover rate uses delivered as its denominator (serving T2 over all episodes, T3/T4 and handover T3 over carried)
_rn2("transport sub-types condition on carried, serving and handover on delivered (Appendix E.8)",
     "transport sub-types condition on carried (Appendix E.8)")

# F34 (l.96): ablations are tested on clearance by Mann-Whitney and TOST and on rates by Fisher or McNemar (E.1, §6 i); the shield p is Fisher's
_rn2("paired ablation arms by McNemar's test on the episodes both complete",
     "ablation arms on clearance (Mann–Whitney, TOST) and on rates (Fisher, McNemar)")

# F35 (l.96): fig:scatter plots ablation, shield and control cells (humanoid, plus three early pi0.5 T1 arms), not every cell
_rn2("plots every cell's completion against its unsafe rate", "plots ablation cells' completion against their unsafe rate")

# F23 (l.98): the G1 T5b is a kinematic body's constraint force (exposure), so the G1 speed-and-force set is {T5a} (Table III prints T5a 100)
_rn2("{T5a, T5b} on the humanoid and *exposure* on the tabletop (T5b there is the capsule's constraint force, not what a free hand feels; E.8)",
     "{T5a} on the humanoid (its T5b, like the tabletop's, is a kinematic body's constraint force) and *exposure* on the tabletop (E.8)")

# F36 (l.98): Table IVe covers the tabletop family only (its caption omits the humanoid's rows)
_rn2("behind each cell of Table III.", "behind each tabletop cell of Table III.")

# F32 (l.102): Table III marks no per-cell witness; the scored cells without one (T6b on both embodiments, G1 T2-T4) are named as unattributed
_rn2("Table III marks which rates have one; T2's covers one serving placement (E.8).",
     "T6b and G1 T2–T4 have no witness (unattributed); tabletop T2's covers one serving placement (E.8).")

# --- appendix counterparts named in the findings' fixes ---

# F30 (Appendix D, T5c bullet): same wording as l.72 -- a labelled secondary quantity, not an exposure
_rn2("a sharp tool is excluded from permitted contact, so the rate is an exposure;",
     "a sharp tool is excluded from permitted contact;")
_rn2("adopted post hoc, so it is kept out of every score and reported as an exposure",
     "adopted post hoc, so it is kept out of every score and reported as a labelled secondary quantity (Table IIIc)")

# F37 (Appendix D, T6b bullet): state each embodiment's rule in the terms of Table II
_rn2("[60]; any deceleration passes;",
     "[60]; on the tabletop a slowdown below 80 % of the transport speed passes, on the G1 any deceleration;")

# F42 (E.8, l.1906): the serving bowl offset is from the person's axis, as in l.96 and E.8
_rn2("(bowl 0.32 m from the body)", "(bowl 0.32 m from the person's axis)")
