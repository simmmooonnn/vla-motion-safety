# -*- coding: utf-8 -*-
# Page budget, fifth pass: the section-5 lead sentence, the attribution pointer and the Table III caption. Exec'd after a53.
_p = t.find("Table III is the benchmark's main result;")
if _p >= 0:
    _e = t.find("\n\n", _p)
    t = t[:_p] + t[_e + 2:]
RN("Appendix C gives thresholds and seeds, Appendix A every cell; completion under a substitute driver (2026-09-08 to 09-14) is not pooled (§8).",
   "Thresholds and seeds: Appendix C; every cell: Appendix A.")
_p = t.find("**Table III. Main results: one score per policy and dimension.**")
if _p >= 0:
    _e = t.find("\n\n", _p)
    t = (t[:_p] + "**Table III. Main results: one score per policy and dimension.** Bold: mean of the dimension's fixed sub-type set (§4.2), "
         "formed when every member has ≥ 8 scored episodes; brackets: sub-type rates (counts below eight). T3 pooled over bearings (chance "
         "50 %); T5a on the G1 only; T5c and the tabletop T5a exposure in Table IIIb. Last row: a scripted straight-line carry from privileged "
         "state, blind to the person (§5.5) — a column on which it scores like the policies is set by scene or task. *Witness*: a compliant "
         "completion shown in the scene." + t[_e:])
