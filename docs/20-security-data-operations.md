# 20 — Security, data lifecycle and operational design

This document turns the product's privacy and safety requirements into concrete boundaries and operational rules. See also [09 — Security and privacy](09-security-and-privacy.md), [04 — Data model and synchronisation](04-data-model-and-synchronisation.md) and [07 — Trade management and risk](07-trade-management-and-risk.md).

## 1. Threat model

Protect against:
- A compromised renderer attempting filesystem, process, credential or trade access.
- Malformed or malicious IPC/protocol payloads.
- Accidental credential leakage through logs, command-line arguments, crash dumps or diagnostics.
- Wrong-account data appearing after account switching or delayed asynchronous responses.
- Duplicate or stale history records corrupting financial calculations.
- Stale broker metadata causing unsafe management requests.
- Process/terminal failure after a broker operation was submitted.
- Malicious or tampered update packages and dependency supply-chain compromise.
- Unintended diagnostic or report disclosure.

The application is local-first and does not require a cloud account. This does not eliminate local malware, OS compromise, broker/terminal compromise or user-selected export disclosure.

## 2. Electron security boundary

- Enable context isolation.
- Disable node integration in renderer.
- Enable renderer sandbox where compatible.
- Expose only named, typed preload methods through contextBridge.
- Do not expose ipcRenderer, generic invoke/send, Node APIs or arbitrary filesystem access.
- Validate IPC sender origin/window and every payload at main.
- Apply strict Content Security Policy; no untrusted remote scripts.
- Deny unexpected navigation, popups and remote content.
- Restrict file dialogs and paths to main-owned user-approved workflows.
- Do not treat renderer-side validation as security enforcement.
- Keep Electron and dependencies patched; audit dependencies for releases.

## 3. Python process boundary

- Spawn a bundled, known executable with controlled arguments and environment.
- Never pass MT5 password through command-line arguments or environment variables.
- Use local stdin/stdout only; do not open unauthenticated network listeners.
- Bound message size, request timeouts, pending queue and restart loops.
- Validate every message independently in Python.
- stdout is protocol-only; stderr diagnostics are redacted.
- On unexpected exit, invalidate service-session state, mark data stale and apply bounded restart.
- After restart, reconnect and reconcile before re-enabling management.

## 4. Application password and local protection

The application password is an application unlock gate, not an MT5 credential. Persist only a strong password verifier; never plaintext or a reversible password. The current architecture recommendation is Argon2id with a per-install random salt, calibrated work factor, maintained library and versioned parameters. This is a recommendation requiring dependency and performance validation.

Five incorrect attempts trigger a temporary lock whose state survives process restart. Require password on every launch, after minimising/reopening and after configurable inactivity. No Windows Hello and no password recovery flow.

DPAPI protects selected local data at rest; it is not a password hashing algorithm. Define the exact protected data set and migration behaviour. The MT5 trading password exists in memory only for authentication and should be cleared as soon as practical. Never persist it, include it in diagnostics or retain it in crash reports.

Forgotten application password recovery is a documented local application-data reset with an explicit warning that settings, layouts, custom EA metadata and other local state may be lost. Exact reset boundary, confirmation flow and backup implications remain an open design item.

## 5. Data classification and retention

| Data | Classification | Persistence | Retention / deletion |
|---|---|---|---|
| MT5 trading password | Secret | Memory only | Clear as soon as practical |
| App password verifier | Sensitive | Local protected app data | Until reset/uninstall policy |
| Settings/preferences | Private | Durable local | User-controlled |
| Dashboard layouts | Private | Durable local | User-controlled |
| Custom EA metadata | Private | Durable local | User-controlled |
| Trading history/deals/derived analytics | Financial sensitive | Temporary account-scoped cache | Configurable retention; clear-cache |
| Diagnostic logs | Potentially sensitive | Local rotating logs | 30 days |
| Trade-management audit | Financial sensitive | Local app data; retention policy to define | Must never include credentials |
| Exported reports | Financial sensitive | User-selected folder | Until manually deleted |
| Backup archive | Private/sensitive | User-selected destination | User-controlled; must exclude history/passwords |

Do not create a permanent trading-history database. Cache format is undecided; whichever format is chosen must support account isolation, retention, clear-cache, atomic writes where applicable and idempotent updates. A rolling 30-day default is a recommendation, not an approved requirement.

Account switch must invalidate active in-memory data and prevent late old-session responses from rendering. Tag each request/result/cache namespace with an account session generation. Persistent custom EA metadata must not accidentally bind to the wrong broker account; define identity scope explicitly.

## 6. Logging and diagnostics

Use structured local logs with severity, timestamp, component, correlation/request ID, safe error code and redacted context. Do not log passwords, tokens, full secret payloads or unrestricted account identifiers. Retain diagnostics for 30 days.

No automatic telemetry or background upload. A user-initiated diagnostic share must:
1. Build a bounded diagnostic bundle.
2. Redact sensitive values.
3. Show a preview and destination/recipient.
4. Require explicit consent.
5. Record the user's choice locally without transmitting automatically.

## 7. Backup, restore and reset

Backups include only settings, dashboard layouts and custom EA metadata. Exclude trading history, cache, MT5 credentials and diagnostic secrets. Validate archive structure, schema version and size before restore. Warn before overwrite and preserve a recoverable pre-restore copy where practical. Whether archives are encrypted is open; do not claim encryption until implemented and tested.

Reset/uninstall UX must separately explain:
- settings and preferences;
- dashboard layouts;
- custom EA metadata;
- temporary trading cache;
- diagnostic logs;
- exported reports (never delete without explicit consent);
- user-created backup files (outside app control unless explicitly selected).

## 8. Trade safety and recovery

Risk evaluation and broker validation happen in Python immediately before submission. Main and renderer may prevent accidental UI use but are not authoritative.

Every operation:
- Is one of the six permitted management actions.
- Targets broker IDs, not only symbol names.
- Uses current broker/session/volume/price/stops/freeze/filling metadata.
- Checks app maximum lot, risk state and account state.
- Requires explicit confirmation of account, target, action and parameters.
- Has a local unique operation ID and audit record.
- Reports accepted/rejected/partial/unknown and reconciled state separately.

Close-all attempts all open positions, reports each result and does not cancel pending orders. It cannot guarantee execution. The recommended policy is to keep emergency close-all separately available when ordinary management is blocked, but still subject to explicit confirmation and broker/market constraints; confirm this policy before implementation.

Unknown outcomes after timeout, disconnect or crash must transition to reconciliation. Never retry blindly. A restarted service must retrieve actual positions/orders/deals and compare them with the intended operation before presenting a resolved status.

## 9. Updates and software supply chain

- Pin dependency versions and commit lockfiles.
- Review dependency licences and redistribution terms, especially the MetaTrader5 Python package and bundled Python runtime.
- Build reproducibly where feasible and associate release artifacts with a tagged source commit.
- Sign MSI and update packages; verify signed metadata and package signatures before installation.
- Check for updates at startup and periodically, but require user confirmation before installation.
- Preserve settings/layouts/EA metadata during upgrades.
- Publish checksums, release notes and stable semantic versions.
- Never silently install updates.
- Test install, upgrade, repair, rollback/recovery and uninstall on clean Windows 10/11 x64.

Signing certificate, timestamping provider, update distribution channel and installer/updater technology remain open choices.

## 10. Operational observability and health

Expose local health states for:
- Electron main lifecycle.
- Python process and protocol handshake.
- MT5 terminal/session.
- Account snapshot freshness.
- Position/order freshness.
- History coverage and last sync.
- EA evidence freshness.
- Active report/sync jobs.
- Last successful reconciliation.

Do not collapse all health into one green “connected” state. A running Python process does not prove MT5 connectivity; a connected terminal does not prove history completeness; recent trades do not prove EA runtime.

## 11. Shutdown and recovery

On minimise, keep monitoring and tray notifications active, but lock the app according to the configured security policy. On explicit exit, stop scheduling and alert evaluation, cancel safe background work, flush allowed durable data and gracefully terminate Python. Do not silently convert minimise into exit.

On backend crash:
1. Mark all backend-derived data stale.
2. Disable management actions.
3. Preserve operation IDs and any unknown management outcomes.
4. Restart under a bounded policy.
5. Handshake and reconnect.
6. Reconcile account state and uncertain operations.
7. Restore controls only when current state and policy permit.

## 12. Security acceptance checklist

- Renderer cannot access Node/filesystem/process APIs.
- IPC rejects invalid sender, malformed payload and forbidden operations.
- Process protocol rejects malformed/oversized messages and unsupported major versions.
- MT5 password is absent from durable storage, logs, args and diagnostics.
- App-password lockout survives restart and behaves as specified.
- DPAPI failure is handled without insecure fallback.
- No automatic network telemetry occurs.
- Diagnostics are previewed and shared only with explicit consent.
- Cache is account-scoped and clearable.
- Account switching rejects late old-session responses.
- No new-order API is exposed by UI, IPC or Python trade gateway.
- Unknown trade outcome is reconciled, never blindly retried.
- Update signatures are verified before install.
