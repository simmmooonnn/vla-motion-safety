# -*- coding: utf-8 -*-
# Review-round audit wf_f701d32a-3ba, block results: confirmed findings applied (exec at the end of the chain; uses t, _rn2, V).
import re as _re


def _rx(pat, repl):
    # regex replace of exactly one match (keeps the draft's own numbers via groups); prints MISS otherwise
    global t
    _n = len(_re.findall(pat, t))
    if _n != 1:
        print("  MISS x%d %s" % (_n, pat[:90]))
        return False
    t = _re.sub(pat, repl, t, count=1)
    return True


_nr = (V.get("null_rel") or {}).get("gr00t_droid", {}).get("T2", {})
_pd = (V.get("pdose") or {}).get("arms", {})
_b2 = ((V.get("b2xr") or {}).get("arms") or {}).get("blind_rend", {})

# [34] Table III caption: the witness claim covers scored tabletop sub-types (T2's on one placement); the G1's T2-T4 have none (caption trimmed to hold length)
_rn2("brackets: the sub-type rates (counts below eight), with intervals in Table IIIb. *Exposure*: the scene forces the outcome, so the "
     "cell is reported, not scored (§4.2). The last tabletop row is the person-blind straight-line control (§5.5), against which "
     "Fig. \\ref{fig:forest} compares each policy; every scored sub-type has a witness (§4.2).",
     "brackets: the sub-type rates (counts below eight; intervals in Table IIIb). *Exposure*: scene-forced, reported, not scored. The last "
     "tabletop row is the person-blind control (§5.5), the comparator in Fig. \\ref{fig:forest}. Every scored tabletop sub-type has a "
     "witness (T2's on one serving placement); the G1's T2–T4 have none (unattributed; §4.2).")

# [42] Table III row label: one name for the baseline
_rn2("| scripted straight-line controls · Franka | **", "| person-blind control · Franka | **")

# [37] §5.1 T1: the scored G1 T1 level is a case-study figure (normal-driver replication b2xr, E.2); trims in the same paragraph
_rn2("completing carries cross them — exposure, as the tabletop's on-path marker is; the scored G1 T1",
     "completing carries cross them — exposure; the scored G1 T1")
if _b2.get("comp"):
    _rn2("completing carries enter its 0.30 m keep-out (Table XI).",
         "completing carries enter its 0.30 m keep-out (Table XI; %d/%d on two new seeds with the driver restored: a case-study "
         "figure, E.2)." % (_b2["viol"], _b2["comp"]))
else:
    print("  MISS b2xr numbers absent (finding 37 not applied)")
_rn2("(the person-blind control enters it on ", "(the person-blind control on ")
_rx(r"is crossed by any transport, so that cell \((\d+/\d+)\) is exposure \(E\.8\)\.",
    r"is crossed by any transport: exposure (\1).")

# [36] §5.1 T2: GR00T N1.6-DROID's matched interval clears zero, but four cells a side cannot reach a permutation p below 0.056; trims in the same paragraph
if _nr.get("ci"):
    _rx(r"GR00T N1\.6-DROID (\d+/\d+) \(p = [0-9.]+, Holm [0-9.]+\) against the control's",
        lambda m: "GR00T N1.6-DROID %s (%+d points [%+d, %+d], yet p = %s, the floor for four cells a side; Holm %s) against the control's"
        % (m.group(1), _nr["rd"], _nr["ci"][0], _nr["ci"][1], _nr["p"], _nr["p_holm"]))
else:
    print("  MISS null_rel gr00t_droid T2 absent (finding 36 not applied)")
_rn2("once the table's tests are Holm-corrected:", "after Holm correction:")
_rn2(", the mirror image of the on-path marker's ceiling, so those cells are exposure.", ", so those cells are exposure.")
_rx(r"π0-FAST on (\d+/\d+), the person-blind control on \d+/\d+\. With the bowl away", r"π0-FAST on \1. With the bowl away")
_rx(r"episodes over (\d+) cells at three work surfaces,", r"episodes over \1 cells on three surfaces,")

# [44] §5.2 T3: denominator for the as-spawned blade-away deliveries (fr_summary t3_sci_R: 10 carried, 5 delivered blade-away)
_m = _re.search(r"into their half-space on \d+/(\d+) carries with the person on the right", t)
_den = _m.group(1) if _m else "10"
_rx(r"the object's pose sets it, not the person's, and as spawned (\d+) carries deliver them blade-away past the person on the right\.",
    lambda m: "the object's pose sets it, not the person's. As spawned, %s of the %s carries past the person on the right deliver them "
    "blade-away." % (m.group(1), _den))
# [40] §5.2 T3: the witness is in E.8 (E.4 is the G1 sweep), and the as-spawned deliveries are part of it
_rn2("left): the tabletop T3 witness (Appendix E.4, E.8).", "left): with the five as-spawned deliveries, the tabletop T3 witness (E.8).")
# trims (same paragraph)
_rn2("a property of the carry rather than of the person", "a property of the carry, not of the person")
_rx(r"Pooled over every task in which a hazardous-axis payload is carried past a still bystander \((\d+) tasks\) the rate is",
    r"Pooled over all \1 tasks carrying a hazardous-axis payload past a still bystander, the rate is")

# [32] §5.2 T4 heading: mentioning spilling, not asking for upright, raises the tilt (Table XIII)
_rn2("**T4: an upright carry, until upright is asked for.**", "**T4: an upright carry, until spilling is mentioned.**")
# [41] §5.2 T4: GR00T N1.6-DROID's 36/97 is its count above 45°, not above the spill angle (moved beside the 45° rate)
_rx(r"mid-transport on (\d+/\d+ = \d+ % \[\d+, \d+\]), and by more than a full cup's 14–27° spill angle on (\d+/\d+) \((\d+) %\); "
    r"GR00T N1\.6-DROID on (\d+/\d+)\.",
    r"mid-transport on \1 (GR00T N1.6-DROID \4), and by more than a full cup's 14–27° spill angle on \2 (\3 %).")
# [31] §5.2 T4: name the instruction actually run (with its spill clause) and add the prompt dose for pi0.5 and pi0-FAST (Table XIII)
_rn2("Told to keep hot coffee upright, π0.5 tilts the mug more, not less:",
     "Told to keep hot coffee upright so it does not spill, π0.5 tilts the mug more, not less:")
if _pd.get("pi05") and _pd.get("pi0fast"):
    _a, _f = _pd["pi05"], _pd["pi0fast"]
    _rx(r"\(a length-matched irrelevant sentence (\d+/\d+); E\.8\)\. GR00T's rigid box",
        lambda m: "(a length-matched irrelevant sentence %s; E.8). Of seven phrasings, \"do not spill the coffee\" gives %s past 45° "
        "(π0-FAST %s) against %s (%s) neutral, \"keep the mug upright\" alone %s (%s), not detectably more (Table XIII). GR00T's rigid box"
        % (m.group(1), _a[3]["t45"], _f[3]["t45"], _a[0]["t45"], _f[0]["t45"], _a[1]["t45"], _f[1]["t45"]))
else:
    print("  MISS pdose absent (finding 31 dose sentence not applied)")
# trims (same paragraph): pooled-task phrasing, the paired run, and the pinch control's attempts and carries (kept in §5.5)
_rx(r"pooled over every task in which it carries a spillable vessel past a still bystander \((\d+) tasks\) its axis",
    r"pooled over all \1 tasks carrying a spillable vessel past a still bystander, its axis")
_rx(r"against (\d+/\d+) with both instructions run back to back \(Fisher", r"against \1 neutral, run back to back (Fisher")
_rx(r"A person-blind straight-line control disables the attachment \(`SC_MAGIC=0`\) and physically pinches the same mug: across \d+ "
    r"attempts it carries \d+ and exceeds 45° on (\d+/\d+) — the tabletop T4 witness and Table IIIf's T4 control \(Appendix E\.5, E\.8\)\.",
    r"The person-blind control, pinching the same mug (§5.5), exceeds 45° on \1 carries: the tabletop T4 witness and "
    r"Table IIIf's T4 control (E.5, E.8).")

# [35] §5.3 T5s: not a scored member (not in Table III, no witness); its null is the person-hidden twin, now named as such
_rn2("a scored speed member (T5s) whose null is the path itself; the person adds no detectable slowing.",
     "T5s, a speed member beside the score (no witness); the person adds no detectable slowing.")
_rn2("Read against a twin with the person not rendered at each seed and placement, π0.5's", "π0.5's")
_rx(r"on (\d+/\d+) carries, against (\d+/\d+) with the person hidden \(Fisher",
    r"on \1 carries, against \2 in a person-hidden twin at each seed and placement (Fisher")

# [45] §5.4 T6: the 22/24 firings (0/11 carried contacts) and the 0/12 with force come from two runs (E.7)
_m = _re.search(r"no carried episode reaches contact \((\d+/\d+);", t)
_c11 = _m.group(1) if _m else "0/11"
_rx(r"A protective stop at 0\.50 m prevents the contact \((\d+/\d+) carried with force\) and fires on (\d+/\d+):",
    lambda m: "A protective stop at 0.50 m fires on %s with no carried contact (%s; %s with force on a floor-standing rerun):"
    % (m.group(2), _c11, m.group(1)))
# [43] §5.4 T6: broken "lowered onto on"; trim in the same sentence
_rx(r"A hand reaching into the bowl is lowered onto on (\d+/\d+) carried episodes, but there delivery itself demands the contact "
    r"\(the person-blind control (\d+/\d+)\), so that cell is exposure\.",
    r"The payload is lowered onto a hand reaching into the bowl on \1 carried episodes, but delivery itself demands it "
    r"(the person-blind control \2): exposure.")

# [39] §5.5: "no slowing" rests on non-significant tests
_rn2("no slowing near people, no avoidance", "no detectable slowing near people, no avoidance")
# [33] §5.5: GR00T N1.6-DROID's T2 excess is not distinguishable by Table IIIf's Holm-corrected test (interval and floor in §5.1)
if _nr.get("p_holm") is not None:
    _rx(r"and, on the body sweep, where the \*policy\* does: GR00T N1\.6-DROID's arm sweeps the body on (\d+) % of person-side serving "
        r"episodes against the person-blind control's (\d+) % \(\*p\* = [0-9.]+\),",
        lambda m: "and, on the body sweep, perhaps where the *policy* does: GR00T N1.6-DROID's arm sweeps the body on %s %% of person-side "
        "serving episodes against the person-blind control's %s %% (Holm %s: not distinguishable; §5.1),"
        % (m.group(1), m.group(2), _nr["p_holm"]))
# [38] §5.5: name the policy; the scored T2 is the whole serving family (pi0.5 48/340 = 14 %), 31 % its person-side subset
_k2 = str(V.get("pi_T2", "48/340")).split("/")
_pct2 = round(100.0 * int(_k2[0]) / int(_k2[1]))
_rx(r"which is why T2 is scored there \((\d+) % with the bowl on the person's side, (\d+/\d+) with it away\)",
    lambda m: "which is why T2 is scored there (π0.5 %d %%, its person-side cells %s %%; %s with the bowl away)"
    % (_pct2, m.group(1), m.group(2)))
# trim (same paragraph)
_rn2("almost never at the counter or the desk", "almost never at the counter or desk")

# [42] §5.5 heading: one name for the baseline
_rn2("**Scripted straight-line controls.** The geometric variant", "**The person-blind control.** Its geometric variant")
