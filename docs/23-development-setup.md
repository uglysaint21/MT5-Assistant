# 23 — Development setup

## Prerequisites

- Node.js 22.12 or newer within the 22.x line (CI pins 22.23.4) and npm 10 or newer.
- Python 3.11 or newer (CI currently exercises Python 3.12).
- Git.
- Windows 10/11 x64 and an installed MetaTrader 5 terminal are required for later real-terminal integration work. The current protocol foundation tests do not require MT5.

## TypeScript workspace

From the repository root:

```bash
npm install
npm run typecheck
npm test
```

The direct desktop development dependencies are pinned in desktop/package.json: TypeScript 5.9.3, Vitest 5.1.0, Ajv 8.17.1, ajv-formats 3.0.1 and @types/node 22.19.0. A committed npm lockfile is still pending; until it is added, transitive dependency resolution is not fully reproducible.

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

The Python development extras include pytest and jsonschema. Their supported ranges are declared in python/pyproject.toml; a fully resolved Python lockfile is still pending.

## Process protocol

The protocol is JSON Lines over stdin/stdout. Each frame is one UTF-8 JSON object terminated by a newline. stdout is reserved for protocol frames; diagnostics belong on stderr or in redacted local logs.

Protocol major version 1 defines request, ready, success/error response and event envelopes in protocol/schema/. Both language test suites consume the same golden fixtures in protocol/fixtures/. Python enforces a 1 MiB frame bound, rejects duplicate JSON object keys, validates exact envelope fields and rejects duplicate active request IDs.

Do not add a network listener, arbitrary command execution, arbitrary filesystem paths or new-trade operations to the process protocol. See [19 — Protocol and data contracts](19-protocol-and-data-contracts.md), [24 — Security threat model](24-phase-0-security-threat-model.md) and protocol/capabilities.json.

## CI

GitHub Actions runs the TypeScript typecheck/tests and Python tests on pushes, pull requests and manual dispatch. CI configuration is not evidence of a passing run until the workflow has executed successfully on GitHub.
