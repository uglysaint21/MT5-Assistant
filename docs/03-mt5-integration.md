# 03 — MT5 integration

## Integration model
Use the official MetaTrader5 Python package to communicate with an installed MetaTrader 5 desktop terminal on Windows. It is not a generic remote broker API. The terminal is a required dependency and must be usable for the Python integration to initialise and access account state. Verify bundled Python runtime, package version, terminal build and 64-bit compatibility.

## Terminal discovery
- Detect candidate installations using supported Windows locations and registry/shortcut evidence where available.
- Validate each candidate by executable existence, launchability and successful package initialisation.
- Remember selected executable path; allow manual browsing.
- A discovered path alone is not a successful connection.
- Optionally launch the selected terminal when it is not running.
- Explain missing terminal, incompatible build, permission issue, terminal busy and failed initialisation.

## Authentication
Prefer the terminal's already authenticated session. Manual login accepts account number, broker/server and trading password. Password may exist in memory only for authentication; never persist or log it. Remember account number, broker/server and terminal location. Validate account identity after connection and show demo/real status. Only one account is active; account switching clears account-scoped live cache before connecting to the next account.

## Account and instrument compatibility
Support netting and hedging, demo and real, and forex, metals, indices, shares, cryptocurrencies, energy and broker-supported futures/other instruments. Discover all symbols exposed by the terminal and preserve broker names exactly, including prefixes/suffixes. A discovered symbol is not necessarily visible in Market Watch, tradable now or supported for every operation.

## Broker constraints
Before management requests, query/refresh relevant metadata:
- trade mode and current trading session;
- minimum, maximum and step volume;
- permitted filling/order modes;
- tick size, tick value and digits/precision;
- stops and freeze levels;
- allowed position/order operations;
- margin/account constraints where exposed.

Validate locally, then treat MT5/server response as final authority. Explain unsupported operations and continue in read-only mode where possible.

## Market availability
Disable management controls when market/session status is closed or broker indicates trading is unavailable. Monitoring remains active. Python independently re-checks status immediately before sending because conditions can change.

## Refresh and synchronisation
Refresh account snapshot, positions and pending orders every five seconds. Initial connection retrieves all history available. Later history updates are incremental with overlap/reconciliation windows. Never download all history every five seconds. Display last successful update and stale-data state. Reconcile snapshots against MT5-provided values.

## Error taxonomy
Provide stable codes for terminal not found, initialization failed, terminal disconnected, account unauthorised, account mismatch, history unavailable, symbol unavailable, market closed, broker constraint violation, unsupported operation, request rejected, timeout/unknown outcome and package/terminal incompatibility. Messages must be actionable and must not expose secrets or raw traces.
