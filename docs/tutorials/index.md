# Tutorials

Two end-to-end notebooks. Both use openly available data; no NASA Earthdata or Vantor credentials, no API keys.

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
- `bundle_adjust` on full images
- `mapproject` to the COP-DEM grid
- `parallel_stereo` on the mapprojected pair
- `asp_plot --pc_align` for ICESat-2 alignment

Output: ~1 m DEM of UCSD campus.
:::
::::

## Suggested order

If you've never run ASP before, do the ASTER tutorial first. It has fewer parameters, and a coarser resolution.

The WorldView tutorial then adds bundle adjustment, cropping, and a finer resolution, higher accuracy result.

## Beyond the tutorials

The [`asp_plot` example notebooks](https://asp-plot.readthedocs.io/en/latest/examples/index.html) cover jitter correction, planetary missions (LRO NAC, Mars MOC NA, CTX), no-mapprojection variants, and scene selection.
