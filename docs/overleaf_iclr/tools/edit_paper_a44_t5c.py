# -*- coding: utf-8 -*-
# T5c joins the predicate table and §5.3: a hazardous end that carries speed near a person. Exec'd after a43 (uses R, N, t).
import sys as _sys

if N.get("pi_t5c"):
    # --- Table II: the predicate and its reason
    _anchor = "| Dynamics | T6 | Moving person |"
    _i = t.find(_anchor)
    if _i < 0:
        _sys.exit("ANCHOR: Table II T6 row")
    _row = ("| Speed & force | T5c | Hazardous end in motion | speed of a held tool's hazardous end while it is within "
            "0.5 m of the person | > 0.25 m/s inside 0.5 m | ISO 10218-1 reduced speed for collaborative operation "
            "(250 mm/s); a moving edge is a transient contact, which the quasi-static limits of T5b do not cover |\n")
    t = t[:_i] + _row + t[_i:]

    # --- §5.3: its own paragraph, after T5b
    _j = t.find("\n\n### 5.4")
    if _j < 0:
        _sys.exit("ANCHOR: section 5.4")
    t = t[:_j] + "\n\n**T5c: a hazardous end that carries speed.** " + N["pi_t5c_sentence"].strip() + t[_j:]

    # --- §4.1: name the tool tasks among the tabletop family
    _a = "and a second task, serving, whose bowl stands at the table edge beside the adult."
    if t.count(_a) == 1:
        t = t.replace(_a, "a second task, serving, whose bowl stands at the table edge beside the adult; and tool tasks "
                          "(stir, scrape, toss) where the policy holds an implement rather than a payload.")

# --- page budget: the cross-policy paragraph says what the matrix already shows, and the caption repeats §4.1
_i = t.find("The tabletop family changes the embodiment, the task and the policy.")
if _i >= 0:
    _j = t.find("\n\n", _i)
    t = (t[:_i]
         + "Across four policies and two embodiments the profile recurs (Table III; Fig. \\ref{fig:heatmap}): keep-outs "
           "crossed, a hazard's orientation frozen, no slowing near people, no avoidance of a moving body. It differs "
           "where the embodiment does — the walking humanoid sweeps its body into bystanders, the fixed arm does not; "
           "the arm tilts a cup the rigid box could not show — and where the task does: serving beside the person raises "
           "the body-sweep rate tenfold. π0 carries on " + N['p0_carry'] + " episodes and GR00T N1.6-DROID on "
         + N['g0_carry'] + "; where they carry, both repeat the pattern (Appendix E.8)."
         + t[_j:])

_cap = ("A dimension's score is the mean of its sub-types' unsafe rates, each sub-type weighted equally (they name "
        "different hazards, and pooling by episode count would let the larger cell decide); the sub-type rates are "
        "given in each cell and their counts in Table IIIb. Predicates as in Table II, tasks as in §4.1.")
if t.count(_cap) == 1:
    t = t.replace(_cap, "A dimension's score is the mean of its sub-types' unsafe rates, each weighted equally; the "
                        "sub-type rates are in each cell, their counts in Table IIIb. Predicates: Table II; tasks: §4.1.")

# --- more room for T5c: the rebuttals and the release paragraph keep every claim in fewer words
_pairs = [
 ("(i) *Collision avoidance renamed.* The predicates are classical; the object of measurement — a policy with no map, planner or filter, scored against human-referenced standards along four dimensions, with fixability ablations — is not, and three of the four findings have no collision analogue.",
  "(i) *Collision avoidance renamed.* The predicates are classical; the object of measurement — a policy with no map, planner or filter, scored against human-referenced standards along four dimensions — is not, and three of the four findings have no collision analogue."),
 ("(ii) *An external layer fixes it.* Each instrument fixes one dimension at a cost — the shield clears a keep-out only at twice its radius (0/28 at ≥ 0.60 m, 22/25 at 0.30–0.50 m), the stop never releases before a static person (0/6) and misses the arms, the governor alone halts (0/12) — and none corrects orientation: what remains is what the policy must own (§1).",
  "(ii) *An external layer fixes it.* Each instrument fixes one dimension at a cost — the shield needs twice the radius (0/28 at ≥ 0.60 m), the stop never releases before a static person (0/6) and misses the arms, the governor alone halts (0/12) — and none corrects orientation (§1)."),
 ("Each sub-type is a scene family that ships three things (Fig. \\ref{fig:pipeline}): **(1)** the success-conditioned unsafe rate of an unmodified policy with its interval; **(2)** fixability ablations — name the hazard, hide it — at a placement where the rate can move; **(3)** a feasibility witness, so that the rate is attributable to the policy rather than to the scene.",
  "Each sub-type ships three things (Fig. \\ref{fig:pipeline}): **(1)** the success-conditioned unsafe rate of an unmodified policy with its interval; **(2)** fixability ablations at a placement where the rate can move; **(3)** a feasibility witness, so the rate is attributable to the policy, not the scene."),
 ("**Release.** Scene configurations, metric recorders, analysis scripts and every per-episode log behind Appendix A are released (anonymized repository); adding a policy is a server swap, adding a task a new scene family. Canonical thresholds and open design decisions are in Appendix H.",
  "**Release.** Scene configurations, recorders, analysis scripts and every per-episode log behind Appendix A are released (anonymized repository): adding a policy is a server swap, a task a new scene family. Thresholds and open decisions: Appendix H."),
]
for _a, _b in _pairs:
    if t.count(_a) == 1:
        t = t.replace(_a, _b)

# --- last page-budget pass: §8 keeps every caveat, Appendix F holds the detail
_p2 = [
 ("Cells are **small** (eight episodes per tabletop cell; T1 headline cells 3–8 completing carries, T5a *n* = 6, T6 *n* = 11 plus replicates) and the G1 person cell's payload is labelled, not physically, hazardous.",
  "Cells are **small** (eight episodes per tabletop cell; T5a *n* = 6, T6 *n* = 11) and the G1 person cell's payload is labelled, not physically, hazardous."),
 ("On GR00T two proxies are weak — the box's long axis stands in for a hazardous axis (T3) and its rigid box cannot spill (T4) — which the tabletop's scissors and mug replace; the people are capsules (the static ones without a collider) and the link metric uses link origins.",
  "On GR00T two proxies are weak — a box's long axis for a hazardous axis (T3), a rigid box that cannot spill (T4) — which the tabletop's scissors and mug replace; the people are capsules and the link metric uses link origins."),
 ("We state the boundaries plainly; Appendix F expands each. The evidence is **simulation-only**; each policy is measured in one scene family (GR00T in the corridor, π0.5 and π0 at the table), the tabletop family has witnesses for T3, T5b and T6 only, and π0 carries too rarely for most of its rates.",
  "We state the boundaries plainly; Appendix F expands each. The evidence is **simulation-only**; GR00T is measured in the corridor and the other policies at the table, the tabletop witnesses cover T3, T5b and T6 only, and π0 carries too rarely for most of its rates."),
]
for _a, _b in _p2:
    if t.count(_a) == 1:
        t = t.replace(_a, _b)
