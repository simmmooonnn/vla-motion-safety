# -*- coding: utf-8 -*-
# Checkpoint lineage (2026-10-04 review: analyst + verifier, public GCS metadata, the PolaRiS README and paper, the GR00T
# card). The tabletop rows do not share one training corpus: pi0.5 loads openpi's base DROID joint-position checkpoint
# (gs://openpi-assets-simeval/pi05_droid_jointpos, every weight shard md5-identical to gs://openpi-assets/checkpoints/
# pi05_droid_jointpos); pi0, pi0-FAST and PaliGemma-binning load the PolaRiS checkpoints (gs://openpi-assets/checkpoints/
# polaris/*_droid_jointpos_polaris), co-trained for 1,000 steps on 90 % DROID and 10 % simulated DROID-platform data. The
# draft said "one corpus read by three decoders". Main text: wording only, length-neutral (p10 has no slack); the full
# statement goes to the Reproducibility Statement and Appendix F, where there is room. Never "DROID alone": pi0.5's own
# pretraining is a multi-source mixture. Exec'd after a148 (uses t, _rn2).

# ---------------- main text
_rn2("π0.5, π0, π0-FAST (openpi; one backbone, two action decoders; a binning decoder does not move the object, Appendix E.8)",
     "π0.5, π0, π0-FAST (openpi; the last two co-trained on 10 % simulated data by PolaRiS; Appendix E.8)")
_rn2("the openpi decoders sweep the body about as often as the blind carrier does",
     "the openpi policies sweep the body about as often as the blind carrier does")
_rn2("and, on the body sweep, where the *decoder* does: the humanoid sweeps its body into bystanders on",
     "and, on the body sweep, where the *policy* does: the humanoid sweeps its body into bystanders on")
_rn2("of episodes and the GR00T decoder's arm on", "of episodes and GR00T N1.6-DROID's arm on")
_rn2("(the openpi decoders tilt no more often than the pinch-grasp control)",
     "(the openpi policies tilt no more often than the pinch-grasp control)")
_rn2("five policies, four of them one corpus read by three decoders, and differs where the embodiment does.",
     "five policies, four of them public DROID checkpoints, and differs where the embodiment does.")

# ---------------- Appendix E.8
_rn2("for the openpi decoders T2 does not distinguish a policy", "for the openpi policies T2 does not distinguish a policy")
_rn2("so on this predicate the decoders diverge where §5.5 finds them recurring",
     "so on this predicate the policies diverge where §5.5 finds them recurring")
_rn2("is produced at the table by this decoder's arm and by no other.", "is produced at the table by this policy's arm and by no other.")
_rn2("The decoders trained on one dataset agree with each other and with GR00T N1.6-DROID, whose backbone and decoder both "
     "differ: the drift is learned from the demonstrations, not added by any one action head.",
     "The two openpi policies agree with each other although only one was co-trained on simulated data, and both agree with "
     "GR00T N1.6-DROID, whose backbone, decoder and training mixture differ: the drift is common to these DROID policies and "
     "is not added by one action head or by the simulated co-training.")

# ---------------- Reproducibility Statement
_rn2("The policies are the public GR00T N1.6 G1 loco-manipulation checkpoint [13] and the public π0.5 and π0 openpi "
     "checkpoints for the Franka/DROID joint-position configuration and the public GR00T N1.6-DROID checkpoint, run "
     "unmodified behind IsaacLab-Arena's policy runner [15];",
     "The policies are public checkpoints run unmodified behind IsaacLab-Arena's policy runner [15]: on the G1, the GR00T "
     "N1.6 loco-manipulation checkpoint fine-tuned on simulated demonstrations of this box carry [13]; on the Franka, served "
     "by openpi, π0.5 from gs://openpi-assets-simeval/pi05_droid_jointpos (every weight shard identical to openpi's base "
     "DROID joint-position checkpoint gs://openpi-assets/checkpoints/pi05_droid_jointpos), and π0, π0-FAST and "
     "PaliGemma-binning from gs://openpi-assets/checkpoints/polaris/{pi0,pi0_fast,paligemma_binning}_droid_jointpos_polaris, "
     "which PolaRiS (arXiv 2512.16881) co-trained for 1,000 steps on 90 % DROID and 10 % simulated DROID-platform data; and "
     "nvidia/GR00T-N1.6-DROID, a DROID fine-tune of GR00T N1.6-3B. A policy row is one checkpoint: any two rows differ in "
     "more than one of backbone, action decoder, pretraining and fine-tuning data, so we report differences between rows "
     "without attributing them to any one of these, and compare each row with the scripted straight line, which loads no "
     "checkpoint;")

# ---------------- Appendix F
_rn2("Table III is narrower than the suite, and the gap is now specific.",
     "**The tabletop rows do not share a training corpus.** π0.5 is openpi's base DROID joint-position checkpoint, without "
     "the PolaRiS simulated co-training; π0, π0-FAST and PaliGemma-binning are the PolaRiS checkpoints, co-trained for 1,000 "
     "steps on 90 % DROID and 10 % simulated data; GR00T N1.6-DROID fine-tunes a base model pretrained partly on synthetic "
     "data; and the G1 policy is fine-tuned only on simulated demonstrations of its own task and room. We therefore report "
     "differences between rows without attributing them to the action decoder, and claim only the recurrence of the "
     "profile, each row's separation from the blind straight line, and within-policy contrasts. A π0.5 PolaRiS twin would "
     "show whether the simulated co-training changes the profile; it would not isolate the decoder.\n\n"
     "Table III is narrower than the suite, and the gap is now specific.")
