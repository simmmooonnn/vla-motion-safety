# -*- coding: utf-8 -*-
# C2 (compute queue): more action decoders on the same backbone and data -- openpi's PolaRiS DROID joint-position checkpoints of
# pi0-FAST (autoregressive FAST tokens, labels f0_) and PaliGemma-binning (RT-2-style bins, labels pb_) beside pi0 / pi0.5 (flow
# matching). If the base-relative bow recurs across decoders it is inherited from the DROID data, not from one action head.
# Every sentence is guarded on the floor and the verdict is decided from the numbers. Exec'd after a115 (uses t, RN, V).
_nd = int(V.get("n_new_decoders", "0") or 0)
_dr, _ob, _tn, _tu = V.get("drift", {}), V.get("t1_off_by", {}), V.get("t1_near", {}), V.get("t1_unseen", {})
_dc = V.get("dec_counts", {})
_NAME = {"f0": "π0-FAST", "pb": "PaliGemma-binning"}
_DESC = {"f0": "autoregressive FAST action tokens", "pb": "RT-2-style binned action tokens"}


def _n(x):
    try:
        return int(str(x).split("/")[1])
    except Exception:
        return 0


def _far(w, sf):
    return _dr.get(sf, {}).get(w, {}).get("far", "—")


def _cnt(w, sf):
    try:
        return int(_dr.get(sf, {}).get(w, {}).get("n", "0"))
    except Exception:
        return 0


def _fl(x):
    try:
        return float(x)
    except Exception:
        return None


def _ci(w, k):
    try:
        return int(_dc.get(w, {}).get(k, "0"))
    except Exception:
        return 0


_have = [w for w in ("f0", "pb") if _cnt(w, "desk") >= 8 and _cnt(w, "counter") >= 8]
# a decoder that was run at scale but never passes the floor is a capability boundary of the decoder, stated as such
_inert = [w for w in ("f0", "pb") if _ci(w, "att") >= 40 and _ci(w, "car") < 8]
_named = {"f0": "π0-FAST", "pb": "a PaliGemma-binning policy"}

# ---- section 4: the policy list of the tabletop family
if _nd >= 1:
    _live = [w for w in ("f0", "pb") if w not in _inert]
    _lst = ", ".join(_named[w] for w in _live)
    if len(_live) == 2:
        _tail = (" — openpi's PolaRiS DROID joint-position checkpoints, one backbone and one dataset under three action decoders "
                 "(flow matching, autoregressive FAST tokens, RT-2-style bins) — and GR00T N1.6-DROID")
    else:
        _tail = (" — openpi's PolaRiS DROID joint-position checkpoints, one backbone and one dataset under two action decoders "
                 "(flow matching, autoregressive FAST tokens); a third, RT-2-style binning, does not move the object in our scenes "
                 "(Appendix E.8) — and GR00T N1.6-DROID")
    RN("A second family puts the predicates around a Franka arm driven by π0.5, π0 (openpi) and GR00T N1.6-DROID",
       "A second family puts the predicates around a Franka arm driven by π0.5, π0, " + _lst + _tail)

# ---- Appendix E.8: the drift table gains a column per decoder that passes the floor at the counter and the desk
if _have:
    def _cell(w, sf):
        f = _far(w, sf)
        return f + (" (n=" + str(_cnt(w, sf)) + ")" if f != "—" else "")
    _old = "| Surface | π0.5 | π0 | scripted control |\n|---|---|---|---|\n" + V.get("drift_rows", "")
    _hdr = "| Surface | π0.5 | π0 | " + " | ".join(_NAME[w] for w in _have) + " | scripted control |\n|---|---|---|" + "---|" * len(_have) + "---|\n"
    _new = _hdr + "\n".join("| " + sf + " | " + " | ".join(_cell(w, sf) for w in ["pi", "pi0"] + _have + ["ik"]) + " |"
                            for sf in ("dining", "counter", "desk", "packing", "drawer"))
    RN(_old, _new)

# ---- the decoder sentence after the drift reading (verdict from the desk / counter bows; > 0.02 m = the bow is there) and the
#      inert-decoder note, appended to the same sentence
_anchor = ("What the trajectory dimension measures on the tabletop is therefore a bow the policy carries into every transport, large enough "
           "at some surfaces to enter a keep-out that a straight carry clears.")
_add = ""
_agree = []
_flat = []
if _have:
    _bows = {w: (_fl(_far(w, "desk")), _fl(_far(w, "counter"))) for w in _have}
    _agree = [w for w in _have if all(v is not None and v >= 0.02 for v in _bows[w])]
    _flat = [w for w in _have if w not in _agree]
    _parts = []
    for w in _have:
        s = _NAME[w] + " (" + _DESC[w] + "; the same PaliGemma backbone and DROID data) bows " + _far(w, "counter") + " m at the counter and " + \
            _far(w, "desk") + " m at the desk"
        d28 = _ob.get(w, {}).get("d28", {}).get("rate", "—")
        if _n(d28) >= 8:
            s += ", enters the 0.28 m far-side keep-out on " + d28
            nr, ur = _tn.get(w, {}).get("rate", "—"), _tu.get(w, {}).get("rate", "—")
            if _n(nr) >= 8 and _n(ur) >= 8:
                s += " (the near-side marker " + nr + ", the unrendered far-side keep-out " + ur + ")"
        _parts.append(s)
    if _agree and not _flat:
        _verdict = ("The decoders trained on one dataset agree with each other and with GR00T N1.6-DROID, whose backbone and decoder "
                    "both differ: the drift is inherited from the demonstrations, not from any one action head.")
    elif _agree and _flat:
        _verdict = (" and ".join(_NAME[w] for w in _flat) + " carries no such bow, so the drift is not a property of the data alone: "
                    "it depends on the decoder that reads it.")
    else:
        _verdict = ("The added decoder carries no such bow, so the drift belongs to the flow-matching heads (π0, π0.5) and to "
                    "GR00T-DROID, not to the DROID data as such.")
    _add += " The bow is not one action head's: " + "; ".join(_parts) + ". " + _verdict
for w in _inert:
    _add += (" " + _NAME[w] + " (" + _DESC[w] + ", the same backbone and data) is a boundary of the decoder rather than a row: over " +
             _dc[w]["att"] + " attempts on the Table III cells it lifts the object on " + _dc[w]["car"] + ", and its arm barely leaves "
             "the home pose, so it enters no table.")
if _add:
    RN(_anchor, _anchor + _add)

# ---- section 6 (ii): one clause, only when every decoder that passes the floor agrees
if _have and _agree and not _flat:
    RN("the near-side marker is entered on 0/32 and the far-side keep-out *unrendered* on 9/32 (Appendix E.8).",
       "the near-side marker is entered on 0/32 and the far-side keep-out *unrendered* on 9/32, and the bend recurs under a FAST-token "
       "decoder of the same data (Appendix E.8).")
