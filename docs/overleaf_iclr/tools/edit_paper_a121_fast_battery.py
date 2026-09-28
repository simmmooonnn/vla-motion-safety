# -*- coding: utf-8 -*-
# pi0-FAST on the task battery: a Table IV-style table in Appendix E.8 (rows = tasks it carries on >= 8 episodes) and the
# section-8 clause "pi0 and GR00T-DROID cover the canonical task only" made exact. Guarded on at least three battery tasks.
# Exec'd after a120 (uses t, RN, V).
_rows, _nt = V.get("tab4_f0_rows", ""), int(V.get("n_tasks_f0", "0") or 0)
_nb = V.get("n_tasks_f0_boundary", "0")

if _nt >= 3 and _rows:
    _anchor = ("The keep-out entries of the trajectory dimension are therefore the benchmark's transports sitting inside the "
               "demonstrations' workspace, and a scene laid out farther from the base would see the bow reverse.")
    if _anchor in t:
        RN(_anchor, _anchor + "\n\n**π0-FAST on the task battery.** The battery of Table IV run on π0-FAST (" + str(_nt) +
           " tasks carried on eight episodes or more; " + _nb + " below the floor), scored exactly as π0.5's rows:\n\n"
           "| Task | att. / carried / deliv. | tier | Trajectory | Orientation | Speed & force | Dynamics |\n|---|---|---|---|---|---|---|\n" +
           _rows + "\n\n")
    # section 8: the coverage clause
    if "π0 and GR00T-DROID cover the canonical task only," in t:
        RN("π0 and GR00T-DROID cover the canonical task only,",
           "π0 and GR00T-DROID cover the canonical task only (π0-FAST " + str(_nt) + " battery tasks too, Appendix E.8),")
