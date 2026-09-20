# -*- coding: utf-8 -*-
# Review round 3, C1 + C3: disclose the control's magic attach, retract the T4 inference it cannot support, and state every
# cross-row comparison over the cells the rows share. Exec'd after a73 (uses t, RN, V).
_m = V.get("matched", {})
RN("**A scripted straight-line carry as the control.** A scripted carrier that reads the payload and bowl poses from the "
   "simulator, ignores the person and carries on a straight line at " + V["ik_v_trans"] + " m/s (" + V["ik_carried"] +
   " carries; last row of Table III) scores T1 " + V["ik_T1_pct"] + " % and T2 " + V["ik_T2_pct"] + " %, as the policies do: "
   "the marker lies on every direct path and the sweep is set by the geometry. Its T3 splits " + V["ik_T3_R"] + " right against " +
   V["ik_T3_L"] + " left — π0.5's " + V["pi_T3_R"] + " and " + V["pi_T3_L"] + " are the signature of a carry yaw that never "
   "responds to the person. It scores T4 " + V["ik_T4_pct"] + " % where π0.5 scores " + V["pi_T4_pct"] + " %: a level carry "
   "exists, so the tabletop T4 is the policy's. It reaches the hand on " + V["ik_T6"] + ": that cell measures exposure. "
   "Where control and policies agree (T1, T2, T6) the column is set by scene or task; where they differ (T4; the mechanism "
   "behind T3) the policy owns the rate.",
   "**A scripted straight-line carry as the control.** A scripted carrier reads the payload and bowl poses from the simulator, "
   "ignores the person and carries on a straight line at " + V["ik_v_trans"] + " m/s (" + V["ik_carried"] + " carries; last row "
   "of Table III). Its arm is inverse-kinematics-driven like any other, but its *payload* is held by a kinematic attachment "
   "rather than a closed grasp: during the carry the object's pose is written to the simulator each step, at the tool centre and "
   "at its spawn orientation (Appendix C). That bounds what the control can witness. It can witness geometry: the arm's own "
   "sweep, and whether a direct path admits a compliant payload direction. It cannot witness what a physical grasp would do to "
   "an object's attitude, and it cannot be deflected by contact — so its T4 and T6 cells are properties of the attachment, and "
   "we draw no attribution from them. What it does establish, on the " + _m.get("n_cells", "four") + " cells it shares with "
   "π0.5: T2 " + _m.get("ik_T2", "2/64") + " against π0.5's " + _m.get("pi_T2", "1/64") + " — a fixed arm working inside the "
   "table's footprint sweeps the same way whether or not it looks at the person, so that column is set by the workspace; and "
   "T3 " + _m.get("ik_T3", "16/32") + " against " + _m.get("pi_T3", "11/20") + ", statistically indistinguishable, so the "
   "orientation column separates neither. The blade-away variant of the same carrier delivers " + V.get("ik_t3w", {}).get("R", {}).get("ok_done", "28") +
   " of its carries with the tip out of the person's half-space (§5.2), which is the witness that matters: a compliant "
   "direction exists on these paths and no policy takes it.")
if _m.get("pi_T4"):
    RN("**T4.** π0.5 carries a mug tilted in its grasp",
       "**T4.** The tabletop tilt has no control witness: the scripted carrier's payload is pinned upright by its attachment, "
       "so its " + V["ik_T4_pct"] + " % is that attachment's residual, not evidence that a grasped mug can be carried level "
       "(on the shared cells, " + _m.get("ik_T4", "5/32") + " against π0.5's " + _m.get("pi_T4", "19/31") + "). Whether a "
       "closed grasp on this arm could hold a mug upright along the same path is open, and we mark T4 unattributed until a "
       "grasping control answers it.\n\n**T4.** π0.5 carries a mug tilted in its grasp")
