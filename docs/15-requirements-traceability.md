# 15 — Requirements traceability

This matrix maps confirmed requirement groups to implementation ownership and verification. Add individual test IDs as implementation begins.

| ID | Requirement group | Primary implementation | Verification |
| --- | --- | --- | --- |
| RQ-001 | Windows MSI, x64, Win10/11 | packaging/release | clean-install matrix |
| RQ-002 | Electron + React + TypeScript UI | desktop/renderer | UI and E2E tests |
| RQ-003 | Bundled Python child process | process manager/protocol | process integration tests |
| RQ-004 | MT5 auto-detect and manual path | Python mt5/terminal | discovery/connection tests |
| RQ-005 | Existing session/manual login; no password persistence | mt5/auth + security | credential handling tests |
| RQ-006 | One account, demo/real, netting/hedging | mt5/domain | account-mode test matrix |
| RQ-007 | Five-second live refresh | sync/live | timing and stale-state tests |
| RQ-008 | Initial full history + incremental updates | sync/history | dedupe/replay tests |
| RQ-009 | No permanent trading DB; temporary cache | cache/storage | retention and clear-cache tests |
| RQ-010 | Account dashboard and custom widgets | renderer/dashboard | UI/E2E tests |
| RQ-011 | Account, instrument, portfolio analytics | analytics | reference calculation fixtures |
| RQ-012 | Gross/net PnL and cash-flow adjusted returns | analytics/pnl | financial reconciliation tests |
| RQ-013 | EA discovery, attribution and status | ea | fixtures and heartbeat tests |
| RQ-014 | Notifications and configurable thresholds | alerts/risk | state/cooldown tests |
| RQ-015 | Limited management actions only | mt5/trade + risk | safety/broker-rule tests |
| RQ-016 | Emergency close-all, positions only | mt5/trade | per-position outcome tests |
| RQ-017 | PDF/XLSX/CSV on-demand reports | reports | export content tests |
| RQ-018 | App password, DPAPI, secure IPC | security/desktop | security test plan |
| RQ-019 | No telemetry; diagnostic consent | privacy/diagnostics | network and consent tests |
| RQ-020 | Backups for settings/layouts/EA metadata | storage/backup | backup/restore tests |
| RQ-021 | Auto-update check, user confirmation | updater | signed update tests |
| RQ-022 | GitHub CI, regression and E2E tests | workflows/tests | branch/release gates |
| RQ-023 | Public stable releases, semver | release | tag/package correspondence |
| RQ-024 | English-first, translation-ready | renderer/i18n | locale extraction tests |
| RQ-025 | User and architecture docs | docs | release checklist |

## Status conventions
- Confirmed: explicitly selected by user.
- Recommendation: architect-proposed default requiring validation/approval.
- Open: not yet decided or dependent on compatibility testing.

A requirement is not complete merely because its module exists. It needs acceptance evidence and traceability to a test or documented manual verification.
