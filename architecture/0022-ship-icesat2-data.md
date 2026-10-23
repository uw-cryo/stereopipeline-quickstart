# 22. Ship the tutorials' ICESat-2 data as release assets

- **Date:** 2026-10-23
- **Status:** Accepted
- **Context doc:** `ARCHITECTURE.md` § `--reuse-selections` for comparable reports

## Context
Every report cell asked SlideRule for ICESat-2 ATL06-SR points when it ran. The first ASTER report crashed while SlideRule was under heavy load, with `TypeError: 'NoneType' object is not iterable` raised from inside `sliderule.run()`. For a first-time user the tutorial then fails at the step that shows its results, for a reason they can't fix.

asp_plot's own parquet cache doesn't avoid the request. It is used only when the new request matches the cached one exactly, and the default time range ends today, so the cache misses the next day. `asp_report --reuse-selections` does avoid it: the sidecar's `parquet_cache` path is loaded directly and no SlideRule request is made.

The ASTER request also had to be narrowed. Over the full mission, the Rainier footprint matches 301 ATL03 granules and SlideRule rejects requests over 300, so the ASTER report cells pass `--atl06sr-time-range 2018-10-14,2020-10-14`, the first two years of ICESat-2 and the closest to the 2017 scene.

## Decision
Ship each tutorial's ICESat-2 points and figure selections, and replay them in every report:

- From a known-good run of each tutorial's first report, save `atl06sr_all.parquet` and the `*_figure_selections.yml` sidecar. Rewrite the sidecar's `parquet_cache` path relative to `notebooks/` (`../data/<tutorial>/icesat2_shipped/atl06sr_all.parquet`).
- Attach the four files to a GitHub release with a dated tag (`icesat2-2026-10-23`), not to a commit.
- `download_aster.sh` and `download_worldview_ucsd.sh` fetch them with `curl -f` into `data/<tutorial>/icesat2_shipped/`, so a missing asset fails the download step. `postCreate.sh` runs `download_aster.sh`, so the ASTER files are already there when the Codespace opens.
- Every report cell passes `--reuse-selections` with the shipped sidecar. A `FRESH_ICESAT2 = False` switch at the top of each notebook turns this off; `True` requests fresh data from SlideRule, and the second report of a pair then reuses the first report's own sidecar as before.

## Consequences
- **+** The tutorials run when SlideRule is down or overloaded, and the reports are the same for every user.
- **+** Report cells are faster: no SlideRule request, and no ESA WorldCover sampling of the points.
- **+** Clones stay small: the 18 MB ASTER parquet lives on the release, not in git history.
- **−** The shipped points stop at the date they were requested; new ICESat-2 passes need `FRESH_ICESAT2 = True` or a new release.
- **−** A change of scene, crop, or report arguments needs new files and a new dated release, and the URL in the download scripts updated. Old releases stay, so older clones keep working.
- **−** The `icesat2_shipped/` folder keeps the shipped files apart from asp_plot's own `atl06sr_all.parquet`, so a fresh request can't overwrite them, but there are now two parquets in the data folder.

## Alternatives considered
- **Commit the files** — rejected: an 18 MB parquet would stay in every clone forever, even after it was replaced.
- **Rely on asp_plot's parquet cache** — rejected: it misses as soon as the default time range moves on, the next day.
- **Zenodo or Git LFS** — not needed: a release on this repo needs no extra account or tooling, and `curl -f` against its URL fails loudly when an asset is missing.
