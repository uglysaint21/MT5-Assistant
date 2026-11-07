# Protocol and MT5 fixtures

All records in this directory are synthetic test data. They do not represent a real brokerage account or person.

- Protocol envelope fixtures are language-neutral golden inputs shared by desktop and Python contract tests.
- `mt5/account-history-cases.json` provides a deterministic starting dataset for netting/hedging, partial closes, commissions, swaps, deposits, withdrawals, broker symbol suffixes and distinct position identifiers.
- Monetary and volume values are decimal strings to avoid implying binary floating-point accounting.
- Timestamps are UTC examples. Production adapters must preserve broker/server time interpretation and must not silently treat UTC as broker time.

These fixtures establish test coverage scenarios; they do not yet define expected financial analytics results. Golden PnL/return/drawdown outputs belong with the Phase 3 analytics tests once calculation definitions and edge-case semantics are implemented.
