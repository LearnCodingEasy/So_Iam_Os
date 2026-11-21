# Backend Architecture

## Django project and routing

**VERIFIED:** `backend_django/backend_django/settings.py` installs Django/DRF integrations and 17 project apps: `ai`, `automation`, `challenges`, `codex`, `core`, `goals`, `jobs_opportunity`, `knowledge`, `learning`, `memory`, `notification`, `personal_finance`, `projects`, `scraper`, `social`, `tasks`, and `users_accounts`. `backend_django/backend_django/urls.py` mounts their API URL modules, plus admin, allauth, and media patterns.

The usual domain API chain is URL module → view/viewset → serializer → model, with services used for selected business operations. This pattern is **VERIFIED** in representative flows such as `backend_django/goals/api/urls.py`, `backend_django/goals/api/views/goals_views.py`, `backend_django/goals/api/serializers/goals_serializers.py`, and `backend_django/goals/models/goal.py`. It is not uniform across all apps.

## Domain app inventory

| App | Source-visible scope | Evidence |
|---|---|---|
| `users_accounts` | Custom user and account/profile API | `users_accounts/models/user.py`; `users_accounts/api/` |
| `core` | Shared settings, dashboard and debug console | `core/models/`; `core/api/`; `core/debug_console/` |
| `goals`, `tasks`, `projects`, `challenges` | Personal plans, execution items, project links, challenge progress | respective `models/`, `api/`, and `services/` directories |
| `learning`, `knowledge` | Learning pathways, assessment and knowledge/file workflows | respective `models/`, `api/`, `services/`, and `tasks/` |
| `jobs_opportunity`, `personal_finance` | Career records/workflows and personal finance records/reports | respective `models/`, `api/`, and `services/` |
| `ai`, `codex` | AI providers/conversations/workflows and project intelligence/execution tools | `ai/`; `codex/` |
| `automation`, `scraper` | Desktop/workflow automation and configurable scraping | `automation/`; `scraper/` |
| `social`, `memory`, `notification` | Social relations, memory items, and user notifications | respective `models/` and `api/` |

The detailed entities and domain behavior live in [domain documents](./domains/ai-and-codex.md); the table above is an index, not a claim that each domain is complete.

## Authentication and permissions

**VERIFIED:** Global DRF defaults in `backend_django/backend_django/settings.py` configure JWT authentication and authenticated access. The configured user model is `users_accounts.User`; account views explicitly permit signup and authenticate other account operations (`backend_django/users_accounts/api/views/users_accounts_views.py`). Per-object ownership checks vary by app, for example `backend_django/goals/api/views/goals_views.py`, `backend_django/learning/api/views/user_owned_queryset_mixin_views.py`, and `backend_django/personal_finance/api/views/owned_views.py`.

**UNKNOWN:** Static review does not establish that every endpoint scopes related-object writes and reads correctly. See [Security and Operations](./06-security-and-operations.md).

## Services, async work, and events

**VERIFIED:** Celery is configured for autodiscovery (`backend_django/backend_django/celery.py`). Task implementations are present for learning task generation, AI learning-plan work, knowledge-file extraction, job-source work, and automation execution. A daily learning-task schedule is declared in `backend_django/backend_django/settings.py`.

**VERIFIED:** ASGI routes HTTP to Django and WebSockets to `core.debug_console.routing.websocket_urlpatterns` (`backend_django/backend_django/asgi.py`).

**UNKNOWN:** No worker, broker, scheduler, or WebSocket service was started; declared tasks and channels are not runtime-confirmed.

## Persistence and side effects

Database selection and media root are configured in `backend_django/backend_django/settings.py`; user uploads and knowledge-file extraction are implemented in `backend_django/users_accounts/models/user.py` and `backend_django/knowledge/`. AI provider requests and job feed requests are visible in `backend_django/ai/providers/` and `backend_django/jobs_opportunity/tasks.py`. Desktop/window/screenshot effects are in `backend_django/automation/`.

For entity relationships see [Data Architecture](./05-data-architecture.md); for external and privileged effects see [Security and Operations](./06-security-and-operations.md).
