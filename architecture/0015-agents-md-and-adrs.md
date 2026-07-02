# 15. Contributor docs as AGENTS.md + ADRs; retire CLAUDE.md and the CHANGELOG

- **Date:** 2026-07-02
- **Status:** Accepted
- **Context doc:** this repo's `AGENTS.md` and `architecture/`

## Context
Repo design context lived in a gitignored `CLAUDE/CLAUDE.md`, invisible to contributors. A `CHANGELOG.md` in Keep-a-Changelog / SemVer form also sat at the root, but this repo ships no versioned releases (no package, no tags, no `pip install`), so an `## [Unreleased]` changelog with nothing ever released was a poor fit. Meanwhile the accumulated why-decisions were being captured as informal prose, which risks drift between wherever a decision is restated.

## Decision
Adopt two git-tracked contributor documents with a clear division of labor:

- `AGENTS.md` — the current-state onboarding reference: repo layout, conventions, how to work here. Mutable; kept in sync with the code.
- `architecture/` — immutable ADRs holding the why behind each consequential decision, in Nygard format with supersession tracking. Where `AGENTS.md` describes a decision, it links to the ADR rather than restating the rationale (one source of truth per decision).

Retire the gitignored `CLAUDE/CLAUDE.md` (its durable content moved into `AGENTS.md`; workflow preferences live in agent memory) and delete `CHANGELOG.md`.

## Consequences
- **+** The repo self-documents for anyone joining, not just the original author's local agent session.
- **+** Decisions have one immutable home each; AGENTS.md stays a current-state reference without duplicating rationale.
- **+** No misleading SemVer changelog for a repo that does not release versions; history lives in git and the ADRs.
- **−** ADR discipline is now a maintenance expectation: consequential decisions get a record, and AGENTS.md links out rather than re-explaining.
- The `architecture/` folder is hidden from the Codespace file explorer (contributor infra, not learner-facing), alongside the other infrastructure files.

## Alternatives considered
- **A single `DESIGN_DECISIONS.md`** — rejected: loses per-decision immutability, supersession tracking, and stable `ADR-NNNN` references; it would effectively be AGENTS.md's decisions section renamed, reintroducing drift.
- **Keep the SemVer CHANGELOG** — rejected: this repo has no releases to log.
- **Keep design notes only in the gitignored CLAUDE.md** — rejected: invisible to contributors, the problem this ADR set solves.
