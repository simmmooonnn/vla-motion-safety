# -*- coding: utf-8 -*-
# ICLR-readiness review (items 12 and 13/17): T3 by distance to the person (E, the tabletop T3 paragraph) -- read at the
# closest transport approach wherever it falls, the rate is the same when gated to approaches within 0.60 m; and the
# Reproducibility Statement names the golden test that re-scores every released cell. Exec'd after a164 (uses t, _rn2, V).
_g3 = V.get("t3_gate") or {}
if _g3.get("pi05") and _g3.get("scripted"):
    _rn2("so the rate tracks the object's initial pose across three settings with the person fixed.As on the G1",
         "so the rate tracks the object's initial pose across three settings with the person fixed. Nor does distance change it: "
         "restricted to closest approaches within 0.60 m of the person, the tip points into their half-space on "
         + _g3["pi05"]["0.6"] + " of π0.5's scored carries and " + _g3["scripted"]["0.6"] + " of the person-blind control's "
         "(at any distance " + _g3["pi05"]["9"] + " and " + _g3["scripted"]["9"] + "). As on the G1")
_rn2("The tabletop orientation scorer is checked against a truth fixture and an offline test suite (Appendix C).",
     "The tabletop orientation scorer is checked against a truth fixture and an offline test suite (Appendix C), and a golden "
     "test re-scores every released tabletop cell with the released scorer and reproduces every scored field of the summary "
     "the tables are generated from; the scoring specification lists each predicate, its field and threshold.")
