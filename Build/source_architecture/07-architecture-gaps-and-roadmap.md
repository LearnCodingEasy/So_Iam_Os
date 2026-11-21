# Architecture Gaps and Prioritized Roadmap

This document separates source-observed gaps from recommendations. Static findings are not runtime defects unless stated as such.

## Priorities

### P0 — Review sensitive execution boundaries

**VERIFIED:** Codex includes local workspace/file operations and command execution (`backend_django/codex/services/execution.py`, `backend_django/codex/services/build_workspace.py`). Automation contains desktop/process operations and a `shell=True` call (`backend_django/automation/engine_runtime.py`).

**INFERRED recommendation:** Perform a dedicated security review of authorization, path containment, command allowlists, user approval, audit records, and isolation before expanding these capabilities. Source inspection alone does not prove exploitable behavior or adequate deployment isolation.

### P1 — Establish consistent API integration

**VERIFIED:** The frontend has a primary Axios client, another configured Axios client, global defaults, and direct fetch usage (`frontend_vue/src/services/Shared/api.js`, `axiosInstance.js`, `mcpService.js`, `frontend_vue/src/main.js`, `frontend_vue/src/services/AI/AIService.js`). Auth keys and error/telemetry behavior differ.

**INFERRED recommendation:** Define and enforce one documented client/auth/error convention, then trace active view → service → endpoint → backend handler → serializer contract. Do not assume the existing endpoint builder is exhaustive or runtime-correct.

### P2 — Close or clearly mark partial user journeys

**VERIFIED:** `frontend_vue/src/services/AI/aiPlatformService.js` marks workflow execution unsupported; a Codex capabilities component contains mock data; `frontend_vue/src/components/automation/Workflow/WorkflowVersions.vue` includes placeholder behavior. `SavingPlan` is a model without a matching URL registration found in `backend_django/personal_finance/api/urls.py`.

**INFERRED recommendation:** Decide whether each path should be completed, hidden, or identified as a placeholder. Verify UI reachability before classifying a component as disconnected.

### P3 — Verify operations and data isolation

**VERIFIED:** Redis, Celery, Channels, providers, and database backends are configured in code (`backend_django/backend_django/settings.py`). Ownership checks appear in multiple app-specific patterns.

**INFERRED recommendation:** Validate deployed configuration and independently audit user isolation for every endpoint and relationship write. This audit did not run services or inspect a production environment.

## Additional observations

- **PARTIAL:** Job and finance APIs are broader than evidence of their active view integrations; map every service method to a current route and payload contract (`frontend_vue/src/services/Jobs/`, `frontend_vue/src/services/Finance/`, corresponding backend APIs).
- **UNKNOWN:** Database migrations' effective compatibility, transaction behavior, provider availability, scheduler operation, and WebSocket deployment are not verified.
- **INFERRED:** A source-backed integration inventory and explicit status labels would reduce confusion between model presence, API declaration, UI integration, and runtime availability.

## Suggested sequence

1. Review security-sensitive Codex and Automation operations.
2. Produce endpoint and ownership coverage matrices.
3. Consolidate frontend client conventions and verify active integration paths.
4. Resolve or label mock, unsupported, and model-only functionality.
5. Validate operational dependencies and deployment behavior in a separate approved environment.

For evidence and boundaries see [API and Integration Map](./04-api-and-integration-map.md), [Data Architecture](./05-data-architecture.md), and [Security and Operations](./06-security-and-operations.md).
