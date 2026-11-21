# Automation and Scraper Domains

This note documents only these domains' source-visible behavior. Shared component architecture is in [System Architecture](../01-system-architecture.md); backend/frontend organization is in [Backend Architecture](../02-backend-architecture.md) and [Frontend Architecture](../03-frontend-architecture.md); execution risk is in [Security and Operations](../06-security-and-operations.md).

## Automation

**VERIFIED:** `backend_django/automation/models/` defines programs/elements, workflows/nodes/edges, actions, tasks/task runs, screen states, and delays. `automation/api/urls.py` registers these resources; execution paths are in `automation/workflow_runner.py`, `automation/engine_runtime.py`, `automation/engine/`, and `automation/tasks.py`. The Vue feature includes automation views and service modules under `frontend_vue/src/views/automation/` and `frontend_vue/src/services/Automation/`.

The implementation includes desktop/window interaction, keyboard/mouse input, screenshots, and execution logs (`automation/engine_runtime.py`, `automation/services/screenshot.py`, `automation/workflow_runner.py`). **PARTIAL:** Source presence does not establish supported operating systems, safe execution isolation, or successful live workflow runs.

The automation permission policy declares default categories in `backend_django/automation/permission_policy.py`. Actual enforcement must be checked at each execution path; the policy declaration alone does not prove complete enforcement.

## Scraper

**VERIFIED:** `backend_django/scraper/models/` defines websites, selectors, scraping configurations/jobs, and scraped data. API routes/views are in `scraper/api/`; task code is in `scraper/tasks.py`. The routed frontend surface is `frontend_vue/src/views/scraper/ScraperView.vue` and `frontend_vue/src/services/Scraper/`.

**UNKNOWN:** Site-specific compatibility, external site availability, scheduling, and production data quality were not runtime-tested.

## Domain-specific gaps

- **VERIFIED review item:** `automation/engine_runtime.py` contains a `shell=True` process call. This warrants focused security review, but is not by itself proof of exploitability.
- **PARTIAL:** Workflow-version UI contains placeholder/mock behavior (`frontend_vue/src/components/automation/Workflow/WorkflowVersions.vue`). Its use in the active route is not established here.
- **UNKNOWN:** Whether permission prompts/policies cover every desktop, filesystem, network, and shell operation.
- **INFERRED recommendation:** Treat automation and scraping as privileged side-effect boundaries; confirm ownership, authorization, safe URL handling, logs, and deployment isolation. See [Security and Operations](../06-security-and-operations.md).
