# -*- coding: utf-8 -*-
# Consistency audit wf_fe8809d8-343, range appBCDE1: confirmed findings applied (exec at the end of the chain; uses t, _rn2, V).
# Every edit below is in the appendices (after '## Appendix A.'), so the main-text word count does not change. The main-text
# echoes some findings name (Sec. 4.2 T5b, Sec. 5.4 '11 contacts' and the 22/24 stop, Sec. 6 (i) 'about 3 cm') belong to other
# ranges and are left alone here.
import re as _re


def _a175_g1():
    # the G1 row of Table IIIb (typed into the generator): T1 .. T6b
    for _r in V["tab3b_rows"].split("\n"):
        if _r.startswith("| GR00T N1.6 · G1 |"):
            _c = [c.strip() for c in _r.strip().strip("|").split("|")][1:]
            return dict(zip(["T1", "T2", "T3", "T4", "T5a", "T5b", "T6", "T6b"], _c))
    return {}


_G1 = _a175_g1()
_G1n = {k: v.split(" = ")[0] for k, v in _G1.items()}
_g1_t5a = _G1n.get("T5a", "22/22")
_g1_t6b = _G1n.get("T6b", "17/18")
_m175 = _re.search(r"(\d+)/(\d+) contacts", _G1.get("T5b", ""))
_g1_o140, _g1_enc = ((_m175.group(1) + "/" + _m175.group(2)), int(_m175.group(2))) if _m175 else ("14/21", 21)


def _a175_wlo(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n)
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return int(round(100 * (c - h) / d))


_t5a_k = int(_g1_t5a.split("/")[0])
_t5a_more = _t5a_k - 6          # the 6 matched carries of E.6; the rest are the Sec. 5.1 person cell
_t6b_k, _t6b_n = (int(x) for x in _g1_t6b.split("/"))

# Finding (Appendix B, T6): the tabletop evidence was the reaching hand, which is exposure; the scored tabletop T6 is the crossing hand
_rn2("- **Evidence (tabletop):** a coworker's hand reaching into the destination bowl is reached by π0.5's mug on 81/83 carried episodes and pressed for ≥ 5 s in 16/83 (5.3–23.5 s; §5.4).",
     "- **Evidence (tabletop, scored):** a coworker's forearm crossing the transport line ahead of the payload is reached by π0.5's payload on " + V["pi_T6"]
     + " scored carries (pick-and-place " + V["hx_pi05"]["reach"] + ", pouring " + V["pour2"]["pi"]["hx"] + ") and waited for on " + V["T6_wait_pi05"] + " (§5.4, E.8).\n"
     "- **Exposure (tabletop, not scored):** a coworker's hand reaching into the destination bowl is reached by π0.5's mug on " + V["pi_T6_hand"]
     + " carried episodes (delivery itself forces the contact) and pressed for ≥ 5 s in " + V["pi_handK"]["ge5"] + " (5.3–23.5 s; §5.4).")

# Finding (Appendix D, availability rule): the reaching hand listed as a T6 condition; only the crossing hand is scored
_rn2("moving for T6 (a hand reaching into the destination, or crossing the transport line ahead of the payload) and T6b",
     "moving for T6 (a hand crossing the transport line ahead of the payload; a hand reaching into the destination forces the contact and is reported as exposure) and T6b")

# Finding (E.7 Annex A reading of the G1 crossing forces; Sec. 5.3 says they are not read against Annex A): recast as scale only
_rn2("Against ISO/TS 15066 Annex A, 17/21 peaks exceed the 110 N abdominal",
     "These are constraint forces of a kinematic body, an upper bound and exposure (§5.3), so Annex A is a scale here, not a score: against ISO/TS 15066 Annex A, 17/21 peaks exceed the 110 N abdominal")
# same finding: the Appendix B T5 heading claimed 'forces above body-region limits'
_rn2("— *T5a: no slowing; T5b: forces above body-region limits*",
     "— *T5a: no slowing; T5b: exposure (constraint forces of a kinematic body)*")
_rn2("records 55–539 N peaks on every carried encounter, §5.4;",
     "records 55–539 N peaks on every carried encounter (constraint forces of a kinematic body: exposure), §5.4;")

# Finding (Table IVe, T5b row): 'the humanoid corridor' named as T5b's scored pool, but G1 T5b is exposure too; cells shown as exposure
_m175b = _re.search(r"\| Speed & force \| T5b \| the humanoid corridor; on the tabletop the force is the capsule's \(exposure\) \|([^\n]*)", t)
if _m175b:
    _cells175 = _re.sub(r"0 \((\d+)\) / (\d+) / (\d+)", lambda m: "(" + m.group(1) + " task / " + m.group(2) + " / " + m.group(3) + ": exposure)", _m175b.group(1))
    t = t[:_m175b.start()] + "| Speed & force | T5b | none: exposure on both families (the crossing person and the tabletop hand are kinematic; constraint forces) |" + _cells175 + t[_m175b.end():]
else:
    print("  MISS x0 Table IVe T5b row")

# Finding (E.2): 'a safety command changes ... never where its path runs' contradicts the 3 cm hidden-stove shift (p = 0.017)
_rn2("a safety command changes whether GR00T finishes the task and never where its path runs;",
     "a safety command changes whether GR00T finishes the task and moves its path by 3 cm at most (with the stove hidden, *p* = 0.017);")

# Finding (Appendix B, T1 fixability): 'no detectable prompting or perception effect (Sec. 5.1 ...)' -- E.2 finds significant clearance shifts; the ablations are in Sec. 6 / E.2
_rn2("- **Fixability:** no detectable prompting or perception effect (§5.1, though the ablation is underpowered) → an external reactive shield",
     "- **Fixability:** neither naming nor hiding the hazard produces a significant drop in the violation rate (Table XI); on the continuous clearance, rendering moves the path 2–5 cm toward the hazard and naming moves a hidden-hazard path 3 cm away (E.2) → an external reactive shield")

# Finding (Table IIIe caption): '13 single-task pools / 22 one-goal pools' still count the five exposure T5b pools; recomputed from Table IIIb
def _a175_scored():
    n, on = 0, False
    for _r in V["tab3b_rows"].split("\n"):
        if "*Tabletop benchmark*" in _r:
            on = True; continue
        if "*Humanoid case study*" in _r:
            break
        if on and _r.startswith("|"):
            _c = [c.strip() for c in _r.strip().strip("|").split("|")][1:]
            n += sum(1 for c in _c if c and not c.startswith("(") and c != "—")
    return n


_single175 = _a175_scored() - len([r for r in V["tab3e_rows"].split("\n") if r.startswith("|")])
_rn2("The other 13 scored pools rest on one task, where the pooled and task-macro rates coincide by construction; 22 pools rest on one goal (those 13 and 9 of the rows above).",
     "The other " + str(_single175) + " scored pools rest on one task, where the pooled and task-macro rates coincide by construction; "
     + str(_single175 + int(V["tab3e_onegoal_multi"])) + " pools rest on one goal (those " + str(_single175) + " and " + V["tab3e_onegoal_multi"] + " of the rows above).")

# Finding (Table IIIb caption): G1 T6b defined over 'the 11 contacts' while the cell is 17/18
_rn2("T6b on the G1 is the absence of any deceleration before the 11 contacts (E.7).",
     "T6b on the G1 is the absence of any deceleration before the encounter, over " + str(_t6b_n) + " scored crossing carries (11/11 in three seeds, "
     + str(_t6b_k - 11) + "/" + str(_t6b_n - 11) + " in two further seeds; §5.4, E.7).")
# same finding: E.7 never reported the two further seeds behind the 17/18
_rn2("What happens at contact depends on the timing of the crossing:",
     "Two further seeds (2026-09-28) reach the person on 6/8 carried episodes, with no deceleration before the encounter on "
     + str(_t6b_k - 11) + "/" + str(_t6b_n - 11) + " scored carries (" + ("one decelerates" if _t6b_n - _t6b_k == 1 else str(_t6b_n - _t6b_k) + " decelerate")
     + "); with the 11 they give Table IIIb's T6b " + _g1_t6b + ". What happens at contact (in the three seeds) depends on the timing of the crossing:")

# Finding (Table IIIb, G1 T5b): '14/21 contacts' -- contact is 21/21; 14/21 is the count over 140 N
_rn2("(14/21 contacts, kinematic body: exposure)",
     "(" + _g1_o140 + " over 140 N; contact " + str(_g1_enc) + "/" + str(_g1_enc) + ", kinematic body: exposure)")

# Finding (Table IIIc, G1 'any contact' 13/13 and T6c 3/5): superseded raised-capsule run; the floor-standing rerun gives 21/21
_rn2("| T5b any contact with the hand / person | 13/13 = 100 % [77, 100] |",
     "| T5b any contact with the hand / person | " + str(_g1_enc) + "/" + str(_g1_enc) + " = 100 % [" + str(_a175_wlo(_g1_enc, _g1_enc)) + ", 100] |")
_rn2("| T6c payload kept pressed ≥ 5 s (hand) / until the episode ends (person) | 3/5 (below the floor) |",
     "| T6c payload kept pressed ≥ 5 s (hand) / until the episode ends (person) | 3/5 (below the floor; the superseded raised capsule, E.7) |")

# Finding (Table IIIc, held-on-hand row): 'nested in T6' -- the reaching hand is exposure, not the scored crossing-hand T6
_rn2("| T6, payload kept on the reaching hand ≥ 0.6 s (cumulative contact > 1 N at the 1/15 s steps; nested in T6;",
     "| Payload kept on the reaching hand ≥ 0.6 s (cumulative contact > 1 N at the 1/15 s steps; nested in the reaching-hand exposure, π0.5 "
     + V["pi_T6_hand"] + ", not in the scored T6;")

# Finding (E.1): categorical nulls from 12 episode pairs (p = 0.28) and n = 8 vs 6 (p = 0.52)
_rn2("and the bystander is not one of the things it varies with.",
     "and at this sample size (12 episode pairs) the bystander produces no detectable change in it.")
_rn2("but nothing in it answers to the person",
     "but nothing detectable in it answers to the person")
_rn2("so what the readout shows is that a person standing beside the transport is not an input to the base command;",
     "so what the readout shows is that no input from a person standing beside the transport is detectable in the base command;")

# Finding (E.1): 'met exactly as one present from the start or absent' from non-significant tests at 16 per arm
_rn2("(on the tabletop a person arriving mid-carry is met exactly as one present from the start or absent, E.8)",
     "(on the tabletop no slowing for a person who arrives mid-carry was detected, 16 episodes per arm, E.8)")

# Finding (E.2): 'Naming does not reduce the violation rate' from Fisher p = 0.76 / 0.77 with falling point estimates
_rn2("*Naming* does not reduce the violation rate in either rendering condition",
     "*Naming* produces no significant reduction in the violation rate in either rendering condition")

# Finding (E.2): rendering shift '2–3 cm' -- Table XI medians give 2.3 cm (blind) and 4.8 cm (named)
_rn2("the minimum clearance is 2–3 cm smaller in both language conditions (Mann-Whitney",
     "the median minimum clearance is 2–5 cm smaller in both language conditions (0.333 → 0.310 m blind, 0.363 → 0.315 m named; Mann-Whitney")

# Finding (E.2): one uncorrected Fisher test (p = 0.03) declared 'real' beside 'not powered to adjudicate'
_rn2("The perception effect on completion is therefore real but acts at the grasp,",
     "Whatever the completion difference reflects (*p* = 0.03, one uncorrected test), it acts at the grasp,")

# Finding (Appendix D, T1 'why'): radius-flat result is the on-path (exposure) G1 run; the scored off-path pools are offset-sensitive
_t1o = V["t1_by_off"]["pi05"]
_rn2("illustrative radii, below any ISO 13855 separation; the rate is flat for radii 0.15–0.80 m (clearances are bimodal), so the choice does not drive it",
     "illustrative radii, below any ISO 13855 separation; on the G1's path (exposure) the rate is flat for radii 0.15–0.80 m (clearances are bimodal), "
     "but the scored off-path pools sit at the keep-out's edge, where the rate turns on the radius and the offset (tabletop π0.5 " + _t1o["20"]
     + " at a 0.20 m offset, " + _t1o["28"] + " at 0.28 m), so both offsets are reported")

# Finding (Table IV, office-desk serving row): T2 denominator 48 above the 43 attempted -- the link log keeps episodes the payload log lacks
_svo = V["sv_surf"]["office"]
if int(_svo["T2"].split("/")[1]) > int(_svo["att"]):
    _rn2("| serving beside the person, office desk | 43 / 26 / 17 | exercised | T2 6 (3/48) |",
         "| serving beside the person, office desk | " + _svo["att"] + " / " + _svo["car"] + " / " + _svo["dl"] + " | exercised | T2 " + _svo["T2_pct"]
         + " (" + _svo["T2"] + ": T2 reads every episode's link log, and " + str(int(_svo["T2"].split("/")[1]) - int(_svo["att"])) + " of the "
         + _svo["T2"].split("/")[1] + " episodes have no payload record) |")

# Finding (Appendix B, T4 heading): 'null on ... π0.5's mug' although 78/996 pass 45° -- the comparison is the placement-matched one of Table IIIf
_t4m = V["t4_thr_matched"]["pi05"]["45"]
_rn2("— *measured (null on GR00T's rigid box and π0.5's mug; GR00T N1.6-DROID tilts it)*",
     "— *measured (null on GR00T's rigid box; π0.5's mug past 45° on " + V["pi_T4_pct"] + " %, no detectable difference from the placement-matched control, p = "
     + ("%.2f" % _t4m["p"]) + "; GR00T N1.6-DROID's on " + V["t4task_g0_pct"] + " %, above it, p = "
     + ("%.3f" % V["t4_thr_matched"]["gr00t_droid"]["45"]["p"]) + "; Table IIIf)*")

# Finding (Appendix B, T5 grounding): only the 6 matched carries were given; the scored G1 T5a also holds the 16 of the Sec. 5.1 person cell
_rn2("— 6/6 completing carries pass the person at full speed inside the stop distance;",
     "— " + _g1_t5a + " completing carries (6 matched, " + str(_t5a_more) + " on the §5.1 person cell) pass the person at full speed inside the stop distance;")
# same finding: E.6's envelope paragraph
_rn2("(Wilson 95 % CI 61–100 %); the conclusion survives",
     "(Wilson 95 % CI 61–100 %; with the " + str(_t5a_more) + "/" + str(_t5a_more) + " completing carries of the §5.1 person cell, " + _g1_t5a
     + ", Wilson " + str(_a175_wlo(_t5a_k, _t5a_k)) + "–100 %); the conclusion survives")

# Finding (Table IV, pitcher row): 1 delivered with 0 carried reads as an error; delivered is defined without a lift
_pt = V["pitcher"]
if int(_pt["delivered"]) > int(_pt["carried"]):
    _rn2("| pick-and-place, pitcher (liquid vessel) | 16 / 0 / 1 |",
         "| pick-and-place, pitcher (liquid vessel) | " + _pt["att"] + " / " + _pt["carried"] + " / " + _pt["delivered"] + " (ends within 10 cm of the bowl without a lift) |")

# Finding (Appendix B, T6 fixability): 0/12 with force (floor-standing rerun) and 22/24 firings (raised-capsule run) joined as one run
_rn2("a protective stop at the 0.50 m SSM distance does (0/12 carried encounters with force), firing on 22/24 episodes (§5.4).",
     "a protective stop at 0.50 m does: 0/12 carried encounters with force on the floor-standing rerun (the earlier raised-capsule run fired on 22/24 episodes, with 0/11 carried episodes reaching contact; Appendix E.7).")

# Finding (Table VI, 'Our proxy' column): T3 and T4 proxies list only the G1 box
_rn2("| box long axis as the hazardous axis, 90° criterion |",
     "| box long axis (G1); scissors blade tip, fork tines (tabletop); 90° criterion |")
_rn2("| rigid-box tilt (null); filled-cup test proposed |",
     "| rigid-box tilt (G1, null); mug-axis tilt over the transport, 45° with the 14–27° spill angle alongside (tabletop) |")

# Finding (Appendix B, T2): 0.10 m attributed to the standard as its Z (Appendix D: our value, no standard fixes it); 0.48 m is several times, not an order of magnitude
_rn2("The 0.10 m is ISO/TS 15066's position-uncertainty allowance $Z$, *not* a protective separation: the separation the standard would require for an approaching arm is an order of magnitude larger",
     "The 0.10 m is the value we adopt for the uncertainty allowance $Z$ in the ISO/TS 15066 formula (no standard fixes one), *not* a protective separation: the separation the standard would require for an approaching arm is several times larger")
_rn2("the robot's own body comes closer to a person than the standard's own uncertainty budget",
     "the robot's own body comes closer to a person than that uncertainty allowance")

# Finding (E.7, human-mesh crosser): 'the person's appearance changes nothing' from one untested cell without a collider
_rn2("on the humanoid too, the person's appearance changes nothing, as the capsule, the mesh and the unrendered bystander agreed at the table (Appendix E.8).",
     "on the humanoid too the mesh is reached as the capsule was, though without a collider the two cells are not directly comparable (at the table the capsule, the mesh and the unrendered bystander show no detectable difference, Appendix E.8).")
