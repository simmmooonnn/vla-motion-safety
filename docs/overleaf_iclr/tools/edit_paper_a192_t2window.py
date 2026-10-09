# -*- coding: utf-8 -*-
# 2026-10-09 (review round wf_40b97194-223, W1): the link recorder DOES keep a per-step distance trace (link_clearance_traj, 15 Hz);
# the earlier check looked for the wrong key. Appendix C's 'the logs keep only each episode's minimum' is false. Cutting GR00T
# N1.6-DROID's 90 s traces at 35 s gives 44/54 (the pre-registered 35 s rerun: 43/58). The control's episodes mostly run the full
# 35 s (median 525 steps) while the policies end on delivery (median 192 and 210 steps), so the window does not favour the policies;
# their first entries fall at a median 12.2 s and 10.9 s, in the transport and placement. Numbers from the server's link logs
# (_scratch/tmp/t2win.txt, 2026-10-09). Exec'd after a191 (uses t, _rn2).
_rn2("so its arm has a longer window in which to approach the body; the logs keep only each episode's minimum distance, so the "
     "comparison cannot be cut to 35 s afterwards.",
     "so its arm has a longer window in which to approach the body. Cut at 35 s, its logged per-step distances give 44/54 within "
     "the band (the duration check below was frozen on the mistaken belief that they could not be cut).")
_rn2("These cells enter no pool.\n\n**Table XVI.",
     "Episode windows do not favour the policies: the control's episodes mostly run the full 35 s (median 35 s; it carries "
     "on every episode but delivers on 24/64), while π0.5's and π0-FAST's end on delivery (median 12.8 s and 14.0 s), and the "
     "policies first enter the band at a median 12.2 s and 10.9 s, in the transport and placement, not while idling beside the "
     "person. These cells enter no pool.\n\n**Table XVI.")
