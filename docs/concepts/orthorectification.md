# Orthorectification

```{note}
ASP calls this step "mapprojection" in its toolchain (the binary is `mapproject`, the bundle-adjust flag is `--mapproj-dem`). This guide uses "orthorectification" — the more standard photogrammetry term — for the concept while keeping ASP's tool names verbatim.
```

Resampling each input image onto a reference DEM grid before stereo turns a wide-search-range matching problem into a small-disparity one.

## Why it helps

Raw images of the same terrain from two viewpoints differ a lot: the satellite geometry shifts every pixel, and relief shifts them further. To find a pixel's match, the correlator has to search a wide range, which is slow and error-prone. Orthorectifying both images onto the same reference DEM removes most of that geometric difference up front, so the correlator only searches a small range around each pixel.

![Orthorectification shrinks the search range stereo matching must cover](figures/ortho-search-range.svg)

Measured on the ASTER tutorial pair over the tutorial's window, run both ways with the tutorial's matcher settings: the spread of horizontal {term}`disparity <disparity map>` the correlator has to cover (1st to 99th percentile) drops from about 140 pixels to about one.

![Disparity histograms for the same ASTER pair, raw vs orthorectified](figures/aster-disparity-hist.png)

After orthorectification, the residual disparity is dominated by error in the reference DEM (small) rather than satellite geometry (large).

## When you can skip it

Very flat terrain, missing reference DEMs, or quick first passes can use ASP's `--alignment-method affineepipolar` instead, which aligns the images with a single image-wide transformation rather than a per-pixel one. The ASTER tutorial's first pass runs this way.

## What reference DEM to use

| Reference | Coverage | Notes |
|---|---|---|
| [Copernicus GLO-30](https://registry.opendata.aws/copernicus-dem/) | global | free on AWS Open Data; what the tutorials use (see [Data sources and licences](../reference/data.md) for the required notice) |
| [USGS 3DEP](https://www.usgs.gov/3d-elevation-program) | United States | lidar-derived, high resolution |
| [ArcticDEM](https://www.pgc.umn.edu/data/arcticdem/) | Arctic | WorldView-derived strips and mosaics |
| [REMA](https://www.pgc.umn.edu/data/rema/) | Antarctica | WorldView-derived strips and mosaics |
| MOLA | Mars | mission altimetry |
| LOLA | Moon | mission altimetry |

ASP expects DEM heights above the {term}`ellipsoid`, but many products (including COP30) ship heights above a {term}`geoid`. Feeding a geoid-referenced DEM to `mapproject` introduces a vertical bias of tens of meters. The tutorials' `fetch_cop_dem.py` script applies the geoid-to-ellipsoid shift for you; if you bring your own reference DEM, check its vertical datum first.

## Two-pass processing

When you have no good reference DEM, produce one: run a coarse first stereo pass on the raw imagery, then orthorectify against that DEM and re-run stereo. Your own first-pass DEM is more locally accurate than a global reference.

![Two-pass recipe: a coarse first DEM feeds orthorectification for a refined second pass](figures/two-pass-flow.svg)

The [ASTER tutorial](../tutorials/01_aster_rainier.ipynb) skips the first pass and orthorectifies straight onto COP30. The {term}`hillshades <hillshade>` below are the same two runs over the Mount Rainier massif, without and with orthorectification: the raw run has holes around the summit and on the east side, and smooths out the ridges and valleys; the orthorectified run keeps them.

![Hillshades of DEMs from the ASTER tutorial's raw and orthorectified images over Mount Rainier](figures/aster-raw-vs-ortho-hillshade.png)

## Where to read more

- [ASP mapproject docs](https://stereopipeline.readthedocs.io/en/latest/tools/mapproject.html)
- [ASP stereo with mapprojected images](https://stereopipeline.readthedocs.io/en/latest/examples/aster.html#aster)
