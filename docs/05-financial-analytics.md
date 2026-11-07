# 05 — Financial analytics

## Single calculation engine
Implement calculations in one Python analytics package and reuse outputs for dashboard, account analytics, EA pages, instrument pages and reports. UI components must not independently recalculate PnL.

## PnL definitions
Primary performance metric is net PnL after commissions and swaps. Show separately gross trading profit/loss, commissions, swaps/financing, other broker fees where supplied, net trading PnL, deposits, withdrawals and other cash movements.

For closed deals, net contribution reconciles from broker-provided profit, commission, swap and fee fields according to documented MT5 semantics. Avoid double-counting costs when aggregating deal and position records. Floating PnL comes from open positions and is reconciled to MT5 account snapshot. Combined PnL may show realised plus floating results; cash movements are not trading profit.

## Cash-flow-adjusted returns
Exclude deposits/withdrawals from trading profit. Calculate equity-based percentage returns adjusted for external cash flows. Architect recommendation: use time-weighted return when sufficiently frequent valuations and cash-flow timestamps exist; otherwise use a documented Modified Dietz approximation over the interval. Label method and limitations. Do not divide PnL by arbitrary starting balance when flows materially distort results.

## Time boundaries
Use broker/server time for trading-day and report boundaries. Dashboard periods: today, current week, current month, previous month, current quarter, current year, previous year and all time. Daily risk reset uses a separately configurable timezone. Daily summary delivery time is interpreted in broker/server time. Reports support custom date ranges.

## Performance and risk metrics
Implement where source data supports: realised/floating/total net PnL; cash-flow-adjusted return; equity and balance curves; peak equity, current and maximum drawdown from peak equity; win rate; profit factor; average/largest win and loss; average duration and risk/reward where risk data exists; consecutive wins/losses; trading volume; long/short; daily/weekly/monthly/yearly/all-time performance; instrument and EA contribution.

Drawdown requires sufficiently complete historical equity. If only deal history exists, do not represent a deal-derived approximation as account-equity drawdown.

## Portfolio
Provide separate views for capital/account allocation (balance, equity, used/free margin) and market exposure by instrument and buy/sell direction. Do not present forex notional exposure as owned capital. Use account currency and broker-provided conversions where available. If conversion data is unavailable/stale, show unconverted values or mark unavailable rather than inventing rates.

## Reconciliation
Use broker precision and account currency. Validate totals against MT5 snapshots and history. Surface rounding differences and incomplete data. Keep gross/net and cost components visible at account and trade level.
