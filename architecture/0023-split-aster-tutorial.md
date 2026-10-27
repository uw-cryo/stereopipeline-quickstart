# 23. Split the ASTER tutorial: quick look first, orthorectified pass second

- **Date:** 2026-10-23
- **Status:** Superseded by [0027](0027-single-aster-tutorial.md): the two ASTER notebooks became one. Amended [0008](0008-aster-cop30-two-reports.md)
- **Context doc:** `ARCHITECTURE.md` § Sentinel files per step

## Context
[ADR-0008](0008-aster-cop30-two-reports.md) put both ASTER passes in one notebook, `01_aster_rainier.ipynb`: a raw pass with `asp_bm` and `--subpixel-mode 1`, then a COP30 fetch, `mapproject`, and a second pass with `asp_mgm` and `--subpixel-mode 9`, each with a report. The second pass is the slow part of that notebook. Besides orthorectifying, it switches to the slower matcher and subpixel mode.

The first notebook is what a first-time user runs, and what someone who only wants to see ASP work runs. With both passes in it, they waited for the slow pass before reaching the end of the first notebook, and there was no short "click and see results" path.

## Decision
Split the ASTER notebook in two, and keep each comparison pair together (01–02 ASTER, 03–04 WorldView):

1. `01_aster_rainier.ipynb`, the ASTER quick look: download, `aster2asp`, `asp_bm` stereo, 30 m DEM, report. It keeps its filename, so links to the first tutorial still work.
2. `02_aster_rainier_ortho.ipynb`, new: COP30 fetch, `mapproject`, `asp_mgm` stereo, and a report that replays the first report's figure selections. It repeats the download and `aster2asp` cells, which skip when Tutorial 1 has run, so it also runs on its own.
3. `03_worldview_ucsd.ipynb`, formerly `02_worldview_ucsd.ipynb`.
4. `04_worldview_ucsd_ba.ipynb`, formerly `03_worldview_ucsd_ba.ipynb`.

The `data/aster_rainier/` output paths are unchanged, so the shipped ICESat-2 sidecar ([ADR-0022](0022-ship-icesat2-data.md)) and the figures made from earlier runs stay valid. Each notebook states its run time measured in a 4-core Codespace, at the top and above each step. Measured on 2026-10-23, Run All to report: 01 ~6 min, 02 ~19.5 min, 03 ~5.5 min, 04 ~20 min. That is not a fastest-first order (03 is as quick as 01), so the order follows the pairs instead.

Earlier ADRs keep the old filenames, since accepted records are not edited: in 0008, `01_aster_rainier.ipynb` means both ASTER notebooks; in 0012 and 0018, `02_worldview_ucsd.ipynb` / tutorial 2 is now 03, and `03_worldview_ucsd_ba.ipynb` / tutorial 3 is now 04.

## Consequences
- **+** The first notebook takes about 6 minutes, as short as any in the repo, and it doubles as the path for someone who only wants to see ASP produce a DEM and a report.
- **+** Each comparison pair sits side by side, and every notebook says how long it takes.
- **−** Comparing the two ASTER reports now spans two notebooks; Tutorial 2 links both reports.
- **−** Renumbering the WorldView notebooks breaks links to their old filenames from outside this repo.

## Alternatives considered
- **Keep one ASTER notebook and mark the second pass optional** — rejected: "Run All" runs it anyway, and the slow pass would still sit between a first-time user and the end of the first notebook.
- **Keep the WorldView numbers and call the new notebook 01b** — rejected: the numbers would no longer give the order to run them in.
- **Number strictly by run time** (01 ASTER quick look, 02 WorldView, 03 ASTER orthorectified, 04 WorldView with BA) — rejected: it splits each comparison pair.
