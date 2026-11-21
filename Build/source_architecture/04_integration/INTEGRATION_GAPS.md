# Frontend and Backend Integration Gaps

## Scope

This is a static gap register based on the current source inventory and the verified/representative traces in [Frontend/Backend Mapping](FRONTEND_BACKEND_MAPPING.md) and [API Integration Catalogue](API_INTEGRATION_CATALOGUE.md). It does not claim runtime compatibility.

## Confirmed coverage limits

| Area | Current evidence | Gap / status |
|---|---|---|
| Route inventory | 133 literal `path()`/`re_path()` calls and 89 `router.register()` declarations in 18 URL modules | These are declarations, not expanded method/path endpoint operations. `@action` routes and resolver behavior are not exhaustively represented. |
| Frontend consumer mapping | Mapping document contains representative cross-domain traces and one detailed Goals list trace | Exhaustive page-to-component-to-store/service-to-handler mapping remains incomplete. |
| Request and response schemas | Existing API guides and route catalogue identify views and some serializers | Full per-operation payload, validation, error, and response contracts have not been extracted. |
| Authentication and permissions | Source files and existing security documentation are indexed | Endpoint-level effective authentication, object ownership, and permission behavior need handler-by-handler review; runtime enforcement was not tested. |
| Model relationships | 132 model class declarations are counted | Exhaustive fields, relationships, constraints, indexes, managers, signals, and migration history remain incomplete. |
| Unmatched backend routes | Mapping identifies nine installed scaffold apps without an app URL module or frontend consumer, plus a model-only `SavingPlan` | No matching endpoint/consumer was identified in the inspected sources; this does not prove no indirect or dynamically constructed consumer exists. |
| AI workflow | `aiPlatformService.js` marks workflow execution unsupported while backend workflow routes are present | No completed frontend-to-backend workflow execution connection is established. |
| Jobs and Automation | Existing mapping notes identify partial surfaces | Calls and routes require operation-level comparison before declaring them connected or unused. |
| Shared frontend | `shared` is a routed frontend domain with calls spread across the domain mounts | It has no one-to-one backend application mapping. |
| Runtime compatibility | Static source references only | No API calls, browser execution, builds, tests, or runtime permission checks were performed. |

## Mismatch reporting boundary

No URL, HTTP method, request-schema, response-schema, or authentication mismatch is asserted without a direct comparison of the corresponding source declarations. The current evidence is insufficient for an exhaustive mismatch verdict. The detailed Goals list trace is a verified source chain, but response compatibility and successful execution remain unverified.

## Evidence

- `Build/source_architecture/00_project_overview/REPOSITORY_INVENTORY.md` — discovery counts and route-count methodology.
- `Build/source_architecture/04_integration/FRONTEND_BACKEND_MAPPING.md` — representative trace and explicit unmapped/partial areas.
- `Build/source_architecture/04_integration/API_INTEGRATION_CATALOGUE.md` — URL declaration catalogue and scope limitations.
- `Build/source_architecture/02_backend/BACKEND_COVERAGE_AUDIT.md` — unresolved backend contract/model/security work.
- `Build/source_architecture/03_frontend/FRONTEND_COVERAGE_AUDIT.md` — frontend file/domain coverage versus semantic mapping limits.
