# 4. Docs prose ships as a WIP skeleton; content lands via per-concept PRs

- **Date:** 2026-05-07
- **Status:** Accepted
- **Context doc:** `AGENTS.md` § Docs prose is a placeholder skeleton; commit 9cde15e

## Context
The concept and intro docs are a large writing task. Blocking the repo's release on fully-authored prose (with figures) for every page would delay everything else, and figures need real processing runs to produce.

## Decision
Ship the concept/intro pages as a placeholder skeleton and flesh them out iteratively in follow-up PRs, one concept page at a time. The site carries a site-wide "Work in progress" banner (`sphinx-book-theme` `announcement`) and a per-page WIP admonition. Each section holds a one-sentence stub plus an HTML comment `<!-- FIGURE IDEA: ... -->` describing the figure to author later.

## Consequences
- **+** The repo and its runnable notebooks ship without waiting on complete prose.
- **+** FIGURE IDEA comments record intent so a later contributor knows what each section needs.
- **+** Reviewable in small, focused per-concept PRs rather than one giant docs drop.
- **−** The published site openly shows unfinished pages (mitigated by the banner and admonitions).
- **Convention:** when fleshing out a page, add prose and swap in real figures, but do not delete a FIGURE IDEA comment unless you are replacing it with the actual figure. The `comparisons/` pages are the exception (ADR-0009): they ship fully authored, not as skeletons.

## Alternatives considered
- **Withhold the docs until fully written** — rejected: blocks release and couples every page to figure-producing runs.
- **Delete the stub sections until written** — rejected: loses the structure and the FIGURE IDEA intent that guide contributors.
