import glob
import json
import math
import os
import sys

DEST = (-0.245, -1.627)  # blue_sorting_bin xy (destination)
d = sys.argv[1] if len(sys.argv) > 1 else "."
for f in sorted(glob.glob(os.path.join(d, "clearance_*.json"))):
    j = json.load(open(f))
    px, py = j["person_xy"]
    print(f"== {os.path.basename(f)} person=({px},{py}) ==")
    for i, ep in enumerate(j.get("episodes", [])):
        b = ep["box_xy"]
        if not b:
            print(f"  ep{i}: EMPTY")
            continue
        sx, sy = b[0]
        ex, ey = b[-1]
        dperson = min(math.hypot(x - px, y - py) for x, y in b)
        ddest = min(math.hypot(x - DEST[0], y - DEST[1]) for x, y in b)
        disp = math.hypot(ex - sx, ey - sy)
        print(f"  ep{i}: start=({sx:.3f},{sy:.3f}) end=({ex:.3f},{ey:.3f}) steps={len(b)} "
              f"min->person={dperson:.3f} min->dest={ddest:.3f} disp={disp:.3f}")
