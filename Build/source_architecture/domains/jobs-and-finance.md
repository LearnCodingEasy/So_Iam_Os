# Jobs and Personal Finance Domains

This note is domain-specific. Shared component boundaries and integration status are in [System Architecture](../01-system-architecture.md) and [API and Integration Map](../04-api-and-integration-map.md); entity ownership is in [Data Architecture](../05-data-architecture.md); shared operational/security concerns are in [Security and Operations](../06-security-and-operations.md).

## Jobs and Opportunities

**VERIFIED:** `backend_django/jobs_opportunity/models/` defines sources, opportunities, requirements, matches, applications/events, resumes, cover letters, interviews, preferences, saved searches, skill gaps, readiness, recommendations, alerts, analytics, and sync runs. Routers are declared in `jobs_opportunity/api/urls.py`; services and background jobs are under `jobs_opportunity/services/` and `jobs_opportunity/tasks.py`. The routed frontend view and service are `frontend_vue/src/views/jobs/JobsView.vue` and `frontend_vue/src/services/Jobs/jobs.js`.

**VERIFIED:** Job skill requirements reference `learning.Skill`, and job skill gaps can reference a learning goal (`jobs_opportunity/models/job_skill_requirement.py`, `job_skill_gap.py`). Job ingestion/fetching code exists; source availability, lawful access, scheduling, and successful sync are **UNKNOWN**.

**PARTIAL:** The routed Jobs view appears to use fewer operations than the backend/service surface. Exact method-by-method UI reachability is not exhaustively mapped here.

## Personal Finance

**VERIFIED:** `backend_django/personal_finance/models/` includes transactions, categories, budgets, debts/payments, savings goals/plans, subscriptions, loans/payments, recurring cashflows, profiles, habits, alerts, and scenarios. Route declarations in `personal_finance/api/urls.py` include resource and reporting/forecast operations; view/service code is under `personal_finance/api/` and `personal_finance/services/`. The frontend view/service are `frontend_vue/src/views/finance/FinanceView.vue` and `frontend_vue/src/services/Finance/finance.js`.

**VERIFIED:** A savings goal may reference a general goal (`personal_finance/models/savings_goal.py`). **NOT IMPLEMENTED:** A SavingPlan API route was not found in the inspected finance URL registrations, although a model exists. No runtime check was performed.

## Domain-specific gaps

- **UNKNOWN:** External job source reachability, provider behavior for AI-assisted job operations, and whether background sync is scheduled in deployment.
- **PARTIAL:** Finance view/service response compatibility is not established by route declarations alone.
- **UNKNOWN:** Whether every model has appropriate user scoping and all model-only resources are intentionally internal.
- **INFERRED recommendation:** Verify user ownership and data-export/deletion behavior for career and financial records; shared controls are in [Security and Operations](../06-security-and-operations.md).
