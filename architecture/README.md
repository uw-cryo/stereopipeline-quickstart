# Architecture Decision Records — stereopipeline-quickstart

Why-decisions for this repo, in [Nygard](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) format (Context · Decision · Consequences · Alternatives). Each record is immutable once Accepted; a later record may supersede or amend an earlier one (noted in its status).

These records were backfilled on 2026-07-02 from the repo's git history and issue tracker, then maintained going forward. Numbers are assigned once and never reused. The Date field records when each decision was effectively made, so dates are not strictly monotonic with record numbers.

`AGENTS.md` holds the lean always-loaded onboarding (commands, editing rules, conventions); `ARCHITECTURE.md` holds the current-state codemap (repo layout, how the pieces fit); these ADRs hold the durable why behind the choices both describe. Where they overlap, the other two link here rather than restating the rationale.

- [0001 — Separate repo, not folded into asp_plot](0001-separate-repo.md)
- [0002 — Scope: a CLI quickstart, not a GUI or cloud-processing venue](0002-cli-quickstart-scope.md)
- [0003 — Sphinx + myst-nb docs (not Jupyter Book, Quarto, or MkDocs)](0003-sphinx-myst-nb-docs.md)
- [0004 — Docs prose ships as a WIP skeleton; content lands via per-concept PRs](0004-docs-wip-skeleton.md)
- [0005 — "Orthorectification" (concept) vs mapproject (ASP tool) naming](0005-orthorectification-vs-mapproject.md)
- [0006 — Pre-built image on GHCR under the bpurinton namespace](0006-ghcr-bpurinton-namespace.md)
- [0007 — COP30 reference DEM: AWS Open Data + local EGM2008 to ellipsoid shift](0007-cop30-egm2008-shift.md)
- [0008 — ASTER tutorial restructured around a COP30 reference + two reports](0008-aster-cop30-two-reports.md) — *supersedes the downsample-reference workflow; two-report design superseded by 0027*
- [0009 — Tool comparisons stay qualitative, not journal-grade quantitative](0009-qualitative-tool-comparisons.md)
- [0010 — 4-core Codespace floor](0010-4-core-codespace-floor.md) — *supersedes the 8-core floor*
- [0011 — WV3 ROI + resolution: coastal 2x2 km, TR 1.0 / 4 m DEM](0011-wv3-roi-and-resolution.md) — *superseded by 0029*
- [0012 — No-BA WV tutorial is canonical; BA is the _ba variant](0012-no-ba-canonical-wv.md) — *supersedes the BA-first tutorial; superseded by 0029*
- [0013 — Python 3.12 floor (sliderule PEP 701 f-strings)](0013-python-312-floor.md)
- [0014 — Automated ASP-version tracking via PR-based bumps, not auto-merge](0014-asp-version-tracking.md)
- [0015 — Contributor docs as AGENTS.md + ADRs; retire CLAUDE.md and the CHANGELOG](0015-agents-md-and-adrs.md)
- [0016 — Move the codemap to ARCHITECTURE.md; slim AGENTS.md](0016-architecture-md-codemap.md) — *amends 0015*
- [0017 — Per-page WIP admonitions retired; FIGURE IDEA comments are the per-page WIP marker](0017-retire-per-page-wip-admonitions.md) — *amends 0004*
- [0018 — Docs figures: hand-authored SVGs on an opaque light surface; data figures from real runs](0018-docs-figure-conventions.md)
- [0019 — Glossary term links with hover previews via sphinx-tippy](0019-glossary-term-hover-previews.md)
- [0020 — Soften the site-wide banner; reader reports via a GitHub issue form](0020-soften-banner-issue-form.md) — *amends 0017*
- [0021 — Bound asp-plot to one major version](0021-asp-plot-major-version-bound.md)
- [0022 — Ship the tutorials' ICESat-2 data as release assets](0022-ship-icesat2-data.md)
- [0023 — Split the ASTER tutorial: quick look first, orthorectified pass second](0023-split-aster-tutorial.md) — *amends 0008; superseded by 0027*
- [0024 — Tutorials open in JupyterLab on a forwarded port, from a start page](0024-jupyterlab-start-page.md) — *superseded by 0025*
- [0025 — Back to VS Code: the JupyterLab start page is reverted](0025-back-to-vs-code.md) — *supersedes 0024*
- [0026 — A simplified VS Code window for the tutorials](0026-simplified-vs-code.md)
- [0027 — One ASTER tutorial: orthorectify, then `asp_mgm`, on a window around the summit](0027-single-aster-tutorial.md) — *supersedes 0023 and 0008's two reports*
- [0028 — Tutorial data on this repo's releases, fetched by the notebooks](0028-tutorial-data-on-releases.md) — *extends 0022*
- [0029 — WorldView tutorials on Mount Soledad crops: one pair, then three pairs blended](0029-ucsd-soledad-tutorials.md) — *supersedes 0011 and 0012*
