# -*- coding: utf-8 -*-
"""Round 3, C5: the Speed-and-force fixed set is per family. Power-and-force limiting is the applicable collaborative mode
for a table-side arm, so speed-and-separation monitoring (T5a) has no business in a tabletop mean; on the walking humanoid
both apply. dim_cell() now takes the row's family and prints the set it used."""
import io

p = "gen_a45_numbers.py"
s = io.open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)


rep('DIMS = [("Trajectory", ["T1", "T2"]), ("Orientation", ["T3", "T4"]), ("Speed & force", ["T5a", "T5b"]), ("Dynamics", ["T6", "T6b"])]',
    '''# The fixed sub-type set per dimension. Speed & force differs by family: the tabletop arm is scored under power-and-force
# limiting (T5b), the walking humanoid under both speed-and-separation monitoring and PFL (review round 3, C5).
DIMS = [("Trajectory", ["T1", "T2"]), ("Orientation", ["T3", "T4"]), ("Speed & force", ["T5b"]), ("Dynamics", ["T6", "T6b"])]
DIMS_G1 = [("Trajectory", ["T1", "T2"]), ("Orientation", ["T3", "T4"]), ("Speed & force", ["T5a", "T5b"]), ("Dynamics", ["T6", "T6b"])]''')

rep('''def dim_cell(sub):
    """Mean over the fixed set when every member is scored with n >= FLOOR; otherwise the vector only."""
    out = []
    for name, ids in DIMS:''',
    '''def dim_cell(sub, dims=None):
    """Mean over the fixed set when every member is scored with n >= FLOOR; otherwise the vector only."""
    out = []
    for name, ids in (dims if dims is not None else DIMS):''')

rep('N["tab3_rows"] = "\\n".join("| " + rows[p]["_name"] + " | " + " | ".join(dim_cell(rows[p])) + " |" for p in ORDER)',
    'N["tab3_rows"] = "\\n".join("| " + rows[p]["_name"] + " | " + " | ".join(dim_cell(rows[p], DIMS_G1 if p == "g1" else DIMS)) + " |" for p in ORDER)\n'
    'N["dims_note"] = ("Speed & force is the mean over {T5a, T5b} on the G1 and over {T5b} alone on the tabletop, where "\n'
    '                  "power-and-force limiting is the applicable collaborative mode and the speed-and-separation envelope is reported as exposure")')

io.open(p, "w", encoding="utf-8").write(s)
print("patched")
