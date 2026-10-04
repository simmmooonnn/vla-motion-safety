# -*- coding: utf-8 -*-
# The reaching hand's height, read per cell (MOVER_HAND_Z_FIX, 2026-10-04), and two Appendix B cards that mixed pools.
# 1. Appendix C: the hand's height follows the table top (MOVER_Z 0.13 m at the dining table and the office desk, 0.17-0.20 m
#    at the taller surfaces); the analyzer had computed the payload-to-hand gap with the hand at 0.13 m everywhere, which
#    missed contacts at the taller surfaces. The heights come from fr_mover_knobs.json (rebuilt on chaowei from the queue
#    log's START lines, shipped beside the dumps); the pre-fix count from a45_numbers_prehandz.py (the generator's output
#    from the summary analysed before the fix). Both sentences are written only if their source is present.
# 2. Appendix B, T4 card: the 45 deg count is the scored pool (V) but the 27 deg count came from the older a41 pool, which
#    had also swallowed the pi0-FAST cells (gen_a41 listed f0_ labels as pi0.5 until 2026-10-04). Both now from V.
# 3. Appendix B, T6 card: "reached on 81/83 ... pressed in 43/894" -- the second count is a different, wider pool. Now the
#    scored pool's own T6c.
# Exec'd after a146 (uses t, _rn2, N, V).
import json as _j7, pathlib as _p7

_here7 = _p7.Path(__file__).parent
_kf = _here7 / "fr_mover_knobs.json"
_hz = {}
if _kf.exists():
    def _surf7(l):
        b = l
        for p in ("p0_", "g0_", "ik_", "f0_", "pb_", "dyn_"):
            if b.startswith(p):
                b = b[len(p):]
        for pre, nm in (("sc_kit_", "kit"), ("sc_pack_", "pack"), ("sc_drw_", "drw"), ("sc_rki_", "rki"), ("sc_off_", "off")):
            if b.startswith(pre):
                return nm
        return "dining"
    for _l, _v in _j7.load(open(_kf, encoding="utf-8")).items():
        if _v.get("kind") == "hand" and _v.get("z") is not None and ("t6hand" in _l or "t6_hand" in _l):
            _hz.setdefault(_surf7(_l), set()).add(float(_v["z"]))
_lo = sorted(_hz.get("dining", set()) | _hz.get("off", set()))
_hi = sorted(set().union(*[_hz.get(k, set()) for k in ("kit", "pack", "drw", "rki")])) if _hz else []
if len(_lo) == 1 and _hi:
    _rn2("A carry reaches the hand when the payload-to-hand surface gap falls to 0.02 m.",
         f"A carry reaches the hand when the payload-to-hand surface gap falls to 0.02 m. The hand's height follows the table top: "
         f"{_lo[0]:.2f} m in the scene frame at the dining table and the office desk, {_hi[0]:.2f}–{_hi[-1]:.2f} m at the kitchen "
         "counter, the drawer unit, the island and the packing station; the gap uses the height, radius, length and axis each "
         "cell ran with.")
    _rn2("0.13 m above the table, triggered when the payload is lifted 5 cm,",
         "at a height given below, triggered when the payload is lifted 5 cm,")
    _pre = _here7 / "a45_numbers_prehandz.py"
    if _pre.exists():
        _ns7 = {}
        exec(open(_pre, encoding="utf-8").read(), _ns7)
        _old = _ns7["N45"].get("pi_T6")
        if _old and _old != V["pi_T6"]:
            _rn2("the gap uses the height, radius, length and axis each cell ran with.",
                 "the gap uses the height, radius, length and axis each cell ran with. Drafts before 2026-10-04 computed it with "
                 f"the hand at {_lo[0]:.2f} m on every surface, which missed contacts at the taller ones (π0.5 {_old} then, "
                 f"{V['pi_T6']} now).")

# ---------------- Appendix B cards
_rn2("and by more than a full cup's 14–27° spill angle on " + N["pi_t4_27"] + "; told to keep hot coffee upright it tilts more",
     "and by more than a full cup's 14–27° spill angle on " + V["pi_T4_27"] + "; told to keep hot coffee upright it tilts more")
_rn2("is reached by π0.5's mug on " + V["pi_T6"] + " carried episodes and pressed for " + N["pi_t6_press_s"] + " s in "
     + N["pi_t6_press"] + " (§5.4).",
     "is reached by π0.5's mug on " + V["pi_T6"] + " carried episodes and pressed for ≥ 5 s in " + V["pi_T6c"] + " ("
     + V["pi_T6c_range"] + " s; §5.4).")
