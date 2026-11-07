# 10 — Notifications and alerts

## Channels
Support in-app and Windows desktop notifications. Sounds can be enabled/disabled in Settings.

## Events
- MT5 terminal disconnected/reconnected.
- Connection or account authentication failure.
- EA stopped/inactive or resumed trading.
- Low margin/margin-level warning.
- Daily loss threshold reached.
- Drawdown threshold reached.
- Position opened, modified or closed.
- Pending order triggered.
- Daily performance summary.

## Thresholds and schedules
Risk thresholds are configurable with conservative architect-recommended defaults. Minimum margin-level warning and account-wide drawdown warning are configurable. Daily loss threshold is in account currency and account-wide. Daily loss reset timezone is configurable. Daily summary delivery time is configurable and interpreted in broker/server time.

## State and cooldown
Model each alert as NORMAL, TRIGGERED or RECOVERED. Notify immediately on first trigger, then apply configurable cooldown to repeated notifications. Notify when condition recovers. Avoid a new alert every five-second polling cycle while a condition remains triggered.

## History and background behaviour
Keep searchable in-app notification history until user clears it. Store event time, type, severity, state, relevant symbol/EA and concise explanation. Do not store secrets.

Continue evaluating alert conditions and sending Windows notifications while minimised to tray. Stop when explicitly exited. During stale/disconnected periods, distinguish unavailable monitoring from a normal condition; do not imply thresholds are checked when data is stale.
