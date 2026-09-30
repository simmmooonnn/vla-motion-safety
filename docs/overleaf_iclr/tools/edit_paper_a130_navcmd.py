# -*- coding: utf-8 -*-
# Round-4 item R7: the navigate_cmd readout Appendix E.1 names as the clean test has been run. GR00T's base command is a
# live output that varies episode to episode, and it varies no more with the bystander present or absent than between two
# episodes of one condition -- including over the steps where the person is closest. That closes both open alternatives:
# a memorised route (the command is not a replay) and a tracker that flattens an avoidance GR00T commands (the
# insensitivity is in the command, before the tracker).
# Exec'd after a129 (uses t, RN, V, _rn2).
_NV = V["nav"]

# ---------------- Appendix E.1: replace the flagged caveat with the measurement
_rn2("One caveat bounds the mechanism: what we measure is the *realized* base path (GR00T's command **as executed by** "
     "the language/vision-blind tracker), so while the tracker cannot *introduce* the observed insensitivity, we do not "
     "separately exclude a tracker that *flattens* an avoidance GR00T commands; logging the raw `navigate_cmd` "
     "distribution across conditions would fully isolate the command, and we flag that readout as the clean test of the "
     "\"GR00T-level competence\" reading (the weaker \"prompting does not fix it / an external layer does\" conclusion of "
     "§6 holds regardless).",
     "Earlier drafts bounded the mechanism with a caveat: what we measured was the *realized* base path, GR00T's command "
     "**as executed by** the language- and vision-blind tracker, so while the tracker cannot *introduce* the observed "
     "insensitivity, a tracker that *flattens* an avoidance GR00T commands was not excluded. **That readout has now been "
     "taken.** One JSON line per control step is written where the action term slices the navigation command out of the "
     "incoming policy action, in " + _NV["runs"] + " runs of " + _NV["eps"] + " episodes — the bystander present and "
     "absent, seeds 42 and 7, " + _NV["steps"] + " steps in all. Three facts follow. *The command is a live output, not a "
     "replay*: it is non-zero at every step (forward " + _NV["vx"] + " m/s, s.d. " + _NV["vx_sd"] + "; yaw "
     + _NV["wz"] + " rad/s, s.d. " + _NV["wz_sd"] + "), and two episodes of the *same* run differ by a median "
     + _NV["B_med"] + " on the largest-channel absolute difference, so the same command sequence every episode is ruled "
     "out. *Removing the bystander changes it no more than re-running the same condition*: matched by episode index and "
     "aligned from each episode's first step, the person-versus-absent difference is a median " + _NV["A_med"] + " over "
     + _NV["A_n"] + " episode pairs against that same-condition floor of " + _NV["B_med"] + " over " + _NV["B_n"] + " "
     "pairs (Mann-Whitney *U* = " + _NV["U"] + ", *z* = " + _NV["z"] + ", *p* = " + _NV["p"] + ") — if anything smaller "
     "than the floor. *Nor does the difference appear at closest approach*: the bystander stands beside the middle of the "
     "transport, so the carried box stays within " + _NV["dmin"] + "–" + _NV["dmax"] + " m of them throughout and there "
     "is no far band; splitting instead at " + _NV["close_r"] + " m, the person-versus-absent difference over the "
     + _NV["close_n"] + " closest steps is " + _NV["close_btw"] + " against a same-condition floor of "
     + _NV["close_flr"] + ", while over the " + _NV["ends_n"] + " steps beyond " + _NV["ends_r"] + " m it is "
     + _NV["ends_btw"] + " against a floor of " + _NV["ends_flr"] + ". The behavioural outcome agrees: among carries that "
     "completed inside the episode cap the closest robot-to-bystander separation is a median " + _NV["clr_person"] + " m "
     "with the person there (*n* = " + _NV["clr_np"] + ") and " + _NV["clr_absent"] + " m without (*n* = "
     + _NV["clr_na"] + ", *p* = " + _NV["clr_p"] + "), and the episode length is a median " + _NV["len_med"] + " steps "
     "either way. So the base command is GR00T's own, it varies from episode to episode, and the bystander is not one of "
     "the things it varies with. Route memorisation survives only in the form that matters least — the command is no "
     "fixed replay, but nothing in it answers to the person — and the flattening-tracker reading is excluded, since the "
     "insensitivity is already in the command the tracker is handed. The bystander here is static and visible from the "
     "first step, so what the readout shows is that a person standing beside the transport is not an input to the base "
     "command; a person who appears late or who moves could in principle enter a command that this one does not.")

# ---------------- section 6 (iii): the main-text sentence
_rn2("Neither orientation, which no stop can correct, nor speed, which a slowdown would change, is adapted; the yaw "
     "follows the object's initial pose instead.",
     "Neither orientation, which no stop can correct, nor speed, which a slowdown would change, is adapted; the yaw "
     "follows the object's initial pose instead. On the humanoid this now holds of the base command itself: logged step "
     "by step, GR00T's navigation command differs no more between a bystander present and absent than between two "
     "episodes of one condition (median " + _NV["A_med"] + " against " + _NV["B_med"] + ", *p* = " + _NV["p"] + "; E.1).")

# ---------------- page budget for the sentence above
_rn2("Across eight bystander azimuths (*N* = 8 each) GR00T holds a fixed carry yaw (circular mean +3°, s.d. 11°) "
     "whatever the person's position; treating the box's long axis as the hazardous axis, it points into the person's "
     "half-space on 14/27 completing carries — chance — and on 20/20 with the person at the two azimuths the frozen axis "
     "faces (seeds 42 / 7; 11/11 with an explicit command to keep the knife away).",
     "Across eight bystander azimuths (*N* = 8 each) GR00T holds a fixed carry yaw (circular mean +3°, s.d. 11°) "
     "whatever the person's position; treating the box's long axis as the hazardous axis, it points into their "
     "half-space on 14/27 completing carries — chance — and on 20/20 at the two azimuths the frozen axis faces (11/11 "
     "with a command to keep the knife away).")
_rn2("A pedestrian who stops at the first contact receives the same (5/5, median 177 N), and under the protective stop "
     "of §5.4 no carried encounter registers a force (0/13). A tabletop placement is slow: the coworker's hand is "
     "touched on 65/83 carried episodes at peaks up to 260 N,",
     "A pedestrian who stops at first contact receives the same (5/5, median 177 N), and under §5.4's protective stop no "
     "carried encounter registers a force (0/13). A tabletop placement is slow: the hand is touched on 65/83 carried "
     "episodes at peaks up to 260 N,")
_rn2("A **task battery** around it — serving beside the person, a cluttered table, pouring, pushing without a grasp, "
     "tool use (stir, scrape, toss), handover, put-away in a drawer, clearing a table, closing a door, four environment "
     "maps, five further placements — is scored task by task in Table IV (Appendix E.8),",
     "A **task battery** around it — serving beside the person, a cluttered table, pouring, pushing, tool use (stir, "
     "scrape, toss), handover, a drawer, clearing a table, a door, four environment maps, five further placements — is "
     "scored task by task in Table IV (E.8),")
_rn2("and for VLAs the remedy space is being populated (VLSA [22], filters [41]–[44], SPARK on the G1 [40]; the "
     "HRI-safety line [46]–[52]).",
     "and for VLAs the remedy space is being populated (VLSA [22], filters [41]–[44], SPARK on the G1 [40]; HRI safety "
     "[46]–[52]).")
_rn2("On the path this probe is ceiling-limited, so we calibrated a placement with headroom (the stove 0.28 m off the "
     "path, blind rate 37 %) and ran the naming × rendering design: naming changes nothing, rendering changes nothing "
     "(Table XI).",
     "On the path the probe is ceiling-limited, so we calibrated a placement with headroom (the stove 0.28 m off the "
     "path, blind rate 37 %) and ran the naming × rendering design: neither changes anything (Table XI).")
_rn2("The **suite is smaller than its battery** and the matrix narrower still (Appendix F).",
     "The **suite is smaller than its battery**, the matrix narrower still (F).")
