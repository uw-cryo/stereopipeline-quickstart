# Architecture

The current-state codemap for this repo: what lives where and how the pieces fit. Mutable; keep it in sync with the code. The always-loaded agent/contributor onboarding (editing rules, gotchas, style conventions) is [`AGENTS.md`](AGENTS.md); the durable why behind consequential decisions lives in the architecture decision records under [`architecture/`](architecture/README.md), linked per section below.

This is a standalone repo teaching ASP itself, with `asp_plot` as the visualization layer at every step (not the subject); see [ADR-0001](architecture/0001-separate-repo.md).

## Repo layout

```
stereopipeline-quickstart/
├── README.md                          # Codespace badge + landing
├── LICENSE                            # BSD-3 (matches asp_plot)
├── AGENTS.md                          # lean agent/contributor onboarding
├── ARCHITECTURE.md                    # this file
├── architecture/                      # ADRs (why-decisions); index in architecture/README.md
├── .gitignore                         # CLAUDE/, data/, NTFs, etc.
├── requirements.txt                   # pip-only path for non-Codespace users
├── .readthedocs.yaml                  # RTD config
├── .vscode/
│   └── settings.json                  # hide AI chat panel by default; disable AI
├── .devcontainer/
│   ├── devcontainer.json              # pulls pre-built image; build: fallback
│   ├── Dockerfile                     # ASP binaries + asp_plot conda env
│   ├── environment.yml                # conda env spec (python 3.12)
│   ├── onCreate.sh                    # ASP/asp_plot health check (runs in prebuilds; no data download)
│   ├── postAttach.sh                  # opens Tutorial 1 once VS Code attaches (after the trust prompt), installs close-panel/
│   ├── close-panel/                   # tiny VS Code extension: closes the terminal panel and clears notifications once on first launch, collapses code cells, starts Tutorial 1 once, announces results zips
│   └── postStart.sh                   # (stashed; not active)
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── problem-report.yml         # reader problem-report form (linked from docs)
│   │   └── config.yml                 # routes ASP-itself questions upstream
│   └── workflows/
│       ├── build-image.yml            # GHCR build & push, monthly cron
│       └── asp-version-check.yml      # monthly ASP-release auto-bump PR
├── docs/                              # Sphinx + myst-nb (mirrors asp_plot)
│   ├── conf.py
│   ├── requirements.txt               # RTD-only deps
│   ├── _static/css/custom.css
│   ├── _static/js/external-links.js   # external links open in a new tab
│   ├── index.md                       # the beginner path: five steps with screenshots (ADR-0036); large type via a page-local style block
│   ├── start/
│   │   ├── what-is-asp.md             # fully authored; history/toolchain/CLI-vs-GUI framing
│   │   ├── codespaces.md
│   │   └── figures/                   # authored SVG diagrams (asp-timeline, asp-toolchain, parallax) + launch-*.png screenshots for the home page
│   ├── concepts/
│   │   ├── pipeline-overview.md
│   │   ├── figures/                   # authored SVG diagrams + data-figure PNGs from real runs
│   │   ├── stereo-photogrammetry.md
│   │   ├── bundle-adjustment.md
│   │   ├── orthorectification.md      # was mapprojection.md; renamed for the concept
│   │   ├── alignment.md
│   │   └── visualization.md
│   ├── comparisons/                   # ASP vs other open-source stereo pipelines
│   │   ├── index.md                   # overview + scope note + key-differences table
│   │   ├── cars.md                    # CARS (CNES) run + hillshade comparison
│   │   ├── setsm.md                   # SETSM (OSU/PGC) run + hillshade comparison
│   │   └── figures/                   # soledad-{asp,cars,setsm}-hillshade.png, from scripts/docs_figures/
│   ├── tutorials/
│   │   ├── index.md                   # tutorial gallery
│   │   └── 0*.ipynb                   # executed copies of notebooks/, for the site (scripts/execute_tutorials.py)
│   └── reference/
│       ├── glossary.md
│       ├── output-files.md
│       ├── installation.md            # local-install guide; demoted from start/
│       └── further-reading.md
├── notebooks/
│   ├── 01_aster_rainier.ipynb         # ASTER: L1A → skyplot → mapproject onto COP30 → asp_mgm 30 m DEM (summit window) + report
│   ├── 02_worldview_ucsd.ipynb        # WV3 Mount Soledad pair: cam2rpc crops → BA → mapproject → asp_mgm 2.4 m DEM + report
│   ├── 03_worldview_ucsd_blend.ipynb  # WV3 three crops → BA → three raw pairs → dem_mosaic blend + report
│   └── utils.py                       # run/run_stereo (status lines, logs, live tile map), timer, average_crop, plotting helpers
├── scripts/
│   ├── download_aster.sh              # all ASTER data from release aster-rainier-* (L1A, ICESat-2, COP30) + unzip
│   ├── download_worldview_ucsd.sh     # WV3 NTF + XML from SpaceNet's bucket over HTTPS; ICESat-2 + COP30 from release ucsd-soledad-*
│   ├── fetch_cop_dem.py               # COP30 from AWS, local geoid→ellipsoid shift
│   ├── docs_figures/                  # make_figures.py remakes docs/concepts/figures/*.png from local runs; run_aster_*.sh, run_comparisons.sh (+ setsm_inputs.py, cars_config.yaml): the extra runs it needs; annotate_screenshots.py labels the home page's Tutorial 1 screenshot
│   └── prefetch_basemap.py            # the tutorials' stereo geometry map tiles, run by onCreate.sh
└── CLAUDE/                            # gitignored; local session/design scratch notes
```

## Docs site

### Sphinx + myst-nb

Same stack as `asp_plot`; see [ADR-0003](architecture/0003-sphinx-myst-nb-docs.md). The notebooks in `notebooks/` have no outputs (a clean start in a Codespace, readable diffs). The site renders executed copies, `docs/tutorials/*.ipynb`, which `scripts/execute_tutorials.py` makes by running the notebooks in a fresh run folder and which are committed; see [ADR-0035](architecture/0035-executed-notebooks-for-the-site.md). They are remade when a tutorial changes. `nb_execution_mode = "off"` in `docs/conf.py`: RTD has no ASP, and the runs take half an hour.

Site is live at https://stereopipeline-quickstart.readthedocs.io/. RTD installs a GitHub webhook on import; pushes to `main` auto-rebuild.

Two RTD build constraints:

- `docs/requirements.txt` pins exact versions. An unpinned build resolved sphinx-book-theme 1.4 / pydata-sphinx-theme 0.20, which renders a header navbar whose search button duplicates the sidebar search field.
- `.readthedocs.yaml` overrides `build.jobs.build.html` to run sphinx **without `-j auto`** (RTD's default adds it). sphinx-tippy is not parallel-safe: pages rendered in worker processes embed references to per-page tip files that the main process never writes, so every hover preview 404s on the deployed site while working fine in a serial local build.

Import gotcha: RTD's auto-detect can flag a public repo as "private" when its cached view of the GitHub OAuth grant is stale. Fix is to **Sync** the GitHub connection under RTD account settings, or use **Import Manually** (paste URL) which skips the API visibility check.

### Docs content state

See [ADR-0004](architecture/0004-docs-wip-skeleton.md) (skeleton phase), [ADR-0017](architecture/0017-retire-per-page-wip-admonitions.md) (admonitions retired), and [ADR-0020](architecture/0020-soften-banner-issue-form.md) (banner softened). The concept/intro pages shipped as a WIP skeleton and have since been fleshed out with prose and figures (issue #6); the site-wide banner (`announcement` in `docs/conf.py`) read "In development, but ready for usage" until 2026-10-29 and now says only "Please report issues here", with the link on "here". Reader contact is the GitHub issue form (`.github/ISSUE_TEMPLATE/problem-report.yml`), linked from the banner, the landing page's "Reporting problems" section, the Codespace page, and the tutorials index. Figures that still need full processing runs are marked by the remaining HTML comments `<!-- FIGURE IDEA: ... -->`.

Figure conventions are in [ADR-0018](architecture/0018-docs-figure-conventions.md): conceptual diagrams are hand-written SVGs in a `figures/` dir next to the page, drawn on an opaque light surface so one file reads on both themes; data-backed figures are matplotlib/asp_plot PNGs from real runs, with provenance stated in the page prose. The data figures in `concepts/figures/` are made by `scripts/docs_figures/make_figures.py` from local runs of Tutorials 1 and 2 with their final settings, plus two extra runs it needs: `run_aster_raw.sh` (Tutorial 1's stereo on the raw ASTER images, for the raw-vs-orthorectified and GoodPixelMap figures) `run_aster_align.sh` (Tutorial 1's DEM aligned to COP30, for the alignment page's before-and-after maps) and `run_comparisons.sh` (SETSM and CARS in Docker on Tutorial 2's crops, for the comparison pages; `setsm_inputs.py` builds the camera files SETSM needs). Its docstring has the commands; see [ADR-0033](architecture/0033-docs-figure-scripts-in-repo.md). The figures were last remade on 2026-10-29; the earlier ones came from the tutorial configurations before [ADR-0027](architecture/0027-single-aster-tutorial.md), with scripts that were never committed.

Glossary linking is in [ADR-0019](architecture/0019-glossary-term-hover-previews.md): jargon links to `docs/reference/glossary.md` with the MyST `{term}` role at its first occurrence on a page, prose only. `sphinx-tippy` (in `docs/requirements.txt`) turns those links into hover previews, scoped to glossary anchors by `tippy_skip_urls` in `docs/conf.py`; term links get a dotted underline and the tooltip box follows the theme via `--pst-*` variables in `custom.css`. tippy.js and popper are vendored as pinned copies in `docs/_static/js/` (`tippy_js` in `conf.py`), so no CDN is involved.

### `docs/comparisons/` section

See [ADR-0009](architecture/0009-qualitative-tool-comparisons.md). A top-level section running Tutorial 2's WorldView-3 pair, as the tutorial crops it (Mount Soledad, 1.2 m crops, 2.4 m DEMs), through ASP, CARS (CNES), and SETSM (OSU/PGC), side by side and qualitative (no quantitative ranking). Remade on 2026-10-29 from the old `21deg_12d` pair with `scripts/docs_figures/run_comparisons.sh`. Unlike the concept pages these ship fully-fleshed, not WIP: `index.md` carries an overview, a scope-disclaimer note, a "Key Differences" table, and a hidden toctree over `setsm`, `cars`; `cars.md` / `setsm.md` carry full Docker recipes, config, run-metrics tables, and 2-up hillshade grids (`figures/soledad-*-hillshade.png`, committed). `docs/index.md` adds a landing card and a "Comparisons" toctree section; `docs/conf.py` needs no change (`nb_execution_mode = "off"` is global).

### "Orthorectification" (concept) vs "mapproject" (ASP tool)

See [ADR-0005](architecture/0005-orthorectification-vs-mapproject.md) and the naming rule in `AGENTS.md`. Each affected page carries a callout note surfacing the naming gap between the concept term used in prose and ASP's own tool names.

## Container and Codespace

### Pre-built image on GHCR (not built per-Codespace)

See [ADR-0006](architecture/0006-ghcr-bpurinton-namespace.md). CI builds and pushes `ghcr.io/bpurinton/stereopipeline-quickstart:latest` on every `Dockerfile` / `environment.yml` change plus a monthly cron; Codespaces pulls it. The from-source `build:` block stays commented out in `devcontainer.json` as a fallback. Hosted under the `bpurinton` namespace (not `uw-cryo`) because making a `uw-cryo` GHCR package public needs org admin. The cross-namespace push uses a classic PAT with `write:packages`, stored as the `GHCR_PAT` Actions secret; the workflow's GHCR login step uses `username: bpurinton` + that secret. To revert to `GITHUB_TOKEN` auth under the repo owner's namespace, swap those two lines and update `IMAGE_NAME`.

### Codespace machine size: 4-core floor

See [ADR-0010](architecture/0010-4-core-codespace-floor.md). `hostRequirements`: 4-core / 16 GB / 32 GB. The 16 GB / 32 GB values match GitHub's 4-core tier; raising them forces the machine back to 8 cores. The tutorials are tuned to run at this floor; larger machines work by bumping the thread/process counts and `TR`.

### Python 3.12 (not 3.11)

See [ADR-0013](architecture/0013-python-312-floor.md). The conda env is pinned to 3.12 in `environment.yml` (documented in `installation.md`) because `sliderule >= 5.3` (transitive via `asp_plot` 1.14) uses PEP 701 f-strings that only parse on 3.12+; on 3.11 `import asp_plot.altimetry` fails with a `SyntaxError`.

### asp-plot: bounded to one major version

See [ADR-0021](architecture/0021-asp-plot-major-version-bound.md). `requirements.txt`, `environment.yml`, and the install snippets in `installation.md` all require `asp-plot>=3.5,<4`. The notebooks call the `asp_report` CLI (hyphenated flags) and `StereoGeometryPlotter.stereo_geom_plot()`, both introduced in asp_plot 2.0/3.0, and `asp_report --figures-directory`, introduced in 3.5.0. Moving to a new major version is a manual bump of all three files plus a notebook check.

### PATH plumbing for ASP in the container

Two-pronged so ASP works from any shell context:

1. Image ENV: `PATH=/opt/conda/envs/asp/bin:/opt/StereoPipeline/bin:...`. Conda env first so its `python` shadows ASP's bundled `/opt/StereoPipeline/bin/python` (which has none of the conda env's packages and would break `import asp_plot`).
2. `/etc/profile.d/99-asp.sh` written in the Dockerfile, idempotently appends `/opt/StereoPipeline/bin` to PATH if it's not already there. Catches Codespaces' `loginInteractiveShell` env probe, which sources `~/.bashrc` (running `source activate asp`) and can rearrange PATH.
3. `onCreate.sh` also explicitly exports `PATH=/opt/conda/envs/asp/bin:/opt/StereoPipeline/bin:$PATH` at the top, defensively, so it doesn't depend on shell-wrapping behavior.

### Notebook kernel registration

No Jupyter kernel is registered in the image. VS Code's Jupyter extension resolves the kernel from the Python environment rather than from registered kernelspecs, and `python.defaultInterpreterPath` in `devcontainer.json` points it at `/opt/conda/envs/asp/bin/python`. The notebooks' metadata matches what VS Code writes for that environment (`kernelspec: {display_name: "asp", language: "python", name: "python3"}` plus a full `language_info` block), so opening one produces no metadata diff. A registered `asp` kernel with `kernelspec.name = "asp"` was tried and dropped in d8b2ccf: VS Code rewrote the metadata to `python3` on first open.

With every Python in the image visible, VS Code does not pick a kernel for a notebook it hasn't opened before, so the first Run All opened the kernel picker, with "Create Python Environment" as the recommended choice. `jupyter.kernels.excludePythonEnvironments` in `devcontainer.json` hides the image's other Pythons (`/opt/conda/bin/python`, `/opt/StereoPipeline/bin/python`, `/usr/bin/python3`); with `asp` the only environment left, VS Code selects it on its own (tested in a fresh Codespace on 2026-10-23). Re-registering an `asp` kernel with matching notebook metadata was tested the same day and did not help.

A new Codespace starts in Restricted Mode and asks "Do you trust the authors of the files in this folder?"; the lifecycle commands wait for that answer. `.devcontainer/postAttach.sh` (`postAttachCommand`) then opens `notebooks/01_aster_rainier.ipynb` with the remote `code` CLI, once per Codespace. The tutorials run in VS Code's notebook editor; opening them in JupyterLab instead was tried and reverted ([ADR-0025](architecture/0025-back-to-vs-code.md)). `postAttach.sh` replaced `customizations.codespaces.openFiles`, which opened the notebook before the trust prompt, in Restricted Mode, as raw JSON. With no `openFiles` at all, Codespaces opened the README preview before the trust prompt; `"openFiles": []` opens nothing (tested 2026-10-29), so the first thing a user sees is the trust dialog, then Tutorial 1. The README is written for GitHub: the button, a line pointing at the guide, and what happens after the click. Lifecycle commands may not inherit `VSCODE_IPC_HOOK_CLI`, so the script falls back to the newest `/tmp/vscode-ipc-*.sock` and `/vscode/bin/*/*/bin/remote-cli/code`. `workbench.editorAssociations` maps `*.ipynb` to the notebook editor. The same settings block turns off the YAML extension's telemetry prompt, extension recommendations, the Welcome page and tips. It also turns git off (`git.enabled: false`): the git extension asks "periodically run git fetch?" whenever `git.autofetch` is off, so setting that to `false` doesn't silence it. With git off, the explorer also loses the source-control badges and the dimmed, gitignored `data/`; `git` in a terminal still works.

Codespaces runs the lifecycle commands in a terminal and opens the panel to show it. `terminal.integrated.hideOnStartup` doesn't stop that, and `devcontainer.json` can't run VS Code commands (GitHub staff, community discussion 43125), so `postAttach.sh` zips `.devcontainer/close-panel/` into a `.vsix` with Python's `zipfile` and installs it with `code --install-extension`. On activation the extension runs `workbench.action.closePanel` and `notifications.clearAll` at 0.5, 2 and 5 s, then sets a `globalState` flag so it never runs again. The first time Tutorial 1 opens, the extension waits for the Python and Jupyter extensions plus 5 s, runs `notebook.execute`, watches the cells for an execution start for 15 s, and tries again up to four times (once, in a new Codespace, a single try did nothing and the user had to click Run All); each stage is logged with a timestamp in the "Quickstart launch" Output channel. Clearing the notifications removes the PDF viewer's one-time donation notice (`mathematic.vscode-pdf` shows it when it starts, keyed on its own `globalState`, with no setting to turn it off). `sirmspencer.vscode-autohide` was considered: it only hides the panel when the user clicks into an editor, and its hide-on-open also hides the file explorer.

### PDF viewer extension

`mathematic.vscode-pdf` (web-compatible) is in `devcontainer.json`'s `customizations.vscode.extensions`. The popular `tomoki1207.pdf` does NOT declare a `browser` entrypoint in its `package.json` and refuses to load in a browser-based Codespace.

A stash exists with an alternative approach: a `.devcontainer/postStart.sh` that launches `python -m http.server 8000`, plus a `pdf_link()` helper that prints a clickable forwarded-port URL to PDFs. Not active; kept in case the extension approach ever breaks.

### Editor settings split: workspace-wide vs Codespace-only

Two places set VS Code settings, and the split is deliberate:

- `.vscode/settings.json` (workspace scope) applies everywhere the folder is opened, local *and* Codespace. It holds only editor behavior that should always apply: `chat.disableAIFeatures`, `workbench.secondarySideBar.defaultVisibility: "hidden"`, `files.autoSaveDelay`.
- `.devcontainer/devcontainer.json` → `customizations.vscode.settings` (Remote [Codespaces] scope) applies only inside the container. Open the folder locally without "Reopen in Container" and these never apply.

The file-explorer hiding lives in the devcontainer block, not workspace settings, so it is Codespace-only. Its `files.exclude` hides infrastructure a first-time learner doesn't need — `.github`, `.devcontainer`, `.vscode`, `docs`, `architecture`, `.readthedocs.yaml`, `requirements.txt`, `.gitignore`, `AGENTS.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `LICENSE` — plus `README.md` and `scripts/` (the notebooks run the scripts; a learner doesn't need to open them), so the explorer shows only `notebooks/` and `data/`. Local development shows the full tree. `files.exclude` merges across scopes, so the empty workspace block is intentionally absent (nothing is hidden locally).

Opening the Codespace on `notebooks/` itself (`workspaceFolder`, or a `.code-workspace` file) was considered and not used: it would hide `data/`, where the outputs land and where the notebooks send users to download the report, and the lifecycle commands' `.devcontainer/` paths would need rewriting. Hiding the rest with `files.exclude` gets the same explorer with neither problem.

### A simplified window

The devcontainer block also hides the parts of the VS Code window the tutorials don't use: `workbench.statusBar.visible: false`, `workbench.layoutControl.enabled: false`, `window.commandCenter: false`, `breadcrumbs.enabled: false`, `editor.minimap.enabled: false`, `explorer.openEditors.visible: 0`. The activity bar and the tab strip stay. A first version also hid the activity bar (`workbench.activityBar.location: "hidden"`) and showed one tab at a time (`workbench.editor.showTabs: "single"`); in testing, that made moving between open files and notebooks hard, and it removed the menu: in the browser the menu lives in the activity bar (`window.menuBarVisibility` defaults to `compact` on the web), and `window.menuBarVisibility` is an application setting, which Remote settings can't change (setting it to `classic` in `devcontainer.json` had no effect). `workbench.activityBar.location: "top"` (a row of icons above the explorer, with the menu) also works; the standard left-hand activity bar was chosen as the most familiar (2026-10-26).

VS Code's server takes its environment from a login shell, and the image's `.bashrc` runs `source activate asp`, so `CONDA_PREFIX` is set in VS Code. The Python Environments extension then shows "CONDA_PREFIX is set for this VS Code session. Selection saved for new terminals only." when the `asp` kernel is selected (`condaEnvManager.ts`, whenever the selected env's path differs from `CONDA_PREFIX`). `remoteEnv` sets `CONDA_PREFIX` to empty and `CONDA_SHLVL` to `0`: clearing `CONDA_PREFIX` alone made every new terminal's `source activate asp` fail with "CondaValueError: CONDA_SHLVL is 1 but CONDA_PREFIX is unset or empty". With both, a terminal activates `asp` from scratch, and the kernel keeps the rest of the login shell's activated env (`PATH`, `PROJ_DATA`, `GDAL_DATA`). Skipping the login-shell probe (`userEnvProbe: "none"`) was tested and rejected: without `/opt/conda/bin` on `PATH`, `.bashrc`'s `source activate` isn't found.

## CI workflows

### ASP-version-check workflow

See [ADR-0014](architecture/0014-asp-version-tracking.md). Runs monthly (plus manual trigger), polls StereoPipeline releases, and opens a PR (never auto-merge) that sed-bumps the pinned version consistently across four files:

- `.devcontainer/Dockerfile` (the `ARG ASP_VERSION` / `ARG ASP_BUILD_DATE`)
- `.devcontainer/devcontainer.json` (the commented-out fallback args)
- `.github/workflows/build-image.yml` (workflow_dispatch defaults + inline default expressions)
- `docs/reference/installation.md` (local-install snippet + verify line)

One-time setup: repo Settings → Actions → General → Workflow permissions, enable "Allow GitHub Actions to create and approve pull requests". Without it, `create-pull-request` fails.

## Tutorial pipeline design

### ASTER tutorial

See [ADR-0027](architecture/0027-single-aster-tutorial.md), which supersedes the two-notebook split of [ADR-0023](architecture/0023-split-aster-tutorial.md) and the two-report design of [ADR-0008](architecture/0008-aster-cop30-two-reports.md). One notebook, `01_aster_rainier.ipynb`, runs the standard workflow on a processing window around the summit and shows the data after each step with `asp-plot` calls in the cells:

1. `download_aster.sh`: the L1A archive (a copy of the Zenodo record), the shipped ICESat-2 data and the COP30 reference DEM (`ref/cop30_rainier.tif`, the window plus 2 km, made once with `fetch_cop_dem.py` and rewritten with `gdal_translate -a_srs EPSG:32610`, so its CRS is inside the GeoTIFF rather than in an `.aux.xml` sidecar the release wouldn't carry) from release `aster-rainier-2026-10-27`, about 55 MB, so the tutorial needs no host but GitHub, no SlideRule request and no AWS fetch. The notebook's first step runs it; Codespace startup doesn't pre-fetch it ([ADR-0028](architecture/0028-tutorial-data-on-releases.md)); it fetches only the background map tiles for the stereo geometry plot, with `prefetch_basemap.py`, into `data/basemap_cache/`, which the notebook points contextily at (contextily otherwise caches tiles in a new temporary folder per Python process, and fetching them took 13-45 s; [ADR-0032](architecture/0032-prefetch-basemap-tiles.md)). Then `aster2asp`.
2. Stereo geometry: `StereoGeometryPlotter(inputs=[out-Band3N.xml, out-Band3B.xml]).stereo_geom_plot()` (skyplot + footprint map; the basemap needs internet).
3. Raw images: `Raster(fn, downsample=8).read_array()` drawn with `Plotter().plot_array()`, through a small `show_pair()` defined in the cell.
4. `mapproject` both views onto COP30 at 15 m with `--t_projwin 577305 5172975 615705 5209035` (`T_PROJWIN`, UTM 10N, about 38 × 36 km), one cell of its own.
5. The orthorectified images, with the same `show_pair()`.
6. `parallel_stereo -t aster --stereo-algorithm asp_mgm --subpixel-mode 9 --dem ref/cop30_rainier.tif` on the orthorectified pair, `point2dem --tr 30` → `stereo/run-DEM.tif`; then a hillshade from `Raster.hillshade()`.
7. `asp_report` with `--reference-dem` (the DEM figure's third panel shows the COP30 difference) and without `--no-geometry` (asp-plot reads ASTER geometry from the `aster2asp` camera XML) → `stereo/rainier_aster_report.pdf`.

`asp_mgm` stereo runs `--processes 1 --threads-multiprocess 4` for the 4-core floor.

### Tutorial data on releases

See [ADR-0028](architecture/0028-tutorial-data-on-releases.md). Each tutorial dataset has one dated release of this repo with everything it needs that may be re-hosted, as separate assets: `aster-rainier-2026-10-27` (L1A archive, ICESat-2 points and figure selections, COP30 clip) and `ucsd-soledad-2026-10-27` (ICESat-2 points, both WorldView reports' figure selections, COP30 clip). The release notes record each file's source, licence and how it was made; `docs/reference/data.md` lists the same for readers, with the Copernicus notice. The WorldView-3 imagery is IARPA CORE3D data on SpaceNet's AWS bucket, outside the bucket's CC BY-SA licence and with no redistribution grant found, so `download_worldview_ucsd.sh` fetches it from there over plain HTTPS (no AWS CLI) and it is not re-hosted. COP30 clips are rewritten with `gdal_translate -a_srs <EPSG>` before upload: `fetch_cop_dem.py` writes a 3D CRS that GDAL keeps in an `.aux.xml` sidecar, and without it ASP can't place the DEM. Large downloads go to a `.part` file first, so an interrupted one is never taken for a finished one.

Codespace startup downloads no data (`onCreate.sh` only checks the toolchain); each notebook's download cell fetches its dataset, so a Codespace always gets the release its checked-out code names.

### `--reuse-selections` for comparable reports

Every report replays shipped figure selections, so a rerun matches the committed outputs and no SlideRule request is made. The two WorldView reports share one ICESat-2 sample, so their profiles follow the same track:

- By default every report replays the sidecar shipped with the tutorial: `data/<tutorial>/icesat2_shipped/figure_selections.yml`, whose `parquet_cache` points at the shipped `atl06sr_all.parquet` beside it, so no SlideRule request is made. The download scripts fetch both with `curl -f` from the tutorial's dated release, together with its COP30 reference DEM: `download_aster.sh` from `aster-rainier-2026-10-27` (regenerated for the processing window, [ADR-0027](architecture/0027-single-aster-tutorial.md)), `download_worldview_ucsd.sh` from `ucsd-soledad-2026-10-27` (one sidecar per WorldView report, `pair_figure_selections.yml` and `blend_figure_selections.yml`, both pointing at the same parquet; [ADR-0029](architecture/0029-ucsd-soledad-tutorials.md)). Each writes the tag to `data/<tutorial>/RELEASE` and replaces shipped files from any other release. See [ADR-0022](architecture/0022-ship-icesat2-data.md) and [ADR-0028](architecture/0028-tutorial-data-on-releases.md).
- With `FRESH_ICESAT2 = True` (first code cell of each notebook), the report requests fresh data from SlideRule instead.

asp_plot writes the sidecar next to each report PDF (`<report_stem>_figure_selections.yml`) and reads it back via `asp_report --reuse-selections <path>`. The cells pass the flag only when the file exists (`reuse = ... if Path(prior).exists() else ""`), so each stays runnable standalone. The sidecar's `parquet_cache` path is resolved from the working directory, so shipped sidecars are written relative to `notebooks/`.

As of asp_plot ≥ 1.18.0 the report's Processing Parameters page also renders the reconstructed `mapproject` command(s), rebuilt from the mapprojected output GeoTIFF metadata (ASP's `mapproject` writes no log to parse). No notebook change is needed to get this; `asp_plot` produces it. This surfaces the tool name `mapproject` in the reports, consistent with [ADR-0005](architecture/0005-orthorectification-vs-mapproject.md).

### Report figures inline

PDFs open poorly in the browser-based editor, so each report cell also shows three of the report's figures below it. `asp_report --figures-directory` (asp_plot ≥ 3.5.0) keeps a copy of each figure as `NN_<title>.png` in `<stereo dir>/report_figures/`, which asp_report otherwise deletes with its `tmp_asp_report_plots/` directory. `show_report_figures()` in `notebooks/utils.py` displays the ones named in `REPORT_FIGURES` (DEM results, detailed hillshade, ICESat-2 profile), picked by title because the number shifts when a section is skipped. They are scaled to 1400 px wide, about 2.6 MB of notebook output per report; the PDF keeps them at full resolution. The two WorldView reports show the same three figures, with the ICESat-2 profile on the same track.

The notebooks' prose follows [ADR-0034](architecture/0034-beginner-notebook-prose.md): two or three plain sentences per step, one link per step to the docs page that explains the method, a caption cell under every figure, the report link as a heading, and a timing line per step. Nothing about the Codespace, the scripts, the helpers or the flags; the collapsed code cells and the docs carry those. `devcontainer.json` sets `notebook.markup.fontSize` 17 and `notebook.output.fontSize` 15 so the text is readable in a Codespace.

### COP30 reference DEM: AWS Open Data + local EGM2008 → ellipsoid shift

See [ADR-0007](architecture/0007-cop30-egm2008-shift.md). Each tutorial's clip was made with `scripts/fetch_cop_dem.py` once and ships on its release. It fetches Copernicus GLO-30 tiles from the public AWS bucket `copernicus-dem-30m` (no API key) and shifts them from EGM2008 geoid to WGS84 ellipsoid heights locally via `gdalwarp` with a compound CRS pair (mirrors `uw-cryo/fetch_dem`):

- Source: `EPSG:4326+EPSG:3855` (WGS84 lon/lat + EGM2008 geoid).
- Target: `<t_srs>+EPSG:4979` (requested horizontal + WGS84 ellipsoid).

`gdalwarp` applies the per-pixel shift via PROJ's bundled EGM2008 grid; `gdal_edit.py -a_srs <t_srs>` then tags the output with the 2D horizontal SRS, and any `.aux.xml` is removed. Until 2026-10-27 it re-asserted the compound CRS instead, which a GeoTIFF can't store: GDAL kept it in an `.aux.xml` sidecar, and a copy of the `.tif` alone had no CRS (`mapproject` wrote all-nodata images, then stereo failed with "ERROR: Could not find interest points."). The heights are ellipsoidal either way, which ASP assumes. ASP represents DEM heights above the datum ellipsoid (per its `dem_geoid` / `mapproject` docs), so skipping this shift feeds geoid heights into `mapproject` and injects a vertical datum-mismatch bias (tens of meters; ~−35 m at UCSD). If a Codespace can't find the EGM2008 grid, `gdalwarp` errors ("Cannot find proj.db" / "egm08_25.gtx"); pre-caching the grid in the Dockerfile is a fallback.

### WV3 window, crops and resolution

See [ADR-0029](architecture/0029-ucsd-soledad-tutorials.md). Both WorldView tutorials work on a 3 × 3 km window around the summit of Mount Soledad, `T_PROJWIN = "476000 3632000 479000 3635000"` in UTM 11N (the cropped benchmark's crop A). `cam2rpc -t dg --dem-file <COP30 over the window + 250 m> --save-tif-image` cuts each NTF to the window and fits an RPC camera to the crop; `average_crop()` in `notebooks/utils.py` averages 4 × 4 blocks (native ~0.31 m → ~1.2 m) and rescales the RPC line/sample offsets and scales to match. Everything after runs on the crops with `-t rpc`: `bundle_adjust` in seconds instead of ~16 minutes on the full scenes (with `--heights-from-dem <COP30> --heights-from-dem-uncertainty 10`, which removes the vendor cameras' ~8 m vertical offset here), `mapproject --tr 1.2`, stereo, `point2dem --tr 2.4`.

### WV3 thread budget tuned for the 4-core floor

Config detail behind [ADR-0029](architecture/0029-ucsd-soledad-tutorials.md). `asp_mgm` stereo runs `--processes 1 --threads-multiprocess 4 --threads-singleprocess 4` (MGM is memory-heavy and multithreads within a process, so few-processes-many-threads is right on a 16 GB box; `--processes 4` risks OOM). On a bigger machine, raise `--processes` (cores ÷ threads). `bundle_adjust` and `mapproject` use `--threads 4`. The WorldView stereo also passes `--job-size-w 4096 --job-size-h 4096`, so each stage runs once over the whole ~2,700-pixel crop instead of in 2048-pixel tiles with 256-pixel collars: about 30% faster, same DEM. (`--parallel-tile-size` is `parallel_stereo`'s internal option and fails when passed by hand: "Cannot produce tiles without a valid L.tif".) Don't raise the job size for larger crops without checking memory: one 6000-pixel MGM job warned "Unable to compute valid search ranges for SGM input. Increase --corr-memory-mb" and left most of the DEM empty.

### Notebook path and helper conventions

The no-chdir `DATA` pattern itself is an editing rule in `AGENTS.md`. Earlier iterations chdir'd into the data dir; dropped because:

- Re-running the chdir cell after later cells produce subdirs compounds the chdir and breaks subsequent paths.
- It hides what's actually happening. With explicit paths in every cell, the reader sees the layout.

`notebooks/utils.py` holds `average_crop()` (see § WV3 window, crops and resolution) and the plotting helpers the notebooks call (`show_image_pair`, `show_dem_hillshade`, `show_hillshades`, `show_report_figures`), so cells show `asp-plot` calls without matplotlib boilerplate.

It also holds the run helpers, which keep ASP's verbose output out of the notebook (all three tutorials; [ADR-0031](architecture/0031-status-lines-and-logs.md)):

- `run(cmd, log, label)` prints the command, sends all output to `log` (under `data/<tutorial>/logs/`), and shows the last 5 lines of the log (small grey text, lines starting with "Warning:" left out) and a status line with the time so far, both updated every second. When the command ends, the tail is cleared and the status line says ✅ with the time, or ❌ with the last 30 log lines, and the cell stops. Commands run with `PYTHONUNBUFFERED=1`, or ASP's Python wrappers hold their output back while it goes to a file. `parallel_stereo` and `mapproject` still collect each tile's output and print it when the tile ends, so within a tile the tail doesn't move.
- `run_stereo(cmd, prefix, log)` does the same for `parallel_stereo`, with the stage and tile from `<prefix>-stereo-status.txt` and a time-left estimate. The estimate starts after the first stage: it scales the later stages' laptop times (`STEREO_STAGES`) by how much slower the finished stages ran, and within a stage uses the time per tile so far. The status file says `stereo_pprc` while the low-resolution matching runs, and goes through `stereo_corr`, `stereo_blend` and `stereo_tri` again with 0 tiles done while the tiles are joined at the end; the status line says "Writing the full-size outputs" then. Once `<prefix>-L__R.match` exists, it shows `asp-plot`'s match-point figure (`StereoPlotter` won't start without a DEM in the stereo directory, though the match plot doesn't read it, so the left image is passed as `dem_fn`). Then a two-panel map fills in as tiles finish: each tile's `-D.tif` shift (its collar cut off) and `-PC.tif` heights (ECEF to ellipsoid height with pyproj), drawn every 4 pixels and placed by pixel position in the orthorectified left image. Tile folders are deleted when `parallel_stereo` ends, so the map is drawn while it runs. Tutorial 1 uses `--job-size-w 1280 --job-size-h 1202`: four equal tiles at the same run time as the default 2048 px tiles, which split the 2560 × 2404 window unevenly.
- `timer(label)` shows the same status line for a slow Python step, from a background thread (the stereo geometry plot).
- `zip_results(zip_path, files, eight_bit)` ends each tutorial (section 8, "Download the results"): it puts the report, the DEM, the intersection-error map and the orthoimages (Tutorial 3: the report and the blended DEM) in `<tutorial>_results.zip` in the top folder, next to `notebooks/` and `data/` (gitignored), with paths relative to the files' common folder, and lists any missing file. It writes `<name>.part` and renames it when complete. The orthoimages (`eight_bit`) go in as 8-bit copies, scaled from their min–max to 1–255 with 0 for no data, which keeps every zip under 32 MB (about 23, 22 and 14 MB). VS Code for the web downloads a file over 32 MB by asking for write access to a local folder (`showDirectoryPicker`, in `fileImportExport.ts`), and Chrome refuses ~/Downloads for that; at 32 MB or less it is an ordinary browser download. The 32-bit float orthos were 24–27 MB each, and Tutorial 3's pair DEMs and error maps would have taken its zip to 37 MB.

The close-panel extension collapses each tutorial's code cells when it opens (`notebook.cell.collapseCellInput`; VS Code ignores the notebooks' `jupyter.source_hidden` metadata), and the first time Tutorial 1 opens it runs all cells, after the Python extension has found the environments and 5 s more, so the `asp` kernel is attached and no kernel picker opens. Scrolling to each cell as it starts was tried and dropped ([ADR-0030](architecture/0030-no-scroll-to-running-cell.md)); the notebook tells the user to scroll.

The extension also lists the top folder every 3 s and, when a `*_results.zip` is new or rewritten, shows a notification with a "Show in Explorer" button; right-click → Download saves it. It polls because, when the zips were first written in `data/`, no file watcher saw them: `files.watcherExclude` has `**/data/**` (ASP writes thousands of files there). The button refreshes the explorer before revealing the zip.

### Sentinel files per step

Each long-running notebook cell is wrapped in the idempotent skip pattern (see `AGENTS.md`). The sentinels:

ASTER — 01_aster_rainier.ipynb (see [ADR-0027](architecture/0027-single-aster-tutorial.md)):
- `out-Band3N.tif` (aster2asp)
- `out-Band3{N,B}_ortho.tif` (mapproject, one check per view)
- `stereo/run-DEM.tif` (stereo + point2dem)
- `stereo/rainier_aster_report.pdf` (report)
- `ref/cop30_rainier.tif` is fetched by `download_aster.sh`, which handles its own idempotency

WV3 — 02_worldview_ucsd.ipynb and 03_worldview_ucsd_blend.ipynb share `data/ucsd_soledad/` (see [ADR-0029](architecture/0029-ucsd-soledad-tutorials.md)); 03 reuses 02's downloads and crops:
- `crops/<catid>_P001.tif` (cam2rpc + average_crop, one check per scene; shared). The crops keep the vendor files' `<catid>_P001` stem so `asp_report` resolves the stereo log's camera paths to the vendor XMLs in `data/ucsd_soledad/`, which carry the geometry metadata the crops' RPC XMLs lack
- 02: `ba/run-final_residuals_pointmap.csv`, `ortho/<catid>.tif`, `stereo/run-DEM.tif`, `stereo/soledad_wv3_report.pdf`
- 03: `ba3/run-final_residuals_pointmap.csv`, `pairs/<left>_<right>/run-DEM.tif` (one check per pair), `pairs/<first pair>/run-blend-DEM.tif`, `pairs/<first pair>/soledad_wv3_blend_report.pdf`

The download `*.sh` scripts handle their own idempotency, so those cells are not wrapped.
