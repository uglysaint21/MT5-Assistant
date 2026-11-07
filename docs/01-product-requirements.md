# 01 — Product requirements

## Purpose and users
MT5 Assistant is a local-first Windows desktop application for monitoring and analysing one connected MetaTrader 5 account at a time. It is monitoring-first, but includes a defined limited set of trade-management operations. It is not a trade-entry platform and must not open new market or pending orders. The intended audience is the general public; users install the app and configure their own terminal/account.

## Platform
- Windows 10 and Windows 11, 64-bit.
- Existing MetaTrader 5 desktop terminal required.
- Demo and real accounts; netting and hedging modes.
- One connected account at a time. Switching requires disconnecting and connecting another account.

## First-release scope
1. Terminal discovery, manual executable selection, authentication and reconnection.
2. Account dashboard and account statistics.
3. Open positions, pending orders and complete available trading history.
4. Portfolio, instrument and account analytics.
5. EA discovery, attribution, performance and runtime-status reporting.
6. Risk monitoring, in-app and Windows notifications.
7. On-demand PDF, XLSX and CSV reports.
8. Selected trade-management operations with safeguards.
9. Settings, custom dashboard layouts, local security, MSI installation and updates.

## Functional requirements

### Terminal and account
- Detect installed MT5 terminals automatically and remember the selected terminal; permit manual browsing.
- Launch the selected terminal if it is not running.
- Prefer an already authenticated session; offer manual login using account number, broker/server and trading password.
- Never save the MT5 trading password.
- Validate terminal connectivity, account authentication and data retrieval during setup.
- Show connection state and last successful update; reconnect automatically with increasing retry intervals.
- Permit disconnect and one-at-a-time account switching.

### Dashboard and account views
Display balance, equity, available/free/used margin, margin level, leverage, floating PnL, realised PnL, total PnL, daily PnL and return, deposits, withdrawals, position count and pending-order count. Widgets include account health, positions, pending orders, EA summary, portfolio allocation, recent activity, connection state and daily performance.

### Trading activity
Show open positions and pending orders. Retrieve all history available from MT5; initially synchronise all history and subsequently retrieve changes incrementally. History filters: date range, instrument, direction, profit/loss, EA and position/deal identifier. Position table includes symbol, direction, volume, entry/current price, SL/TP, floating PnL, swap/commission, open time and position identifier.

### Instruments and brokers
Discover all instruments exposed by the terminal. Support forex, metals, indices, shares, crypto, energy and broker-supported futures/other instruments. Preserve broker-native symbol names and suffixes/prefixes. A discovered symbol is not necessarily visible, tradable or supported for every operation. Adapt operations to broker rules; monitoring remains available in read-only mode if some operations are unsupported.

### Analytics
Provide account, instrument and EA analytics. Primary PnL is net of commission and swap, while gross profit, commissions, swaps and net profit are shown separately. Exclude cash deposits/withdrawals from trading profit and adjust returns for cash flows. Use account currency and broker/server time for trading-period boundaries.

### EA monitoring
Discover EAs from trade comments and optionally use Magic Numbers as fallback. Support custom names, descriptions and categories, separate instance views and grouped views. Show performance, open positions, exposure, trade counts, win rate, profit factor, drawdown, holding time and charts. Runtime status must indicate evidence quality.

### Trade management
Allowed actions only: modify open positions; partially or fully close an individual position; close all open positions; modify pending orders; cancel pending orders. Do not provide new trade entry, reversal or other unselected operations. See document 07.

### Reports and alerts
Generate reports on demand only. Support PDF, XLSX and CSV, custom date ranges, section/chart selection, EA/instrument inclusion and detailed trade rows. Notifications cover connection, EA activity, margin, loss/drawdown, position/order events and daily summaries.

## Non-functional requirements
Five-second live refresh; responsive UI; background historical sync; fast startup with progressive loading; automatic reconnect with progressive backoff; Python backend restart where possible; clean shutdown; no automatic telemetry; configurable stale-data/cache/risk thresholds; stable public MSI releases and automated tests.

## Out of scope
Opening new market or pending orders; cloud account or cloud storage; automatic report scheduling; automatic liquidation on risk threshold; claiming EA runtime status based only on trade history; guaranteeing broker execution.
