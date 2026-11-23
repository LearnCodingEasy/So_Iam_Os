# Current Documentation Manifest — 2026-11-23

> This is the current reconciled index for the supplied archive. It supersedes stale status/count claims in the historical `01_governance/DOCUMENTATION_MANIFEST.md` for this archive snapshot only. The historical file is intentionally preserved under the existing additive-only governance policy.

## Authority and policy

- Engineering/architecture source of truth: current source code and configuration.
- Engineering documentation authority: `Build/`.
- User-facing docs site: `project_docs/` (not present in the supplied archive; cannot be reconciled here).
- Change method: EGM workflow in `Build/source_architecture/EGM_LIVING_CHANGE_WORKFLOW.md`.
- No source application code or dependency files were changed in this documentation pass.

## Current archive facts

- Backend app directories: **26**; explicitly present in `INSTALLED_APPS`: **25/26**.
- `Build/` Markdown files: **333**.
- `Build/source_architecture/` Markdown files: **59**.
- `Build/complete_project_documentation/` Markdown files: **267**.
- Full reproducible count definitions and archive omissions: `00_project_overview/CURRENT_SOURCE_BASELINE_2026-11-23.md`.

## Current authoritative entry points

| Artifact | Status | Purpose |
|---|---|---|
| `Build/PROJECT_MASTER_MAP.md` | CURRENT | Single navigation entry point |
| `00_project_overview/CURRENT_SOURCE_BASELINE_2026-11-23.md` | CURRENT | Recomputed source/archive baseline |
| `00_project_overview/PROJECT_FEATURE_REGISTRY.md` | PARTIAL | Route and API mount declaration registry; not runtime verification |
| `02_backend/APPLICATION_KNOWLEDGE_BASE_INDEX.md` | CURRENT INDEX | Maps all 26 app directories (25 installed) to existing guides |
| `02_backend/APPLICATION_INTERNAL_STRUCTURE_INDEX.md` | PARTIAL | Internal folder/file counts per app |
| `02_backend/BACKEND_COVERAGE_AUDIT_2026-11-23.md` | CURRENT SNAPSHOT | Per-app Python counts and installation status |
| `03_frontend/FRONTEND_COVERAGE_AUDIT_2026-11-23.md` | CURRENT SNAPSHOT | Current Vue file and route counts |
| `01_governance/DOCUMENTATION_RECONCILIATION_2026-11-23.md` | CURRENT | Historical/current discrepancy register |
| `05_catalogues/BACKEND_SOURCE_CATALOGUE.md` | PARTIAL | Backend app/source inventory |
| `05_catalogues/FRONTEND_SOURCE_CATALOGUE.md` | PARTIAL | Frontend route/source inventory |
| `05_catalogues/DATABASE_MODEL_CATALOGUE.md` | PARTIAL | Model and ORM relationship declarations |
| `05_catalogues/SHARED_INFRASTRUCTURE_CATALOGUE.md` | PARTIAL | Shared infrastructure file inventory |
| `04_integration/PROJECT_DEPENDENCY_MAP.md` | PARTIAL | Root URL mounts and ORM relation declarations |
| `04_integration/CROSS_APPLICATION_IMPORT_GRAPH.md` | PARTIAL | Explicit Python import dependencies |
| `EGM_LIVING_CHANGE_WORKFLOW.md` | CURRENT PROCESS | Required EGM lifecycle and safety gates |
| `PROJECT_NEXT_ACTIONS.md` | CURRENT BACKLOG | Prioritized unresolved work |
| `DOCUMENTATION_CHANGELOG.md` | CURRENT LOG | Records this documentation pass |
| `reviews/GOLDFISH_REVIEW_2026-11-23.md` | CONDITIONAL ACCEPTANCE | Second-pass static review and open findings |

## Existing documentation retained

- `Build/complete_project_documentation/backend/` contains legacy guides for 17 apps.
- `Build/source_architecture/02_backend/applications/` contains newer summaries for nine additional apps.
- Existing frontend domain guides and shared infrastructure guides remain in `Build/complete_project_documentation/frontend/`.
- Existing high-level architecture docs, prior coverage audits, and prior Goldfish review remain available as historical evidence.

## Known stale or conflicting historical claims

1. Older master/repository guides refer to 17 apps; current source has 26 app-like directories, of which 25 are installed.
2. Older coverage register says 266 Markdown files in `complete_project_documentation`; current archive count is 267.
3. Historical Python/frontend counts use different inclusion rules; use the new baseline's counting definitions.
4. Historical manifest contains planned/completed statuses that do not match the present file tree.
5. Previous frontend counts (286/287/288) differ from direct Vue SFC count; compare only after agreeing on included extensions and paths.

These historical documents were not silently overwritten. The current Master Map and baseline are the starting point; a future dedicated reconciliation can update or archive old statements with owner approval.

## Archive limitations

`.git/`, `project_docs/`, `PROJECT_CONTEXT.json`, and `project_manifest.json` are absent from this supplied ZIP. No live working tree, protected-item list, or VuePress link integrity can be certified from this archive.

## Installed-app exception

`backend_django/skills/` has `apps.py` but is absent from `INSTALLED_APPS`; it is placeholder-only. The active `Skill` model is under `learning`. It is intentionally not activated as part of this documentation pass.
