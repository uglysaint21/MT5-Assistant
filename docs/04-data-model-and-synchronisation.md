# 04 — Data model and synchronisation

## Persistence policy
Do not create a permanent trading-history database. Trading records and derived analytics may be held in memory and temporary cache with configurable retention and clear-cache controls. Persist only application settings/preferences, dashboard layouts/widget configurations, custom EA names/descriptions/categories, diagnostic logs (30 days), user-exported reports (until manually deleted) and user-created backups of settings/layouts/EA metadata.

Cache is account-scoped. On account switch, invalidate account-scoped snapshots and prevent one account's data appearing under another.

## Logical domain entities
- AccountSnapshot: login identifier, broker/server, demo/real, margin mode, currency, balance, equity, margin, free margin, margin level, leverage and capture time.
- SymbolInfo: broker symbol, description, asset class, digits, tick data, volume limits, trade mode, sessions and supported operations.
- Position: position identifier, symbol, direction, volume, open price/time, current price, SL/TP, profit, swap, magic and comment.
- Order: order identifier, symbol, type, volume, price, SL/TP, state, setup/expiry times and linked position where supplied.
- Deal: deal identifier, order identifier, position identifier, symbol, entry/exit type, volume, price, profit, commission, swap, fee, time, magic and comment.
- CashMovement: deposit, withdrawal, credit or other non-trading balance operation, classified separately.
- EAIdentity: instance key, display name, description, category, attribution method and confidence.
- DataQuality: current/stale/incomplete/unavailable, reason and last successful timestamp.

Use broker identifiers; do not assume order, deal and position IDs are interchangeable.

## Trade reconstruction
A position may comprise multiple deals, partial closes, additions and modifications. Reconstruct lifecycle by stable position identifier and broker semantics. Partial closes are components of the same lifecycle, not independent completed trades. Preserve raw deal facts in temporary cache so calculations can be recomputed.

For netting accounts, a symbol may represent an aggregate position with changing volume/direction. For hedging accounts, multiple positions on the same symbol can coexist. Never key positions only by symbol.

## Synchronisation
Initial sync: capture account identity/snapshot; retrieve available history; normalise and validate; deduplicate; reconstruct positions/trades; compute analytics; mark coverage and limitations.

Incremental sync: track last successful server timestamp and identifiers; re-fetch an overlap window to tolerate delayed/updated records; upsert by stable identifiers; recompute affected lifecycles; periodically reconcile totals/recent history against MT5. Retries must be idempotent.

## Data quality and time
Use broker/server time for trading-day/report boundaries. Store timestamps with explicit timezone/offset or preserve raw server timestamp plus documented interpretation. Mark records incomplete if history is truncated/unavailable/inconsistent. Metrics requiring unavailable equity/deal history are unavailable or estimated with a clear label, never fabricated.

## Cache retention
Architect recommendation: evaluate a rolling 30-day default, configurable and user-clearable. Validate against data size and privacy. Clear-cache action explains that history will be fetched again from MT5 and may take time.
