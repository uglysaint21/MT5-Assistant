# 09 — Security and privacy

## Principles
Protect local account information, prevent renderer compromise from becoming arbitrary system access, avoid credential persistence and make all trade-management actions explicit. Local-first; no cloud account required.

## Electron hardening
- contextIsolation enabled.
- nodeIntegration disabled.
- Renderer sandbox enabled where compatible.
- Minimal preload API; never expose raw ipcRenderer, Node APIs or generic filesystem access.
- Strictly validate IPC channel names and payload schemas.
- Restrictive Content Security Policy; disallow untrusted remote scripts.
- Deny unexpected navigation, window creation and remote content.
- Keep dependencies updated and audit releases.

## Python process boundary
Main owns child process and validates every request. Python validates every incoming message independently. Use local stdin/stdout only; no unauthenticated network listener. Stdout carries protocol only; stderr carries diagnostics. Bound message size, timeouts and restart loops. Never pass arbitrary code or unrestricted paths. Avoid secrets in command-line arguments, environment dumps and logs.

## Application password
Require app password on first launch and every later launch. Store only a strong password verifier, never plaintext or reversible password. Architect recommendation: Argon2id with per-install random salt and calibrated work factor using a maintained library and versioned parameters. DPAPI protects data at rest; it is not password hashing. Lock temporarily after five incorrect attempts; lockout state should survive process restart. Configurable inactivity timeout and password prompt after minimising. No Windows Hello and no recovery mechanism.

Forgotten-password reset is a documented local application-data reset with explicit warning that saved settings, layouts, EA metadata and other local data may be lost. Exact reset boundary must be designed and tested.

## DPAPI and MT5 credentials
Use Windows DPAPI to protect sensitive local application data where appropriate. Never persist the MT5 trading password. Manual login password exists in memory only for authentication and should be cleared as soon as practical.

## Local data and diagnostics
Persistent data: settings, layouts, custom EA metadata, diagnostic logs and exported reports. Trading data is temporary cache. Diagnostic logs retained 30 days. Redact account identifiers where not required; never log passwords, tokens or secret payloads.

No automatic telemetry. Sharing diagnostics requires explicit user permission and preview of what will be shared. Explain that nothing is transmitted automatically.

## Backup and restore
User-initiated backup/restore for settings, dashboard layouts and EA metadata. Backups must not contain MT5 passwords or trading history. Protect backup files and validate before restore. Warn before overwriting existing settings.

## Updates and supply chain
Verify update metadata and package signatures; use code signing for public Windows distribution. Pin/audit dependencies. Never auto-install updates without user confirmation.
