# stereopipeline-quickstart

A guide to the [NASA Ames Stereo Pipeline (ASP)](https://stereopipeline.readthedocs.io/), runnable in a pre-configured GitHub Codespace with ASP and [`asp-plot`](https://asp-plot.readthedocs.io/en/latest/) installed.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/uw-cryo/stereopipeline-quickstart?quickstart=1)
[![Documentation Status](https://readthedocs.org/projects/stereopipeline-quickstart/badge/?version=latest)](https://stereopipeline-quickstart.readthedocs.io/)

> Have a `.edu` email? Apply to the [GitHub Student Developer Pack](https://education.github.com/pack) (or [GitHub for Teachers](https://education.github.com/teachers) for faculty) for a larger monthly Codespaces allowance.

## What this is

The Ames Stereo Pipeline produces digital elevation models (DEMs) from stereo imagery. `stereopipeline-quickstart` is a guided introduction: launch a Codespace, run the notebooks, inspect the output with `asp-plot`.

The companion package [`asp-plot`](https://github.com/uw-cryo/asp_plot) handles visualization: diagnostic plots, PDF reports, ICESat-2 comparisons.

## Run in the browser (recommended for first-time users)

Click "Open in GitHub Codespaces" above. The Codespace pulls a pre-built container image with ASP and `asp-plot` already installed, then opens VS Code in your browser. Open a notebook under `notebooks/` and run cells top-to-bottom.

The tutorials use openly available data; no API keys, no Earthdata login required:

| Tutorial | Sensor | Region | Data source |
|---|---|---|---|
| `01_aster_rainier.ipynb` | ASTER L1A | Mt. Rainier, WA | Zenodo (10.5281/zenodo.7972223) |
| `02_worldview_ucsd.ipynb` | WorldView-3 | UCSD, San Diego | SpaceNet CORE3D (AWS S3) |
| `03_worldview_ucsd_ba.ipynb` | WorldView-3 | UCSD, San Diego | SpaceNet CORE3D (AWS S3) |

## Read the static docs

For explanations and conceptual background, visit [stereopipeline-quickstart.readthedocs.io](https://stereopipeline-quickstart.readthedocs.io/).

## Local install (no Codespace)

1. Install ASP. [Download a binary release](https://github.com/NeoGeographyToolkit/StereoPipeline/releases) and add `bin/` to your `PATH`.
2. Install `asp-plot` via `pip install asp-plot` or `conda install -c conda-forge asp-plot`.
3. Clone this repo and `pip install -r requirements.txt` for notebook dependencies.

See [`docs/start/installation.md`](docs/start/installation.md) for details.

## Related

- [`NeoGeographyToolkit/StereoPipeline`](https://github.com/NeoGeographyToolkit/StereoPipeline) — ASP itself
- [ASP documentation](https://stereopipeline.readthedocs.io/) — canonical reference
- [`uw-cryo/asp_plot`](https://github.com/uw-cryo/asp_plot) — visualization companion (used heavily here)
- [`uw-cryo/asp_tutorials`](https://github.com/uw-cryo/asp_tutorials) — earlier tutorial repo this one evolves from

## License

BSD 3-Clause. See [LICENSE](LICENSE).
