# Documentation Change Log

## 2026-11-23 — Source-grounded orientation and governance pack

**Input:** supplied `So_Iam_Os_Complete.zip` archive. **Scope:** documentation-only additions under `Build/`; no application source, dependency, migration, database, environment, or user-facing docs files were changed.

### Added

- `Build/PROJECT_MASTER_MAP.md` — single navigation entry point.
- `Build/source_architecture/00_project_overview/CURRENT_SOURCE_BASELINE_2026-11-23.md` — recomputed archive counts and limitations.
- `Build/source_architecture/00_project_overview/PROJECT_FEATURE_REGISTRY.md` — route/API declaration register with conservative evidence statuses.
- `Build/source_architecture/02_backend/APPLICATION_KNOWLEDGE_BASE_INDEX.md` — index for all discovered backend apps and existing docs.
- `Build/source_architecture/04_integration/PROJECT_DEPENDENCY_MAP.md` — URL mounts and model relationship declarations.
- `Build/source_architecture/04_integration/CROSS_APPLICATION_IMPORT_GRAPH.md` — explicit Python cross-app imports.
- `Build/source_architecture/02_backend/APPLICATION_INTERNAL_STRUCTURE_INDEX.md` — per-app folder/file counts.
- `Build/source_architecture/05_catalogues/BACKEND_SOURCE_CATALOGUE.md`.
- `Build/source_architecture/05_catalogues/FRONTEND_SOURCE_CATALOGUE.md`.
- `Build/source_architecture/05_catalogues/DATABASE_MODEL_CATALOGUE.md`.
- `Build/source_architecture/05_catalogues/SHARED_INFRASTRUCTURE_CATALOGUE.md`.
- `Build/source_architecture/EGM_LIVING_CHANGE_WORKFLOW.md`.
- `Build/source_architecture/PROJECT_NEXT_ACTIONS.md`.
- `Build/source_architecture/reviews/GOLDFISH_REVIEW_2026-11-23.md`.
- `Build/source_architecture/01_governance/CURRENT_DOCUMENTATION_MANIFEST_2026-11-23.md`.
- `Build/source_architecture/01_governance/CURRENT_EXECUTION_STATUS_2026-11-23.md`.
- `Build/source_architecture/01_governance/DOCUMENTATION_RECONCILIATION_2026-11-23.md`.
- `Build/source_architecture/02_backend/BACKEND_COVERAGE_AUDIT_2026-11-23.md`.
- `Build/source_architecture/03_frontend/FRONTEND_COVERAGE_AUDIT_2026-11-23.md`.

### Preserved

- Existing documentation, including historical coverage registers, manifests, prior Goldfish review, and app guides, was preserved. This avoids silently rewriting history; the new baseline/master map explicitly supersede stale counts for this archive.
- Application source code and dependencies were not changed.

### Additional correction discovered during second review

- Rechecked `INSTALLED_APPS` using the parsed settings assignment: 25 of 26 app-like directories are registered. `skills/` is an unregistered placeholder package; its guide and current summaries were corrected. The active `Skill` model is in `learning`.

### Verification

- Static inventory and consistency checks only.
- No test, lint, build, migration, database, server, API, browser, or Celery execution is claimed.
- `.git/` and `project_docs/` were not present in the supplied archive.
