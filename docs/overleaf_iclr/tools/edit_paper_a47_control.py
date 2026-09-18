# -*- coding: utf-8 -*-
# Roadmap A6 + B3/B1 results: the scripted straight-line carry as the control row, and the child-height / seated bystander and
# receiver-state probes. Exec'd after a46 (uses RN, t, V = N45).
if V.get("has_scripted"):
    RN("*Witness*: a compliant completion shown in the scene.\n\n| Policy | Trajectory (T1, T2) |",
       "*Witness*: a compliant completion shown in the scene. The last row is a **scripted control**: a straight-line carry from "
       "privileged state (differential IK, payload attached to the tool centre, blind to the person) on the same cells; a column on "
       "which it scores like the policies is set by the scene or the task, not by the policy.\n\n| Policy | Trajectory (T1, T2) |")
    RN("a pushed object ends within reach of the person on 2/16.",
       "a pushed object ends within reach of the person on 2/16.\n\n"
       "**A scripted straight-line carry as the control.** On the same canonical cells a scripted carrier that reads the payload and bowl "
       "poses from the simulator, ignores the person and moves the payload on a straight line at " + V["ik_v_trans"] + " m/s (" +
       V["ik_carried"] + " carried episodes; last row of Table III) scores T1 " + V["ik_T1_pct"] + " % (" + V["ik_T1"] + "): the rendered "
       "marker sits between pick and place, so any direct carry crosses it, and the tabletop T1 is a property of the scene. It scores T2 " +
       V["ik_T2_pct"] + " % (" + V["ik_T2"] + "), as the policies do: the fixed arm's body sweep is set by the geometry. Its T3 is " +
       V["ik_T3_pct"] + " % pooled — " + V["ik_T3_R"] + " with the person on the right and " + V["ik_T3_L"] + " on the left — the same "
       "side split as π0.5 (" + V["pi_T3_R"] + " and " + V["pi_T3_L"] + "): a carrier that never turns its payload scores exactly this, so "
       "π0.5's presentation rate is the signature of a carry yaw that does not respond to the person and of nothing else. It scores T4 " +
       V["ik_T4_pct"] + " % (" + V["ik_T4"] + ") where π0.5 scores " + V["pi_T4_pct"] + " %: a level carry exists on these cells, which "
       "makes the tabletop T4 attributable to the policy — the T4 witness the design lacked. It reaches the coworker's hand on " +
       V["ik_T6"] + " (T6) and presses on it above 140 N on " + V["ik_T5b"] + " (T5b): the reaching-hand cell is one no direct carrier "
       "can pass, so its T6 rate is exposure and its T5b the force of a descent. Where control and policies agree (T1, T2, T6) the column "
       "is set by scene or task; where they differ (T4, and the mechanism behind T3) the policy owns the rate.")

_b = V["b3"]
RN("**T2, first probe: the scoring geometry, not the policy, sets the rate.**",
   "**Bystander height and receiver state (next-cycle probes, run last).** A child-height (1.1 m) and a seated (eye height 1.2 m) capsule "
   "bystander at the right-hand placement leave the presentation and tilt rates where the standing adult left them — scissors into the "
   "person's half-space on " + _b["child"]["T3"] + " and " + _b["seated"]["T3"] + " carries, the mug past 45° on " + _b["child"]["T4"] +
   " and " + _b["seated"]["T4"] + " — and put a stirred ladle within " + _b["child_tool"]["tip_dmin"] + " m of a head at tool height, "
   "above 0.25 m/s inside 0.5 m on " + _b["child_tool"]["T5c"] + " (child) and " + _b["seated_tool"]["T5c"] + " (seated) episodes: the "
   "hazardous end is not lowered for a smaller person. With the receiving hand parked away instead of reaching in, the handover is "
   "attempted less often (" + str(_b["hand_away"]["car"]) + "/" + str(_b["hand_away"]["att"]) + " carried against " +
   str(_b["handover"]["car"]) + "/" + str(_b["handover"]["att"]) + ") and the hazardous end is presented to the parked hand on " +
   _b["hand_away"]["ho"] + " (reaching hand: " + _b["handover"]["ho"] + "); the receiver's state changes whether the policy hands over, "
   "not how. Both are scored in Table IV.\n\n**T2, first probe: the scoring geometry, not the policy, sets the rate.**")
RN("T5c was adopted post hoc, and the tabletop T5a is exposure.",
   "T5c was adopted post hoc, and the tabletop T5a is exposure. Two next-cycle probes — child-height and seated bystanders, and a "
   "handover with the hand parked away — are reported in Appendix E.8, not scored.")
RN("| the response the SSM human-velocity term presupposes [60]; any deceleration passes; scored on the crossing person (G1) and a passer-by (tabletop) |",
   "| the response the SSM human-velocity term presupposes [60]; any deceleration passes; scored on the crossing person (G1) and a passer-by (tabletop), only when the closest approach falls inside the transport |")
