# -*- coding: utf-8 -*-
# ICLR-readiness review (wf_425459e6-f4b, items 2, 4, 5): the humanoid under the tabletop's own availability rule. Its on-path
# hazards are exposure (any completing carry crosses them) and its scored T1 is the stove 0.28 m off the path; its T5b forces act
# on a kinematic body and are exposure; its T5a is unchanged under the witness's own envelope. The T5a equivalence wording goes.
# Exec'd after a159 (uses t, _rn2, V).
_i = t.find("**T1: completing carries pass through the keep-out.** In the primary cells 10/10 completing carries violate")
_j = t.find("On the tabletop the scored T1 is", _i)
if _i > 0 and _j > _i:
    t = t[:_i] + ("**T1: completing carries pass through the keep-out.** On the humanoid the corridor's hazards stand on the carry "
                  "path, so every completing carry crosses them (121/125, each inside the proxy's contact distance) — exposure, as "
                  "the tabletop's on-path marker is; the scored G1 T1 is the stove placed 0.28 m off the path, where the rate has "
                  "headroom: 11/30 completing carries enter its 0.30 m keep-out (Table XI). A repulsion shield given the hazard's "
                  "coordinates clears the on-path hazard (8/8 → 0/8, *p* = 1.6 × 10⁻⁴, completion kept; Fig. \\ref{fig:shield}) — "
                  "the witness that a clearing path exists (E.2). ") + t[_j:]
else:
    print("  [a160 MISS] 5.1 G1 T1")
_rn2("A matched present-versus-absent design removes the trajectory confound: 0.340 ± 0.029 m/s with the person present, 0.367 ± "
     "0.006 m/s without (Welch *p* ≈ 0.06) — no modulation, and in the benign direction.",
     "A matched present-versus-absent design removes the trajectory confound: 0.340 ± 0.029 m/s with the person present, 0.367 ± "
     "0.006 m/s without (Welch *p* ≈ 0.06, six carries) — no detectable modulation; the point estimate is 7 % slower with the person.")
_rn2("A strict governor with the 0.60 m shield completes 3/6 carries inside the envelope: the scene admits a compliant carry (E.6).",
     "A strict governor with the 0.60 m shield completes 3/6 carries inside the envelope for a still person ($v_h = 0$): the scene "
     "admits a compliant carry (E.6), and scored against that same envelope the policy's count is unchanged, since every carry "
     "passes within $C + Z$ = 0.30 m of the person.")
_rn2("Its near-band speed is the same with the person there or not (0.109 vs 0.113 m/s, *p* = 0.79; Table IIIb).",
     "Its near-band speed shows no detectable change with the person there (0.109 vs 0.113 m/s, *p* = 0.79; Table IIIb).")
_rn2("At the payload's height Annex A's torso limits apply: 17/21 peaks pass 110 N (abdomen), 14/21 140 N (chest), 4/21 the 220 N "
     "transient.",
     "The person is a kinematic body, so these are solver constraint forces with no compliance behind them: an upper bound, exposure "
     "as on the tabletop, and not read against Annex A's torso limits (110–140 N at the payload's height).")
