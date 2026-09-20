# -*- coding: utf-8 -*-
# The pour numbers in section 6 follow the summary (more seeds). Exec'd after a65 (uses t, RN, V).
_po = V.get("pour", {})
if _po.get("away", "0/0") != "0/0":
    RN("a pour tilts only over the bowl (0/11 away),", "a pour tilts away from the bowl on " + _po["away"] + " carries (over it on " + _po["over"] + "),")
