# 02 — System architecture (summary)

The detailed target architecture has been expanded into a coordinated set of architecture documents:

- [17 — Architecture overview](17-architecture-overview.md): architecture style, deployment topology, module boundaries, domain model, workflows, resilience, quality attributes and implementation sequence.
- [18 — Component design](18-component-design.md): component responsibilities, application use cases, dependency rules and test seams.
- [19 — Protocol and data contracts](19-protocol-and-data-contracts.md): JSON Lines envelopes, handshake, request lifecycle, DTOs, management-operation state machine and error taxonomy.
- [20 — Security, data lifecycle and operations](20-security-data-operations.md): threat model, Electron/process hardening, credential protection, retention, diagnostics, trade recovery and release security.
- [21 — Architecture decisions and validation register](21-architecture-decisions.md): confirmed constraints, recommendations and unresolved implementation decisions.

## Architecture at a glance

Electron main owns desktop lifecycle, secure IPC, the bundled Python child process, local settings, tray, notifications and update orchestration. The React/TypeScript renderer is presentation-only and communicates through a minimal typed preload API. Python owns MT5 integration, domain workflows, history synchronisation, the shared analytics engine, EA attribution, risk evaluation, alerts and report generation.

The two processes communicate through versioned JSON Lines over stdin/stdout. The installed MT5 terminal is accessed through the official MetaTrader5 Python package. Trading data remains in temporary account-scoped cache; durable application data is limited to settings, layouts, custom EA metadata, diagnostics, exports and user-created backups.

## Non-negotiable boundaries

- No new trade entry; only the documented position and pending-order management operations are permitted.
- Backend revalidates broker constraints and risk policy immediately before every management request.
- A timeout or process failure after submission is an unknown outcome; reconcile actual MT5 state before any further action.
- The renderer cannot access Node.js, filesystem APIs, MT5 or generic IPC.
- The Python service has no unauthenticated network listener; stdout is protocol-only.
- No permanent trading-history database, no automatic telemetry and no persisted MT5 trading password.
- Monitoring continues in the system tray; explicit exit stops it.

See document 17 as the canonical architecture description. This summary is retained for compatibility with the original documentation index.
