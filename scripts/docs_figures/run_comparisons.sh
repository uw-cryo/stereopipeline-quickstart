#!/usr/bin/env bash
# Run SETSM and CARS on Tutorial 2's pair over its square, for the docs'
# comparison pages (docs/comparisons/) and their hillshade figures
# (scripts/docs_figures/make_figures.py).
#
#   bash scripts/docs_figures/run_comparisons.sh <wv run> <output folder>
#
# <wv run> is the top folder of a checkout where Tutorial 2 has run (it holds
# notebooks/ and data/). The tutorial orthorectifies straight from the full
# scenes, so this first cuts the square plus a 250 m margin out of each scene
# with cam2rpc, at the images' own resolution, with an RPC camera fitted to
# the crop (data/ucsd_penasquitos/crops/<catid>_P001.{tif,xml}): the raw crops
# with RPC cameras that SETSM and CARS take. Needs Docker, with the `setsm` image built as
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

# The crops: Tutorial 2's square (its T_PROJWIN) plus 250 m, so the RPC fit
# covers the square with margin, cut from the full scenes.
DATA="${RUN}/data/ucsd_penasquitos"
read -r XMIN YMIN XMAX YMAX <<< "480420 3641720 481420 3642720"
mkdir -p "${DATA}/crops"
if [[ ! -f "${DATA}/crops/rpc_box.tif" ]]; then
    gdal_translate -q -projwin $((XMIN - 250)) $((YMAX + 250)) $((XMAX + 250)) $((YMIN - 250)) \
        "${DATA}/ref/cop30_penasquitos.tif" "${DATA}/crops/rpc_box.tif"
fi
for catid in 104001000496A100 10400100071D8800; do
    if [[ ! -f "${DATA}/crops/${catid}_P001.tif" ]]; then
        cam2rpc -t dg --dem-file "${DATA}/crops/rpc_box.tif" --save-tif-image \
            "${DATA}/${catid}_P001.NTF" "${DATA}/${catid}_P001.xml" \
            "${DATA}/crops/${catid}_P001.xml" > "${DATA}/crops/${catid}_cam2rpc.log" 2>&1
    fi
done

# SETSM. -minH/-maxH span the square's heights (COP30: about -30 to 90 m).
python "${HERE}/setsm_inputs.py" "${RUN}" "${OUT}/setsm/input"
docker run --platform linux/amd64 --rm --memory 11g --cpus 6 \
    -v "${OUT}/setsm/input:/data" -v "${OUT}/setsm:/out" -w /data setsm \
    -image 104001000496A100_P001.tif -image 10400100071D8800_P001.tif \
    -outpath /out/results -outres 1 -mem 10 -minH -60 -maxH 150 -projection utm \
    > "${OUT}/setsm/setsm.log" 2>&1

# CARS.
mkdir -p "${OUT}/cars"
cp "${HERE}/cars_config.yaml" "${OUT}/cars/config.yaml"
docker run --platform linux/amd64 --rm --memory 11g --cpus 6 \
    -v "${RUN}/data/ucsd_penasquitos/crops:/input:ro" -v "${OUT}/cars:/output" \
    cnes/cars /output/config.yaml > "${OUT}/cars/cars.log" 2>&1
