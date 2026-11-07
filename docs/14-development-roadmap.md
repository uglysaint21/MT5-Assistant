# 14 — Development roadmap

## Recommended delivery strategy
Architect recommendation: develop in cohesive phases, then publish the first stable public release only after all agreed first-release capabilities and acceptance criteria are satisfied. Phases are internal milestones, not promises of separate public releases.

## Phase 0 — Specification and engineering foundation
Resolve open decisions and validate MT5/Python compatibility. Establish monorepo, TypeScript/Python tooling, formatting, linting and CI. Define JSON protocol schemas, domain models, error taxonomy and threat model. Create test fixtures and sample MT5 datasets.

## Phase 1 — Desktop foundation and security
Electron/React shell, navigation, theme, settings and app-password flow. Secure preload/IPC. Python child-process manager and versioned protocol. Local settings, DPAPI integration, diagnostics and lifecycle.

## Phase 2 — MT5 connection and monitoring
Terminal detection/manual selection, launch, authentication and reconnect. Account snapshot, symbols, positions, pending orders. Five-second refresh, stale-data state and initial/incremental history sync. Account/history tables with data-quality indicators.

## Phase 3 — Shared analytics
Position/deal reconstruction and cash movement classification. Net/gross PnL, commissions, swaps, returns and drawdown. Portfolio capital allocation and market exposure. Instrument and account analytics.

## Phase 4 — EA monitoring and alerts
Comment attribution, optional magic fallback and custom metadata. EA grouping/instance views and performance. Optional MQL5 heartbeat and evidence-aware status. Alert engine, cooldowns, recovery and tray notifications.

## Phase 5 — Trade management and reporting
Broker constraints and risk evaluation. Confirmed management operations and emergency close-all. Reconciliation of uncertain outcomes. PDF/XLSX/CSV reports and customisation.

## Phase 6 — Hardening and first public release
Full E2E, regression, real-terminal and clean-Windows testing. Security, performance, installer, update and uninstall validation. Documentation, code signing, stable version tag and public MSI release.

## Prioritisation
First-release priorities include connection/monitoring, dashboard/account statistics, history, EA analytics, risk/notifications, account analytics/charts and reports/exports. Selected trade management is also included with safeguards. Do not defer these without explicit scope change.
