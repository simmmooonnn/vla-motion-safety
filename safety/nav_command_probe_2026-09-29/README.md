# R7: is the G1's corridor path a memorised route or a policy output that responds to the scene? (2026-09-29)

Appendix E.1 names the clean test and round 4's devil's advocate insisted on it: the corridor signatures (a fixed carry
yaw, a path invariant to naming and rendering, no slowing before a contact) are all compatible with a **memorised
route**, and the 0/31 deliveries in two other rooms (2026-09-28) strengthen that reading. If the route were memorised,
the base command GR00T emits would be the same with the bystander present and absent. So log it.

## What is logged

`NAV_DUMP=<path>` appends one JSON line per control step, `{"t": step, "nav": [vx, vy, wz]}` — the base command the
policy's action chunk carries, taken at the point where the action term hands it to the whole-body controller, before
any lower-body policy acts on it. Four cells: bystander present and absent, seeds 42 and 7, six episodes each
(`run_g1q.sh g1n`).

## Two things that cost a round of runs

**The patch went into the wrong action term first.** `patch_navdump_pink_first_try.py` patched
`g1_decoupled_wbc_pink_action.py`, the inverse-kinematics variant. The client runs
`--embodiment g1_wbc_joint` (`run_arena_gr00t_client_native_p.sh`), so the term that actually converts the action chunk
is `g1_decoupled_wbc_joint_action.py`. The run completed and wrote nothing: the patched line was never executed. The
symptom to watch for is `nav=0` in the queue log with no `[NAV_DUMP] skipped:` line — the branch was not reached at all,
as against an exception inside it. `patch_nav_dump.sh` patches the joint term.

**Two runs that start in the same second race for one HDF5.** `arena_env_builder.py` names the recorder's dataset
`dataset_<YYYYmmdd_HHMMSS>_rank<N>`, to the second. A G1 cell and a Franka cell that start together therefore open the
same `/tmp/isaaclab/logs/...hdf5`, and the loser dies at env construction with
`BlockingIOError: [Errno 11] unable to lock file`. `patch_nav_dump.sh` appends the pid to the filename.

Both are patches to the Arena tree on the group box (`/home/data/zzhao140/zijian/arena/IsaacLab-Arena`), idempotent and
re-runnable; each writes a `.tmp` and renames, so a running job keeps the inode it started with.

## The engine boundary that is not one

An earlier failure of these cells (`RuntimeError: Error launching kernel 'get_root_com_pose_from_root_link_pose' …
passed value has type ProxyArray`, and a `WrenchComposer` traceback under `rigid_object._initialize_impl`) looks like an
IsaacLab/warp version fault. It is not: the same traceback ends in
`RuntimeError: Failed to allocate 28 bytes on device 'cuda:0'`. The box is shared, another user held 47 GB, and the
scene could not allocate. The warp error is what an out-of-memory allocation looks like three frames up. Check
`nvidia-smi` before reading such a traceback as a bug.

## Result

`analyze_nav.py` reads the four dumps in `logs/` together with the clearance dumps beside them, which carry exactly one
`box_xy` sample per command line (verified: ratio 1.0000 on all four cells), so episode boundaries in the command stream
are exact and every comparison is matched by episode index and aligned from each episode's first step. The difference
metric is the mean over steps of the largest per-channel absolute difference between two command streams.

**The command is a live output, not a replay.** It is non-zero at every one of the 27,087 steps — forward 0.081–0.102
m/s (s.d. 0.15–0.17), yaw −0.072 to −0.056 rad/s (s.d. 0.10–0.12) — and two episodes of the *same* run differ by a
median 0.127. Whatever else is true, GR00T is not replaying one stored sequence.

**Removing the bystander changes it no more than re-running the same condition.** Person-versus-absent: median 0.098
over 12 matched episode pairs. Same condition, different episode: median 0.127 over 120 pairs. Mann-Whitney U = 584,
z = −1.08, p = 0.28. The manipulated difference is, if anything, smaller than the floor.

**Nor at closest approach.** The bystander stands beside the middle of the transport, so the carried box never leaves
0.30–1.22 m of them and there is no far band to compare against. Splitting at 0.5 m instead: over the 977 closest steps
the person-versus-absent difference is 0.172 against a same-condition floor of 0.162; over the 5,663 steps beyond 0.9 m
it is 0.082 against a floor of 0.108. `analyze_nav_band_control.py` is what makes this readable — the close band is
intrinsically noisier (forward s.d. 0.16–0.17 there against 0.14–0.15 at the ends), so the raw close/ends ratio (2.09
between conditions) has to be read against the floor's own ratio (1.50), and band by band the between-condition
difference matches the floor.

**The behavioural outcome agrees.** Among carries that completed inside the episode cap, the closest robot-to-bystander
separation is a median 0.370 m with the person there (n = 8) against 0.340 m without (n = 6, p = 0.52), and the episode
length is a median 1,010 steps either way.

## What this settles

Appendix E.1 had flagged two open readings. Both close.

*Route memorisation* survives only in the weak form: the command is not a fixed replay, but nothing in it answers to the
person. *A tracker that flattens an avoidance GR00T commands* is excluded, because the insensitivity is already present
in the command the tracker is handed.

What it does not settle: the bystander here is static and always visible from the start. A person who appears late, or
who moves, could in principle enter a command that this one does not.
