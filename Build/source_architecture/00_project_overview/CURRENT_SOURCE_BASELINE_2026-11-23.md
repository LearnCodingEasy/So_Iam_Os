# Current Source Baseline — 2026-11-23

> **Authority:** this report is generated from the supplied archive `So_Iam_Os_Complete.zip`, not from the user's live Windows checkout. It supersedes conflicting historical counts for this archive only. It does not assert runtime correctness.

## Archive scope

- Archive root: `So_Iam_Os/`
- Files present in extracted project tree: **1,702**
- `backend_django/` files: **1,003**
- Python files under backend (including tests and migrations): **996**
- Python files excluding `tests/` and `migrations/`: **836**
- `frontend_vue/` files: **358**
- Vue SFC files (`*.vue`) under frontend: **142**
- Markdown files under `Build/`: **333**
- Markdown files under `Build/complete_project_documentation/`: **267**
- Django app directories containing `apps.py`: **26**
- Local app names in `INSTALLED_APPS`: **25** (the `skills/` package is not registered)

- App-like directory names found: agents, ai, ai_tools_laboratory, analytics, architecture, automation, challenges, codex, core, crm, goals, jobs_opportunity, knowledge, learning, marketing, memory, notification, personal_finance, projects, revenue, sales, scraper, skills, social, tasks, users_accounts
- App URL modules found: **25** (module files, not expanded HTTP operations)
- Literal `path()` / `re_path()` lines in app URL modules: **112** (not a count of resolved endpoint operations)
- Direct `models.Model` subclasses discovered by static AST scan: **164** (heuristic; review abstract/inherited models manually)
- Frontend route declarations extracted: **44**
- Explicit cross-app Python import edges: **58** (static import graph; not runtime call graph)
- Python files successfully parsed with `ast.parse` across the full backend: **996**, with **0 syntax parse failures**. Frontend route extraction is regex-based; nested/dynamic declarations may require manual review.

## Critical archive omissions

- `.git/` is absent: branch, uncommitted changes, and the previously reported modified paths cannot be checked.
- `project_docs/` is absent: the user-facing VuePress site and its links cannot be reconciled.
- No `PROJECT_CONTEXT.json` or `project_manifest.json` was found at the archive root or recursively in the supplied tree.
- Dependencies may not be installed; this report does not claim tests, lint, builds, migrations, server startup, API requests, or browser workflows were executed.

## Counting rules

Counts above are reproducible from file extensions and folder boundaries. They must not be compared directly with older counts unless those documents use the same inclusion/exclusion rules. In particular, total Python count includes tests and migrations; non-test/non-migration count excludes both.

## Local checkout safety

Before applying any future change to `D:\So_Iam_Os`, inspect `git status --short` and preserve all pre-existing changes. Recheck (do not assume) the historical paths `backend_django/db.sqlite3`, `project_docs/docs/.vuepress/.temp/pages/Learn_Django/start_app.html.vue`, and `project_docs/docs/Learn_Django/start_app.md`.

## App directory vs installed app distinction

The repository contains 26 directories with `apps.py`, but only 25 are listed in the literal `INSTALLED_APPS` list. `backend_django/skills/` is not installed, has placeholder files only, and has no app URL include. The `Skill` model used by other apps is defined in `backend_django/learning/models/skill.py`; it is not defined in the `skills/` package. This archive audit does not add the scaffold to `INSTALLED_APPS`.
