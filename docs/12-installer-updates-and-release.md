# 12 — Installer, updates and release

## Platform and installer
Public 64-bit Windows MSI, targeting Windows 10 and 11 x64. Bundle compatible Python runtime and dependencies. Require separately installed MT5 desktop terminal. Include Start Menu and desktop shortcut options; offer launch-at-Windows-startup. Ask during uninstall whether to keep or delete application data.

## Packaging
Package Electron UI and Python service together. Verify architecture compatibility between Windows, Electron, bundled Python, MetaTrader5 package and installed terminal. Installer checks OS compatibility and reports missing/incompatible MT5 prerequisite clearly. End users should not need to install Python separately.

## Updates
Check automatically at startup and periodically while running. Notify when update available. Ask confirmation before installation. Verify signed update metadata/package and preserve settings, dashboard layouts and custom EA metadata. Never silently install.

## Release conventions
Use semantic versioning MAJOR.MINOR.PATCH. Publish stable public releases only. Release notes explain user-visible changes, fixes, migration and known limitations. Public source and binary release correspond to same tagged version/commit.

## Signing and distribution
Architect recommendation: sign MSI and update packages with a reputable code-signing certificate and timestamp signatures. Publish checksums and release notes. Review all third-party dependency licences and redistribution terms, especially MetaTrader5 package and bundled runtime.

## Uninstall and data
Ask whether to retain or delete app data. Describe settings, layouts, EA metadata, cache, logs and reports. Do not delete user-exported reports without explicit consent. Define reset/uninstall paths and test them.

## Licence recommendation
Architect recommendation: evaluate Apache License 2.0 for public source because it is permissive and includes an express patent grant. MIT is a simpler alternative. Confirm ownership, contribution policy, dependency licences and redistribution restrictions before choosing. The user has not approved a specific licence.
