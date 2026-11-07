# 07 — Trade management and risk

## Scope
The app is primarily for monitoring. Do not implement opening new market or pending orders. Permitted actions only: modify an open position; partially/full close an individual position; close all open positions; modify a pending order; cancel a pending order. Close-all applies to all open positions and does not cancel pending orders.

## Global controls
Trade management enabled by default, with master switch to disable ordinary management. Monitoring and alerts continue when management is disabled. Disable controls when market/session is closed or broker metadata says operation unavailable. Backend revalidates all conditions at execution time; renderer state is not authoritative.

## Confirmation and transparency
Every management action requires confirmation. Show account identity, symbol, action, target position/order ID, direction, volume, relevant price/SL/TP fields and estimated spread/commission/other costs where available. Explain estimates and limitations.

After sending, show success, rejection, partial completion or unknown outcome. For close-all, show per-position results and summary. Never report success based solely on request submission.

## Broker validation
Retrieve current broker limits and validate min/max/step volume and app maximum-lot setting; symbol trade mode and market session; filling mode and allowed action; stop/freeze distance and price precision; margin/account restrictions where exposed. Server/broker remains final authority. Re-check immediately before sending.

## Risk controls
- Configurable maximum lot size.
- Configurable account-wide daily loss threshold in account currency.
- Configurable minimum margin-level warning threshold.
- Configurable account-wide drawdown warning percentage.
- Conservative architect-recommended defaults, clearly labelled as defaults and not guarantees.
- Daily loss reset timezone is user-configurable.
- When daily loss threshold is reached, warn and disable further ordinary trade-management actions for the entire account. Do not automatically close positions.

## Emergency close-all
Provide a distinct emergency close-all control with explicit confirmation. It attempts to close all open positions but cannot guarantee execution. It does not cancel pending orders. Architect recommendation: keep it separately available when ordinary management is blocked by risk threshold or ordinary management master switch, subject to confirmation and current broker/market constraints. If a future setting disables all trading operations, define its interaction with emergency close-all explicitly.

## Failure and uncertain outcomes
Timeout, process crash or lost connection after submission means outcome is unknown, not failed. Never automatically resend. Reconnect, retrieve positions/orders/deals, reconcile intended action against actual state, then present resolved or still-unknown status. Use unique local operation IDs; do not claim MT5 offers exactly-once execution unless verified.

## Auditability
Maintain local action log: timestamp, account identity, action, target IDs, requested parameters, confirmation, broker response and reconciled outcome. Never log passwords/secrets.
