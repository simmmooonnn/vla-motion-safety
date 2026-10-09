# -*- coding: utf-8 -*-
# Cross-region consistency fixes after the a193 rewrite (workflow wf_d65792df-931: 2 lenses + skeptics, 18 confirmed, appx-1
# duplicates main-1). Exact replacements, each checked to occur once. Exec'd after a193_appEF (uses t).
_A194 = [
    ('main-1', 'and the T4 and three small T3 control comparisons are untested', 'and three T4 and three small T3 control comparisons are untested'),
    ('main-2', 'against 70 % for a person-blind carry read at the same moment', 'against 70 % without a passer-by, read at the same moment'),
    ('main-3', 'where a policy rarely delivers, its T2 measures competence, not safety', 'where a policy rarely delivers, a low T2 measures competence, not safety'),
    ('main-5', 'body the rate floors at 3/605, and those cells score no T2', "body π0.5's rate floors at 3/605, and those cells score no T2"),
    ('main-6', 'mainly late in transport', 'mainly near the bowl'),
    ('main-7', 'so no naming effect on the rate is established.', 'so no naming effect on the rate is established, and naming no longer detectably moves the hidden-stove path (*p* = 0.49).'),
    ('main-8', 'naming moves a hidden-hazard path 3 cm away (E.2)', 'naming moved a hidden-hazard path 3 cm away on two seeds but not on two new ones (E.2)'),
    ('main-9', "though not the desk's 0.28 m keep-out (π0.5 11/16)", 'though no 0.28 m keep-out (π0.5 12/64; desk 11/16)'),
    ('main-4', '(cut at 35 s: T1 8/9, T4 18/57; C).', "(cut at 35 s: T1 8/9, T4 18/57; C); π0's T2 reflects competence (§5.5)."),
    ('main-12', '(delivered: 26/56, 32/56, 14/14 against 0/24)', '(delivered, post hoc: 26/56, 32/56, 14/14 against 0/24)'),
    ('main-10', "F gives the witnesses, corrected errors and Annex A's meaning for bystanders", "F gives the witnesses, corrected errors and ISO/TS 15066 Annex A's meaning for bystanders"),
    ('main-11', 'the 0.30 m delivery criterion (§4.2)', 'the 0.30 m completion criterion (§4.2)'),
    ('appx-4', 'with the smallest attainable p added as "min" when it is above 0.01', 'with the p a policy with no violations would get against the control\'s cells added as "min" on the three small T3 rows (Table XVII)'),
    ('appx-3', "Since every T1 transport runs the same way, these data cannot tell a bend fixed to the robot's base from one fixed to the direction of travel.", "Since every T1 transport runs parallel to the y axis on the +x side of the base, these data cannot tell a bend fixed to the robot's base from one fixed to the world; reversing the transport keeps it on the same side (E.8), so the direction of travel does not set its side."),
    ('appx-2', "π0's zero is a capability boundary, since", "π0's zero is a competence limit, since"),
    ('appx-5', 'the reaching hand (exposure) is reached on 10/11 carried episodes and touched on 3/9', 'the crossing hand is reached on 10/11 scored carries and the reaching hand (exposure) touched on 3/9'),
    ('appx-6', 'stays a capability boundary (45/112 carried, 4 delivered)', 'stays *carried, not delivered* (45/112 carried, 4 delivered)')
]
for _id, _old, _new in _A194:
    if t.count(_old) == 1:
        t = t.replace(_old, _new)
    elif _new not in t:
        print("  [a194 MISS x%d] %s" % (t.count(_old), _id))
