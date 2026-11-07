# 22 — Implementation status

This document tracks verified repository implementation against the sequence in [14 — Development roadmap](14-development-roadmap.md) and [17 — Architecture overview](17-architecture-overview.md).

A checked item means code or automation exists in the repository; it does not imply production readiness. Validation status must be based on executed checks, not intended CI configuration.

## Phase 0 — Specification and engineering foundation

### Started in this increment
- [x] Establish a monorepo layout for the desktop TypeScript package and Python service.
- [x] Add strict TypeScript compiler configuration.
- [x] Add Python package metadata and pytest configuration.
- [x] Define the initial protocol-v1 request schema and canonical request fixture.
- [x] Add TypeScript process-response contracts and basic validation.
- [x] Add Python JSON Lines framing primitives with a 1 MiB frame limit and protocol-version check.
- [x] Add focused TypeScript and Python protocol tests.
- [x] Add GitHub Actions jobs for TypeScript and Python verification.
- [x] Add baseline generated-artifact, environment and secret exclusions.

### Remaining Phase 0 work
- [ ] Complete the protocol schemas for ready, success/error response and event envelopes.
- [ ] Define the complete stable error-code catalogue and operation/capability registry.
- [ ] Add cross-language golden fixtures and schema validation on both sides.
- [ ] Add malformed, oversized, duplicate-ID, unknown-field and unsupported-version contract tests.
- [ ] Create representative MT5 account/history fixtures for netting, hedging, partial closes, cash flows, commissions and swaps.
- [ ] Validate the supported Windows, Python, MetaTrader5 package and terminal compatibility matrix.
- [ ] Select and pin the supported toolchain versions; commit reproducible lockfiles.
- [ ] Complete the threat model and map security acceptance tests.
- [ ] Verify the CI workflow on GitHub and resolve all failures.

## Delivery discipline

- Follow the phases and dependencies in document 14; do not start later-phase product features before their foundation is in place.
- Treat architecture recommendations and open decisions in document 21 as unresolved until evidence and approval are recorded.
- Keep the first public-release scope intact unless the product requirements are explicitly changed.
- A feature is complete only when its tests, documentation and relevant acceptance evidence are present.
- Trade-management capabilities must not be exposed until the dedicated risk, confirmation and reconciliation design is implemented and tested.

## Current implementation boundary

The current code is a foundation slice only. It does not yet launch Electron, render a UI, start a Python child process, connect to MetaTrader 5, persist settings, or implement any trading operation. No trading capability is currently implemented.
