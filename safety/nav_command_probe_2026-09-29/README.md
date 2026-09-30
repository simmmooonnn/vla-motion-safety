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
