# 16. Per-page WIP admonitions retired; FIGURE IDEA comments are the per-page WIP marker

- **Date:** 2026-07-07
- **Status:** Accepted; amends [ADR-0004](0004-docs-wip-skeleton.md)
- **Context doc:** `AGENTS.md` § Docs prose is a placeholder skeleton; PR #16

## Context
ADR-0004 shipped the concept/intro pages as a WIP skeleton with three signals: a site-wide banner, a per-page "Placeholder content. Being rewritten with figures." admonition, and `<!-- FIGURE IDEA: ... -->` comments. PR #16 (issue #6) fleshed out every skeleton page with full prose and figures, leaving only a handful of figures that need complete processing runs to produce. The per-page admonitions were now inaccurate: the pages are no longer placeholders, and a banner-plus-admonition on every page overstated how unfinished the site is.

## Decision
Remove all per-page WIP admonitions. The site-wide `sphinx-book-theme` announcement banner ("⚠️ Work in progress. Codespace notebooks are functional. Please report issues!", linking to the issue tracker) is the only reader-facing WIP signal. Pending figures are tracked solely by the remaining FIGURE IDEA comments, which are invisible to readers; the ADR-0004 rule stands that a comment is deleted only when replaced by the actual figure.

## Consequences
- **+** Pages read as what they now are: authored documentation with a few figures pending, not placeholders.
- **+** One WIP signal to maintain and eventually remove (the banner), instead of one per page.
- **−** Readers get no per-page hint that a specific figure is coming; the gap is visible only to contributors reading the source.
- When the last FIGURE IDEA comments are resolved and the site is considered stable, the banner itself can be dropped or reworded.

## Alternatives considered
- **Keep softened per-page admonitions ("Some figures still to come")** — rejected: repeats the banner's message on every page and ages poorly as figures land one by one.
- **Drop the banner too** — rejected: the site is young and the maintainers want an explicit report-issues invitation while early readers exercise it.
