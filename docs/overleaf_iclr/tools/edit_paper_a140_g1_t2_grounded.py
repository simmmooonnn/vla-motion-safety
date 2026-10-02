# -*- coding: utf-8 -*-
# G1 T2 rerun with the scorer's 3-D body standing on the floor (g1r2, 2026-10-02). The B8 cells scored a body whose axis ran
# z 0.17-1.07 with a head at 1.28 while the G1 stands on a floor at -0.79, so only arms and shoulders could reach it. Same four
# positions, seed and episode count with a 1.74 m adult on the floor (axis -0.635..0.505, head 0.825 r 0.12). analyze_b8 on
# link_t4_3d_gr_*: within 0.10 m 27/32 (pickR 8/8, pickL 4/8, binR 8/8, binL 7/8); contact (0 m) 19/32 (8, 2, 7, 2); pooled
# within r = 0.05 / 0.10 / 0.15 / 0.20 m: 72 / 84 / 100 / 100 %. Exec'd after a139 (uses t, _rn2).
_rn2("a robot link comes within 0.10 m of the body surface on 26/32 episodes and touches it on 9/32 — the right hand at the "
     "right-pick position, the turning shoulder at the left —",
     "a robot link comes within 0.10 m of the body surface on 27/32 episodes and touches it on 19/32 — the hands at the right pick "
     "and the drop, the shoulder at the left —")
_rn2("the humanoid's body comes within 0.10 m of a bystander on 81 % of episodes",
     "the humanoid's body comes within 0.10 m of a bystander on 84 % of episodes")
_rn2("the humanoid sweeps its body into bystanders on 81 % of episodes", "the humanoid sweeps its body into bystanders on 84 % of episodes")
_rn2("under the 3-D body-surface metric at all four positions 26/32 episodes come within 0.10 m of the body and 9/32 touch it (§5.1).",
     "under the 3-D body-surface metric at all four positions 27/32 episodes come within 0.10 m of the body and 19/32 touch it (§5.1).")
_rn2("Run at all four positions (2026-09), the 3-D metric finds a link within 0.10 m of the body surface on 26/32 episodes — "
     "pick-right 8/8, pick-left 8/8 (the right shoulder and palm, the person standing 0.45 m to the robot's left-rear), bin-right "
     "4/8 (the left hand at the drop), bin-left 6/8 (the right hand) — and touching it on 9/32 (pick-right 8, pick-left 1); the "
     "pooled fraction within $r$ of the surface is 50 / 81 / 94 / 100 % at $r$ = 0.05 / 0.10 / 0.15 / 0.20 m",
     "Run at all four positions with the body standing on the floor (rerun 2026-10-02; the September cells scored a body raised "
     "0.8 m, which only the arms and shoulders could reach), the 3-D metric finds a link within 0.10 m of the body surface on "
     "27/32 episodes — pick-right 8/8, pick-left 4/8 (the right shoulder and elbow, the person standing 0.45 m to the robot's "
     "left-rear), bin-right 8/8 (the left hand at the drop), bin-left 7/8 (the right hand) — and touching it on 19/32 (pick-right "
     "8, pick-left 2, bin-right 7, bin-left 2); the pooled fraction within $r$ of the surface is 72 / 84 / 100 / 100 % at $r$ = "
     "0.05 / 0.10 / 0.15 / 0.20 m")
_rn2("| pick left (2026-09) | 8 | (all) | 8 / 8 | 100 % [68, 100] | contact (0 mm): 1 / 8 |\n"
     "| bin right (2026-09) | 8 | (all) | 4 / 8 | 50 % [22, 78] | contact (0 mm): 0 / 8 |\n"
     "| bin left (2026-09) | 8 | (all) | 6 / 8 | 75 % [41, 93] | contact (0 mm): 0 / 8 |\n"
     "| pooled four positions | 32 | (all) | 26 / 32 | 81 % [65, 91] | contact (0 mm): 9 / 32 |",
     "| pick left (body on the floor, 2026-10) | 8 | (all) | 4 / 8 | 50 % [22, 78] | contact (0 mm): 2 / 8 |\n"
     "| bin right (body on the floor, 2026-10) | 8 | (all) | 8 / 8 | 100 % [68, 100] | contact (0 mm): 7 / 8 |\n"
     "| bin left (body on the floor, 2026-10) | 8 | (all) | 7 / 8 | 88 % [53, 98] | contact (0 mm): 2 / 8 |\n"
     "| pooled four positions | 32 | (all) | 27 / 32 | 84 % [68, 93] | contact (0 mm): 19 / 32 |")
_rn2("| pick right | 8 | (all) | 8 / 8 | 100 % [68, 100] | contact (0 mm): 8 / 8 |\n| pick left (body",
     "| pick right (body on the floor, 2026-10) | 8 | (all) | 8 / 8 | 100 % [68, 100] | contact (0 mm): 8 / 8 |\n| pick left (body")
_rn2("and GR00T's hand or shoulder on 9/32 over four positions (§5.1)", "and GR00T's hand or shoulder on 19/32 over four positions (§5.1)")
_rn2("gives 26/32 within 0.10 m of the surface and 9/32 at contact — 81 % against π0.5's 53 % at the matched geometry.)",
     "gives 27/32 within 0.10 m of the surface and 19/32 at contact — 84 % against π0.5's 53 % at the matched geometry.)")
_rn2("sweeps into a bystander on 26/32 episodes; this sub-type's difficulty is set by the embodiment.",
     "sweeps into a bystander on 27/32 episodes; this sub-type's difficulty is set by the embodiment.")
