# -*- coding: utf-8 -*-
# Review round 2026-10-06, page budget for the forest figure: Table III's caption cut to three sentences (the reviewers: "a methods
# section"), section 2's "what is new" list cut to a positioning paragraph whose claim is the human reference with attribution,
# and 5.3's T5b paragraph to two sentences (the detail is in E.7/E.8). Exec'd after a180 (uses t, _rn2, V).
_i = t.find("**Table III. Main results: one score per policy and dimension.**")
_e = t.find("\n\n", _i)
if _i > 0 and _e > _i:
    t = t[:_i] + ("**Table III. Main results: one score per policy and dimension.** Bold: the mean of the dimension's sub-type rates, "
                  "formed when every member has at least eight scored episodes; brackets: the sub-type rates (counts below eight), with "
                  "intervals in Table IIIb. *Exposure*: the scene forces the outcome, so the cell is reported, not scored (§4.2). The "
                  "last tabletop row is the person-blind straight-line control (§5.5), against which Fig. \\ref{fig:forest} compares "
                  "each policy; every scored sub-type has a witness (§4.2).") + t[_e:]
else:
    print("  [a181 MISS] Table III caption")
_i = t.find("**What is, and is not, new here.**")
_e = t.find("\n\n", _i)
if _i > 0 and _e > _i:
    t = t[:_i] + ("**What is, and is not, new here.** Constraining *how* a motion unfolds is classical [8]–[11], [16]–[18], and "
                  "trajectory-level VLA-safety evaluation exists: SafeVLA-Bench [27], VLA-Arena [69] and MANIGUARD [71] score "
                  "object-level constraints with no person, LIBERO-Safety [24] a margin to a hand proxy beside a fixed-base arm, "
                  "HRIBench [68] whether an animated intruder is yielded to, and concurrent SafeStage [61] cuts execution the same way "
                  "on the same simulated arm with no person in its scenarios. What we add is the human reference with attribution: "
                  "every sub-type is scored against a person-referenced quantity and read against a person-blind control and a "
                  "feasibility witness, with fixability ablations where the rate can move, and a humanoid case study. Table I and "
                  "Appendix G place this work among the 2026 suites.") + t[_e:]
else:
    print("  [a181 MISS] what is new")
_i = t.find("**T5b: the force that reaches the person.**")
_e = t.find("\n\n", _i)
if _i > 0 and _e > _i:
    t = t[:_i] + ("**T5b: the force that reaches the person.** The crossing person's contact sensor registers a contact on every "
                  "carried encounter (21/21, median 148 N), and a tabletop hand is touched on 65/83 carried episodes; both proxies are "
                  "kinematic, so these are constraint forces with no compliance behind them and T5b is exposure on both embodiments "
                  "(E.7, E.8).") + t[_e:]
else:
    print("  [a181 MISS] T5b")
