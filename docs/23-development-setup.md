# 23 — Development setup

## Prerequisites

- Node.js 22.x and npm 10 or newer.
- Python 3.11 or newer.
- Git.
- Windows 10/11 x64 and an installed MetaTrader 5 terminal are required for later real-terminal integration work. The current protocol foundation tests do not require MT5.

## TypeScript workspace

From the repository root:

```bash
npm install
npm run typecheck
npm test
```

## Python service

From the repository root:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
python -m pip install -e "python[dev]"
pytest python/tests
```

## Process protocol

The protocol is JSON Lines over stdin/stdout. Each frame is one UTF-8 JSON object terminated by a newline. stdout is reserved for protocol frames; diagnostics belong on stderr or in redacted local logs. Protocol major version 1 is currently represented by the initial schema and framing helpers.

Do not add a network listener, arbitrary command execution, arbitrary filesystem paths or new-trade operations to the process protocol. See [19 — Protocol and data contracts](19-protocol-and-data-contracts.md).

## CI

GitHub Actions runs the TypeScript typecheck/tests and Python tests on pushes, pull requests and manual dispatch. CI configuration is not evidence of a passing run until the workflow has executed successfully on GitHub.
