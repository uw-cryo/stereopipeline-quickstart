# 8. ASTER tutorial restructured around a COP30 reference + two reports

- **Date:** 2026-06-10
- **Status:** Accepted (supersedes the earlier self-made downsample-reference workflow)
- **Context doc:** `AGENTS.md` § ASTER two-report workflow; commit 479c0fe

## Context
The original ASTER notebook produced its own reference by running a raw first pass, downsampling to a 200 m grid, and mapprojecting onto that before a second pass. It was hard to explain and did not reuse the WorldView machinery. The COP30 fetch built for WV (ADR-0007) is a cleaner, externally-sourced reference.

## Decision
Restructure `01_aster_rainier.ipynb` to mirror the WV flow and produce two DEMs and two reports for comparison:

1. Raw pass: `parallel_stereo` on the raw imagery (no BA, no ortho) to a 30 m DEM, with `--stereo-algorithm asp_bm` + `--subpixel-mode 1` (parabolic), plus its report.
2. Ortho pass: fetch a COP30 DEM, `mapproject` both views onto it at 15 m, re-run stereo with `asp_mgm` + `--subpixel-mode 9`, plus its report (COP30 as reference).

The bbox and UTM zone are derived from the camera footprints (`notebooks/utils.py`), so nothing is hardcoded. Subpixel mode 9 is used only on the ortho pass because mode 9 is unsupported with `asp_bm` block matching ("Use mode <= 6").

## Consequences
- **+** The COP30 reference is cleaner to explain and reuses the WV COP30 + camera-footprint machinery.
- **+** Two reports make the effect of orthorectification directly visible, matching the WV tutorial's two-report shape.
- **−** Adds a COP30 fetch and a second stereo pass to the ASTER runtime; tuned for the 4-core floor (`asp_mgm` runs `--processes 1 --threads-multiprocess 4`).

## Alternatives considered
- **Keep the self-made downsampled reference** (raw pass to a 200 m grid, mapproject onto it, second pass) — rejected: harder to explain and does not reuse the WV COP30 path.
