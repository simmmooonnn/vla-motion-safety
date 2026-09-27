# -*- coding: utf-8 -*-
# Page budget after the pi0-FAST row and the decoder clause in section 4: the section-4 policy sentence shorter, three section-8
# clauses tightened, the conclusion's policy count follows the data. Exec'd after a116 (uses t, RN, V).
_nd = int(V.get("n_new_decoders", "0") or 0)


def RNI(old, new):
    """RN only if the anchor is present (mutually exclusive variants)."""
    if old in t:
        RN(old, new)


RNI(" — openpi's PolaRiS DROID joint-position checkpoints, one backbone and one dataset under two action decoders "
   "(flow matching, autoregressive FAST tokens); a third, RT-2-style binning, does not move the object in our scenes "
   "(Appendix E.8) — and GR00T N1.6-DROID",
   " (openpi's PolaRiS DROID joint-position checkpoints: one backbone and dataset, two action decoders; a binning decoder "
   "does not move the object, Appendix E.8) and GR00T N1.6-DROID")
RNI(" — openpi's PolaRiS DROID joint-position checkpoints, one backbone and one dataset under three action decoders "
   "(flow matching, autoregressive FAST tokens, RT-2-style bins) — and GR00T N1.6-DROID",
   " (openpi's PolaRiS DROID joint-position checkpoints: one backbone and dataset, three action decoders, Appendix E.8) "
   "and GR00T N1.6-DROID")

RNI("We state the boundaries plainly (Appendix F expands each).", "Appendix F expands each boundary.")
RNI("On GR00T two proxies are weak — a box's long axis for a hazardous axis (T3), a rigid box that cannot spill (T4) — which the "
   "tabletop's scissors and mug replace.",
   "On GR00T two proxies are weak (a box's long axis for T3, a rigid box for T4); the tabletop's scissors and mug replace them.")
RNI("Cells run 2026-09-08 to 09-14 used a substitute driver that lowered pick success; their conditional rates are unaffected "
   "(Appendix E.7).",
   "A substitute driver lowered pick success on cells run 09-08 to 09-14; conditional rates are unaffected (E.7).")

if _nd >= 1:
    RNI("The profile recurs across two embodiments and four policies, and differs where the embodiment does;",
       "The profile recurs across two embodiments and " + ("five" if _nd == 1 else "six") + " policies, and differs where the embodiment does;")

# more slack: one clause each in (iii), section 7 and section 8
RNI("the same whether the person is a capsule, a photorealistic human or not rendered (Appendix E.8)",
    "the same at any rendering of the person (Appendix E.8)")
RNI(" A general guard is future work. **Release.**", " **Release.**")
RNI("and the operator standards scored against are applied to untrained bystanders, whom ISO 13482 would treat more conservatively.",
    "and operator standards are applied to bystanders, whom ISO 13482 treats more conservatively.")
RNI("below eight a sub-type prints as a count and forms no score)", "below eight a sub-type forms no score)")
RNI("and the next-cycle probes of Appendix E.8 are unscored.", "and E.8's next-cycle probes are unscored.")

# second pass: the section-4 parenthetical to its shortest, one clause in (iii), the hypothesis pointer
RNI(" (openpi's PolaRiS DROID joint-position checkpoints: one backbone and dataset, two action decoders; a binning decoder "
    "does not move the object, Appendix E.8) and GR00T N1.6-DROID",
    " (openpi; one backbone, two action decoders; a binning decoder does not move the object, Appendix E.8) and GR00T N1.6-DROID")
RNI(" (openpi's PolaRiS DROID joint-position checkpoints: one backbone and dataset, three action decoders, Appendix E.8) "
    "and GR00T N1.6-DROID", " (openpi; one backbone, three action decoders, Appendix E.8) and GR00T N1.6-DROID")
RNI("orientation, which no stop can correct, and speed, which a slowdown would change, are never adapted.",
    "neither orientation, which no stop can correct, nor speed, which a slowdown would change, is adapted.")
RNI("not from the prompt or the percept; argument, first test and alternative readings in Appendix F.",
    "not from the prompt or the percept (argument, first test and alternatives in Appendix F).")

# third pass, whole lines on page 10: the (iv) pointer sentence, the hypothesis pointer, the release clause
RNI(" The external stop that prevents it is itself incomplete on a humanoid (Appendix E.7).", " (Appendix E.7.)")
RNI("not from the prompt or the percept (argument, first test and alternatives in Appendix F).",
    "not from the prompt or the percept (Appendix F).")
RNI("Scenes, recorders, scripts and every per-episode log are released anonymously; a policy is a server swap, a task a new scene family.",
    "Scenes, recorders, scripts and every per-episode log are released anonymously.")

# fourth pass: two section-8 sentences
RNI(" The on-path ablations are **ceiling-limited**; the non-ceiling ablation detects only large effects.", "")
RNI("T2 has **no witness**; T3 has a geometric scripted witness on the tabletop, T4 a physical pinch-grasp witness based on 31 carried episodes, and T1 a witness on the G1 only.",
    "T2 has **no witness**; T3's is geometric, T4's a physical pinch grasp (31 carries), T1's on the G1 only.")
