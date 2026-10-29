# 35. The site renders executed copies of the notebooks, committed in docs/tutorials/

- **Date:** 2026-10-29
- **Status:** Accepted; amends [0003](0003-sphinx-myst-nb-docs.md), which copied `notebooks/*.ipynb` into `docs/tutorials/` at build time
- **Context doc:** `ARCHITECTURE.md` § Docs site

## Context
The docs site rendered the notebooks as they are in `notebooks/`, which have no outputs since the WorldView rework ([0029](0029-ucsd-soledad-tutorials.md)): a new Codespace should open a clean notebook, and output-free notebooks give readable diffs. So the site showed the tutorials' code and prose with no figures, status lines or report pages, and a reader couldn't see what a tutorial produces without running it. `docs/requirements.txt` had assumed committed outputs all along; Read the Docs has no ASP and can't execute them.

## Decision
- **Executed copies** of the three notebooks live in `docs/tutorials/`, committed, and the site renders those. The build no longer copies `notebooks/*.ipynb` over them (the `pre_build` step in `.readthedocs.yaml` and the `builder-inited` hook in `docs/conf.py` are gone).
- **`scripts/execute_tutorials.py`** makes them: it runs each notebook with nbclient in a fresh run folder (a copy of `notebooks/` and `scripts/` with an empty `data/`), so every step runs and shows its output, as in a new Codespace, and writes the executed notebook to `docs/tutorials/`.
- **They are remade when a tutorial changes,** on a laptop (about 25 minutes for all three); the status lines then show laptop times, shorter than the Codespace timing lines in the prose.
- **`notebooks/` stays output-free.**

## Consequences
- **+** The site shows each tutorial as a reader would see it after a run: figures, captions, status lines and the report figures.
- **+** No change to Read the Docs; it renders committed files as before.
- **−** About 8 MB per notebook (the report figures are 3.8 MB of it), so each refresh adds about 25 MB to the repository's history. A refresh happens only when a tutorial changes.
- **−** Two copies of each notebook: an edit to `notebooks/` shows on the site only after the script runs again.

## Alternatives considered
- **Attach the executed notebooks to a GitHub release and download them in the RTD build:** no history growth, but another release to keep current and a build that depends on it.
- **Smaller report figures in the executed copies only:** about 5 MB instead of 8; not worth a second rendering path for the figures.
- **Commit outputs in `notebooks/` itself:** rejected in 0029; the Codespace would open notebooks full of old outputs, and every run would change them.
