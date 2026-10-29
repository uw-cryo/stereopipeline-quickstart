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
    "sphinx_tippy",
    "sphinx.ext.intersphinx",
]

# Hover previews for {term} glossary references (sphinx-tippy). Tip content is
# generated statically at build time. The skip regex limits tips to glossary
# term links, so other internal links stay plain. tippy.js and popper are
# vendored in _static/js (tippy 6.3.7, popper 2.11.8) instead of the
# extension's unpkg CDN default, so tooltips work offline and behind blockers.
tippy_js = ("js/popper.min.js", "js/tippy-bundle.umd.min.js")
tippy_skip_urls = [r"^(?!.*glossary\.html#term-).*"]
tippy_enable_wikitips = False
tippy_enable_doitips = False
tippy_anchor_parent_selector = "article.bd-article"

source_suffix = {
    ".md": "myst-nb",
    ".ipynb": "myst-nb",
}

# Don't execute notebooks at doc build time. Tutorials are heavy
# (parallel_stereo runs) and rendering must work on RTD which has no ASP
# installed. docs/tutorials/*.ipynb are executed copies of notebooks/*.ipynb,
# made by scripts/execute_tutorials.py and committed (ADR-0035).
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
        "In development, but ready for usage. Please report issues "
        '<a href="https://github.com/uw-cryo/stereopipeline-quickstart/issues/new?template=problem-report.yml" '
        'target="_blank" rel="noopener noreferrer">here</a>.'
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
html_js_files = ["js/external-links.js"]

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
