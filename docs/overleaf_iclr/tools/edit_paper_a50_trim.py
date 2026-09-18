# -*- coding: utf-8 -*-
# Page budget: Table I (related-work placement) moves to Appendix G and the "risk no layer covers" paragraph to Appendix B,
# each with a one-line pointer in the main text. Exec'd after a49 (uses t, RN, _re).
import re as _re50

# --- Table I block: from its caption to the end of its table
_m = _re50.search(r"\*\*Table I\. Where this work sits among 2026 trajectory-level VLA-safety benchmarks\.\*\*[^\n]*\n\n(?:\|[^\n]*\n)+", t)
if _m:
    _blk = _m.group(0)
    t = t[:_m.start()] + t[_m.end():]
    RN("## Appendix G. Extended related work\n\n", "## Appendix G. Extended related work\n\n" + _blk.rstrip("\n") + "\n\n")
    # pointer at the end of the "What is, and is not, new here." paragraph
    _p = t.find("**What is, and is not, new here.**")
    _e = t.find("\n\n", _p)
    t = t[:_e] + " Table I (Appendix G) places this work among the 2026 trajectory-level suites." + t[_e:]

# --- the per-dimension "risk that no layer below the policy covers" paragraph -> Appendix B
_p = t.find("Each dimension also names a risk that no layer below the policy covers.")
if _p >= 0:
    _e = t.find("\n\n", _p)
    _para = t[_p:_e]
    t = t[:_p] + t[_e + 2:]
    RN("## Appendix B. Per-type schema instantiations\n\n",
       "## Appendix B. Per-type schema instantiations\n\n**Why no layer below the policy covers a dimension.** " + _para + "\n\n")
    RN("Dynamics is kept apart from the three motion dimensions because it alone is scored against a reference that moves: the question is not where, how or how fast, but whether the motion changes in time.",
       "Dynamics is kept apart from the three motion dimensions because it alone is scored against a reference that moves: the question is not where, how or how fast, but whether the motion changes in time. Each dimension also names a risk that no layer below the policy — collision checker, protective stop, force limit — covers (Appendix B).")
