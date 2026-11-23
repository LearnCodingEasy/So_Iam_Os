# Backend Coverage Audit — Current Archive Snapshot (2026-11-23)

> This current audit supersedes conflicting counts in the earlier `BACKEND_COVERAGE_AUDIT.md` for the supplied archive. It uses explicit folder/extension rules and does not claim semantic completeness or runtime correctness.

## Summary

- App-like directories containing `apps.py`: **26**.
- Local apps registered in `INSTALLED_APPS`: **25**. Unregistered scaffold: `skills/`.
- Python files inside app directories, including tests/migrations: **988**.
- Python files inside app directories, excluding paths containing `tests` or `migrations`: **828**.
- Python files outside app directories: **8**.
- Total Python files under `backend_django/`: **996**.
- Direct model subclasses (`models.Model`): 164; see `../05_catalogues/DATABASE_MODEL_CATALOGUE.md`.
- App URL module files: 25; literal `path()`/`re_path()` declaration lines in app URL modules: 112. This excludes expanded DRF router operations.
- Python AST parsing: 988 app Python files parsed; zero syntax parse failures. Parsing is not importing Django or running tests.

## App inventory

| App-like directory | Python files (all) | Excluding tests/migrations | In INSTALLED_APPS | Per-app documentation exists | Root API prefix |
|---|---:|---:|---|---|---|
| `agents` | 27 | 21 | Yes | Yes | /api/agents/ |
| `ai` | 93 | 71 | Yes | Yes | /api/ai/ |
| `ai_tools_laboratory` | 26 | 20 | Yes | Yes | /api/ai-tools/ |
| `analytics` | 26 | 20 | Yes | Yes | /api/analytics/ |
| `architecture` | 26 | 20 | Yes | Yes | /api/architecture/ |
| `automation` | 69 | 65 | Yes | Yes | /api/automation/ |
| `challenges` | 25 | 18 | Yes | Yes | /api/challenges/ |
| `codex` | 143 | 131 | Yes | Yes | /api/codex/ |
| `core` | 33 | 27 | Yes | Yes | /api/core/ |
| `crm` | 26 | 20 | Yes | Yes | /api/crm/ |
| `goals` | 23 | 17 | Yes | Yes | /api/goals/ |
| `jobs_opportunity` | 81 | 72 | Yes | Yes | /api/jobs/ |
| `knowledge` | 30 | 24 | Yes | Yes | /api/knowledge/ |
| `learning` | 80 | 75 | Yes | Yes | /api/learning/ |
| `marketing` | 26 | 20 | Yes | Yes | /api/marketing/ |
| `memory` | 15 | 11 | Yes | Yes | /api/memory/ |
| `notification` | 16 | 12 | Yes | Yes | /api/notifications/ |
| `personal_finance` | 61 | 57 | Yes | Yes | /api/finance/ |
| `projects` | 19 | 15 | Yes | Yes | /api/projects/ |
| `revenue` | 26 | 20 | Yes | Yes | /api/revenue/ |
| `sales` | 26 | 20 | Yes | Yes | /api/sales/ |
| `scraper` | 23 | 18 | Yes | Yes | /api/scraper/ |
| `skills` | 7 | 6 | No | Yes | — |
| `social` | 24 | 20 | Yes | Yes | /api/social/ |
| `tasks` | 20 | 15 | Yes | Yes | /api/tasks/ |
| `users_accounts` | 17 | 13 | Yes | Yes | /api/users/ |

## Important exception: `skills/`

`backend_django/skills/` contains `apps.py` but is absent from `INSTALLED_APPS`. It contains placeholder files and no model/API implementation. The `Skill` model referenced by goals, jobs, tasks, and challenges is defined in `backend_django/learning/models/skill.py`. This audit intentionally does not register the scaffold.

## Coverage interpretation

- Documentation presence means an app guide/index exists; it does not mean every file has a meaningful explanation.
- File counts do not establish all business logic, endpoint contracts, permissions, ownership checks, task triggers, or runtime behavior are documented.
- See `APPLICATION_KNOWLEDGE_BASE_INDEX.md`, `APPLICATION_INTERNAL_STRUCTURE_INDEX.md`, `CROSS_APPLICATION_IMPORT_GRAPH.md`, and `PROJECT_DEPENDENCY_MAP.md` for navigation and dependency evidence.

## Remaining gaps

1. Trace every API operation to serializer, view/service, permission/ownership behavior, model, and frontend consumer.
2. Document full model fields, constraints, indexes, inherited fields, and migration state.
3. Trace task enqueue callers, retries, idempotency, scheduling, and failure handling.
4. Run approved runtime verification in a disposable environment; none was performed for this archive audit.