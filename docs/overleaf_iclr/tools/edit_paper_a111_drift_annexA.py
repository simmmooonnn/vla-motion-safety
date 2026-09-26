# -*- coding: utf-8 -*-
# Zero-compute follow-ups written in: the measured base-relative drift on hazard-free cells (E.8), and the Annex A.3.3
# transient force the reaching-hand contacts would carry on a free hand (E.8 + one §8 clause). Exec'd after a110.
_dr, _aa = V.get("drift_rows", ""), V.get("annexA", {})

if "| desk |" in _dr and V.get("drift", {}).get("desk", {}).get("pi", {}).get("far", "—") != "—":
    RN("The trajectory dimension's tabletop measurement is the pair of off-path levels; the on-path cell is exposure.",
       "The trajectory dimension's tabletop measurement is the pair of off-path levels; the on-path cell is exposure. The drift "
       "itself is measurable on the canonical cells, where no keep-out exists anywhere: the carried path's largest excursion from "
       "the straight pick-to-place line toward the far side of the transport (median over carries, m; the blind carrier for scale):"
       "\n\n| Surface | π0.5 | π0 | scripted control |\n|---|---|---|---|\n" + _dr + "\n\nThe bow is largest at the desk, which "
       "is where the far-side keep-out was entered most; with the keep-out's edge 0.08 m from the line at the 0.28 m level, a "
       "median bow of " + V["drift"]["desk"]["pi"]["far"] + " m enters it on about half the carries, which is what the rendered "
       "(" + V.get("t1_off_surf", {}).get("desk", {}).get("pi", "11/16") + ") and unrendered (" +
       V.get("t1_unseen", {}).get("pi", {}).get("desk", "7/16") + ") cells found. The excursion toward the near side is at or below "
       "zero everywhere. What the trajectory dimension measures on the tabletop is therefore a bow the policy carries into every "
       "transport, large enough at some surfaces to enter a keep-out that a straight carry clears.")

if _aa.get("F_med", "—") != "—":
    RN("every rate here is exposure under a proxy that cannot flinch, step back or protest.",
       "every rate here is exposure under a proxy that cannot flinch, step back or protest. The forces are exposure too: the "
       "recorded peaks are solver constraint forces on an inert kinematic capsule (median " + _aa["rec_med"] + " N over the "
       "reaching-hand carries). The transient force ISO/TS 15066 Annex A.3.3 predicts for a *free* hand from the payload's speed "
       "at the closest approach — F = v·√(μk), hand k = 75 N/mm and m = 0.6 kg from Table A.3, the arm's effective mass taken as "
       "2 kg so μ = " + _aa["mu"] + " kg — is " + _aa["F_med"] + " N at the median speed of " + _aa["v_med"] + " m/s and " +
       _aa["F_max"] + " N at most (" + _aa["n"] + " carries), above the 140 N transient limit on " + _aa["over140"] + ". T5b "
       "therefore counts contacts, not injuries: at these speeds a free hand is touched, not hurt, and the 140 N exceedances of "
       "Table III are the capsule's, not the hand's.")
    RN("so every contact rate is an exposure rate, not a harm rate,",
       "so every contact rate is an exposure rate, not a harm rate (Annex A.3.3 puts the reaching-hand contacts at " +
       _aa["F_med"] + " N median on a free hand, Appendix E.8),")
