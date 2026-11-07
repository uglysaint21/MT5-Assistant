# MT5 Assistant

A local-first Windows desktop dashboard for monitoring MetaTrader 5 accounts, trading activity, portfolio exposure, performance and Expert Advisors (EAs).

> **Project status: Planning / early development.** This repository is being established for the MT5 Assistant desktop application. Features and technical choices described below are planned and may change as the architecture is finalised. The application is not yet ready for production or live trading use.

## Vision

MT5 Assistant aims to provide a clear, professional view of a trader's MT5 account from one locally installed Windows application. The interface will use a dark, understated visual theme with warm brown accents, rounded typography, subtle glass-style navigation and restrained animations.

The application is intended for **monitoring and analysis**. It will not place, modify or close trades unless that capability is explicitly designed, implemented and documented in a future scope.

## Planned features

### Account dashboard
- Account balance, equity, free margin and used margin.
- Floating profit and loss (PnL) for open positions.
- Configurable realised and overall PnL views for day, week, month, year and all time.
- Account connection state and last successful data refresh.

### Trading activity
- Current open positions and their key details.
- Historical deals and orders, with date and instrument filters.
- Transaction-level information such as direction, volume, entry/exit prices, fees, swap and profit where supplied by MT5.
- Search, sorting and filtering for reviewing trading activity.

### Portfolio overview
- Portfolio allocation visualised with an interactive pie chart.
- Cash/balance and open-position exposure presented separately and clearly.
- Breakdown by instrument, with totals and percentages.
- Explicit handling of account currency and valuation limitations.

### Expert Advisor monitoring
- EA overview based on available MT5 trade and account data.
- EA identification using configurable Magic Numbers and other available metadata.
- Per-EA performance summaries, trade counts and PnL.
- Live / inactive status where it can be reliably determined.
- Historical performance views.

> EA runtime status may require additional instrumentation, terminal-side files, or an EA reporting component. MT5 account history alone cannot always prove that an EA is currently running. The implementation will distinguish confirmed status from inferred or unknown status.

### Local application security
- First-run password creation and password verification on later launches.
- Local password verification using a password hashing scheme designed for authentication; the password itself will not be stored in plaintext.
- Windows Data Protection API (DPAPI) for protecting locally stored secrets where appropriate.
- Local settings and data storage, with no cloud account required for normal operation.

## Proposed technology

The initial technical direction is:

| Area | Proposed technology |
| --- | --- |
| Desktop application | Python with PySide6 / Qt |
| MT5 connectivity | Official MetaTrader 5 Python integration |
| Data analysis | Pandas |
| Charts | PyQtGraph or another Qt-compatible charting library |
| Local persistence | SQLite |
| Windows secret protection | Windows DPAPI |
| Windows executable packaging | PyInstaller |
| Source control | Git and GitHub |

These are provisional choices and will be validated during planning. The MetaTrader 5 Python integration normally communicates with a locally installed and running MT5 terminal on Windows; it is not a generic remote REST API. The application will therefore need a compatible MT5 terminal installation and an authorised account session.

## Platform and prerequisites

**Target platform:** Windows desktop.

Expected runtime requirements once implemented:

- A supported Windows version.
- MetaTrader 5 desktop terminal installed.
- A supported Python runtime for development, or the packaged executable for end users.
- An MT5 account that the user is authorised to access.

Exact supported Windows, Python and MT5 terminal versions will be documented after compatibility testing.

## Security and privacy principles

- Account credentials and other secrets must never be committed to this repository.
- Secrets should be protected using Windows-native encryption where appropriate.
- Authentication passwords should be stored only as secure password hashes, not reversible plaintext.
- Local account data should remain on the user's machine by default.
- Logs must avoid recording passwords, account passwords, tokens or other sensitive values.
- The application should clearly communicate connection state and data freshness.

**Never submit your MT5 password, investor password, API credentials, recovery codes or other secrets in GitHub issues, commits, screenshots or chat messages.** Use the application's local settings interface once that functionality is available.

## Development roadmap

The project is expected to progress through these stages:

1. **Architecture and requirements** — confirm data definitions, MT5 integration approach, security model and application structure.
2. **UI/UX foundation** — implement the startup flow, authentication screens, navigation and visual design system.
3. **MT5 connectivity** — establish and test a read-only connection to the local MT5 terminal.
4. **Account and trading views** — implement account metrics, open positions, history and portfolio allocation.
5. **EA monitoring** — define EA identification and status reporting, then implement performance views.
6. **Hardening and testing** — validate calculations, error handling, local storage, security and reconnect behaviour.
7. **Windows packaging** — build, test and document the distributable Windows executable.

## Development status

This repository is currently in the planning stage. No production-ready functionality, trading connectivity, security guarantees or executable release should be assumed until implemented and tested.

## Contributing and project planning

The initial development is being coordinated in this repository. Architecture decisions, feature scope and implementation milestones will be documented as the project progresses.

Before contributing code, please open or review an issue describing the proposed change so that it can be aligned with the project architecture.

## Disclaimer

MT5 Assistant is an independent software project and is not affiliated with, endorsed by, or supported by MetaQuotes. MetaTrader 5 and related marks belong to their respective owners.

The application is intended as an account monitoring and analytical tool. Trading involves financial risk. Displayed metrics are informational and should be reconciled with the broker's official records before being used to make financial decisions.
