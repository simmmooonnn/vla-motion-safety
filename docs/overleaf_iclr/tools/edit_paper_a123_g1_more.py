# -*- coding: utf-8 -*-
# G1 corridor family on chaowei (2026-09-28): two more seeds of the crossing person with the contact sensor (carried 8, reached 6/8,
# force on 7/8, above 110 N on 5/8, no deceleration on 6/7), pooled into the G1 row (T6 21/24, T5b 15/21, T6b 17/18); and the
# walking-speed approach probe (the person walks toward the robot on the path at 0.6 m/s and stops in front of it): 5 carried of 24,
# reached 3/5, peaks 170-204 N, no deceleration 4/4 -- under the floor, reported as a probe. Exec'd after a122 (uses t, RN, V).
RN("On every completing on-path carry in three seeds (11/11), and 4/5 carried episodes of a replicate, the payload reaches the person",
   "On every completing on-path carry in three seeds (11/11), 4/5 carried episodes of a replicate and 6/8 of two further seeds, "
   "the payload reaches the person")
# the walking-speed approach probe goes to Appendix E.7 (page budget), in front of the 2026-09 controls block
_ctl = "**Controls (2026-09 round; 12 episodes per cell, seed 42, one GR00T server).**"
if _ctl in t:
    RN(_ctl, "**Walking-speed approach (2026-09-28 probe).** A person who walks toward the robot on its path at 0.6 m/s once the base has "
             "passed the trigger line, 0.50 m, and then stands in front of it — the tabletop's approach-and-stop cell on the humanoid — "
             "is reached on 3/5 carried episodes over 24 attempts (two seeds), with contact peaks of 170–204 N and no deceleration before the "
             "encounter on 4/4 scored carries; the pick succeeds too rarely in this cell for a score, so it is reported as a probe." + chr(10) + chr(10) + _ctl)
if "T6 *n* = 11;" in t:
    RN("T6 *n* = 11;", "T6 *n* = 18;")

# page budget after the G1 additions: five clauses in sections 5.4 / 5.6 tightened (RNI = only if present)
def _rni(a, b):
    if a in t:
        RN(a, b)
_rni("A protective stop at the 0.50 m separation implied by the crossing speed prevents the payload contact (0/11 carried; 0/13 with force) "
     "— the scene's witness — and fires on 22/24 episodes, the demand on the layer (Appendix E.7).",
     "A protective stop at 0.50 m prevents the contact (0/11 carried, 0/13 with force) and fires on 22/24 episodes: the scene's witness "
     "and the layer's demand (Appendix E.7).")
_rni("holding it there for at least 5 s (5.3–23.5 s) in 16/83;", "holding it ≥ 5 s in 16/83;")
_rni("The count is partly scene-set (no 1.9 m traversal stays outside $d_0$), so the policy-attributable finding is the absence of slowing.",
     "The count is partly scene-set (no 1.9 m traversal stays outside $d_0$); the policy's own finding is the absence of slowing.")
_rni("A strict speed governor with the 0.60 m shield completes 3/6 carries inside the envelope at every step: the scene admits a "
     "compliant carry (Appendix E.6).",
     "A strict governor with the 0.60 m shield completes 3/6 carries inside the envelope: the scene admits a compliant carry (Appendix E.6).")
_rni("(a walking-speed approach is next-cycle work, §8)", "(a walking-speed approach: Appendix E.7)")
