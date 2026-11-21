# Documentation Coverage Register

## Scope and source inventory
Evidence is restricted to implementation/configuration under backend_django/ and frontend_vue/. Existing contents in Build/ and project_docs/ are protected and were not used as architectural evidence.

| Inventory | Count | Coverage treatment |
|---|---:|---|
| Installed Django applications | 17 | Each has seven application documents |
| Python files under backend_django | 772 | 50 tests and 59 migrations included in the static catalogs; none executed/applied |
| Python files in installed apps | 764 | Listed in per-app source-file catalogs |
| Project-level Python files outside apps | 8 | Listed in 01-complete-repository-map.md |
| Routed frontend view domains | 18 | Each has seven domain documents |
| JS/Vue/TS files under frontend_vue/src | 203 | Includes five frontend test files |
| SCSS/CSS files under frontend_vue/src | 83 | Included in the shared frontend source catalog |
| Frontend JS/Vue/TS/style files indexed | 286 | Listed in frontend/shared-infrastructure/source-file-catalog.md |
| Additional HTML/Markdown resources | 4 | Path-inventoried; Markdown contents not used as architecture evidence |
| Binary images under frontend_vue/src | 17 | Path-inventoried; content excluded from code-symbol analysis |
| SQLite database artifact | 1 | Excluded; not opened or modified |

Counts are static extension/path counts and do not measure complexity.

## Exact documentation manifest
Project-level (13): 00-master-project-guide.md; 01-complete-repository-map.md; 02-system-component-catalog.md; 03-cross-application-dependencies.md; 04-complete-data-flow.md; 05-complete-api-catalog.md; 06-database-and-model-catalog.md; 07-authentication-and-permissions.md; 08-background-jobs-and-integrations.md; 09-configuration-and-deployment.md; 10-developer-maintenance-guide.md; 11-project-completeness-and-gaps.md; 99-documentation-coverage-register.md.

Backend: for each of ai, automation, challenges, codex, core, goals, jobs_opportunity, knowledge, learning, memory, notification, personal_finance, projects, scraper, social, tasks, users_accounts: README.md, architecture.md, models.md, api.md, services-and-workflows.md, source-file-catalog.md, security-and-testing.md (119 files).

Frontend: for each of accounts, ai, automation, challenges, codex, core, finance, goals, jobs, knowledge, learning, memory, notifications, projects, scraper, shared, social, tasks: README.md, views-and-routes.md, components.md, services-and-api.md, state-management.md, workflows.md, source-file-catalog.md (126 files).

Shared frontend infrastructure (8): router.md; authentication.md; api-clients.md; shared-state.md; layouts-and-common-components.md; plugins-and-ui.md; utilities-and-assets.md; source-file-catalog.md.

**Total: 266 Markdown files**, all under Build/complete_project_documentation/. Existing Build/source_architecture/ documents were neither read nor changed.

## Completion and quality status
| Area | Discovered | Inspected | Documented | Cross-referenced | Independent review | Remaining |
|---|---|---|---|---|---|---|
| Project-level | Yes | Static source inspection | 13/13 | Yes | Pending | API/data catalogs are source indexes, not exhaustive runtime contracts |
| Backend apps | 17/17 | Definition/import/route/field scans plus targeted source review | 119/119 | Yes | Pending | Exact response compatibility, all permission semantics and model constraints need deeper review |
| Backend Python files | 772/772 inventoried: 764 app + 8 project files | Static declarations/import excerpts | 772 listed | Partial | Pending | Callers are not a complete call graph; method behavior needs targeted tracing |
| Frontend domains | 18/18 | Route/import/export/state scans | 126/126 | Yes | Pending | Component contracts and end-to-end flows are not runtime-verified |
| Frontend code/style | 286/286 cataloged | Static import/declaration inventory | Cataloged | Partial | Pending | Consumers/callers are not exhaustive; HTML/Markdown resources and binary images are separate |
| Shared frontend | 8/8 guides | Static source inspection | 8/8 | Yes | Pending | Client consolidation/compatibility remains an engineering decision |

## Evidence and exclusions
- Labels VERIFIED, INFERRED, PARTIAL, UNKNOWN, and NOT IMPLEMENTED distinguish direct code evidence from interpretation or absence within a scoped search.
- No application code was executed; tests, builds, migrations, database operations, and application scripts were not run.
- Generated caches/bytecode, dependency trees, database contents, and binary asset contents are excluded.
- Production runtime, provider availability, workers, database state, and live endpoint behavior remain UNKNOWN.
- Static catalogs can miss dynamic imports/reflection and do not establish reachability. Do not claim runtime success or complete security coverage.


## Independent quality review
A separate read-only reviewer inspected all project-level guides and this register, checked all 17 backend API catalogs and 18 frontend service/API guides at inventory level, and spot-checked representative source paths. The review found and corrected the users_accounts mount (`/api/users/`, from `backend_django/backend_django/urls.py`) and one invalid API-client cross-reference. The review did not verify every handler payload, permission behavior, frontend/backend compatibility, or runtime endpoint execution. No tests, scripts, builds, migrations, or application code were run.

## Remaining interpretation limits
The generated per-application/domain catalogs are static inventories and source navigation aids. Their extracted declarations and relative file entries do not establish complete call graphs, runtime reachability, or end-to-end behavior. API response compatibility, object-level authorization semantics, dynamic imports/reflection, deployment configuration in live environments, and external provider availability remain PARTIAL or UNKNOWN pending targeted source review and runtime validation.