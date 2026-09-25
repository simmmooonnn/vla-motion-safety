# Compute queue after review round 3 (2026-09-26)

Ordered by value per GPU-hour. Status is updated as queues land. All cells run on chaowei via `run_frq.sh`; results regenerate
through `_scratch/rebuild_a45.sh pull`. GPU 1 belongs to another user's job; GPU 2 carries other users' memory (use ≤ 1 Isaac there).

## A. No new scene code (each ≤ 1 GPU-day)

| # | Experiment | What it builds | Claim it supports | Status |
|---|---|---|---|---|
| A5 | Second seed of the crossed surface × map design (Table IVd) | none; re-run seed 7 | turns the surface/map main effect from a one-seed hypothesis into a testable one (review B5) | queued p68 |
| A3 | A "hurry" instruction on the canonical cells and the tool cells | instruction text only | whether a command can push the speed near a person *up* — the reverse of the "slowly" ablation | queued p69 |
| A1 | A bystander's forearm on the table as the off-path keep-out target (0.20 / 0.28 m from the transport line) | `T4_SEG` forearm already exists; analyzer gate `_t1a` | unifies the tabletop T1 (marker) with the G1 T1 (a person is the keep-out); tests whether the attraction holds for a body part | queued p70 |
| A6 | GR00T-DROID on the off-path keep-out | none | third row on the discriminating trajectory cell (low yield: it rarely carries) | after A1 |
| A4 | Two hazards near one path | env: second marker (HAZ2) | dose in the number of hazards | after A2 |

## B. Environment code first (1–3 days engineering)

| # | Experiment | Status |
|---|---|---|
| A2 | Cue-bearing walker: a gesture 1 s before the person moves; predicate = speed change inside the cue window (review D4) | engineering while A-queues run |
| B1 | Annex A contact model for T5b: spring-mounted hand or A.3.3 energy post-processing, 0.5 s transient boundary (review D2) | not started |
| B2 | Pinch hazard: hand in a drawer / door gap (review D3) — blocked by the drawer task being a capability boundary | not started |
| B3 | Surface-push witness (Codex `an` toppled the mug): inspect contact location before touching the controller | Codex's lane |
| B4 | Full stow after the 10 s physical grasp (Codex `ao`/`ap`) | Codex's lane |

## C. Large builds (days)

| # | Item |
|---|---|
| C1 | Rebuild the G1 corridor family on chaowei (ARCH is gone): fills the G1 T5a blank, enables walking-speed approach on the humanoid |
| C2 | A third policy family (e.g. OpenVLA-OFT) so "recurs across policies" spans three architectures |
| C3 | Scald / drop as scored events (liquid or deformable assets) |
| C4 | A person with attention and intent (another paper) |
