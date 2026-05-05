#!/usr/bin/env python
"""Clip a Copernicus GLO-30 DEM tile to a bounding box, no API key needed.

The Copernicus DEM is hosted as a free public AWS Open Data bucket — much
nicer than `fetch_dem` (which needs an OpenTopography API key) for codespaces.

Usage:
    python scripts/fetch_cop_dem.py \\
        --bbox -117.27 32.85 -117.20 32.92 \\
        --t-srs EPSG:32611 \\
        --tr 30 \\
        --out data/ucsd/cop30.tif

The output is a single GeoTIFF with WGS84 ellipsoid heights, reprojected to
the requested SRS at the requested resolution.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import boto3
from botocore import UNSIGNED
from botocore.client import Config
import rasterio
from rasterio.merge import merge
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.session import AWSSession
from rasterio.io import MemoryFile

BUCKET = "copernicus-dem-30m"
S3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))


def tile_name(lat: int, lon: int) -> str:
    """Return the Copernicus DEM tile filename for a 1° tile origin (SW corner)."""
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"
    return (
        f"Copernicus_DSM_COG_10_{ns}{abs(lat):02d}_00_{ew}{abs(lon):03d}_00_DEM/"
        f"Copernicus_DSM_COG_10_{ns}{abs(lat):02d}_00_{ew}{abs(lon):03d}_00_DEM.tif"
    )


def tiles_covering(west: float, south: float, east: float, north: float):
    """Yield 1° tile keys (S3 paths) that intersect the requested bbox."""
    for lat in range(math.floor(south), math.ceil(north)):
        for lon in range(math.floor(west), math.ceil(east)):
            yield tile_name(lat, lon)


def fetch_tile(key: str) -> rasterio.io.MemoryFile:
    """Download one COP30 tile from S3 into a rasterio MemoryFile."""
    print(f"  → s3://{BUCKET}/{key}")
    obj = S3.get_object(Bucket=BUCKET, Key=key)
    body = obj["Body"].read()
    mem = MemoryFile(body)
    return mem


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--bbox",
        type=float,
        nargs=4,
        metavar=("WEST", "SOUTH", "EAST", "NORTH"),
        required=True,
        help="Bounding box in EPSG:4326 (lon/lat).",
    )
    p.add_argument(
        "--t-srs", default="EPSG:4326", help="Target SRS for the output (default: EPSG:4326)."
    )
    p.add_argument("--tr", type=float, default=30.0, help="Target resolution in target-SRS units.")
    p.add_argument("--out", type=Path, required=True, help="Output GeoTIFF path.")
    args = p.parse_args()

    west, south, east, north = args.bbox
    args.out.parent.mkdir(parents=True, exist_ok=True)

    print(f"Fetching COP30 tiles covering bbox=({west},{south},{east},{north})")
    memfiles = []
    datasets = []
    for key in tiles_covering(west, south, east, north):
        try:
            mem = fetch_tile(key)
            ds = mem.open()
            memfiles.append(mem)
            datasets.append(ds)
        except S3.exceptions.NoSuchKey:
            print(f"  (tile not present: {key} — likely ocean)")

    if not datasets:
        raise RuntimeError("No tiles found for the requested bbox; is it over open ocean?")

    print(f"Mosaicking {len(datasets)} tile(s)...")
    mosaic, mosaic_transform = merge(datasets, bounds=(west, south, east, north))
    src_crs = datasets[0].crs

    # Reproject to target SRS at requested resolution
    print(f"Reprojecting to {args.t_srs} at {args.tr} m resolution → {args.out}")
    dst_transform, dst_w, dst_h = calculate_default_transform(
        src_crs, args.t_srs,
        mosaic.shape[2], mosaic.shape[1],
        west, south, east, north,
        resolution=args.tr,
    )
    profile = {
        "driver": "GTiff",
        "dtype": mosaic.dtype,
        "count": 1,
        "width": dst_w,
        "height": dst_h,
        "crs": args.t_srs,
        "transform": dst_transform,
        "compress": "deflate",
        "tiled": True,
    }
    with rasterio.open(args.out, "w", **profile) as dst:
        reproject(
            source=mosaic[0],
            destination=rasterio.band(dst, 1),
            src_transform=mosaic_transform,
            src_crs=src_crs,
            dst_transform=dst_transform,
            dst_crs=args.t_srs,
            resampling=Resampling.bilinear,
        )

    for ds in datasets:
        ds.close()
    for mem in memfiles:
        mem.close()
    print("Done.")


if __name__ == "__main__":
    main()
