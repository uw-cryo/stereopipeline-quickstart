"""Sphinx config for stereopipeline-quickstart docs.

Stack mirrors asp_plot (Sphinx + myst-nb + sphinx-book-theme + sphinx-design)
so a contributor familiar with one repo can navigate the other.
"""

from __future__ import annotations

import shutil
from pathlib import Path

# -- Project information -----------------------------------------------------
project = "stereopipeline-quickstart"
author = "UW Terrain Analysis and Cryosphere Observation Lab"
copyright = "2026, UW TACO Lab"

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_nb",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx.ext.intersphinx",
]

source_suffix = {
    ".md": "myst-nb",
    ".ipynb": "myst-nb",
}

# Don't actually execute notebooks at doc build time. Tutorials are heavy
# (parallel_stereo runs) and rendering must work on RTD which has no ASP
# installed. Notebooks are executed locally / in Codespaces and committed
# with their outputs.
nb_execution_mode = "off"

# Allow MyST extensions used in the prose pages.
myst_enable_extensions = [
    "colon_fence",     # ::: instead of ``` for admonitions
    "deflist",
    "tasklist",
    "substitution",
    "linkify",
]
myst_heading_anchors = 3

# -- HTML output -------------------------------------------------------------
html_theme = "sphinx_book_theme"
html_title = "stereopipeline-quickstart"
html_theme_options = {
    "announcement": (
        "Work in progress — content is being rewritten. "
        "Notebooks in <code>notebooks/</code> are functional; prose pages are placeholders."
    ),
    "repository_url": "https://github.com/uw-cryo/stereopipeline-quickstart",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "path_to_docs": "docs",
    "launch_buttons": {
        "binderhub_url": "",            # Codespaces is our launch target, not Binder
        "colab_url": "",
        "notebook_interface": "jupyterlab",
    },
    "show_navbar_depth": 2,
}

html_static_path = ["_static"]
html_css_files = ["css/custom.css"]

# -- Cross-references --------------------------------------------------------
intersphinx_mapping = {
    "asp_plot": ("https://asp-plot.readthedocs.io/en/latest/", None),
    "rasterio": ("https://rasterio.readthedocs.io/en/stable/", None),
    "geopandas": ("https://geopandas.org/en/stable/", None),
}

# -- Excluded files ----------------------------------------------------------
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/.ipynb_checkpoints",
]


# Mirror notebooks/*.ipynb into docs/tutorials/ at the start of every build.
# RTD does this via .readthedocs.yaml pre_build; this hook makes local
# `sphinx-build` behave the same so edits to notebooks/ flow through.
def _copy_notebooks(app):
    src = Path(app.srcdir).parent / "notebooks"
    dst = Path(app.srcdir) / "tutorials"
    dst.mkdir(exist_ok=True)
    for nb in src.glob("*.ipynb"):
        shutil.copy2(nb, dst / nb.name)


def setup(app):
    app.connect("builder-inited", _copy_notebooks)
