# Orthorectification

```{admonition} Work in progress
:class: warning
Placeholder content. Being rewritten with figures.
```

```{note}
ASP calls this step "mapprojection" in its toolchain (the binary is `mapproject`, the bundle-adjust flag is `--mapproj-dem`). This guide uses "orthorectification" — the more standard photogrammetry term — for the concept while keeping ASP's tool names verbatim.
```

Resampling each input image onto a reference DEM grid before stereo turns a wide-search-range matching problem into a small-disparity one.

## The intuition

<!-- FIGURE IDEA: two-panel disparity-range diagram. Left: raw stereo, large search box per pixel. Right: post-orthorectification, tiny search box per pixel. Overlay the actual disparity histogram from the WV3 tutorial showing the dramatic reduction in spread. -->

After orthorectification, residual disparity is dominated by error in the reference DEM (small) rather than satellite geometry (large), making stereo matching far easier.

## When you can skip it

Very flat terrain, missing reference DEMs, or quick first passes can use ASP's `--alignment-method affineepipolar` instead.

## What reference DEM to use

<!-- FIGURE IDEA: world map shaded by reference-DEM coverage and resolution: COP30 globally, 3DEP / ArcticDEM / REMA highlighted regions. Companion to the table the rewrite will eventually re-introduce. -->

For Earth, Copernicus GLO-30 (free, on AWS Open Data) is the default; planetary bodies have their own canonical DEMs (MOLA, LOLA, etc.).

## The two-pass trick

<!-- FIGURE IDEA: flow diagram of the two-pass recipe used in the ASTER tutorial — pass 1 (raw imagery → coarse DEM) feeds into pass 2 (orthorectified imagery → refined DEM). Pair with hillshades of pass-1 vs pass-2 outputs from the actual tutorial run to show the quality gain. -->

Run a coarse first stereo pass on raw imagery, downsample its DEM, orthorectify against that DEM, and re-run stereo — your own DEM is more locally accurate than a global reference.

## Where to read more

- [ASP mapproject docs](https://stereopipeline.readthedocs.io/en/latest/tools/mapproject.html)
- [ASP stereo with mapprojected images](https://stereopipeline.readthedocs.io/en/latest/examples/aster.html#aster)
