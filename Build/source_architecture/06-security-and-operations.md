# Security and Operations

## Authentication and authorization

**VERIFIED:** Django REST Framework defaults to JWT authentication and authenticated access in `backend_django/backend_django/settings.py`. The custom model is `users_accounts.User`. Account views explicitly allow signup; other account operations declare authentication (`backend_django/users_accounts/api/views/users_accounts_views.py`). Vue stores access/refresh tokens in localStorage and attaches bearer tokens via `frontend_vue/src/services/Shared/api.js` and `frontend_vue/src/stores/accounts/user.js`.

**PARTIAL:** Ownership checks are implemented at view/serializer boundaries, but patterns vary by app. Examples include project, learning, knowledge, and finance ownership code in `backend_django/projects/api/`, `backend_django/learning/api/`, `backend_django/knowledge/api/`, and `backend_django/personal_finance/api/`. A full endpoint-by-endpoint permission audit is required before asserting uniform isolation.

## Secrets and environment configuration

**VERIFIED:** Settings load environment-specific files, define production checks for secret-key quality and AI credential encryption, configure allowed origins/hosts and secure-cookie/HSTS behavior, and select database/cache/provider settings from environment. Evidence: `backend_django/backend_django/settings.py`.

No secret values are reproduced here. **UNKNOWN:** effective environment values, secret-manager use, deployment TLS, and production policy are not inspectable from static source alone.

## Sensitive operations and side effects

| Boundary | Source evidence | Static assessment |
|---|---|---|
| Codex workspace/file operations | `backend_django/codex/services/execution.py`, `build_workspace.py`, `extensions.py`; Codex API views | **VERIFIED** local file reads/writes and commands are represented; path/approval guarantees need deeper review |
| Desktop automation | `backend_django/automation/engine_runtime.py`, `workflow_runner.py`, `permission_policy.py` | **VERIFIED** desktop input, window/process, screenshot, and file/log behavior exists; `shell=True` path merits security review |
| AI providers | `backend_django/ai/providers/`, `backend_django/ai/services/provider_service.py` | **VERIFIED** provider adapters and network request code exist; credentials and providers may not be configured at runtime |
| Job-source fetching | `backend_django/jobs_opportunity/tasks.py` | **VERIFIED** external source fetching code exists; reachable sources and scheduling unknown |
| User file storage | `backend_django/knowledge/models/knowledge_file.py`, `backend_django/users_accounts/models/user.py`, `backend_django/backend_django/settings.py` | **VERIFIED** upload fields and media root configured; deployed storage/access controls unknown |
| Debug WebSocket | `backend_django/core/debug_console/` and `backend_django/backend_django/asgi.py` | **VERIFIED** route/consumer code exists; runtime exposure unknown |

These are risk boundaries for review, not findings of exploitability.

## Runtime components

**VERIFIED:** Celery uses Django settings and autodiscovery; Redis is the default broker/result/cache target; Channels defaults to an in-memory layer with a Redis option; media uses the configured Django media root. Evidence: `backend_django/backend_django/celery.py`, `backend_django/backend_django/settings.py`, `backend_django/backend_django/asgi.py`.

**UNKNOWN:** No database, Redis, Celery worker/beat, provider, HTTP server, or WebSocket service was started or queried. No runtime readiness claim is made.

## Recommended security review

Prioritize endpoint ownership checks, Codex path containment and approval flows, automation shell/desktop execution controls, OAuth callback handling, and browser token storage. These recommendations are based on the source paths above and require focused verification; they are not a substitute for a security assessment.

See [Data Architecture](./05-data-architecture.md) and [Architecture Gaps and Roadmap](./07-architecture-gaps-and-roadmap.md).
