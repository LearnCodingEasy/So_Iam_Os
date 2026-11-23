# Backend Coverage Audit

## Scope and method

This audit cross-checks source paths under `backend_django/` against the current source tree and existing documentation. Each `.py` file is counted, including tests and migration package files. `__pycache__`, bytecode, media, and non-source assets are excluded. For the 17 already-documented apps, every Python path was checked for presence in that app's `source-file-catalog.md`; the path match is a catalogue check, not proof every behavior is fully explained. Nine additional app directories are covered by the new per-app documents in `applications/`; eight are installed, while `skills/` is an unregistered scaffold.

The project-level count is eight Python files outside local app directories. All eight are named with a purpose in `Build/complete_project_documentation/01-complete-repository-map.md`. The previous coverage register's count of eight project-level Python files is current, while its total backend Python count and installed-app count are stale.

## Coverage matrix

| Application | Source files | Documented | Missing | Status |
|---|---:|---:|---:|---|
| `agents` | 7 | 7 | 0 | PARTIAL — scaffold documented; no implemented domain behavior found |
| `ai` | 93 | 93 | 0 | PARTIAL — all Python paths listed in existing catalogue; route contracts and runtime behavior remain incomplete |
| `ai_tools_laboratory` | 7 | 7 | 0 | PARTIAL — scaffold documented; no implemented domain behavior found |
| `analytics` | 7 | 7 | 0 | PARTIAL — scaffold documented; no implemented domain behavior found |
| `architecture` | 7 | 7 | 0 | PARTIAL — scaffold documented; no implemented domain behavior found |
| `automation` | 69 | 69 | 0 | PARTIAL — all Python paths listed; sensitive runtime effects and complete route contracts need deeper review |
| `challenges` | 18 | 18 | 0 | PARTIAL — all Python paths listed; exhaustive endpoint contracts not verified |
| `codex` | 143 | 143 | 0 | PARTIAL — all Python paths listed; command/file execution permissions need deeper review |
| `core` | 32 | 32 | 0 | PARTIAL — all Python paths listed; cross-app event behavior needs deeper review |
| `crm` | 7 | 7 | 0 | PARTIAL — scaffold documented; no implemented domain behavior found |
| `goals` | 23 | 23 | 0 | PARTIAL — all Python paths listed; route contracts are not all traced to consumers |
| `jobs_opportunity` | 81 | 81 | 0 | PARTIAL — all Python paths listed; external fetch/schedule runtime not verified |
| `knowledge` | 30 | 30 | 0 | PARTIAL — all Python paths listed; file storage/extraction runtime not verified |
| `learning` | 80 | 80 | 0 | PARTIAL — all Python paths listed; complete endpoint permissions and response contracts remain open |
| `marketing` | 7 | 7 | 0 | PARTIAL — scaffold documented; no implemented domain behavior found |
| `memory` | 15 | 15 | 0 | PARTIAL — all Python paths listed; exhaustive API/permission review remains open |
| `notification` | 16 | 16 | 0 | PARTIAL — all Python paths listed; delivery/runtime behavior is not established |
| `personal_finance` | 61 | 61 | 0 | PARTIAL — all Python paths listed; all model/API mapping still needs detailed reconciliation |
| `projects` | 19 | 19 | 0 | PARTIAL — all Python paths listed; exhaustive contract compatibility is not verified |
| `revenue` | 7 | 7 | 0 | PARTIAL — scaffold documented; no implemented domain behavior found |
| `sales` | 7 | 7 | 0 | PARTIAL — scaffold documented; no implemented domain behavior found |
| `scraper` | 23 | 23 | 0 | PARTIAL — all Python paths listed; external scraping behavior is not runtime-verified |
| `skills` | 7 | 7 | 0 | PARTIAL — scaffold documented; no implemented domain behavior found |
| `social` | 24 | 24 | 0 | PARTIAL — all Python paths listed; exhaustive endpoint permissions remain open |
| `tasks` | 20 | 20 | 0 | PARTIAL — all Python paths listed; async generation/schedule behavior is not runtime-verified |
| `users_accounts` | 17 | 17 | 0 | PARTIAL — all Python paths listed; provider callback and endpoint authorization need runtime/source review |
| **App subtotal** | **827** | **827** | **0** | **PARTIAL** — path coverage complete; behavioral and contract coverage is not complete |
| Django project/scripts outside apps | 8 | 8 | 0 | PARTIAL — path/purpose index exists in the repository map; detailed file contracts are not all repeated here |
| **Backend total** | **835** | **835** | **0** | **PARTIAL** — all Python source paths are represented; full semantic/API/security/runtime audit is not complete |

## Counts and findings

- **App-like directories with `apps.py`:** 26. **Installed local Django applications:** 25. The `skills/` package is not listed in `INSTALLED_APPS` and contains placeholder scaffolding only. Third-party entries in `INSTALLED_APPS` are excluded from this local-app denominator.
- **Python source-path representation:** 835/835 (100%) when existing per-app catalogues, the project-level repository map, and the nine new app guides are considered together. This is path presence only.
- **Existing app catalogue cross-check:** 764/764 Python paths across the original 17 documented apps appear in their respective source-file catalogues.
- **New app source files:** 63 files across nine apps, seven Python files each. Each app contains `__init__.py`, `admin.py`, `apps.py`, `models.py`, `tests.py`, `views.py`, and `migrations/__init__.py`; all are represented in its new guide.
- **Django model declarations:** 132 declarations in model modules. The field-by-field model catalogue remains planned and this count does not prove migration/database schema state.
- **URL declaration inventory:** 18 URL modules contain 133 literal `path()`/`re_path()` calls and 89 DRF `router.register()` calls. These are declarations, not fully expanded HTTP method/path operations.
- **Celery task declarations:** 11 `@shared_task` functions were found. Their existence does not establish a running worker or scheduler.

## Unresolved backend coverage

1. Complete route-by-route method, path, view, serializer, auth, permission, validation, request/response, error, model, and frontend consumer mapping for all URL declarations.
2. Exhaustive field, relationship, constraint, index, manager, signal, and migration-history inventory for all 132 model declarations.
3. Endpoint-level object-ownership and permission review across every handler.
4. Full task trigger/input/output/retry/schedule and failure-path analysis, including non-Celery management commands and signal-triggered behavior.
5. Runtime confirmation of route resolution, database schema, task workers, broker, and integrations; none was attempted in this static audit.

The `PARTIAL` statuses are intentional: file-path coverage is complete, but the requested business/API/security semantics are not fully audited by path catalogues alone.
