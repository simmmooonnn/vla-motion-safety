# -*- coding: utf-8 -*-
# The T2 witness (roadmap N5, queue iksvw, 2026-10-04): the blind straight-line carrier on the serving geometry sets the payload
# down 0.07 m beyond the bowl centre, on the side away from the person, after a vertical descent (SC_AWAY_SHIFT). Written only
# when the cells exist and the witness holds (at most one episode in the 0.10 m band and at least eight deliveries); otherwise
# the "no witness" sentences stay. Exec'd after a152 (uses t, _rn2, V).
_sw = V.get("ik_svw")
_ok = False
if _sw:
    _k, _n = (int(v) for v in _sw["T2"].split("/"))
    _ok = _k <= 1 and int(_sw["delivered"]) >= 8
if _ok:
    _desc = (_sw["T2"] + " in the band, " + _sw["delivered"] + "/" + _sw["att"] + " delivered")
    _rn2("T2 has a control but no witness (Appendix E.8).", "T2 has a control and a witness (E.8).")      # main text: no room
    _rn2("T2 has **no witness** and does not separate the blind control (§5.1);", "T2 does not separate the blind control (§5.1);")
    _rn2("T2 has no witness, and T4's is the pinch-grasp control.",
         "T2's witness is the straight-line carry set down away from the person, and T4's the pinch-grasp control.")
    _rn2("T2 has no witness and its rate is partly set by the scoring geometry;",
         "T2's witness is a straight-line carry set down away from the person (" + _desc + ") and its rate is partly set by the "
         "scoring geometry;")
    _rn2("π0 does not come closer (" + V["p0_T2"] + ").",
         "π0 does not come closer (" + V["p0_T2"] + "). **The T2 witness.** The blind straight-line carrier on the same serving "
         "geometry sweeps the body on " + _sw["T2_noshift"] + " episodes; set down 0.07 m beyond the bowl centre on the side away "
         "from the person, after a vertical descent from carry height, it enters the band on " + _sw["T2"] + " (contact on "
         + _sw["contact"] + ") and delivers " + _sw["delivered"] + "/" + _sw["att"] + " (" + _sw["delivered_noshift"] + "/"
         + _sw["att_noshift"] + " without the shift; " + _sw["cells"] + " cells, mug and scissors). A carry that serves the bowl "
         "without sweeping the person exists in this scene, so the policies' rate is theirs and not the geometry's alone.")
