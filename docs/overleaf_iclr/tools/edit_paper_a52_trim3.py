# -*- coding: utf-8 -*-
# Page budget, third pass: Table II loses its "why this predicate" column (the reasons become a list in Appendix D); two
# background paragraphs move to Appendix G. Exec'd after a51 (uses t, RN).
import re as _re52

# --- Table II: strip the last column, collect the reasons
_h = t.find("| Dimension | ID | Sub-type | Measured quantity | Unsafe when | Why this predicate |")
if _h >= 0:
    _e = t.find("\n\n", _h)
    _rows = t[_h:_e].split("\n")
    _new, _why = [], []
    for _r in _rows:
        _c = [x.strip() for x in _r.strip().strip("|").split("|")]
        if len(_c) == 6 and not set(_r.strip()) <= set("|-: "):
            _new.append("| " + " | ".join(_c[:5]) + " |")
            if _c[1] != "ID":
                _why.append("- **" + _c[1] + " " + _c[2] + ".** " + _c[5])
        elif set(_r.strip()) <= set("|-: "):
            _new.append("|---|---|---|---|---|")
        else:
            _new.append(_r)
    t = t[:_h] + "\n".join(_new) + t[_e:]
    RN("Tables VI and VII place the six sub-types against the safety standards and against the peer taxonomies.",
       "Tables VI and VII place the six sub-types against the safety standards and against the peer taxonomies.\n\n"
       "**Why each predicate.** Where a standard fixes the value we adopt it; where none does we state the choice and report the rate's "
       "sensitivity to it.\n\n" + "\n".join(_why))
    RN("The last column of Table II gives the reason for each predicate: where a standard fixes the value we adopt it, and where none does we state the choice and report the rate's sensitivity to it.",
       "Appendix D gives the reason for each predicate: where a standard fixes the value we adopt it, and where none does we state the choice and report the rate's sensitivity to it.")

# --- two background paragraphs -> Appendix G
for _head in ("**Classical motion safety.**", "**VLA agents.**"):
    _p = t.find(_head)
    if _p >= 0:
        _e = t.find("\n\n", _p)
        _para = t[_p:_e]
        t = t[:_p] + t[_e + 2:]
        RN("## Appendix G. Extended related work\n\n", "## Appendix G. Extended related work\n\n" + _para + "\n\n")
RN("**Instruction-level safety.** A growing body of work asks whether an embodied agent should comply with a command at all:",
   "**Instruction-level safety.** (The VLA lineage and the classical motion-safety machinery this work builds on are summarized in Appendix G.) "
   "A growing body of work asks whether an embodied agent should comply with a command at all:")
