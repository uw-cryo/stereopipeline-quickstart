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
│   ├── onCreate.sh                    # ASP/asp_plot health check + download_aster.sh pre-fetch (runs in prebuilds)
│   ├── postStart.sh                   # starts JupyterLab on port 8890 at every Codespace start
│   ├── postAttach.sh                  # writes + opens START_HERE.md (link to Tutorial 1 in that JupyterLab) after the trust prompt, installs close-panel/
│   └── close-panel/                   # tiny VS Code extension: closes the terminal panel once on first launch
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
│   ├── index.md
│   ├── start/
│   │   ├── what-is-asp.md             # fully authored; history/toolchain/CLI-vs-GUI framing
│   │   ├── codespaces.md
│   │   └── figures/                   # authored SVG diagrams (asp-timeline, asp-toolchain, parallax)
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
│   │   └── figures/                   # ucsd-{asp,cars,cop30,setsm}-hillshade.png
│   ├── tutorials/
│   │   └── index.md                   # tutorial gallery; notebooks copied here at build
│   └── reference/
│       ├── glossary.md
│       ├── output-files.md
│       ├── installation.md            # local-install guide; demoted from start/
│       └── further-reading.md
├── notebooks/
│   ├── 01_aster_rainier.ipynb         # ASTER quick look: L1A → raw 30 m DEM (asp_bm) + report
│   ├── 02_aster_rainier_ortho.ipynb   # ASTER: COP30 fetch + mapproject + asp_mgm 30 m DEM + report reusing 01's selections
│   ├── 03_worldview_ucsd.ipynb        # WV3 → 4 m DEM, no-BA canonical (mapproj + stereo + pc_align report)
│   ├── 04_worldview_ucsd_ba.ipynb     # WV3 BA variant (adds bundle_adjust; _ba-suffixed outputs)
│   └── utils.py                       # scene_bbox/utm_epsg via camera_footprint
├── scripts/
│   ├── download_aster.sh              # Zenodo fetch + shipped ICESat-2 (release) + unzip
│   ├── download_worldview_ucsd.sh     # SpaceNet S3 fetch + shipped ICESat-2 (release) + tar extract + rename
│   └── fetch_cop_dem.py               # COP30 from AWS, local geoid→ellipsoid shift
└── CLAUDE/                            # gitignored; local session/design scratch notes
```

## Docs site

### Sphinx + myst-nb

Same stack as `asp_plot`; see [ADR-0003](architecture/0003-sphinx-myst-nb-docs.md). Notebooks live in `notebooks/` and are mirrored into `docs/tutorials/` at build time:

- On RTD: `.readthedocs.yaml` `pre_build` runs `cp notebooks/*.ipynb docs/tutorials/`.
- Locally: a `builder-inited` hook in `docs/conf.py` does the same, so `sphinx-build docs docs/_build/html` works with no preamble.

`docs/tutorials/*.ipynb` is gitignored — the copies are build artifacts, not source.

Site is live at https://stereopipeline-quickstart.readthedocs.io/. RTD installs a GitHub webhook on import; pushes to `main` auto-rebuild.

Two RTD build constraints:

- `docs/requirements.txt` pins exact versions. An unpinned build resolved sphinx-book-theme 1.4 / pydata-sphinx-theme 0.20, which renders a header navbar whose search button duplicates the sidebar search field.
- `.readthedocs.yaml` overrides `build.jobs.build.html` to run sphinx **without `-j auto`** (RTD's default adds it). sphinx-tippy is not parallel-safe: pages rendered in worker processes embed references to per-page tip files that the main process never writes, so every hover preview 404s on the deployed site while working fine in a serial local build.

Import gotcha: RTD's auto-detect can flag a public repo as "private" when its cached view of the GitHub OAuth grant is stale. Fix is to **Sync** the GitHub connection under RTD account settings, or use **Import Manually** (paste URL) which skips the API visibility check.

### Docs content state

See [ADR-0004](architecture/0004-docs-wip-skeleton.md) (skeleton phase), [ADR-0017](architecture/0017-retire-per-page-wip-admonitions.md) (admonitions retired), and [ADR-0020](architecture/0020-soften-banner-issue-form.md) (banner softened). The concept/intro pages shipped as a WIP skeleton and have since been fleshed out with prose and figures (issue #6); the site-wide banner (`announcement` in `docs/conf.py`) now reads "In development, but ready for usage" rather than flagging a WIP. Reader contact is the GitHub issue form (`.github/ISSUE_TEMPLATE/problem-report.yml`), linked from the banner, the landing page's "Reporting problems" section, the Codespace page, and the tutorials index. Figures that still need full processing runs are marked by the remaining HTML comments `<!-- FIGURE IDEA: ... -->`.

Figure conventions are in [ADR-0018](architecture/0018-docs-figure-conventions.md): conceptual diagrams are hand-written SVGs in a `figures/` dir next to the page, drawn on an opaque light surface so one file reads on both themes; data-backed figures are matplotlib/asp_plot PNGs from real runs, with provenance stated in the page prose. The BA residual figures come from a `bundle_adjust` run matching the tutorial-4 config (`--ip-per-tile 10`); the remaining `concepts/figures/*.png` come from full local runs of the tutorial-1 and tutorial-2 (ASTER raw and orthorectified passes) and tutorial-3 (WV3) configurations, plus two extras kept under `data/ucsd_stereo_21deg_12d/`: `stereo_knobs/` (an 800 m crop run with `asp_bm`/`asp_mgm` × subpixel 1/2/9 for the knobs figure) and `align_demo/` (a DEM-vs-COP30 `pc_align` run quoted on the alignment page).

Glossary linking is in [ADR-0019](architecture/0019-glossary-term-hover-previews.md): jargon links to `docs/reference/glossary.md` with the MyST `{term}` role at its first occurrence on a page, prose only. `sphinx-tippy` (in `docs/requirements.txt`) turns those links into hover previews, scoped to glossary anchors by `tippy_skip_urls` in `docs/conf.py`; term links get a dotted underline and the tooltip box follows the theme via `--pst-*` variables in `custom.css`. tippy.js and popper are vendored as pinned copies in `docs/_static/js/` (`tippy_js` in `conf.py`), so no CDN is involved.

### `docs/comparisons/` section

See [ADR-0009](architecture/0009-qualitative-tool-comparisons.md). A top-level section running the same WorldView-3 UCSD pair (`21deg_12d`, 21.2° convergence) through ASP, CARS (CNES), and SETSM (OSU/PGC), side by side and qualitative (no quantitative ranking). Unlike the concept pages these ship fully-fleshed, not WIP: `index.md` carries an overview, a scope-disclaimer note, a "Key Differences" table, and a hidden toctree over `setsm`, `cars`; `cars.md` / `setsm.md` carry full Docker recipes, config, run-metrics tables, and 3-up hillshade grids (`figures/ucsd-*-hillshade.png`, committed). `docs/index.md` adds a landing card and a "Comparisons" toctree section; `docs/conf.py` needs no change (`nb_execution_mode = "off"` is global).

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

A new Codespace starts in Restricted Mode and asks "Do you trust the authors of the files in this folder?"; the lifecycle commands wait for that answer. `.devcontainer/postAttach.sh` (`postAttachCommand`) then opens the start page (§ Opening the tutorials) with the remote `code` CLI, once per Codespace, or `notebooks/01_aster_rainier.ipynb` when there is no Codespace name. It replaced `customizations.codespaces.openFiles`, which opened the notebook before the trust prompt, in Restricted Mode, as raw JSON. Lifecycle commands may not inherit `VSCODE_IPC_HOOK_CLI`, so the script falls back to the newest `/tmp/vscode-ipc-*.sock` and `/vscode/bin/*/*/bin/remote-cli/code`. `workbench.editorAssociations` maps `*.ipynb` to the notebook editor and `START_HERE.md` to the Markdown preview. The same settings block turns off the YAML extension's telemetry prompt and extension recommendations; the `git fetch` prompt and the PDF viewer's donation notice still appear in VS Code.

Codespaces runs the lifecycle commands in a terminal and opens the panel to show it. `terminal.integrated.hideOnStartup` doesn't stop that, and `devcontainer.json` can't run VS Code commands (GitHub staff, community discussion 43125), so `postAttach.sh` zips `.devcontainer/close-panel/` into a `.vsix` with Python's `zipfile` and installs it with `code --install-extension`. On activation the extension runs `workbench.action.closePanel` at 0.5, 2 and 5 s, then sets a `globalState` flag so it never closes the panel again. `sirmspencer.vscode-autohide` was considered: it only hides the panel when the user clicks into an editor, and its hide-on-open also hides the file explorer.

### Opening the tutorials

The tutorials run in JupyterLab, not VS Code's notebook editor ([ADR-0024](architecture/0024-jupyterlab-start-page.md)). `.devcontainer/postStart.sh` (`postStartCommand`, every start) starts `/opt/conda/envs/asp/bin/jupyter lab` on port 8890, rooted at the repo, with no token, and logs to `/tmp/stereopipeline-quickstart-jupyterlab.log`. A lifecycle command's background jobs are killed when it ends (a `setsid nohup ... &` left no server and no log), so the script uses `setsid -f` and waits until the port listens. It also writes JupyterLab user settings, each only if the user has none for that plugin: `apputils-extension/notification` turns off the news pop-up and the update check, and `apputils-extension/sessionDialogs` sets `skipKernelRestartDialog`, so the toolbar's ⏩ (restart the kernel and run all cells) runs a notebook without the "Restart Kernel?" dialog. `devcontainer.json` forwards 8890 with `onAutoForward: silent`. The port is private, which is what stands in for the token: made public, it would expose a JupyterLab that runs code for anyone with the URL.

After the trust prompt, `postAttach.sh` writes the gitignored `START_HERE.md`, one heading link, "Click Here to Begin", to `https://${CODESPACE_NAME}-8890.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}/lab/tree/notebooks/01_aster_rainier.ipynb`. A private forwarded port signs the user in through a redirect when opened as a page; Codespaces' own `?editor=jupyter` page embeds it in a frame instead, and that fails on a first visit. JupyterLab's only kernel is the `asp` environment's `python3`, since the server runs from that environment. The `postAttach.sh` marker keeps the start page from reopening on later attaches; `START_HERE.md` stays in the file explorer.

JupyterLab shows a cell's whole output. The `parallel_stereo`, `mapproject` and `bundle_adjust` cells carry `"scrolled": true` in their cell metadata, which JupyterLab renders as a fixed-height scroll box; VS Code ignores the key and keeps truncating long output itself.

### PDFs

In JupyterLab, a report link in a notebook opens the PDF in a JupyterLab tab, rendered by the browser's own PDF viewer.

For VS Code, `mathematic.vscode-pdf` (web-compatible) is in `devcontainer.json`'s `customizations.vscode.extensions`. The popular `tomoki1207.pdf` does NOT declare a `browser` entrypoint in its `package.json` and refuses to load in a browser-based Codespace.

### Editor settings split: workspace-wide vs Codespace-only

Two places set VS Code settings, and the split is deliberate:

- `.vscode/settings.json` (workspace scope) applies everywhere the folder is opened, local *and* Codespace. It holds only editor behavior that should always apply: `chat.disableAIFeatures`, `workbench.secondarySideBar.defaultVisibility: "hidden"`, `files.autoSaveDelay`.
- `.devcontainer/devcontainer.json` → `customizations.vscode.settings` (Remote [Codespaces] scope) applies only inside the container. Open the folder locally without "Reopen in Container" and these never apply.

The file-explorer hiding lives in the devcontainer block, not workspace settings, so it is Codespace-only. Its `files.exclude` hides infrastructure a first-time learner doesn't need — `.github`, `.devcontainer`, `.vscode`, `docs`, `architecture`, `.readthedocs.yaml`, `requirements.txt`, `.gitignore`, `AGENTS.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `LICENSE` — to focus the explorer on `notebooks/` + `data/`. Local development shows the full tree. `files.exclude` merges across scopes, so the empty workspace block is intentionally absent (nothing is hidden locally).

## CI workflows

### ASP-version-check workflow

See [ADR-0014](architecture/0014-asp-version-tracking.md). Runs monthly (plus manual trigger), polls StereoPipeline releases, and opens a PR (never auto-merge) that sed-bumps the pinned version consistently across four files:

- `.devcontainer/Dockerfile` (the `ARG ASP_VERSION` / `ARG ASP_BUILD_DATE`)
- `.devcontainer/devcontainer.json` (the commented-out fallback args)
- `.github/workflows/build-image.yml` (workflow_dispatch defaults + inline default expressions)
- `docs/reference/installation.md` (local-install snippet + verify line)

One-time setup: repo Settings → Actions → General → Workflow permissions, enable "Allow GitHub Actions to create and approve pull requests". Without it, `create-pull-request` fails.

## Tutorial pipeline design

### ASTER two-report workflow

See [ADR-0008](architecture/0008-aster-cop30-two-reports.md), amended by [ADR-0023](architecture/0023-split-aster-tutorial.md). The two ASTER notebooks mirror the WV flow, producing two DEMs + two reports:

1. Raw pass (`01_aster_rainier.ipynb`, the quick look): `parallel_stereo` on the raw imagery (no BA, no ortho) → `stereo/run-DEM.tif` at 30 m → `stereo/rainier_aster_report.pdf`. Uses `--stereo-algorithm asp_bm` + `--subpixel-mode 1`; mode 9 is unsupported on block matching ("Use mode <= 6").
2. Ortho pass (`02_aster_rainier_ortho.ipynb`): fetch a COP30 DEM, `mapproject` both views onto it at 15 m, re-run stereo with `asp_mgm` + `--subpixel-mode 9` → `stereo_ortho/run-DEM.tif` → `stereo_ortho/rainier_aster_ortho_report.pdf` (COP30 reference).

`asp_mgm` stereo runs `--processes 1 --threads-multiprocess 4` for the 4-core floor.

### `--reuse-selections` for comparable reports

Both two-report comparisons replay the first run's figure selections so the PDFs line up panel-for-panel (same ICESat-2 points, profile track, hillshade crops) and only the processing change shows:

- By default every report, the first of each pair included, replays the sidecar shipped with the tutorial: `data/<tutorial>/icesat2_shipped/figure_selections.yml`, whose `parquet_cache` points at the shipped `atl06sr_all.parquet` beside it, so no SlideRule request is made. The download scripts fetch both from the `icesat2-2026-10-23` release with `curl -f`. See [ADR-0022](architecture/0022-ship-icesat2-data.md).
- With `FRESH_ICESAT2 = True` (first code cell of each notebook), the first report requests fresh data from SlideRule, and the second reuses the first's own sidecar: the 02 ortho report reuses 01's `stereo/rainier_aster_report_figure_selections.yml` (run 01 first), and the 04 BA report reuses 03's `stereo/ucsd_wv3_report_figure_selections.yml` (run 03 first).

asp_plot writes the sidecar next to each report PDF (`<report_stem>_figure_selections.yml`) and reads it back via `asp_report --reuse-selections <path>`. The cells pass the flag only when the file exists (`reuse = ... if Path(prior).exists() else ""`), so each stays runnable standalone. The sidecar's `parquet_cache` path is resolved from the working directory, so shipped sidecars are written relative to `notebooks/`.

As of asp_plot ≥ 1.18.0 the report's Processing Parameters page also renders the reconstructed `mapproject` command(s), rebuilt from the mapprojected output GeoTIFF metadata (ASP's `mapproject` writes no log to parse). No notebook change is needed to get this; `asp_plot` produces it. This surfaces the tool name `mapproject` in the reports, consistent with [ADR-0005](architecture/0005-orthorectification-vs-mapproject.md).

### Report figures inline

PDFs open poorly in the browser-based editor, so each report cell also shows three of the report's figures below it. `asp_report --figures-directory` (asp_plot ≥ 3.5.0) keeps a copy of each figure as `NN_<title>.png` in `<stereo dir>/report_figures/`, which asp_report otherwise deletes with its `tmp_asp_report_plots/` directory. `show_report_figures()` in `notebooks/utils.py` displays the ones named in `REPORT_FIGURES` (DEM results, detailed hillshade, ICESat-2 profile), picked by title because the number shifts when a section is skipped. They are scaled to 1400 px wide, about 2.6 MB of notebook output per report; the PDF keeps them at full resolution. Both reports of a pair show the same three figures, which line up because of `--reuse-selections`.

### COP30 reference DEM: AWS Open Data + local EGM2008 → ellipsoid shift

See [ADR-0007](architecture/0007-cop30-egm2008-shift.md). `scripts/fetch_cop_dem.py` fetches Copernicus GLO-30 tiles from the public AWS bucket `copernicus-dem-30m` (no API key) and shifts them from EGM2008 geoid to WGS84 ellipsoid heights locally via `gdalwarp` with a compound CRS pair (mirrors `uw-cryo/fetch_dem`):

- Source: `EPSG:4326+EPSG:3855` (WGS84 lon/lat + EGM2008 geoid).
- Target: `<t_srs>+EPSG:4979` (requested horizontal + WGS84 ellipsoid).

`gdalwarp` applies the per-pixel shift via PROJ's bundled EGM2008 grid; `gdal_edit.py -a_srs` then re-asserts the compound CRS. ASP represents DEM heights above the datum ellipsoid (per its `dem_geoid` / `mapproject` docs), so skipping this shift feeds geoid heights into `mapproject` and injects a vertical datum-mismatch bias (tens of meters; ~−35 m at UCSD). If a Codespace can't find the EGM2008 grid, `gdalwarp` errors ("Cannot find proj.db" / "egm08_25.gtx"); pre-caching the grid in the Dockerfile is a fallback.

### WV3 ROI and resolution

See [ADR-0011](architecture/0011-wv3-roi-and-resolution.md). `T_PROJWIN = "476000 3637000 478000 3639000"` in UTM 11N (coastal 2 × 2 km, sea cliffs → UCSD campus). Processing GSD `TR = 1.0` (`mapproject`), output `point2dem --tr 4.0` → a 4 m DEM. 4 m is coarse for WV3, a deliberate teaching-artifact tradeoff; bump `TR` down on a bigger machine. A denser-ICESat-2 crossover ROI east of UCSD (`477750 3634800 480750 3637800`) exists but the coastal clip is kept for the landscape.

### WV3 thread budget tuned for the 4-core floor

Config detail behind [ADR-0011](architecture/0011-wv3-roi-and-resolution.md). `asp_mgm` stereo runs `--processes 1 --threads-multiprocess 4 --threads-singleprocess 4` (MGM is memory-heavy and multithreads within a process, so few-processes-many-threads is right on a 16 GB box; `--processes 4` risks OOM). On a bigger machine, raise `--processes` (cores ÷ threads). `bundle_adjust` and `mapproject` use `--threads 4`.

### Notebook path and helper conventions

The no-chdir `DATA` pattern itself is an editing rule in `AGENTS.md`. Earlier iterations chdir'd into the data dir; dropped because:

- Re-running the chdir cell after later cells produce subdirs compounds the chdir and breaks subsequent paths.
- It hides what's actually happening. With explicit paths in every cell, the reader sees the layout.

`notebooks/utils.py` holds two helpers used by the COP30 cells: `scene_bbox(*image_camera_pairs, session=None, pad=0.05)` runs ASP's `camera_footprint` on each view and unions the results into a `"minlon minlat maxlon maxlat"` string; `utm_epsg(bbox)` returns the UTM EPSG at the bbox center. Both notebooks use these so neither hardcodes a bbox or `T_SRS`. `camera_footprint` needs no DEM — `--datum WGS84` intersects the camera rays with the ellipsoid — and works for both the raw ASTER images (no georeferencing) and the WV NTFs (RPC metadata GDAL won't intersect on its own).

### Sentinel files per step

Each long-running notebook cell is wrapped in the idempotent skip pattern (see `AGENTS.md`). The sentinels:

ASTER — 01_aster_rainier.ipynb runs raw-imagery stereo with its report; 02_aster_rainier_ortho.ipynb repeats the download and aster2asp steps (skipped if 01 ran) and adds an orthorectified pass against a fetched COP30 DEM, with its own report (see [ADR-0023](architecture/0023-split-aster-tutorial.md)):
- `out-Band3N.tif` (aster2asp)
- `stereo/run-DEM.tif` + `stereo/rainier_aster_report.pdf` (raw pass)
- `ref/cop30_rainier.tif` (COP30 fetch)
- `out-Band3{N,B}_ortho.tif` (mapproject)
- `stereo_ortho/run-DEM.tif` + `stereo_ortho/rainier_aster_ortho_report.pdf`

WV3 — 03_worldview_ucsd.ipynb is the NO-BA canonical; the BA recipe is the variant 04_worldview_ucsd_ba.ipynb with `_ba`-suffixed outputs so both can run in one data dir (see [ADR-0012](architecture/0012-no-ba-canonical-wv.md)):
- `ref/cop30_ucsd.tif` (COP30 fetch; shared)
- canonical: `<catid>_P001_ortho.tif`, `stereo/run-DEM.tif`, `stereo/ucsd_wv3_report.pdf`
- BA variant: `ba/run-final_residuals_pointmap.csv`, `<catid>_P001_ortho_ba.tif`, `stereo_ba/run-DEM.tif`, `stereo_ba/ucsd_wv3_ba_report.pdf`

The download `*.sh` scripts handle their own idempotency, so those cells are not wrapped.
