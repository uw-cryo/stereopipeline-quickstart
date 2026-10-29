"""Run the tutorial notebooks and save the executed copies for the docs site.

    python scripts/execute_tutorials.py <run folder> [<output folder>]

<run folder> holds a copy of notebooks/ and scripts/ and an empty data/; the
notebooks download and process everything there, as in a new Codespace, so
their outputs show every step running rather than skipped. <output folder>
defaults to docs/tutorials/, where the site renders them from (ADR-0035).
The notebooks in notebooks/ stay as they are, without outputs.

Run it in the environment the notebooks use, with ASP on PATH. On a Mac with
a conda env, the env's bin folder goes before ASP's (both have asp_report)
and PROJ_DATA and GDAL_DATA point at the env's share/ folders. About 25
minutes on an 8-core laptop for all three.
"""
import shutil
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

NOTEBOOKS = ["01_aster_rainier", "02_worldview_ucsd", "03_worldview_ucsd_blend"]


def main():
    run = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path(__file__).resolve().parents[1] / "docs/tutorials"
    out.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).resolve().parents[1] / "notebooks"
    for name in NOTEBOOKS:
        shutil.copy(src / f"{name}.ipynb", run / "notebooks" / f"{name}.ipynb")
        nb = nbformat.read(run / "notebooks" / f"{name}.ipynb", as_version=4)
        start = time.time()
        NotebookClient(nb, timeout=None, kernel_name="python3",
                       resources={"metadata": {"path": str(run / "notebooks")}}).execute()
        nbformat.write(nb, out / f"{name}.ipynb")
        print(f"{name}: {(time.time() - start) / 60:.1f} min, {(out / f'{name}.ipynb').stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
