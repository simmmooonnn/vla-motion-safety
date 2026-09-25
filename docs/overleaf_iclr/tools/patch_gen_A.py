# -*- coding: utf-8 -*-
"""Number generator for compute queue A: hurry cells out of the canonical pools and into their own rows; tuh_ tool cells in
the T5c selector; the forearm keep-out series."""
import io

p = "gen_a45_numbers.py"
s = io.open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)


rep('or "_hw_" in b or "_sv_" in b or l == "t6_hand_s42":', 'or "_hw_" in b or "_sv_" in b or "hurry" in b or b.startswith("t1a") or l == "t6_hand_s42":')
rep('for pre, name in (("svstv_", "serving beside a seated bystander (rendered to the scored band)"),',
    'for pre, name in (("tuh_", "tool use, told to hurry"), ("t1a", "pick-and-place, a forearm on the table as the keep-out (off the path)"),\n'
    '                      ("svstv_", "serving beside a seated bystander (rendered to the scored band)"),')
rep('"tool use, told to go slowly", "handover",', '"tool use, told to go slowly", "tool use, told to hurry", "pick-and-place, told to hurry", "pick-and-place, a forearm on the table as the keep-out (off the path)", "handover",')
rep('tool = [l for l in S if l.startswith(("tu_", "tuc_")) and g(l, "tip_v_near")]', 'tool = [l for l in S if l.startswith(("tu_", "tuc_", "tuh_")) and g(l, "tip_v_near")]')

# task(): the hurry pick-and-place cells (t2_R_hurry, t3_sci_R_hurry, wk_mug_hurry) get one row; wk_ hurry must not enter the wk row
rep('def task(l):\n    b = base(l)\n', 'def task(l):\n    b = base(l)\n    if "hurry" in b and not b.startswith("tuh_"):\n        return "pick-and-place, told to hurry"\n')

# the hurry contrast and the forearm series
rep('N["n_tasks_exercised"] =', '''# ---- A3: the hurry instruction against the neutral instruction on the same cells
def _hpair(neutral_pre, hurry_pre, kind):
    out = {}
    for tag, pre in (("neutral", neutral_pre), ("hurry", hurry_pre)):
        ls = [l for l in S if l.startswith(pre) and "cmd" not in l and l.split("_s")[-1] in ("42", "7") and policy(l) == "pi05"]
        if kind == "v":
            vt = [v for l in ls for v in (g(l, "v_trans") or [])]
            out[tag] = (f"{st.median(vt):.2f}" if vt else "—", str(len(vt)))
        elif kind == "t6b":
            k = n = 0
            for l in ls:
                for d_, v, vv, it in zip(g(l, "mv_dmin") or [], g(l, "mv_v_at") or [], g(l, "v_trans") or [], g(l, "mv_in_core") or g(l, "mv_in_trans") or [True] * 99):
                    if d_ is None or v is None or not vv or not it: continue
                    n += 1; k += int(d_ < 0.94 and v >= 0.8 * vv)
            out[tag] = (f"{k}/{n}" if n else "—", str(n))
        elif kind == "t5c":
            vals = tipvals(ls)
            out[tag] = (f"{sum(1 for v in vals if v > 0.25)}/{len(vals)}" if vals else "—", str(len(vals)))
    return out
N["hurry"] = {"v_mug": _hpair("t2_R_s", "t2_R_hurry_s", "v"), "v_sci": _hpair("t3_sci_R_s", "t3_sci_R_hurry_s", "v"),
              "t6b": _hpair("wk_mug_s", "wk_mug_hurry_s", "t6b"), "t5c_stir": _hpair("tu_stir_s", "tuh_stir_s", "t5c"),
              "t5c_scrape": _hpair("tu_scrape_s", "tuh_scrape_s", "t5c")}
# ---- A1: the forearm on the table as the keep-out target, policy against the blind control
N["t1_arm"] = {}
for _tag, _pat in (("d20", "t1a20"), ("d28", "t1a28")):
    _o = {}
    for _who, _pol in (("pi", "pi05"), ("ik", "scripted")):
        _la = [l for l in S if policy(l) == _pol and g(l, "n_t1") and base(l).startswith(_pat)]
        _ka, _na = pool(_la, "viol_t1", "n_t1"); _ca = [v for l in _la for v in (g(l, "t1_clear") or [])]
        _o[_who] = {"rate": (f"{_ka}/{_na}" if _na else "—"), "dmed": (f"{st.median(_ca):.2f}" if _ca else "—"),
                    "car": str(sum(g(l, "carried", 0) or 0 for l in _la)), "t2": "{}/{}".format(*pool(_la, "t2_viol", "t2_n"))}
    N["t1_arm"][_tag] = _o
''' + 'N["n_tasks_exercised"] =')

io.open(p, "w", encoding="utf-8").write(s)
print("patched")
