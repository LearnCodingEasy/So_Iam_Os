# Background Jobs and Integrations

## Celery
**VERIFIED:** backend_django/backend_django/celery.py configures Celery from Django settings with autodiscovery. Settings define Redis broker/result defaults and a daily task schedule. Task source exists in ai/tasks/, knowledge/tasks/, jobs_opportunity/tasks.py, automation/tasks.py, tasks/tasks.py, scraper/tasks.py, and codex/tasks.py.

**UNKNOWN:** Workers, beat, broker connectivity, retries, and task completion were not run or verified.

## Channels
**VERIFIED:** backend_django/backend_django/asgi.py routes HTTP to Django and WebSockets to core.debug_console.routing. Settings choose in-memory Channels by default with a Redis option. Vue WebSocket consumers occur under shared and automation components. Runtime reachability is unknown.

## Integrations
| Boundary | Evidence | Status |
|---|---|---|
| AI providers | backend_django/ai/providers/ and ai/services/ | **PARTIAL** request code exists; credentials/runtime unknown |
| Google OAuth | settings.py and users_accounts/ | **PARTIAL** configured; callback operation unverified |
| Job source fetching | jobs_opportunity/tasks.py | **PARTIAL** network code exists; sources/scheduling unknown |
| File extraction/media | knowledge/ and settings.py | **VERIFIED** source processing/storage paths |
| Desktop automation | automation/ | **PARTIAL** process/window/screenshot code; environment/security need review |


