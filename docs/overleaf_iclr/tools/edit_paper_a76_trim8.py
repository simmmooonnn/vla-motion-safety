# -*- coding: utf-8 -*-
# Page budget after the round-3 disclosures: the control paragraph, the T4 retraction and the withdrawing-hand sentence
# tightened; the hand sentence is in the appendix, so only the first two pay for main-text lines. Exec'd after a75.
_m = V.get("matched", {})
RN("A scripted carrier reads the payload and bowl poses from the simulator, ignores the person and carries on a straight line at " +
   V["ik_v_trans"] + " m/s (" + V["ik_carried"] + " carries; last row of Table III). Its arm is inverse-kinematics-driven like "
   "any other, but its *payload* is held by a kinematic attachment rather than a closed grasp: during the carry the object's "
   "pose is written to the simulator each step, at the tool centre and at its spawn orientation (Appendix C). That bounds what "
   "the control can witness. It can witness geometry: the arm's own sweep, and whether a direct path admits a compliant "
   "payload direction. It cannot witness what a physical grasp would do to an object's attitude, and it cannot be deflected by "
   "contact — so its T4 and T6 cells are properties of the attachment, and we draw no attribution from them. What it does "
   "establish, on the " + _m.get("n_cells", "four") + " cells it shares with π0.5: T2 " + _m.get("ik_T2", "2/64") + " against "
   "π0.5's " + _m.get("pi_T2", "1/64") + " — a fixed arm working inside the table's footprint sweeps the same way whether or "
   "not it looks at the person, so that column is set by the workspace; and T3 " + _m.get("ik_T3", "16/32") + " against " +
   _m.get("pi_T3", "11/20") + ", statistically indistinguishable, so the orientation column separates neither.",
   "A scripted carrier reads the payload and bowl poses from the simulator, ignores the person and carries on a straight line "
   "at " + V["ik_v_trans"] + " m/s (" + V["ik_carried"] + " carries; last row of Table III). Its arm is inverse-kinematics-driven, "
   "but its payload is held kinematically, not grasped: the object's pose is written to the simulator each step, at the tool "
   "centre and at its spawn orientation (Appendix C). It therefore witnesses geometry only — the arm's sweep, and whether a "
   "path admits a compliant payload direction — while its T4 and T6 cells are properties of the attachment and carry no "
   "attribution. On the " + _m.get("n_cells", "four") + " cells it shares with π0.5 it scores T2 " + _m.get("ik_T2", "2/64") +
   " against " + _m.get("pi_T2", "1/64") + ", so that column is set by the workspace, and T3 " + _m.get("ik_T3", "16/32") +
   " against " + _m.get("pi_T3", "11/20") + ", indistinguishable, so orientation separates neither.")
RN("**T4.** The tabletop tilt has no control witness: the scripted carrier's payload is pinned upright by its attachment, so "
   "its " + V["ik_T4_pct"] + " % is that attachment's residual, not evidence that a grasped mug can be carried level (on the "
   "shared cells, " + _m.get("ik_T4", "5/32") + " against π0.5's " + _m.get("pi_T4", "19/31") + "). Whether a closed grasp on "
   "this arm could hold a mug upright along the same path is open, and we mark T4 unattributed until a grasping control "
   "answers it.",
   "**T4.** The tabletop tilt has no witness: the control's payload is pinned upright by its attachment, so its " +
   V["ik_T4_pct"] + " % is that pinning's residual, not a level carry. T4 is reported unattributed.")
