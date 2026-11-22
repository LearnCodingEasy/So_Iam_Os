# So_Iam_Os implementation checklist

Updated: 2026-11-22

This checklist records work completed in the current engineering mission. Existing
changes are preserved; in particular, `backend_django/db.sqlite3` was already
modified before this mission and is not to be overwritten.

## P0 — Preserve and understand the current project

- [x] Read `Build/No/Project_structure.md` and inspect the repository layout.
- [x] Record the initial Git state (`backend_django/db.sqlite3` already modified).
- [x] Confirm all 25 Django apps are listed in settings.
- [x] Finish the per-application responsibility and integration map in `Build/source_architecture/08_APPLICATION_INTEGRATION_MAP.md`.
- [x] Record the baseline findings and continue with safe implementation.

## P1 — Repair existing integration defects

- [x] Run Django check, migration consistency, and migration plan commands.
- [x] Run frontend unit tests and production build.
- [x] Verify the priority-app frontend-to-backend API contracts and mounted routes.
- [x] Implement and verify the initial auth, settings, and challenge ownership repairs.

## P2–P9 — Complete the integrated platform

- [ ] Complete application ownership, API, and dependency contracts (eight priority apps remain scaffold-only; define product ownership before adding domain code).
- [ ] Integrate AI engineering workflow and centralized agent management.
- [ ] Evaluate and implement provider routing, local model support, and usage tracking.
- [ ] Evaluate MCP and orchestration integrations against least privilege.
- [ ] Extend existing Knowledge models and services for justified retrieval needs.
- [ ] Complete automation, analytics, marketing, CRM, sales, and revenue integration.
- [ ] Complete security review, documentation, and production verification.
- [ ] Create and verify `So_Iam_Os_Complete.zip` without packaging private data.

## Current findings and blockers

- The system Python initially had no Django; the repository `venv` contains Django.
- Django settings contained Windows console-incompatible import-time Unicode
  prints; these were removed so management commands run in the local shell.
- The configured social adapter module was missing. Added
  `users_accounts/adapter.py` to map provider identity data to the custom user's
  required `name` and optional `surname` fields. Email is now required in allauth
  signup configuration, and the deprecated email-required setting was removed.
- Django check passes with no issues. `makemigrations --check --dry-run` reports
  no changes, and `migrate --plan` reports no planned operations.
- `users_accounts.tests.test_users_accounts`: 2 tests pass.
- Frontend Vitest: 5 files and 13 tests pass. Production build succeeds, with
  existing CSS pseudo-selector warnings and large bundle warnings.
- Full Django test run was interrupted after more than six minutes with no output
  in the earlier attempt. A focused run of challenge ownership and local AI
  provider switching completed: 13 tests passed in 23.9 seconds. The provider
  tests use a local loopback server and were not the stall source.
- Retried the full suite with `--verbosity 2`: all 154 tests completed in 160.3
  seconds, with 2 errors in XPath scraper tests because `lxml` is absent from the
  active virtualenv. The root `requirements.txt` already declares `lxml>=6,<7`.
  Django reported no system-check issues; migrations ran against a shared
  in-memory SQLite test database and the test database was destroyed normally.
- No lock or background task caused the observed slowdown. Migration setup took
  roughly 40 seconds, and per-test database setup accounts for much of the
  remaining runtime. The exact reason the earlier process made no output for
  six minutes is not established; this retry demonstrates the suite can progress
  and terminate under verbosity 2.
- Git safety review: latest commit `1588f9c` changed the tracked SQLite database
  binary and included it in the commit. The current working tree has no database
  diff. The remaining modifications and untracked map are preserved working-tree
  changes; no reset, cleanup, revert, or history rewrite was performed. Git
  evidence cannot establish whether any pre-checkout uncommitted changes were
  overwritten, but there is no evidence of that in the current diff.
- `backend_django/backend_django/urls.py` mounts AI and core APIs. Several
  priority apps have only scaffold files and no API URL modules. Confirm app
  ownership and behavior before building those contracts.
- No migrations will be applied during this work without a reviewed plan.

## Stage 2 progress

- [x] Inspect status, recent history, HEAD summary/diff, and tracked database state.
- [x] Record the committed database change and current working-tree safety state.
- [x] Map all nine priority apps, including ownership, APIs, permissions, tests,
  routes, frontend consumers, and missing integrations.
- [x] Trace the suite stall with focused and full diagnostic runs.
- [ ] Resolve the missing local `lxml` dependency, then rerun the two XPath tests
  and full suite.
- [ ] Continue approved backend and frontend integrations in small slices.
