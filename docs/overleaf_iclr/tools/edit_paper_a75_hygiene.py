# -*- coding: utf-8 -*-
# Review round 3, C7 + C8 + C9: one number per quantity, the T6b secondary as its own quantity, and the exposure
# correction the authors' own data require. Exec'd after a74 (uses t, RN, between, V).

# --- C8: the coverage table gains the control's column (its episodes were already inside the caption's total)
RN("| Work surface | π0.5 | π0 | GR00T N1.6-DROID |",
   "| Work surface | π0.5 | π0 | GR00T N1.6-DROID | scripted control |")
_h = t.find("| Work surface | π0.5 | π0 | GR00T N1.6-DROID | scripted control |")
if _h >= 0:
    _e = t.find("\n", _h) + 1
    if t[_e:_e + 16].startswith("|---|---|---|---|") is False:
        pass
    _row = t[_e:t.find("\n", _e)]
    if _row.count("|") == 5:
        t = t[:_e] + "|---|---|---|---|---|" + t[t.find("\n", _e):]

# --- C8: the capability-boundary count follows the table
RN("tabletop tasks are exercised, four are capability boundaries",
   "tabletop tasks are exercised, " + V.get("n_tasks_boundary", "6") + " are capability boundaries")

# --- C9: the withdrawing hand is touched less often; say so, and say what does not change
_hs = V.get("hand_state", {})
if _hs.get("withdraw", "0/0") != "0/0":
    RN("A hand that pulls back is re-approached, not yielded to: the exposure rates of the static hand are not an artefact "
       "of a proxy that cannot move away.",
       "A hand that can move away is touched less often than one that cannot — " + _hs["withdraw"] + " against " +
       _hs["static"] + " (" + _hs["withdraw_pct"] + " % against " + _hs["static_pct"] + " %, Fisher *p* = " + _hs["p"] +
       ") — so part of the static hand's exposure is the proxy's immobility. What withdrawal does not buy is avoidance: the "
       "payload follows the retreating hand back to contact distance on " + V.get("hw", {}).get("follow", "20/25") +
       " of the withdrawals, so the hand is re-approached rather than yielded to, and every rate here is exposure under a "
       "proxy that cannot flinch, step back or protest.")
