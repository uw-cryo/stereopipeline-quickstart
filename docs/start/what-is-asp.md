# What is the Ames Stereo Pipeline?

```{admonition} Work in progress
:class: warning
Placeholder content. Being rewritten with figures.
```

The NASA Ames Stereo Pipeline (ASP) is open-source software that turns pairs (or sets) of overlapping satellite or planetary images into digital elevation models (DEMs).

## A short history

<!-- FIGURE IDEA: timeline graphic — ASP releases vs major sensor-support milestones (HiRISE, MOC, WorldView, ASTER, CSM/jitter). Could be a horizontal timeline with sensor icons. -->

ASP began at NASA Ames in the late 2000s for planetary stereo (Mars, Moon) and grew to support Earth-observation sensors; it remains actively developed at NASA Ames Research Center.

## A toolchain of modular executables

<!-- FIGURE IDEA: block diagram of the ASP binaries with arrows showing data flow (raw imagery → aster2asp/wv_correct → bundle_adjust → mapproject → parallel_stereo → point2dem → pc_align → DEM). Each block labeled with the CLI tool name; arrows annotated with the file types passed between. -->

ASP is not one program but dozens of single-purpose command-line binaries (`bundle_adjust`, `mapproject`, `parallel_stereo`, `point2dem`, `pc_align`, ...) that pipe outputs into each other. This UNIX-style modularity is powerful but means the workflow is expressed as a sequence of CLI invocations.

## Why "stereo"?

<!-- FIGURE IDEA: classic two-camera parallax diagram — a tall feature (mountain or building) seen from two satellite positions, with rays from each camera converging on the feature. Pixel positions on each sensor offset by an amount proportional to height. Caption emphasizes "parallax encodes height". -->

A single satellite image cannot recover height; two images of the same ground from different angles produce parallax, which encodes height.

## Where `asp_plot` fits

[`asp_plot`](https://asp-plot.readthedocs.io/) reads ASP's scattered output files and produces diagnostic figures and PDF reports; it's used at every step of this guide.

## What's next

- [Pipeline overview](../concepts/pipeline-overview.md) — the full flow.
- [Open the Codespace](codespaces.md) — run a real pipeline.
- [ASTER tutorial](../tutorials/01_aster_rainier.ipynb) — gentlest end-to-end notebook.
