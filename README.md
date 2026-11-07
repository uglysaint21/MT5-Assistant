# MT5 Assistant

A local-first Windows desktop application for monitoring and analysing MetaTrader 5 accounts, trading activity, portfolio exposure, performance and Expert Advisors (EAs), with carefully safeguarded position and pending-order management.

> **Status: Requirements and architecture specification.** This repository currently documents the intended product and implementation. Do not assume planned features are implemented or production-ready until code, tests and releases demonstrate that.

## Product direction

MT5 Assistant is monitoring-first and supports one connected MT5 account at a time. It supports demo and real accounts, netting and hedging modes, and broker-supported instruments. It does not open new trades. Selected management operations are limited to modifying positions and pending orders, closing positions (including partial and account-wide close), and cancelling pending orders.

The first public release is intended to include MT5 connectivity, account monitoring, dashboard, history, account/instrument/EA analytics, risk alerts, on-demand PDF/XLSX/CSV reports and the selected limited management operations.

## Technology direction

| Layer | Planned technology |
| --- | --- |
| Desktop shell | Electron |
| UI | React, TypeScript, HTML and CSS |
| Local service | Bundled Python child process |
| MT5 integration | Official MetaTrader5 Python package and installed MT5 desktop terminal |
| Local process protocol | Versioned JSON messages over stdin/stdout |
| Local protection | Windows DPAPI plus password hashing |
| Distribution | Signed, 64-bit Windows MSI |
| Source control and CI | Public GitHub repository and automated workflows |

Python owns MT5 communication, data synchronisation, financial calculations, EA attribution, risk evaluation and report generation. The renderer must not access Node.js or the filesystem directly.

## Documentation

1. [Product requirements](docs/01-product-requirements.md)
2. [System architecture (original summary)](docs/02-system-architecture.md)
17. [Full architecture overview](docs/17-architecture-overview.md)
18. [Component boundaries and responsibilities](docs/18-component-design.md)
19. [Process protocol and data contracts](docs/19-protocol-and-data-contracts.md)
20. [Security, data lifecycle and operations](docs/20-security-data-operations.md)
21. [Architecture decisions and validation register](docs/21-architecture-decisions.md)
3. [MT5 integration](docs/03-mt5-integration.md)
4. [Data model and synchronisation](docs/04-data-model-and-synchronisation.md)
5. [Financial analytics](docs/05-financial-analytics.md)
6. [EA monitoring](docs/06-ea-monitoring.md)
7. [Trade management and risk](docs/07-trade-management-and-risk.md)
8. [UI/UX specification](docs/08-ui-ux-specification.md)
9. [Security and privacy](docs/09-security-and-privacy.md)
10. [Notifications and alerts](docs/10-notifications-and-alerts.md)
11. [Reporting and exports](docs/11-reporting-and-exports.md)
12. [Installer, updates and release](docs/12-installer-updates-and-release.md)
13. [Testing and acceptance](docs/13-testing-and-acceptance.md)
14. [Development roadmap](docs/14-development-roadmap.md)
15. [Requirements traceability](docs/15-requirements-traceability.md)
16. [Decisions and open questions](docs/16-decisions-and-open-questions.md)

## Non-negotiable product constraints

- One active MT5 account at a time; switching requires disconnecting the current account.
- Never persist the MT5 trading password. A manually entered password may exist in memory only for authentication.
- Refresh live account data every five seconds. Do not redownload full account history on every refresh.
- Retrieve all available history on first connection, then synchronise incrementally.
- Do not create a permanent trading-history database. Keep trading data in temporary cache with configurable retention. Persist only application settings, layouts, custom EA metadata, diagnostic logs and user-exported reports.
- Use broker/server time for trading-day boundaries and reporting periods. Daily risk reset has a separately configurable timezone.
- Treat account capital allocation and market exposure as different concepts.
- Exclude deposits and withdrawals from trading profit and adjust percentage returns for external cash flows.
- Clearly identify stale, incomplete, unavailable and inferred data. Never fabricate missing metrics.
- Never retry an uncertain trade-management request blindly after timeout or backend recovery. Reconcile actual MT5 state first.
- Monitoring continues while minimised to the system tray. Explicit exit stops background monitoring.
- No automatic telemetry. Diagnostics leave the device only after explicit user permission.

## Development principles

Use contract-first TypeScript interfaces and versioned JSON process messages. Validate external MT5 data and all process/IPC messages. Keep calculations in one shared Python analytics engine. Treat trade execution as a high-risk side effect: confirmation, broker validation, account-state reconciliation and per-item outcomes are mandatory.

Use semantic versioning (major.minor.patch), publish stable releases only, and keep confirmed requirements separate from architect recommendations and open questions.

## Disclaimer

This is a planning specification, not a claim of implemented functionality or a guarantee of trading safety. MT5 Assistant is independent and is not affiliated with or endorsed by MetaQuotes. Financial metrics are informational and must be checked against broker records. Trading involves risk.
