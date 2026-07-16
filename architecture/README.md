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
- [0008 — ASTER tutorial restructured around a COP30 reference + two reports](0008-aster-cop30-two-reports.md) — *supersedes the downsample-reference workflow*
- [0009 — Tool comparisons stay qualitative, not journal-grade quantitative](0009-qualitative-tool-comparisons.md)
- [0010 — 4-core Codespace floor](0010-4-core-codespace-floor.md) — *supersedes the 8-core floor*
- [0011 — WV3 ROI + resolution: coastal 2x2 km, TR 1.0 / 4 m DEM](0011-wv3-roi-and-resolution.md)
- [0012 — No-BA WV tutorial is canonical; BA is the _ba variant](0012-no-ba-canonical-wv.md) — *supersedes the BA-first tutorial*
- [0013 — Python 3.12 floor (sliderule PEP 701 f-strings)](0013-python-312-floor.md)
- [0014 — Automated ASP-version tracking via PR-based bumps, not auto-merge](0014-asp-version-tracking.md)
- [0015 — Contributor docs as AGENTS.md + ADRs; retire CLAUDE.md and the CHANGELOG](0015-agents-md-and-adrs.md)
- [0016 — Move the codemap to ARCHITECTURE.md; slim AGENTS.md](0016-architecture-md-codemap.md) — *amends 0015*
