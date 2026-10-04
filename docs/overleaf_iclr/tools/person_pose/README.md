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
