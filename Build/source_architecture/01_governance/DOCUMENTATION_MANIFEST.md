# Documentation Manifest

## Governance

- **Documentation root:** `Build/source_architecture/`
- **Evidence rule:** Current source/configuration is authoritative; existing documentation is supporting context only and is not silently treated as current.
- **Write policy:** Additive only. Existing documentation is preserved; a filename conflict is a stop condition for that item.
- **Verification policy:** Static inspection only. No tests, builds, migrations, database commands, server starts, API calls, or background tasks are run as part of this audit.
- **Status meanings:** `COMPLETE` means the listed document has been created and inspected; `IN PROGRESS` means work is underway; `PLANNED` means not yet created; `REUSED` means existing documentation is a dependency and is not duplicated; `PARTIAL` means the document states a verified boundary or remaining gap.

## Existing documentation to reuse

| ID | Existing document set | Scope reused | Current limitation |
|---|---|---|---|
| E-01 | `Build/source_architecture/00-project-overview.md` through `07-architecture-gaps-and-roadmap.md` | Existing overview, backend/frontend architecture, integration, data, security, and gap summaries | These docs currently name 17 backend apps and contain representative/partial API and model coverage. Retained unchanged; this audit supplies current-checkout corrections. |
| E-02 | `Build/source_architecture/domains/*.md` | Five cross-domain summaries | Retained unchanged; not a substitute for per-app source catalogues. |
| E-03 | `Build/complete_project_documentation/backend/<app>/*.md` for 17 apps | Existing per-app architecture, model, API, workflow, catalogue, security/test guides | The set omits nine installed local apps and uses an older 772-file backend count. |
| E-04 | `Build/complete_project_documentation/frontend/<domain>/*.md` for 18 domains and `shared-infrastructure/*.md` | Existing domain route/component/state/service guides | Coverage register reports 286 frontend source/style entries; current `frontend_vue/src/` inventory differs and requires reconciliation. |
| E-05 | `Build/complete_project_documentation/00-*.md` through `11-*.md` and `99-documentation-coverage-register.md` | Existing repository map, API/data indexes, operations, and prior quality notes | API and model catalogues explicitly identify themselves as initial/partial inventories. |

## New documentation plan

| ID | Proposed filename | Target directory | Application/domain | Source files covered | Purpose | Depends on | Priority | Creation status |
|---|---|---|---|---|---|---|---|---|
| D-00 | `REPOSITORY_INVENTORY.md` | `00_project_overview/` | Whole repository | `backend_django/backend_django/settings.py`; `backend_django/backend_django/urls.py`; app URL/model/task files; `frontend_vue/src/router/index.js`; existing coverage register | Record current discovery counts, methodology, and gaps | E-01–E-05 | P0 | COMPLETE |
| D-01 | `DOCUMENTATION_MANIFEST.md` | `01_governance/` | Whole repository | Inventory and existing docs | Define additive plan, dependencies, status, and expected volume | D-00, E-01–E-05 | P0 | COMPLETE |
| B-01 | `agents.md` | `02_backend/applications/` | `agents` | `backend_django/agents/**` and settings registration | Document omitted app purpose, files, models, routes, dependencies, and security | D-00, D-01 | P1 | COMPLETE |
| B-02 | `ai_tools_laboratory.md` | `02_backend/applications/` | `ai_tools_laboratory` | `backend_django/ai_tools_laboratory/**` and settings registration | Same per-app source contract for the omitted app | D-00, D-01 | P1 | COMPLETE |
| B-03 | `analytics.md` | `02_backend/applications/` | `analytics` | `backend_django/analytics/**` and settings registration | Same per-app source contract for the omitted app | D-00, D-01 | P1 | COMPLETE |
| B-04 | `architecture.md` | `02_backend/applications/` | `architecture` | `backend_django/architecture/**` and settings registration | Same per-app source contract for the omitted app | D-00, D-01 | P1 | COMPLETE |
| B-05 | `crm.md` | `02_backend/applications/` | `crm` | `backend_django/crm/**` and settings registration | Same per-app source contract for the omitted app | D-00, D-01 | P1 | COMPLETE |
| B-06 | `marketing.md` | `02_backend/applications/` | `marketing` | `backend_django/marketing/**` and settings registration | Same per-app source contract for the omitted app | D-00, D-01 | P1 | COMPLETE |
| B-07 | `revenue.md` | `02_backend/applications/` | `revenue` | `backend_django/revenue/**` and settings registration | Same per-app source contract for the omitted app | D-00, D-01 | P1 | COMPLETE |
| B-08 | `sales.md` | `02_backend/applications/` | `sales` | `backend_django/sales/**` and settings registration | Same per-app source contract for the omitted app | D-00, D-01 | P1 | COMPLETE |
| B-09 | `skills.md` | `02_backend/applications/` | `skills` | `backend_django/skills/**` and settings registration | Same per-app source contract for the omitted app | D-00, D-01 | P1 | COMPLETE |
| B-10 | `BACKEND_COVERAGE_AUDIT.md` | `02_backend/` | Django backend | All `backend_django/**/*.py`, URL modules, app docs | Reconcile all 26 apps, files, models, routes, jobs, tests, and internal dependencies | B-01–B-09, E-03, D-00 | P1 | COMPLETE (PARTIAL findings retained) |
| F-01 | `FRONTEND_COVERAGE_AUDIT.md` | `03_frontend/` | Vue frontend | `frontend_vue/src/**`, router, services, stores, components | Reconcile all 18 routed domains and current file counts against existing guides | E-04, D-00 | P1 | COMPLETE (PARTIAL findings retained) |
| I-01 | `FRONTEND_BACKEND_MAPPING.md` | `04_integration/` | Cross-stack | Vue routes/views/services and Django URL/view/serializer/model sources | Trace verified vertical paths and record unmatched or mismatched operations | B-10, F-01, E-05 | P1 | PLANNED |
| I-02 | `API_INTEGRATION_CATALOGUE.md` | `04_integration/` | API surface | All backend URL modules, viewsets/views, serializers, frontend service calls | Inventory route declarations and verified frontend consumers/contracts | I-01, B-10, F-01 | P1 | PLANNED |
| I-03 | `INTEGRATION_GAPS.md` | `04_integration/` | Cross-stack | Same as I-01/I-02 | List unconsumed routes, unresolved calls, and static mismatch findings with evidence | I-01, I-02 | P2 | PLANNED |
| C-01 | `BACKEND_SOURCE_CATALOGUE.md` | `05_catalogues/` | Backend | All project-owned backend Python files | Searchable file inventory with symbols/responsibility and related docs | B-10, D-00 | P1 | PLANNED |
| C-02 | `FRONTEND_SOURCE_CATALOGUE.md` | `05_catalogues/` | Frontend | All implementation/test/style files under `frontend_vue/src/` | Searchable file inventory linked to existing domain guides | F-01, D-00 | P1 | PLANNED |
| C-03 | `DATABASE_MODEL_CATALOGUE.md` | `05_catalogues/` | Database | All Django model modules and migrations | Index model declarations and link to field/relationship documentation | B-10, E-03 | P1 | PLANNED |
| C-04 | `BACKGROUND_TASK_CATALOGUE.md` | `05_catalogues/` | Async and scheduled work | Celery task modules, settings schedule, management commands, signals | Document task triggers, arguments, outputs, retry behavior, and runtime unknowns | B-10, D-00 | P1 | PLANNED |
| C-05 | `SHARED_INFRASTRUCTURE_CATALOGUE.md` | `05_catalogues/` | Shared infrastructure | Project settings, middleware, auth, ASGI/WSGI, Celery, Vue bootstrap/config, HTTP clients | Index cross-domain infrastructure and configuration | B-10, F-01 | P2 | PLANNED |
| Q-01 | `STATIC_ANALYSIS_LIMITATIONS.md` | `01_governance/` | Whole repository | All statically inspected implementation/configuration | State inspected, inferred, unverified, and runtime-unknown behavior | D-00, B-10, F-01 | P1 | PLANNED |
| Q-02 | `DOCUMENTATION_QUALITY_AUDIT.md` | `06_quality_audit/` | Whole repository | All created docs, existing guides, and cited source | Answer the 16 requested quality questions with status/evidence | All preceding docs | P1 | PLANNED |
| R-01 | `GOLDFISH_INDEPENDENT_REVIEW.md` | `reviews/` | Whole documentation set | Review docs plus selected original sources supplied to an isolated reviewer | Record independent findings and readiness | Q-02 and all preceding docs | P1 | PLANNED |

## Expected documentation volume

The audit reuses 17 existing backend app guides and 18 existing frontend-domain guide sets, plus the existing shared infrastructure and architecture material. It plans 24 new files: one repository inventory, one manifest, nine omitted-app guides, one backend coverage audit, one frontend coverage audit, three integration documents, five catalogues, one static-analysis limitations document, one quality audit, and one independent review report. The source catalogues are expected to represent 1,128 implementation/test/style/script files using the inventory's declared scope. This volume is driven by verified source coverage; it does not imply that each file needs its own Markdown document.

## Conflict and preservation record

Before creation, the planned targets above were checked against `Build/source_architecture/`; none existed. Existing lower-case numbered architecture docs, domain docs, and the 329 existing `Build/` Markdown files are preserved. If any planned target is found to exist at write time, the item must be skipped and reported rather than overwritten.
