# stereopipeline-quickstart

Make a 3D model of the terrain from satellite images, in your browser, in about 10 minutes, with the [NASA Ames Stereo Pipeline (ASP)](https://stereopipeline.readthedocs.io/).

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/uw-cryo/stereopipeline-quickstart?quickstart=1)

## First time here? Read the guide: [stereopipeline-quickstart.readthedocs.io](https://stereopipeline-quickstart.readthedocs.io/)

You need a free [GitHub account](https://github.com/signup). There is nothing to install: the button above opens a ready-made workspace in your browser.

## What happens when you click the button

1. GitHub builds your workspace, which takes about a minute, and opens VS Code in your browser.
2. A box asks whether you trust the authors of the files in this folder. Click **Trust Folder & Continue**.
3. Tutorial 1 opens and starts running by itself. Scroll down to follow it. After about 10 minutes you have a 3D model (a DEM) of Mount Rainier and a PDF report.

## The tutorials

| Tutorial | What you get | Time |
|---|---|---|
| 1. ASTER, Mount Rainier | A 30 m DEM and a PDF report from two ASTER images of the mountain | about 10 min |
| 2. WorldView-3, Los Peñasquitos Canyon | A 1 m DEM from a sharp WorldView-3 pair over a canyon in San Diego, compared with ICESat-2 laser heights | about 12 min |
| 3. Three images blended | Three WorldView-3 pairs of the same place, blended into one DEM with fewer holes | about 22 min more |

Times are for the standard 4-core workspace. All the data is open; no login other than GitHub. The sources and licenses are listed in the guide: [Data sources and licenses](https://stereopipeline-quickstart.readthedocs.io/en/latest/reference/data.html).

The [guide](https://stereopipeline-quickstart.readthedocs.io/) explains what ASP does, each step of the pipeline, and how to read the results. ASP's own documentation is at [stereopipeline.readthedocs.io](https://stereopipeline.readthedocs.io/).

## Students and educators

GitHub gives every account free Codespaces hours each month. With a `.edu` email, the [GitHub Student Developer Pack](https://education.github.com/pack) or [GitHub for Teachers](https://education.github.com/teachers) gives more.

## Running on your own computer

1. Install ASP: [download a binary release](https://github.com/NeoGeographyToolkit/StereoPipeline/releases) and add its `bin/` to your `PATH`.
2. Install `asp-plot`: `pip install asp-plot` or `conda install -c conda-forge asp-plot`.
3. Clone this repo and run `pip install -r requirements.txt` for the notebooks' dependencies.

See [the local install guide](https://stereopipeline-quickstart.readthedocs.io/en/latest/reference/installation.html) for details.

## For contributors

The reasoning behind the repo's design is in architecture decision records under [`architecture/`](architecture/README.md), one record per consequential choice. `AGENTS.md` is the onboarding reference for contributors and coding agents, and `ARCHITECTURE.md` is the current-state map of the repo.

## Related

- [`NeoGeographyToolkit/StereoPipeline`](https://github.com/NeoGeographyToolkit/StereoPipeline): ASP itself
- [`uw-cryo/asp_plot`](https://github.com/uw-cryo/asp_plot): the visualization companion the tutorials use for their figures and reports
- [`uw-cryo/asp_tutorials`](https://github.com/uw-cryo/asp_tutorials): the earlier tutorial repo this one evolves from

## License

BSD 3-Clause. See [LICENSE](LICENSE). The tutorial data have their own licenses and credits, listed in the guide: [Data sources and licenses](https://stereopipeline-quickstart.readthedocs.io/en/latest/reference/data.html).
