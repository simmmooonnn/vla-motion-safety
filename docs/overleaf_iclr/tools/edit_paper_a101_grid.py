# -*- coding: utf-8 -*-
# The off-path keep-out as a surface x level grid, policy against the blind control, in Appendix E.8. Guarded on the packing
# station's 0.12 m level existing. Exec'd after a100 (uses t, RN, V).
_grid = V.get("t1_grid_rows", "")
if "packing station | " in _grid and _grid.count("—") <= 2:
    RN("The bend is real and it is scene-dependent; the pooled number is what Table IV carries, and the desk is where it lives.",
       "The bend is real and it is scene-dependent; the pooled number is what Table IV carries, and the desk is where it lives. "
       "The full grid (entered / scored, π0.5 / blind control):\n\n"
       "| Surface | on the path | 0.12 m off | 0.20 m off | 0.28 m off |\n|---|---|---|---|---|\n" + _grid)
