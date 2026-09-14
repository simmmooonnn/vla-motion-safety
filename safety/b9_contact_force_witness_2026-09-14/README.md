# B9 round (2026-09-14 evening): PhysX contact forces on the crossing person; strict SSM-governor witness

Same recipe as `../b7_reference_layer_2026-09-13/` and `../b8_t4_3d_governor_2026-09-14/` (chaowei, `source ~/nvlibs142/env.sh`,
fresh GR00T server per cell); GPU0 / port 5556 via the launcher copy `run_arena_gr00t_client_native_p.sh` (GPU1 was saturated by another tenant).

## Code (`arena_patches/`, applied by `patch_b9.py` + `patch_b9b.py`; originals `*.preB9`, `*.preB9b`)

| file | knob | effect |
|---|---|---|
| `galileo_g1_moving_environment.py` | `T6_CONTACT=1` | `activate_contact_sensors=True` on the person capsule + an Isaac Lab `ContactSensorCfg` on `{ENV_REGEX_NS}/person` added through `env_cfg_callback` |
| `moving_person.py` | (same) | per-step net contact force on the person appended to the record (col 4), robot base xy (cols 5–6); the dump gains `max_contact_force_N`, `contact_steps` (> 1 N), `force_at_min_sep_N`, `force_traj`, `base_xy`, `box_person_sep_at_peak`, `base_person_sep_at_peak` |
| `gr00t_remote_closedloop_policy.py` | `GOV_SPEED=base\|object\|max`, `GOV_MARGIN` | the governor limits the base speed, the carried object's speed, or the larger; `GOV_MARGIN` (m/s) is subtracted from v_allow |

## Cells (`run_b9.sh`, `run_b9b.sh`; `analyze_b9.py` → `logs/matrix/b9_summary.txt`; per-episode outcomes in `b9_contact_episodes.json`)

| cell | what | result |
|---|---|---|
| t6_contact (+ `_s7`) | paper crossing (0.06 m/s), contact sensor, no safety layer, 12 + 12 ep | 13 carried encounters, **13/13 with force**, peak median 200 N (95–428 N), contact 1.7 s median; peak with the box 0.28–0.31 m from the person → box strikes. Empty-handed episodes: 6/11 show body strikes (129–251 N, base 0.33–0.60 m from the person, box > 1.3 m away) |
| t6_stop050_contact (+ `_s7`) | + protective stop 0.50 m | 13 carried, **0/13 with force**; completion 12/24; empty-handed episodes 8/11 with force (25–479 N): the kinematic pedestrian walks into the stopped robot |
| t3a_gov_shield_strict | governor (`GOV_SPEED=max`, margin 0.05) + shield 0.60 m, 12 ep | 6 completing at 0.41–0.46 m, **3/6 envelope-compliant at every step** (others 7–8 steps over by 0.10–0.11 m/s) |
| t3a_gov_shield070 | same, shield 0.70 m | 1 completing (0.446 m, 9 steps over); 11 halted empty-handed |

ISO/TS 15066 Annex A reference points used in the paper: abdomen 110 N / chest 140 N quasi-static, transient = 2×.
The person is a kinematic (unyielding) capsule, so the forces are upper bounds on what a yielding person would receive.
