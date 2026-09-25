# -*- coding: utf-8 -*-
# Review round 3, C2: replace the kinematic-attachment T4 pseudo-witness with a physical pinch-grasp witness.
# Exec'd after a95 (uses t, RN, V = N45).
_pg = V.get("ik_pg", {})
if _pg.get("t45", "0/0") != "0/0":
    RN("Last row: a scripted straight-line carry from privileged state, blind to the person (§5.5) — a column on which it "
       "scores like the policies is set by scene or task.",
       "Last row: scripted straight-line controls from privileged state, blind to the person (§5.5): a kinematic-attachment "
       "variant supplies the geometric columns, and a physical pinch-grasp variant supplies T4 only.")

    RN("Table III marks which rates have one; without it (T2, T3, the tabletop) the rate may be partly set by the scene.",
       "Table III marks which rates have one; without it (T2) the rate may be partly set by the scene.")

    RN("| Witness in scene | yes (G1: T1) | yes (tabletop: T3, T4, scripted carry) | yes (G1: T5a; both: T5b) | yes (both: T6) |",
       "| Witness in scene | yes (G1: T1) | yes (tabletop: T3 geometric; T4 physical pinch-grasp) | yes (G1: T5a; both: T5b) | yes (both: T6) |")

    RN("the tabletop T3 witness, and with its level carry (T4 8 %) the T4 witness (Appendix E.4, E.8).",
       "the tabletop T3 witness (Appendix E.4, E.8).")

    RN("GR00T's rigid box stays near-level in transit (0/17), its grasp and release tilts (median 55–56°) unchanged by either "
       "instruction (Appendix E.5).",
       "GR00T's rigid box stays near-level in transit (0/17), its grasp and release tilts (median 55–56°) unchanged by either "
       "instruction. A separate person-blind straight-line control disables the kinematic attachment (`SC_MAGIC=0`) and "
       "physically pinches the same mug: across " + _pg["attempted"] + " attempts it carries " + _pg["carried"] + ", completes " +
       _pg["completed"] + ", and exceeds 45° on " + _pg["t45"] + " carries (median " + _pg["tilt_median"] + "°; " +
       _pg["t27"] + " above 27°). This supplies the tabletop T4 feasibility witness, not a matched policy comparison (Appendix E.5, E.8).")

    RN("**A scripted straight-line carry as the control.** A scripted carrier reads the poses from the simulator, ignores the "
       "person and carries on a straight line (414 carries; last row of Table III). Its arm is inverse-kinematics-driven, but "
       "its payload is held kinematically rather than grasped, so it witnesses geometry only: the cells it shares with π0.5 "
       "agree on the body sweep and do not separate on orientation, its tilt and contact cells are properties of the attachment, "
       "and its off-path keep-out result is the trajectory witness of §5.1 (Appendix E.8).",
       "**Scripted straight-line controls.** The geometric variant reads simulator state, ignores the person and carries with an "
       "inverse-kinematics-driven arm and a kinematically attached payload (414 carries); it supplies the T1–T3 geometric "
       "comparisons, while its tilt and contact cells carry no attribution. For T4 only, an otherwise matched variant disables "
       "the attachment (`SC_MAGIC=0`) and physically pinches the mug: " + _pg["carried"] + "/" + _pg["attempted"] + " carries, " +
       _pg["completed"] + " deliveries, and " + _pg["t45"] + " above 45°. Its off-path result remains the T1 trajectory witness "
       "of §5.1; neither variant is a matched policy comparison (Appendix E.8).")

    RN("T2 has **no witness**; T3 has one on the tabletop (the scripted carry, whose payload is held kinematically, so it "
       "witnesses geometry only and leaves **T4 unattributed**), T1 on the G1 only.",
       "T2 has **no witness**; T3 has a geometric scripted witness on the tabletop, T4 a physical pinch-grasp witness based on " +
       _pg["carried"] + " carried episodes, and T1 a witness on the G1 only.")

    RN("the tabletop scene family (six work surfaces, a rendered adult, a reaching hand, a passer-by) is one environment with "
       "per-sub-type flags (Appendix C).",
       "the tabletop scene family (six work surfaces, a rendered adult, a reaching hand, a passer-by) is one environment with "
       "per-sub-type flags (Appendix C). The physical T4 witness uses the same straight-line controller with `SC_MAGIC=0`, "
       "five seeds (42 / 7 / 11 / 23 / 31) and " + _pg["attempted"] + " attempts; all " + _pg["carried"] + " carried episodes "
       "enter the tilt denominator.")

    RN("**What the scripted control licenses.** Its arm is driven by inverse kinematics like any other, but the payload is held "
       "by a kinematic attachment: during the carry the object's pose is written to the simulator each step, at the tool centre "
       "and at its spawn orientation (Appendix C). It cannot tilt and cannot be deflected, so its T4 and T6 cells are properties "
       "of the attachment and carry no attribution. What it does establish: on the 14 cells it shares with π0.5 it scores T2 "
       "3/208 against 2/205, so that column is set by the workspace, and T3 46/112 against 32/75, so orientation separates "
       "neither; the blade-away variant delivers 14 carries with the tip out of the person's half-space, so a compliant direction "
       "exists and no policy takes it; and on the off-path keep-out it violates 0/32 where π0.5 violates 12/32.",
       "**What the scripted controls license.** In the geometric variant the inverse-kinematics-driven arm moves normally, but "
       "the payload pose is written to the simulator at every step. That variant licenses T1–T3 only: on the 14 cells it shares "
       "with π0.5 it scores T2 3/208 against 2/205 and T3 46/112 against 32/75; its blade-away variant supplies the compliant "
       "T3 direction, and it clears the 0.28 m off-path keep-out 0/32 where π0.5 enters it 12/32. Its T4 and T6 cells remain "
       "attachment properties. The physical pinch-grasp variant instead sets `SC_MAGIC=0` and applies tool-centre force while "
       "following the same straight line. Over " + _pg["attempted"] + " attempts it carries " + _pg["carried"] + " times and "
       "delivers " + _pg["completed"] + "; tilt exceeds 45° on " + _pg["t45"] + ", 27° on " + _pg["t27"] + " and 14° on " +
       _pg["t14"] + " (median " + _pg["tilt_median"] + "°, maximum " + _pg["tilt_max"] + "°). The " + _pg["t45"] +
       " carry supplies the T4 feasibility witness; the experiment is not a matched policy comparison.")

    RN("and none yet for T4 — a scripted upright carry would make its T4 rate attributable; T2 has no witness",
       "and a physical pinch-grasp witness for T4 (`SC_MAGIC=0`; " + _pg["t45"] + " carries exceed 45°); T2 has no witness")
