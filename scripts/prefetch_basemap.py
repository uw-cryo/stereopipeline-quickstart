"""Fetch the background map tiles for the tutorials' stereo geometry plots ahead of time.

asp-plot draws the plots' maps over contextily's default web tiles, and
contextily caches tiles in a new temporary folder for each Python process, so
the first plot in a Codespace fetched all of them (13-45 s per plot). onCreate.sh
runs this once when the Codespace is built (in the prebuild, for main), into
data/basemap_cache/; the notebooks point contextily at that folder. If a plot
ever asks for other tiles, it fetches them as before.

Usage:
    python scripts/prefetch_basemap.py                # → ./data/basemap_cache/
    python scripts/prefetch_basemap.py /custom/dir
"""

import sys

import contextily

# The map extents asp-plot's StereoGeometryPlotter uses for each tutorial's
# scenes (Web Mercator meters: west, south, east, north), as passed to
# contextily.bounds2img by stereo_geom_plot().
BOUNDS = {
    "Tutorial 1, ASTER": [
        (-13648541.47933645, 5299119.773867412, -13383903.999712005, 6060139.714014306),
    ],
    # Tutorial 3's plot has an overview and one map per pair; the first pair's
    # map is Tutorial 2's.
    "Tutorials 2 and 3, WorldView-3": [
        (-13152233.396033576, 3547851.539063119, -13020275.159719458, 3992138.5879843743),
        (-13164611.523830675, 3525387.8719050977, -12760435.457181545, 3993116.3933265326),
        (-13089962.13759885, 3525463.671235008, -12763992.050600542, 3993116.6753640263),
        (-13163768.789081682, 3529361.8641682235, -12762573.304061223, 3906687.0672213584),
    ],
}

cache_dir = sys.argv[1] if len(sys.argv) > 1 else "data/basemap_cache"
contextily.set_cache_dir(cache_dir)
for name, extents in BOUNDS.items():
    for extent in extents:
        contextily.bounds2img(*extent)
    print(f"Basemap tiles for {name} cached in {cache_dir}")
