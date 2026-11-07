# 19 — Process protocol and data contracts

## 1. Transport

Use newline-delimited JSON (JSON Lines) over the Python child process's stdin/stdout streams.

- Electron main is the sole process supervisor and protocol client.
- Python is the sole protocol server.
- One complete UTF-8 JSON object per line.
- stdout is protocol-only; all diagnostics go to stderr or redacted rotating local logs.
- No localhost TCP/HTTP server, WebSocket listener or cloud endpoint.
- Set maximum frame size, queue bounds, request deadlines and output backpressure.
- Reject malformed JSON, duplicate/unknown envelope fields where strict validation is enabled, unsupported protocol versions and invalid payloads.
- Never pass arbitrary Python commands or untrusted filesystem paths.

## 2. Envelope model

The following are illustrative contract shapes. Exact field names and schema tooling are implementation decisions; maintain compatibility through explicit protocol versioning.

### Request

```json
{
  "kind": "request",
  "protocolVersion": 1,
  "requestId": "uuid",
  "operation": "account.getSnapshot",
  "payload": {}
}
```

### Successful response

```json
{
  "kind": "response",
  "protocolVersion": 1,
  "requestId": "uuid",
  "ok": true,
  "result": {}
}
```

### Error response

```json
{
  "kind": "response",
  "protocolVersion": 1,
  "requestId": "uuid",
  "ok": false,
  "error": {
    "code": "MT5_TERMINAL_DISCONNECTED",
    "message": "The MetaTrader 5 terminal is disconnected.",
    "retryable": true,
    "details": {}
  }
}
```

### Unsolicited event

```json
{
  "kind": "event",
  "protocolVersion": 1,
  "eventId": "uuid",
  "event": "sync.progress",
  "occurredAt": "2026-11-07T18:00:00Z",
  "payload": {}
}
```

Use UTC ISO-8601 timestamps for transport metadata; trading timestamps preserve broker/server interpretation separately. Do not use transport time as a substitute for broker time.

## 3. Handshake and capabilities

Python sends a ready message only after validating configuration and loading required modules:

```json
{
  "kind": "ready",
  "protocolVersion": 1,
  "serviceVersion": "0.1.0",
  "capabilities": [
    "account.read",
    "history.sync",
    "analytics.read",
    "trade.modifyPosition",
    "trade.closePosition",
    "trade.closeAllPositions",
    "trade.modifyPendingOrder",
    "trade.cancelPendingOrder",
    "reports.export"
  ]
}
```

Capabilities are descriptive and do not replace backend authorization. Optional MQL5 heartbeat is advertised only when its adapter is available. Main must fail closed on incompatible major protocol versions. Minor additions must be backward-compatible; breaking envelope/semantic changes increment the protocol major version.

## 4. Request lifecycle and concurrency

- Every request has a unique request ID and a bounded deadline.
- Main tracks pending requests and resolves only the matching response.
- Responses may arrive out of order; correlation is by request ID.
- Duplicate request IDs within an active session are rejected.
- A timed-out read may be retried only when the use case is idempotent and policy permits.
- A timed-out management request transitions to UNKNOWN and triggers reconciliation; never resubmit automatically.
- Cancellation is a separate request referencing a cancellable job ID. It does not imply that an already submitted broker operation can be undone.
- Events are best-effort progress/state notifications; authoritative state can be re-read after reconnect.
- Apply bounded concurrency. Serialize MT5 commands where required by package/thread-safety validation.

## 5. Core DTO contracts

### Data quality

```json
{
  "state": "CURRENT",
  "reason": null,
  "observedAt": "2026-11-07T18:00:00Z",
  "lastSuccessfulAt": "2026-11-07T18:00:00Z",
  "coverage": "COMPLETE"
}
```

Allowed state values: CURRENT, STALE, INCOMPLETE, UNAVAILABLE. Coverage may be COMPLETE, PARTIAL, UNKNOWN. Missing values remain null/omitted with an explicit reason; do not substitute zero.

### Account snapshot

Includes account identity (minimised/redacted where appropriate), broker/server, demo/real, netting/hedging, account currency, balance, equity, margin, free margin, margin level, leverage and capture time. Monetary values use decimal-safe representations or integer minor units where currency semantics permit; never use binary floating point as the canonical accounting representation.

### Position and order

Include account/session context, broker identifier, exact broker symbol, side/type, volume, prices, SL/TP, broker timestamps, current status, costs/PnL where supplied, magic/comment where relevant, and data quality. Position identity is not the symbol. Preserve broker precision and volume step.

### Analytics result

Every metric result includes:
- Value and unit/currency.
- Period start/end and time basis (broker/server or configured risk timezone).
- Calculation method/version where applicable.
- Source coverage and quality state.
- Whether the value is exact, estimated or unavailable.
- Explanation for estimates or missing data.

### Management operation

Suggested state machine:

```text
DRAFT -> PREPARED -> AWAITING_CONFIRMATION -> SUBMITTED
  |          |                 |                |
  v          v                 v                v
REJECTED   EXPIRED          CANCELLED       ACCEPTED / REJECTED /
                                             PARTIAL / UNKNOWN
                                                  |
                                                  v
                                             RECONCILING
                                                  |
                                                  v
                                      RESOLVED / STILL_UNKNOWN
```

Operation record includes local UUID, account session generation, target broker IDs, action, requested parameters, prepared snapshot/version, expiry, confirmation evidence, submission timestamp, broker response and reconciled outcome. Confirmation is bound to the prepared operation; if target state or critical constraints change, invalidate and prepare again.

Allowed action enum only:
- MODIFY_POSITION
- PARTIAL_CLOSE_POSITION
- CLOSE_POSITION
- CLOSE_ALL_POSITIONS
- MODIFY_PENDING_ORDER
- CANCEL_PENDING_ORDER

There is intentionally no open-order/open-position action enum.

## 6. Error taxonomy

Define stable codes at minimum:
- TERMINAL_NOT_FOUND
- TERMINAL_INITIALIZATION_FAILED
- TERMINAL_DISCONNECTED
- ACCOUNT_UNAUTHORISED
- ACCOUNT_MISMATCH
- HISTORY_UNAVAILABLE
- SYMBOL_UNAVAILABLE
- MARKET_CLOSED
- BROKER_CONSTRAINT_VIOLATION
- UNSUPPORTED_OPERATION
- REQUEST_REJECTED
- REQUEST_TIMEOUT_UNKNOWN
- PROTOCOL_VERSION_UNSUPPORTED
- PROTOCOL_INVALID_MESSAGE
- SERVICE_START_FAILED
- SERVICE_CRASHED
- DATA_STALE
- DATA_INCOMPLETE
- RISK_LIMIT_REACHED
- APP_LOCKED
- EXPORT_FAILED
- OPERATION_RECONCILIATION_REQUIRED

Each code has safe user message, retryability, recovery guidance and redaction policy. Do not return secrets, raw stack traces or unfiltered vendor messages.

## 7. Schema governance

- Keep protocol schemas and representative fixtures under version control.
- Validate on both sides independently.
- Add contract tests for every operation and event.
- Include malformed, oversized, missing-field, wrong-type, unsupported-version and unknown-enum cases.
- Add compatibility tests for supported desktop/service version pairs.
- Generate TypeScript/Python types from a single schema only if the selected toolchain is stable and maintainable; otherwise maintain equivalent definitions and cross-language golden fixtures.
- Treat protocol changes as compatibility changes, not ordinary refactors.
