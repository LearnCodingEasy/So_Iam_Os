# Shared Frontend API Clients

## Primary client
**VERIFIED:** frontend_vue/src/services/Shared/api.js creates an Axios instance with base URL VITE_API_BASE_URL or local /api default; attaches bearer tokens; handles refresh/retry; emits sanitized API telemetry; and manages NProgress. frontend_vue/src/services/Shared/endpoints.js contains endpoint builders.

## Parallel request paths
| Path | Source | Difference visible in code |
|---|---|---|
| Main API | services/Shared/api.js | user.access/user.refresh, refresh interceptor, long timeout, API log events |
| Alternate Axios | services/Shared/axiosInstance.js | separate auth_token convention, timeout/error notification |
| Global Axios defaults | src/main.js | VITE_API_URL/VITE_API_BASE_URL or host root; applies to raw Axios use |
| MCP client | services/Shared/mcpService.js | separate Axios configuration and credentials option |
| AI stream | services/AI/AIService.js | fetch stream with token helper, bypasses Axios interceptors |

**INFERRED risk:** This multiplicity can produce different auth, base URL, error, and telemetry behavior. Determine actual consumers before consolidation.

## Integration boundary
Endpoint path declaration is not proof of a corresponding active backend handler or compatible response. For endpoint inventory, use [the complete-project API catalog](../../05-complete-api-catalog.md) and the per-domain services-and-api.md guides. These map declarations to source paths without treating them as runtime proof.

