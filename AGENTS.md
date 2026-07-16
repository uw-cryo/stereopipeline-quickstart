# AGENTS.md

Guidance for AI coding agents (Claude Code and others) and human contributors working in this repository. Lean by design: only what an agent can't infer from the code. The current-state codemap (what lives where, container/CI/pipeline design) is [`ARCHITECTURE.md`](ARCHITECTURE.md); the durable why behind consequential decisions lives in the architecture decision records under [`architecture/`](architecture/README.md). Keep all three in sync with the code.

## Goal

A separate, beginner-friendly home for the NASA Ames Stereo Pipeline (ASP) itself, distinct from `asp_plot`'s notebooks. The repo:

1. Teaches ASP from scratch using openly available data (ASTER, WorldView).
2. Runs end-to-end in a pre-configured GitHub Codespace with no setup beyond clicking the badge.
3. Has clean static documentation alongside the runnable notebooks.
4. Uses `asp_plot` as the visualization layer at every diagnostic step.

## Dev commands

- Docs build: `sphinx-build docs docs/_build/html` (deps in `docs/requirements.txt`). A `builder-inited` hook copies `notebooks/*.ipynb` into `docs/tutorials/` first, so no preamble is needed; RTD does the same via `pre_build`.
- No test suite, linter, or release process; the site rebuilds automatically on push to `main`.

## Editing rules and gotchas

- `docs/tutorials/*.ipynb` are gitignored build artifacts — edit `notebooks/` only.
- Prose (docs + notebook markdown) says "orthorectification"; ASP's own names (`mapproject`, "mapprojection", `--mapproj-dem`, paths like `out_stereo_proj`) stay verbatim in code, filenames, and CLI references. Don't rename them. See [ADR-0005](architecture/0005-orthorectification-vs-mapproject.md).
- Concept pages are a WIP skeleton ([ADR-0004](architecture/0004-docs-wip-skeleton.md)): add prose, swap in real figures, but don't delete a `<!-- FIGURE IDEA: ... -->` comment unless you're replacing it with the actual figure.
- sphinx-design's `:click-parent:` only works inside a `grid-item-card` (it needs a positioned ancestor). On a standalone `button-link` the link covers the whole page and every click navigates. Strip it when copy-pasting button snippets unless the button is inside a card.
- `docs/reference/parameter-cheatsheet.md` was deleted as redundant with upstream ASP docs. Don't re-author it.
- Tutorials are tuned to the 4-core / 16 GB Codespace floor ([ADR-0010](architecture/0010-4-core-codespace-floor.md)). Don't raise thread/process counts or lower `--tr` in the committed notebooks; `ARCHITECTURE.md` documents the per-tool budgets.
- Use "Vantor" (not "Maxar") across docs and notebook prose for the WorldView imagery rights-holder.

## Notebook conventions

No chdir; full relative paths from `notebooks/`. Cell 1 of each notebook defines a single literal:

```python
DATA = "../data/aster_rainier"        # or "../data/ucsd_stereo_21deg_12d"
!mkdir -p {DATA}
```

Then every subsequent path is interpolated:
- Shell magics: `!cmd {DATA}/foo` (IPython `{var}` expansion).
- Python f-strings: `Path(f"{DATA}/foo").exists()`.
- Bare variable when a string would equal `{DATA}`: `directory=DATA`.

Each long-running cell is wrapped so re-runs skip completed steps:

```python
if Path(f"{DATA}/<sentinel>").exists():
    print("...exists; skipping <step>. Delete <thing> to reprocess.")
else:
    !<long command>
```

The per-step sentinel files are listed in `ARCHITECTURE.md`. The download `*.sh` scripts handle their own idempotency, so those cells are not wrapped.

Output naming uses `_ortho` for the orthorectified products (not `_proj`/`_map`/`_mp`), since "orthorectification" is the concept term used throughout (ASP's tool is still `mapproject`).

Both notebooks declare `kernelspec.name = "asp"` in their metadata; keep it when editing notebook metadata.

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
