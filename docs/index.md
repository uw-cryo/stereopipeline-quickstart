# stereopipeline-quickstart

A guide to the NASA Ames Stereo Pipeline (ASP), runnable in a pre-configured GitHub Codespace with ASP and [`asp_plot`](https://asp-plot.readthedocs.io/) installed.

```{button-link} https://codespaces.new/uw-cryo/stereopipeline-quickstart?quickstart=1
:color: primary
:expand:
Open this repo in a GitHub Codespace
```

This site is the static companion to the [GitHub repo](https://github.com/uw-cryo/stereopipeline-quickstart). The repo contains the notebooks; this site explains why each step exists.

## Pick your path

::::{grid} 1 1 2 3
:gutter: 3

:::{grid-item-card} New to stereo photogrammetry
:link: start/what-is-asp
:link-type: doc
What ASP does, what a "stereo pipeline" is, and where the moving parts fit. Read this first if you're not sure why bundle adjustment exists.
:::

:::{grid-item-card} Ready to run something
:link: start/codespaces
:link-type: doc
Launch the Codespace, open a notebook, hit Run All.
:::

:::{grid-item-card} Want a deeper concept primer
:link: concepts/pipeline-overview
:link-type: doc
The end-to-end mental model: from raw imagery to aligned DEM. With diagrams.
:::

:::{grid-item-card} Want to run the tutorials
:link: tutorials/index
:link-type: doc
Two walkthroughs: ASTER (medium-res) and WorldView-3 (high-res). Both fully open.
:::

:::{grid-item-card} Need to look something up
:link: reference/glossary
:link-type: doc
Glossary, ASP output-file naming, parameter cheat sheet, links to the canonical ASP docs.
:::

:::{grid-item-card} Want pretty plots from your run
:link: concepts/visualization
:link-type: doc
How `asp_plot` produces diagnostic figures, PDF reports, and ICESat-2 comparisons.
:::
::::

## What this is not

A replacement for the [official ASP documentation](https://stereopipeline.readthedocs.io/). ASP has hundreds of options for dozens of sensors. This guide covers the path of least resistance: two openly-available datasets, a small set of parameters, and explanations of why each step exists. The official docs are the authoritative reference.

## Contents

```{toctree}
:maxdepth: 2
:caption: Get started

start/what-is-asp
start/codespaces
```

```{toctree}
:maxdepth: 2
:caption: Concepts

concepts/pipeline-overview
concepts/stereo-photogrammetry
concepts/bundle-adjustment
concepts/orthorectification
concepts/alignment
concepts/visualization
```

```{toctree}
:maxdepth: 2
:caption: Tutorials

tutorials/index
tutorials/01_aster_rainier
tutorials/02_worldview_ucsd
```

```{toctree}
:maxdepth: 2
:caption: Reference

reference/glossary
reference/output-files
reference/installation
reference/further-reading
```
