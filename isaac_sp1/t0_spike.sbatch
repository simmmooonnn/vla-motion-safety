#!/bin/bash
#SBATCH --job-name=t0-spike
#SBATCH --partition=nvl
#SBATCH --gpus=1
#SBATCH --time=00:30:00
#SBATCH --account=aszalay1_ssci
#SBATCH --output=/weka/scratch/aszalay1/zijian/isaac/logs/t0.%j.out
set -uo pipefail
BASE=/weka/scratch/aszalay1/zijian
export OUTDIR=$BASE/safety/ISAAC_SP1
mkdir -p $OUTDIR $BASE/isaac/logs
# Accept the Omniverse EULA non-interactively, and keep Isaac's (multi-GB)
# shader/asset caches on scratch instead of the small HOME quota.
export OMNI_KIT_ACCEPT_EULA=YES
export HOME=$BASE/isaac/omnihome
mkdir -p $HOME
# Bare compute nodes lack workstation GL/X libs (libGLU, libXt, ...) the RTX
# renderer needs; supply them from the conda-forge syslibs env on scratch.
export LD_LIBRARY_PATH=$BASE/isaac/syslibs/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
echo "=== node $(hostname) job ${SLURM_JOB_ID:-manual} $(date) HOME=$HOME ==="
nvidia-smi --query-gpu=driver_version,name --format=csv,noheader
echo "=== render spike ==="
$BASE/envs/isaaclab/bin/python $BASE/isaac/t0_render_spike.py
echo "spike_exit=$?"
ls -la $OUTDIR/t0_frame.png 2>/dev/null
echo "=== DONE ==="
