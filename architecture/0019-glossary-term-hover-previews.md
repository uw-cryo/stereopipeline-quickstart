# 19. Glossary term links with hover previews via sphinx-tippy

- **Date:** 2026-07-08
- **Status:** Accepted
- **Context doc:** `docs/reference/glossary.md`; `docs/conf.py`; PR #16

## Context
The docs carry a glossary (`{glossary}` directive), but no prose page linked into it, so a beginner hitting "parallax" or "RPC" mid-sentence had to find the glossary on their own. CARS's technical-foundations page (raised on PR #16) hyperlinks jargon to its glossary; we wanted the same, plus the definition surfaced on hover so readers don't lose their place. `sphinx-hoverxref` provides hover but depends on the Read the Docs embed API, so tooltips would not work in local builds or any non-RTD hosting.

## Decision
Jargon links to the glossary via the MyST `{term}` role at its first occurrence on a page, in prose only (not tables or code). Hover previews come from `sphinx-tippy`, which bakes tooltip HTML into per-page static JS at build time, so they work identically locally and on RTD. `tippy_skip_urls` restricts tooltips to glossary `#term-` anchors: other internal links stay plain. Term links get a dotted underline (custom.css) as the hover affordance, and the tooltip box is restyled with `--pst-*` theme variables so it follows the light/dark toggle. tippy.js and popper are vendored as pinned minified copies in `docs/_static/js/` via the `tippy_js` config (not loaded from the extension's unpkg CDN default), so tooltips work offline and are immune to content blockers.

## Consequences
- **+** Definitions appear in place on hover; the link still works as a normal glossary link (and is the fallback wherever JS is disabled).
- **+** Static generation: no runtime API, works in local builds, previews render in PR review builds.
- **+** No external requests at view time; the vendored scripts make the built site self-contained.
- **−** New docs dependency (`sphinx-tippy`) in `docs/requirements.txt`, plus two vendored minified libraries (tippy.js 6.3.7, popper 2.11.8) to bump manually if they ever need updating.
- Adding a glossary entry makes it linkable everywhere; `{term}` references to missing entries fail the build with a warning, which keeps links honest.

## Alternatives considered
- **`sphinx-hoverxref`** — rejected: tooltips only render on RTD-hosted pages, dead in local builds.
- **`{abbr}` role (native browser title tooltips)** — rejected: duplicates definition text at every use site and provides no link to the glossary.
- **Plain `{term}` links without hover** — rejected: works, but the hover preview is the main reader benefit; the plain link remains as the degraded mode anyway.
