# So_Iam_Os — Restructure Report (Phase 1: Knowledge)

Status: **IN PROGRESS — 1 of 17 Django apps restructured.** Not the final deliverable.

## App inventory (discovered, not assumed)
INSTALLED_APPS contains **17** project apps, not 18. `backend_django/users/` is only a media folder (avatars/covers), with no Python and no app. Tell me if you meant another app.

| # | App | Frontend | Backend | Imports updated | Tests |
|---|-----|----------|---------|-----------------|-------|
| 1 | knowledge | DONE (service moved to `services/Knowledge/Knowledge.js`, view renamed `knowledgeView.vue`) | DONE (models/api/services/validators/extractors/tasks/tests) | DONE (verified by build + check) | Backend 18/18 OK; Frontend 11/11 OK |
| 2-17 | ai, automation, challenges, codex, core, goals, jobs_opportunity, learning, memory, notification, personal_finance, projects, scraper, social, tasks, users_accounts | NOT STARTED | NOT STARTED | NOT STARTED | NOT RUN (baseline only) |

## Knowledge: what changed
- Backend: `models.py` -> `models/` (2 entities); `views.py`/`serializers.py`/`urls.py` -> `api/`; `services.py` split into `KnowledgeService` + `KnowledgeFileService` (all 10 methods preserved); `file_validation.py` -> `validators/`; `metadata.py` + `_extract_text` -> `extractors/`; `tasks.py` -> `tasks/`; tests -> `tests/`.
- Proof nothing was lost: AST comparison of every original class/function vs new modules. Only intended edits differ (import paths, `add_file` call site, `extract_text` rename, task decorator).
- Celery task keeps its legacy name `knowledge.tasks.process_knowledge_file` so queued jobs stay valid.
- Migrations untouched; `makemigrations --check` reports no changes. No model, field, API route or URL path changed.
- External references updated: `backend_django/urls.py`, `learning/serializers.py`.

## Counts (Knowledge phase, from git, renames detected)
Moved/renamed: 13 | Modified: 7 | New: 15 | Deleted: 1 (`knowledge/tests.py`, an empty Django stub with only a comment; replaced by `tests/`).

## Defects found and fixed
1. **Restore button could never work**: `POST /items/{id}/restore/` returned 404 for archived items because the queryset hides archived rows and the frontend sends no `include_archived`. Fixed for the `restore` action only; covered by a test.
2. **Frontend build failed on Linux/CI**: views import `AI/AI.scss` but the file was `Ai.scss` (works only on case-insensitive Windows). Renamed to match.
3. Added 9 API integration tests (auth, owner isolation, archive/restore, extract-metadata, upload validation, task name).

## Defects found, NOT fixed (outside Knowledge)
- `ai/` has both `tests.py` and a `tests/` package, so `manage.py test` (whole project) fails at discovery. Per-app runs work.
- `vite build` compiles, then **exits 1**: the PWA plugin rejects a single 6.5 MB main chunk (limit 2 MiB) because `router/index.js` statically imports most views. Real fix = lazy route imports (router work, planned for a later phase). Raising the workbox limit would only hide it.
- `automation` imports Windows-only modules (`pywinauto`, `win32com`) at module level, so it cannot even be imported on Linux. I stubbed them for testing only (outside the project).
- Frontend `views/knowledge/knowledgeView.vue` follows your spec's casing, but folder casing across `src/` is inconsistent (`AI/`, `knowledge/`, `Knowledge/`). That inconsistency caused defect #2; a casing convention should be decided before the other apps.
- `db.sqlite3` is inside the uploaded project and I left it in; remove it before sharing if it holds real data.

## Verification actually run
- `manage.py check`: OK (2 pre-existing allauth deprecation warnings). `makemigrations --check`: no changes.
- `manage.py test knowledge`: 18 tests, OK.
- `vitest run`: 5 files / 11 tests OK. oxlint on Knowledge frontend: 0 warnings, 0 errors.
- Vue<->Django contract: all 12 Knowledge endpoints used by the frontend exist in the backend with matching methods.
- NOT run: browser/UI click-through, real Celery worker, PostgreSQL, other 16 apps' tests (baseline per-app run timed out in this sandbox; `challenges` = 0 tests).
- Test env: placeholder env vars from `.env.example`, Windows-only modules stubbed, SQLite. No secrets used.

## Remaining plan (same method per app: split by script, AST-verify, check, test, commit)
Order by risk: small apps first (challenges, memory, projects, notification) -> medium (goals, tasks, personal_finance, scraper, social, users_accounts) -> large (core, codex, jobs_opportunity, knowledge-linked learning, automation, ai). `learning` (8.2k LOC) and `ai` (7.1k LOC) need their own sessions.
