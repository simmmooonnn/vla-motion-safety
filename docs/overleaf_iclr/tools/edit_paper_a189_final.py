# -*- coding: utf-8 -*-
# Final check (workflow wf_0d582743-281: 3 lenses + skeptics, 27 confirmed). Sources were fixed for the figure captions, the
# forest panel, the generator (min rule, design-effect stars) and the a187 date; these are the remaining exact replacements.
# Exec'd after a188 (uses t).
_A189 = [
    ('numbers-table3-control-t2-exposure', 'its T2 comes from bowl-away cells (serving cell: 0/64, §5.1).', "its T2 pools its bowl-away cells (3/456), which score no policy's T2 (§5.1), because its serving cells (0/64, §5.1) enter no pool; scored on 0/64 its trajectory score is still 6."),
    ('consistency-bowlaway-exposure', 'With the bowl away from the body no link need approach it and the rate floors at 3/605, so those cells are exposure.', "With the bowl away from the body no link need approach it and the rate floors at 3/605, so those cells score no policy's T2."),
    ('consistency-appF-witness', 'T2 (the set-down-away carry, one placement)', 'T2 (the straight line on one serving placement, unshifted or set down away)'),
    ('consistency-cone-matched', 'On the eight placements π0.5 shares with that carrier (14 cell-seeds) the rates are 50/74 against 66/112 at 90°', "On the eight placements π0.5 shares with that carrier, restricted to the 14 cell-seeds both ran (Table IIIf's 79/128 also counts the carrier's two cells without a π0.5 twin), the rates are 50/74 against 66/112 at 90°"),
    ('prose-51-commasplice', 'the control never brings a link within 0.10 m of the body (0/64), π0.5 does on 26/60 episodes', 'the control never brings a link within 0.10 m of the body (0/64); π0.5 does on 26/60 episodes'),
    ('prose-51-heading-overclaim', '**Against the control, the arms sweep the person.**', "**Against the control, π0.5's and π0-FAST's arms sweep the person.**"),
    ('prose-55-humanoid-embodiment', "the humanoid sweeps its body into bystanders on 84 % of episodes, GR00T N1.6-DROID's arm on 78 % of person-side serving episodes and π0's on 2 %", "GR00T N1.6-DROID's arm sweeps the body on 78 % of person-side serving episodes and π0's on 2 % (the humanoid, in its own scene, on 84 %)"),
    ('prose-52-their-pose', 'Turning their initial pose by 180°', "Turning the scissors' initial pose by 180°"),
    ('prose-e8-witness-comma', 'on the side away from the person it also stays out of the band', 'on the side away from the person, it also stays out of the band'),
    ('prose-e8-intervals-comma', "lie above the control's [0, 6] and π0's ([0, 8]) overlaps it", "lie above the control's [0, 6], and π0's ([0, 8]) overlaps it"),
    ('prose-appD-tables-list', "(except the control's T2 in Tables III and IVe:", "(except the control's T2 in Tables III, IIIb and IVe:"),
    ('prose-F-its-rate', '(0/32, 26/32 delivered) and its rate is partly set by the scoring geometry', "(0/32, 26/32 delivered), and T2's rate is partly set by the scoring geometry")
]
for _id, _old, _new in _A189:
    if t.count(_old) == 1:
        t = t.replace(_old, _new)
    elif _new not in t:
        print("  [a189 MISS x%d] %s" % (t.count(_old), _id))
