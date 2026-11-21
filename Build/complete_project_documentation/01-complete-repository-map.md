# Complete Repository Map

This map covers implementation under backend_django/ and frontend_vue/. Generated data, dependency trees, and binary assets are not application source.

## Backend
| Path | Responsibility | Evidence |
|---|---|---|
| backend_django/backend_django/ | Django settings, root URLs, ASGI/WSGI, Celery app | settings.py, urls.py, asgi.py, wsgi.py, celery.py |
| backend_django/<installed app>/ | One of 17 apps registered in INSTALLED_APPS | backend_django/backend_django/settings.py |
| backend_django/<app>/api/ | Domain routes, views, serializers, API helpers where present | app-local api/urls.py, views/, serializers/ |
| backend_django/<app>/models/ | ORM definitions | app-local models/ |
| backend_django/<app>/services/ | Domain operations where present | app-local services/ |
| backend_django/<app>/tests/ | Test source; not executed | app-local tests/ |
| backend_django/<app>/migrations/ | Schema history; not applied | app-local migrations/ |
| backend_django/<app>/tasks.py or tasks/ | Async work where present | AI, Knowledge, Jobs, Automation, Tasks, Scraper, Codex |
| backend_django/core/debug_console/ | Debug-console WebSocket implementation | core/debug_console/ and asgi.py |
| backend_django/scripts/ | Helper source; not executed | scripts/ |
| backend_django/media/ | User/generated media data | settings.py MEDIA_ROOT |

Installed apps: ai, automation, challenges, codex, core, goals, jobs_opportunity, knowledge, learning, memory, notification, personal_finance, projects, scraper, social, tasks, users_accounts. Directory names alone do not define app boundaries.

## Frontend
| Path | Responsibility | Evidence |
|---|---|---|
| frontend_vue/src/main.js | Vue bootstrap and plugin/component registration | main.js |
| frontend_vue/src/router/ | Route declarations and guards | router/index.js |
| frontend_vue/src/views/<domain>/ | Screen-level features | router/index.js and views/ |
| frontend_vue/src/components/ | Domain and shared components | components/ |
| frontend_vue/src/services/<domain>/ | API/helper services | services/ |
| frontend_vue/src/services/Shared/ | HTTP clients and endpoint builders | api.js, endpoints.js, axiosInstance.js |
| frontend_vue/src/stores/ | Pinia state/persistence | stores/ |
| frontend_vue/src/composables/ | Reusable composition functions | composables/ |
| frontend_vue/src/plugins/, presets/, utils/ | Plugins, themes, helpers | corresponding directories |
| frontend_vue/src/assets/ | Source styles and binary assets | assets/ |
| frontend_vue/public/ | Public static assets | public/ |
| frontend_vue/*.config.js | Vite/Vitest/lint/CSS configuration | frontend root config files |

Routed view domains: accounts, ai, automation, challenges, codex, core, finance, goals, jobs, knowledge, learning, memory, notifications, projects, scraper, shared, social, tasks. Evidence: frontend_vue/src/router/index.js.

## Exclusions
Python bytecode/cache, dependency trees, the SQLite database file, media uploads, binary images, and generated build output are not source-symbol files. Tests and migration files are inventoried but never run/applied. Build/ and project_docs/ contents are protected and excluded as evidence.


## Backend project-level Python files

These eight Python files are outside the 17 installed app folders and are listed here so the application entry/configuration surface is not omitted:

| File | Source-visible responsibility |
|---|---|
| backend_django/manage.py | Django command dispatch; do not invoke during this audit |
| backend_django/backend_django/settings.py | Installed apps, middleware, database, auth, cache, Celery, Channels, media and security configuration |
| backend_django/backend_django/urls.py | Project API mounts and admin/allauth/media routes |
| backend_django/backend_django/asgi.py | HTTP/WebSocket protocol routing |
| backend_django/backend_django/wsgi.py | WSGI application factory |
| backend_django/backend_django/celery.py | Celery configuration and task autodiscovery |
| backend_django/backend_django/__init__.py | Project Python package initializer |
| backend_django/scripts/repair_database.py | Database inspection and migration-repair script; inspected as text only and never executed |

