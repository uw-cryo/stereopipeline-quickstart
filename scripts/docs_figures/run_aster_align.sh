#!/usr/bin/env bash
# Align Tutorial 1's DEM to its COP30 reference with pc_align and grid the
# result, for the docs figure dh-before-after-alignment.png
# (scripts/docs_figures/make_figures.py).
#
#   bash scripts/docs_figures/run_aster_align.sh <run folder> <output folder>
#
# <run folder> is the top folder of a checkout where Tutorial 1 has run (it
# holds notebooks/ and data/). A translation only, with a 50 m limit; the
# aligned DEM is gridded on Tutorial 1's window at 30 m in UTM zone 10N.
# Writes <output folder>/run-*. About a minute.

set -euo pipefail

DATA="$1/data/aster_rainier"
OUT="$2"

pc_align --max-displacement 50 --compute-translation-only --save-transformed-source-points \
    "${DATA}/ref/cop30_rainier.tif" "${DATA}/stereo/run-DEM.tif" -o "${OUT}/run"
point2dem --t_srs EPSG:32610 --tr 30 --t_projwin 577305 5172975 615705 5209035 \
    "${OUT}/run-trans_source.tif"
