# SO_IAM_OS — Frontend/Backend API Integration Guide

## 1. Canonical connection contract

- Django API root: `/api/`.
- Frontend shared Axios client: `frontend_vue/src/services/api.js`.
- Configure `frontend_vue/.env` from `.env.example` with `VITE_API_BASE_URL=http://127.0.0.1:8000/api` (include `/api` exactly once).
- Shared client automatically adds the access token from `localStorage` key `user.access`, attempts refresh through `/users/refresh/` on HTTP 401, and emits request metadata without logging request/response bodies.
- Prefer `services/endpoints.js` for paths and the app-specific service modules for requests. Do not call a URL hard-coded to `localhost` from a page.
- Protected endpoints require a valid authenticated user. Django querysets must continue to scope private records to `request.user`.

## 2. App-by-app integration map

| Django app / prefix | Backend contract files | Frontend service / entry point | Endpoint families |
|---|---|---|---|
| Users / `/api/users/` | `users_accounts/urls.py`, `api.py` | `services/usersAccounts.js`, `stores/user.js` | `me`, `signup`, `login`, `refresh`, `profile/<uuid>/`, `editprofile`, `editpassword` |
| Core / `/api/core/` | `core/urls.py`, `views.py` | `services/ecosystemApi.js`, `services/settings.js`, `services/endpoints.js` | `health`, `dashboard`, `learning-settings` |
| Knowledge / `/api/knowledge/` | `knowledge/models.py`, `serializers.py`, `views.py`, `urls.py`, `services.py` | `services/knowledge.js`; Learning also calls Knowledge through `services/learning.js` | `items`, `files`; item actions `archive`, `restore`, `extract-metadata`, `connect-topic`, `disconnect-topic`, `upload-file` |
| Learning / `/api/learning/` | `learning/models.py`, `serializers.py`, `views.py`, `urls.py`, `services/` | `services/learning.js`, `views/learning/LearningView.vue`, `views/learning/LearningTopic.vue` | `skills`, `goals`, `paths`, `topics`, `lessons`, `resources`, `notes`, `progress`, `sessions`, `assessments`, question/choice/attempt/response resources, applications/submissions/reviews, revisions |
| Goals / `/api/goals/` | `goals/models.py`, `serializers.py`, `views.py`, `urls.py`, `services.py` | `services/goals.js`, `services/endpoints.js` | list/detail CRUD; detail actions `complete`, `pause`, `resume`, `progress` |
| Tasks / `/api/tasks/` | `tasks/models.py`, `serializers.py`, `views.py`, `urls.py`, `services.py`, `daily_generation.py` | `services/tasks.js`, `services/taskService.js` | CRUD; `today`, `generate`, `complete`, `postpone`, `start`, `cancel`, `reopen`, `stats`, `progress`, `calendar`, `overdue`, `generation-status/<task_id>` |
| Jobs Opportunity / `/api/jobs/` | `jobs_opportunity/models.py`, `serializers.py`, `views.py`, `urls.py`, `services.py`, `tasks.py`, `scraper.py` | `services/jobs.js`, `views/jobs/JobsView.vue` | sources, opportunities, matches, applications, companies, interviews, resumes, cover-letters, preferences, saved-searches, skill-gaps, readiness, recommendations, alerts, analytics, workspace |
| Scraper / `/api/scraper/` | `scraper/models.py`, `serializers.py`, `views.py`, `urls.py`, `services.py`, `tasks.py` | `services/scraperApi.js`, `views/Scraper/ScraperView.vue` | sources, selectors, configs, runs; source actions `stats`, `test_connection`, `run`; run action `results` |
| AI / `/api/ai/` | `ai/models.py`, `serializers.py`, `views.py`, `urls.py`, `services.py`, `providers.py` | `services/ai.js`, `services/AIService.js`, `composables/useAI.js`, `services/endpoints.js` | chat, conversations, settings, credentials, provider models, prompts, learning preview/approve/async, task status, topic chat, agent plan |
| Codex / `/api/codex/` | `codex/urls.py`, `views.py`, `services/`, `models.py` | `services/codex.js`, Codex views | build workspace/manifest, projects, features, files, APIs, protected items, changes, snapshots, context, intelligence, registry, policy, tools, audit, agent runs |
| Social / `/api/social/` | `social/urls.py`, `api.py` | `services/social.js`, `services/ecosystemApi.js` | profile, recommendations, friend suggestions/requests/friends/unfriend |
| Automation / `/api/automation/` | `automation/urls.py`, `views.py` | `services/AutomationService.js`, `services/workflowService.js`, `services/taskService.js` | programs, program-elements, workflows/nodes/edges, actions, tasks/runs, screen-states, delays, `get_open_windows` |
| Notifications / `/api/notifications/` | `notification/urls.py`, `views.py` | `services/notifications.js` | list/detail CRUD and actions as exposed by `NotificationViewSet` |
| Memory / `/api/memory/` | `memory/urls.py`, `views.py` | `services/ecosystemApi.js` and domain endpoint map | `items` |
| Projects / `/api/projects/` | `projects/urls.py`, `views.py` | `services/ecosystemApi.js` | `projects`, `members`, `contexts` |
| Challenges / `/api/challenges/` | `challenges/urls.py`, `views.py` | `services/ecosystemApi.js` | `challenges`, `steps`, `attempts`, `progress` |
| Finance / `/api/finance/` | `personal_finance` URLs/views | `services/ecosystemApi.js` | transactions, categories, budgets, debts, savings, subscriptions, loans, cashflows, reports, coach, alerts, forecast |

The route families above come from the checked-in Django URL configuration. `API_ENDPOINT_AUDIT.csv` contains 396 statically extracted route/action entries with method and frontend-service mapping; entries are static inventory, not proof of successful runtime calls. A route family does not mean every action has been runtime-tested in this environment.

## 3. Learning endpoint contract

All routes below are under `/api/learning/` and use the shared `api` client.

| Resource | Methods / actions used by the UI or service |
|---|---|
| `skills/` | GET (global active skill catalog) |
| `goals/` | GET/POST; `goals/<id>/` GET/PATCH/DELETE; `generate/`, `dashboard/`, `complete/`, `pause/`, `resume/` actions as defined by `LearningGoalViewSet` |
| `paths/` | GET/POST; detail GET/PATCH/DELETE; `start/`, `complete/`, `pause/`, `reorder-topics/` |
| `topics/` | GET/POST; detail GET/PATCH/DELETE; `start/`, `complete/`, `skip/`, `generate-content/` |
| `progress/` | GET/POST/PATCH where supported; `update-progress/` accepts a topic plus progress fields; `summary/` reads progress aggregates |
| `sessions/` | CRUD; `finish/` action |
| `assessments/` | list/detail; `learner/`, `start/`, `submit/` actions |
| `assessment-questions/`, `assessment-choices/`, `assessment-attempts/`, `assessment-responses/` | CRUD methods as permitted by each ViewSet and its serializer |
| `lessons/`, `resources/`, `notes/` | CRUD/read endpoints as configured; notes have create/update/delete helpers in `services/learning.js` |
| `applications/` | CRUD plus `submit/`, `review/`, `history/` where declared in the ViewSet |
| `application-submissions/`, `application-reviews/` | read/write methods defined by each ViewSet |
| `revisions/` | CRUD plus `start/`, `complete/`, `skip/` |

The Learning dashboard's `getLearningDashboard()` loads skills, goals, paths, topics, progress, assessments, attempts, applications and revisions in parallel. If any required request fails, the dashboard reports an error rather than silently filling the missing data with mock records.

## 4. Jobs Opportunity and Scraper: real data flow

### A. Jobs source manager

1. Create or edit a `JobSource` at `/api/jobs/sources/`. Required fields depend on the source type. For API/RSS sources, use `base_url` or `feed_url`; keep credentials out of URLs and `config`.
2. Configure `config.adapter` when required. The existing source worker recognizes `greenhouse`, `lever`, `remotive`, `arbeitnow`, and `jobicy`, plus generic JSON and RSS parsing.
3. Review the URL, usage terms and configuration, then set `enabled=true`.
4. Test with `POST /api/jobs/sources/<id>/test/`.
5. Queue one source with `POST /api/jobs/sources/<id>/sync/`, or enabled sources with `POST /api/jobs/sources/sync-all/`.
6. The response includes a Celery task ID when queued. Results are persisted to `JobOpportunity`; query them through `GET /api/jobs/opportunities/`.
7. The Jobs UI supports filtering by `q`, `skill`, `location`, `remote`, `job_type`, and `experience`.

### B. Public data sources to configure

Use one source at a time and test it first. These are known public API/feed patterns represented in this repository; availability, terms, and fields can change, so test them from the backend host before enabling scheduled use.

- Remotive API example: `https://remotive.com/api/remote-jobs?search=python`, adapter `remotive`.
- Arbeitnow API example: `https://www.arbeitnow.com/api/job-board-api`, adapter `arbeitnow`.
- Jobicy API example: `https://jobicy.com/api/v2/remote-jobs?tag=python`, adapter `jobicy`.
- Greenhouse board API: `https://boards-api.greenhouse.io/v1/boards/<board_token>/jobs?content=true`, adapter `greenhouse`; replace `<board_token>` with a real public board token.
- Lever postings API: `https://api.lever.co/v0/postings/<site>?mode=json`, adapter `lever`; replace `<site>` with the employer's public Lever site slug.
- Public RSS example in the existing presets: `https://www.python.org/jobs/feed/rss/`, source type `rss`.

Do not expect a template URL containing `<board_token>` or `<site>` to work until configured. Do not scrape login-protected pages, bypass CAPTCHAs, ignore robots.txt, or use a source that forbids automated access.

### D. Example: configure and sync a real public API

After obtaining a valid access token from the existing login flow, create a source for the current user. The following is a request-body example, not a claim that the external service was live-tested from this environment:

```http
POST /api/jobs/sources/
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json

{
  "name": "Remotive Python Jobs",
  "source_type": "api",
  "base_url": "https://remotive.com/api/remote-jobs?search=python",
  "feed_url": "",
  "enabled": true,
  "max_items_per_sync": 100,
  "config": {
    "adapter": "remotive",
    "ai_analyze_on_import": false
  }
}
```

Then test and queue it:

```http
POST /api/jobs/sources/<SOURCE_ID>/test/
Authorization: Bearer <ACCESS_TOKEN>

POST /api/jobs/sources/<SOURCE_ID>/sync/
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json

{ "background": true }
```

A successful queue returns HTTP `202` and a Celery task ID. Check the task/worker logs and then call `GET /api/jobs/opportunities/?q=python`. If no records appear, inspect `last_sync_status`, `last_sync_error`, the source's parsed item count, and the worker logs before changing source selectors.

### E. Example: configure the Scraper app

For an RSS source, `POST /api/scraper/sources/` accepts a body like:

```json
{
  "name": "Python Jobs RSS",
  "base_url": "https://www.python.org/jobs/feed/rss/",
  "source_type": "rss",
  "is_active": true,
  "request_timeout": 15,
  "config": { "ai_analyze_on_import": false }
}
```

For HTML, `config` must additionally contain `item_selector`, a `fields` object, and `terms_confirmed: true`; enable it only after checking the site's rules and `robots.txt`.

### C. Scraper app

- Create a source using `POST /api/scraper/sources/` with `name`, `base_url`, `source_type` (`json`, `rss`, or `html`), `is_active`, `request_timeout`, and `config`.
- JSON can use `config.items_path` (for example `jobs` or `data.results`).
- HTML requires a CSS `item_selector` and optional `fields` mapping such as `{"title":{"selector":"h2"},"company":{"selector":".company"},"url":{"selector":"a","attribute":"href"},"description":{"selector":".description"}}`. Confirm permission to collect HTML before enabling it.
- Test with `POST /api/scraper/sources/<uuid>/test_connection/`.
- Start a run with `POST /api/scraper/sources/<uuid>/run/`. This queues `scraper.tasks.run_scraping_job`; the worker must be running.
- Check `GET /api/scraper/runs/`, then `GET /api/scraper/runs/<uuid>/results/` for raw normalized results.
- When the source belongs to an authenticated user, successful runs mirror valid job records into that user's `JobOpportunity` data and the corresponding `JobSource`. Duplicates are identified by source/external ID or a stable URL hash. Matching/readiness is recalculated after import.
- `config.ai_analyze_on_import=true` opts into AI analysis for each imported job. It is off by default to avoid unexpected AI costs and slow ingestion.

### D. AI for jobs

- `POST /api/jobs/opportunities/<id>/analyze/` runs deterministic extraction plus an AI enrichment attempt using the user's configured provider and fallback chain.
- If AI is unavailable or returns invalid JSON, deterministic extraction remains available and `metadata.ai_analysis.status` records `fallback`; this is not reported as AI success.
- `POST /api/jobs/opportunities/<id>/generate_cover_letter/` uses the user's resume (if selected/default) and configured AI provider chain. The prompt explicitly forbids inventing qualifications.
- Skill matching, readiness, skill gaps, and recommendations are database-backed services. The AI analysis step does not fabricate match scores.

### E. AI configuration

- Configure the preferred provider/model at `/api/ai/settings/`.
- User provider credentials are managed under `/api/ai/credentials/`; the backend model encrypts credential values. Never commit real keys or place them in frontend source files.
- Supported provider implementations in `ai/providers.py`: Ollama, OpenAI, OpenRouter. Fallback order starts with the requested/preferred provider and tries the other supported providers. A provider must still have a valid key/model or a reachable local Ollama server.

## 5. Cross-app data contracts

- Knowledge → Learning: `KnowledgeItemViewSet` exposes `connect-topic/` and `disconnect-topic/`; payload includes `topic_id`.
- Jobs → Learning: `POST /api/jobs/skill-gaps/<id>/start_learning/` creates or reuses the linked learning goal for a skill gap.
- Goals ↔ Tasks: goals are user-owned records and task relations are counted from actual task links; progress must be based on completion status, not record creation.
- Scraper → Jobs: source ownership is inherited from the authenticated Scraper `Website.created_by`; only valid public HTTP(S) job URLs are persisted as opportunities.
- AI → Learning: `/api/ai/topic-chat/` requires `topic_id` and `message`; learning content is context, not trusted instructions.

## 6. Operational commands

Run in separate terminals from the project root:

```powershell
# Backend
cd backend_django
python -m venv venv
.env\Scripts\Activate.ps1
pip install -r ..
equirements.txt
python manage.py check
python manage.py migrate
python manage.py runserver

# Frontend
cd ..rontend_vue
npm ci
npm run dev
```

For asynchronous collection, configure Redis using `REDIS_URL`, `CELERY_BROKER_URL`, and `CELERY_RESULT_BACKEND`, then run a worker from `backend_django`:

```powershell
celery -A backend_django worker -l info
```

Confirm the actual Celery app module/name in `backend_django/backend_django/` if the command differs in your local checkout. A `202 Accepted` response only means the task was queued; confirm the run record and saved jobs before considering it successful.

## 7. Verified changes in this delivery

- Removed the shadowed duplicate `JobOpportunityViewSet` declaration and the shadowed duplicate serializer declaration.
- Added user-scoped `POST /api/jobs/sources/sync-all/` and wired it to the Jobs UI.
- Fixed Jobs source preview path to `/jobs/sources/<id>/preview/`.
- Added canonical Scraper endpoint builders and frontend helpers for source configs/selectors/run results.
- Scraper HTML source configuration supports JSON field mappings, stored run results, and explicit permission confirmation. HTML fetching and robots.txt checks reject redirects, private/local host addresses, non-standard ports, and responses larger than 5 MB.
- Scraper imports now normalize common Greenhouse/Lever/Remotive/Arbeitnow/Jobicy fields, strip HTML descriptions, create/update Jobs records, and recalculate matching/readiness. The Jobs worker uses the shared bounded public-fetch utility for API/RSS sources, rejects redirects and private/local source hosts, and skips imported records without valid HTTP(S) job URLs.
- Added opt-in AI analysis on import and explicit AI-backed job analysis; added a bounded provider fallback class for supported providers. AI-on-import is off by default to control latency and provider costs.
- AI chat frontend now calls the real JSON `/api/ai/chat/` endpoint instead of the nonexistent SSE `/api/ai/chat/stream/` and `/api/ai/models/` paths. Cancellation stops the browser request; it cannot guarantee server-side cancellation.
- Fixed Learning goal pause/resume to use the shared authenticated Axios client; fixed legacy About/Auth callback endpoints.
- API telemetry no longer includes request or response bodies.
- Added data migration `jobs_opportunity.0002_normalize_source_types` to correct legacy `html_scraper` source values and copy the old terms-confirmation key without granting consent. Added migration `0003_expand_job_url_length` for longer valid job URLs.
- Added Task API service helpers for the backend's stats/calendar/overdue/status/generation-status actions.

## 8. Important unverified items

This execution environment does not have Django/DRF installed and `frontend_vue/node_modules` is absent. Therefore Django system checks, database migrations, full API tests, Celery/Redis integration, and Vite production build could not be run here. Python syntax compilation and Node syntax checks were run for changed source files. No live external source sync was run, so real-world source availability must be confirmed from your backend machine after configuration.

The checked-in project also contains service modules whose routes do not appear in the root Django URL configuration (for example `mcpService.js` and `explainsService.js`). They are marked as requiring separate route verification rather than being claimed as connected.
