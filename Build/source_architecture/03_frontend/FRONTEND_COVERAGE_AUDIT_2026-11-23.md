# Frontend Coverage Audit — Current Archive Snapshot (2026-11-23)

> Current direct counts for the supplied archive. These counts are not directly comparable to historical 286/287/288 path inventories because those inventories used a different extension/scope rule.

- Files under `frontend_vue/`: **358**.
- Vue SFC files (`*.vue`) under `frontend_vue/`: **142**.
- Route declarations matched in `src/router/index.js`: **44**.
- Frontend router source: `frontend_vue/src/router/index.js`.

## Route inventory

| Path | Route name |
|---|---|
| `/` | `home` |
| `/About` | `About` |
| `/login` | `login` |
| `/auth-callback` | `AuthCallback` |
| `/profile/:id` | `profile` |
| `/knowledge` | `knowledge` |
| `/learning` | `learning` |
| `/learning/topics/:topicId` | `learning-topic` |
| `/goals` | `goals` |
| `/tasks/today` | `today-tasks` |
| `/progress` | `progress` |
| `/jobs` | `jobs` |
| `/scraper` | `scraper` |
| `/tasks` | `tasks` |
| `/codex` | `codex` |
| `/projects` | `projects` |
| `/challenges` | `challenges` |
| `/finance` | `finance` |
| `/agents` | `agents` |
| `/ai-tools` | `ai-tools-laboratory` |
| `/analytics` | `analytics` |
| `/architecture` | `architecture` |
| `/crm` | `crm` |
| `/marketing` | `marketing` |
| `/revenue` | `revenue` |
| `/sales` | `sales` |
| `/memory` | `memory` |
| `/ai/agents` | `ai-agents` |
| `/social` | `social` |
| `/notifications` | `notifications` |
| `/system/frontend` | `frontend-enhancements` |
| `/settings` | `settings` |
| `/ai` | `ai-chat` |
| `/ai/control` | `ai-control` |
| `/ai/operations` | `ai-operations` |
| `/dashboard` | `dashboard` |
| `/automation` | `automation` |
| `/automation_Dashboard` | `automation_Dashboard` |
| `/automation_ProgramList` | `automation_ProgramList` |
| `/automation_programs_create` | `automation_programs_create` |
| `/automation/:id` | `automation_programs_edit` |
| `/automation_TaskCreate` | `automation_TaskCreate` |
| `/automation_TaskEditor` | `automation_TaskEditor` |
| `/:catchAll(.*)` | `NotFound` |

## Interpretation and gaps

- Route declarations do not prove component rendering, route reachability, auth behavior, or API success.
- Vue SFC count is not a complete frontend source count; JS/TS/CSS/SCSS/assets are separate.
- Historical 18-domain guide coverage remains useful for navigation but is not equivalent to one-to-one route count.
- Full route → view → component → store/service → backend operation mapping remains incomplete.
- No npm tests, lint, production build, or browser workflow was run.