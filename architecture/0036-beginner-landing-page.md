# 36. The docs home page is the beginner path, with screenshots of the launch

- **Date:** 2026-10-29
- **Status:** Accepted
- **Context doc:** `ARCHITECTURE.md` § Docs site

## Context
The home page was a gallery: six cards (run Tutorial 1, what ASP is, launch the Codespace, concepts, reference, comparisons), a "what this is not" section and the full table of contents. A first-time user, who the tutorials are for, had to pick a card before learning the one thing they need: click the button, click Trust, watch Tutorial 1 run. The Codespaces page had the launch steps, below a paragraph about container images. Group feedback (2026-10-27) asked for a very simple landing page in large type, with screenshots of the clicks a user can't avoid, the startup time, and a note that the "High codespace CPU" pop-up is normal.

## Decision
- **`docs/index.md` is the beginner path only:** five numbered steps (sign in to GitHub, click the button, click Trust, watch Tutorial 1 run, then), with screenshots of the launch: the building screen, the trust dialog, Tutorial 1 just opened with its parts labeled, and the end of the run. Everything else is a short "More" list at the bottom, and the tables of contents are hidden in the page (they stay in the sidebar).
- **Large type on that page only,** through a `{raw} html` style block at the top of the page, scoped to `article.bd-article`. A `{div}` with a class was tried first: headings inside a directive aren't sections, so they rendered small and left the page's contents list.
- **The screenshots** are taken in a new Codespace on `main` at the browser test tool's window size (1512 × 802) and live in `docs/start/figures/launch-*.png`. `scripts/docs_figures/annotate_screenshots.py` draws the numbered labels on the Tutorial 1 screenshot, with the boxes' pixel coordinates in the script.
- **`docs/start/codespaces.md` keeps the details** (machine size, costs, storage, the CPU pop-up, what the notebooks make), and points at the home page for the launch itself.

## Consequences
- **+** A first-time user reads one page, top to bottom, and knows what to click and what to expect.
- **+** The README and the home page say the same three things in the same order.
- **−** Screenshots go stale when VS Code, Codespaces or the notebooks change their look; retaking them is a Codespace launch and the annotation script.
- **−** The gallery cards are gone; the concept pages are one link each in "More" and in the sidebar.

## Alternatives considered
- **Keep the gallery and add a "Start here" card:** rejected; the card is one more choice before the first click.
- **Put the launch steps only on the Codespaces page:** rejected; the home page is where the docs link and the README send people.
- **A walkthrough video:** on hold (Ben, 2026-10-28); clear screenshots should be enough.
