# 3. Sphinx + myst-nb docs (not Jupyter Book, Quarto, or MkDocs)

- **Date:** 2026-05-04
- **Status:** Accepted
- **Context doc:** `AGENTS.md` § Sphinx + myst-nb

## Context
The docs site needs to render both Markdown prose and executable-looking notebooks, and it should be maintainable by the same people who work on `asp_plot`'s documentation.

## Decision
Use the same stack as `asp_plot`: Sphinx + myst-nb, hosted on ReadTheDocs. Notebooks live in `notebooks/` and are mirrored into `docs/tutorials/` at build time (RTD `pre_build` copy; a `builder-inited` hook in `docs/conf.py` for local builds). The copied `docs/tutorials/*.ipynb` are gitignored build artifacts.

## Consequences
- **+** Docs contributors move between this repo and `asp_plot` without learning a new tool.
- **+** `sphinx-build docs docs/_build/html` works locally with no preamble because the conf.py hook mirrors the notebooks.
- **+** Notebooks have a single source of truth in `notebooks/`; the docs copies are derived, never edited directly.
- **−** Two copy mechanisms (RTD `pre_build` and the conf.py hook) must stay in sync.

## Alternatives considered
- **Jupyter Book proper** — rejected: diverges from the `asp_plot` toolchain contributors already know.
- **Quarto** — rejected: a separate ecosystem and build toolchain for no gain here.
- **MkDocs** — rejected: weaker notebook rendering story and, again, not what `asp_plot` uses.
