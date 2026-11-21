# SO_IAM_OS Master Project Guide

## Project identity
**VERIFIED:** The Vue interface labels the application “Personal AI OS” and presents a signed-in dashboard and navigation for goals, tasks, learning, knowledge, jobs, finance, AI, projects, Codex, and automation. Evidence: frontend_vue/src/components/ai/layout/Sidebar.vue; frontend_vue/src/views/shared/HomeView.vue; frontend_vue/src/router/index.js.
**INFERRED:** SO_IAM_OS is a personal productivity and self-management application combining life/work domains with AI-assisted features. The code supports this interpretation but does not prove a broader future vision of a fully autonomous operating system.

## System at a glance
**VERIFIED:** The browser client is Vue with Vue Router and Pinia; the backend is one Django project with DRF modules for 17 installed domain apps. Celery and Channels are configured in source. Evidence: frontend_vue/package.json; frontend_vue/src/main.js; backend_django/backend_django/settings.py; backend_django/backend_django/asgi.py; backend_django/backend_django/celery.py.

~~~mermaid
flowchart LR
 Person --> Vue[Vue SPA]
 Vue --> Services[Feature services and stores]
 Services --> API[Django REST APIs]
 API --> Domain[Views, serializers, services]
 Domain --> DB[(Configured database)]
 Domain --> Jobs[Celery tasks]
 Jobs --> Redis[(Configured Redis)]
 Domain --> External[Providers, job feeds, media, desktop automation]
 Vue -. WebSockets .-> ASGI[ASGI and Channels]
~~~

The diagram reflects source configuration, not verified production services or live request success.

## Capability snapshot
| Area | Evidence | Assessment |
|---|---|---|
| Accounts | backend_django/users_accounts/; frontend_vue/src/views/accounts/ | **VERIFIED** account models, routes and UI |
| Planning | backend_django/goals/ and tasks/; frontend_vue/src/views/goals/ and tasks/ | **VERIFIED** models, APIs and routed views |
| Learning and knowledge | backend_django/learning/ and knowledge/; corresponding Vue views | **VERIFIED** broad model/API/UI surface |
| Jobs and finance | backend_django/jobs_opportunity/ and personal_finance/; corresponding Vue views/services | **PARTIAL** broad implementation; workflow/runtime unknown |
| AI and Codex | backend_django/ai/ and codex/; frontend_vue/src/views/ai/ and codex/ | **PARTIAL** substantial code; provider/workspace runtime unknown |
| Automation and scraping | backend_django/automation/ and scraper/; frontend views/services | **PARTIAL** side-effecting code exists; deployment/safeguards need review |

## Developer navigation
- Backend root routing: backend_django/backend_django/urls.py; app routing: each api/urls.py.
- Frontend routing: frontend_vue/src/router/index.js.
- Main HTTP client and endpoint builders: frontend_vue/src/services/Shared/api.js and endpoints.js.
- Persistence and cross-domain models: backend_django/<app>/models/.
- Domain state: frontend_vue/src/stores/.
- Business and async operations: backend_django/<app>/services/, task modules, backend_django/backend_django/celery.py.
- API details: 05-complete-api-catalog.md; coverage: 99-documentation-coverage-register.md.

## Evidence limits
**UNKNOWN:** Deployed topology, production environment values, live DB state, provider availability, and worker/socket health. No tests, builds, migrations, application scripts, or runtime services were executed.

