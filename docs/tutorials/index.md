# Tutorials

Three end-to-end notebooks. All use openly available data; no NASA Earthdata or Vantor credentials, no API keys.

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 1. ASTER Mt. Rainier
:link: 01_aster_rainier
:link-type: doc

Stereo from a single ASTER L1A scene. The gentlest end-to-end flow:
- `aster2asp` to extract nadir + back-looking views
- `parallel_stereo` (raw, then mapprojected for cleaner output)
- `point2dem` to grid the result
- `asp_plot` for diagnostics + PDF report

Output: ~30 m DEM of Mt. Rainier.
:::

:::{grid-item-card} 2. WorldView-3 UCSD
:link: 02_worldview_ucsd
:link-type: doc

Stereo from a high-resolution commercial-style WV3 pair (SpaceNet CORE3D, openly hosted on AWS). The full recipe:
- Stereo geometry analysis with `StereoGeometryPlotter`
- COP-DEM clip from AWS Open Data
- `mapproject` to the COP-DEM grid
- `parallel_stereo` on the mapprojected pair
- `asp_plot --pc_align` for ICESat-2 alignment

Output: 2 m DEM over University City, San Diego.
:::

:::{grid-item-card} 3. WorldView-3 UCSD with bundle adjustment
:link: 03_worldview_ucsd_ba
:link-type: doc

Variant of Tutorial 2 that adds `bundle_adjust` to refine the vendor RPC cameras before orthorectification. Outputs are suffixed `_ba`, so both runs share a data directory and the two `asp_plot` reports can be compared side by side.
:::
::::

## Suggested order

If you've never run ASP before, do the ASTER tutorial first. It has fewer parameters, and a coarser resolution.

The WorldView tutorial then adds cropping and a finer resolution, higher accuracy result. The bundle-adjustment variant comes last: run it after Tutorial 2 and compare the reports to see what camera refinement adds.

## Beyond the tutorials

The [`asp_plot` example notebooks](https://asp-plot.readthedocs.io/en/latest/examples/index.html) cover jitter correction, planetary missions (LRO NAC, Mars MOC NA, CTX), no-mapprojection variants, and scene selection.
