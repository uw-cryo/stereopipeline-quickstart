#!/usr/bin/env bash
# Runs once when the Codespace is created (onCreateCommand), including in
# Codespaces prebuilds. Keep this fast.
#
# What we do here:
#   1. Confirm ASP and the python env are healthy.
#   2. Fetch the background map tiles for the tutorials' stereo geometry plots.
#   3. Print a short "what now?" message into the terminal.
#
# It downloads no data: each notebook's download cell fetches its own, from a
# release of this repo, so a Codespace always gets the data its checked-out code
# names (a prebuild made before a data change can't hand out stale files). The
# map tiles are only the plot's background, so an older copy does no harm.

set -euo pipefail

# Codespaces invokes onCreateCommand through a login-interactive-shell env
# probe; conda's activation in ~/.bashrc can strip /opt/StereoPipeline/bin
# from PATH even though the image-level ENV directive includes it. Make PATH
# explicit here so this script doesn't depend on the shell wrapping.
#
# Order matters: the conda env's bin must come first because ASP bundles its
# own python at /opt/StereoPipeline/bin/python that has none of the conda
# env's packages (asp_plot, rasterio, etc.) — putting ASP first shadows
# `python` and breaks the asp_plot import check below.
export PATH="/opt/conda/envs/asp/bin:/opt/StereoPipeline/bin:${PATH:-/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin}"

echo "==> stereopipeline-quickstart onCreate.sh"

# ---- 1. Sanity check toolchain ----------------------------------------------
echo "--> ASP version:"
parallel_stereo --version || { echo "ERROR: parallel_stereo not on PATH"; exit 1; }

echo "--> asp_plot version:"
# Use the full conda env python explicitly — defensive against any PATH
# manipulation in lifecycle wrapping.
/opt/conda/envs/asp/bin/python -c "import asp_plot; print(asp_plot.__version__)"

# ---- 2. Basemap tiles ---------------------------------------------------------
# Without them, the first stereo geometry plot fetches them itself (13-45 s).
# Not fatal: the plot still works without the cache.
echo "--> Fetching basemap tiles for the stereo geometry plots:"
timeout 120 /opt/conda/envs/asp/bin/python scripts/prefetch_basemap.py data/basemap_cache \
    || echo "Could not fetch the basemap tiles; the stereo geometry plot will fetch them itself."

# ---- 3. Friendly hello -------------------------------------------------------
cat <<'EOF'

===============================================================

stereopipeline-quickstart
ASP + asp_plot, ready to go.

Next steps:
  1. Tutorial 1 (notebooks/01_aster_rainier.ipynb) opens and starts
     running by itself. Scroll down to follow it.
  2. Or read docs/start/codespaces.md for an orientation tour.

===============================================================

EOF
