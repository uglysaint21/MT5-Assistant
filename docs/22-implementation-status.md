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
- [x] Verify the GitHub Actions workflow on the latest PR head and resolve failures. Earlier runs exposed TypeScript import interoperability, a case-sensitive Python assertion and one formatting issue; all were fixed. Latest run 42418697169 (run #195) passed both jobs, including Prettier, TypeScript typecheck, 13 TypeScript tests, npm high-severity audit, Ruff lint/format and 29 Python tests. The initial npm install reported two critical and two moderate advisories; after upgrading Vitest and Ajv, the high-severity audit gate passes.
- [ ] Add stronger property/fuzz tests for protocol parsing and request lifecycle under concurrency.
- [x] Extend synthetic MT5 fixtures for duplicate/out-of-order history delivery, bounded overlap synchronisation, broker/server time and DST edge cases.
- [ ] Close or explicitly record the remaining compatibility/toolchain and protocol-schema decisions in [21 — Architecture decisions](21-architecture-decisions.md).

## Validation evidence

- Python protocol, schema, fixture, history-sync, operation-registry and error-catalogue tests: **29 passed** in an isolated verification workspace using Python 3.13.5 and pytest 9.0.2. The CI target remains Python 3.12 and the project constraint is Python 3.11+.
- TypeScript CI: Prettier check, full tsc --noEmit and all 13 Vitest/Ajv tests passed in run #195.
- GitHub Actions: latest run #195 (42418697169) passed both TypeScript and Python jobs on the current PR head.
- Windows/MT5 compatibility: not yet tested.

## Delivery discipline

- Follow the phases and dependencies in document 14; do not start later-phase product features before their foundation is in place.
- Treat architecture recommendations and open decisions in document 21 as unresolved until evidence and approval are recorded.
- Keep the first public-release scope intact unless the product requirements are explicitly changed.
- A feature is complete only when its tests, documentation and relevant acceptance evidence are present.
- Trade-management capabilities must not be exposed until the dedicated risk, confirmation and reconciliation design is implemented and tested.

## Current implementation boundary

The current code is a protocol/tooling foundation only. It does not yet launch Electron, render a UI, start a Python child process, connect to MetaTrader 5, persist settings, or implement any trading operation. No trading capability is currently implemented.
