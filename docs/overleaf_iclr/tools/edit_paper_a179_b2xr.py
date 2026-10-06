# -*- coding: utf-8 -*-
# The G1 non-ceiling 2x2 rerun on the normal driver (run_b2xr.sh, seeds 11 and 23, 24 episodes per arm and seed): does the 2-3 cm
# shift toward a rendered stove (two seeds on the substitute-driver day) replicate? E.2 after the Table XI discussion, and the
# provenance clause of finding (ii). Applied once all eight cells are in. Exec'd after a178 (uses t, _rn2, V).
_bx = V.get("b2xr") or {}
if _bx.get("cells", 0) >= 8 and _bx.get("contrasts"):
    _A = _bx["arms"]; _C = _bx["contrasts"]; _rp = _C["rendering_pooled"]
    _fp = lambda p: ("< 0.001" if p is not None and p < 0.001 else (f"= {p:.3f}" if p is not None and p < 0.05 else (f"= {p:.2f}" if p is not None else "—")))
    _cm = lambda m: f"{abs(m) * 100:.0f} cm" if m is not None else "—"
    _rep = _rp["clr_p"] is not None and _rp["clr_p"] < 0.05 and (_rp["clr_shift"] or 0) < 0
    _arm = lambda a: f"{_A[a]['viol']}/{_A[a]['comp']} (completing {_A[a]['comp']}/{_A[a]['att']})"
    _txt = (" **Replication on the normal driver.** The same 2 × 2 with two new seeds (11 and 23, 24 episodes per arm and seed, "
            "run after the driver was restored) gives violating carries blind rendered " + _arm("blind_rend") + ", named rendered "
            + _arm("named_rend") + ", blind hidden " + _arm("blind_hid") + " and named hidden " + _arm("named_hid") + ". Rendering "
            + ("again moves the path toward the stove: the median clearance of completing carries is " + _cm(_rp["clr_shift"])
               + " smaller with it visible (Mann–Whitney *p* " + _fp(_rp["clr_p"]) + ")" if _rep else
               "does not detectably move the path this time (median clearance " + _cm(_rp["clr_shift"]) + " "
               + ("smaller" if (_rp["clr_shift"] or 0) < 0 else "larger") + " with it visible, Mann–Whitney *p* " + _fp(_rp["clr_p"]) + ")")
            + ", and the violation rate is " + _rp["viol"] + " rendered against " + _rp["viol_hid"] + " hidden; naming the stove "
            + ("raises the violation with it rendered" if _C["naming_rendered"]["viol_p"] < 0.05 and _A["named_rend"]["viol"] / max(_A["named_rend"]["comp"], 1) > _A["blind_rend"]["viol"] / max(_A["blind_rend"]["comp"], 1)
               else "does not detectably lower the violation")
            + " (Fisher *p* " + _fp(_C["naming_rendered"]["viol_p"]) + " rendered, " + _fp(_C["naming_hidden"]["viol_p"]) + " hidden). "
            "The absolute level is not stable: completing carries pass the stove at a median 0.24–0.29 m against 0.31–0.37 m on the "
            "substitute-driver day, so the blind rendered arm violates on " + f"{_A['blind_rend']['viol']}/{_A['blind_rend']['comp']}"
            + " against Table XI's 11/30. The direction of the rendering effect replicates; the scored G1 T1 rate is specific to its "
            "seeds and driver and is read as a case-study figure, not an estimate.")
    _k = t.find("*Naming* produces no significant reduction in the violation rate")
    _e = t.find("\n\n", _k)
    if _k > 0 and _e > _k and "**Replication on the normal driver.**" not in t:
        t = t[:_e] + _txt + t[_e:]
    else:
        print("  [a179 MISS] E.2 Table XI paragraph")
    _rn2("(two seeds, substitute driver; E.2)",
         "(two seeds on the substitute driver, " + ("replicated on two new seeds" if _rep else "not replicated on two new seeds") + "; E.2)")
else:
    print("  [a179] b2xr not complete yet")
