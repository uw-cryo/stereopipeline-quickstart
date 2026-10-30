# 33. The docs' data figures are made by a script in this repo

- **Date:** 2026-10-29
- **Status:** Accepted; amends [0018](0018-docs-figure-conventions.md), whose consequences said the generating scripts live outside the repo
- **Context doc:** `ARCHITECTURE.md` § Docs site

## Context
The data figures on the concept pages (`docs/concepts/figures/*.png`) and the comparison pages' hillshades (`docs/comparisons/figures/`) came from the tutorial settings before [ADR-0027](0027-single-aster-tutorial.md) and [ADR-0029](0029-ucsd-soledad-tutorials.md): the old ASTER raw-imagery quick look with `asp_bm`, and an earlier WorldView pair. They showed lower quality than the tutorials now produce. The scripts that made them were kept outside the repo and were lost, so every figure had to be rebuilt from scratch.

## Decision
- **Script:** `scripts/docs_figures/make_figures.py` makes every data figure on the concept and comparison pages from local runs of the tutorials with their final settings. Its docstring has the commands.
- **Extra runs:** some figures need runs the tutorials don't do.
  - `run_aster_raw.sh` runs Tutorial 1's stereo on the raw ASTER images, for the raw-vs-orthorectified figures and the GoodPixelMap figure.
  - `run_aster_align.sh` aligns Tutorial 1's DEM to COP30 with `pc_align`, for the before-and-after difference maps on the alignment page.
  - `run_comparisons.sh` runs SETSM and CARS (both in Docker) on Tutorial 2's crops, for the comparison pages' hillshades and run metrics. `setsm_inputs.py` builds the camera files SETSM needs from the crops and the vendor XMLs; `cars_config.yaml` is the CARS config. *(Amended 2026-10-30: the tutorial no longer crops, so the script makes `cam2rpc` crops of the square for CARS and converts the full scenes to TIFF for SETSM, which runs with `-boundary_*`; `setsm_inputs.py` is gone. SETSM on `cam2rpc` crops at the images' own resolution wrote noise, matching only a few hundred points at its coarsest pyramid level; the 1.2 m crops of the earlier window had merely got away with it.)*
- **What stays the same:** ADR-0018's conventions; the PNGs are committed, and each page still says in prose where its figure comes from.

## Consequences
- **+** **Remaking them is one command** after a local run of the tutorials, for example when the tutorials' settings or `asp-plot`'s figures change.
- **+** **Provenance is in git:** which run, window and settings made each figure.
- **−** **The extra runs take time:** on a laptop, about 6 minutes for the raw ASTER run, 1 for the alignment, and 15 (SETSM) plus 8 (CARS) for the comparisons, which run amd64 images under emulation on an Apple Silicon Mac.
- **−** **Some choices are copied in:** the Tutorial 3 pair shown in the GoodPixelMap figure, the report page titles, and the SETSM camera-file fields. A change to the tutorials' data or to `asp_report`'s page titles means updating the script.

## Alternatives considered
- **Keep the scripts in the scientific workbench repo:** rejected. The figures belong to these docs and should be remade from this repo.
- **Make the figures in the notebooks and copy them:** the notebooks don't make most of these figures (raw vs orthorectified, before and after alignment), and the docs need some in other layouts.
