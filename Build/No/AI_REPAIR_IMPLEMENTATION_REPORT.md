# SO_IAM_OS — AI Repair Implementation Report

## Scope

This update repairs the existing AI execution path and its Vue/Django integration while preserving the existing applications, model definitions, and migration history. `AI_FRONTEND_RULES.md` was reviewed and applied to the frontend changes.

## Implemented

### Backend configuration and providers

- Django now loads the environment-specific file first (`.env.local` or `.env.production`) and falls back to the project-root `.env`; existing process/container environment variables remain authoritative.
- Removed repeated AI reliability setting assignments so each timeout, retry, deadline, and provider-attempt setting has one effective definition.
- Added validation for provider base URLs before outbound requests. Production external providers require HTTPS and cannot target literal private/loopback/link-local IPs; Ollama remains able to use local HTTP endpoints.
- Standardized provider connect/read timeout handling across OpenAI-compatible, Gemini, and Ollama requests.
- Improved Ollama streaming authentication/options/cleanup and OpenAI-compatible stream response cleanup.
- Removed the accidental duplicate provider factory from the Gemini module. `ai.services.providers` is now a backward-compatible export shim to the canonical `ai.providers` implementations.
- Streaming generation now uses the shared provider gateway. It can fall back before the first emitted delta, but will not switch providers after partial output has already reached the client.
- The configured `AISettings.fallback_enabled` preference is now respected by normal and streaming chat. Authentication, quota, or configuration errors from the explicitly selected provider are surfaced instead of silently switching providers.
- New user AI settings inherit `AI_DEFAULT_PROVIDER` once; existing user-selected provider preferences are not overwritten.

### Models, credentials, audit, and observability

- Cleaned `ai.models` exports, removed the service import from model initialization, and exported `AIBudgetReservation` so budget services can import it.
- Aligned execution/audit writes with the actual `AiAuditLog` schema introduced by migration `0014`; execution IDs and result metadata are stored in its `details` JSON field.
- Restored the authenticated `/api/ai/audit/` endpoint used by the frontend and added a serializer exposing a safe result projection.
- Credential upserts now merge provider metadata and preserve an existing encrypted key when the request only updates other settings. Arbitrary metadata keys are not persisted or returned.
- Added the dedicated `AI_CREDENTIAL_ENCRYPTION_KEY` placeholder to `.env.example`.
- Added regression tests for model exports, provider URL validation, fallback policy, streaming fallback, credential metadata preservation, execution audit persistence, and application provider defaults.

### Frontend integration

- Consolidated overlapping provider/settings/health API operations in `aiPlatformService.js` by delegating to the canonical `aiControl.js` service.
- Streaming requests now use the shared JWT refresh/rotation helper rather than bypassing token refresh through raw `fetch` calls. The stream URL also handles a trailing slash in the API base URL.
- Fixed case-sensitive local import paths in `views/Goals/Goals.vue` (`Goals` directory casing), which failed the repository's Linux import check.

## Database findings from the supplied SQLite file

- AI migrations were applied through `0014_aiauditlog`.
- One user preference row selected `openai` and had fallback enabled.
- Three user-scoped encrypted credential records existed: OpenAI, Gemini, and Ollama. Their stored status values were all `invalid`; this is a persisted status, not proof of the current live connectivity state.
- The legacy `AIProviderConfig` table had no records. The active provider path in this codebase is user-scoped `AIProviderCredential` plus `AISettings` and application-level environment fallbacks.
- No credentials or decrypted secret values were read into this report.

## Validation performed

| Check | Result |
|---|---|
| Python source AST validation (`scripts/verify_source.py`) | PASS — 387 Python files parsed |
| Frontend local import validation (`scripts/check_frontend_imports.py`) | PASS |
| Python bytecode compilation (`python -m compileall -q backend_django`) | PASS |
| JavaScript syntax (`node --check` for frontend source `.js`) | PASS |
| Frontend `package.json` and lockfile JSON parsing | PASS |
| Django system check and Django test suite | BLOCKED — Django is not installed in the execution environment |
| Vue/Vite production build | BLOCKED — frontend `node_modules` are not installed (`vite: not found`) |
| Real OpenAI/Gemini/DeepSeek/Ollama connectivity | PENDING — the supplied archive contains `.env.example`, not the user's `.env`; no live API call was made |
| Migration execution / `makemigrations --check` | NOT RUN — Django runtime dependencies are unavailable |

## Preserved intentionally

- Existing migration history `0001`–`0014` was not rewritten. No schema migration was added because the active model schema was aligned to the already-applied `0014` migration.
- The old root-level `models.py` and `serializers.py` files were not deleted. Python resolves the modular `models/` and `serializers/` packages in their place; removing legacy files without a full Django import/test run would be unsafe.
- The legacy `AIProviderConfig` model/table was retained for backward compatibility, although no rows were present and the active service path does not use it.

## Remaining blockers / follow-up

1. Install backend dependencies from `requirements.txt`, then run `python manage.py check`, `python manage.py makemigrations --check --dry-run`, migrations against a disposable test database, and the full Django test suite.
2. Run `npm ci` in `frontend_vue/`, then run the Vitest suite and `npm run build`.
3. Supply the local `.env` outside the archive and perform real authenticated provider tests. The stored credential records currently report `invalid`, so each provider must be retested; do not manually change their status to `valid`.
4. Workflow execution remains intentionally unavailable in the existing frontend service (`runWorkflow` throws and the UI marks execution disabled); this update did not invent a workflow execution endpoint.
5. The literal-IP URL validation is a defensive baseline, not complete DNS-rebinding protection. Production deployments should additionally enforce outbound network egress policies or a strict provider-host allowlist.

## Delivery hygiene

The release ZIP excludes `.env` files (except safe examples), SQLite runtime data containing user records/encrypted credentials, uploaded media, Python bytecode/cache directories, `node_modules`, and build artifacts. The full source tree, lockfiles, migrations, tests, and documentation are retained.
