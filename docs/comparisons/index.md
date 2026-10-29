# Alternative Open-Source Stereo Pipelines

Comparisons of ASP with other widely used open-source stereo photogrammetry pipelines, on the WorldView-3 pair of [Tutorial 2](../tutorials/02_worldview_ucsd.ipynb) (Mount Soledad, San Diego), prepared as the tutorial prepares it.

```{note}
This is not a comprehensive comparison of processing parameters between ASP, CARS, and SETSM. We make no quantitative ranking between DEM outputs.

In these sections, we seek to:

- document the processing setup for the pipelines,
- briefly discuss some key differences,
- and demonstrate reasonable, comparable results for the same stereo scenes from each tool.

We encourage users to make their own comparisons; these notes document the setup for each tool.
```

::::{grid} 1
:gutter: 3

:::{grid-item-card} SETSM
:link: setsm
:link-type: doc

Surface Extraction with TIN-based Search-space Minimization (Ohio State / PGC).
:::

:::{grid-item-card} CARS
:link: cars
:link-type: doc

CNES open-source stereo pipeline with Pandora dense matching.
:::

::::

## Key Differences

ASP is general purpose software for geodesy and stereogrammetry. It contains tooling for alignment of point clouds, structure-from-motion, jitter solving, camera intrinsic refinement, and more beyond DEM generation from stereo-pairs.

Our comparison focuses only on the standard stereo pipeline for the three tools.

| Feature | ASP | CARS | SETSM |
|---|---|---|---|
| Language | C++ | Python + C++ (pybind11) | C++ |
| Dense matching | NCC, MGM, SGM, etc. | Pandora (Census + SGM) | TIN-based NCC |
| Bundle adjustment | Separate tool (`bundle_adjust`) | Separate tool (`cars-bundleadjustment`) | None (RPC bias comp. only) |
| Install | Pre-built binaries | pip / Docker | Build from source |

```{toctree}
:maxdepth: 1
:hidden:

setsm
cars
```
