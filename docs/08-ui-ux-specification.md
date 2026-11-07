# 08 — UI/UX specification

## Visual direction
Professional, restrained, modern desktop interface. System theme preference with coordinated dark/light themes. Dark reference with dark-brown accents and tasteful light-brown text accents. Subtle textured backgrounds, floating glass-style sidebar, rounded cards/panels, soft shadows, depth and subtle transitions. Modern rounded sans-serif typography and consistent icons. Profit/loss must not rely on colour alone.

## Navigation
Collapsible floating sidebar with icon and text labels:
- Dashboard
- Open positions and pending orders
- Trading history
- Expert Advisors
- Account analytics
- Reports
- Notifications
- Settings

Startup opens dashboard after successful setup/connection. Close-to-window action minimises to system tray and monitoring continues. Explicit exit stops monitoring.

## Dashboard
Widgets: balance/equity, margin/account health, today's PnL, open positions, pending orders, EA summary, portfolio allocation, recent activity, connection status and daily performance chart.

Users can add, remove, rearrange and resize widgets; layouts auto-save. Provide predefined and custom layouts, reset-to-default with confirmation. Reconcile earlier fixed-size preference with later resize request by using discrete widget size/grid-span presets (small/medium/large), not arbitrary pixel resizing.

Provide compact and spacious density modes. Clicking a chart/statistic/widget opens relevant detail.

## Tables and charts
Open positions columns: symbol, buy/sell, volume, entry/current price, SL/TP, floating PnL, swap/commission, open time and position ID.

History filters: date range, instrument, direction, profit/loss, EA and position/deal ID.

Charts: equity/balance curves, weekly/monthly/yearly performance, capital allocation, instrument exposure, profit/loss and win/loss distribution. Offer clean overview and interactive/advanced views.

## Formatting and accessibility
Account currency and broker precision by default; configurable date, number and currency formats. Keyboard navigation, readable text, sufficient contrast, tooltips and clear labels. Support Windows text scaling where practical. Balanced information density.

## Setup and security UX
Guided first-run wizard: detect terminal, manual selection if needed, launch terminal, authenticate, test connection/data retrieval, show diagnostics and open dashboard. Explain steps and common MT5 problems.

App password required first launch and every subsequent launch. Require password when reopening after minimising and after configurable inactivity. Lock temporarily after five incorrect attempts. No Windows Hello and no password recovery flow.
