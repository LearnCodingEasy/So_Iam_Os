# AI and Codex Domains

This note covers domain-specific behavior only. Shared system boundaries are in [System Architecture](../01-system-architecture.md), backend structure in [Backend Architecture](../02-backend-architecture.md), frontend structure in [Frontend Architecture](../03-frontend-architecture.md), and security boundaries in [Security and Operations](../06-security-and-operations.md).

## AI domain

**VERIFIED:** `backend_django/ai/models/` defines provider credentials/configuration, settings, prompts, conversations/messages, executions, usage, budgets/reservations, workflows/runs, feedback, and audit records. `backend_django/ai/api/urls.py` declares chat, conversation, provider/configuration, workflow, feedback, usage, and learning/task-related endpoints. Provider adapters are under `backend_django/ai/providers/`; orchestration and accounting logic are under `backend_django/ai/services/`.

**VERIFIED:** The Vue side has AI chat/control/operations views and service modules under `frontend_vue/src/views/ai/` and `frontend_vue/src/services/AI/`. Streaming chat uses fetch and the shared token helper in `AIService.js`.

**PARTIAL:** Provider and async code paths are implemented in source, but live credentials, provider availability, task completion, and end-to-end UX are **UNKNOWN**. `frontend_vue/src/services/AI/aiPlatformService.js` explicitly reports workflow execution as unsupported.

## Codex domain

**VERIFIED:** `backend_django/codex/models/` represents project registries, files, features, API endpoints, snapshots, change sets, policies, protected items, capability definitions/runs, agent runs, audit, and local AI jobs. API declarations are in `backend_django/codex/api/urls.py`; code is grouped in `codex/api/`, `codex/services/`, and `codex/tasks.py`.

The frontend domain is under `frontend_vue/src/views/codex/`, `frontend_vue/src/services/Codex/`, and `frontend_vue/src/stores/codex/`. **PARTIAL:** A capabilities UI component includes mock data; its reachability from the current routed views is **UNKNOWN**.

## Relationship between domains

AI and Codex are distinct: AI focuses on provider-backed conversations and user workflows; Codex models project scanning, context, code intelligence, governance, and local operations. This distinction is **INFERRED** from their models, routes, and service names; runtime coupling is not established here.

## Domain-specific gaps

- **UNKNOWN:** Complete operation-by-operation API request/response compatibility and deployed workspace root behavior.
- **PARTIAL:** AI workflow support is broader in backend routes than the frontend `runWorkflow` service path.
- **INFERRED risk:** Codex local operations and AI credentials warrant careful access-control and secret-handling review; see the shared security document rather than duplicating those controls here.
