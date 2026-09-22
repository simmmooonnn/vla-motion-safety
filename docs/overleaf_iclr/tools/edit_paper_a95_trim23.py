# -*- coding: utf-8 -*-
# Page budget, decisive: §5.5's control paragraph keeps what it licenses and what it cannot; the matched-cell numbers and the
# attachment's mechanics move to Appendix E.8. Exec'd after a94 (uses t, RN, V).
_m = V.get("matched", {})
_long = ("**A scripted straight-line carry as the control.** A scripted carrier reads the payload and bowl poses from the "
         "simulator, ignores the person and carries on a straight line at " + V["ik_v_trans"] + " m/s (" + V["ik_carried"] +
         " carries; last row of Table III). Its arm is inverse-kinematics-driven, but its payload is held kinematically, not "
         "grasped: the object's pose is written to the simulator each step, at the tool centre and at its spawn orientation "
         "(Appendix C). It therefore witnesses geometry only: its T4 and T6 cells are properties of the attachment and carry no "
         "attribution, and on the " + _m.get("n_cells", "14") + " cells it shares with π0.5 it scores T2 " + _m.get("ik_T2", "3/208") +
         " against " + _m.get("pi_T2", "2/205") + " (the column is set by the workspace) and T3 " + _m.get("ik_T3", "46/112") +
         " against " + _m.get("pi_T3", "32/75") + " (orientation separates neither). The blade-away variant of the same carrier "
         "delivers " + V.get("ik_t3w", {}).get("R", {}).get("ok_done", "14") + " of its carries with the tip out of the person's "
         "half-space (§5.2), which is the witness that matters: a compliant direction exists on these paths and no policy takes it.")
_short = ("**A scripted straight-line carry as the control.** A scripted carrier reads the poses from the simulator, ignores the "
          "person and carries on a straight line (" + V["ik_carried"] + " carries; last row of Table III). Its arm is "
          "inverse-kinematics-driven, but its payload is held kinematically rather than grasped, so it witnesses geometry only: "
          "the cells it shares with π0.5 agree on the body sweep and do not separate on orientation, its tilt and contact cells "
          "are properties of the attachment, and its off-path keep-out result is the trajectory witness of §5.1 (Appendix E.8).")
_extra = ("**What the scripted control licenses.** Its arm is driven by inverse kinematics like any other, but the payload is "
          "held by a kinematic attachment: during the carry the object's pose is written to the simulator each step, at the tool "
          "centre and at its spawn orientation (Appendix C). It cannot tilt and cannot be deflected, so its T4 and T6 cells are "
          "properties of the attachment and carry no attribution. What it does establish: on the " + _m.get("n_cells", "14") +
          " cells it shares with π0.5 it scores T2 " + _m.get("ik_T2", "3/208") + " against " + _m.get("pi_T2", "2/205") +
          ", so that column is set by the workspace, and T3 " + _m.get("ik_T3", "46/112") + " against " + _m.get("pi_T3", "32/75") +
          ", so orientation separates neither; the blade-away variant delivers " +
          V.get("ik_t3w", {}).get("R", {}).get("ok_done", "14") + " carries with the tip out of the person's half-space, so a "
          "compliant direction exists and no policy takes it; and on the off-path keep-out it violates " +
          V.get("t1_off_ctrl", {}).get("d28", {}).get("rate", "0/32") + " where π0.5 violates " +
          V.get("t1_off", {}).get("d28", {}).get("rate", "12/32") + ".\n\n")
if _long in t:
    t = t.replace(_long, _short)
    _a = "**A keep-out off the path (trajectory with headroom).**"
    _j = t.find(_a)
    if _j >= 0:
        t = t[:_j] + _extra + t[_j:]
