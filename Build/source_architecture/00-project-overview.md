# SO_IAM_OS: Source-Based Project Overview

## Purpose and identity

**VERIFIED:** The frontend labels the application “Personal AI OS” and presents an authenticated dashboard with entry points for goals, projects, learning, knowledge, and an AI assistant. The router also exposes tasks, jobs, finance, memory, social, challenges, Codex, scraping, and automation. Evidence: `frontend_vue/src/components/ai/layout/Sidebar.vue`, `frontend_vue/src/views/shared/HomeView.vue`, `frontend_vue/src/router/index.js`.

**INFERRED:** SO_IAM_OS is a personal productivity and self-management application that groups work, learning, career, finance, and AI tools behind one account. This interpretation is supported by the UI and user-owned models; source code does not establish the owner's complete product vision or a generalized autonomous operating system.

## Implemented capability map

| Capability | Source evidence | Status |
|---|---|---|
| Accounts and user profiles | `backend_django/users_accounts/models/user.py`; `backend_django/users_accounts/api/urls.py`; `frontend_vue/src/services/Accounts/usersAccounts.js` | **VERIFIED** account routes and user model; provider lifecycle is not runtime-verified |
| Goals and tasks | `backend_django/goals/models/`; `backend_django/tasks/models/task.py`; `frontend_vue/src/views/goals/Goals.vue`; `frontend_vue/src/views/tasks/` | **VERIFIED** models, routes, and UI entry points |
| Learning and knowledge | `backend_django/learning/models/`; `backend_django/knowledge/models/`; `frontend_vue/src/views/learning/`; `frontend_vue/src/views/knowledge/` | **VERIFIED** substantial data/API/UI surface |
| Career and finance | `backend_django/jobs_opportunity/models/`; `backend_django/personal_finance/models/`; `frontend_vue/src/views/jobs/`; `frontend_vue/src/views/finance/` | **PARTIAL** broad implementation; end-to-end use is not established |
| AI and project assistance | `backend_django/ai/`; `backend_django/codex/`; `frontend_vue/src/views/ai/`; `frontend_vue/src/views/codex/` | **PARTIAL** broad source implementation; external service/runtime behavior is unknown |
| Desktop/workflow automation | `backend_django/automation/`; `frontend_vue/src/views/automation/` | **PARTIAL** execution paths exist; operating environment and safeguards need further review |

## How a user encounters the product

**VERIFIED:** `/` is an authenticated route, the router initializes the account store, and protected routes redirect unauthenticated users to login. The logged-in application shell renders routed views. Evidence: `frontend_vue/src/router/index.js`, `frontend_vue/src/stores/accounts/user.js`, `frontend_vue/src/App.vue`, `frontend_vue/src/components/ai/layout/AppLayout.vue`.

**INFERRED:** A typical use pattern is to sign in, review the dashboard, and navigate to one or more personal domains. Source code does not prove a required sequence or that every feature is active in a deployed instance.

## Product maturity snapshot

**INFERRED:** The codebase is a broad, modular application foundation with substantial domain models and APIs. Its maturity is uneven: some frontend paths use mock data or explicitly unsupported operations, API client conventions differ, and no runtime or deployment verification was performed. See [Architecture Gaps and Roadmap](./07-architecture-gaps-and-roadmap.md).

## Reading map

- [System Architecture](./01-system-architecture.md)
- [Backend Architecture](./02-backend-architecture.md)
- [Frontend Architecture](./03-frontend-architecture.md)
- [API and Integration Map](./04-api-and-integration-map.md)
- [Data Architecture](./05-data-architecture.md)
- [Security and Operations](./06-security-and-operations.md)
- [Domain documents](./domains/ai-and-codex.md)

All findings are based on static inspection of `backend_django/` and `frontend_vue/`. **UNKNOWN:** live endpoint health, production configuration, provider availability, and actual user workflow completion.
