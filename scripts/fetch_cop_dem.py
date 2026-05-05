#!/usr/bin/env python
"""Clip a Copernicus GLO-30 DEM to a bounding box with WGS84 ellipsoid heights.

Source: AWS Open Data bucket `copernicus-dem-30m` (no API key, no auth).
That data ships heights referenced to the EGM2008 geoid (EPSG:3855). ASP
expects ellipsoid heights (EPSG:4979), so this script applies the
geoid -> ellipsoid shift via gdalwarp with a compound source/target CRS,
mirroring the recipe in uw-cryo/fetch_dem (which OpenTopography uses for
its `_E` demtype variants).

Usage:
    python scripts/fetch_cop_dem.py \\
        --bbox -117.27 32.85 -117.20 32.92 \\
        --t-srs EPSG:32611 \\
        --tr 30 \\
        --out data/ucsd/cop30_wgs84_ellip.tif
"""

from __future__ import annotations

import argparse
import math
import subprocess
import tempfile
from pathlib import Path

import boto3
from botocore import UNSIGNED
from botocore.client import Config

BUCKET = "copernicus-dem-30m"
S3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))


def tile_name(lat: int, lon: int) -> str:
    """Return the Copernicus DEM tile S3 key for a 1° tile origin (SW corner)."""
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"
    return (
        f"Copernicus_DSM_COG_10_{ns}{abs(lat):02d}_00_{ew}{abs(lon):03d}_00_DEM/"
        f"Copernicus_DSM_COG_10_{ns}{abs(lat):02d}_00_{ew}{abs(lon):03d}_00_DEM.tif"
    )


def tiles_covering(west: float, south: float, east: float, north: float):
    for lat in range(math.floor(south), math.ceil(north)):
        for lon in range(math.floor(west), math.ceil(east)):
            yield tile_name(lat, lon)


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
        "--t-srs",
        default="EPSG:4326",
        help="Target horizontal SRS (default: EPSG:4326).",
    )
    p.add_argument(
        "--tr",
        type=float,
        default=30.0,
        help="Target resolution in target-SRS units (default: 30).",
    )
    p.add_argument("--out", type=Path, required=True, help="Output GeoTIFF path.")
    args = p.parse_args()

    west, south, east, north = args.bbox
    args.out.parent.mkdir(parents=True, exist_ok=True)

    # COP30 ships WGS84 lon/lat (EPSG:4326) + EGM2008 geoid heights (EPSG:3855).
    # Target: requested horizontal SRS + WGS84 ellipsoid heights (EPSG:4979).
    # gdalwarp applies the per-pixel geoid -> ellipsoid shift via PROJ's
    # bundled EGM2008 grid.
    src_crs = "EPSG:4326+EPSG:3855"
    dst_crs = f"{args.t_srs}+EPSG:4979"

    print(f"Fetching COP30 tiles covering bbox=({west},{south},{east},{north})")
    with tempfile.TemporaryDirectory() as tmpdir:
        tile_files: list[str] = []
        for key in tiles_covering(west, south, east, north):
            try:
                obj = S3.get_object(Bucket=BUCKET, Key=key)
            except S3.exceptions.NoSuchKey:
                print(f"  (tile not present: {key} — likely ocean)")
                continue
            tile_path = Path(tmpdir) / Path(key).name
            tile_path.write_bytes(obj["Body"].read())
            tile_files.append(str(tile_path))
            print(f"  → {key}")

        if not tile_files:
            raise RuntimeError(
                "No tiles found for the requested bbox; is it over open ocean?"
            )

        print(f"Reprojecting {len(tile_files)} tile(s) to {dst_crs} at {args.tr} units")
        subprocess.run(
            [
                "gdalwarp",
                "-r", "cubic",
                "-co", "COMPRESS=LZW",
                "-co", "TILED=YES",
                "-co", "BIGTIFF=IF_SAFER",
                "-te_srs", "EPSG:4326",
                "-te", str(west), str(south), str(east), str(north),
                "-tr", str(args.tr), str(args.tr),
                "-s_srs", src_crs,
                "-t_srs", dst_crs,
                *tile_files,
                str(args.out),
            ],
            check=True,
        )

    # gdalwarp tags the output with only the target horizontal SRS; re-assert
    # the compound CRS so downstream tools see the vertical component.
    subprocess.run(
        ["gdal_edit.py", str(args.out), "-a_srs", dst_crs],
        check=True,
    )
    print("Done.")


if __name__ == "__main__":
    main()
