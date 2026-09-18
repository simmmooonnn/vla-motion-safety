# -*- coding: utf-8 -*-
# Page budget, fourth pass: micro-trims so the conclusion ends on page 10. Exec'd after a52 (uses t, RN).
RN(" Table IIIb gives every count with its Wilson interval.", "")
RN(" — the null SafeManip's prompt ablation also reports on GR00T [30]", " (as SafeManip reports on GR00T [30])")
_p = t.find("Six sub-types were fixed before any tabletop cell ran;")
if _p >= 0:
    _e = t.find("settled.", _p) + len("settled.")
    t = t[:_p] + ("Six sub-types were fixed before any tabletop cell ran; T5c was added on 2026-09-17 after the tool-use cells and stays "
                  "outside the speed-and-force score until its sensitivity is settled (Appendix E.8).") + t[_e:]
RN("VLA safety asks whether a task should be done and whether it ended well, not whether it was done *safely* in between. We defined that \"how\" as a third axis, decomposed it into four parallel dimensions of a motion — where it goes, how its payload is oriented, how fast and hard it meets a person, and whether it reacts — and built a benchmark that scores each policy on each. Across two embodiments and four policies the profile recurs — keep-outs crossed, orientation frozen, no slowing, no avoidance of a moving body — and differs where the embodiment does; a command changes whether they finish, a rendered hazard pulls the path closer, and neither changes how. What a policy owns is not the safety function but the demand it places on it — now measurable along each dimension.",
   "VLA safety asks whether a task should be done and whether it ended well, not whether it was done *safely* in between. We defined that \"how\" as a third axis with four dimensions — where a motion goes, how its payload is oriented, how fast and hard it meets a person, whether it reacts — and a benchmark that scores each policy on each. Across two embodiments and four policies the profile recurs and differs where the embodiment does; a command changes whether they finish, a rendered hazard pulls the path closer, and neither changes how. What a policy owns is not the safety function but the demand it places on it — now measurable along each dimension.")
