# 18 — Component boundaries and responsibilities

This document decomposes the target architecture in [17 — Architecture overview](17-architecture-overview.md) into implementable components. Package names are recommendations; behaviour and ownership constraints are normative where they restate approved requirements.

## 1. Component map

| Component | Process | Responsibilities | Must not own |
|---|---|---|---|
| Renderer application | Renderer | Pages, widgets, forms, filters, charts, accessibility | Filesystem, MT5, trade policy, financial formulas |
| Preload bridge | Preload | Expose narrow typed capabilities | Generic IPC, Node, filesystem |
| IPC gateway | Main | Validate sender, channel, payload, auth state, request limits | Domain calculations |
| Desktop lifecycle | Main | Single instance, windows, tray, shutdown | MT5 vendor calls |
| Python supervisor | Main | Spawn, handshake, restart, terminate, protocol framing | Domain policy |
| Local security | Main + Python adapters | App password, lock state, DPAPI protection, redaction | MT5 password persistence |
| Protocol host | Python | Envelope validation, dispatch, event routing | Domain-specific persistence |
| MT5 terminal adapter | Python | Discovery, initialise/shutdown, account/market/trading API | UI formatting |
| Account service | Python application | Connect/disconnect, identity, snapshots | Vendor DTO leakage |
| Synchronisation service | Python application | Polling, initial/incremental history, dedupe, reconciliation | Permanent history storage |
| Domain model | Python domain | Normalised entities, invariants, state transitions | Framework/vendor dependencies |
| Analytics engine | Python | PnL, returns, drawdown, exposure, EA metrics | UI-specific chart formatting |
| EA service | Python | Attribution, identity metadata, evidence and status | Unverified runtime claims |
| Risk/trade service | Python | Allow-list, broker validation, confirmation binding, execution and reconciliation | New-order entry |
| Alert service | Python | Threshold evaluation, state/cooldown, notification events | UI notification rendering |
| Reporting service | Python | Report model, job lifecycle, exporter coordination | UI rendering |
| Cache adapter | Python | Temporary account-scoped cache, retention, clear | Permanent trade-history archive |
| Settings adapter | Main | Durable settings/layout preferences | Trading records |
| EA metadata adapter | Main or Python via narrow port | Custom names/descriptions/categories | MT5 password |
| Notification adapter | Main | Windows toast/tray notifications | Risk calculation |
| Optional heartbeat adapter | Python | Validate and timestamp local MQL5 heartbeat | Trade execution |

## 2. Python application use cases

Expose use cases, not internal classes, over the process protocol.

### Connection and account
- `discover_terminals()`
- `validate_terminal(path)`
- `connect_account(terminal_ref, credentials?)`
- `disconnect_account()`
- `get_connection_status()`
- `get_account_snapshot()`
- `switch_account(...)` — orchestrated as disconnect then connect, never concurrent.

Manual credentials must be transient. Avoid retaining them in request objects after authentication. Do not include credentials in response envelopes or error details.

### Monitoring and history
- `get_live_snapshot()`: account, positions, pending orders, symbol metadata required for display.
- `start_initial_sync()`: full available history as a cancellable job.
- `sync_history(cursor)`: overlap-window incremental sync.
- `reconcile_account()`: compare current state and recent history with MT5.
- `query_history(filters)`: read from current cache; report coverage and retention limitations.

### Analytics and EA
- `get_account_analytics(period)`
- `get_instrument_analytics(period, filters)`
- `get_portfolio_exposure()`
- `get_ea_instances()`
- `get_ea_analytics(period, instance_or_group)`
- `update_ea_metadata(identity, metadata)`
- `get_ea_runtime_evidence()`

All metric outputs include currency/time basis, calculation method where relevant, source coverage and data-quality state.

### Risk, management and alerts
- `evaluate_risk(scope)`
- `prepare_management_operation(intent)`
- `execute_management_operation(operation_id, confirmation_token)`
- `reconcile_management_operation(operation_id)`
- `evaluate_alerts()`
- `list_notifications(filters)`

The backend is the final authority. A renderer-supplied “risk passed” flag or displayed broker limit is never trusted.

### Reports
- `create_report_job(options, destination)`
- `get_job_status(job_id)`
- `cancel_job(job_id)`

Only a destination explicitly selected/approved by the user may be used. Do not allow arbitrary renderer-provided filesystem paths.

## 3. MT5 adapter subcomponents

Separate responsibilities behind a single adapter facade:
- **TerminalDiscovery:** candidate enumeration and manual path validation.
- **TerminalSession:** initialise/shutdown, terminal info, connected/account identity.
- **AccountReader:** account snapshot and account mode.
- **MarketReader:** symbol metadata, sessions, tick/price and operation capabilities.
- **PositionReader / OrderReader:** current state snapshots.
- **HistoryReader:** deal/order history retrieval with time windows and identifiers.
- **TradeGateway:** only approved modify/close/cancel actions.
- **ErrorMapper:** map vendor return codes/exceptions to stable internal codes.

Do not assume every symbol returned by the terminal is visible or tradable. Preserve exact symbol spelling. Query broker constraints near the time of a management operation and re-check before submission. Keep read-only monitoring available when trading operations are unsupported.

## 4. Renderer feature ownership

| Feature | Reads | User commands | Presentation-specific state |
|---|---|---|---|
| Dashboard | Snapshot, analytics, quality, alert summary | Refresh, navigate to detail | Widget layout, selected period |
| Positions | Position snapshot, symbol constraints | Prepare/confirm permitted modification or close | Sort, filters, selected row |
| Pending orders | Order snapshot | Prepare/confirm modify/cancel | Sort, filters |
| History | Cached deals/reconstructed trades, coverage | Filter/export selection | Date/filter/pagination |
| EAs | EA identity, analytics, evidence | Edit custom metadata, filter/group | Selected instance/group |
| Analytics | Canonical metric DTOs | Period/filter selection | Chart mode, comparison selection |
| Reports | Job progress/results | Create/cancel export job | Report section selections |
| Notifications | Alert/notification history | Acknowledge/clear where supported | Filter/read state |
| Settings | Preferences and connection metadata | Save settings, backup/restore, cache clear | Form draft state |

Dashboard custom layouts use predefined size classes (small/medium/large), not arbitrary pixel resizing. Layout state is durable; trading data is not.

## 5. Dependency direction

Allowed dependency direction:

```text
Renderer -> Preload API -> Main IPC gateway -> Python protocol client
                                             -> Python protocol host
                                                  -> Application use cases
                                                       -> Domain + Ports
                                                            <- Infrastructure adapters
```

The domain layer depends on abstractions and value types only. Adapters depend inward on domain/ports. UI DTOs are not domain entities. MT5 vendor objects are mapped at the adapter boundary. Do not share mutable objects across processes.

## 6. Error ownership

- MT5 adapter: vendor errors, terminal state, broker response mapping.
- Application layer: use-case preconditions, orchestration, operation outcome.
- Domain: invariant/policy violations.
- Protocol host: malformed envelope, unsupported version, invalid payload.
- Main IPC: invalid renderer sender, locked app, forbidden channel, invalid request.
- Renderer: present safe actionable message and preserve data-quality status.

Every error crossing a boundary uses a stable code and safe message. Stack traces and raw vendor details remain in redacted local diagnostics only.

## 7. Test seam requirements

Each component must be replaceable in tests through an interface or fixture:
- MT5 adapter replaced by deterministic terminal/account/history/trade fixtures.
- Clock and timezone injected for daily boundaries, cooldowns and DST.
- Cache adapter replaced by in-memory test cache.
- Export adapter writes to temporary test destination.
- Process protocol tested with fake child process and malformed/late/out-of-order frames.
- UI features consume mocked typed preload contracts.

Trade tests must include netting/hedging, partial close, broker rejection, market closed, stop/freeze violation, risk block, timeout after submission, process crash and reconciliation. See [13 — Testing and acceptance](13-testing-and-acceptance.md).
