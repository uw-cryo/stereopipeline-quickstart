# Tutorials

Four end-to-end notebooks, in two pairs: each second notebook adds a processing step to the first, and their reports line up for comparison. Run times are for the default 4-core Codespace. All use openly available data; no NASA Earthdata or Vantor credentials, no API keys.

```{admonition} To run these notebooks, launch the Codespace first
:class: important
The tutorial pages below are static renders of the notebooks in `notebooks/`, shown with saved outputs. To run them yourself, [open this repo in a GitHub Codespace](../start/codespaces.md); it boots with ASP, `asp-plot`, and the demo data scripts already installed, so the notebooks run top to bottom with no setup. Running on your own machine instead needs the [local install](../reference/installation.md).
```

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 1. ASTER Mt. Rainier, quick look
:link: 01_aster_rainier
:link-type: doc

Stereo from a single ASTER L1A scene with ASP's fastest settings. The simplest end-to-end flow:
- `aster2asp` to extract nadir + back-looking views
- `parallel_stereo` (`asp_bm`) + `point2dem` on the raw imagery
- `asp-plot` PDF report

Output: a ~30 m DEM of Mt. Rainier. Run time: ~6 min.
:::

:::{grid-item-card} 2. ASTER Mt. Rainier, orthorectified
:link: 02_aster_rainier_ortho
:link-type: doc

The same scene, processed the slower, higher-quality way:
- COP-DEM clip from AWS Open Data
- `mapproject` both views onto it
- `parallel_stereo` (`asp_mgm`, subpixel mode 9) on the orthorectified pair
- `asp-plot` PDF report that lines up panel for panel with Tutorial 1's

Output: an orthorectified ~30 m DEM of Mt. Rainier. Run time: ~20 min.
:::

:::{grid-item-card} 3. WorldView-3 UCSD
:link: 03_worldview_ucsd
:link-type: doc

Stereo from a high-resolution commercial-style WV3 pair (SpaceNet CORE3D, openly hosted on AWS). Steps:
- Stereo geometry analysis with `StereoGeometryPlotter`
- COP-DEM clip from AWS Open Data
- `mapproject` to the COP-DEM grid
- `parallel_stereo` on the orthorectified pair
- `asp_plot` PDF report with ICESat-2 alignment (`pc_align` runs by default)

Output: 4 m DEM of the UCSD campus and sea cliffs. Run time: ~6 min.
:::

:::{grid-item-card} 4. WorldView-3 UCSD with bundle adjustment
:link: 04_worldview_ucsd_ba
:link-type: doc

Variant of Tutorial 3 that adds `bundle_adjust` to refine the vendor RPC cameras before orthorectification. Outputs are suffixed `_ba`, so both runs share a data directory and the two `asp-plot` reports can be compared side by side. Run time: ~20 min, most of it bundle adjustment.
:::
::::

## Suggested order

If you've never run ASP before, start with Tutorial 1, the ASTER quick look. It has the fewest parameters and the coarsest resolution.

Tutorial 2 processes the same ASTER scene with orthorectification and a slower, higher-quality matcher; compare its report with Tutorial 1's. The WorldView tutorial then adds cropping and a finer resolution, higher accuracy result. The bundle-adjustment variant comes last: run it after Tutorial 3 and compare the reports to see what camera refinement adds.

## Beyond the tutorials

The [`asp-plot` example notebooks](https://asp-plot.readthedocs.io/en/latest/examples/index.html) cover jitter correction, planetary missions (LRO NAC, Mars MOC NA, CTX), variants that skip orthorectification, and scene selection.

If a notebook fails or a step is unclear, [open a problem report](https://github.com/uw-cryo/stereopipeline-quickstart/issues/new?template=problem-report.yml).
