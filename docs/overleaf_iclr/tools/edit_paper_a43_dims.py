# -*- coding: utf-8 -*-
# Table III becomes the policy x dimension matrix the review asked for (four parallel dimensions, one score each); the
# per-sub-type numbers move to Appendix A, where every cell already lives. Exec'd last by edit_paper_a41.py (uses R, N, t).
import sys as _sys

_i = t.find("| @@groups | Trajectory |")
_j = t.find("\n\n", t.find("| Witness in scene |", _i))
if _i < 0 or _j < 0:
    _sys.exit("ANCHOR: Table III block not found")
_old_block = t[_i:_j]

_wit = ("| Witness in scene | yes (G1) | " + ("yes (tabletop)" if N.get("t3_witness") else "—")
        + " | yes (both families) | yes (both families) |")
_new_block = (
    "| Policy | Trajectory | Orientation | Speed & force | Dynamics |\n"
    "|---|---|---|---|---|\n"
    + N["dim_table"] + "\n" + _wit)
t = t[:_i] + _new_block + t[_j:]

# caption: say what a dimension score is, and where the sub-types went
_capA = "**Table III. Main results: unsafe rate per policy and sub-type.**"
assert t.count(_capA) == 1, "ANCHOR: Table III caption"
t = t.replace(_capA, "**Table III. Main results: one score per policy and dimension.**")
_capB = "Unsafe rate in % (unsafe / scored); predicates as in Table II, tasks as in §4.1, every cell in Table X."
assert t.count(_capB) == 1, "ANCHOR: Table III caption body"
t = t.replace(_capB,
              "A dimension's score is the mean of its sub-types' unsafe rates, each sub-type weighted equally (they name "
              "different hazards, and pooling by episode count would let the larger cell decide); the sub-type rates are "
              "given in each cell and their counts in Table IIIb. Predicates as in Table II, tasks as in §4.1.")

# the sub-type detail table, in the appendix next to the per-cell table
_anchor = "### E.8"
_k = t.find(_anchor)
if _k < 0:
    _k = t.find("## Appendix E")
_ins = t.find("\n\n", t.find("\n", _k)) + 2
_detail = ("**Table IIIb. The same measurements by sub-type.** Unsafe rate in % (unsafe / scored). Table III averages "
           "each pair into its dimension.\n\n"
           "| Policy | T1 payload path | T2 body sweep | T3 presentation | T4 load tilt | T5a speed | T5b force | T6 moving person |\n"
           "|---|---|---|---|---|---|---|---|\n" + N["subtype_table"] + "\n\n")
t = t[:_ins] + _detail + t[_ins:]
