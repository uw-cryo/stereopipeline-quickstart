# 20. Soften the site-wide banner; reader reports via a GitHub issue form

- **Date:** 2026-07-20
- **Status:** Accepted; amends [ADR-0017](0017-retire-per-page-wip-admonitions.md)
- **Context doc:** `ARCHITECTURE.md` § Docs content state; PR #16

## Context
ADR-0017 kept the site-wide `sphinx-book-theme` announcement banner ("⚠️ Work in progress...") as the only reader-facing WIP signal while PR #16 authored the concept and intro pages. With the rewrite complete and merging, that wording overstates how unfinished the site is, but a site-wide pointer to the issue board is still wanted — and a bare issue-board link produces blank issues with no reproduction details.

## Decision
Keep the banner, drop the WIP framing: it now reads "In development, but ready for usage. Please report issues here.", with "here" linking straight to a new-issue form. The form (`.github/ISSUE_TEMPLATE/problem-report.yml`) asks where the problem occurred, what happened, and the environment (Codespace / local / just reading). The docs also link the form directly: a "Reporting problems" section on the landing page, plus one-line pointers on the Codespace page and the tutorials index. `.github/ISSUE_TEMPLATE/config.yml` routes questions about ASP itself to the upstream ASP support forum.

## Consequences
- **+** Every page keeps a pointer to the issue board without presenting finished pages as a work in progress.
- **+** Reports arrive with location and environment details instead of as blank issues (blank issues stay enabled for everything else).
- **−** A permanent banner spends some reader attention on every page; accepted while the site is young and reports are the priority.
- FIGURE IDEA comments remain the internal per-page WIP marker per ADR-0017; the banner wording no longer tracks page completeness.

## Alternatives considered
- **Remove the banner entirely, links in-page only** — rejected: while the site is new, a site-wide report pointer is worth the attention cost; in-page links alone reach only readers who hit those pages.
- **Bare link to the issue board, no template** — rejected: first-time reporters (the audience of this repo) get no prompt for the details a report needs.
