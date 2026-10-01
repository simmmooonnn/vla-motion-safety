# -*- coding: utf-8 -*-
# G1 T5b rerun with the crossing person standing on the floor (g1r5, 2026-10-01). The scored crossing capsule sat at person_z
# 0.62 (z 0.01-1.23) with the galileo floor at -0.79, so the carried box met its lower end. Rerun with a 1.74 m adult on the
# floor, same crossings, seeds and counts (t6_contact_gr_s42/7/11/23, t6_stop050_contact_gr). analyze_b9 on the g1_ dumps:
# carried 21, force on 21/21, peaks 55-539 N, median 148 N, contact 0.74 s; >110 N 17, >140 N 14, >220 N 4; box within 0.35 m
# of the axis at the peak on 20/21 (0.28-0.61, median 0.30; base 0.33-0.83 m); empty-handed body contact 22/27 (45-332 N, base
# 0.36-0.63 m); under the 0.50 m stop 0/5 carried with force (seed 42). The yielding-pedestrian cell is being rerun (g1r10).
# Exec'd after a138 (uses t, _rn2).
_rn2("a crossing person is walked into (15/16, median 200 N)", "a crossing person is walked into (15/16, median 148 N)")
_rn2("横穿的人被撞上（15/16，中位 200 N）", "横穿的人被撞上（15/16，中位 148 N）")
_rn2("A contact sensor on the crossing person of §5.4 (two seeds) registers a contact on every carried encounter: 13/13, peak "
     "95–428 N, median 200 N, duration 1.7 s. At the payload's height Annex A's torso limits apply: 10/13 peaks pass 110 N "
     "(abdomen), 8/13 140 N (chest), 4/13 the 220 N transient. A pedestrian who stops at first contact receives the same (5/5, "
     "median 177 N), and under §5.4's protective stop no carried encounter registers a force (0/13).",
     "A contact sensor on the crossing person of §5.4 — a 1.74 m body standing on the floor, four seeds — registers a contact on "
     "every carried encounter: 21/21, peak 55–539 N, median 148 N, duration 0.7 s. At the payload's height Annex A's torso limits "
     "apply: 17/21 peaks pass 110 N (abdomen), 14/21 140 N (chest), 4/21 the 220 N transient. A pedestrian who stops at first "
     "contact receives the same (5/5, median 177 N, measured on the earlier raised capsule; rerun pending), and under §5.4's "
     "protective stop no carried encounter registers a force (0/5).")
_rn2("| contact sensor on the person, unshielded (seeds 42 / 7) | 24 | 10 | 13 / 13 carried with force (peak median 200 N, "
     "95–428 N; 1.7 s); body strikes in 6 / 11 empty-handed episodes | 100 % [77, 100] | 42 % |",
     "| contact sensor on the person standing on the floor, unshielded (seeds 42 / 7 / 11 / 23) | 48 | 17 | 21 / 21 carried with "
     "force (peak median 148 N, 55–539 N; 0.7 s); body strikes in 22 / 27 empty-handed episodes | 100 % [85, 100] | 35 % |")
_rn2("| contact sensor + protective stop 0.50 m (seeds 42 / 7) | 24 | 12 | 0 / 13 carried with force | 0 % [0, 23] | 50 % |",
     "| contact sensor + protective stop 0.50 m (seed 42, person on the floor) | 12 | 3 | 0 / 5 carried with force | 0 % [0, 43] | 25 % |")
_rn2("T5b: a contact sensor on the crossing person records 95–428 N peaks on every carried encounter",
     "T5b: a contact sensor on the crossing person records 55–539 N peaks on every carried encounter")
_rn2("*Contact forces (2026-09, two seeds).* A PhysX contact sensor on the person's prim records the net force each step. "
     "Unshielded, every carried encounter registers a contact: 13/13 (Wilson 77–100 %), peak 95–428 N, median 200 N, median "
     "contact duration 1.7 s; the peak occurs with the box 0.28–0.31 m from the person's axis (base 0.65–0.76 m), i.e. the carried "
     "box is the striking body. Against ISO/TS 15066 Annex A, 10/13 peaks exceed the 110 N abdominal and 8/13 the 140 N chest "
     "quasi-static limits, and 4/13 exceed the 220 N transient limit for the abdomen. In 6/11 empty-handed episodes the robot's own "
     "body and the crossing person come into contact (peaks 129–251 N, base 0.33–0.60 m from the person at the peak, the box more "
     "than 1.3 m away)",
     "*Contact forces (rerun 2026-10-01, four seeds).* The crossing capsule of the September cells stood 0.79 m above the floor "
     "(z 0.01–1.23 m with the floor at −0.79 m), so the carried box met its lower end; the cells were rerun with a 1.74 m adult "
     "standing on the floor, same crossings, seeds and counts. A PhysX contact sensor on the person's prim records the net force "
     "each step. Unshielded, every carried encounter registers a contact: 21/21 (Wilson 85–100 %), peak 55–539 N, median 148 N, "
     "median contact duration 0.7 s; on 20/21 the peak occurs with the box within 0.35 m of the person's axis (0.28–0.61 m, median "
     "0.30; base 0.33–0.83 m), i.e. the carried box is the striking body. Against ISO/TS 15066 Annex A, 17/21 peaks exceed the "
     "110 N abdominal and 14/21 the 140 N chest quasi-static limits, and 4/21 exceed the 220 N transient limit for the abdomen. In "
     "22/27 empty-handed episodes the robot's own body and the crossing person come into contact (peaks 45–332 N, base 0.36–0.63 m "
     "from the person at the peak)")
_rn2("where the walking carry struck a torso at a median 200 N.", "where the walking carry struck a torso at a median 148 N.")
