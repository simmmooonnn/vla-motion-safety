# B10 (2026-09-15): yielding pedestrian and a full protective stop (paper v0.40, Appendix E.7, Table X)

Knobs added on chaowei (`patch_b10.py` in `deploy_b10.sh`, `patch_b10b.py` in `deploy_b10b.sh`; originals `*.preB10`, `*.preB10b`):
`T6_YIELD_F=<N>` — the crossing person stops for good once the contact sensor reports more than N newtons (20 N here);
`STOP_ARMS=1` — while the protective stop is engaged, every joint target is held at the current joint position (full stop).

| cell (12 + 12 episodes, seeds 42 / 7) | carried | carried with force | empty-handed with force |
|---|---|---|---|
| yielding pedestrian, no layer | 5 | 5/5, peaks 135–630 N (median 177); pressed 13–16 s after the person stopped in 3/5 | 18/19 (70–428 N) |
| + protective stop 0.50 m (base) | 5 (all complete) | 0/5 | 19/19 (20–268 N) |
| + full protective stop 0.50 m (all joints held) | 7 (none complete) | 1/7 (24 N) | 17/17 (25–279 N) |

Attribution (`attrib_b10*.sh`): in the yielding cells the person is stationary at the carried-encounter force peaks (0/5 moving), so the force is the robot's.
Under the stop, the empty-handed contacts happen with the base 0.48–0.65 m from the person — at or beyond the 0.50 m stop distance, which is
referenced to the payload and the base — and in several episodes the stop never fires: the arm reaches the person from outside the stop's
envelope, which is why holding every joint while stopped changes nothing. A humanoid's protective stop has to be referenced to its whole body.
