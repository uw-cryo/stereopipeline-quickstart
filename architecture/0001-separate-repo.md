# 1. Separate repo, not folded into asp_plot

- **Date:** 2026-05-04
- **Status:** Accepted
- **Context doc:** `AGENTS.md` § Separate repo (not folded into `asp_plot`)

## Context
`asp_plot`'s example notebooks already double as both visualization demos and implicit ASP tutorials. A beginner-facing "learn ASP from scratch" resource needs a different audience, a different release cadence, and a heavyweight pre-built container, none of which fit cleanly inside the `asp_plot` python package.

## Decision
Build this as a standalone repository (`uw-cryo/stereopipeline-quickstart`) that teaches ASP itself, using `asp_plot` as the visualization layer at every diagnostic step rather than as the subject.

## Consequences
- **+** Audience separation is explicit: `asp_plot` docs target users of asp_plot; this repo targets users new to ASP entirely.
- **+** The multi-GB Codespace image lives here, so it never slows `asp_plot`'s CI or docs builds.
- **+** ASP can be pinned and released on its own cadence (every few months) independent of the more active `asp_plot`.
- **−** Two repos to keep coherent; shared conventions (docs stack, prose style) must be mirrored deliberately.

## Alternatives considered
- **A new `tutorials/` section inside `asp_plot`** — rejected: mixes audiences and drags the heavyweight image into the package repo's CI.
- **Reuse `uw-cryo/asp_tutorials`** — rejected: that repo predates the Codespace-first, `asp_plot`-driven approach; a clean start was cheaper than retrofitting it. It remains linked as the predecessor.
