# 21. Bound asp-plot to one major version

- **Date:** 2026-10-22
- **Status:** Accepted
- **Context doc:** `ARCHITECTURE.md` § asp-plot: bounded to one major version

## Context
The repo required `asp-plot>=1.19.0` with no upper bound, and `build-image.yml` rebuilds the container monthly. The 2026-10-01 rebuild installed asp_plot 3.4.0, which carries two breaking releases:

- 2.0.0 renamed the `asp_plot` CLI to `asp_report` and `StereoGeometryPlotter.dg_geom_plot()` to `stereo_geom_plot()`, with no aliases.
- 3.0.0 hyphenated every CLI option (`--stereo_directory` → `--stereo-directory`) and turned boolean options into single switches (`--plot_geometry False` → `--no-geometry`).

The committed notebooks still used the 1.x names, so the published Codespace image no longer ran them. The report cells failed quietly: a `!` shell magic prints `asp_plot: command not found` instead of raising. Nothing flagged the break. Unlike ASP ([ADR-0014](0014-asp-version-tracking.md)), asp_plot has no version-check workflow, and the image rebuild has no notebook smoke test.

## Decision
Update the notebooks and docs to the asp_plot 3.x names and require `asp-plot>=3.4,<4` in `requirements.txt`, `.devcontainer/environment.yml`, and the install snippets in `docs/reference/installation.md`. Minor and patch releases still flow in through the monthly rebuild; a new major version is adopted by a manual bump.

## Consequences
- **+** A monthly rebuild can no longer pull in a release that asp_plot's semantic versioning marks as breaking.
- **+** Local installs following `installation.md` get the same range as the Codespace.
- **−** New asp_plot major versions are not picked up until someone bumps the bound, and nothing currently reports that one exists.
- **−** A breaking change shipped in a minor release would still get through.

## Alternatives considered
- **Exact pin (`==3.4.0`)** — rejected: drops asp_plot's bug fixes and report improvements between deliberate bumps, and asp_plot follows semantic versioning.
- **Stay unbounded and fix forward** — rejected: that is how the break happened; the image would keep breaking silently on each major release.
- **An asp-plot version-check workflow like ADR-0014's** — not adopted now; worth revisiting if major releases keep coming at the 2026 pace (2.0 to 3.0 in under a month).
