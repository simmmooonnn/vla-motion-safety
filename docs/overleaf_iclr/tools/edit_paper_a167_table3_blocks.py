# -*- coding: utf-8 -*-
# ICLR-readiness review (item 2): Table III in two blocks -- the tabletop benchmark (a Franka arm, four public policies and the
# person-blind control) and the humanoid case study (one policy on a G1, one task family), never pooled; the generator writes
# the block titles into tab3_rows. The witness row moves into the caption (the rows of both blocks share it). Exec'd after
# a166 (uses t, _rn2, V).
_rn2("| Witness in scene | yes (G1: T1; tabletop: T2, one placement) | yes (tabletop: T3 geometric; T4 physical pinch-grasp) | "
     "yes (G1: T5a; both: T5b) | yes (both: T6) |\n", "")
_rn2("Last row: scripted straight-line controls from privileged state, blind to the person (§5.5): a kinematic-attachment variant "
     "supplies the geometric columns, and a physical pinch-grasp variant supplies T4 only. *Witness*: a compliant completion shown "
     "in the scene.",
     "The tabletop block ends with the scripted straight-line controls from privileged state, blind to the person (§5.5): a "
     "kinematic-attachment variant supplies the geometric columns, a physical pinch-grasp variant T4. Every dimension has a "
     "*witness*, a compliant completion shown in the scene: T1 (G1), T2 (tabletop, one placement), T3 and T4 (tabletop), T5a (G1), "
     "T5b and T6 (both).")
_rn2("(star: design effect > 1.5). tabletop T1 is the *off-path*", "(star: design effect > 1.5). Tabletop T1 is the *off-path*")
