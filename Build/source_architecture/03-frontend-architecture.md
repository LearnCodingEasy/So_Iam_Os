# Frontend Architecture

## Application startup

**VERIFIED:** `frontend_vue/src/main.js` creates the Vue app, installs Pinia, Vue Query, Vue Router, i18n, PrimeVue services/components, markdown and toast integrations, then mounts the app. `frontend_vue/vite.config.js` configures the Vue plugin, `@` alias, PWA plugin, and Workbox caching behavior.

## Routes and shell

**VERIFIED:** `frontend_vue/src/router/index.js` declares routes for account, goals, tasks, learning, knowledge, jobs, finance, AI, Codex, projects, automation, scraping, and other areas. The global guard initializes the user store and checks `requiresAuth`/`requiresGuest`. `frontend_vue/src/App.vue` renders `RouterView` and shared shell components.

The route table confirms navigation declarations only; it does not establish that every destination renders or completes its full workflow successfully.

## Feature structure and state

The source groups feature code under `frontend_vue/src/views/`, `components/`, `services/`, and `stores/`. **VERIFIED:** examples of service/store/view wiring include Goals (`services/Goals/goals.js`, `stores/goals/goalsStore.js`, `views/goals/Goals.vue`), Projects (`services/Projects/projects.js`, `stores/projects/projects.js`, `views/projects/ProjectsView.vue`), and Codex (`services/Codex/codex.js`, `stores/codex/codex.js`, `views/codex/`).

**VERIFIED:** Account tokens and profile data are stored in browser localStorage by `frontend_vue/src/stores/accounts/user.js`; other local persistence exists for theme, locale, and automation graph state (`frontend_vue/src/stores/shared/`, `frontend_vue/src/services/Automation/nodeStorageService.js`).

## HTTP and error handling

**VERIFIED:** `frontend_vue/src/services/Shared/api.js` creates the main Axios client, attaches bearer tokens, refreshes tokens, retries selected 401 responses, and emits API telemetry events. Endpoint paths are collected in `frontend_vue/src/services/Shared/endpoints.js`.

**PARTIAL:** There are additional clients and direct requests with different configuration and auth conventions: `frontend_vue/src/services/Shared/axiosInstance.js`, `frontend_vue/src/services/Shared/mcpService.js`, global Axios defaults in `main.js`, and streaming fetch in `frontend_vue/src/services/AI/AIService.js`. Consequently, uniform auth, timeout, telemetry, and error behavior cannot be assumed across features.

Error and notification patterns include `frontend_vue/src/utils/apiError.js`, `frontend_vue/src/composables/useAppToast.js`, and view-level handlers. Forms use several approaches; `vee-validate`/Zod integration is present in `frontend_vue/src/views/ai/AIControl.vue`.

## Live and local effects

**VERIFIED:** `frontend_vue/src/components/shared/LiveDebugConsole.vue` gates its debug WebSocket on configuration and UI state; automation components also create WebSocket connections. `frontend_vue/src/views/scraper/ScraperView.vue` polls for updates. These are source behaviors, not proof of a reachable backend socket or successful polling in a deployed environment.

See [API and Integration Map](./04-api-and-integration-map.md) and [Security and Operations](./06-security-and-operations.md).
