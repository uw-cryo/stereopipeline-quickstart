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
# the crop (data/ucsd_penasquitos/crops/<catid>_P001.{tif,xml}), for CARS.
# Needs Docker, with the `setsm` image built as
# docs/comparisons/setsm.md describes and `cnes/cars` pulled; both images are
# amd64 and run emulated on an Apple Silicon Mac. Writes
# <output folder>/setsm/results/results_dem.tif and
# <output folder>/cars/results/dsm/dsm.tif, with each tool's log beside it.
#
# CARS takes the crops, reading the RPC from their GeoTIFF tags; SETSM takes
# the full scenes (below).

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

# SETSM runs on the full scenes, converted to TIFF as its manual says (section
# 2.1.4; ASP's gdal_translate has the JPEG2000 driver the NTFs need), with
# the vendor XMLs beside them, and -boundary_* limiting the output to the
# square so memory scales with the square, not the scenes. It does not get
# the crops: on cam2rpc crops at the images' own resolution it matched only a
# few hundred points at its coarsest level and wrote noise (NMAD 37 m against
# the lidar), where the full scenes with the same boundary gave a DEM. The
# 1.2 m crops of the earlier window had worked, which hid this.
# -minH/-maxH span the square's heights (COP30: about -30 to 90 m).
# ASP's gdal_translate reads the NTFs' JPEG2000 through a plugin in ASP's lib/,
# which it finds only with GDAL_DRIVER_PATH set (mapproject sets it itself).
export GDAL_DRIVER_PATH="${GDAL_DRIVER_PATH:-$(cd "$(dirname "$(command -v gdal_translate)")/../lib" && pwd)}"
mkdir -p "${OUT}/setsm"
for catid in 104001000496A100 10400100071D8800; do
    if [[ ! -f "${OUT}/setsm/${catid}_P001.tif" ]]; then
        gdal_translate -q --config GDAL_CACHEMAX 2048 -ot UInt16 -co NBITS=16 \
            -co bigtiff=if_safer -co tiled=yes -co compress=lzw \
            "${DATA}/${catid}_P001.NTF" "${OUT}/setsm/${catid}_P001.tif"
    fi
    cp "${DATA}/${catid}_P001.xml" "${OUT}/setsm/${catid}_P001.xml"
done
docker run --platform linux/amd64 --rm --memory 11g --cpus 6 \
    -v "${OUT}/setsm:/data" -w /data setsm \
    -image 104001000496A100_P001.tif -image 10400100071D8800_P001.tif \
    -outpath /data/results -outres 1 -mem 10 -minH -60 -maxH 150 \
    -boundary_min_X "${XMIN}" -boundary_min_Y "${YMIN}" -boundary_max_X "${XMAX}" -boundary_max_Y "${YMAX}" \
    -projection utm \
    > "${OUT}/setsm/setsm.log" 2>&1

# CARS.
mkdir -p "${OUT}/cars"
cp "${HERE}/cars_config.yaml" "${OUT}/cars/config.yaml"
docker run --platform linux/amd64 --rm --memory 11g --cpus 6 \
    -v "${RUN}/data/ucsd_penasquitos/crops:/input:ro" -v "${OUT}/cars:/output" \
    cnes/cars /output/config.yaml > "${OUT}/cars/cars.log" 2>&1
