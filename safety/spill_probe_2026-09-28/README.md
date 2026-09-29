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

## Why it does not measure (a contact-resolution boundary, not a timestep one)

The contents are dynamic: spawned in mid-air they fall, drop into the cup and are counted correctly (4 out, then 0
once they are inside). What fails is the contact behaviour of small bodies inside a thin-walled container that a
stiff actuated gripper is carrying:

* **Light contents (10 spheres, 8 mm, 3 g) are pinned.** Over 32 carries (pi0.5 and the scripted control, two seeds
  each) their largest radius in the cup's frame is 0.032 m -- the inner wall -- in *every* episode, and they never
  leave the base. One trace holds 79-100 deg of tilt for 2.3 s while descending and nothing comes out; another
  reaches 120 deg. A 3 g ball weighs 0.03 N, far less than the depenetration impulses it sees each step, so contact
  resolution, not gravity, decides where it goes.
* **Heavy contents (5 spheres, 12 mm, 50 g) are ejected.** They leave the cup, but through the wall: one sphere ends
  up on the floor 5.8 m away, sliding at a steady 0.4 m/s, in 2 of 4 episodes.

Sleeping was ruled out (`sleep_threshold=0`, `stabilization_threshold=0`, gravity set explicitly), and the physics
step is 1/120 s with decimation 8 (15 Hz control), so the step size is not the problem. Both regimes are artefacts,
so neither can score a spill.

**What would be needed:** a contents model that is not a cloud of small free bodies against a thin shell -- a particle
or deformable solver, or a single shaped "liquid" body with a tuned contact material -- plus a container with thicker
walls than a cup's. That is a scene-physics project, not a knob.

**Conclusion.** No spill claim enters the paper. Tilt remains the scored orientation predicate (T4), with the
geometric "tilts toward the person" count as its exposure measure, and this folder records exactly what a physically
simulated spill would take.
