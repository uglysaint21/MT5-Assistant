# 16 — Decisions and open questions

## Confirmed decisions
- Windows desktop app, public x64 MSI, Windows 10/11.
- Electron + React + TypeScript frontend; Python backend.
- Python child process communicates by JSON over stdin/stdout.
- Official MetaTrader5 Python package and separately installed MT5 terminal.
- One active account; demo and real; netting and hedging.
- Five-second live refresh; full initial history then incremental sync.
- No permanent trading-history database; configurable temporary cache.
- App password on first and every later launch; five-failure temporary lock; inactivity lock; no Windows Hello/password recovery.
- Never persist MT5 trading password.
- DPAPI for sensitive local app data.
- Monitoring-first with selected management operations; no new trade entry.
- Confirmations, broker validation, max lot, daily loss threshold, margin and drawdown warnings.
- Risk threshold blocks ordinary management; no automatic liquidation. Emergency close-all is separate, confirmed and positions-only.
- Broker/server time for reporting/trading-day calculations; configurable risk reset timezone.
- No telemetry; diagnostics shared only with permission.
- Reports on demand, PDF/XLSX/CSV, user-selected folder, retained until deleted.
- User-initiated backup/restore for settings, layouts and EA metadata.
- Public source, stable releases only, semantic versioning.

## Architect recommendations requiring validation
1. Monorepo with Electron main, React renderer and modular Python service.
2. Argon2id password hashing with calibrated work factor and versioned parameters. DPAPI protects data at rest; it is not a password hash.
3. Evaluate rolling 30-day temporary-cache default, configurable and user-clearable.
4. Configurable stale thresholds per data category; a missed five-second poll should use a tested grace period, not one universal threshold.
5. Conservative configurable risk defaults, never claimed to guarantee protection. Numerical defaults require risk review.
6. Time-weighted return where valuation/cash-flow data permits; Modified Dietz approximation otherwise, clearly labelled.
7. Discrete widget size classes to reconcile fixed-size and resizable requirements.
8. EA states RUNNING/IDLE/INACTIVE/UNKNOWN with evidence/confidence.
9. Optional guided MQL5 companion for local heartbeat; no trade execution.
10. Evaluate Apache-2.0 for permissive licensing with express patent grant; MIT is simpler. Final choice is not approved.
11. Sign MSI and updates; verify signatures before installation.
12. Phased implementation; first public release only after all first-release scope and acceptance criteria pass.

## Open questions before implementation
- Exact supported Python version and MetaTrader5 package/terminal build matrix.
- Installer framework and Electron packaging technology.
- Cache retention default, maximum and storage format.
- Stale-data thresholds per account/position/history/EA status.
- Numerical default risk thresholds and cooldown values.
- Whether backup archives should be encrypted and restore behaviour across schema versions.
- Final licence and dependency redistribution review.
- MQL5 heartbeat transport and deployment constraints.
- Exact app-data reset UX and deletion boundaries.
- Update distribution channel (e.g. GitHub Releases) and signature verification.
- Support policy and issue-reporting workflow.

## Product contradictions resolved
- Fixed widget sizes vs resize: discrete predefined size classes.
- Monitoring-first vs management: only selected management operations; never add trade entry.
- No permanent trading DB vs persistent app data: trading history is temporary cache; settings/layouts/EA metadata/reports/logs persist separately.
- Master switch vs emergency close-all: recommendation is separate emergency operation, always confirmed and subject to broker/market constraints.
- Market closed: disable management controls but keep monitoring.
- EA status: never infer runtime solely from recent trades or open positions.

## Change control
Any change to account scope, trading operations, data retention, credential handling, financial formulas or release acceptance criteria must update this document and relevant specification, with corresponding traceability and test updates.
