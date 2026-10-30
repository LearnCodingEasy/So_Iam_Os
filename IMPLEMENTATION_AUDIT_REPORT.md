# SO_IAM_OS — API Integration, Jobs/Scraper, and AI Audit

## Delivery scope and status

This is an incremental implementation against the uploaded project, not a claim that every item in the larger 250-feature roadmap is complete. The changes focus on connecting existing Vue services to real Django endpoints, repairing concrete integration defects, making `jobs_opportunity` and `scraper` cooperate, and using configured AI providers without reporting fake success.

`API_INTEGRATION_GUIDE.md` documents the API root, per-app route families, Learning contracts, real-source setup, AI configuration, and run commands. `API_ENDPOINT_AUDIT.csv` contains 396 statically extracted URL/router/action entries with their methods, backend view/action, and frontend service mapping. Static route extraction is not a runtime-success claim.

## Main fixes delivered

### 1. Jobs Opportunity

- Removed the shadowed duplicate `JobOpportunityViewSet` declaration so actions are not silently lost at import time.
- Removed the shadowed duplicate `JobOpportunitySerializer` declaration.
- Added user-scoped `POST /api/jobs/sources/sync-all/` and wired the Jobs UI button to it.
- Changed source testing from a configuration-only response to a bounded live connection test that reports status and item count.
- Fixed source URL validation, disabled/manual-source behavior, and source URL configuration validation.
- Added parsing for nested JSON `items_path`, and normalized Greenhouse, Lever, Remotive, Arbeitnow, and Jobicy field variants.
- Stabilized external IDs for sources without IDs, skipped records with missing titles or unsafe/missing job URLs, stripped HTML from descriptions, and safely parsed dates and salary values.
- Uses the shared bounded public-fetch utility for API/RSS sources; redirects and private/local source hosts are rejected.
- Added migrations to normalize legacy `html_scraper` source values and expand the opportunity URL field to 500 characters.

### 2. Scraper integration

- Scraper UI now supports JSON item paths, HTML CSS selectors, per-field JSON mapping, run-result inspection, and an explicit HTML terms confirmation.
- Added frontend helpers for source configs, selectors, runs, and run results.
- Scraper source tests report a real parsed item count.
- Successful Scraper runs mirror eligible records into the authenticated user's Jobs data, create/update a corresponding `JobSource`, normalize common public job API fields, and recalculate matching/readiness.
- Scraper-to-Jobs configuration is translated to the schema expected by the Jobs source worker, including HTML selector mapping and JSON `items_path`.
- Added bounded response sizes, redirect rejection, public URL checks, and safe `robots.txt` fetching for HTML scraping.
- AI analysis on import is opt-in (`config.ai_analyze_on_import`) and disabled by default to avoid unexpected costs/latency.

### 3. AI integration

- Added a bounded `AIProviderFallbackChain` for configured Ollama, OpenAI, and OpenRouter providers.
- Explicit job analysis now attempts AI enrichment after deterministic extraction; if no provider works or the response is invalid, deterministic results remain available and `metadata.ai_analysis.status` records `fallback`.
- Cover-letter generation already uses the provider chain and remains user-scoped.
- Main AI chat now calls the actual JSON endpoint `/api/ai/chat/`; the frontend no longer depends on nonexistent `/api/ai/chat/stream/` and `/api/ai/models/` routes.
- Added optional system prompt and temperature fields to the existing AI chat API. The system safety/application context remains present.
- AI topic chat now uses the provider fallback chain and returns a clear 502 response when all configured providers fail. The Automation agent planner attempts constrained AI JSON planning and reports `planning_mode=heuristic_fallback` when AI is unavailable; plans are never executed by this endpoint.
- Browser-side cancellation aborts the HTTP request; it cannot guarantee that server-side model processing stops.

### 4. Frontend/API alignment

- Fixed the Jobs source preview endpoint builder.
- Fixed Learning goal pause/resume to call `learning.js` and the `/api/learning/goals/...` endpoints rather than the separate Goals app.
- Added Learning service functions for more of the registered goals, sessions, lessons, resources, progress, assessments, application history, and revision endpoints.
- Added Tasks client helpers for start/cancel/reopen, stats/progress, calendar, overdue tasks, and generation status.
- Replaced the About page's hard-coded `/api/jobs/` request with the existing Jobs service.
- Removed a duplicate OAuth callback hook that called a nonexistent `/api/auth/google/callback/` endpoint; the active callback path continues to consume the tokens returned through the callback route.
- Updated the legacy auth callback file to use the shared API client.
- API telemetry no longer logs request/response bodies, reducing risk of leaking prompts, resumes, API keys, or other personal data.
- Added `frontend_vue/.env.example` with the canonical `VITE_API_BASE_URL=http://127.0.0.1:8000/api` value.

## Changed/new files

Backend:
- `backend_django/ai/providers.py`
- `backend_django/ai/serializers.py`
- `backend_django/ai/services.py`
- `backend_django/ai/views.py`
- `backend_django/jobs_opportunity/default_sources.py`
- `backend_django/jobs_opportunity/models.py`
- `backend_django/jobs_opportunity/serializers.py`
- `backend_django/jobs_opportunity/services.py`
- `backend_django/jobs_opportunity/tasks.py`
- `backend_django/jobs_opportunity/views.py`
- `backend_django/jobs_opportunity/scraper.py`
- `backend_django/jobs_opportunity/signals.py`
- `backend_django/jobs_opportunity/test_rss_parser.py`
- `backend_django/jobs_opportunity/management/commands/bootstrap_job_sources.py`
- `backend_django/jobs_opportunity/migrations/0002_normalize_source_types.py` (new)
- `backend_django/jobs_opportunity/migrations/0003_expand_job_url_length.py` (new)
- `backend_django/scraper/serializers.py`
- `backend_django/scraper/services.py`
- `backend_django/scraper/views.py`
- `backend_django/scraper/tests.py`

Frontend:
- `frontend_vue/.env.example` (new)
- `frontend_vue/src/services/api.js`
- `frontend_vue/src/services/endpoints.js`
- `frontend_vue/src/services/ai.js`
- `frontend_vue/src/services/AIService.js`
- `frontend_vue/src/services/jobs.js`
- `frontend_vue/src/services/learning.js`
- `frontend_vue/src/services/scraperApi.js`
- `frontend_vue/src/services/tasks.js`
- `frontend_vue/src/composables/useAI.js`
- `frontend_vue/src/views/AboutView.vue`
- `frontend_vue/src/views/learning/LearningView.vue`
- `frontend_vue/src/views/jobs/JobsView.vue`
- `frontend_vue/src/views/Scraper/ScraperView.vue`
- `frontend_vue/src/views/Authentication/AuthCallback.vue`
- `frontend_vue/src/views/Authentication/auth-callback.vue`
- `frontend_vue/src/components/AI/AIChat.vue`
- `frontend_vue/src/components/Automation/AIPrompt.vue`

Documentation:
- `API_INTEGRATION_GUIDE.md` (new)
- `API_ENDPOINT_AUDIT.csv` (new)

## Verification actually performed

- Python syntax compilation passed for 19 changed backend Python files after the final edits.
- Node syntax checks passed for the changed JavaScript service/composable files.
- JavaScript syntax checks passed for 8 modified Vue script blocks.
- Focused direct behavior checks passed for Greenhouse-style job normalization, HTML description cleanup, not treating an ID as a URL, relative URL resolution, public job URL filtering, nested JSON-path extraction, and Atom feed parsing.
- Added Django regression tests for unsafe job URLs and nested JSON-path extraction. These tests were not run through Django in this environment.
- `python manage.py check` was attempted and failed immediately with `ModuleNotFoundError: No module named django`. `npm run build` was attempted and failed because `vite` is not installed (`frontend_vue/node_modules` is absent). Therefore Django system checks, migration execution, authenticated API tests, Celery/Redis integration, and the Vite production build remain unverified.
- No live public job source was synced during this execution; source availability must be verified from the user's backend machine after configuration.

## Remaining integration caveats

- `mcpService.js` and `explainsService.js` reference route families that are not included in the root Django URL configuration. The route audit marks these as not wired rather than claiming they work.
- Some routes are present in Django but may not have dedicated UI controls yet. The endpoint audit lists route/action contracts, but payload shapes must be checked against each serializer/view before calling them.
- The project-wide 250-feature roadmap remains partially unverified. Existing files or feature labels are not counted as completed implementation.

## Required final checks in the project environment

Run from `backend_django` after installing `requirements.txt` and configuring a safe local `.env`:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py test jobs_opportunity
python manage.py test scraper
python manage.py test ai
```

Run the frontend checks from `frontend_vue`:

```powershell
npm ci
npm run build
```

For asynchronous source collection, start Redis and the Celery worker using the project's configured broker/result backend. Test one public API or RSS source, verify the Celery task completes, then verify the saved job is visible in `/api/jobs/opportunities/` and in the Jobs UI. Do not run destructive database resets against the user's data.
