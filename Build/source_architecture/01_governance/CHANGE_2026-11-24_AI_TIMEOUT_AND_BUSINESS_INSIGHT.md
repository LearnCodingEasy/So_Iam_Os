# Change record — 2026-11-24 — AI timeout hierarchy + business insight

Verification level: static + stubbed resolver run + read-only inspection of the supplied db.sqlite3.
NOT RUN: Django check/tests, migrations, Celery worker, live Ollama, frontend build (dependencies absent, network off).

## Root cause of "Ollama request timed out"
Evidence (read-only query of shipped db.sqlite3, table ai_aiexecution): 32 executions, 0 succeeded; 4 `timeout`
failures ending at 17–48 s. Code path: `AIService.chat` -> `AIFallbackChainService.generate_completion`
never received the user's `AISettings.timeout_seconds` (saved value was 60). Each attempt was capped by the global
`AI_PROVIDER_TIMEOUT_SECONDS` (35) and the whole chain by `AI_TOTAL_DEADLINE_SECONDS` (60 in settings.py; fallback
default 45), so a cold local model could never finish. Only the streaming path honoured the saved value.
Axios was also fixed at 150–180 s and Celery tasks had no time limits.

## New behaviour
Hierarchy: request -> agent -> provider (OLLAMA_TIMEOUT_SECONDS=120) -> global -> safe default (60s).
Bounds 5..600 s (AI_TIMEOUT_MIN/MAX_SECONDS), validated in `ai/services/timeouts.py`; request input is rejected
(HTTP 400) when out of range, config layers are clamped. Connect timeout stays separate
(AI_PROVIDER_CONNECT_TIMEOUT_SECONDS). Total budget = primary timeout (+30 s fallback window).
Ollama reports connect vs read timeout (`timeout_kind`); API returns 504 with `error_code=timeout`.
Execution metadata records timeout_seconds / timeout_source / elapsed. Token counts from Ollama/OpenAI-style
`raw` are now stored in AIExecution/AIUsageRecord. Celery `generate_learning_plan`: soft/hard limits derived from
MAX, no autoretry on soft-limit; status endpoint adds `state` (queued/running/completed/failed/timeout/cancelled).
Known limitation: a saved AISettings.timeout_seconds equal to 35 (the legacy model default) is treated as "unset".

## New feature
`GET/POST /api/ai/insights/business/` — aggregates the user's real CRM/Sales/Revenue rows, refuses (409) if empty,
otherwise calls the audited AI path with task_type=business_insight. Result is returned with execution_id; it is not
stored in a dedicated table (no migration added).

## Files
Changed: backend_django/settings.py, ai/services/{core,learning_actions}.py, ai/providers/ollama.py,
ai/api/{urls.py,views/ai_views.py,serializers/{conversations,settings}.py}, ai/tasks/ai_tasks.py,
frontend_vue/src/{services/AI/AIService.js,components/ai/AIChat.vue,views/ai/AIChat.vue}, .env.example.
Created: ai/services/{timeouts,business_insights}.py, ai/api/views/business_insight_views.py,
ai/tests/{test_timeouts,test_business_insight}.py. No migrations; nothing deleted.
