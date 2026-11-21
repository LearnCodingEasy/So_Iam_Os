# Complete Data Flow

## Common request path
**VERIFIED:** The main Axios client attaches bearer credentials and telemetry (frontend_vue/src/services/Shared/api.js); endpoint builders are centralized in endpoints.js. Django root URLs dispatch to app route modules (backend_django/backend_django/urls.py). Handlers may use serializers, services, ORM models, or direct queries.

~~~mermaid
sequenceDiagram
 actor User
 participant View as Vue view/component
 participant State as Store/service
 participant Client as HTTP client
 participant URL as Django URLconf
 participant Handler as View, serializer, service
 participant DB as ORM database
 User->>View: interact
 View->>State: read or mutate feature state
 State->>Client: request endpoint
 Client->>URL: HTTP request
 URL->>Handler: dispatch
 Handler->>DB: ORM access
 DB-->>Handler: result
 Handler-->>Client: response
 Client-->>State: response or error
 State-->>View: render update
~~~

This is a common pattern; a feature may omit layers. It is not runtime-verified.

## Async and external paths
**VERIFIED:** Celery bootstrap/autodiscovery is in backend_django/backend_django/celery.py. Task code exists in ai/tasks/, knowledge/tasks/, jobs_opportunity/tasks.py, automation/tasks.py, tasks/tasks.py, scraper/tasks.py, and codex/tasks.py.
Provider calls, job-source fetching, media storage, and desktop operations are present in backend_django/ai/providers/, jobs_opportunity/tasks.py, settings.py, and automation/engine_runtime.py.

**UNKNOWN:** Broker connectivity, queueing, retries, worker execution, external responses, and deployed credentials were not checked.

## Response handling
**PARTIAL:** Shared Axios interceptors handle refresh and telemetry, but additional clients and fetch paths exist (frontend_vue/src/services/Shared/api.js, axiosInstance.js, mcpService.js, frontend_vue/src/services/AI/AIService.js). Feature response/error normalization needs method-level documentation.

