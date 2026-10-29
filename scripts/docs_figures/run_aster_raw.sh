#!/usr/bin/env bash
# Run Tutorial 1's stereo on the raw ASTER images, without orthorectifying
# them first, for the docs figures that compare the two
# (scripts/docs_figures/make_figures.py).
#
#   bash scripts/docs_figures/run_aster_raw.sh <run folder> <output folder>
#
# <run folder> is the top folder of a checkout where Tutorial 1 has run (it
# holds notebooks/ and data/). Matcher settings are Tutorial 1's; the full
# scene is matched and point2dem grids Tutorial 1's window at 30 m in UTM
# zone 10N. Writes <output folder>/run-*. About 6 minutes on an 8-core laptop.

set -euo pipefail

DATA="$1/data/aster_rainier"
OUT="$2"

parallel_stereo -t aster --stereo-algorithm asp_mgm --subpixel-mode 9 \
    --processes 2 --threads-multiprocess 4 \
    --matches-per-tile 300 --ip-per-tile 1500 --matches-per-tile-params 512 640 \
    "${DATA}/out-Band3N.tif" "${DATA}/out-Band3B.tif" \
    "${DATA}/out-Band3N.xml" "${DATA}/out-Band3B.xml" \
    "${OUT}/run"
point2dem --t_srs EPSG:32610 --tr 30 --t_projwin 577305 5172975 615705 5209035 \
    --errorimage "${OUT}/run-PC.tif"
