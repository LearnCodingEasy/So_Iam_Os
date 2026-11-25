# UI/UX Upgrade — 2026-11-24

Incremental enhancement of the existing Vue 3 / PrimeVue frontend. No backend files, API contracts, routes, stores or models were changed.

## Design system (new)
| File | Role |
|---|---|
| `src/assets/scss/design-system/_design-system.scss` | `--ds-*` tokens (light/dark), glass/gradient/lift primitives, page header, stat tile, state blocks, shell polish, RTL-correct mobile drawer, `prefers-reduced-motion` |
| `src/composables/useMotion.js` | GSAP helpers: `revealChildren`, `useReveal`, `tweenNumber`, `prefersReducedMotion`. All tweens run in a `gsap.context` that is reverted on unmount; inline styles are cleared (`clearProps`); inputs are never animated; no-op under reduced motion |
| `src/components/ui/PageHeader.vue` | Gradient header with animated background and SVG illustration; `#actions` slot |
| `src/components/ui/StatTile.vue`, `AnimatedCounter.vue` | KPI tile with animated number (only real values; no invented trends) |
| `src/components/ui/StateBlock.vue` | Unified empty / error / loading state; action button only when a label is given |
| `src/components/ui/HeroIllustration.vue` | Original inline-SVG illustrations (goals, finance, learning, ai, tasks, jobs, projects, knowledge, empty, error, dashboard). No external images |

## Shell
- `AppLayout.vue`: `dir="rtl"`, route-change stagger entrance, mobile backdrop; fixes off-canvas sidebar sliding the wrong way in RTL.
- `Sidebar.vue` / `Topbar.vue`: Unicode glyphs replaced with PrimeIcons, active indicator, stagger-in. **All 40 nav items and routes are unchanged.**
- `index.html`: `lang="ar" dir="rtl"`, title `SO_IAM_OS`.

## Pre-existing defects found and fixed
1. **Goals page**: create / edit / details / milestone / AI-plan dialogs existed only inside a commented-out legacy template, so their buttons did nothing. Dialogs restored into the live template (logic untouched).
2. **Dashboard**: weekday task chart was fabricated (fixed multipliers, fallback `10`/`5`) → now a bar chart of the real `total / completed / pending` values. Fake week/month/year selector removed (no backend support). "Export report" only showed a toast → now a real client-side CSV download of the loaded KPIs. "Add item" modal showed a fake success toast for invented infra services → now creates a real task via `POST /tasks/` (`title`, `priority`) and reloads. Hard-coded user name fallback and `console.log` calls removed.
3. `StatCard.vue` no longer prints a hard-coded "from last month" trend.

## Pages upgraded
Goals, Dashboard, CRM, Marketing, Revenue, Analytics, Architecture (PageHeader + illustration), plus entrance animation on every routed page via `AppLayout`.

## Feature map (touched functionality)
| App | Function | Endpoint | Method | Vue | Status |
|---|---|---|---|---|---|
| tasks | Create task from dashboard | `/tasks/` | POST | `DashboardView.vue` | Wired; **not run** |
| core | Load dashboard | `/core/dashboard/` | GET | `DashboardView.vue` | Unchanged |
| goals | Create/edit/details/milestones/AI plan | existing `services/Goals/goals` | — | `Goals.vue` | Dialogs restored; **not run** |

## Verification performed / not performed
- Done: syntax parse of every changed `.vue`/`.js`/`.scss` file (Prettier parsers, debug mode), import-path resolution, Goals template ↔ script identifier check.
- **Not done** (no Django, no `node_modules`, network closed in the authoring environment): `npm run build`, `vitest`, ESLint, Django tests/checks, browser/visual checks, real animation timing, RTL visual check, PrimeIcons name availability (e.g. `pi-microchip-ai`). Run locally: `cd frontend_vue && npm install && npm run build && npm run lint && npm run test:unit`.

## Not done (scope)
Full redesign of the remaining ~20 app views, image optimisation pass, the Backend Integration feature-map for every app, Pinia/perf audits. The shell, the design system and entrance motion apply to all pages; per-page redesign was applied to the pages listed above.
