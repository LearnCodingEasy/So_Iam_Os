# Repository Inventory

> **Historical checkpoint (2026-11-21):** counts in this file are preserved as the earlier audit snapshot. For the 2026-11-23 supplied archive, use `CURRENT_SOURCE_BASELINE_2026-11-23.md` and `DOCUMENTATION_RECONCILIATION_2026-11-23.md`; in particular, 26 app-like directories exist but only 25 are registered in `INSTALLED_APPS`.


**Audit type:** Static repository discovery  
**Repository:** `D:\So_Iam_Os`  
**Discovery date:** 2026-11-21

## Scope and counting method

Counts below come from the current source tree, not from the prior documentation register. Project source was counted in `backend_django/`, `frontend_vue/src/`, and root `scripts/`. The backend count includes Python migrations and test source because both are project-owned Python files; neither was executed. The frontend count includes JavaScript, TypeScript, Vue, CSS, SCSS, and HTML source beneath `frontend_vue/src/`. The six root scripts are included. Dependency trees, virtual environments, Git metadata, bytecode/cache directories, build output, media, databases, binary assets, and Markdown are excluded from the source-file total.

The API count is a **route declaration inventory**, not an expansion into every HTTP method and generated DRF router URL. It counts literal `path()`/`re_path()` calls and `router.register()` calls in backend URL modules. Dynamic router actions and methods require separate extraction to compute concrete method/path operations.

## Discovered counts

| Inventory item | Count | Method and qualification |
|---|---:|---|
| Local Django applications | 26 | Distinct directories with `apps.py`; 25 of 26 are listed in `backend_django/backend_django/settings.py` `INSTALLED_APPS`. The `skills/` package is an unregistered placeholder scaffold. This excludes third-party Django apps. |
| Routed Vue domains | 18 | Feature routes/domains declared in `frontend_vue/src/router/index.js`; names are not inferred from directory names alone. |
| Project source files | 1,128 | 835 backend `.py` files + 287 frontend source/style files + 6 root scripts, using the scope above. |
| Important configuration and routing files | 61 | 26 `apps.py` + 18 backend URL modules + 4 Django project runtime files (`settings.py`, `asgi.py`, `wsgi.py`, `celery.py`) + `automation/celery.py` + 7 frontend manifest/config files + root `requirements.txt` + 4 environment templates/overlays. This is a declared audit set, not every file containing a setting. |
| Model class declarations | 132 | Classes found in Django `models.py` and `models/` modules with model base classes. This does not establish database tables currently present. |
| URL declarations | 222 | 133 `path()`/`re_path()` calls + 89 `router.register()` calls across 18 `urls.py` files. Router expansion, `@action` routes, and effective resolver behavior are not included in this number. |
| Vue single-file components | 134 | `.vue` files under `frontend_vue/src/`. |
| Frontend service-layer files | 32 | JavaScript/TypeScript files in `frontend_vue/src/services/`; the directory also contains helpers and test material, so this is not a count of unique backend API consumers. |
| Celery task definitions | 11 | Functions decorated with `@shared_task` in backend source. Scheduling declarations and management commands are inventoried separately. |
| Existing Markdown under `Build/` | 329 | Recursive file count before this audit's additions. |
| Existing Markdown under `Build/source_architecture/` | 13 | Eight root documents and five domain documents. |
| Existing Markdown across repository | 411 | Markdown files excluding `.git`, `venv`, and `node_modules`; includes generated/vendor-independent project documentation outside `Build/`. |

## Applications and domains

The 26 local Django app configurations are: `agents`, `ai`, `ai_tools_laboratory`, `analytics`, `architecture`, `automation`, `challenges`, `codex`, `core`, `crm`, `goals`, `jobs_opportunity`, `knowledge`, `learning`, `marketing`, `memory`, `notification`, `personal_finance`, `projects`, `revenue`, `sales`, `scraper`, `skills`, `social`, `tasks`, and `users_accounts`.

The 18 routed frontend domains are: `accounts`, `ai`, `automation`, `challenges`, `codex`, `core`, `finance`, `goals`, `jobs`, `knowledge`, `learning`, `memory`, `notifications`, `projects`, `scraper`, `shared`, `social`, and `tasks`.

## Existing documentation and gaps

The repository has 329 Markdown files under `Build/`, including 266 files under `Build/complete_project_documentation/` according to its own manifest and additional project reports. `Build/source_architecture/` already has 13 documents. These files were preserved and used as existing inputs; none was overwritten.

The prior coverage register at `Build/complete_project_documentation/99-documentation-coverage-register.md` lists 17 backend apps and 772 backend Python files. Current source discovery finds 26 app-like directories (25 installed) and 836 Python files excluding tests and migrations under the current counting rule. Its 17 backend per-application document folders omit the nine additional app directories `agents`, `ai_tools_laboratory`, `analytics`, `architecture`, `crm`, `marketing`, `revenue`, `sales`, and `skills`; eight are installed and `skills` is an unregistered scaffold. The existing source-architecture overview likewise describes 17 apps. These prior counts are therefore historical/stale relative to this checkout.

The existing API catalog identifies itself as an initial route inventory and says route methods, handler/serializer details, permission behavior, request/response contracts, and frontend consumers still need per-route review. Existing integration maps provide representative traces, not exhaustive endpoint-to-consumer matching. Existing model catalog describes model families and explicitly leaves field-level schema, constraints, and all relationships incomplete. Existing source catalog claims require reconciliation against the 63-file increase in backend Python sources and the current frontend source count.

## Discovery limitations

- Static declarations do not prove that routes resolve, requests succeed, or all UI paths are reachable.
- Installed-app registration does not prove a deployment has loaded or migrated the app.
- Model-class counts do not prove migration state or live database schema.
- Task declarations and schedules do not prove a worker or scheduler is running.
- No tests, builds, migrations, scripts, API calls, database operations, or background tasks were run.
- Environment values were not used to establish runtime configuration.

## Evidence index

- Django app registration and backend settings: `backend_django/backend_django/settings.py`.
- Project route composition: `backend_django/backend_django/urls.py` and app `api/urls.py` modules.
- Vue route declarations: `frontend_vue/src/router/index.js`.
- Existing coverage register: `Build/complete_project_documentation/99-documentation-coverage-register.md`.
- Existing API and model indexes: `Build/complete_project_documentation/05-complete-api-catalog.md` and `06-database-and-model-catalog.md`.
