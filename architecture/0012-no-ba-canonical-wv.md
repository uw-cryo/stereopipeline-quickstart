# 12. No-BA WV tutorial is canonical; BA is the _ba variant

- **Date:** 2026-06-10
- **Status:** Accepted (supersedes the bundle-adjust-first WV tutorial)
- **Context doc:** `AGENTS.md` § ASTER two-report / WV3 thread budget; issue #7, commit ba37079

## Context
Bundle adjustment was the slowest step of the WV tutorial by a wide margin (measured around 21 minutes on 4 cores in #7). For a good reference DEM (COP30) over near-flat coastal terrain, skipping BA entirely was identified as the single biggest runtime lever, and 10-15 minutes was judged an acceptable tutorial target. But BA is still a lesson worth teaching.

## Decision
Make the no-BA recipe the canonical WorldView tutorial (`02_worldview_ucsd.ipynb`), and keep bundle adjustment as a separate variant (`03_worldview_ucsd_ba.ipynb`) with `_ba`-suffixed outputs so both can run in one data directory. The BA variant uses `--ip-per-tile 10` (halved BA time in local tests versus the default interest-point density, at effectively the same residual). Run 02 first so 03 can reuse its report figure selections for a panel-for-panel comparison.

## Consequences
- **+** The default path is fast enough for the 4-core floor; BA is available for those who want it.
- **+** Two notebooks in one data dir make the with/without-BA comparison concrete.
- **−** Two notebooks to keep coherent; shared setup (COP30 fetch, ROI) is duplicated across them.
- Further BA speedups (mapprojected-data BA, pre-supplied `ba/` outputs) were surfaced in #7/#12 but not adopted; they reorder the workflow or hide the compute.

## Alternatives considered
- **Keep BA in the single canonical tutorial** — rejected: too slow on 4 cores for a first-run experience.
- **`--mapprojected-data` bundle adjustment** (fastest measured BA) — deferred (#12): reorders the notebook and needs explanatory prose.
- **Pre-supply `ba/` outputs as a download** — deferred (#12): removes the compute but hides the lesson.
