# Further reading

## ASP itself

- **[ASP documentation](https://stereopipeline.readthedocs.io/)** — the canonical reference. Hundreds of pages, very thorough.
- **[ASP examples](https://stereopipeline.readthedocs.io/en/latest/examples.html)** — per-sensor recipes (DigitalGlobe, ASTER, HiRISE, CTX, MOC, LRO NAC, Pleiades, SPOT, Cassini, …). When you need to process a sensor we don't cover, start here.
- **[ASP GitHub](https://github.com/NeoGeographyToolkit/StereoPipeline)** — source, releases, issues.

## Visualization and diagnostics

- **[`asp_plot` documentation](https://asp-plot.readthedocs.io/)** — full API reference + example notebooks for jitter correction, planetary missions, no-mapprojection workflows, scene selection.

## Reference data

- **[Copernicus DEM on AWS](https://registry.opendata.aws/copernicus-dem/)** — global 30 m DEM, free, no auth.
- **[ICESat-2 ATL06](https://nsidc.org/data/atl06)** — the underlying altimetry product. Use [SlideRule](https://slideruleearth.io/) for cloud-native access.
- **[USGS 3DEP](https://www.usgs.gov/3d-elevation-program)** — high-resolution US elevation data, useful for validating Earth DEMs.
- **[NASA Earthdata](https://search.earthdata.nasa.gov/)** — ASTER L1A, MODIS, Landsat, and most other NASA products.
- **[NASA ODE GDS](https://ode.rsl.wustl.edu/)** — planetary altimetry (LOLA, MOLA) and imagery archives.

## Companion repositories

- **[uw-cryo/asp_plot](https://github.com/uw-cryo/asp_plot)** — visualization companion (heavily used here).
- **[uw-cryo/asp_tutorials](https://github.com/uw-cryo/asp_tutorials)** — earlier tutorial repo. Some of the example data here originates there.
- **[uw-cryo/skysat_stereo](https://github.com/uw-cryo/skysat_stereo)** — high-cadence Planet imagery + ASP.
- **[uw-cryo/wv_stereo_processing](https://github.com/uw-cryo/wv_stereo_processing)** — production-grade WorldView pipelines.
- **[NeoGeographyToolkit/StereoPipelineSolvedExamples](https://github.com/NeoGeographyToolkit/StereoPipelineSolvedExamples)** — solved examples shipped with ASP itself.

## Related communities

- **[ASP support group](https://groups.google.com/g/ames-stereo-pipeline-support)** — best place to ask sensor-specific questions. 
- **[ASP issue tracker](https://github.com/NeoGeographyToolkit/StereoPipeline/issues)** — place to note bugs in ASP.
