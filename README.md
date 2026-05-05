# stereopipeline-quickstart

A guide to the [NASA Ames Stereo Pipeline (ASP)](https://stereopipeline.readthedocs.io/), runnable in a pre-configured GitHub Codespace with ASP and [`asp_plot`](https://asp-plot.readthedocs.io/) installed.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/uw-cryo/stereopipeline-quickstart?quickstart=1)
[![Documentation Status](https://readthedocs.org/projects/stereopipeline-quickstart/badge/?version=latest)](https://stereopipeline-quickstart.readthedocs.io/)

> Status: early draft. Tutorials cover ASTER (Mt. Rainier) and WorldView-3 (UCSD). Data is openly available; no NASA Earthdata or Vantor credentials required.

> Have a `.edu` email? Apply to the [GitHub Student Developer Pack](https://education.github.com/pack) (or [GitHub for Teachers](https://education.github.com/teachers) for faculty) for a larger monthly Codespaces allowance.

## What this is

The Ames Stereo Pipeline produces digital elevation models (DEMs) from stereo imagery. `stereopipeline-quickstart` is a guided introduction: launch a Codespace, run the notebooks, inspect the output with `asp_plot`.

The companion package [`asp_plot`](https://github.com/uw-cryo/asp_plot) handles visualization: diagnostic plots, PDF reports, ICESat-2 comparisons.

## Two ways to use this

### 1. Run in the browser (recommended for first-time users)

Click "Open in GitHub Codespaces" above. The Codespace pulls a pre-built container image with ASP and `asp_plot` already installed, then opens VS Code in your browser. Open a notebook under `notebooks/` and run cells top-to-bottom.

The two tutorials use openly available data; no API keys, no Earthdata login required:

| Tutorial | Sensor | Region | Data source |
|---|---|---|---|
| `01_aster_rainier.ipynb` | ASTER L1A | Mt. Rainier, WA | Zenodo (10.5281/zenodo.7972223) |
| `02_worldview_ucsd.ipynb` | WorldView-3 | UCSD campus, San Diego | SpaceNet CORE3D (AWS S3) |

### 2. Read the static docs

For concepts, parameter cheatsheet, and pre-rendered notebook output, visit [stereopipeline-quickstart.readthedocs.io](https://stereopipeline-quickstart.readthedocs.io/).

## What you'll learn

- The mental model. Why stereo, what bundle adjustment is for, when to mapproject, what `pc_align` does.
- The toolchain. `parallel_stereo`, `bundle_adjust`, `point2dem`, `mapproject`, `pc_align`, `geodiff`.
- Reading the outputs. How to use `asp_plot` to check disparity, residuals, and DEM quality, and how to generate a PDF report.
- Two workflows. A medium-resolution ASTER pipeline (~15 m DEM) and a high-resolution WorldView-3 pipeline (~1 m DEM).

## Local install (no Codespace)

1. Install ASP. [Download a binary release](https://github.com/NeoGeographyToolkit/StereoPipeline/releases) and add `bin/` to your `PATH`.
2. Install `asp_plot` via `pip install asp-plot` or `conda install -c conda-forge asp-plot`.
3. Clone this repo and `pip install -r requirements.txt` for notebook dependencies.

See [`docs/start/installation.md`](docs/start/installation.md) for details.

## Related

- [`NeoGeographyToolkit/StereoPipeline`](https://github.com/NeoGeographyToolkit/StereoPipeline) — ASP itself
- [`uw-cryo/asp_plot`](https://github.com/uw-cryo/asp_plot) — visualization companion (used heavily here)
- [`uw-cryo/asp_tutorials`](https://github.com/uw-cryo/asp_tutorials) — earlier tutorial repo this one evolves from
- [ASP documentation](https://stereopipeline.readthedocs.io/) — canonical reference

## License

BSD 3-Clause. See [LICENSE](LICENSE).
