"""Fetch the background map tiles for Tutorial 1's stereo geometry plot ahead of time.

asp-plot draws the plot's map over contextily's default web tiles, and
contextily caches tiles in a new temporary folder for each Python process, so
the first plot in a Codespace fetched all of them (13-20 s). onCreate.sh runs
this once when the Codespace is built (in the prebuild, for main), into
data/basemap_cache/; the notebook points contextily at that folder. If the plot
ever asks for other tiles, it fetches them as before.

Usage:
    python scripts/prefetch_basemap.py                # → ./data/basemap_cache/
    python scripts/prefetch_basemap.py /custom/dir
"""

import sys

import contextily

# The map extent asp-plot's StereoGeometryPlotter uses for the Tutorial 1
# scene (Web Mercator meters: west, south, east, north), as passed to
# contextily.bounds2img by stereo_geom_plot().
ASTER_RAINIER_BOUNDS = (-13648541.47933645, 5299119.773867412, -13383903.999712005, 6060139.714014306)

cache_dir = sys.argv[1] if len(sys.argv) > 1 else "data/basemap_cache"
contextily.set_cache_dir(cache_dir)
contextily.bounds2img(*ASTER_RAINIER_BOUNDS)
print(f"Basemap tiles for Tutorial 1 cached in {cache_dir}")
