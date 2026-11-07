# 02 — System architecture

## Recommended architecture

Use an Electron + React + TypeScript desktop shell with a bundled Python service. Python is authoritative for MT5 access, data normalisation, synchronisation, financial calculations, EA attribution, risk evaluation and report generation.

~~~mermaid
flowchart TB
  UI[React + TypeScript renderer]
  PRELOAD[Minimal typed preload API]
  MAIN[Electron main process]
  PY[Bundled Python service]
  MT5[Installed MT5 terminal]
  CACHE[Temporary trading-data cache]
  STORE[Persistent app settings and EA metadata]
  REPORTS[User-exported reports]
  UI --> PRELOAD --> MAIN
  MAIN <-->|Versioned JSON lines| PY
  PY <-->|MetaTrader5 Python package| MT5
  PY --> CACHE
  MAIN --> STORE
  PY --> REPORTS
~~~

## Module boundaries

### Electron main
Owns lifecycle, single-instance policy, window/tray, installer/update orchestration and Python child process. It is the only renderer-facing IPC boundary. It does not calculate financial metrics or call MT5 directly.

### React renderer
Owns pages, widgets, tables, charts, forms and accessible interactions. It holds presentation state only; no unrestricted Node or filesystem access. It calls a narrow typed preload API.

### Python service
Recommended modules:
- mt5: terminal discovery, connection, account, positions, orders, history, symbols and trade operations.
- sync: initial history sync, incremental sync, deduplication and reconciliation.
- domain: normalised entities and enums.
- analytics: PnL, returns, drawdown, portfolio, instrument and EA calculations.
- ea: attribution, instance registry, status and optional heartbeat ingestion.
- risk: limits, evaluations and action gating.
- alerts: state transitions, cooldowns and notification events.
- reports: report models and PDF/XLSX/CSV exporters.
- cache: temporary trading-data cache and retention.
- protocol: JSON message schemas, validation and version negotiation.

## Process communication contract
Use newline-delimited JSON over Python stdin/stdout. Stdout is reserved exclusively for protocol messages; diagnostics go to stderr or rotating local logs.

Every request contains protocol version, unique request ID, operation name and validated payload. Every response contains the matching request ID and either a typed result or structured error (code, safe message, optional details). Unsolicited events use a separate event envelope. Define timeouts, cancellation, maximum message size, schema validation, startup handshake and protocol-version mismatch behaviour.

Do not send arbitrary Python commands or filesystem paths from the renderer. Main validates renderer requests; Python validates its own boundary.

## Lifecycle and recovery
1. Electron starts, verifies app-password gate and loads settings.
2. Main starts bundled Python and waits for version/capability handshake.
3. Python discovers/attaches to selected terminal and validates account data.
4. Dashboard renders available current data; history sync runs in background.
5. Every five seconds, refresh live account/position/order state; history uses incremental sync.
6. On terminal disconnect, mark data stale immediately and reconnect with progressive backoff and a cap.
7. On Python crash, restart under a bounded restart policy, reconnect and reconcile state.
8. On explicit exit, stop polling, stop child process gracefully and close. Minimise-to-tray is not exit.

A restarted backend must not repeat a trade operation whose result is unknown. Reconcile positions/orders/history before re-enabling management.

## Performance and architecture decisions
Use asynchronous IPC and background work. Long analytics/report jobs must not block UI or Electron main event loop. Provide progress and cancellation. No separate server/cloud service is required. MQL5 is optional and only for terminal-side EA heartbeat/status evidence.
