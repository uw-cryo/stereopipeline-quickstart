# 2. Scope: a CLI quickstart, not a GUI or cloud-processing venue

- **Date:** 2026-06-05
- **Status:** Accepted (tracked in [#9](https://github.com/uw-cryo/stereopipeline-quickstart/issues/9), which remains open for the broader audience discussion)
- **Context doc:** issue #9; closed PR #2

## Context
An SNWG-adjacent goal is a browser GUI where non-technical users select options and never touch the CLI. A GUI prototype inside the Codespace was explored in PR #2 (closed) and left much to be desired: it still requires a GitHub account, opening a Codespace, and launching a GUI from within it, and a GUI user who then needs to process larger scenes is immediately forced back to the CLI with no cloud path.

## Decision
Keep this repo focused on a beginner-friendly CLI quickstart. Do not shoehorn a GUI ASP experience into the Codespace. Non-technical cloud processing is a separate concern for a dedicated cloud-backed website, out of scope here.

## Consequences
- **+** One coherent audience: users who want to on-ramp to ASP quickly, then install it locally and process larger scenes than a Codespace allows.
- **+** Effort concentrates on making the CLI path clear and runnable rather than maintaining a fragile in-Codespace GUI.
- **−** The "never touch the CLI" audience is not served here; that need is deferred to a future cloud resource.
- Related: the 4-core optimization work (ADR-0010, ADR-0011, ADR-0012) is what makes the CLI path viable for newcomers on free-tier machines.

## Alternatives considered
- **Embed a browser GUI in the Codespace** (PR #2) — rejected: high friction, poor experience, and a dead end the moment the user outgrows Codespace-sized scenes.
- **Target both CLI and GUI audiences in one repo** — rejected: the audiences and delivery venues (Codespace vs dedicated cloud site) differ enough that combining them dilutes both.
