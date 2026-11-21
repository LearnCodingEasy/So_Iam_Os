# Complete API Catalog — Initial Route Inventory

## Evidence status
**VERIFIED** below means URL/view declarations exist in source. It does not mean requests succeed. The completed catalog must add each route's methods, handler, permission, serializer, frontend consumer, payload contract review, and runtime-verification status.

## Project mounts
backend_django/backend_django/urls.py mounts:
- /api/codex/ (with two build routes also declared at root)
- /api/users/, /api/core/, /api/knowledge/, /api/learning/, /api/scraper/, /api/ai/
- /api/goals/, /api/tasks/, /api/jobs/, /api/social/, /api/automation/, /api/notifications/
- /api/memory/, /api/projects/, /api/challenges/, /api/finance/
- /accounts/, /admin/, and configured media patterns.

## Route source index
| Prefix | Route declaration | Handler/contract locations | Frontend area | Status |
|---|---|---|---|---|
| users | users_accounts/api/urls.py | api/views/, serializers/ | Accounts | **PARTIAL** |
| core | core/api/urls.py | api/views/ | Core | **PARTIAL** |
| knowledge | knowledge/api/urls.py | api/views/, serializers/, models/ | Knowledge | **PARTIAL** |
| learning | learning/api/urls.py | api/views/, serializers/, models/ | Learning | **PARTIAL** |
| scraper | scraper/api/urls.py | api/views/, serializers/, models/ | Scraper | **PARTIAL** |
| ai | ai/api/urls.py | api/views/, serializers/, models/ | AI | **PARTIAL** |
| goals | goals/api/urls.py | api/views/, serializers/, models/ | Goals | **PARTIAL** |
| tasks | tasks/api/urls.py | api/views/, serializers/, models/ | Tasks | **PARTIAL** |
| jobs | jobs_opportunity/api/urls.py | api/views/, serializers/, models/ | Jobs | **PARTIAL** |
| social | social/api/urls.py | api/, models/ | Social | **PARTIAL** |
| automation | automation/api/urls.py | api/views/, serializers/, models/ | Automation | **PARTIAL** |
| notifications | notification/api/urls.py | api/views/, serializers/, models/ | Notifications | **PARTIAL** |
| memory | memory/api/urls.py | api/views/, serializers/, models/ | Memory | **PARTIAL** |
| projects | projects/api/urls.py | api/views/, serializers/, models/ | Projects | **PARTIAL** |
| challenges | challenges/api/urls.py | api/views/, serializers/, models/ | Challenges | **PARTIAL** |
| finance | personal_finance/api/urls.py | api/, models/ | Finance | **PARTIAL** |
| codex | codex/api/urls.py | api/views/, serializers/, models/ | Codex | **PARTIAL** |

The two Codex build endpoint paths are declared at both backend_django/backend_django/urls.py and codex/api/urls.py; no resolver test was run. App api.md files will hold route-level details. No endpoint is runtime-verified.

