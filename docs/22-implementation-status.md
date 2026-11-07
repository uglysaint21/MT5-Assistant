# 22 — Implementation status

This document tracks verified repository implementation against the sequence in [14 — Development roadmap](14-development-roadmap.md) and [17 — Architecture overview](17-architecture-overview.md).

A checked item means code or automation exists in the repository; it does not imply production readiness. Validation status must be based on executed checks, not intended CI configuration.

## Phase 0 — Specification and engineering foundation

### Implemented in this increment
- [x] Establish a monorepo layout for the desktop TypeScript package and Python service.
- [x] Add strict TypeScript compiler configuration, pin direct desktop development dependencies and add Prettier formatting scripts/configuration.
- [x] Add Python package metadata, pytest configuration and Ruff lint/format rules.
- [x] Define protocol-v1 request, ready, success/error response and event JSON Schemas.
- [x] Define TypeScript protocol envelope types and strict runtime guards.
- [x] Add Python JSON Lines framing with a 1 MiB frame bound, protocol-version validation and duplicate JSON-key rejection.
- [x] Add strict Python envelope validation, including exact-field checks and UTC event timestamps.
- [x] Add a bounded active request-ID registry that rejects duplicate in-flight IDs.
- [x] Define a stable protocol error-code catalogue with safe messages, retryability and recovery guidance; add coverage tests for the required error set.
- [x] Define explicit operation and capability registries, marking all operations as planned, mapping operations to capabilities, and listing prohibited trade-entry actions.
- [x] Add shared protocol golden fixtures and validate them in Python and TypeScript test suites.
- [x] Add Ajv and Python jsonschema-based schema validation tests.
- [x] Add malformed JSON, oversized frame, duplicate-key, duplicate-active-ID, unknown-field, invalid timestamp, malformed envelope and unsupported-version tests.
- [x] Add synthetic MT5 netting/hedging account and history fixtures covering partial closes, commissions, swaps, deposits, withdrawals, broker symbol suffixes, distinct position IDs and decimal-safe position-volume reconciliation.
- [x] Add GitHub Actions jobs for TypeScript and Python verification, including Prettier/Ruff checks and an npm high-severity dependency-audit gate; upgrade actions to maintained Node 24-compatible releases.
- [x] Add baseline generated-artifact, environment and secret exclusions.
- [x] Document developer setup and the Phase 0 security threat model/test mapping.

### Remaining Phase 0 work
- [ ] Validate the supported Windows 10/11, Python, MetaTrader5 package and terminal build compatibility matrix on clean target systems.
- [ ] Generate and commit reproducible npm and Python dependency lockfiles. Direct desktop development dependencies are pinned, but transitive dependency resolution is not yet locked.
- [ ] Verify the GitHub Actions workflow on the latest PR head and resolve any failures. Earlier runs exposed TypeScript import interoperability, a case-sensitive Python assertion and one formatting issue; those were fixed. Runs #195 (42418697169) and #197 (42418765126) passed both jobs for earlier commits, including Prettier, TypeScript typecheck, 13 TypeScript tests, npm high-severity audit, Ruff lint/format and 29 Python tests. They do not validate the later fuzz/concurrency test commit; a fresh successful run for the current PR head is still required. The initial npm install reported two critical and two moderate advisories; after upgrading Vitest and Ajv, the high-severity audit gate passed in those earlier runs.
- [x] Add deterministic malformed-input fuzz coverage and a concurrent duplicate-request-ID registration test; make the active-ID registry thread-safe.
- [x] Extend synthetic MT5 fixtures for duplicate/out-of-order history delivery, bounded overlap synchronisation, broker/server time and DST edge cases.
- [x] Record unresolved compatibility, toolchain and protocol-schema decisions in [21 — Architecture decisions](21-architecture-decisions.md); OPEN-01 and OPEN-13 remain blocking until validated and decided.

### Outstanding external validation gates

The following cannot be truthfully closed from the current Linux/GitHub-only execution environment and remain Phase 0 blockers:
- [ ] Generate and commit `package-lock.json` and a fully resolved Python lockfile using the supported package registries; no lockfile has been fabricated from direct pins.
- [ ] Run clean-install and compatibility checks on Windows 10 and Windows 11 x64 with the agreed Python, MetaTrader5 package and terminal-build matrix. This requires actual target systems and a broker/terminal installation.
- [ ] Close OPEN-01 (Windows/Python/MetaTrader5 compatibility) and OPEN-13 (protocol schema tooling) in the decision register with evidence and an explicit decision.

### Review workflow limitation

The prescribed two-axis Standards/Spec review has **not** been completed. The Build review workflow requires `docs/agents/issue-tracker.md`; that file is absent from this repository (the similarly named `docs/agents/issuetracker` path is also absent). The review workflow explicitly requires the project to run `/setup-matt-pocock-skills` to install/provide the issue-tracker integration before the review can be performed. CI success is not a substitute for that independent review. Do not mark the PR ready or begin Phase 1 until this review gate and the external validation gates above are resolved.

## Validation evidence

- Python protocol, schema, fixture, history-sync, operation-registry and error-catalogue tests: **29 passed** in an isolated verification workspace using Python 3.13.5 and pytest 9.0.2. The CI target remains Python 3.12 and the project constraint is Python 3.11+.
- TypeScript CI: Prettier check, full tsc --noEmit and all 13 Vitest/Ajv tests passed in run #195.
- GitHub Actions: run #197 (42418765126) completed successfully for the tracked commit; run #195 (42418697169) also passed both jobs. The new fuzz/concurrency tests in this increment require a fresh CI run before their results can be claimed.
- Windows/MT5 compatibility: not yet tested.
- Review workflow: blocked by the missing `docs/agents/issue-tracker.md` integration.

## Delivery discipline

- Follow the phases and dependencies in document 14; do not start later-phase product features before their foundation is in place.
- Treat architecture recommendations and open decisions in document 21 as unresolved until evidence and approval are recorded.
- Keep the first public-release scope intact unless the product requirements are explicitly changed.
- A feature is complete only when its tests, documentation and relevant acceptance evidence are present.
- Trade-management capabilities must not be exposed until the dedicated risk, confirmation and reconciliation design is implemented and tested.

## Current implementation boundary

The current code is a protocol/tooling foundation only. It does not yet launch Electron, render a UI, start a Python child process, connect to MetaTrader 5, persist settings, or implement any trading operation. No trading capability is currently implemented.
