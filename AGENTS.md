# AGENTS.md

This file provides guidance to AI coding agents (Claude Code and others) and to human contributors when working in this repository. It is the git-tracked onboarding reference for the repo's current-state architecture and conventions; keep it in sync with the code. The durable why behind consequential decisions lives in the architecture decision records under [`architecture/`](architecture/README.md); this file links to them rather than restating rationale.

## Goal

A separate, beginner-friendly home for the NASA Ames Stereo Pipeline (ASP) itself, distinct from `asp_plot`'s notebooks (which double as both visualization examples and implicit ASP tutorials). The repo:

1. Teaches ASP from scratch using openly available data (ASTER, WorldView).
2. Runs end-to-end in a pre-configured GitHub Codespace with no setup beyond clicking the badge.
3. Has clean static documentation alongside the runnable notebooks.
4. Uses `asp_plot` as the visualization layer at every diagnostic step.

## Repo layout

```
stereopipeline-quickstart/
├── README.md                          # Codespace badge + landing
├── LICENSE                            # BSD-3 (matches asp_plot)
├── AGENTS.md                          # this file
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
│   ├── index.md
│   ├── start/
│   │   ├── what-is-asp.md
│   │   └── codespaces.md
│   ├── concepts/
│   │   ├── pipeline-overview.md
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

`docs/reference/parameter-cheatsheet.md` was deleted in the "Cleanup prose" commit as redundant with upstream ASP docs. Don't re-author it.

## Major decisions

Consequential decisions have a full record under [`architecture/`](architecture/README.md); the entries below are current-state summaries that link to the ADR holding the why. Sections without an ADR link are conventions and implementation notes that live here in full.

### Separate repo (not folded into `asp_plot`)

A standalone repo teaching ASP itself, with `asp_plot` as the visualization layer at every step (not the subject). See [ADR-0001](architecture/0001-separate-repo.md).

### Sphinx + myst-nb docs

Same stack as `asp_plot`; see [ADR-0003](architecture/0003-sphinx-myst-nb-docs.md). Notebooks live in `notebooks/` and are mirrored into `docs/tutorials/` at build time:

- On RTD: `.readthedocs.yaml` `pre_build` runs `cp notebooks/*.ipynb docs/tutorials/`.
- Locally: a `builder-inited` hook in `docs/conf.py` does the same, so `sphinx-build docs docs/_build/html` works with no preamble.

`docs/tutorials/*.ipynb` is gitignored — the copies are build artifacts, not source.

Site is live at https://stereopipeline-quickstart.readthedocs.io/. RTD installs a GitHub webhook on import; pushes to `main` auto-rebuild.

Import gotcha: RTD's auto-detect can flag a public repo as "private" when its cached view of the GitHub OAuth grant is stale. Fix is to **Sync** the GitHub connection under RTD account settings, or use **Import Manually** (paste URL) which skips the API visibility check.

### Docs prose is a placeholder skeleton; figures and content land via PRs

See [ADR-0004](architecture/0004-docs-wip-skeleton.md). The concept/intro pages ship as a WIP skeleton: a site-wide "Work in progress" banner (`sphinx-book-theme` `announcement`), per-page WIP admonitions, one-sentence section stubs, and an HTML comment `<!-- FIGURE IDEA: ... -->` per section. Content is fleshed out iteratively in follow-up PRs. When editing concept pages: add prose, swap in real figures, but don't delete a FIGURE IDEA comment unless you're replacing it with the actual figure.

### `docs/comparisons/` section

See [ADR-0009](architecture/0009-qualitative-tool-comparisons.md). A top-level section running the same WorldView-3 UCSD pair (`21deg_12d`, 21.2° convergence) through ASP, CARS (CNES), and SETSM (OSU/PGC), side by side and qualitative (no quantitative ranking). Unlike the concept pages these ship fully-fleshed, not WIP: `index.md` carries an overview, a scope-disclaimer note, a "Key Differences" table, and a hidden toctree over `setsm`, `cars`; `cars.md` / `setsm.md` carry full Docker recipes, config, run-metrics tables, and 3-up hillshade grids (`figures/ucsd-*-hillshade.png`, committed). `docs/index.md` adds a landing card and a "Comparisons" toctree section; `docs/conf.py` needs no change (`nb_execution_mode = "off"` is global).

### "Orthorectification" (our concept) vs "mapproject" (ASP tool)

See [ADR-0005](architecture/0005-orthorectification-vs-mapproject.md). Prose (docs + notebook markdown) uses "orthorectification"; ASP's own names (`mapproject`, "mapprojection", `--mapproj-dem`, paths like `out_stereo_proj`) are kept verbatim in code, filenames, and CLI references. Each affected page carries a callout note surfacing the naming gap. Don't rename `mapproject`, `--mapproj-dem`, or `*_proj`-style paths in code cells.

### `:click-parent:` only inside grid-item-card

sphinx-design's stretched-link option needs a positioned ancestor; a `grid-item-card` provides one. On a standalone `button-link` there isn't one, so the link covers the whole page and every click navigates. Easy to re-introduce by copy-pasting button snippets from sphinx-design docs — strip `:click-parent:` unless the button is inside a card.

### Pre-built container image hosted on GHCR (not built per-Codespace)

See [ADR-0006](architecture/0006-ghcr-bpurinton-namespace.md). CI builds and pushes `ghcr.io/bpurinton/stereopipeline-quickstart:latest` on every `Dockerfile` / `environment.yml` change plus a monthly cron; Codespaces pulls it. The from-source `build:` block stays commented out in `devcontainer.json` as a fallback. Hosted under the `bpurinton` namespace (not `uw-cryo`) because making a `uw-cryo` GHCR package public needs org admin. The cross-namespace push uses a classic PAT with `write:packages`, stored as the `GHCR_PAT` Actions secret; the workflow's GHCR login step uses `username: bpurinton` + that secret. To revert to `GITHUB_TOKEN` auth under the repo owner's namespace, swap those two lines and update `IMAGE_NAME`.

### ASP-version-check workflow

See [ADR-0014](architecture/0014-asp-version-tracking.md). Runs monthly (plus manual trigger), polls StereoPipeline releases, and opens a PR (never auto-merge) that sed-bumps the pinned version consistently across four files:

- `.devcontainer/Dockerfile` (the `ARG ASP_VERSION` / `ARG ASP_BUILD_DATE`)
- `.devcontainer/devcontainer.json` (the commented-out fallback args)
- `.github/workflows/build-image.yml` (workflow_dispatch defaults + inline default expressions)
- `docs/reference/installation.md` (local-install snippet + verify line)

One-time setup: repo Settings → Actions → General → Workflow permissions, enable "Allow GitHub Actions to create and approve pull requests". Without it, `create-pull-request` fails.

### Codespace machine size: 4-core floor

See [ADR-0010](architecture/0010-4-core-codespace-floor.md). `hostRequirements`: 4-core / 16 GB / 32 GB. The 16 GB / 32 GB values match GitHub's 4-core tier; raising them forces the machine back to 8 cores. The tutorials are tuned to run at this floor; larger machines work by bumping the thread/process counts and `TR`.

### Python 3.12 (not 3.11)

See [ADR-0013](architecture/0013-python-312-floor.md). The conda env is pinned to 3.12 in `environment.yml` (documented in `installation.md`) because `sliderule >= 5.3` (transitive via `asp_plot` 1.14) uses PEP 701 f-strings that only parse on 3.12+; on 3.11 `import asp_plot.altimetry` fails with a `SyntaxError`.

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

### No chdir in notebooks; full relative paths from `notebooks/`

Cell 1 of each notebook defines a single literal:

```python
DATA = "../data/aster_rainier"        # or "../data/ucsd_stereo_21deg_12d"
!mkdir -p {DATA}
```

Then every subsequent path is interpolated:
- Shell magics: `!cmd {DATA}/foo` (IPython `{var}` expansion).
- Python f-strings: `Path(f"{DATA}/foo").exists()`.
- Bare variable when a string would equal `{DATA}`: `directory=DATA`.

Earlier iterations chdir'd into the data dir. Dropped because:

- Re-running the chdir cell after later cells produce subdirs compounds the chdir and breaks subsequent paths.
- It hides what's actually happening. With explicit paths in every cell, the reader sees the layout.

`notebooks/utils.py` holds two helpers used by the COP30 cells: `scene_bbox(*image_camera_pairs, session=None, pad=0.05)` runs ASP's `camera_footprint` on each view and unions the results into a `"minlon minlat maxlon maxlat"` string; `utm_epsg(bbox)` returns the UTM EPSG at the bbox center. Both notebooks use these so neither hardcodes a bbox or `T_SRS`. `camera_footprint` needs no DEM — `--datum WGS84` intersects the camera rays with the ellipsoid — and works for both the raw ASTER images (no georeferencing) and the WV NTFs (RPC metadata GDAL won't intersect on its own).

### Idempotent step-skipping in notebook cells

Each long-running cell is wrapped:

```python
if Path(f"{DATA}/<sentinel>").exists():
    print("...exists; skipping <step>. Delete <thing> to reprocess.")
else:
    !<long command>
```

Output naming uses `_ortho` for the orthorectified products (renamed from the older `_proj`/`_map`/`_mp`), since "orthorectification" is the concept term used throughout (ASP's tool is still `mapproject`).

Sentinel files per step:

ASTER — 01_aster_rainier.ipynb runs raw-imagery stereo first, then an orthorectified pass against a fetched COP30 DEM, each with its own report:
- `out-Band3N.tif` (aster2asp)
- `stereo/run-DEM.tif` + `stereo/rainier_aster_report.pdf` (raw pass)
- `ref/cop30_rainier.tif` (COP30 fetch)
- `out-Band3{N,B}_ortho.tif` (mapproject)
- `stereo_ortho/run-DEM.tif` + `stereo_ortho/rainier_aster_ortho_report.pdf`

WV3 — 02_worldview_ucsd.ipynb is the NO-BA canonical; the BA recipe is the variant 03_worldview_ucsd_ba.ipynb with `_ba`-suffixed outputs so both can run in one data dir:
- `ref/cop30_ucsd.tif` (COP30 fetch; shared)
- canonical: `<catid>_P001_ortho.tif`, `stereo/run-DEM.tif`, `stereo/ucsd_wv3_report.pdf`
- BA variant: `ba/run-final_residuals_pointmap.csv`, `<catid>_P001_ortho_ba.tif`, `stereo_ba/run-DEM.tif`, `stereo_ba/ucsd_wv3_ba_report.pdf`

The download `*.sh` scripts handle their own idempotency, so those cells are not wrapped.

### Notebook kernel registration

A system Jupyter kernel `asp` is registered in the Dockerfile via `python -m ipykernel install --name asp --display-name "Python (ASP)" --prefix /usr`. Both notebooks declare `kernelspec.name = "asp"` in their metadata, so VS Code resolves the kernel without prompting on first open.

### PATH plumbing for ASP in the container

Two-pronged so ASP works from any shell context:

1. Image ENV: `PATH=/opt/conda/envs/asp/bin:/opt/StereoPipeline/bin:...`. Conda env first so its `python` shadows ASP's bundled `/opt/StereoPipeline/bin/python` (which has none of the conda env's packages and would break `import asp_plot`).
2. `/etc/profile.d/99-asp.sh` written in the Dockerfile, idempotently appends `/opt/StereoPipeline/bin` to PATH if it's not already there. Catches Codespaces' `loginInteractiveShell` env probe, which sources `~/.bashrc` (running `source activate asp`) and can rearrange PATH.
3. `postCreate.sh` also explicitly exports `PATH=/opt/conda/envs/asp/bin:/opt/StereoPipeline/bin:$PATH` at the top, defensively, so it doesn't depend on shell-wrapping behavior.

### PDF viewer extension

`AdamRaichu.pdf-viewer` (web-compatible) is in `devcontainer.json`'s `customizations.vscode.extensions`. The popular `tomoki1207.pdf` does NOT declare a `browser` entrypoint in its `package.json` and refuses to load in a browser-based Codespace. `AdamRaichu.pdf-viewer` does, and renders pages as images via pdf.js (no text-selection/search but renders cleanly).

A stash exists with an alternative approach: a `.devcontainer/postStart.sh` that launches `python -m http.server 8000`, plus a `pdf_link()` helper that prints a clickable forwarded-port URL to PDFs. Not active; kept in case the extension approach ever breaks.

### Editor settings split: workspace-wide vs Codespace-only

Two places set VS Code settings, and the split is deliberate:

- `.vscode/settings.json` (workspace scope) applies everywhere the folder is opened, local *and* Codespace. It holds only editor behavior that should always apply: `chat.disableAIFeatures`, `workbench.secondarySideBar.defaultVisibility: "hidden"`, `files.autoSaveDelay`.
- `.devcontainer/devcontainer.json` → `customizations.vscode.settings` (Remote [Codespaces] scope) applies only inside the container. Open the folder locally without "Reopen in Container" and these never apply.

The file-explorer hiding lives in the devcontainer block, not workspace settings, so it is Codespace-only. Its `files.exclude` hides infrastructure a first-time learner doesn't need — `.github`, `.devcontainer`, `.vscode`, `docs`, `architecture`, `.readthedocs.yaml`, `requirements.txt`, `.gitignore`, `AGENTS.md`, `LICENSE` — to focus the explorer on `notebooks/` + `data/`. Local development shows the full tree. `files.exclude` merges across scopes, so the empty workspace block is intentionally absent (nothing is hidden locally).

### Vantor (not Maxar) branding

Use "Vantor" (not "Maxar") across docs and notebook prose. This is the project's preferred spelling for the WorldView imagery rights-holder going forward.

## Markdown style conventions

- Drop `**bold**` and `*italic*` in flowing prose. Keep them in tables / definition lists when structurally meaningful.
- Reduce em dashes in prose. Replace with periods, semicolons, or restructured sentences. Keep them in `item — description` list bullets.
- No equations or math notation in the docs.
- Drop editorial framing. No "Sweet spot:", "That's it.", "Running ASP is half the job;", "intimidating for newcomers", etc.
- Don't pre-empt the reader's interpretation of plotted results in the notebooks. Describe what each step *does* (action), not what the output *looks like* (interpretation). Users add their own observations between cells after running.
- No specific wall-time claims, core-hour estimates, or speedup ratios in user-facing docs.
- No unverified hard numbers. Performance/quality claims with magnitudes ("DEM bias drops to ~1 m", "residual reprojection error <1 px") don't belong in user-facing prose. Configuration facts (machine specs, output resolutions set by `--tr`, file sizes of demo data) are fine.
- Don't author from-scratch parameter or API references that duplicate upstream docs. Link out to the ASP CLI's own `--help` and the upstream ASP docs instead.
- Default to concise. Technical-docs prose tends to over-explain and editorialize; trim aggressively.
