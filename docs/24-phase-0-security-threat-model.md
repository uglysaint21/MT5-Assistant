# 24 — Phase 0 security threat model and verification plan

**Status:** Initial threat model and verification plan. This is an engineering baseline, not a claim that the listed controls have already been implemented.

This document operationalises the trust boundaries in [17 — Architecture overview](17-architecture-overview.md), component ownership in [18 — Component design](18-component-design.md), and security/data rules in [20 — Security, data lifecycle and operations](20-security-data-operations.md).

## 1. Security objectives

1. Protect MT5 credentials and application unlock material from disclosure.
2. Prevent a compromised renderer from reaching operating-system, filesystem, process or trading capabilities outside its narrow API.
3. Prevent malformed or replayed local protocol messages from corrupting state or causing unsafe operations.
4. Keep account-scoped financial data isolated across disconnects and account switches.
5. Ensure no new trade-entry capability exists in UI, IPC, protocol, or Python gateway.
6. Make uncertain broker-operation outcomes explicit and reconcile them before further action.
7. Keep private financial information local unless the user explicitly exports or shares it.

## 2. Assets and security boundaries

| Asset | Sensitivity | Primary owner | Required protection |
|---|---|---|---|
| MT5 trading password | Secret | Transient Python authentication flow | Memory-only; never args, env, disk, logs or diagnostics |
| App-password verifier and lockout state | Sensitive | Main/security adapter | Strong password hash, DPAPI-protected state where specified, persistent lockout |
| Active account identity and financial snapshots | Financial sensitive | Python account/session services | Session-generation scoping, redacted logs, no cross-account cache leakage |
| Trading history and analytics cache | Financial sensitive | Python cache adapter | Temporary retention, account namespace, clear-cache |
| Management operation intent/outcome | Financial sensitive | Python management service | Confirmation binding, operation ID, reconciliation, safe audit |
| Local exports and backups | User-controlled private data | Explicit export/backup workflow | Main-selected destination, overwrite confirmation, no silent sharing |
| Update packages and dependencies | Integrity-critical | Release/update pipeline | Dependency review, signed artifacts, signature verification |

Trust boundaries:
- Renderer → preload → Electron main: untrusted renderer input crosses into privileged desktop code.
- Electron main ↔ Python child process: local process boundary; both sides independently validate strict protocol envelopes.
- Python adapter ↔ installed MT5 terminal: vendor/API boundary; broker responses and vendor errors are untrusted inputs.
- Application ↔ filesystem/OS: main-owned, allow-listed operations only.
- Application ↔ user-selected exports/diagnostics: explicit consent and disclosure boundary.

## 3. Threat register

| ID | Threat / abuse case | Impact | Required mitigation | Verification evidence |
|---|---|---|---|---|
| THR-01 | Renderer invokes arbitrary IPC or accesses Node APIs | Local data/credential compromise; unsafe actions | Context isolation, sandbox, no Node integration, named preload API, sender and payload validation | Electron security integration tests; IPC negative tests |
| THR-02 | Malformed, oversized, duplicate-key or unknown-field protocol frame | Crash, confused state, validation bypass | 1 MiB frame bound, duplicate JSON-key rejection, strict envelope schema, stable errors | Python protocol tests; TS Ajv schema tests; fuzz/property tests later |
| THR-03 | Duplicate in-flight request ID correlates a response to the wrong caller | Cross-request data confusion | Bounded active-ID registry; reject duplicates; release only on completion/cancellation/timeout | ActiveRequestIds unit tests; out-of-order response integration tests |
| THR-04 | MT5 password leaks via process args, env, logs or diagnostics | Account compromise | Transient authentication payload; secret redaction; no credential persistence | Secret sentinel scan; process-argument/env assertions; log/diagnostic tests |
| THR-05 | Late response from prior account arrives after account switch | Financial data from wrong account displayed | Session generation on requests/results; invalidate old cache and pending work | Account-switch race integration test |
| THR-06 | Stale broker constraints used for management | Rejected or unsafe trade modification | Backend re-read and revalidation immediately before submission | Broker-constraint mutation tests |
| THR-07 | Management request times out after broker submission | Duplicate action if blindly retried | UNKNOWN state and mandatory reconciliation; no automatic resend | Timeout/crash fault-injection tests |
| THR-08 | New-order operation accidentally becomes reachable | Unintended exposure / violates product scope | Explicit six-action allow-list; no open-order action enum or capability | Static/API contract tests; negative UI/IPC/backend tests |
| THR-09 | Diagnostic or report contains secrets/account identifiers | Privacy breach | Redaction, bounded bundle, preview, explicit user consent | Redaction fixtures and diagnostic export review |
| THR-10 | Tampered update or dependency supply-chain compromise | Arbitrary code execution | Pinned dependencies, licence/security review, signed MSI/update and signature verification | Release pipeline signature tests and dependency audit |
| THR-11 | Python service crash leaves stale data/actions enabled | Unsafe decisions based on old state | Mark data stale, disable management, bounded restart, reconnect and reconcile | Process-crash and stale-state integration tests |
| THR-12 | Cache or history namespace leaks across accounts | Financial privacy and calculation corruption | Account-scoped namespace and session generation; cache clear/retention | Multi-account fixture isolation tests |

## 4. Current Phase 0 evidence

Implemented in this branch:
- Protocol-v1 request, ready, response and event JSON Schemas.
- Strict Python envelope validation, duplicate-key rejection, frame-size bound and bounded active request-ID registry.
- TypeScript runtime envelope guards and Ajv schema validation tests.
- Shared protocol golden fixtures consumed by both language test suites.
- Synthetic netting/hedging account and history fixture using decimal strings.
- Stable protocol error-code catalogue and capability registry.
- CI jobs for TypeScript and Python checks.

Not yet implemented or verified:
- Electron BrowserWindow/preload hardening and privileged IPC gateway.
- Credential-handling, DPAPI, app-password and secret-redaction code.
- Account-session generation and cache isolation.
- Trade-management state machine and broker reconciliation.
- Signed installer/updater and supply-chain release checks.
- GitHub Actions result for the current branch and clean Windows 10/11 validation.

## 5. Security acceptance mapping

| Requirement | Planned test location / evidence |
|---|---|
| Renderer cannot access Node/filesystem/process APIs | `desktop/tests/security/electron-boundary.e2e.ts` (Phase 1) |
| IPC rejects invalid sender, malformed payload and forbidden operations | `desktop/tests/security/ipc-gateway.test.ts` (Phase 1) |
| Protocol rejects malformed, duplicate-key, oversized, unknown-field and unsupported-version frames | `python/tests/test_protocol_contracts.py`; `desktop/tests/protocol.test.ts`; `desktop/tests/schema.test.ts` |
| MT5 password absent from durable storage, args, env, logs and diagnostics | Python/main security integration tests (Phase 1) |
| App-password lockout survives restart | Security persistence integration tests (Phase 1) |
| DPAPI failure has no insecure fallback | Windows-specific security tests (Phase 1/6) |
| No automatic telemetry | Network-observation acceptance test (Phase 6) |
| Cache is account-scoped and clearable | Cache adapter integration tests (Phase 2) |
| Account switching rejects late old-session responses | Session-generation race tests (Phase 2) |
| No new-order API exposed | Capability/schema static checks and trade-gateway negative tests (Phase 5) |
| Unknown trade outcome reconciled, never blindly retried | Operation-state-machine fault-injection tests (Phase 5) |
| Update signatures verified before install | Windows updater integration tests (Phase 6) |

## 6. Risk acceptance and change control

No high-impact threat is considered accepted merely because a mitigation is documented. A mitigation becomes verified only when the corresponding code and repeatable test evidence exist.

Any change to credential handling, renderer privileges, IPC/protocol operations, account scope, persistence/retention, trade-management allow-list, operation retry policy or update verification requires:
1. Updating the relevant threat entry and architecture/requirements documents.
2. Adding or updating a negative test.
3. Reviewing privacy, safety and migration consequences.
4. Recording evidence in the implementation status/release checklist.

## 7. Open security decisions

- Exact app-password hashing library and calibrated Argon2id parameters remain subject to dependency and target-hardware validation.
- Exact DPAPI-protected data set and migration behavior remain open.
- Exact audit-log retention and user controls remain open.
- Backup archive encryption policy remains open.
- Installer/update signing certificate and distribution channel remain open.

These are tracked in [21 — Architecture decisions and validation register](21-architecture-decisions.md); this document does not silently approve them.
