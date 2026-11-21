# API and Integration Map

## Integration method

The frontend's shared endpoint builders are in `frontend_vue/src/services/Shared/endpoints.js`; Django project mounts are in `backend_django/backend_django/urls.py`; app route declarations are in each `backend_django/<app>/api/urls.py`. The examples below trace source declarations. **VERIFIED** means the files define matching code paths; it does not mean an HTTP request was executed or works at runtime.

## Representative vertical traces

| Domain | Frontend path | Backend path | Status |
|---|---|---|---|
| Accounts | `views/accounts/LoginView.vue` → `services/Accounts/usersAccounts.js` → shared endpoints | `users_accounts/api/urls.py` → `api/views/users_accounts_views.py` → serializers and `models/user.py` | **VERIFIED** source mapping; provider callback runtime **UNKNOWN** |
| Goals | `views/goals/Goals.vue` → `services/Goals/goals.js` and goal store | `goals/api/urls.py` → `api/views/goals_views.py` → `goals_serializers.py` → `models/` | **VERIFIED** representative mapping |
| Tasks | `views/tasks/` → `services/Tasks/tasks.js` | `tasks/api/urls.py` → `api/views/tasks_views.py` → `tasks_serializers.py` → `models/task.py` | **VERIFIED** representative mapping |
| Learning | `views/learning/` → `services/Learning/learning.js` | `learning/api/urls.py` → `learning/api/views/` → serializers and models | **VERIFIED** resource families; individual response compatibility **UNKNOWN** |
| Knowledge | `views/knowledge/` → knowledge store/service | `knowledge/api/urls.py` → item/file viewsets and serializers → knowledge models | **VERIFIED** representative mapping |
| Jobs | `views/jobs/JobsView.vue` → `services/Jobs/jobs.js` | `jobs_opportunity/api/urls.py` → job viewsets/actions → serializers/models | **PARTIAL** routed view uses a subset of the broader API surface |
| Finance | `views/finance/FinanceView.vue` → finance service | `personal_finance/api/urls.py` → viewsets/function views → serializers/models | **PARTIAL** source paths align; response shapes are unverified |
| AI | `views/ai/` → AI services and streaming fetch | `ai/api/urls.py` → API views/services → AI models/providers | **PARTIAL** external provider and stream runtime unknown |
| Codex | `views/codex/` → `services/Codex/codex.js` | `codex/api/urls.py` → Codex views/services/models | **PARTIAL** extensive source surface; full per-operation contracts not exhaustively traced |
| Automation | `views/automation/` → automation services | `automation/api/urls.py` → automation views, serializers, models | **PARTIAL** several backend operations are not shown in the routed UI mapping |
| Projects | `views/projects/ProjectsView.vue` → `services/Projects/projects.js` | `/api/projects/` mount plus `projects` router resource → view/serializer/model | **VERIFIED** route composition in source |

## Cross-cutting client differences

**VERIFIED:** The primary API client uses `VITE_API_BASE_URL` and localStorage keys `user.access` / `user.refresh` (`frontend_vue/src/services/Shared/api.js`). A separate Axios instance reads `auth_token` (`frontend_vue/src/services/Shared/axiosInstance.js`); global Axios defaults are also assigned in `frontend_vue/src/main.js`; AI streaming uses `fetch` with `getValidAccessToken()` (`frontend_vue/src/services/AI/AIService.js`). These are distinct request paths with different configuration.

## Static mismatches and partial paths

- **VERIFIED:** Codex build workspace and manifest paths are declared in both `backend_django/backend_django/urls.py` and `backend_django/codex/api/urls.py`. This is duplicate route declaration; no URL resolver behavior was tested.
- **VERIFIED:** Finance exposes a `SavingPlan` model, while `backend_django/personal_finance/api/urls.py` does not register a SavingPlan endpoint. **NOT IMPLEMENTED:** a public API route for that model was not found in the inspected URL module.
- **VERIFIED:** `frontend_vue/src/services/AI/aiPlatformService.js` reports workflow execution as unsupported. The existence of backend workflow routes does not complete that frontend operation.
- **PARTIAL:** Several service exports and backend endpoints are not invoked by the main routed Jobs view. This is not proof they are unused elsewhere.
- **PARTIAL:** Mock/placeholder UI exists in `frontend_vue/src/components/codex/Capabilities/` and `frontend_vue/src/components/automation/Workflow/WorkflowVersions.vue`; connection to the primary route and end-to-end behavior must be checked before calling these live features.

## Validation boundary

No HTTP calls, endpoint contract tests, or server startup were performed. **UNKNOWN:** status codes, response shape compatibility, route reachability, CORS behavior, and deployed API base URLs. For shared client architecture see [Frontend Architecture](./03-frontend-architecture.md); for permission review see [Security and Operations](./06-security-and-operations.md).
