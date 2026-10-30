#!/usr/bin/env bash
# Run SETSM and CARS on Tutorial 2's cropped images, for the docs' comparison
# pages (docs/comparisons/) and their hillshade figures
# (scripts/docs_figures/make_figures.py).
#
#   bash scripts/docs_figures/run_comparisons.sh <wv run> <output folder>
#
# <wv run> is the top folder of a checkout where Tutorial 2 has run (it holds
# notebooks/ and data/). Needs Docker, with the `setsm` image built as
# docs/comparisons/setsm.md describes and `cnes/cars` pulled; both images are
# amd64 and run emulated on an Apple Silicon Mac. Writes
# <output folder>/setsm/results/results_dem.tif and
# <output folder>/cars/results/dsm/dsm.tif, with each tool's log beside it.
#
# SETSM needs camera files with more than the RPC (see setsm_inputs.py), so
# the crops are copied to <output folder>/setsm/input with those files. CARS
# reads the RPC from the crops' GeoTIFF tags directly.

set -euo pipefail

RUN="$(cd "$1" && pwd)"
mkdir -p "$2"
OUT="$(cd "$2" && pwd)"
HERE="$(cd "$(dirname "$0")" && pwd)"

# SETSM. -minH/-maxH span the window's heights (COP30: -32 to 216 m).
python "${HERE}/setsm_inputs.py" "${RUN}" "${OUT}/setsm/input"
docker run --platform linux/amd64 --rm --memory 11g --cpus 6 \
    -v "${OUT}/setsm/input:/data" -v "${OUT}/setsm:/out" -w /data setsm \
    -image 104001000496A100_P001.tif -image 10400100071D8800_P001.tif \
    -outpath /out/results -outres 2.4 -mem 10 -minH -50 -maxH 300 -projection utm \
    > "${OUT}/setsm/setsm.log" 2>&1

# CARS.
mkdir -p "${OUT}/cars"
cp "${HERE}/cars_config.yaml" "${OUT}/cars/config.yaml"
docker run --platform linux/amd64 --rm --memory 11g --cpus 6 \
    -v "${RUN}/data/ucsd_penasquitos/crops:/input:ro" -v "${OUT}/cars:/output" \
    cnes/cars /output/config.yaml > "${OUT}/cars/cars.log" 2>&1
