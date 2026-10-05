# -*- coding: utf-8 -*-
# ICLR-readiness review (wf_425459e6-f4b, 2026-10-05): the evaluated policies and their data were never cited, and the
# related-work sweep found concurrent work (June-October 2026) the paper misses. Every entry below was checked against its
# arXiv page on 2026-10-05. Citations go where they cost the fewest words in the main text; Table I gains the overlapping
# suites and a null/witness column. Exec'd after a155 (uses t, _rn2).
_NEW_REFS = [
    (62, 'K. Black, N. Brown, D. Driess, et al., "$\pi_0$: A vision-language-action flow model for general robot control," arXiv:2410.24164, 2024.'),
    (63, 'Physical Intelligence, K. Black, et al., "$\pi_{0.5}$: A vision-language-action model with open-world generalization," arXiv:2504.16054, 2025.'),
    (64, 'K. Pertsch, K. Stachowicz, B. Ichter, et al., "FAST: Efficient action tokenization for vision-language-action models," arXiv:2501.09747, 2025.'),
    (65, 'A. Khazatsky, K. Pertsch, S. Nair, et al., "DROID: A large-scale in-the-wild robot manipulation dataset," in *Proc. Robotics: Science and Systems (RSS)*, 2024, arXiv:2403.12945.'),
    (66, 'A. Jain, M. Zhang, K. Arora, W. Chen, M. Torne, M. Z. Irshad, S. Zakharov, Y. Wang, S. Levine, C. Finn, W.-C. Ma, D. Shah, A. Gupta, and K. Pertsch, "PolaRiS: Scalable real-to-sim evaluations for generalist robot policies," arXiv:2512.16881, 2025.'),
    (67, 'Physical Intelligence, "openpi," GitHub repository, 2025. [Online]. Available: https://github.com/Physical-Intelligence/openpi'),
    (68, 'J. Luo, Q. Zhang, W. Wang, and W. Jiang, "SafeStage: Evaluating safety before, during, and after vision-language-conditioned robot manipulation," arXiv:2609.21223, 2026.'),
    (69, 'C. Liu, J. Zhang, T. Zhang, Y. Wang, H. Zhou, and Q. Jin, "HRIBench: Benchmarking interaction-centric human-robot collaboration," arXiv:2607.13056, 2026. (Concurrent work.)'),
    (70, 'B. Zhang, J. Li, J. Shen, Y. Zhang, Y. Cai, L. Liu, H. Ji, Y. Chen, J. Dai, J. Ji, and Y. Yang, "VLA-Arena: An open-source framework for benchmarking vision-language-action models," arXiv:2512.22539, 2025.'),
    (71, 'C. He, S. Yuan, L. Fan, and S. Zhu, "A physics-consistent benchmark for contact-rich human-robot interaction in assistive care," arXiv:2609.02402, 2026. (Concurrent work.)'),
    (72, 'Y. Peng, P. Wang, S. S. Zhan, et al., "MANIGUARD: A benchmark and data suite for specification-grounded safety evaluation and improvement of robotic manipulation," arXiv:2608.17386, 2026. (Concurrent work.)'),
    (73, 'A. Balaji, A. Bahety, S. Ambatipudi, D. Lam, J. Xu, and R. Martín-Martín, "OopsieVerse: A safety benchmark with damage-aware simulation for robot manipulation," in *Proc. Robotics: Science and Systems (RSS)*, 2026, arXiv:2606.31993.'),
    (74, 'J. Song, S. Jeong, B. Jeon, S. Kim, M. Seo, H. Son, and K. Lee, "HABIT: Human-aware behavior and interaction training dataset for robot manipulation," arXiv:2606.31682, 2026.'),
    (75, 'M. Wilkinson, E. Fourney, J. W. Burdick, and A. D. Ames, "VLPSA: Vision-language-Poisson-safe actions for full-body safety of learned policies," arXiv:2609.22462, 2026.'),
    (76, 'Y. Agarwal and V. Raghunathan, "Multi-link safety filtering for VLA policies around moving hazards," arXiv:2609.40007, 2026.'),
    (77, 'S. Zhen, S. Jo, Y. Zhang, and W. Luo, "WBAG: A whole-body and attached-geometry safety framework for vision-language-action manipulation," arXiv:2610.01083, 2026.'),
    (78, 'M. Tayal and A. Nambi, "ShieldVLA: Feasibility-aware safety alignment for vision-language-action models," arXiv:2609.13231, 2026.'),
    (79, 'I. Tabbara, Y. Yang, and H. Sibai, "Towards general language-conditioned latent safety filters," arXiv:2608.00315, 2026.'),
    (80, 'Q. Wang, X. Wu, G. Shi, D. Chen, X. Yang, and D. Manocha, "Act on what you see: Unlocking safe social navigation in vision-language-action models," arXiv:2606.10495, 2026.'),
    (81, 'D. Jing, J. Nie, T. Zhang, J. Liu, H. Yao, Z. Lu, and M. Ding, "TempoVLA: Learning speed-controllable vision-language-action policies," arXiv:2606.06491, 2026.'),
    (82, 'A. Bajrami, M. Elshamouty, and W. Kraus, "How long until your robot ignores you? A safety benchmark for LLM orchestrators in human-humanoid collaboration," arXiv:2609.07288, 2026.'),
    (83, 'J. Kim, W. Chen, D. Soleymanzadeh, et al., "Modular safety guardrails are necessary for foundation-model-enabled robots in the real world," arXiv:2602.04056, 2026.'),
]
# SafeStage already sits at [61]; [68] would duplicate it -> drop 68 and keep the numbering contiguous by renumbering the rest
_NEW_REFS = [r for r in _NEW_REFS if r[0] != 68]
_REN = {}
_k = 68
for _n, _r in _NEW_REFS:
    if _n >= 69:
        _REN[_n] = _k; _k += 1
_NEW_REFS = [(_REN.get(_n, _n), _r) for _n, _r in _NEW_REFS]
R = {name: _REN.get(num, num) for name, num in (("hri", 69), ("arena", 70), ("care", 71), ("maniguard", 72), ("oopsie", 73), ("habit", 74),
                                                 ("vlpsa", 75), ("multilink", 76), ("wbag", 77), ("shield", 78), ("langfilter", 79),
                                                 ("salsa", 80), ("tempo", 81), ("orch", 82), ("guard", 83))}
_i = t.find("\n## References")
if _i > 0 and "[62] " not in t[_i:]:
    _j = t.find("\n## ", _i + 5)
    _j = len(t) if _j < 0 else _j
    _block = t[_i:_j].rstrip("\n")
    t = t[:_i] + _block + "\n\n" + "\n\n".join(f"[{n}] {r}" for n, r in _NEW_REFS) + "\n" + t[_j:]
elif _i <= 0:
    print("  [a156 MISS] References section")

# ---- the policies and their data, cited where they are introduced
_rn2("driven by π0.5, π0, π0-FAST (openpi; the last two co-trained on 10 % simulated data by PolaRiS; Appendix E.8) and GR00T N1.6-DROID",
     "driven by π0.5 [63], π0 [62], π0-FAST [64] (openpi [67]; the last two co-trained on 10 % simulated data by PolaRiS [66]; "
     "Appendix E.8) and GR00T N1.6-DROID")
_rn2("GR00T N1.6 on a Unitree G1 and four DROID-trained policies on a Franka", "GR00T N1.6 on a Unitree G1 and four DROID-trained [65] policies on a Franka")

# ---- section 2: concurrent evaluation work, the hypothesis' independent evidence, the remedy space
_rn2("for VLAs the remedy space is being populated (VLSA [22], filters [41]–[44], SPARK on the G1 [40]; HRI safety [46]–[52]).",
     f"for VLAs the remedy space is being populated (VLSA [22], filters [41]–[44], [{R['vlpsa']}]–[{R['langfilter']}], SPARK on the G1 [40]; "
     f"speed-conditioned VLAs [{R['tempo']}]; HRI safety [46]–[52]).")
_rn2("LIBERO-Safety [24] a margin to a hand proxy beside a fixed-base arm,",
     f"LIBERO-Safety [24] a margin to a hand proxy beside a fixed-base arm, HRIBench [{R['hri']}] whether an animated intruder is yielded to,")
_rn2("ForesightSafety-VLA [23], ROBOSHACKLES [56], TouchSafeBench [57] and HazardArena [19] sit elsewhere.",
     f"ForesightSafety-VLA [23], ROBOSHACKLES [56], TouchSafeBench [57] and HazardArena [19] sit elsewhere, and VLA-Arena [{R['arena']}], "
     f"MANIGUARD [{R['maniguard']}] and OopsieVerse [{R['oopsie']}] score object-level constraints with no person.")
_rn2("It is a testable hypothesis, not a demonstrated law: the same gap should appear in any imitation-trained VLA whose corpus was "
     "collected for success rather than for how the task is done.",
     f"It is a hypothesis, and two concurrent results bear on it: fine-tuning on human-present demonstrations elicits yielding "
     f"[{R['habit']}], and a navigation VLA encodes pedestrians it does not act on [{R['salsa']}].")
_rn2("(iii) scoring every dimension against a human-referenced quantity;",
     f"(iii) scoring every dimension against a human-referenced quantity for a bystander's unintended exposure ([{R['care']}] scores "
     f"intended care contact);")
_rn2("(i) on a locomoting humanoid with a human in the scene;",
     f"(i) of an end-to-end VLA on a locomoting humanoid with a human in the scene ([{R['orch']}] tests LLM orchestrators on one);")

# ---- Appendix G: the three-axis cut among other taxonomies; Table I
_rn2("Our three-axis cut", f"A modular-guardrail view splits action, decision and human-centred safety [{R['guard']}]. Our three-axis cut")
_rn2("Policies evaluated: SafeVLA-Bench 9, LIBERO-Safety 10, SafeManip 6, ForesightSafety 4 (+7 partial), HazardArena 4, this work 3.",
     "Policies evaluated: SafeVLA-Bench 9, LIBERO-Safety 10, SafeManip 6, ForesightSafety 4 (+7 partial), HazardArena 4, this work 5.")
_rn2("| Benchmark | Embodiment | Human in scene | Channels (≈ ours) | Speed / force vs a human | Carried hazard past a bystander | Fixability ablation |\n"
     "| --- | --- | --- | --- | --- | --- | --- |",
     "| Benchmark | Embodiment | Human in scene | Channels (≈ ours) | Speed / force vs a human | Carried hazard past a bystander | Fixability ablation | Person-blind null and feasibility witness |\n"
     "| --- | --- | --- | --- | --- | --- | --- | --- |")
import re as _re6
_ti = t.find("| Benchmark | Embodiment | Human in scene | Channels (≈ ours)")
if _ti > 0:
    _te = t.find("\n\n", _ti)
    _rows = t[_ti:_te].split("\n")
    _out = []
    for _r in _rows:
        if _r.startswith("| **This work**"):
            _r = ("| **This work** | **locomoting humanoid** + fixed-base arm | **Yes**: passive bystander; coworker's reaching or crossing "
                  "hand; passer-by | **T1–T6 in four dimensions** | **Yes**: T5a speed (ISO/TS 15066), T5b force by body region | **Yes**: "
                  "hot-plate keep-out beside the carry; scissors past an adult | **Yes**: prompt / perception, non-ceiling | **Yes**: "
                  "blind straight-line control; a witness per sub-type |")
        elif _r.startswith("| ---"):
            pass
        elif _r.startswith("| ") and not _r.startswith("| Benchmark") and _r.count("|") == 8:
            _r = _r + " No |"
        _out.append(_r)
    _extra = [f"| SafeStage [61] | fixed-base arm | No | before / during / after execution (≈T1/T2 during) | No | No | No | No |",
              f"| HRIBench [{R['hri']}] | fixed-base arm | **Yes**: animated instructor / collaborator / intruder (≈T6) | collision-free rate, "
              f"workspace intrusion | No | No | No | No |",
              f"| VLA-Arena [{R['arena']}] | fixed-base (LIBERO) | No | obstacle, cautious grasp ≈T3, hazard avoidance ≈T1, state "
              f"preservation ≈T4, dynamic obstacles ≈T6 | No | No | No | No |",
              f"| MANIGUARD [{R['maniguard']}] | fixed-base | No | spill / topple / drop invariants ≈T4, temporal constraints | No | No | "
              f"fine-tuning, not ablation | safe-success demonstrations |",
              f"| OopsieVerse [{R['oopsie']}] | fixed-base | No | object damage (force, heat, liquid) | No (objects) | No | No | No |",
              f"| Assistive-care benchmark [{R['care']}] | fixed-base arm | **Yes**: deformable patient, intended contact | region-wise "
              f"contact force | force on a simulated human (intended) | No | No | No |"]
    _hb = next(k for k, r in enumerate(_out) if r.startswith("| **This work**"))
    _out = _out[:_hb] + _extra + _out[_hb:]
    t = t[:_ti] + "\n".join(_out) + t[_te:]
else:
    print("  [a156 MISS] Table I")
