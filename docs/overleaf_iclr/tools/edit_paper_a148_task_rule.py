# -*- coding: utf-8 -*-
# The matrix landing (2026-10-04 review, two verifiers per question; journal wf_040e9913-86f).
# 1. Tasks and task goals. A task stays a row of Table IV; its *goal* is the instruction's goal and success condition (a task
#    is a goal under one setting of surface, bystander, placement, keep-out or mover). Table IVe prints both counts. Counted by
#    goals, every tabletop sub-type rests on pick-and-place into the bowl, and only T3/T4 add a second goal (the drawer).
#    Appendix F says so, and what the advisor's criterion still lacks.
# 2. Pool corrections (generator): moving cells out of T1-T4 (the approach cells had been scored for T3 against an
#    unrendered default point); one rendering per task variant (pre-fix child / seated cells leave T2); T1's keep-out point is
#    a marker or a bystander's resting hand; T6b's denominator gated at d0. Appendix D states them.
# 3. Section 5.1's T1 sentence names both keep-out kinds and the control's pooled count.
# Exec'd after a147 (uses t, _rn2, V).
import re as _re8

# ---------------- 5.1: T1
_rn2("On the tabletop the scored T1 is a marker 0.20 or 0.28 m *beside* the transport, offsets a direct carry clears: π0.5 "
     "enters it on " + V["pi_T1"] + " against the blind carrier's 15/64 and 0/64.",
     "On the tabletop the scored T1 is a marker or a bystander's resting hand 0.20 or 0.28 m *beside* the transport, offsets "
     "a direct carry clears: π0.5 enters it on " + V["pi_T1"] + " against the blind carrier's " + V["ik_T1"] + ".")

# ---------------- Appendix F: the coverage paragraph, by both counts
def _ive(sid):
    """{policy column: (goals, variants)} parsed from Table IVe's row for one sub-type."""
    for row in V["dimtask_rows"].split("\n"):
        c = [x.strip() for x in row.strip("|").split("|")]
        if len(c) > 3 and c[1] == sid:
            out = {}
            for nm, cell in zip(("pi", "q0", "f0", "g0", "ik"), c[3:]):
                m = _re8.match(r"(\d+) \((\d+)\)", cell)
                out[nm] = (int(m.group(1)), int(m.group(2))) if m else None
            return out
    return {}


_G = {sid: _ive(sid) for sid in ("T1", "T2", "T3", "T4", "T6", "T6b")}
_GN = V.get("goals_n_by_sub", {})
_two = [sid for sid in ("T1", "T2", "T3", "T4", "T6", "T6b")
        if sum(1 for v in _GN.get(sid, {}).get("pi", {}).values() if v >= 8) > 1]          # a second goal above the floor
_low_goals = [(sid, g_) for sid in ("T1", "T2", "T3", "T4", "T6", "T6b") for g_, v in _GN.get(sid, {}).get("pi", {}).items()
              if g_ != "pick-and-place into the bowl" and 0 < v < 8]
_GV = {"put away in a drawer": "putting away in a drawer", "pour": "pouring", "hand to the person": "handing over",
       "clear the table": "clearing the table"}


def _second(tag, sids):
    """'T3 and T4 (putting away in a drawer) and T1 and T6 (pouring)': the sub-types grouped by the extra goal they add."""
    by = {}
    for sid in sids:
        extra = [g_ for g_, v in _GN.get(sid, {}).get(tag, {}).items() if g_ != "pick-and-place into the bowl" and v >= 8]
        by.setdefault(", ".join(_GV.get(g_, g_) for g_ in extra) or "another goal", []).append(sid)
    parts = [" and ".join(v) + " (" + k + ")" for k, v in by.items()]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + ", and " + parts[-1]
_two_f0 = [sid for sid in ("T1", "T2", "T3", "T4", "T6", "T6b")
           if sum(1 for v in _GN.get(sid, {}).get("f0", {}).values() if v >= 8) > 1]
_old_f = ("Table III is narrower than the suite, and the gap is now specific. Trajectory and orientation rest on several "
          "tasks: T2 on the serving family (" + V["t2sv_pi_cells"] + " cells at ")
_i = t.find(_old_f)
if _i >= 0 and _G["T3"]:
    _j = t.find("for the rest, Table IV's breadth supports the design and not the matrix.", _i)
    if _j > 0:
        _j += len("for the rest, Table IV's breadth supports the design and not the matrix.")
        _w2 = lambda xs: " and ".join(xs)
        _new = ("Table III is narrower than the suite, and the gap is now specific. A task is a row of Table IV; its *goal* is "
                "the instruction's goal and success condition, and a task is a goal under one setting of work surface, "
                "bystander, placement, keep-out or mover (Appendix D). Counted by tasks, trajectory and orientation are "
                "broad: T2 rests on the serving family (" + V["t2sv_pi_cells"] + " cells at " + _word(V["t2sv_pi_surf"])
                + " work surfaces for π0.5), T3 on " + V["t3task_pi_n"] + " tasks and T4 on " + V["t4task_pi_n"]
                + ", for π0-FAST on " + V["t3task_f0_n"] + " and " + V["t4task_f0_n"] + ", and T1 on two kinds of keep-out "
                "point. Counted by goals they are not: every tabletop sub-type rests on pick-and-place into the bowl, and "
                + (("only " + _second("pi", _two) + " add a second goal for π0.5"
                    + (", and only " + _second("f0", _two_f0) + " for π0-FAST" if _two_f0 else "")
                    + ", each on fewer carries than the first") if _two else
                   "none adds a second goal with eight or more scored episodes")
                + ("; " + " and ".join(sid for sid, g_ in _low_goals)
                   + (" reaches" if len(_low_goals) == 1 else " reach") + " a second goal ("
                   + ", ".join(_GV.get(g_, g_) for sid, g_ in _low_goals) + ") on fewer than eight scored episodes"
                   if _low_goals else "")
                + " (Table IVe). " + ("**Speed and force and dynamics rest on one goal.** " if "T6" not in _two else
                                      "**Speed and force rests on one goal.** ") + "Speed and force is "
                "scored on the humanoid corridor alone, since the tabletop cell is exposure; dynamics rests on "
                + ("two mechanisms for T6 — a hand reaching into the destination, at six work surfaces, and a hand crossing the "
                   "transport line — and one for T6b, a person walking past, at three." if V.get("hx_pi05") else
                   "one mechanism per sub-type — a hand reaching into the destination for T6, at six work surfaces, and a person "
                   "walking past for T6b, at three.")
                + " π0 and GR00T-DROID rest on one goal wherever they are scored. What the next cells must add is "
                "therefore goals other than pick-and-place — handing over, putting away, clearing the table — with the person "
                "present, not more surfaces; until then Table IV's breadth supports the design, and the matrix rests on one "
                "goal under many settings.")
        t = t[:_i] + _new + t[_j:]
    else:
        print("  [a148 MISS] Appendix F coverage paragraph end")
else:
    print("  [a148 MISS] Appendix F coverage paragraph")

# ---------------- Table IVe caption
_rn2("Every entry is *tasks / cells / episodes*: a task is a row of Table IV, a cell is one label (a placement and a seed), "
     "and an episode is one that entered that sub-type's denominator.",
     "Every entry is *goals (tasks) / cells / episodes* (a goal with fewer than eight scored episodes counts after a plus "
     "sign): a goal is the instruction's goal and success condition "
     "(pick-and-place into the bowl, put away in a drawer, hand to the person, …), a task a row of Table IV (a goal under "
     "one setting of work surface, bystander, placement, keep-out or mover), a cell one label (a placement and a seed), and "
     "an episode one that entered that sub-type's denominator.")

# ---------------- Appendix D: the definitions and the corrections
_rn2("The interaction-geometry placements are reported as their own group (E.8), as in earlier drafts. Table IVe counts what "
     "is left, per sub-type and policy.",
     "The interaction-geometry placements are reported as their own group (E.8), as in earlier drafts. Table IVe counts what "
     "is left, per sub-type and policy. A task's *goal* is the instruction's goal and success condition, the object noun "
     "aside; work surface, environment map, clutter, the bystander's body, the placement, the keep-out kind and what a "
     "moving person or hand does are factors, and a task — a row of Table IV — is a goal under one setting of them; Table "
     "IVe counts both, and a dimension rests on several goals only where Table IVe says so. Whether the person is still is read from the run, not from the cell's name: a cell that "
     "ran with a moving person or hand enters none of T1–T4 (until 2026-10-04 the approach-and-stop cells entered T3, scored "
     "against a default point at which nothing is rendered, and the withdrawing-hand cells entered T4). Each task keeps "
     "the rendering that matches the body it is scored against: the child-height and seated cells run before the render fix "
     "of 2026-09-20 showed a standing adult, so they leave T2, which reads the body, and count in T3 and T4 as the adult the "
     "policy saw; the re-rendered cells are the child-height and seated tasks. T1's keep-out point is a hot-plate marker "
     "or the hand of a bystander resting a forearm on the dining table, at the same offsets and on the same far side of the "
     "transport. T6b counts an episode only when the walker's closest approach falls inside the transport core and inside "
     "$d_0$ = 0.94 m.")
