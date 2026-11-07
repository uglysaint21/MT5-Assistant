# 11 — Reporting and exports

## Generation model
Reports are generated on demand only. Daily, weekly, monthly, yearly and all-time are report period options, not scheduled jobs. Support account-level and EA-level reports.

## Formats and destination
PDF, Excel XLSX and CSV. Let user choose export folder. Keep reports until manually deleted. Report generation must not block the interface; provide progress, cancellation and clear failure messages.

## Filters and customisation
Choose date range, sections and charts; include/exclude individual EAs and instruments; choose account-level or EA-level report; include detailed trade-by-trade information.

## Report contents
Selectable sections:
- Account overview and key statistics.
- Realised and floating PnL.
- Deposits, withdrawals, commissions, swaps and fees.
- Equity and balance charts.
- Drawdown and risk statistics.
- Open and closed trade breakdown.
- Instrument-level performance.
- EA performance summaries.
- Winning/losing trade statistics.
- Trading activity summary.
- Detailed deal/trade rows.

## Consistency and limitations
Use shared Python analytics engine. Separate cash movements from trading performance. Show gross profit, costs and net profit separately. Label broker/server time and account currency. Disclose incomplete history, unavailable equity series, inferred EA attribution and unsupported conversions. Never fabricate missing values.

## File safety
Use safe filenames and atomic export where practical. Do not overwrite existing files without confirmation. Remind users reports may contain sensitive account information.
