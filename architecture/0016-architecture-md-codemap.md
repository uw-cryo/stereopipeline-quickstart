# 16. Move the codemap to ARCHITECTURE.md; slim AGENTS.md to lean always-loaded onboarding

- **Date:** 2026-07-16
- **Status:** Accepted (amends [ADR-0015](0015-agents-md-and-adrs.md))
- **Context doc:** [uw-cryo/agents#1](https://github.com/uw-cryo/agents/issues/1), [uw-cryo/asp_plot#157](https://github.com/uw-cryo/asp_plot/pull/157)

## Context

ADR-0015 split contributor docs into `AGENTS.md` (mutable current-state reference) and ADRs (immutable why), but left everything current-state in `AGENTS.md`: the repo-layout tree, container/CI wiring, and tutorial-pipeline narratives alongside the editing rules. At 266 lines, most of the file loaded into every agent session was descriptive codemap rather than mistake-preventing guidance. Anthropic's best-practices guidance says always-loaded agent context should hold only what an agent can't infer from the code, and that long files bury the rules that matter. The lab discussion in uw-cryo/agents#1 converged on a three-piece convention, adopted by asp_plot in uw-cryo/asp_plot#157: a lean `AGENTS.md` linking to an on-demand `ARCHITECTURE.md` (the mutable what/where, per matklad's codemap pattern) and to ADRs (the append-only why).

## Decision

Adopt the three-piece convention:

- `AGENTS.md` — lean, always-loaded: goal, dev commands, editing rules and gotchas, notebook and markdown conventions. Links out for everything else.
- `ARCHITECTURE.md` — the current-state codemap at the repo root: repo layout, docs-site mechanics, container/Codespace plumbing, CI workflows, tutorial-pipeline design. Mutable; kept in sync with the code; read on demand.
- `architecture/` ADRs — unchanged from ADR-0015.

Content moved from `AGENTS.md` to `ARCHITECTURE.md` largely verbatim; sections that interleaved rules with narrative were split, with the rule staying in `AGENTS.md` and the narrative moving. `CLAUDE.md` remains the one-line `@AGENTS.md` shim. `ARCHITECTURE.md` joins `AGENTS.md` in the Codespace explorer's `files.exclude` (contributor infra, not learner-facing).

## Consequences

- **+** Smaller always-loaded context; the rules an agent must follow every session are no longer diluted by descriptive narrative.
- **+** Converges uw-cryo repos on one convention (asp_plot adopted the same split in uw-cryo/asp_plot#157).
- **−** One more document to keep in sync: the codemap can now drift without breaking any always-loaded context, so updating `ARCHITECTURE.md` is a deliberate maintenance expectation.
- **−** Splitting interleaved sections was editorial, not mechanical; a rule mistakenly routed to `ARCHITECTURE.md` is effectively invisible to agents until someone notices.

## Alternatives considered

- **Keep the 266-line AGENTS.md** — rejected: most of it was the category the guidance says to cut from always-loaded context, and it diverged from the emerging lab convention.
- **Move the codemap into the ADRs** — rejected: ADRs are immutable records of decisions in time; the codemap is a mutable current-state description and needs one home that tracks the code.
- **A `docs/` page instead of root ARCHITECTURE.md** — rejected: `docs/` is the learner-facing site; contributor infra lives at the root, and the root filename is the established community convention.
