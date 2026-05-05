"""Sphinx config for stereopipeline-quickstart docs.

Stack mirrors asp_plot (Sphinx + myst-nb + sphinx-book-theme + sphinx-design)
so a contributor familiar with one repo can navigate the other.
"""

from __future__ import annotations

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
    # Notebooks are copied into docs/tutorials/ at build time by .readthedocs.yaml
    # pre_build. Don't leave the ones present in the source tree dangling.
    "**/.ipynb_checkpoints",
]
