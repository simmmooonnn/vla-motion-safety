# -*- coding: utf-8 -*-
# R6's loose end: the serving cells now carry the scored T2, but Appendix E.8 still introduced them as "a second tabletop
# task" in the battery and Table IV reports the dining-table subset at a higher rate than Table III's pooled figure. Say
# which is which, so the two numbers do not look like a contradiction. Appendix only.
# Exec'd after a130 (uses t, RN, V, _rn2).

_rn2("**A second tabletop task: serving.** With the bowl at the table edge beside the adult (0.32 m from their axis), so "
     "that the object is delivered toward them,",
     "**The serving geometry, which carries the scored T2.** With the bowl at the table edge beside the adult (0.32 m "
     "from their axis), so that the object is delivered toward them — the placement at which a link must enter the "
     "0.10 m band to finish the task, and therefore the pool Table III's T2 is taken over (§5.1) —")

_rn2("the mug leaves upright by more than 45° on 45/62; the approach passes inside the stop distance on 125/126.",
     "the mug leaves upright by more than 45° on 45/62; the approach passes inside the stop distance on 125/126. These "
     "are the dining-table cells alone, which is why Table IV's serving row reads " + V["sv_T2_pct"] + " % where Table "
     "III reads " + V["t2sv_pi_pct"] + " %: the scored pool is the whole serving family, " + V["t2sv_pi_cells"] + " cells "
     "across " + _word(V["t2sv_pi_surf"]) + " work surfaces and three person poses, and the rate at the dining table is the "
     "highest of them.")

_rn2("**Table IIIb. The same measurements by sub-type: unsafe / scored, rate and Wilson 95 % interval.** Below the floor "
     "of eight episodes a count only.",
     "**Table IIIb. The same measurements by sub-type: unsafe / scored, rate and interval (cluster-robust by cell; a star "
     "marks a design effect above 1.5).** Below the floor of eight episodes a count only. On the tabletop T1 is the "
     "off-path keep-out and T2 the serving geometry (§5.1).")
