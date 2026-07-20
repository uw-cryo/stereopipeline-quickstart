# Further reading

## ASP itself

- **[ASP documentation](https://stereopipeline.readthedocs.io/)** — the canonical reference. Hundreds of pages, very thorough.
- **[ASP examples](https://stereopipeline.readthedocs.io/en/latest/examples.html)** — per-sensor recipes (DigitalGlobe, ASTER, HiRISE, CTX, MOC, LRO NAC, Pleiades, SPOT, Cassini, …). When you need to process a sensor we don't cover, start here.
- **[ASP GitHub](https://github.com/NeoGeographyToolkit/StereoPipeline)** — source, releases, issues.
- **[ASP support group](https://groups.google.com/g/ames-stereo-pipeline-support)** — best place to ask sensor-specific questions. 

## Stereo concepts, explained elsewhere

- **[CARS technical foundations](https://cars.readthedocs.io/en/stable/technical_foundations/index.html)** — CNES's illustrated walk from a stereo pair to a DSM. A good second telling of the story this guide's [concept pages](../concepts/pipeline-overview.md) tell.
- **[PGC introduction to stereoscopic imagery](https://www.pgc.umn.edu/guides/stereo-derived-elevation-models/introduction-to-stereoscopic-imagery/)** — how in-track and cross-track stereo collection works, from the group behind ArcticDEM.
- **[UP42 on DEMs, DSMs, and DTMs](https://up42.com/blog/everything-you-need-to-know-about-digital-elevation-models-dem-digital)** — the elevation-model vocabulary sorted out.

## Visualization and diagnostics

- **[`asp-plot` documentation](https://asp-plot.readthedocs.io/en/latest/)** — full API reference + example notebooks for jitter correction, planetary missions, workflows that skip orthorectification, scene selection.

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
