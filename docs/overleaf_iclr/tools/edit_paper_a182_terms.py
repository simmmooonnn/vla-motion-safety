# -*- coding: utf-8 -*-
# Review round 2026-10-06 (clarity): one name for the baseline in the main text -- "person-blind control" -- instead of six
# (blind carrier, person-blind carrier, blind line, blind straight line, ...). The abstract keeps its defining phrase
# ("a person-blind straight-line carry, which sets the rate a scene forces"). Main text only. Exec'd after a181 (uses t).
import re as _re3
_m = t.find("## Appendix A.")
_head, _tail = t[:_m], t[_m:]
_abs_def = "a person-blind straight-line carry, which sets the rate a scene forces"
_head = _head.replace(_abs_def, "@@ABSDEF@@")
for _old, _new in (("a person-blind straight line", "the person-blind control"), ("person-blind straight-line carrier", "person-blind control"), ("blind straight-line carrier", "person-blind control"),
                   ("person-blind carrier", "person-blind control"), ("person-blind carry", "person-blind control"),
                   ("the blind carrier", "the person-blind control"), ("The blind carrier", "The person-blind control"),
                   ("a blind straight line", "the person-blind control"), ("the blind straight line", "the person-blind control"),
                   ("blind straight line", "person-blind control"), ("the blind line", "the person-blind control"),
                   ("a person-blind straight line", "the person-blind control"), ("this blind line", "this control")):
    _head = _head.replace(_old, _new)
_head = _head.replace("person-person-blind", "person-blind")
_head = _head.replace("@@ABSDEF@@", _abs_def)
t = _head + _tail
