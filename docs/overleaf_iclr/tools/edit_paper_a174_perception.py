# -*- coding: utf-8 -*-
# Perception positive control (queues pcpa/pcpb, 2026-10-05; review item 11): can pi0.5 locate the person when asked to? Told to
# put the mug down in front of the person, with the person rendered (B) and hidden (C, the same words without a location).
# Applied when all four arms have both seeds. E (after the T3 paragraph) and, by outcome, finding (iv)'s closing sentence.
# Exec'd after a173 (uses t, _rn2, V).
_pc = V.get("pcp") or {}
if _pc.get("complete"):
    _A, _B, _C, _D = (_pc[a] for a in "ABCD")
    _pbc = float(_pc.get("B_vs_C", "1"))
    _sees = _pbc < 0.05 and _B["near"] / max(_B["n"], 1) > _C["near"] / max(_C["n"], 1)
    _fmt = lambda p: ("< 0.001" if p < 0.001 else f"= {p:.3f}" if p < 0.05 else f"= {p:.2f}")
    _txt = (" **Can the policy locate the person?** Told to put the mug down on the table in front of the person (on the right, "
            "0.51 m from the bowl), π0.5 ends it within 0.35 m of them on " + f"{_B['near']}/{_B['n']}" + " carries with the person "
            "rendered (median distance " + _B["d_med"] + " m) and on " + f"{_C['near']}/{_C['n']}" + " with the same words and the person "
            "hidden (" + _C["d_med"] + " m; Fisher *p* " + _fmt(_pbc) + ", Mann–Whitney on the distances *p* "
            + _fmt(float(_pc.get("B_vs_C_mwu", "1"))) + "); the neutral instruction puts it in the bowl (" + _A["d_med"]
            + " m), and told to \"give it to the person\" it puts the mug in the bowl on " + f"{_D['bowl']}/{_D['n']}"
            + " (median " + _D["d_med"] + " m). "
            + ("The policy finds the person when the instruction asks it to, so the absence of avoidance in §5 is not an absence of "
               "the percept." if _sees else
               "Asked to, the policy does not detectably place the mug by the person, so these runs cannot separate a missing "
               "percept from a missing competence."))
    _k = t.find("**T2.** A fixed-base arm works inside the table's footprint.")
    if _k > 0 and "**Can the policy locate the person?**" not in t:
        t = t[:_k] + _txt.strip() + "\n\n" + t[_k:]
    else:
        print("  [a174 MISS] E anchor")
    if _sees:
        _rn2("That the competences are *absent from the imitation training distribution* (§2) is consistent with every ablation "
             "here; it is not demonstrated by them.",
             "Asked to put a mug in front of the person, π0.5 does so only when the person is rendered (" + f"{_B['near']}/{_B['n']}"
             + " against " + f"{_C['near']}/{_C['n']}" + " hidden; E.8): it perceives where people are. That the competences are "
             "*absent from the imitation training distribution* (§2) is consistent with every ablation here; it is not demonstrated "
             "by them.")
else:
    print("  [a174] perception control not complete yet")
