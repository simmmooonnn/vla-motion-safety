# Character poses for the rendered people (offline, no simulator)

Run with the Arena venv's python on chaowei (`pxr` only). All scripts read the tucked base pose
`person_posed_tuck26.usda` of the F_Business_02 character and write a `.usda` with one SkelAnimation sample.

- `pose_probe.py` — skeleton helper (joint paths, forward kinematics, local-axis rotations).
- `pose_solve.py <reach_d> <wrist_h> <out>` — leaning reach, right wrist at a target (the reaching-hand coworker;
  final: 0.56 m, 0.886 m -> `person_reach_far*.usda`, run with `REACH_OFF=0.470,-0.135`).
- `pose_solve_h.py <reach_d> <wrist_h> <out>` — the same with the hand level and the forearm within `LEVEL_TOL` of level
  (the crossing-hand coworker; final: `LEVEL_TOL=0.08`, 0.45 m, 0.86 m -> `person_cross*.usda`, bend 61 deg, forearm at the
  capsule axis where it crosses the line; run with `REACH_OFF=0.364,-0.130` and the transport line at x 0.64).
- `hang_arm2.py <in> <out> [zmin]` — lets the free (left) arm hang with the fingertips above the table top.

The `_rigid.usda` wrapper is the posed file's reference copied from `person_reach_far_hang2_rigid.usda` with the file name
replaced (sed).

**Final crossing coworker (reel v3, 2026-10-05):** `pose_solve_p.py 0.33 0.897` with `HAND_ZMIN=0.76` -> `person_crossp.usda`
(the forearm point 0.085 m behind the wrist passes through the capsule centre 0.33 m in front of the root; 49 deg lean; head
0.62 m above the table top; the free arm keeps the tucked pose and swings behind her). Run with `REACH_OFF=0.330,-0.146`,
the transport line at x 0.70 (root 1.03, outside the table edge). The level-forearm solve (`pose_solve_h.py`) needed a 61 deg
lean that put her head over the robot's workspace, and any hanging free arm landed in the bowl or the table.

`body_clear.py <mpfull.jsonl>...` — the payload and the gripper against the rendered coworker's head, torso and arms per step
(the character does not collide; only the capsule does). Episodes differ from run to run even with one seed: render several
and keep those whose head / torso / upper-arm gaps stay positive.
