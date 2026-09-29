# Spill as a physically scored event: what was built, and why it does not measure (2026-09-28)

Goal (compute queue C3): score a *spill* directly, rather than inferring it from the payload's tilt — carry an open
container of loose contents past the bystander and count what leaves it, with the blind level carry as the witness.

## Built (all of it still in the tree, inert unless `SPILL_N` is set)

* `cup_hollow.usda` — an authored open cup: a base disc plus twelve wall segments, every one of them real collision
  geometry. It exists because the YCB mug's collider is a **solid convex hull**: spheres placed in the mug are in
  permanent penetration, their coordinates in the mug's frame never change, and nothing can ever leave it.
* `PICK_USD` / `PICK_USD_NAME` / `PICK_MASS` in `franka_safety_table_environment.py` — carry an authored asset
  instead of a library one.
* `SPILL_N` / `SPILL_R` / `SPILL_Z0` / `SPILL_MASS` — n small rigid spheres spawned inside the carried container.
* `SPILL_HOLD=1` — the success termination is replaced by a never-true term, so the episode keeps running after the
  place and the contents have time to fall.
* Scoring in `person_clearance.py`: each step, every sphere is transformed into the **container's own frame** and
  counted as out when it leaves the interior cylinder (`SPILL_RCUP`, `SPILL_ZHI`, `SPILL_ZLO`). A world-distance test
  does not work: a tipped cup holds its contents within 5 cm of its own centre right up to the rim. The dump gains
  `spill_out` (count per step), `spill_dmin` (closest sphere to the bystander), `spill_rmax` / `spill_zmax`.
* Queues `sp0`–`sp7` in `run_frq.sh`.

## Why it does not measure (the engine boundary)

Over 32 carries (π0.5 and the scripted control, two seeds each, 10 spheres per cup) the contents' largest radius in
the cup's frame is **0.032 m in every single episode** — the wall — and their height in that frame never leaves the
base, at tilts of 60°, 78°, 96°, 120° and even 152° (the cup fully inverted). One sphere registered as out in 1 of 32
carries. Sleeping was ruled out (`sleep_threshold=0`, `stabilization_threshold=0`, gravity explicit): the pattern is
unchanged.

The cause is the timestep, not the asset. The DROID environment steps at 1/15 s. Between two steps the grasped cup
rotates far more than an 8 mm, 3 g sphere falls (≈2 mm), so contact depenetration against the moving wall dominates
gravity and the contents are effectively dragged with the container. A faithful liquid proxy needs a much finer
physics step, which would slow every cell in the benchmark.

**Conclusion.** No spill claim enters the paper. Tilt remains the scored orientation predicate (T4), with the
geometric "tilts toward the person" count as its exposure measure, and this folder records what a physically
simulated spill would take.
