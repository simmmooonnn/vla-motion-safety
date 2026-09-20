# -*- coding: utf-8 -*-
# Page budget, decisive cut: the Hypothesis paragraph moves to Appendix F (where its four alternative readings already live),
# leaving one sentence in §6. Exec'd after a80 (uses t, RN, between, V).
_p = t.find("**Hypothesis.**")
if _p >= 0:
    _e = t.find("\n\n", _p)
    _hyp = t[_p:_e]
    t = t[:_p] + ("**Hypothesis.** These findings are what one expects if execution-phase competences are *absent from the "
                  "imitation training distribution* (§2) rather than from the prompt or the percept; the argument, its first "
                  "test and four alternative readings are in Appendix F.") + t[_e:]
    # park the full paragraph at the head of the alternative-readings block in Appendix F
    _alt = t.find("**Alternative views.**")
    if _alt >= 0:
        t = t[:_alt] + _hyp + "\n\n" + t[_alt:]
    else:
        _f = t.find("## Appendix F")
        if _f >= 0:
            _fe = t.find("\n\n", _f)
            t = t[:_fe + 2] + _hyp + "\n\n" + t[_fe + 2:]
