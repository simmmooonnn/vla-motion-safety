"""T0: prove Isaac Sim launches headless and renders a frame on an ARCH GPU node.

Pass = a non-black 256x256 PNG comes back (Vulkan headless rendering works).
This is the hard GO/NO-GO for approach A (pip isaacsim on ARCH).
"""
import os
import numpy as np
import imageio.v2 as imageio
from isaacsim import SimulationApp

app = SimulationApp({"headless": True, "renderer": "RayTracedLighting"})

import omni.replicator.core as rep  # noqa: E402
from pxr import UsdGeom  # noqa: E402
import omni.usd  # noqa: E402

stage = omni.usd.get_context().get_stage()
UsdGeom.Cube.Define(stage, "/World/Cube")
# a distant light so the frame isn't black
rep.create.light(light_type="distant")

cam = rep.create.camera(position=(3.0, 3.0, 3.0), look_at=(0.0, 0.0, 0.0))
rp = rep.create.render_product(cam, (256, 256))
rgb = rep.AnnotatorRegistry.get_annotator("rgb")
rgb.attach(rp)

for _ in range(30):
    rep.orchestrator.step()

frame = np.asarray(rgb.get_data())[..., :3]
out = os.environ.get("OUTDIR", "/tmp") + "/t0_frame.png"
imageio.imwrite(out, frame.astype(np.uint8))
print("WROTE", out, frame.shape, "sum=", int(frame.sum()))
app.close()
print("T0_OK")
