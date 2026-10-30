# 32. Fetch the stereo geometry plot's map tiles when the Codespace is built

- **Date:** 2026-10-28
- **Status:** Accepted; an exception to [0028](0028-tutorial-data-on-releases.md)'s "`onCreate.sh` downloads nothing". Update 2026-10-28: extended to the WorldView tutorials' plots (one map for Tutorial 2, an overview and three pair maps for Tutorial 3); with the cache they take 0.9 s and 2.3 s locally
- **Context doc:** `ARCHITECTURE.md` § ASTER tutorial

## Context
The stereo geometry plot in Tutorial 1 (`asp-plot`'s `StereoGeometryPlotter`) draws its map over web tiles, through contextily: 18 OpenStreetMap tiles for this scene.
- **Time:** the cell took 13–45 s on a laptop, and about 30 s in a Codespace, nearly all of it fetching tiles one after another.
- **No reuse:** contextily caches tiles in a new temporary folder for each Python process, so every new kernel fetched them again.

[ADR-0028](0028-tutorial-data-on-releases.md) moved all data downloads out of `onCreate.sh` into the notebooks. Codespace prebuilds had held stale data twice.

## Decision
- **Script:** `scripts/prefetch_basemap.py` fetches the tiles for the plot's extent into `data/basemap_cache/`. The extent is the one `stereo_geom_plot()` passes to `contextily.bounds2img`, which is the same on every run of this scene.
- **When:** `onCreate.sh` runs it, so on `main` it happens in the prebuild. It has a 120 s timeout, and the Codespace still starts if the fetch fails.
- **In the notebook:** the stereo geometry cell points contextily at that folder (`contextily.set_cache_dir`). If the plot ever asks for other tiles, it fetches them as before.

Map tiles are an exception to ADR-0028 because a stale copy does no harm. They are only the plot's background, and nothing is computed from them.

## Consequences
- **+** **Faster plot:** with the cache, the cell takes about 2 s locally, against 13–45 s without it.
- **+** **Nothing to host:** the tiles are fetched from OpenStreetMap.
- **−** **Fixed extent:** the extent is copied into the script. If `asp-plot` changes how it frames the map, or the tutorial's scene changes, the cache misses and the plot fetches tiles again, until the script is updated.
- **−** **Testing needs `main`:** a Codespace made from a branch starts from `main`'s prebuild and then checks out the branch, so it runs `main`'s `onCreate.sh`. Changes to `onCreate.sh`, including this one, can only be tested in a Codespace after they reach `main`, with a fresh prebuild.
- **−** **Build time:** about 13 s in a Codespace, more if the tile server is slow. On `main` this is spent in the prebuild, not by the user.

## Alternatives considered
- **Fetch the tiles in parallel** (contextily's `n_connections`): this would need a change in `asp-plot`. OpenStreetMap's tile usage policy allows at most 2 connections, so it would gain little.
- **Ship the tiles on a release:** rejected. The tiles are OpenStreetMap's, and this repo would take on attribution and license terms for imagery that is only a background.
- **Fetch them in the notebook's download step:** moves the wait to an earlier cell rather than removing it.
- **Leave it:** the plot works, but a step meant to take a few seconds took half a minute.
