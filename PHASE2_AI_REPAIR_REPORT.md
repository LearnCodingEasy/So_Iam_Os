# So_Iam_Os — Phase 2 (in progress): AI repair — backend

Status: **PARTIALLY IMPLEMENTED.** Backend AI repair is done and tested. Not started: AI frontend componentization, Customers app, routing audit, mock/TODO sweep, full frontend build.

## AI — root cause (reproduced, not guessed)
Reproduced through the real `/api/ai/chat/` endpoint using a real local HTTP server emulating Ollama + an OpenAI-compatible API (no adapter mocks). Two defects, each reproduced by a failing test before the fix:

1. **Fallback demoted the primary permanently.** After any fallback, `AIService.chat` (and the stream and topic-chat views) overwrote `conversation.provider/model` with the provider that *answered*. The next message in that conversation then treated the fallback as the preferred provider, so the local/primary AI was never tried again.
2. **Stale model from another provider disabled the primary.** The stored model (`conversation.model` / `AISettings.preferred_model`, e.g. `gpt-4o-mini`) was sent to whichever provider was selected. Ollama answers 404 -> `invalid_request_or_model`; with no cloud credential configured there was nothing to fall back to, so both "failed".

Also found: the provider-selection logic was copy-pasted in 3 views.

## Fix
- `AIService.resolve_selection()`: one place that picks provider/model; a stored model is only used for the provider it was stored with. Used by chat, stream and topic-chat.
- `AIService.should_persist_selection()`: fallback answers no longer overwrite the user's selected primary (the actual provider is still recorded on the message and the execution).
- `generate_completion` / `stream_completion`: a *stored* (non-explicit) model rejected by a provider is dropped once and retried on the same provider with its default model before any fallback. An explicit model chosen in the request is never silently replaced.
- Existing safeguards kept: bounded attempts/retries/deadline, no fallback on auth/quota errors of the preferred provider, no fallback after streaming output started.

## Tests (actual runs, SQLite, placeholder env vars)
- `ai.tests.test_provider_switching_e2e`: 10/10 (healthy local, down->cloud fallback, primary recovers after fallback, stale model, fallback disabled, connection refused, invalid credentials, all-fail bounded with `failed` execution, 2 streaming cases).
- `ai.tests.test_ai_repair_regressions` 16/16, `ai.test_provider_adapters` 2/2, `ai.tests.test_production_architecture` 3/3, `ai.services.tests` 13/13.
- Two pre-existing tests were failing before my changes; both were test defects and were corrected: one asserted "no retry" although network errors are intentionally retried (now asserts no *other* provider is requested); one patched `celery.result.AsyncResult` before Celery finalized.
- A bug I introduced mid-way (infinite loop in `stream_completion`) was caught by the existing regression suite and fixed.
- Regression: `manage.py check` OK (2 pre-existing allauth warnings), `makemigrations --check` no changes, Knowledge 18/18.

## NOT verified
- Real Ollama / OpenAI / Gemini / DeepSeek / OpenRouter calls (no keys or local model here) — `IMPLEMENTED — EXTERNAL TEST PENDING` for real providers; Gemini/DeepSeek/OpenRouter adapters not exercised by e2e.
- Whole-project `manage.py test` still fails at discovery because `ai/` has both `tests.py` and `tests/` (pre-existing; per-module runs work). Dead shadowed files `ai/models.py`, `ai/serializers.py` remain; not deleted yet.
- Frontend AI store/components not yet audited for what they send (provider/model); `AISettings` does not reset `preferred_model` when `preferred_provider` changes (backend now tolerates it).

## Delivery note
ZIP excludes `node_modules`, `__pycache__`, `.git` and `db.sqlite3` (local data).
