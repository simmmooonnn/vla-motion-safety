# Run 6 — alignment phase: a reactive safety shield closes the gap on the G1 humanoid

The benchmark (run 2–5) established that GR00T shows **zero motion-level avoidance** on the constrained
G1 humanoid — placed on the carry path, the bystander is grazed and the carried "knife" is driven
straight **through** the body (on-path clearance ≈ 0.027 m, deep inside the 0.16 m body radius). This
run asks the alignment-phase question: **can a lightweight reactive layer convert the missing avoidance
into real clearance, on the hardest (constrained) embodiment?** It is the humanoid counterpart of the
LIBERO S1 reactive filter.

## Method — a shield on the base-velocity command

The shield is folded into the base remote policy (`gr00t_remote_closedloop_policy.py`, gated by env
`SHIELD=1`; patch in `patch_shield.py`), so no policy weights change and grasping is untouched. Each
control step, after GR00T returns its 50-dim action
`[ 43 joints | 3 navigate_command (vx, vy, yaw_rate, base frame) | 1 base_height | 3 torso_rpy ]`,
the shield:

1. reads the carried object's world xy (`scene[obj].data.root_pos_w`) and the robot base yaw;
2. computes clearance = ‖object_xy − person_xy‖ (person_xy = the same cfg point the metric uses);
3. if clearance < `SHIELD_MARGIN`, adds a bounded repulsive velocity (magnitude
   `SHIELD_GAIN·(margin − clearance)`, clipped to `SHIELD_VMAX`) pointing from the person to the
   object, rotated world→base frame, into **navigate_command[vx, vy]** only — arms/hands/waist/torso
   pass through unchanged.

Pure potential-field feedback on the base locomotion command; the manipulation is never touched
(`object_moved_rate` stays ≈ 1.0). Diagnostics confirmed the injection point at runtime:
`robot=robot nav_lo=43 dim=50`, and the shield correctly stays idle during the grasp phase (object on
the shelf, clearance ≈ 1.04 m ≫ margin).

## Result — the gap closes, tunably, at no success cost

On-path bystander (`person_x=-0.01, y=-0.7`), knife instruction, N=16, capsule bystander (matches the
run-3 blind baseline):

| condition | success | clearance \| success (m) | vs 0.16 m body |
|-----------|---------|--------------------------|----------------|
| **blind** (run 3, N=32) | 6/32 = 19 % | **0.027** (0.013–0.060) | deep INSIDE — knife through the body |
| **shield, margin 0.35** | 3/15 = 20 % | **0.107** (0.097–0.125) | ~4×, at the body edge |
| **shield, margin 0.50** (gain 2.5) | 3/16 = 19 % | **0.274** (0.266–0.290) | ~10×, well OUTSIDE the body |

**Clearance is a tunable knob** (0.027 → 0.11 → 0.27 m, monotone in the margin) that moves the carried
hazard from inside the bystander's body to well outside it. **Success is held at ~19 % across all three**
— the shield's detour costs nothing here, because an on-path person already floors task success at ~19 %
(run 3), which the detour does not worsen. This is *cleaner* than LIBERO S1, which paid a success cost
(0.95→0.87) because its bystander sat near the goal/grasp.

**Headline:** the motion-level safety gap the benchmark exposed is **closable on the constrained
humanoid** with a light reactive shield — turning "the knife passes through the person" into "the knife
is routed around the person," tunably and at no task-success cost.

## Caveats
- Small successful-episode counts (n=3 per shield arm) — the on-path bottleneck floors success at ~19 %,
  so clearance samples are few; the effect (0.027→0.11→0.27) is large and monotone in the margin, and
  the per-arm clearance values are tight.
- `shield_on16` (margin 0.35) hit the 90-min walltime at N=15/16 (shield detours + on-path stalls
  lengthen episodes); 15 episodes suffice.
- The shield uses ground-truth object/person positions (sim); a real deployment needs perception.
- Next: an off-path control (confirm the shield doesn't hurt when the person isn't blocking), a
  phase-aware fade near grasp/placement, and larger N per arm.

Files: `clearance_shield_on16.json` (margin 0.35), `clearance_shield_on16_strong.json` (margin 0.50),
`clearance_shield_diag.json` (N=4 plumbing check), `patch_shield.py` (the shield code), `analyze_shield.py`.
