# Isaac SP1 — T0 result (2026-08-09)

## Headline
- **Target stack (isaacsim 6 / Isaac Lab 3.0 / Arena) = NO-GO on ARCH via pip.** Their wheels are `manylinux_2_35` (glibc ≥2.35); every ARCH GPU node (l40s/a100/h100/nvl) is RHEL/Rocky 9 **glibc 2.34**. Cannot install or run. Arena depends on isaacsim 5.0+, so the whole Arena-LIBERO plan is blocked on ARCH without a container. → **needs a container (Apptainer + NGC Isaac Lab); Apptainer not installed → cluster admin. Reported to advisor.**
- **Reduced path WORKS: Isaac Sim 4.5 renders headless on ARCH.** `isaacsim==4.5.0` (manylinux_2_34, cp310) installs and renders a frame on nvl (H100 NVL, Vulkan + RTX). Proof: `t0_frame.png` (a rendered cube). This validates that Isaac itself runs on ARCH; only the *newest* stack is glibc-blocked.

## What T0 (reduced, isaacsim 4.5) required
1. **Python 3.10** venv via `uv` at `$BASE/envs/isaaclab` (4.5 ships cp310 wheels).
2. Install from login node (glibc 2.28) targeting compute glibc: `uv pip install --python-platform x86_64-manylinux_2_34 "isaacsim[all,extscache]==4.5.0" --extra-index-url https://pypi.nvidia.com`.
3. **`UV_CACHE_DIR` on scratch** — HOME (`/weka/home`, 52 GB) is too small; the default `~/.cache/uv` fills and extraction dies with `No space left on device`.
4. **`OMNI_KIT_ACCEPT_EULA=YES`** — else the first import blocks on an interactive EULA prompt (EOFError in batch).
5. **`HOME` redirected to scratch** in the job — keeps Isaac's multi-GB shader/asset caches off the small HOME.
6. **System GL/X libs** the bare compute node lacks: `libGLU.so.1`, `libXt.so.6` (RTX/iray + MaterialX). Supplied via a conda-forge `micromamba` env at `$BASE/isaac/syslibs` + `LD_LIBRARY_PATH`. Also `uv pip install requests` (isaacsim.asset.browser). Without libGLU the renderer **segfaults**.

First-run pipeline/shader compile ≈ 3.5 min; cached afterwards (cache on scratch).

## Status vs plan
- T0 gate: **passed on the reduced (4.5) path**; NO-GO on the target stack (glibc).
- T1–T4 (Isaac Lab 3.0 + Arena + GR00T ASR): **blocked** pending the container (Isaac Lab 3.0 needs isaacsim 5.0+ = glibc 2.35). The 4.5 path cannot run Arena/Lab-3.0.

Files: `t0_frame.png` (rendered cube), `setup_isaac.sh`, `t0_render_spike.py`, `t0_spike.sbatch`. See also memory `arch-isaac-glibc-blocker.md`.
