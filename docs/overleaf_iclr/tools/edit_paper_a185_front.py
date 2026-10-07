# -*- coding: utf-8 -*-
# Review-round audit wf_f701d32a-3ba, block front: confirmed findings applied (exec at the end of the chain; uses t, _rn2, V).

_pd = V["pdose"]["arms"]
_nrT1 = V["null_rel"]["pi05"]["T1"]
_g4k, _g4n = (int(x) for x in V["g0_T4"].split("/"))
_g4pct = "%d %%" % round(100.0 * _g4k / _g4n)
_pmin = "%.2f" % (int(100 * min(_pd["pi05"][1]["p"], _pd["pi0fast"][1]["p"])) / 100.0)   # Fisher p of 'keep the mug upright' vs neutral, floored

# ---- Abstract
# trim (abstract, offsets findings 3/5/6/9 below): the two endpoints named, not phrased as questions
_rn2("is judged at two endpoints — should the instruction be followed, and is the end state acceptable — and neither constrains",
     "is judged at two endpoints, the instruction and the end state, and neither constrains")
# trim (abstract): 'how fast and how hard' -> 'how fast and hard', 'the person moves' -> 'they move'
_rn2("how fast and how hard it meets a person, and whether it reacts when the person moves.",
     "how fast and hard it meets a person, and whether it reacts when they move.")
# findings 3 + 10: T4 is not person-referenced, the control exists only on tabletop T1-T4, G1 T2-T4 have no witness; one name for the baseline
_rn2("Each sub-type is scored with a human-referenced predicate and read against two references: a person-blind straight-line carry, "
     "which sets the rate a scene forces, and a witness showing that a compliant completion exists.",
     "Each sub-type is scored with a trajectory predicate, mostly person-referenced, and read, where available, against a "
     "person-blind control (a scripted straight-line carry), which sets the rate a scene forces, and a witness showing a "
     "compliant completion exists.")
# trim (abstract): 'Franka arm' -> 'Franka'
_rn2("on a simulated Franka arm at six work surfaces,",
     "on a simulated Franka at six work surfaces,")
# finding 2: the control enters the keep-out on 18/160, so it does not 'clear' it; no third name ('the straight carry')
_rn2("that the straight carry clears (π0.5 90/159 against 18/160)",
     "that the control rarely enters (π0.5 " + _nrT1["pol"] + " against " + _nrT1["ctl"] + ")")
# finding 6: 'the table's tests' has no referent in an abstract; name the correction and the family
_rn2("and no other difference survives correction for the table's tests.",
     "and no other difference survives Holm correction over " + str(V["holm_m"]) + " matched comparisons.")
# finding 7: the heading is set by the spawn pose and the carry (pi0.5 pitches the blade), not by the person
_rn2("A hazard's orientation stays at its spawn pose wherever the person stands,",
     "A hazard's heading follows its spawn pose and the carry, not the person,")
# finding 5: the T6 counts are pi0.5's; name it and give pi0-FAST's
_rn2("a coworker's forearm crossing the transport is carried into on 57/88 episodes and waited for on 7/88.",
     "π0.5 carries into a coworker's forearm crossing the transport on " + V["pi_T6"] + " and waits on "
     + V["T6_wait_pi05"] + " (π0-FAST " + V["hx_pi0fast"]["reach"] + ", " + V["hx_pi0fast"]["wait"] + ").")
# trim (abstract): 'moves the motion, and in the wrong direction' -> 'moves the motion the wrong way'
_rn2("Safety language moves the motion, and in the wrong direction:",
     "Safety language moves the motion the wrong way:")
# finding 8: flat null from non-significant tests -> 'not detectably' (neutral counts moved into a parenthesis to pay for it)
_rn2('π0-FAST on 14/27, against 3/32 and 0/32 neutral, while "keep the mug upright" alone moves neither (5/32, 1/31).',
     "π0-FAST on " + _pd["pi0fast"][3]["t45"] + " (neutral " + _pd["pi05"][0]["t45"] + ", " + _pd["pi0fast"][0]["t45"]
     + '), while "keep the mug upright" alone moves neither detectably (' + _pd["pi05"][1]["t45"] + ", "
     + _pd["pi0fast"][1]["t45"] + "; p ≥ " + _pmin + ").")
# finding 9: the G1 has no person-blind control, so 'the same profile' is qualified
_rn2("A humanoid case study (GR00T N1.6, Unitree G1) shows the same profile.",
     "A humanoid case study (GR00T N1.6, Unitree G1; no person-blind control) shows a similar pattern.")

# ---- Introduction
# finding 13: 'a solved layer' is an uncited absolute; cite the classical layer ('they' trimmed to pay)
_rn2("out of mapped obstacles is a solved layer.",
     "out of mapped obstacles is a mature layer [8]–[10].")
_rn2("near people, and they fall between the existing layers:",
     "near people, and fall between the existing layers:")

# ---- Contributions
# finding 11: the tabletop sub-types share one canonical task and each rate pools every task with its predicate
# (witness clause compressed to pay); reviewer: the intro sentence above contribution 1 made the same
# 'own task' claim, so it is aligned too (pays for the GR00T N1.6-DROID parenthesis below)
_rn2("give each sub-type its own task and predicate, and report a profile per policy",
     "give each sub-type its own predicate, and report a profile per policy")
_rn2("a task per sub-type in two scene families (a humanoid corridor carry; tabletop pick-and-place at six work surfaces),",
     "a scene configuration per sub-type in two families (a humanoid corridor carry; tabletop pick-and-place at six work "
     "surfaces, rates pooled over tasks),")
_rn2("fixability ablations where the rate can move, and feasibility witnesses that decide whether a rate is the policy's or the scene's.",
     "fixability ablations where rates can move, and feasibility witnesses attributing a rate to the policy or scene.")
# finding 1: name GR00T N1.6-DROID and state that its matched T4 rate does not survive Holm (item compressed to pay:
# 'frozen ... whatever the person does', 'every one', 'Unitree', 'the body sweep varies with the policy')
_rn2("every one worse on the keep-out, and a humanoid case study (GR00T N1.6, Unitree G1);",
     "all worse on the keep-out, and a humanoid case study (GR00T N1.6, G1);")
_rn2("the well-sampled policies hold a frozen payload orientation whatever the person does,",
     "the well-sampled policies' payload orientation ignores the person,")
_rn2("the body sweep varies with the policy (",
     "body sweep varies by policy (")
_rn2(", and one arm policy tilts a cup where the box stays level.",
     ", and GR00T N1.6-DROID tilts a cup (" + _g4pct + "; its matched excess does not survive Holm correction) "
     "where the humanoid's box stays level.")
# reviewer: 37 % is the pooled T4 rate, while the Holm test is on matched placements (7/18 vs 3/31), so the
# parenthesis no longer reads as if the pooled rate were Holm-corrected
# finding 0: the spill clause raises the violation (pi0.5 and pi0-FAST); 'keep the mug upright' alone does not detectably
# (finding (iv) folded to pay)
_rn2("a safety command changes completion but not detectably the violation rate, and asked to keep a cup upright π0.5 tilts it more;",
     'a safety command changes completion, not detectably the violation, yet "do not spill the coffee" raises π0.5\'s and '
     'π0-FAST\'s tilt where "keep the mug upright" does not;')
_rn2("and a moving person is walked into, and one who stops is struck, not avoided.\n5.",
     "and a moving person, even one who stops, is walked into.\n5.")

# ---- Scope
# finding 12: external layers also count the demand (5.4), not only witness feasibility ('at all' trimmed to pay)
_rn2("External layers appear here only as instruments that show a compliant completion exists in a scene (§4.2).",
     "External layers appear here only as instruments that show a compliant completion exists (§4.2) and measure that demand (§5.4).")
_rn2("whether the layer can supply the competence at all:",
     "whether the layer can supply the competence:")

# ---- Section 2
# finding 4: T4 is not person-referenced and the control / witness do not cover every sub-type ('with no person in its
# scenarios' and 'What we add is' compressed to pay)
_rn2("every sub-type is scored against a person-referenced quantity and read against a person-blind control and a feasibility witness,",
     "every sub-type is scored on a trajectory quantity, mostly person-referenced, and, where available, read against a "
     "person-blind control and a feasibility witness,")
_rn2("on the same simulated arm with no person in its scenarios.",
     "on the same simulated arm with no person.")
_rn2("What we add is the human reference with attribution:",
     "We add the human reference with attribution:")
