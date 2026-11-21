# Project Completeness and Gaps

## Current source assessment
- **VERIFIED:** 17 Django apps are installed and 18 frontend view domains are routed.
- **VERIFIED:** Cross-domain model links connect tasks/goals/learning, learning/knowledge, jobs/learning, projects/goals/tasks, and finance/goals.
- **PARTIAL:** Backend domain APIs are broader than some routed frontend surfaces; exhaustive route-to-handler-to-consumer compatibility is still pending.
- **VERIFIED:** Multiple frontend HTTP paths use differing client/auth conventions (frontend_vue/src/services/Shared/ and AIService.js).
- **VERIFIED:** Mock/unsupported behavior exists in some Codex/Automation UI and AI workflow service paths.
- **UNKNOWN:** Production readiness, endpoint success, worker/provider/socket availability, and deployed database state.

## Priority review areas
1. Audit Codex local filesystem/command operations and Automation desktop/shell operations (backend_django/codex/services/; backend_django/automation/engine_runtime.py).
2. Complete permission/ownership mapping for every API.
3. Trace active frontend services, payload/response shape and error handling.
4. Resolve or label mock, unsupported, and model-only behavior.
5. Validate external/runtime infrastructure separately.

Security review items are not claims of exploitability. Coverage remains incomplete until register statuses and per-app catalogs are complete.

