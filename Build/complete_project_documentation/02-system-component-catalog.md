# System Component Catalog

## Backend application catalog
All 17 are in INSTALLED_APPS in backend_django/backend_django/settings.py. Registration does not prove deployment/runtime status.

| App | Source-visible implementation |
|---|---|
| ai | Models, API, providers, services, tasks |
| automation | Models, API, engine, services, workflow runner, task |
| challenges | Models and API |
| codex | Models, API, project scanning/intelligence and execution services |
| core | Shared models/API, signals, debug console |
| goals | Goal/milestone models, API, services |
| jobs_opportunity | Career models/API/services/tasks/signals |
| knowledge | Item/file models, API, extractors/services/tasks |
| learning | Learning and assessment models, API/services |
| memory | Memory model and API |
| notification | Notification model and API |
| personal_finance | Finance models, API, services |
| projects | Project models and API |
| scraper | Scraping models/API/services/tasks |
| social | Social graph models/API/services |
| tasks | Task model/API/services/tasks |
| users_accounts | Custom user, account API, forms/admin |

## Frontend feature catalog
Routed feature names come from frontend_vue/src/router/index.js. Service folders are separate source groupings under frontend_vue/src/services/.

| Domain | Typical source areas |
|---|---|
| accounts | views/accounts, services/Accounts, stores/accounts |
| ai | views/ai, services/AI, stores/ai |
| automation | views/automation, services/Automation, components/automation |
| challenges | views/challenges, services/Challenges |
| codex | views/codex, services/Codex, stores/codex |
| core | views/core, services/Core, components/core |
| finance | views/finance, services/Finance |
| goals | views/goals, services/Goals, stores/goals |
| jobs | views/jobs, services/Jobs |
| knowledge | views/knowledge, services/Knowledge, stores/knowledge |
| learning | views/learning, services/Learning |
| memory | views/memory, services/Memory |
| notifications | views/notifications, services/Notifications |
| projects | views/projects, services/Projects, stores/projects |
| scraper | views/scraper, services/Scraper |
| shared | views/shared and shared UI |
| social | views/social, services/Social |
| tasks | views/tasks, services/Tasks |

## Shared/runtime boundaries
- Frontend dependencies/scripts: frontend_vue/package.json.
- Django/DRF/auth/database/cache/Celery/Channels/media: backend_django/backend_django/settings.py.
- ASGI and Celery bootstraps: backend_django/backend_django/asgi.py and celery.py.
- Provider, job-fetching, file, and desktop effects: backend_django/ai/providers/, jobs_opportunity/tasks.py, knowledge/, automation/.
- Frontend HTTP clients and endpoint registry: frontend_vue/src/services/Shared/.

Per-file coverage is tracked in 99-documentation-coverage-register.md.

