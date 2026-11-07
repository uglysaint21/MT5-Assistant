# 06 — Expert Advisor monitoring

## Discovery and attribution
Discover EAs from historical deals and current positions. Primary attribution signal is trade comment. Magic Number is optional fallback when comments are absent or inconclusive. Do not assume comment or magic data uniquely identifies an EA without validation.

Store attribution method and confidence: confirmed, inferred or unknown. Allow custom EA names, descriptions and categories. Preserve original comment and magic metadata. Treat each EA instance separately by default, with a switch between individual-instance and grouped views; grouping must not erase instance history.

## EA information
Show name/description, instance identity, symbol association, current instruments, allocation/exposure, historical net profit, gross profit, commissions, swaps, floating PnL, historical loss/profit, winning/losing trades, win rate, trade count, average win/loss, largest win/loss, profit factor, maximum drawdown, average holding time, last trade time, open positions and performance chart. Support daily, weekly, monthly, yearly and all-time performance, equity curves and EA comparisons.

## Runtime status
Evidence requested includes EA attached to MT5 chart, terminal Algo Trading permission, recent trade activity, recent heartbeat and open positions. Account history/open positions alone cannot prove EA is attached or currently executing. A running EA may have no recent trades; a position may remain after an EA stops.

Architect-recommended states: RUNNING, IDLE, INACTIVE, UNKNOWN. Show evidence and timestamp. Do not claim every state can always be measured.

## Optional MQL5 companion
Provide guided optional installation/configuration if a lightweight MQL5 heartbeat is required. It may report instance ID, chart/symbol, EA identity, Algo Trading permission and heartbeat timestamp. Use a versioned local-only validated message format. Companion must not execute trades or alter strategy behaviour.

If not installed/unsupported, continue account monitoring and label runtime status unknown/inferred. It is not required for ordinary account monitoring.

## Management and reports
Allow custom names/descriptions, categories, grouped/instance views, detailed reports and individual EA exports. Support EA/instance filters. Do not expose unselected EA start/stop controls.
