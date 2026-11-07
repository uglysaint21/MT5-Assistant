# 21 — Architecture decisions and validation register

This register separates documented user decisions from architectural recommendations and unresolved implementation choices. It is not permission to silently change product scope. Detailed requirement decisions remain in [16 — Decisions and open questions](16-decisions-and-open-questions.md).

## 1. Accepted product constraints (baseline)

| ID | Decision / constraint | Status | Source |
|---|---|---|---|
| BASE-01 | Windows 10/11 x64 desktop application, public MSI | Confirmed | 01, 12 |
| BASE-02 | Electron + React + TypeScript UI, bundled Python child process | Confirmed | README, 01, 02 |
| BASE-03 | Official MetaTrader5 Python package and installed MT5 terminal | Confirmed | 03 |
| BASE-04 | Versioned JSON Lines over stdin/stdout | Confirmed | 02 |
| BASE-05 | One active account; demo/real; netting/hedging | Confirmed | 01, 03 |
| BASE-06 | Five-second live refresh; initial full history then incremental sync | Confirmed | 01–04 |
| BASE-07 | Temporary trading cache only; no permanent history database | Confirmed | README, 04 |
| BASE-08 | Never persist MT5 trading password | Confirmed | 01, 03, 09 |
| BASE-09 | App password each launch, lock after five failures, inactivity/minimise lock, no recovery | Confirmed | 09, 16 |
| BASE-10 | DPAPI for sensitive local app data | Confirmed | 09, 16 |
| BASE-11 | Limited management only; no trade entry | Confirmed | 01, 07 |
| BASE-12 | On-demand PDF/XLSX/CSV reports | Confirmed | 11 |
| BASE-13 | No automatic telemetry; diagnostics only with consent | Confirmed | 09 |
| BASE-14 | Semantic versioning; stable public releases | Confirmed | 12, 16 |
| BASE-15 | Guided optional MQL5 component installation/configuration | Confirmed as optional capability | 06 |
| BASE-16 | Forgotten app password uses documented local-data reset with warning | Confirmed direction; exact boundary open | 09, 16 |
| BASE-17 | Application name is MT5 Assistant | Confirmed | README |
| BASE-18 | MIT licence file currently exists in repository | Repository fact; ownership/intent should be verified | LICENSE, repository metadata |

## 2. Architectural recommendations

| ID | Recommendation | Rationale | Validation / approval needed |
|---|---|---|---|
| ADR-ARCH-001 | Modular monolith across Electron and Python processes; ports/adapters inside Python | Appropriate for local single-user product; avoids premature distributed systems | Review boundaries after first vertical slice |
| ADR-ARCH-002 | Monorepo with desktop and Python service packages | Coordinated releases and contract fixtures | Validate CI/tooling ergonomics |
| ADR-ARCH-003 | Single MT5 command executor until concurrency safety is proven | Avoid races and uncertain package thread behaviour | Test exact package/terminal versions |
| ADR-ARCH-004 | Shared Python analytics engine | Prevent inconsistent dashboard/report calculations | Establish golden financial fixtures |
| ADR-ARCH-005 | Argon2id verifier for app password | Strong dedicated password hashing; DPAPI is not a hash | Select maintained library and calibrate on minimum target hardware |
| ADR-ARCH-006 | Rolling 30-day temporary-cache default | Useful balance of convenience and privacy | Measure data volume; make configurable and clearable |
| ADR-ARCH-007 | Separate freshness policies by data category | Account snapshots, history and EA evidence age differently | Define grace periods and test missed polls |
| ADR-ARCH-008 | Evidence/confidence-based EA runtime states | History alone cannot prove runtime | Validate optional heartbeat feasibility |
| ADR-ARCH-009 | Separate emergency close-all from ordinary management gate | Preserves emergency workflow while retaining safeguards | Confirm interaction with any future global trading-disable setting |
| ADR-ARCH-010 | TWR where supported, Modified Dietz fallback | Avoid misleading returns with external cash flows | Validate data availability and formula implementation |
| ADR-ARCH-011 | Discrete dashboard widget size classes | Reconciles fixed-size and resizable layout requirements | Validate UX prototypes |
| ADR-ARCH-012 | Signed MSI/update artifacts and explicit install consent | Supply-chain integrity and user control | Select certificate, timestamping and updater |
| ADR-ARCH-013 | MIT remains the current repository licence pending explicit review | A LICENSE file already exists; changing licence has legal/ownership implications | Verify contributor rights, dependency terms and project intent before any change |

## 3. Unresolved implementation decisions

| ID | Question | Decision owner / evidence needed | Blocking area |
|---|---|---|---|
| OPEN-01 | Supported Python version and MetaTrader5 package/terminal build matrix? | Compatibility spike on clean Win10/11 x64 and target terminals | Packaging, MT5 adapter |
| OPEN-02 | Electron version, builder/installer framework and MSI authoring? | Compare signing, repair/uninstall, auto-update, native deps | Packaging |
| OPEN-03 | Cache format and storage engine? | Prototype size, query, migration, atomicity and retention | Sync/cache |
| OPEN-04 | Default/min/max cache retention? | Privacy review and representative account history sizes | Data lifecycle |
| OPEN-05 | Stale-data grace thresholds by category? | Poll latency and outage simulations | Monitoring/UI |
| OPEN-06 | Numerical risk defaults, cooldowns and max lot? | Risk review; never infer universal safe values | Risk |
| OPEN-07 | Exact reset/deletion boundary for forgotten app password? | UX/security review; preserve user exports unless explicit consent | Security |
| OPEN-08 | Backup encryption and schema migration policy? | Threat model and recovery tests | Backup |
| OPEN-09 | MQL5 heartbeat local transport and authentication? | Prototype, terminal constraints, local attack surface | Optional EA |
| OPEN-10 | Update channel and signature verification design? | GitHub Releases or alternative, signing certificate and rollback strategy | Release |
| OPEN-11 | Support policy and issue reporting workflow? | Project owner decision | Operations |
| OPEN-12 | Final licence and third-party redistribution review? | Confirm ownership and review dependency licences/MetaTrader5 terms | Legal/release |
| OPEN-13 | Protocol schema tooling and cross-language type generation? | Compare JSON Schema/codegen versus maintained golden fixtures | Contracts |
| OPEN-14 | Trade audit retention and export/clear controls? | Privacy and dispute-resolution needs | Trade safety |

## 4. Decision record template

For every material decision, record:
- ID and short title.
- Status: proposed, accepted, superseded or rejected.
- Context and constraints.
- Decision and alternatives considered.
- Consequences, including security and migration implications.
- Validation evidence and follow-up owner.
- Affected requirements, interfaces, tests and docs.

Do not mark a recommendation accepted solely because it appears in this architecture document.

## 5. Change control

Any change to account scope, permitted trade operations, credential handling, persistence/retention, financial formulas, time semantics, risk gates or release acceptance criteria requires:
1. Updating the originating requirement/specification.
2. Updating this decision register and architecture/interface documents.
3. Updating requirements traceability.
4. Adding or updating automated acceptance/regression tests.
5. Reviewing security, data-integrity and migration consequences.
