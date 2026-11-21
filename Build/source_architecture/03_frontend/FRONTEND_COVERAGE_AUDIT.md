# Frontend Coverage Audit

## Scope and method

The routed-domain denominator comes from route records in `frontend_vue/src/router/index.js`; domain names are not inferred solely from folders. The current source-file count covers JavaScript, JSX, TypeScript, Vue SFC, MJS/CJS, CSS, SCSS, HTML, SQL, shell, and PowerShell files under `frontend_vue/src/`, excluding dependencies, caches, and build output. A path-presence scan compared all discovered files to the 18 domain source catalogues plus `shared-infrastructure/source-file-catalog.md`.

## Domain coverage matrix

The source-file count below covers files under each domain's `views/`, `components/`, `stores/`, and mapped `services/` directory. Shared infrastructure, composables, router, plugins, utilities, and assets are covered by the repository-wide frontend catalogue, not assigned to a feature domain. Four test/resource files are absent from their feature-specific catalogues but appear in the shared catalogue.

| Routed domain | Domain-owned source files | Listed in its domain catalogue | Missing from domain catalogue | Status |
|---|---:|---:|---:|---|
| `accounts` | 9 | 9 | 0 | PASS — source paths represented |
| `ai` | 24 | 23 | 1 | PARTIAL — `services/AI/__tests__/AIService.spec.js` is listed in shared catalogue |
| `automation` | 33 | 33 | 0 | PASS — source paths represented |
| `challenges` | 2 | 2 | 0 | PASS — source paths represented |
| `codex` | 24 | 24 | 0 | PASS — source paths represented |
| `core` | 6 | 6 | 0 | PASS — source paths represented |
| `finance` | 22 | 21 | 1 | PARTIAL — `views/finance/test.html` is listed in shared catalogue |
| `goals` | 7 | 6 | 1 | PARTIAL — `stores/goals/__tests__/goalsStore.spec.js` is listed in shared catalogue |
| `jobs` | 2 | 2 | 0 | PASS — source paths represented |
| `knowledge` | 7 | 6 | 1 | PARTIAL — `stores/knowledge/__tests__/knowledgeStore.spec.js` is listed in shared catalogue |
| `learning` | 7 | 7 | 0 | PASS — source paths represented |
| `memory` | 2 | 2 | 0 | PASS — source paths represented |
| `notifications` | 2 | 2 | 0 | PASS — source paths represented |
| `projects` | 3 | 3 | 0 | PASS — source paths represented |
| `scraper` | 2 | 2 | 0 | PASS — source paths represented |
| `shared` | 25 | 25 | 0 | PASS — source paths represented |
| `social` | 2 | 2 | 0 | PASS — source paths represented |
| `tasks` | 4 | 4 | 0 | PASS — source paths represented |
| **Domain-owned subtotal** | **183** | **179** | **4** | **PARTIAL** — four paths are only in shared catalogue |

## Frontend-wide counts

- **Routed domains:** 18/18 have existing per-domain documentation sets (100% by domain count).
- **Vue SFCs:** 134 `.vue` files under `frontend_vue/src/`.
- **Frontend source/style files:** 288 under the defined extension/scope method. The existing complete-documentation register says 286; the summary count is stale by two files relative to this checkout.
- **Source path representation:** 288/288 discovered paths appear in the existing feature or shared source-file catalogues (100% by path-presence check). This does not measure explanation depth or runtime behavior.
- **Frontend service-layer files:** 32 JavaScript/TypeScript files were found under `frontend_vue/src/services/`; this includes helpers and test-related code and is not an API endpoint count.
- **Domain file counts:** the 183 domain-owned files above are directory-ownership counts, not numbers of components or API calls.

## Source-grounded architecture notes

- Vue startup/plugin installation is in `frontend_vue/src/main.js`; route declarations and guards are in `frontend_vue/src/router/index.js`.
- The main shared Axios client and endpoint builders are in `frontend_vue/src/services/Shared/api.js` and `endpoints.js`. Additional request paths include `axiosInstance.js`, `mcpService.js`, global Axios setup, and AI streaming fetch code; uniform auth/error behavior cannot be inferred across clients.
- Existing domain documents cover views, components, stores, and services, but their catalogue summaries do not prove that each view is reachable or each backend operation is compatible.
- Existing guides and this audit are static. No frontend build, unit test, browser session, or HTTP request was run.

## Remaining frontend work

1. Add the four test/resource paths to their corresponding feature catalogues if maintaining those documents; the global shared catalogue already lists them.
2. Reconcile the shared catalogue's declared file total with the 288 current source paths.
3. Verify page/component/store/service call relationships and route-level reachability rather than relying only on path catalogs.
4. Complete backend endpoint and payload matching in `04_integration/`.
