# Backend Application Knowledge Base

> Each app-like directory is listed once. The repository has 26 such directories; 25 are in `INSTALLED_APPS`. The existing 17-app guides remain in `Build/complete_project_documentation/backend/`; the nine additional app summaries remain in `Build/source_architecture/02_backend/applications/`. Do not create duplicate app docs without first checking these locations.

| App | Existing source documentation | URL mount |
|---|---|---|
| `agents` | `Build/source_architecture/02_backend/applications/agents.md` | /api/agents/ |
| `ai` | `Build/complete_project_documentation/backend/ai/` | /api/ai/ |
| `ai_tools_laboratory` | `Build/source_architecture/02_backend/applications/ai_tools_laboratory.md` | /api/ai-tools/ |
| `analytics` | `Build/source_architecture/02_backend/applications/analytics.md` | /api/analytics/ |
| `architecture` | `Build/source_architecture/02_backend/applications/architecture.md` | /api/architecture/ |
| `automation` | `Build/complete_project_documentation/backend/automation/` | /api/automation/ |
| `challenges` | `Build/complete_project_documentation/backend/challenges/` | /api/challenges/ |
| `codex` | `Build/complete_project_documentation/backend/codex/` | /api/codex/ |
| `core` | `Build/complete_project_documentation/backend/core/` | /api/core/ |
| `crm` | `Build/source_architecture/02_backend/applications/crm.md` | /api/crm/ |
| `goals` | `Build/complete_project_documentation/backend/goals/` | /api/goals/ |
| `jobs_opportunity` | `Build/complete_project_documentation/backend/jobs_opportunity/` | /api/jobs/ |
| `knowledge` | `Build/complete_project_documentation/backend/knowledge/` | /api/knowledge/ |
| `learning` | `Build/complete_project_documentation/backend/learning/` | /api/learning/ |
| `marketing` | `Build/source_architecture/02_backend/applications/marketing.md` | /api/marketing/ |
| `memory` | `Build/complete_project_documentation/backend/memory/` | /api/memory/ |
| `notification` | `Build/complete_project_documentation/backend/notification/` | /api/notifications/ |
| `personal_finance` | `Build/complete_project_documentation/backend/personal_finance/` | /api/finance/ |
| `projects` | `Build/complete_project_documentation/backend/projects/` | /api/projects/ |
| `revenue` | `Build/source_architecture/02_backend/applications/revenue.md` | /api/revenue/ |
| `sales` | `Build/source_architecture/02_backend/applications/sales.md` | /api/sales/ |
| `scraper` | `Build/complete_project_documentation/backend/scraper/` | /api/scraper/ |
| `skills` | `Build/source_architecture/02_backend/applications/skills.md` | — |
| `social` | `Build/complete_project_documentation/backend/social/` | /api/social/ |
| `tasks` | `Build/complete_project_documentation/backend/tasks/` | /api/tasks/ |
| `users_accounts` | `Build/complete_project_documentation/backend/users_accounts/` | /api/users/ |

## App documentation standard for future updates

For each app, keep these sections current: purpose evidenced by source; entry points; models and relationships; API routes and operations; serializers/validation; views/services; permissions/ownership; signals/tasks/events; frontend route/components/services/stores; inbound/outbound dependencies; tests; known gaps; exact source evidence and verification date.

## Additional app summaries already added under source architecture

- `agents`: `Build/source_architecture/02_backend/applications/agents.md`
- `ai_tools_laboratory`: `Build/source_architecture/02_backend/applications/ai_tools_laboratory.md`
- `analytics`: `Build/source_architecture/02_backend/applications/analytics.md`
- `architecture`: `Build/source_architecture/02_backend/applications/architecture.md`
- `crm`: `Build/source_architecture/02_backend/applications/crm.md`
- `marketing`: `Build/source_architecture/02_backend/applications/marketing.md`
- `revenue`: `Build/source_architecture/02_backend/applications/revenue.md`
- `sales`: `Build/source_architecture/02_backend/applications/sales.md`
- `skills`: `Build/source_architecture/02_backend/applications/skills.md`
## Unregistered scaffold

`skills/` is listed as a source directory for completeness, but is not an installed Django app. Its files are placeholders; the real `Skill` model is in `learning`.
