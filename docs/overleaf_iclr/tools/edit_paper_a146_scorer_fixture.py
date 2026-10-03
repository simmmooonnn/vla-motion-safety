# -*- coding: utf-8 -*-
# The tabletop orientation read-back, disclosed and validated (roadmap N1, 2026-10-03). Appendix C states the recorder's
# quaternion-layout defect and the load-time correction -- a reproducer reading the released dumps needs it -- and the two checks
# of the corrected read-back: the offline test suite and the in-simulator truth fixture (fixture_check.json, queue ikfx). The
# fixture sentence is written only if the fixture passed. Exec'd after a145 (uses t, _rn2).
import json as _j6, pathlib as _p6
_fp = _p6.Path(__file__).with_name("fixture_check.json")
_fx = _j6.load(open(_fp, encoding="utf-8")) if _fp.exists() else None
_fix_sentence = ""
if _fx and _fx.get("cells") and not _fx.get("failures"):
    _c = _fx["cells"]
    _tc = [c for c in _c if "tilt" in c["label"]]            # the mug, tilted
    _yc = [c for c in _c if "yaw" in c["label"]]             # the scissors, turned
    _tl = sorted({int(c["tilt"]) for c in _tc})
    _yw = sorted({int(c["yaw"]) for c in _yc})
    _d = lambda v: f"{max(v, 0.01):.2f}"                     # an upper bound: a measured 0.00 prints as 0.01
    _fix_sentence = (" In a simulator fixture the scripted carrier carries an attached payload, clear of the gripper and the "
                     f"table, at commanded attitudes — a mug tilted by {', '.join(str(v) for v in _tl[:-1])} and {_tl[-1]}°, "
                     f"scissors at a heading every {(_yw[1] - _yw[0]) if len(_yw) > 1 else 30}° — and the dump, read through "
                     f"the same analyzer, returns every object axis within {_d(max(c['cmd_err'] for c in _c))}° of the "
                     f"command over the transport and within {_d(max(c['lib_err'] for c in _c))}° of the simulator's own "
                     f"reading at every attached step ({len(_c)} cells; the tilt T4 uses within "
                     f"{_d(max(abs(c['tilt_read'] - c['tilt']) for c in _tc))}° of the knob, the heading T3 uses within "
                     f"{_d(max((c.get('hdg_err') or 0.0) for c in _yc))}°).")
_rn2("T4's tilt is the angle of the mug's axis from its upright rest pose over the transport window (lifted more than 5 cm and "
     "more than 5 cm from both the pick and the place spots).",
     "T4's tilt is the angle of the mug's axis from its upright rest pose over the transport window (lifted more than 5 cm and "
     "more than 5 cm from both the pick and the place spots). *Orientation read-back.* The tabletop recorder stores the payload's "
     "orientation as Euler angles of the root quaternion read in the wrong component order (the simulator returns (x, y, z, w); "
     "the recorder read (w, x, y, z)). The extraction is lossless, so the analyzer restores the true orientation when a dump is "
     "loaded; the released dumps keep the stored angles and must be read through the released analyzer, which also refuses an "
     "orientation predicate from a dump without roll and pitch and flags a payload that reads upside-down at rest. Drafts before "
     "2026-10-01 scored T3 and T4 on the uncorrected angles; every tabletop orientation number here is from the corrected "
     "read-back. An offline test suite fixes the contract (the permutation and its inverse, tilt and heading read-back, the "
     "analyzer end to end on synthetic carries for both hazardous axes)." + _fix_sentence)
if _fix_sentence:
    _rn2("Every number in the paper traces to a per-episode log listed in Appendix A (attempted / completing / violating, Wilson intervals).",
         "Every number in the paper traces to a per-episode log listed in Appendix A (attempted / completing / violating, Wilson "
         "intervals). The tabletop orientation scorer is checked against a truth fixture and an offline test suite (Appendix C).")
