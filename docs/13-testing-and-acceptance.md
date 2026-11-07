# 13 — Testing and acceptance

## Test layers
- Python unit tests for normalisation, synchronisation, PnL, returns, drawdown, risk and reports.
- TypeScript unit tests for UI state, formatting, validation and IPC client.
- Electron–Python integration tests using controlled child process and protocol fixtures.
- Simulated MT5 account fixtures covering netting, hedging, demo/real, partial closes, cash flows, commission and swap.
- End-to-end tests for setup, dashboard, history, EA analytics, reports, notifications and management workflows.
- Regression tests for every fixed defect.
- Automated GitHub workflow tests on changes and before release.
- Real MT5 terminal validation before release.
- Installer/uninstaller tests on clean Windows 10 and 11 x64 systems.

## Mandatory acceptance criteria
A release candidate must demonstrate:
1. Successful installation and first-launch setup on clean Windows 10 and Windows 11 x64 systems.
2. Successful connection to supported demo and real MT5 accounts.
3. Correct monitoring of netting and hedging accounts.
4. Accurate reconciliation of account statistics and trading history against MT5.
5. Correct PnL, cash-flow, commission, swap and drawdown calculations.
6. Reliable EA identification and transparent EA status reporting.
7. Correct enforcement of broker constraints and risk safeguards.
8. Safe operation of all selected trade-management actions.
9. Successful recovery from terminal disconnection and Python backend failure.
10. Successful report generation and export.
11. Secure app-password handling and local data protection.
12. Passing automated tests and release validation checklist.

## Critical safety tests
- No new trade can be opened through UI or backend.
- Every management action requires confirmation.
- Market closed/broker-disabled operation is rejected locally and rechecked by backend.
- Volume minimum/maximum/step and app maximum lot are enforced.
- Daily loss limit disables ordinary management and does not auto-close positions.
- Emergency close-all requires confirmation, attempts all open positions, does not cancel pending orders and reports each result.
- Timeout/crash after request does not cause automatic duplicate resend; account state is reconciled first.
- Switching accounts cannot leak cached data between accounts.

## Data-quality tests
Duplicate/out-of-order deals do not double-count; partial closes group correctly; missing history/equity series produce explicit limitations; cash movements do not inflate PnL; broker/server time and DST transitions are tested; stale state clears only after successful recovery.

## Release checklist
CI green; unit/integration/E2E tests pass; real-terminal smoke tests pass for supported account modes; security and dependency/licence review complete; MSI install/upgrade/repair/uninstall tested; update signature and confirmation tested; documentation/release notes updated; no known critical data-integrity or trade-management safety defects.
