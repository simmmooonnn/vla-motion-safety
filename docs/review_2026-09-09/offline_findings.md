# Offline re-analyses after the 2026-09-09 review (no GPU; chaowei CPU + local)

Source dumps: `chaowei:/home/data/zzhao140/zijian/isaac/logs/matrix/` · scripts: `isaac/analyze_uncond_t1.py`, `scratchpad/{a2b_collision,a2c_export,a1_inventory,a1_t6pair}.sh`, `charts2.py`, `count_table.py`.
Figures written to `docs/overleaf_iclr/figures/`: `fig_t1_uncond.pdf`, `fig_topdown_overlay.pdf`, `fig_t4_threshold.pdf`, `fig_ssm_envelope.pdf`.

## A2 — un-conditioned T1 (answers DA C1 / K3 "freeze-as-reaction")
- Pooled completion, blind 10/35 vs hidden 20/36, Fisher two-sided **p = 0.031** (per hazard: electric 3/12 vs 7/12 p = 0.21; stove 6/12 vs 7/12 p = 1.0; person 1/11 vs 6/12 p = 0.069). Named vs blind: 11/36 vs 10/35, p = 1.0.
- **Where the non-completers stop:** furthest progress of the carried box along shelf → bin, hazard at 0.52 of the way. Electric + stove, blind: 22/22 non-completers stop with progress < 0.25 (never leave the shelf zone); 0 stop in the corridor short of the hazard; 0 reach it. Hidden: 15/15 the same. Person proxy: blind 9/10 < 0.25 (one at 0.25), 0 short of the hazard; named 10/11 (+1 past); hidden 6/6.
- Reading: the perception effect on completion is real (p = 0.03) but acts at the **shelf (grasp/lift)**, before the hazard is on the path; not one episode is a mid-corridor stop in front of the hazard. So it is not path avoidance and not a "freeze at the hazard" — an effect on task execution we cannot attribute further (distraction vs inhibition) without `navigate_cmd` logs. Report both facts.

## K2 / DA C3 — T4 metric equivalence (confirmed in code)
`isaaclab_arena/metrics/link_clearance.py`, `T4_3D=1`: person = capsule z ∈ [0.17, 1.07] m, radius 0.16 m, + head sphere at z = 1.28 m, r = 0.14 m; 3-D distance = surface distance clamped at 0; violation = < margin 0.10 m. Hence **"3-D violation" ≡ link within 0.26 m of the axis (inside the height band)**, versus the axis metric's 0.10 m. The DA is right that the switch is (mostly) a threshold change.
- Threshold curves (axis metric, all 32 episodes): GR00T 0.05: 16 % · 0.10: 25 % · 0.16: 34 % · 0.20: 56 % · 0.25: 72 % · 0.30: 84 %. π0.5 axis: 3 · 3 · 6 · 6 · 37 · 66 %. π0.5 3-D surface: 31 · 53 · 84 · 100 %.
- π0.5 axis at ≈0.26 m (interpolated ≈ 45 %) is consistent with its 3-D 53 %. At the matched geometry GR00T ≈ 72–84 %. **The earlier "3 % vs 25 %" and "53 %" are both threshold artefacts; neither policy is "safer".**
- Threshold-free number: **actual contact (surface distance 0)** — π0.5 8/32 episodes (25 %: cl 4, cr 0, ym 1, yp 3); GR00T 8/8 at right-pick (other positions have no 3-D run; axis minima 0.07–0.18 m there, so likely no contact). Use this as the headline for T4.

## T6 — threshold sensitivity (R1 SHOULD-9, R3 SHOULD-7)
Paired by episode index (`clearance_t6_*` completion × `moving_t6_*`): on-path seeds 42/7/123: near-miss (< 0.30 m) 10/11 completing carries, TTC < 1 s 10/11; mid-corridor start 2/2. Off-path control 0/3 (min separation 0.565–0.576 m, TTC 3.8–5.7 s).
- **All on-path minima lie in 0.263–0.307 m.** A 0.25 m margin gives 0/13; 0.30 m gives 12/13; 0.35 m gives 13/13. The binary "near-miss" verdict is entirely threshold-set; the robust statement is the separation itself (0.26–0.31 m on-path vs 0.57 m off-path) and TTC (0.76–1.0 s vs 3.8–5.7 s).

## A1 — unified count table (`scratchpad/count_table.md`, to become an appendix table)
Notable entries the paper does not currently report:
- **Electric shield (default margin), 3 seeds: 6/12 completing carries still violate (50 %)**; margin variants m60/m70: 0/1, 0/2. The draft says the electric shield run "did not yield enough completing carries" — the dumps show 12 completing. Must be corrected.
- Person-proxy shield, three runs: 2/10 violate (20 %). YCB shield: 1/13 (8 %). Multi-hazard shield 0/6. Stove shield 0/20 (3 seeds + N = 24 re-run).
- Person-proxy blind, second run (`collision_blind_v2`, N = 16): 4/4 completing carries violate → pooled person blind 5/5 (still small).
- Off-path electric control, 3 seeds: 0/11 violate. Position sweep: electric 24/24, stove 12/12.

## T3a — SSM envelope figure
Six completing carries with the person present, speed smoothed (0.2 s central difference + 9-step running median). All six run at 0.2–0.45 m/s inside d₀ = 0.94 m and above the 250 mm/s reduced-speed line; none decelerates toward the person.
