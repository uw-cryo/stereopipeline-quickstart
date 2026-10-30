# Tutorials

Three end-to-end notebooks: the ASTER tutorial, then two WorldView-3 tutorials on the same window: one pair, then three images blended. Run times are for the default 4-core Codespace. All use openly available data; no NASA Earthdata or Vantor credentials, no API keys.

```{admonition} To run these notebooks, launch the Codespace first
:class: important
The tutorial pages below are static renders of the notebooks in `notebooks/`, shown with saved outputs. To run them yourself, [open this repo in a GitHub Codespace](../start/codespaces.md); it boots with ASP, `asp-plot`, and the demo data scripts already installed, so the notebooks run top to bottom with no setup. Running on your own machine instead needs the [local install](../reference/installation.md).
```

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 1. ASTER Mt. Rainier
:link: 01_aster_rainier
:link-type: doc

From a single ASTER L1A scene to a DEM, on a window around the summit, with `asp-plot` figures after each step:
- `aster2asp` to extract nadir + back-looking views, and the stereo geometry
- `mapproject` both views onto a COP30 reference DEM
- `parallel_stereo` (`asp_mgm`, subpixel mode 9) + `point2dem`
- `asp-plot` PDF report

Output: a ~30 m DEM of Mt. Rainier. Run time: ~10 min.
:::

:::{grid-item-card} 2. WorldView-3 UCSD
:link: 02_worldview_ucsd
:link-type: doc

Stereo from a high-resolution WorldView-3 pair over Los Peñasquitos Canyon, a nature preserve on the north edge of San Diego (SpaceNet CORE3D, openly hosted on AWS), at the images' own 0.3 m resolution on a 1 km square. Steps:
- Stereo geometry with `StereoGeometryPlotter`
- `mapproject` of just the area out of each full image, onto a COP30 reference DEM
- `parallel_stereo` (`asp_mgm`, subpixel mode 9, census cost) + `point2dem`
- `asp-plot` PDF report with ICESat-2 alignment (`pc_align` runs by default)

Output: a 1 m DEM of the west end of Los Peñasquitos Canyon. Run time: ~12 min, 2 of them downloading.
:::

:::{grid-item-card} 3. WorldView-3 Los Peñasquitos Canyon, three images blended
:link: 03_worldview_ucsd_blend
:link-type: doc

Adds a third image of the same area: bundle adjusts all three cameras on the orthoimages, runs stereo on each of the three pairs, and averages the three DEMs with `dem_mosaic` into one with fewer holes and less noise. Run time: ~23 min after Tutorial 2.
:::
::::

## Suggested order

If you've never run ASP before, start with Tutorial 1, the ASTER tutorial. It has the fewest parameters and the coarsest resolution.

The WorldView tutorials then add cropping, bundle adjustment and a much finer resolution. Tutorial 3 reuses Tutorial 2's downloads and crops, so run it second.

## Beyond the tutorials

The [`asp-plot` example notebooks](https://asp-plot.readthedocs.io/en/latest/examples/index.html) cover jitter correction, planetary missions (LRO NAC, Mars MOC NA, CTX), variants that skip orthorectification, and scene selection.

If a notebook fails or a step is unclear, [open a problem report](https://github.com/uw-cryo/stereopipeline-quickstart/issues/new?template=problem-report.yml).
