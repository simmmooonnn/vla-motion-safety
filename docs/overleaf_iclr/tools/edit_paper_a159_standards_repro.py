# -*- coding: utf-8 -*-
# ICLR-readiness review (wf_425459e6-f4b, items 13(6), 16, 15(4) and the seed note of 10): standards wording corrected,
# instrument validity and the reach of Annex A stated (Appendix F, one pointer in section 8), the compute cost of the tabletop
# family and what a seed fixes (Appendix C). Exec'd after a158 (uses t, _rn2, V).
# ---- equivalence wording left in 6(iii)
_rn2("the carry speed is the same with and without the person (T5a).", "the carry speed shows no detectable change with the person present (T5a).")
# ---- standards
_rn2("0.25 m/s is the lowest collaborative speed in common use (ISO 10218-1 reduced speed),",
     "0.25 m/s is the ISO 10218-1 reduced speed for manual (teach) mode, used here as a conventional reference,")
_rn2("| + protective stop, 0.94 m (ISO 13855 walking speed) |", "| + protective stop, 0.94 m (ISO/TS 15066 $S_p$ at a 1.6 m/s approach) |")
_rn2("At 0.94 m — the ISO 13855 distance under its 1.6 m/s human-approach assumption —",
     "At 0.94 m — the ISO/TS 15066 protective separation computed with Table VI's parameters for a 1.6 m/s approach —")
_rn2("The crossing person is a kinematic capsule (radius 0.16 m, height 0.9 m, 60 kg) **with a collider**",
     "The crossing person is a kinematic capsule (radius 0.16 m, height 0.9 m; kinematic, so it has no effective mass) **with a collider**")
_rn2("(T5b there is the capsule's constraint force, not what a free hand feels: Annex A.3.3)",
     "(T5b there is the capsule's constraint force, not what a free hand feels; E.8)")
_rn2("(contacts, not force: Annex A.3.3)", "(contacts, not force; E.8)")
# ---- section 8: one pointer; Appendix F: the corrected measurement errors and the reach of Annex A
_rn2("the witnesses are geometric (T3), a pinch grasp (T4) and the blind carrier (T1).",
     "the witnesses are geometric (T3), a pinch grasp (T4) and the blind carrier (T1). Measurement errors corrected after the fact, "
     "and what Annex A's limits mean for a bystander, are in F.")
_fi = t.find("## Appendix F.")
if _fi > 0:
    _fj = t.find("\n\n", t.find("\n", _fi) + 1)
    _add = ("\n\n- **Instrument validity.** Five measurement errors were found and corrected after the cells had run, and each changed "
            "a headline number: the tabletop orientation was read in the wrong quaternion order until 2026-10-01 (every T3 and T4), "
            "the G1 crossing capsule stood 0.79 m above the floor in the September cells, the rendered G1 character was unposed and "
            "floating, the tabletop hand was assumed at 0.13 m on every surface (T6 under-counted on the taller ones), and the "
            "pre-fix child and seated cells rendered an adult while scoring a smaller body. Only orientation has a truth fixture "
            "(a scripted carry at known attitudes read back through the analyzer); every other predicate still rests on code review "
            "and on the rendered-versus-scored body check (PERSON_CHECK).\n"
            "- **The reach of Annex A.** ISO/TS 15066 Annex A gives pain-onset thresholds measured on informed adult volunteers; for "
            "an unaware bystander, a child or the head they are neither conservative nor valid, and we use them as reference points. "
            "A contact at head height is not scored against a force; on the tabletop the forces are a kinematic capsule's and are "
            "exposure (E.8).")
    t = t[:_fj] + _add + t[_fj:]
else:
    print("  [a159 MISS] Appendix F")
# ---- Appendix C: compute and seeds
_ci = t.find("## Appendix C. Reproducibility notes and sweeps")
if _ci > 0:
    _cj = t.find("\n\n", t.find("\n\n", _ci) + 2)
    _add = ("\n\n**Compute.** On the tabletop every cell is eight episodes; on one RTX PRO 6000 (96 GB) shared by three or four "
            "simulator clients and one policy server, the median wall-clock per cell was 15.6 min for π0.5 (645 logged cells), "
            "17.4 for π0, 14.7 for π0-FAST, 42.1 for GR00T N1.6-DROID and 14.4 for the scripted carrier, about 340 client-hours "
            "for the 1,170 cells with a logged start and end. A simulator client holds about 6 GB, a policy server about 30 GB. "
            "Two clients started in the same second collide on Arena's output directory, and two cold starts at once can crash "
            "the shader cache, so cells are staggered.\n\n"
            "**What a seed fixes.** A seed labels a cell; it does not fix an episode. Arena's placement solver, the policy server's "
            "sampling and GPU physics are not seeded together, so the same configuration and seed give different episodes on a "
            "rerun. Every interval is therefore clustered by cell, and every comparison that matters runs its arms in one session, "
            "interleaved.")
    t = t[:_cj] + _add + t[_cj:]
else:
    print("  [a159 MISS] Appendix C")
# ---- the child-height crosser predates the floor fix (centre 0.50 m above the spawn origin, not the floor), so its head height is
# unverified; its contacts are reported, not scored against a force
_rn2("**A child-height crosser (2026-09-28).** With the crossing capsule shrunk to a 1.0 m child (radius 0.12 m, centre 0.50 m, so "
     "the head sits at the carried box's height), GR00T carries on 11/24 attempts and reaches the child on 9/11, with a contact "
     "force on 9/11, above the 110 N limit on 6/11 (peaks 92–643 N) and no deceleration before the encounter on 10/11 — the same "
     "walk-into as for the adult, now at head height.",
     "**A child-height crosser (2026-09-28; not scored).** With the crossing capsule shrunk to a 1.0 m child (radius 0.12 m), GR00T "
     "carries on 11/24 attempts and reaches the child on 9/11, with no deceleration before the encounter on 10/11 — the same walk-into "
     "as for the adult. The cell predates the floor fix of 2026-10-01 (its capsule was placed by the September coordinates), so the "
     "body region struck is unverified and its contact forces are not read against Annex A.")
