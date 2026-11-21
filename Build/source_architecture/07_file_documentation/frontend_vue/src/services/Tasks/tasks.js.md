# File documentation: Tasks API service

## Identity and status

- **Source:** [frontend_vue/src/services/Tasks/tasks.js](../../../../../../../frontend_vue/src/services/Tasks/tasks.js)
- **Area:** Frontend tasks domain; API service module.
- **Purpose:** Exposes task-specific functions that call the shared Axios client using the shared endpoint registry.
- **Evidence status:** Client calls and transformations are **VERIFIED** by static inspection. Backend compatibility and request success are **NOT RUNTIME VERIFIED**.

## Purpose and dependencies

The module imports the default client from services/Shared/api and the endpoint object from services/Shared/endpoints (lines 1–2). It exports named functions and a default object containing the same task operations (lines 6–24).

The local unwrap helper returns an array response unchanged, otherwise returns data.results or an empty array (line 4). It is used by listTasks, listTodayTasks, and getOverdueTasks. Other methods return response.data directly, except deleteTask, which returns true after the request resolves.

## Exported operations

| Export | HTTP request | Endpoint registry entry | Result handling | Evidence |
|---|---|---|---|---|
| listTasks(params = {}) | GET with params | tasks.list | unwrap(response.data) | Line 6 |
| listTodayTasks() | GET | tasks.today | unwrap(response.data) | Line 7 |
| getTask(id) | GET | tasks.detail(id) | response.data | Line 8 |
| createTask(payload) | POST | tasks.list | response.data | Line 9 |
| updateTask(id, payload) | PATCH | tasks.detail(id) | response.data | Line 10 |
| deleteTask(id) | DELETE | tasks.detail(id) | Resolves to true after request completion | Line 11 |
| completeTask(id, actual_minutes) | POST with actual_minutes | tasks.complete(id) | response.data | Line 12 |
| postponeTask(id, until) | POST with until | tasks.postpone(id) | response.data | Line 13 |
| generateTodayTasks(payload = {}) | POST with payload | tasks.generate | response.data | Line 14 |
| startTask(id), cancelTask(id), reopenTask(id) | POST | tasks.start/cancel/reopen(id) | response.data | Lines 15–17 |
| getTaskStats(), getTaskProgress() | GET | tasks.stats/progress | response.data | Lines 18–19 |
| getTaskCalendar(params = {}) | GET with params | tasks.calendar | response.data | Line 20 |
| getOverdueTasks(params = {}) | GET with params | tasks.overdue | unwrap(response.data) | Line 21 |
| getTaskGenerationStatus(taskId) | GET | tasks.generationStatus(taskId) | response.data | Line 22 |

The actual path strings are declared in frontend_vue/src/services/Shared/endpoints.js, lines 47–61. The endpoint registry contains paths without the /api prefix; the shared client supplies its base URL from VITE_API_BASE_URL or its local default in services/Shared/api.js, lines 5 and 14–18.

## Callers and integration

TodayTasks.vue imports listTodayTasks, createTask, updateTask, deleteTask, completeTask, postponeTask, generateTodayTasks, and reopenTask. Other exports support other task views and consumers; repository-wide callers are not exhaustively listed here.

The Django project mounts tasks.api.urls under api/tasks/; that router registers TaskViewSet. The endpoint names and action declarations have source-level counterparts in backend_django/tasks/api/views/tasks_views.py. This mapping is static and does not verify router-expanded URLs or successful HTTP requests.

## Authentication and error behavior

This service does not add authentication headers or catch errors locally. The shared Axios client in services/Shared/api.js adds a bearer token when present, includes refresh handling for 401 responses, and rejects unresolved errors to callers (request interceptor lines 119–156; response interceptor lines 184–247). These client behaviors are outside this module.

Callers may display response error details; this service itself passes rejected requests through. list normalization can turn an unexpected non-array response without a results array into an empty list, as defined by unwrap.

## Related documentation

- [Frontend Tasks service and API guide](../../../../../../complete_project_documentation/frontend/tasks/services-and-api.md)
- [Frontend Tasks workflow guide](../../../../../../complete_project_documentation/frontend/tasks/workflows.md)
- [Frontend architecture](../../../../../03-frontend-architecture.md)
- [API and integration map](../../../../../04-api-and-integration-map.md)
- [Frontend/backend mapping](../../../../../04_integration/FRONTEND_BACKEND_MAPPING.md)
- [TodayTasks view file documentation](../../views/tasks/TodayTasks.vue.md)
- [Backend TaskViewSet file documentation](../../../../backend_django/tasks/api/views/tasks_views.py.md)

## Tests and limitations

The existing frontend Tasks guides list service behavior but do not establish successful requests. The selected backend test file tests TaskService and TaskSerializer behavior, not this Axios service. No frontend or backend tests were run for this pilot.

The mapping documents declared URL builders and handlers only. It does not establish deployed base URL values, server availability, response compatibility for every operation, or runtime authentication behavior.
