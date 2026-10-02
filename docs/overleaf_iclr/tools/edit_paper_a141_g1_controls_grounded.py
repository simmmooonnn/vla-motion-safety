# -*- coding: utf-8 -*-
# The remaining G1 T6/T5b controls rerun with the crossing person standing on the floor (g1r10, g1r11; 2026-10-01/02). The
# September cells used a capsule raised 0.79 m. analyze_b9 / analyze_b7 on the g1_*_gr dumps:
#   yielding pedestrian (stops at the first contact > 20 N), s42+s7: carried 9, force 9/9, peaks 50-526 N, median 244 N; pressed
#     >= 5 s by force on 1/9 (14.0 s), held within 0.32 m >= 5 s on 2/9; empty-handed contact 11/15; completed 2/24
#   protective stop 0.50 m, s42+s7: 0/12 carried with force; completed 9/24 (the stop's firing is planar and unchanged)
#   yielding + base stop: 1/11 carried with force (30 N); completed 9/24
#   yielding + whole-arm stop: 0/5 carried with force; empty-handed contact 16/19; completed 0/24
#   speed sweep 0.3/0.6/1.2 m/s x s42/s7: carried 8, contact 7/8 (6 knocked from the grasp), no deceleration before contact
#   collider off: 2 carried, no force registered
# Exec'd after a140 (uses t, _rn2).
_rn2("With the collider removed the box passes *through* the body (7/7); at 0.3–1.2 m/s the person knocks it from the grasp "
     "(16/23), never after a deceleration; one who stops at first contact is kept pressed 13–16 s (3/5). A protective stop at "
     "0.50 m prevents the contact (0/11 carried, 0/13 with force) and fires on 22/24:",
     "With the collider removed no force registers and the box carries on into the body's volume; at 0.3–1.2 m/s the person "
     "knocks it from the grasp (7/8 carried encounters reach contact), never after a deceleration; one who stops at first contact "
     "is struck on every carried encounter (9/9, median 244 N) and in one kept pressed for 14 s. A protective stop at 0.50 m "
     "prevents the contact (0/12 carried with force) and fires on 22/24:")
_rn2("A pedestrian who stops at first contact receives the same (5/5, median 177 N, measured on the earlier raised capsule; rerun "
     "pending), and under §5.4's protective stop no carried encounter registers a force (0/5).",
     "A pedestrian who stops at first contact receives as much (9/9, median 244 N), and under §5.4's protective stop no carried "
     "encounter registers a force (0/12).")
_rn2("| contact sensor + protective stop 0.50 m (seed 42, person on the floor) | 12 | 3 | 0 / 5 carried with force | 0 % [0, 43] | 25 % |",
     "| contact sensor + protective stop 0.50 m (seeds 42 / 7, person on the floor) | 24 | 9 | 0 / 12 carried with force | 0 % [0, 24] | 38 % |")
_rn2("| contact sensor, yielding pedestrian (stops at the first contact > 20 N), seeds 42 / 7 | 24 | 1 | 5 / 5 carried with force "
     "(peak median 177 N, 135–630 N); pressed 13–16 s in 3 / 5 | 100 % [57, 100] | 4 % |",
     "| contact sensor, yielding pedestrian (stops at the first contact > 20 N), seeds 42 / 7, person on the floor | 24 | 2 | 9 / 9 "
     "carried with force (peak median 244 N, 50–526 N); pressed 14 s in 1 / 9, held at contact distance ≥ 5 s in 2 / 9 | 100 % [70, 100] | 8 % |")
_rn2("| yielding pedestrian + protective stop 0.50 m (base) | 24 | 5 | 0 / 5 carried with force | 0 % [0, 43] | 21 % |",
     "| yielding pedestrian + protective stop 0.50 m (base), person on the floor | 24 | 9 | 1 / 11 carried with force (30 N) | 9 % [2, 38] | 38 % |")
_rn2("| yielding pedestrian + full protective stop 0.50 m (all joints held) | 24 | 0 | 1 / 7 carried with force (24 N); empty-handed "
     "contacts 17 / 17 | 14 % [3, 51] | 0 % |",
     "| yielding pedestrian + full protective stop 0.50 m (all joints held), person on the floor | 24 | 0 | 0 / 5 carried with force; "
     "empty-handed contacts 16 / 19 | 0 % [0, 43] | 0 % |")
_rn2("In a variant in which the person stops for good at the first contact above 20 N, the payload still reaches them on every "
     "carried encounter (5/5, peaks 135–630 N, median 177 N), the peak arriving after the person has stopped, and in 3/5 the payload "
     "stays pressed against the standing person for 13–16 s — a person who stops is treated as an obstacle. Empty-handed episodes "
     "register a contact in 18/19, the robot's base still moving at most force peaks. Under the 0.50 m stop the carried encounters "
     "stay force-free (0/5; all five complete); a full protective stop that also holds every joint while engaged leaves the "
     "empty-handed contacts in place (17/17, 25–279 N) and completes no carried episode (0/7),",
     "In a variant in which the person stops for good at the first contact above 20 N (rerun with the person standing on the floor, "
     "two seeds), the payload still reaches them on every carried encounter (9/9, peaks 50–526 N, median 244 N — harder than the "
     "walking person's 148 N, the peak arriving after the person has stopped), and in one the payload stays pressed against the "
     "standing person for 14 s (held at contact distance for 5 s or more in 2/9; on the raised capsule of the September cells, 3/5 "
     "for 13–16 s) — a person who stops is treated as an obstacle. Empty-handed episodes register a contact in 11/15. Under the "
     "0.50 m stop one carried encounter of 11 registers a force (30 N); a full protective stop that also holds every joint while "
     "engaged leaves the empty-handed contacts in place (16/19, 5–278 N) and completes no carried episode (0/5),")
_rn2("a protective stop at the 0.50 m SSM distance does (0/11 carried), firing on 22/24 episodes (§5.4).",
     "a protective stop at the 0.50 m SSM distance does (0/12 carried encounters with force), firing on 22/24 episodes (§5.4).")
_rn2("**(iv) A moving person is walked into, and pressed against once they stop.** No deceleration precedes contact at any crossing "
     "speed (T6), and a person who stops is treated as an obstacle, the payload pressed against them as a coworker's hand in the "
     "bowl is pressed by π0.5's mug (E.7).",
     "**(iv) A moving person is walked into, and one who stops is struck, not avoided.** No deceleration precedes contact at any "
     "crossing speed (T6), and a person who stops at the first touch is struck on every carried encounter, at a median 244 N, and "
     "can be pressed against as a coworker's hand in the bowl is pressed by π0.5's mug (E.7).")
