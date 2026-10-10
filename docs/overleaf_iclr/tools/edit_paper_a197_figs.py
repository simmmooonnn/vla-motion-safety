# -*- coding: utf-8 -*-
# 2026-10-10: figure integration after the figure audit (_scratch/tmp/figaudit). Appendix only; the main text (Sections 1-9)
# is not touched. (1) One citing sentence for each new appendix figure (fig:t1bend, fig:t2sweep in Appendix C; fig:t4wording
# in E.8). (2) Appendix sentences that the regenerated figures now contradict, as the figure implementers flagged them
# (E.6 SSM at v_h = 0, the E.8 T2-threshold heading, E.7 'off-path' -> 'person-absent' control, Appendix F (iv), and the
# control row name of Tables IIIb / IIIc, which Fig. heatmap now labels 'person-blind control'). Exec'd after a196 (uses t, _rn2).
_a197 = []

# ---- (1) citing sentences for the new figures
_a197.append(_rn2(
    "packing cells stopped at the hour limit before eight episodes and are counted as run. These cells enter no pool.",
    "packing cells stopped at the hour limit before eight episodes and are counted as run. These cells enter no pool. "
    "Fig. \\ref{fig:t1bend} shows the payload paths of the four policies and both controls at one placement, and every "
    "scored carry's closest approach to the keep-out point."))
_a197.append(_rn2(
    " These cells enter no pool.\n\n**A pre-registered extension to π0 and GR00T N1.6-DROID.**",
    " Fig. \\ref{fig:t2sweep} shows every episode's closest approach of the arm to the body and where in the task each "
    "policy enters the band. These cells enter no pool.\n\n**A pre-registered extension to π0 and GR00T N1.6-DROID.**"))
_a197.append(_rn2(
    "\n\n**Table XIII. Prompt dose:",
    " Fig. \\ref{fig:t4wording} plots Tables XIII and XIIIb, tilt and delivery per phrasing, with cell-clustered "
    "intervals.\n\n**Table XIII. Prompt dose:"))

# ---- (2) appendix text the regenerated figures contradict
# E.6: the stationary-human envelope has d0 = C + Z = 0.30 m (as in Section 5.3 and the governor), not 0; Fig. ssm now draws it
_a197.append(_rn2(
    "and fails only if the human is assumed *stationary* ($v_h = 0$), which is not the case the standard's SSM mode addresses.",
    "and survives a stationary human ($v_h = 0$, $d_0 = C + Z = 0.30$ m: every carry passes within 0.30 m of the person, "
    "where the allowed speed is zero)."))
# E.8: the heading now matches Fig. t4thr's title and its own paragraph ('not their order')
_a197.append(_rn2(
    "**T2, first probe: the scoring geometry, not the policy, sets the rate.**",
    "**T2, first probe: the scoring geometry sets the rate; the policy order holds.**"))
# E.7: Table V and Fig. t6contact call the T6 control 'person-absent'
_a197.append(_rn2("In the **off-path control** (*n* = 3)", "In the **person-absent control** (*n* = 3)"))
# Appendix F (iv): Fig. overlay shows no detectable change, not tested equivalence
_a197.append(_rn2("the unchanged paths (Fig. \\ref{fig:overlay})",
                  "the overlaid paths (no detectable change; Fig. \\ref{fig:overlay})"))
# Tables IIIb / IIIc: the control row as Fig. heatmap and the text name it
_a197.append(_rn2("\n| scripted straight-line controls · Franka | ", "\n| person-blind control · Franka | "))
_a197.append(_rn2("| GR00T N1.6-DROID · Franka | scripted straight-line controls · Franka |",
                  "| GR00T N1.6-DROID · Franka | person-blind control · Franka |"))
print("a197 figs: %d/%d edits applied" % (sum(1 for x in _a197 if x), len(_a197)))
