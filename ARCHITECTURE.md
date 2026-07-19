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
│   ├── postCreate.sh                  # ASP/asp_plot health check + ASTER pre-fetch
│   └── postStart.sh                   # (stashed; not active)
├── .github/
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
│   ├── 01_aster_rainier.ipynb         # ASTER L1A → raw 30 m DEM + report, then COP30-ortho pass + report
│   ├── 02_worldview_ucsd.ipynb        # WV3 → 4 m DEM, no-BA canonical (mapproj + stereo + pc_align report)
│   ├── 03_worldview_ucsd_ba.ipynb     # WV3 BA variant (adds bundle_adjust; _ba-suffixed outputs)
│   └── utils.py                       # scene_bbox/utm_epsg via camera_footprint
├── scripts/
│   ├── download_aster.sh              # Zenodo fetch + unzip
│   ├── download_worldview_ucsd.sh     # SpaceNet S3 fetch + tar extract + rename
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

Import gotcha: RTD's auto-detect can flag a public repo as "private" when its cached view of the GitHub OAuth grant is stale. Fix is to **Sync** the GitHub connection under RTD account settings, or use **Import Manually** (paste URL) which skips the API visibility check.

### Docs content state

See [ADR-0004](architecture/0004-docs-wip-skeleton.md) (skeleton phase) and [ADR-0017](architecture/0017-retire-per-page-wip-admonitions.md) (admonitions retired). The concept/intro pages shipped as a WIP skeleton and have since been fleshed out with prose and figures (issue #6). The only reader-facing WIP signal is the site-wide banner (`sphinx-book-theme` `announcement` in `docs/conf.py`, with a link to the issue tracker). Figures that still need full processing runs are marked by the remaining HTML comments `<!-- FIGURE IDEA: ... -->`.

Figure conventions are in [ADR-0018](architecture/0018-docs-figure-conventions.md): conceptual diagrams are hand-written SVGs in a `figures/` dir next to the page, drawn on an opaque light surface so one file reads on both themes; data-backed figures are matplotlib/asp_plot PNGs from real runs, with provenance stated in the page prose. The BA residual figures come from a `bundle_adjust` run matching the tutorial-3 config (`--ip-per-tile 10`); the remaining `concepts/figures/*.png` come from full local runs of the tutorial-1 (ASTER two-pass) and tutorial-2 (WV3) configurations, plus two extras kept under `data/ucsd_stereo_21deg_12d/`: `stereo_knobs/` (an 800 m crop run with `asp_bm`/`asp_mgm` × subpixel 1/2/9 for the knobs figure) and `align_demo/` (a DEM-vs-COP30 `pc_align` run quoted on the alignment page).

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

### PATH plumbing for ASP in the container

Two-pronged so ASP works from any shell context:

1. Image ENV: `PATH=/opt/conda/envs/asp/bin:/opt/StereoPipeline/bin:...`. Conda env first so its `python` shadows ASP's bundled `/opt/StereoPipeline/bin/python` (which has none of the conda env's packages and would break `import asp_plot`).
2. `/etc/profile.d/99-asp.sh` written in the Dockerfile, idempotently appends `/opt/StereoPipeline/bin` to PATH if it's not already there. Catches Codespaces' `loginInteractiveShell` env probe, which sources `~/.bashrc` (running `source activate asp`) and can rearrange PATH.
3. `postCreate.sh` also explicitly exports `PATH=/opt/conda/envs/asp/bin:/opt/StereoPipeline/bin:$PATH` at the top, defensively, so it doesn't depend on shell-wrapping behavior.

### Notebook kernel registration

A system Jupyter kernel `asp` is registered in the Dockerfile via `python -m ipykernel install --name asp --display-name "Python (ASP)" --prefix /usr`. Both notebooks declare `kernelspec.name = "asp"` in their metadata, so VS Code resolves the kernel without prompting on first open.

### PDF viewer extension

`AdamRaichu.pdf-viewer` (web-compatible) is in `devcontainer.json`'s `customizations.vscode.extensions`. The popular `tomoki1207.pdf` does NOT declare a `browser` entrypoint in its `package.json` and refuses to load in a browser-based Codespace. `AdamRaichu.pdf-viewer` does, and renders pages as images via pdf.js (no text-selection/search but renders cleanly).

A stash exists with an alternative approach: a `.devcontainer/postStart.sh` that launches `python -m http.server 8000`, plus a `pdf_link()` helper that prints a clickable forwarded-port URL to PDFs. Not active; kept in case the extension approach ever breaks.

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

See [ADR-0008](architecture/0008-aster-cop30-two-reports.md). The ASTER notebook mirrors the WV flow, producing two DEMs + two reports:

1. Raw pass: `parallel_stereo` on the raw imagery (no BA, no ortho) → `stereo/run-DEM.tif` at 30 m → `stereo/rainier_aster_report.pdf`. Uses `--stereo-algorithm asp_bm` + `--subpixel-mode 1`; mode 9 is unsupported on block matching ("Use mode <= 6").
2. Ortho pass: fetch a COP30 DEM, `mapproject` both views onto it at 15 m, re-run stereo with `asp_mgm` + `--subpixel-mode 9` → `stereo_ortho/run-DEM.tif` → `stereo_ortho/rainier_aster_ortho_report.pdf` (COP30 reference).

`asp_mgm` stereo runs `--processes 1 --threads-multiprocess 4` for the 4-core floor.

### `--reuse_selections` for comparable reports

Both two-report comparisons replay the first run's figure selections so the PDFs line up panel-for-panel (same ICESat-2 points, profile track, hillshade crops) and only the processing change shows:

- 01 ortho report reuses `stereo/rainier_aster_report_figure_selections.yml`.
- 03 BA report reuses `stereo/ucsd_wv3_report_figure_selections.yml` (run 02 first).

asp_plot ≥ 1.16.0 writes the sidecar next to each report PDF (`<report_stem>_figure_selections.yml`) and reads it back via `asp_plot --reuse_selections <path>`. The cells pass the flag only when the file exists (`reuse = ... if Path(prior).exists() else ""`), so each stays runnable standalone. Pinned at `>=1.19.0` in both requirements.txt and environment.yml.

As of asp_plot ≥ 1.18.0 the report's Processing Parameters page also renders the reconstructed `mapproject` command(s), rebuilt from the mapprojected output GeoTIFF metadata (ASP's `mapproject` writes no log to parse). No notebook change is needed to get this; `asp_plot` produces it. This surfaces the tool name `mapproject` in the reports, consistent with [ADR-0005](architecture/0005-orthorectification-vs-mapproject.md).

### COP30 reference DEM: AWS Open Data + local EGM2008 → ellipsoid shift

See [ADR-0007](architecture/0007-cop30-egm2008-shift.md). `scripts/fetch_cop_dem.py` fetches Copernicus GLO-30 tiles from the public AWS bucket `copernicus-dem-30m` (no API key) and shifts them from EGM2008 geoid to WGS84 ellipsoid heights locally via `gdalwarp` with a compound CRS pair (mirrors `uw-cryo/fetch_dem`):

- Source: `EPSG:4326+EPSG:3855` (WGS84 lon/lat + EGM2008 geoid).
- Target: `<t_srs>+EPSG:4979` (requested horizontal + WGS84 ellipsoid).

`gdalwarp` applies the per-pixel shift via PROJ's bundled EGM2008 grid; `gdal_edit.py -a_srs` then re-asserts the compound CRS. ASP represents DEM heights above the datum ellipsoid (per its `dem_geoid` / `mapproject` docs), so skipping this shift feeds geoid heights into `mapproject` and injects a vertical datum-mismatch bias (tens of meters; ~−35 m at UCSD). If a Codespace can't find the EGM2008 grid, `gdalwarp` errors loudly ("Cannot find proj.db" / "egm08_25.gtx"); pre-caching the grid in the Dockerfile is a fallback.

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

ASTER — 01_aster_rainier.ipynb runs raw-imagery stereo first, then an orthorectified pass against a fetched COP30 DEM, each with its own report:
- `out-Band3N.tif` (aster2asp)
- `stereo/run-DEM.tif` + `stereo/rainier_aster_report.pdf` (raw pass)
- `ref/cop30_rainier.tif` (COP30 fetch)
- `out-Band3{N,B}_ortho.tif` (mapproject)
- `stereo_ortho/run-DEM.tif` + `stereo_ortho/rainier_aster_ortho_report.pdf`

WV3 — 02_worldview_ucsd.ipynb is the NO-BA canonical; the BA recipe is the variant 03_worldview_ucsd_ba.ipynb with `_ba`-suffixed outputs so both can run in one data dir (see [ADR-0012](architecture/0012-no-ba-canonical-wv.md)):
- `ref/cop30_ucsd.tif` (COP30 fetch; shared)
- canonical: `<catid>_P001_ortho.tif`, `stereo/run-DEM.tif`, `stereo/ucsd_wv3_report.pdf`
- BA variant: `ba/run-final_residuals_pointmap.csv`, `<catid>_P001_ortho_ba.tif`, `stereo_ba/run-DEM.tif`, `stereo_ba/ucsd_wv3_ba_report.pdf`

The download `*.sh` scripts handle their own idempotency, so those cells are not wrapped.
