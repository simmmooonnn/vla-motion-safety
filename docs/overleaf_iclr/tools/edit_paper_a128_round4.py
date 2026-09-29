# -*- coding: utf-8 -*-
# Round-4 items R2, R4, R5 and R8 (all text; the generator carries R1 and R3).
#   R2  the tabletop speed-and-force cell is exposure, because T5b there is the constraint force on an inert capsule
#   R4  cite and differentiate SafeStage (arXiv:2609.21223), concurrent work on the same simulator and embodiment
#   R5  say plainly that the tabletop rows are one dataset under three decoders, and retitle the recurrence claim
#   R8  T2's 0.10 m is the position-uncertainty allowance, not a protective separation; fix two mis-cited references
# Exec'd after a127 (uses t, RN, V).


def _rni(a, b):
    if a in t:
        RN(a, b)


# ---------------- R2: the fixed set and the caption
_rni("speed and force {T5a, T5b} on the humanoid and {T5b} on the tabletop (power-and-force limiting is the mode that "
     "applies there; the separation envelope is exposure)",
     "speed and force {T5a, T5b} on the humanoid and *exposure* on the tabletop (T5b there is the constraint force on an "
     "inert capsule, which Annex A.3.3 shows is not what a free hand feels, so the cells establish contact, not harm)")
_rni("speed and force is {T5a, T5b} on the G1 and {T5b} on the tabletop;",
     "speed and force is {T5a, T5b} on the G1 and exposure on the tabletop (contacts, not force: Annex A.3.3);")

# ---------------- R3's companion: say what the starred intervals mean
_rni("brackets: sub-type rates (counts below eight).",
     "brackets: sub-type rates (counts below eight). Intervals in Table IIIb are cluster-robust, since episodes inside a "
     "cell share a placement and a spawn pose; a star marks a rate whose design effect exceeds 1.5.")

# ---------------- R4: SafeStage, concurrent and closest
_rni("ForesightSafety-VLA [23], ROBOSHACKLES [56], TouchSafeBench [57] and HazardArena [19] sit elsewhere,",
     "ForesightSafety-VLA [23], ROBOSHACKLES [56], TouchSafeBench [57] and HazardArena [19] sit elsewhere. Concurrent "
     "work, SafeStage [61], scores unsafe contacts and region entries *during* execution on the same simulated DROID arm, "
     "with π0.5 and a GR00T policy among its four; none of its 97 scenarios contains a person, so what we add is the human "
     "reference — predicates defined against a body by an operator standard, each with an in-scene witness (Appendix G),")

# the detail belongs in the extended related work
_rni("**VLA agents.** End-to-end policies from RT-2 [3] and OpenVLA [4]",
     "**Concurrent work.** SafeStage [61] appeared while this paper was being written and cuts manipulation safety the same "
     "way: a lifecycle of before, during and after, whose middle stage — unsafe contacts, trajectories, region entries and "
     "object interactions *during* execution — is our axis. It is implemented in the same simulator family on the same "
     "simulated DROID embodiment (a Franka Panda with a Robotiq 2F-85) and evaluates π0.5 and GR00T N1.7 among four "
     "policies, so two of its rows are two of ours. It differs in what the predicates are *about*: its 97 scenarios contain "
     "no human, and its checks are events on objects and regions, with no separation distance, no force limit and no "
     "standard behind a threshold. The two are complementary — it covers the lifecycle, we cover the person — and the "
     "overlap sharpens rather than removes the contribution here, which is that every predicate is referenced to a human "
     "body through ISO 10218-1, ISO/TS 15066 or ISO 13482 and is paired with a witness that shows a compliant completion "
     "exists in the same scene." + chr(10) + chr(10) + "**VLA agents.** End-to-end policies from RT-2 [3] and OpenVLA [4]")

# ---------------- R5: one dataset, three decoders
_rni("The profile recurs across two embodiments and five policies and differs where the embodiment does;",
     "The profile recurs across two embodiments and five policies — though four of the five are trained on one corpus, so "
     "what recurs across the tabletop rows is a property of DROID's demonstrations read by three action decoders — and "
     "differs where the embodiment does;")

# ---------------- R8: what the 0.10 m threshold is, and two corrected references
_rni("[56] \"ROBOSHACKLES: Video-level safety evaluation for embodied agents,\" arXiv:2606.18632, 2026. (Verify authors/title at camera-ready.)",
     "[56] Z. Yin, C. Liu, W. Yang, R. Li, and Y. Xue, \"ROBOSHACKLES: A safety dataset for human-injury prevention in "
     "embodied foundation models,\" arXiv:2606.18632, 2026.")
_rni("[57] \"TouchSafeBench: A benchmark for physical-contact safety judgments of vision-language models,\" arXiv:2605.31196, 2026. (Verify authors/title at camera-ready.)",
     "[57] J. Wang, X. Xu, and X. Huang, \"Probing collision grounding in vision-language models for safe human-robot "
     "collaboration,\" arXiv:2605.31196, 2026.")
_rni("[60] J. A. Marvel and R. Norcross, \"Implementing speed and separation monitoring in collaborative robot workcells,\" *Robotics and Computer-Integrated Manufacturing*, vol. 44, pp. 144–155, 2017.",
     "[60] J. A. Marvel and R. Norcross, \"Implementing speed and separation monitoring in collaborative robot workcells,\" "
     "*Robotics and Computer-Integrated Manufacturing*, vol. 44, pp. 144–155, 2017.\n\n[61] J. Luo, Q. Zhang, W. Wang, and "
     "W. Jiang, \"SafeStage: Evaluating safety before, during, and after vision-language-conditioned robot manipulation,\" "
     "arXiv:2609.21223, 2026.")

# ---------------- page budget: the main text pays for what round 4 added; the detail is in the appendices
_rni("ForesightSafety-VLA [23], ROBOSHACKLES [56], TouchSafeBench [57] and HazardArena [19] sit elsewhere. Concurrent "
     "work, SafeStage [61], scores unsafe contacts and region entries *during* execution on the same simulated DROID arm, "
     "with π0.5 and a GR00T policy among its four; none of its 97 scenarios contains a person, so what we add is the human "
     "reference — predicates defined against a body by an operator standard, each with an in-scene witness (Appendix G),",
     "ForesightSafety-VLA [23], ROBOSHACKLES [56], TouchSafeBench [57] and HazardArena [19] sit elsewhere. Concurrent work "
     "SafeStage [61] cuts execution the same way on the same simulated arm, but no person appears in its 97 scenarios; the "
     "human reference is what we add (Appendix G),")
_rni("brackets: sub-type rates (counts below eight). Intervals in Table IIIb are cluster-robust, since episodes inside a "
     "cell share a placement and a spawn pose; a star marks a rate whose design effect exceeds 1.5.",
     "brackets: sub-type rates (counts below eight). Table IIIb's intervals are cluster-robust by cell (star: design "
     "effect > 1.5).")
_rni("The profile recurs across two embodiments and five policies — though four of the five are trained on one corpus, so "
     "what recurs across the tabletop rows is a property of DROID's demonstrations read by three action decoders — and "
     "differs where the embodiment does;",
     "The profile recurs across two embodiments and five policies — four of them trained on one corpus, so the tabletop "
     "recurrence is DROID's, read by three decoders — and differs where the embodiment does;")
_rni("speed and force {T5a, T5b} on the humanoid and *exposure* on the tabletop (T5b there is the constraint force on an "
     "inert capsule, which Annex A.3.3 shows is not what a free hand feels, so the cells establish contact, not harm)",
     "speed and force {T5a, T5b} on the humanoid and *exposure* on the tabletop (T5b there is the capsule's constraint "
     "force, not what a free hand feels: Annex A.3.3)")

# finding (i) carries three statistical tests the appendix already tabulates; the finding needs the verdicts, not the tests
_rni("On the path this probe is ceiling-limited, so we calibrated a placement with headroom — the stove 0.28 m off the "
     "path, blind rate 37 % (11/30, two seeds) — and ran the naming × rendering design (Table XI): naming leaves the rate "
     "at 29 % (6/21, Fisher *p* = 0.76), and at 16 % against 21 % with the stove hidden (*p* = 0.77; McNemar on 19 pairs "
     "*p* = 1.0).",
     "On the path this probe is ceiling-limited, so we calibrated a placement with headroom (the stove 0.28 m off the path, "
     "blind rate 37 %) and ran the naming × rendering design: naming changes nothing, rendering changes nothing "
     "(Table XI).")
_rni("The command reaches the policy: named-plus-visible halves completion (29 % against 47–68 % in the other arms, "
     "*p* < 0.001), and on π0.5 a spatial command leaves the plow-through at 88 % vs 94 % while cutting success to 62 %, a "
     "keep-upright command leaves its tilt as it was (22/39), and a blades-away command leaves the presentation unchanged "
     "(20/20).",
     "The command does reach the policy: named-plus-visible halves completion (29 % against 47–68 %, *p* < 0.001). On π0.5 "
     "a spatial command cuts success to 62 % and leaves the plow-through at 88 %, a keep-upright command leaves the tilt as "
     "it was, and a blades-away command leaves the presentation unchanged.")

_rni("In the same design, rendering the stove moves the carried path 2–3 cm *closer* (Mann-Whitney *p* = 0.013 blind, "
     "0.005 named; 33 % vs 18 % violating, pooled over naming).",
     "In the same design, rendering the stove moves the carried path 2–3 cm *closer* (Mann-Whitney *p* = 0.013 and 0.005; "
     "33 % vs 18 % violating).")
_rni("The carry yaw is the same at every bystander azimuth for GR00T and on either side of the table for π0.5 carrying "
     "scissors (T3), the same at any rendering of the person on either embodiment (Appendices E.7, E.8), and the carry "
     "speed is the same with and without the person for both (T5a): neither orientation, which no stop can correct, nor "
     "speed, which a slowdown would change, is adapted.",
     "The carry yaw is the same at every bystander azimuth for GR00T, on either side of the table for π0.5 (T3) and at any "
     "rendering of the person on either embodiment (E.7, E.8); the carry speed is the same with and without the person "
     "(T5a). Neither orientation, which no stop can correct, nor speed, which a slowdown would change, is adapted.")
_rni("No deceleration precedes contact at any crossing speed (T6), and a person who stops on contact is treated as an "
     "obstacle: the payload stays pressed against them, as a coworker's hand in the bowl is pressed by π0.5's mug. "
     "(Appendix E.7.)",
     "No deceleration precedes contact at any crossing speed (T6), and a person who stops on contact is treated as an "
     "obstacle, the payload pressed against them as a coworker's hand in the bowl is pressed by π0.5's mug (E.7).")

# the enumeration of coverage caveats belongs in Appendix F; section 8 keeps the headline
_battery = ("The **suite is smaller than its battery**: 40 of 51 tabletop tasks are exercised and 6 are capability "
            "boundaries; π0 and GR00T-DROID cover the canonical task only (π0-FAST 11 battery tasks, E.8); T5c is post "
            "hoc, the tabletop T5a exposure, and E.8's next-cycle probes unscored.")
if _battery in t:
    RN(_battery, "The **suite is smaller than its battery** and the matrix narrower still (Appendix F).")
    RN("We are deliberate about the boundaries of the empirical claims.",
       "We are deliberate about the boundaries of the empirical claims.\n\n**Coverage.** 40 of 51 tabletop tasks are "
       "exercised and 6 are capability boundaries; π0 and GR00T-DROID cover the canonical task only (π0-FAST 11 battery "
       "tasks, E.8); T5c is post hoc, the tabletop T5a and speed-and-force cell are exposure, and E.8's next-cycle probes "
       "are unscored. Table III is narrower than the suite: it scores the canonical pick-and-place and its two person "
       "variants, so the breadth of Table IV supports the design, not the matrix.")

_rni("The profile recurs across two embodiments and five policies — four of them trained on one corpus, so the tabletop "
     "recurrence is DROID's, read by three decoders — and differs where the embodiment does;",
     "The profile recurs across two embodiments and five policies — four of them one corpus read by three decoders — and "
     "differs where the embodiment does;")
_rni("We defined it as a third axis with four dimensions and scored each policy on each.",
     "We defined it as a third axis with four dimensions and scored each policy on it.")
_rni("Cells are **small** (eight episodes each; below eight a sub-type forms no score), the G1 person cell's payload is "
     "labelled rather than physically hazardous, and **the people have no state**:",
     "Cells are **small** (eight episodes each), the G1 person cell's payload is labelled rather than physically "
     "hazardous, and **the people have no state**:")

_rni("every proxy is a capsule that is static or kinematic, rendered as such to the policy, and reacts only by retreating "
     "on contact in one variant,", "every proxy is static or kinematic and reacts only by retreating on contact in one variant,")
_rni("and operator standards are applied to bystanders, whom ISO 13482 treats more conservatively.",
     "and operator standards are applied to bystanders, whom ISO 13482 treats more conservatively (Appendix F).")
_rni("None of it undercuts the case: along every dimension the policies are unsafe wherever there is something to avoid.",
     "None of it undercuts the case: along every dimension the policies are unsafe wherever there is something to avoid.")

# with the tabletop force cell now exposure, one section-8 clause is stale as well as long
_rni(" and the other policies at the table, and GR00T N1.6-DROID carries too rarely for a speed-and-force score.",
     " and the other policies at the table.")
_rni("VLA safety asks whether a task should be done and whether it ended well, not how it is carried out in between. We "
     "defined it as a third axis with four dimensions and scored each policy on it.",
     "VLA safety asks whether a task should be done and whether it ended well, not how it is carried out in between; we "
     "defined that as a third axis with four dimensions and scored each policy on it.")

_rni("not how it is carried out in between.  We defined it as a third axis with four dimensions and scored each policy on "
     "it. The profile recurs across two embodiments and five policies — four of them one corpus read by three decoders — "
     "and differs where the embodiment does; commands and rendered hazards change whether they finish and where they go, "
     "not how. What a policy owns is not the safety function but the demand it places on it, now measurable dimension by "
     "dimension.",
     "not how it is carried out in between; we defined that as a third axis with four dimensions and scored each policy on "
     "it. The profile recurs across two embodiments and five policies — four of them one corpus read by three decoders — "
     "and differs where the embodiment does, while commands and rendered hazards change whether they finish and where they "
     "go, not how. What a policy owns is not the safety function but the demand it places on it, now measurable dimension "
     "by dimension.")

_rni(" and differs where the embodiment does, while commands and rendered hazards change whether they finish and where "
     "they go, not how. What a policy owns", " and differs where the embodiment does. What a policy owns")
_rni("obstacle, the payload pressed against them as a coworker's hand in the bowl is pressed by π0.5's mug (E.7).\n\n"
     "**Hypothesis.** The competences are *absent from the imitation training distribution* (§2), not from the prompt or "
     "the percept (Appendix F).",
     "obstacle, the payload pressed against them as a coworker's hand in the bowl is pressed by π0.5's mug (E.7). We take "
     "the competences to be *absent from the imitation training distribution* (§2), not from the prompt or the percept "
     "(Appendix F).")

_rni("**Hypothesis.** The competences are *absent from the imitation training distribution* (§2), not from the prompt or "
     "the percept (Appendix F).",
     "The competences are, we think, *absent from the imitation training distribution* (§2) rather than from the prompt or "
     "the percept (Appendix F).")
_rni("The profile recurs across two embodiments and five policies — four of them one corpus read by three decoders — and "
     "differs where the embodiment does. What a policy owns is not the safety function but the demand it places on it, now "
     "measurable dimension by dimension.",
     "The profile recurs across two embodiments and five policies, four of them one corpus read by three decoders, and "
     "differs where the embodiment does. What a policy owns is not the safety function but the demand it places on it, now "
     "measurable dimension by dimension.")

_rni("so every contact rate is an exposure rate, not a harm rate (Annex A.3.3: 7 N median on a free hand, E.8), and "
     "operator standards are applied to bystanders, whom ISO 13482 treats more conservatively (Appendix F).",
     "so every contact rate is exposure, not harm (Annex A.3.3), and operator standards are applied to bystanders "
     "(Appendix F).")
_rni("The evidence is **simulation-only**; GR00T is measured in one corridor (0/31 delivered in two other rooms, E.7) and "
     "the other policies at the table.",
     "The evidence is **simulation-only**, GR00T in one corridor (0/31 delivered in two other rooms, E.7) and the other "
     "policies at the table.")

# ---------------- R8: what 0.10 m is, and what it is not
_rni("**Violation:** min link → body-surface distance < 0.10 m (the SSM position-uncertainty allowance $Z$); contact reported.",
     "**Violation:** min link → body-surface distance < 0.10 m; contact reported. The 0.10 m is ISO/TS 15066's "
     "position-uncertainty allowance $Z$, *not* a protective separation: the separation the standard would require for an "
     "approaching arm is an order of magnitude larger (≈ 0.48 m, Appendix F). T2 is therefore a proximity predicate — the "
     "robot's own body comes closer to a person than the standard's own uncertainty budget — and not a test of "
     "speed-and-separation compliance, which is what T5a reports.")
