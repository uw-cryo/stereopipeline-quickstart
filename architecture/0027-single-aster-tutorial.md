# 27. One ASTER tutorial: orthorectify, then `asp_mgm`, on a window around the summit

- **Date:** 2026-10-26
- **Status:** Accepted; supersedes [0023](0023-split-aster-tutorial.md) and the two-report design of [0008](0008-aster-cop30-two-reports.md)
- **Context doc:** `ARCHITECTURE.md` § ASTER tutorial

## Context
[ADR-0023](0023-split-aster-tutorial.md) split the ASTER material into a fast quick look (Tutorial 1: the whole raw scene through `asp_bm` with `--subpixel-mode 1`, about 5 minutes of stereo in a 4-core Codespace) and an orthorectified pass (Tutorial 2: COP30, `mapproject`, `asp_mgm` with `--subpixel-mode 9`, about 19 minutes). The quick look's DEM is the first result a new user sees, and a colleague found stair-steps in it.

Seven variants of the quick look's stereo step were compared on the same raw images (laptop, 4-core settings):

- The stair-steps are pixel-locking from `--subpixel-mode 1`, which ASP's documentation calls a draft mode. Its disparities have a spike at exactly whole pixels.
- `asp_bm` with subpixel modes 3 or 2 removes the locking, but block matching on these images still smooths away ridges and gorges, at about 4.7× and 17× the run time.
- `asp_mgm` with `--subpixel-mode 9`, the settings of ASP's own ASTER example, keeps ridges, gorges and the texture of the summit glaciers. On a window of about 31 km around the summit it runs in about the quick look's old time.
- Raw images still leave a gap at the snow-covered summit; orthorectifying onto COP30 first fills it and sharpens the DEM.

With both tutorials on `asp_mgm` over the same window, Tutorial 2 took only about 3 minutes longer than Tutorial 1, and gave the better DEM. A separate quick look no longer saved enough time to be worth a second notebook, and it showed a new user the worse result first.

## Decision
One ASTER tutorial, `01_aster_rainier.ipynb`, runs the standard workflow on a processing window around the summit (`T_PROJWIN`, about 38 × 36 km), and shows the data after each step with `asp-plot` calls written into the cells:

1. Download and `aster2asp`; the download script also fetches the COP30 reference DEM for the window from a release, so a prebuilt Codespace already has it.
2. The stereo geometry (`StereoGeometryPlotter`).
3. The raw images (`Raster`, `Plotter.plot_array`).
4. `mapproject` both views onto COP30 over the window (`--t_projwin`).
5. The orthorectified images.
6. `parallel_stereo` with `asp_mgm` and `--subpixel-mode 9`, `point2dem` at 30 m, and a hillshade.
7. `asp_report`, now with the COP30 reference and the stereo geometry.

`02_aster_rainier_ortho.ipynb` is removed. The shipped ICESat-2 points and figure selections ([ADR-0022](0022-ship-icesat2-data.md)) were regenerated for the window. They ship on release `aster-rainier-2026-10-27` together with the COP30 clip (5 MB, made once with `fetch_cop_dem.py`, then rewritten with its CRS inside the GeoTIFF: `fetch_cop_dem.py` writes a 3D CRS that GDAL keeps in a `.aux.xml` sidecar, and ASP can't place the DEM without it), so the tutorial needs neither SlideRule nor AWS; fetching the clip from AWS on every run was slow wherever no prebuild had done it.

## Consequences
- **+** The first DEM a new user sees has no stair-steps and no summit gap, in about 10 minutes.
- **+** Each step has a figure, so the notebook shows what `aster2asp`, orthorectification and stereo each do, not only the final report.
- **+** The report's DEM figure has its reference-difference panel and the stereo-geometry figure, which the quick look lacked.
- **−** The tutorial no longer compares raw and orthorectified stereo side by side; the orthorectification concept page keeps a figure of that comparison.
- **−** It covers a window, not the whole scene. Dropping `--t_projwin` (with a reference DEM for the whole scene) restores it, at several times the run time.
- **−** The triangulation-error panel shows along-track banding (about 20–35 m) from the ASTER cameras, which none of these settings changes.

## Alternatives considered
- **Keep two notebooks, with the quick look on `asp_mgm` over the same window** — built and tested first (raw stereo about 5 minutes, orthorectified about 8). Rejected for the reasons in Context.
- **Keep `asp_bm` and change only the subpixel mode** — rejected: no stair-steps, but still smooth, and 4.7× to 17× slower.
- **A gentler site than Rainier** — not needed once orthorectification fills the summit.
