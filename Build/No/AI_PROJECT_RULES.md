# SO_IAM_OS — AI Project Rules & Engineering Constitution

> **Document type:** Evidence-based architecture reference and AI coding-agent policy  
> **Project:** SO_IAM_OS (Adaptive Personal AI Operating System)  
> **Repository snapshot:** Uploaded `So_Iam_Os.zip`  
> **Audit date:** 2026-11-13  
> **Audit mode:** Read-only static source inspection  
> **Authority:** The current source tree and its executable configuration take precedence over roadmap prose, generated reports, and assumptions.

---

## 1. Project Identity

SO_IAM_OS is described by its README as an **Adaptive Personal AI Operating System**. Its intended lifecycle connects learning, building, applying, executing, measuring, improving, and earning. AI is intended to be a core capability that works with user context, memory, goals, work, learning, and actions.

This is an architectural intent, not proof that every described capability is implemented or production-operational.

### Evidence classification

Use these labels in future engineering work:

- **CONFIRMED:** Directly visible in current source/configuration.
- **STATIC-AUDIT ONLY:** Route, import, declaration, or code path exists; runtime behavior has not been proven.
- **INFERRED — NOT VERIFIED:** Reasonable architectural interpretation that still needs runtime or deeper code verification.
- **UNKNOWN — REQUIRES VERIFICATION:** The supplied source does not establish the fact.
- **PARTIAL / NOT CONNECTED / NOT IMPLEMENTED:** Use when the feature lifecycle is visibly incomplete.

Do not convert a static finding into a claim that a feature works in production.

## 2. Project Overview

### Confirmed technology shape

| Layer | Evidence-based implementation |
|---|---|
| Frontend | Vue 3 application under `frontend_vue/`, built with Vite |
| UI | PrimeVue, PrimeVue themes, PrimeIcons, Font Awesome, Tailwind CSS, SCSS |
| State | Pinia; Vue Query plugin is registered |
| Routing | Vue Router |
| HTTP | Shared Axios client in `frontend_vue/src/services/api.js`; additional Axios-related service files exist |
| Backend | Django project under `backend_django/` |
| API | Django REST Framework |
| Authentication | SimpleJWT; custom user model `users_accounts.User` |
| Database | SQLite default for local settings; PostgreSQL selected by `DATABASE_ENGINE=postgresql`; production setting rejects non-PostgreSQL |
| Async work | Celery, django-celery-results, django-celery-beat, Redis configuration |
| Real-time | Django Channels and ASGI; a debug-console WebSocket route is wired in ASGI |
| AI | Provider/configuration, credential, prompt, conversation, execution, usage, and workflow-related code exists in the `ai` app |
| Tests | Django test modules and Vitest configuration/spec files exist |
| Build | Vite scripts and project release/verification scripts exist |

### Repository layout (observed)

```text
So_Iam_Os/
├── .env.example
├── README.md
├── requirements.txt
├── API_ENDPOINT_AUDIT.csv
├── API_INTEGRATION_GUIDE.md
├── BACKEND_FRONTEND_INTEGRATION_MATRIX.md
├── FEATURE_REGISTER.csv
├── IMPLEMENTATION_AUDIT_REPORT*.md
├── IMPLEMENTATION_NOTES.md
├── CODEX_RELEASE_VALIDATION.md
├── BUILD_CHECKLIST.md
├── PROJECT_CONTEXT.json
├── project_manifest.json
├── scripts/
├── Build/
├── backend_django/
│   ├── backend_django/       # Django project settings, urls, ASGI, WSGI
│   ├── ai/
│   ├── automation/
│   ├── challenges/
│   ├── codex/
│   ├── core/
│   ├── goals/
│   ├── jobs_opportunity/
│   ├── knowledge/
│   ├── learning/
│   ├── memory/
│   ├── notification/
│   ├── personal_finance/
│   ├── projects/
│   ├── scraper/
│   ├── social/
│   ├── tasks/
│   ├── users_accounts/
│   ├── users/                # present in archive; not listed in INSTALLED_APPS
│   ├── manage.py
│   └── db.sqlite3            # included local database file; do not assume production DB
└── frontend_vue/
    ├── package.json
    ├── package-lock.json
    ├── vite.config.js
    └── src/
        ├── components/
        ├── composables/
        ├── plugins/
        ├── presets/
        ├── router/
        ├── services/
        ├── stores/
        ├── utils/
        ├── views/
        ├── assets/
        ├── App.vue
        └── main.js
```

The archive contains 1,150 files in total. Build output, caches, and dependency directories were not treated as application source. The archive includes a SQLite database file; its data has not been queried or treated as authoritative production data.

## 3. System Architecture

### Runtime topology (source-derived)

```text
Browser
  └── Vue 3 + Vite application
       ├── Vue Router
       ├── Pinia stores
       ├── composables / shared components
       └── domain service modules
            └── shared Axios client
                 └── Django API (/api/...)
                      ├── users_accounts
                      ├── core
                      ├── ai
                      ├── knowledge / learning
                      ├── goals / tasks
                      ├── jobs_opportunity / scraper
                      ├── automation / codex
                      ├── projects / challenges
                      ├── social / notification / memory
                      └── personal_finance
```

Supporting backend infrastructure is configured for PostgreSQL, Redis, Celery, and Channels. Exact deployed topology, process manager, reverse proxy, and production host configuration are **UNKNOWN — REQUIRES VERIFICATION** because no Docker Compose, Nginx, or CI deployment definition was found in the inspected archive.

### Django application registration

`backend_django/backend_django/settings.py` registers these 17 project apps:

1. `ai`
2. `automation`
3. `challenges`
4. `codex`
5. `core`
6. `goals`
7. `jobs_opportunity`
8. `knowledge`
9. `learning`
10. `memory`
11. `notification`
12. `personal_finance`
13. `projects`
14. `scraper`
15. `social`
16. `tasks`
17. `users_accounts`

The separate `backend_django/users/` directory exists in the archive but is not in the shown `INSTALLED_APPS` list. Do not import it as an active Django app or remove it without tracing imports and history.

### Application responsibilities (directory and source evidence)

| App | Observed responsibility / code evidence |
|---|---|
| `users_accounts` | Custom user model, account API, views, forms, serializers, admin; configured as `AUTH_USER_MODEL` |
| `core` | Shared core API, services, managers, permissions, pagination, exceptions, signals, debug console |
| `ai` | AI provider configuration/adapters, credential security, prompts, conversations, serializers, views, tasks, chat and diagnostics API |
| `memory` | Memory models, serializers, views, URLs |
| `knowledge` | Knowledge items/files, services, file validation, metadata extraction, tasks |
| `learning` | Learning models, serializers, views, URL routes, dedicated `services/` directory |
| `goals` | Goal models, services, coach logic, serializers, views |
| `tasks` | Task models, services, daily generation, tasks, serializers, views |
| `jobs_opportunity` | Job opportunities, matching/application-related domain, scraper helpers, tasks, feature catalog/default sources |
| `scraper` | Scraper sources/configuration/selectors/runs, services, tasks |
| `automation` | Workflow/program models, runner/runtime/engine, window manager, permission policy, consumers, routing, tasks |
| `codex` | Codex/build workspace, manifest, project/feature/file/API/policy/tool/audit/agent-run related services and management code |
| `projects` | Project, member, context API |
| `challenges` | Challenge, step, attempt, progress API |
| `personal_finance` | Finance models, services, serializers, views |
| `social` | Social profile, recommendations/matching, friend flows |
| `notification` | Notification API and models |

This table describes source organization, not verified business completeness.

### Cross-module rules

- Keep domain ownership in the existing Django app. Do not create a parallel app for a feature already owned by one of these modules.
- Cross-app operations must use explicit service/API boundaries and preserve user scoping.
- Avoid circular imports. Move shared, genuinely cross-domain primitives into `core` only when justified.
- Do not allow frontend-only state to become the authority for access control or business invariants.
- Before changing a model used by another app, trace foreign keys, serializers, services, signals, tasks, API consumers, and migrations.

## 4. Directory Structure & Frontend Architecture

### Frontend source organization

The actual frontend is organized by shared technical layers plus domain-oriented views/components/services/stores. Existing view folder names have mixed capitalization (`AI`, `Dashboard`, `Goals`, `knowledge`, `learning`, `jobs`, etc.). Preserve existing paths unless a planned migration updates all imports and route references.

Important locations:

| Path | Responsibility |
|---|---|
| `frontend_vue/src/main.js` | App bootstrap, global CSS, plugin and PrimeVue registration |
| `frontend_vue/src/App.vue` | Root component |
| `frontend_vue/src/router/` | Vue Router setup and navigation guards |
| `frontend_vue/src/stores/` | Pinia stores |
| `frontend_vue/src/services/api.js` | Shared Axios client, auth token handling, request lifecycle |
| `frontend_vue/src/services/endpoints.js` | Central endpoint path builders |
| `frontend_vue/src/services/` | Domain API services |
| `frontend_vue/src/composables/` | Reusable Composition API logic |
| `frontend_vue/src/components/` | Shared and domain components |
| `frontend_vue/src/views/` | Route-level pages |
| `frontend_vue/src/assets/scss/` | SCSS stylesheets |
| `frontend_vue/vite.config.js` | Vite, Vue plugin, PWA configuration |

### Existing frontend domains/views

The `views/` tree includes `AI`, `Authentication`, `Settings`, `Social`, `AboutView.vue`, `Goals`, `Challenges`, `Finance`, `Progress`, `knowledge`, `HomeView.vue`, `Memory`, `Projects`, `Codex`, `jobs`, `learning`, `Scraper`, `Account`, `Notifications`, `Tasks`, `Dashboard`, and `Automation`.

The router also imports route components for these domains and a not-found page. Route metadata is used for authentication/guest requirements. The root (`/`) and `/About` routes are marked `requiresAuth` in the inspected router source; do not assume they are public based on their names.

### Frontend architecture rules

1. Use Vue 3 Composition API consistently with existing project conventions.
2. Use Pinia for shared client state; avoid duplicating server state in stores when Vue Query or the existing service/query pattern is the better fit.
3. Keep HTTP calls in `src/services/` rather than embedding endpoint construction in views.
4. Prefer `src/services/endpoints.js` for canonical endpoint paths.
5. Keep reusable components in `src/components/`; keep route-level orchestration in `src/views/`.
6. Put reusable stateful logic in `src/composables/`.
7. Keep styles under `src/assets/` and follow the existing SCSS structure. Do not introduce new ad-hoc CSS locations.
8. All new authenticated pages must participate in the existing router/authentication and application layout patterns. Inspect the current `App.vue` and layout components before deciding the wrapper; a single universal AppLayout is a desired governance direction, not proof every existing view currently uses one.
9. Respect responsive layouts, Arabic/English content, RTL/LTR behavior, and existing design tokens. Verify the actual i18n and direction implementation before extending it.
10. Use real API data. Mock data is permitted only in isolated tests, story/demo fixtures, or explicitly labelled empty-state previews; never use fake data as a production fallback.
11. Do not introduce direct `localhost` URLs in views or domain services. Configure the shared client through environment variables.
12. Avoid duplicated UI, validation, upload, chart, drag/drop, editor, and notification implementations when an existing library/component already serves the use case.

### Frontend startup and global configuration

`main.js` registers Vue, Pinia, Vue Query, i18n, FloatingVue, toast notifications, Font Awesome, PrimeVue, and numerous PrimeVue components/services. It imports Tailwind CSS, Animate.css, SCSS, and Markdown styling. PrimeVue components are registered globally in bootstrap. Review `main.js` before adding another global plugin or component registration.

`vite.config.js` configures Vue, the PWA plugin, `@` as an alias for `src`, and a Workbox runtime cache for document/script/style/image/font resources. The PWA manifest still contains product copy such as “Script Youtube” / “My Awesome App”; treat this as an identified branding/configuration cleanup candidate, not an instruction to alter it during an unrelated feature task.

## 5. Frontend Libraries

Versions below are the declared ranges in `frontend_vue/package.json`, not proof of the exact installed runtime version. Static import/reference scans were performed over `src/`; no runtime bundle analysis was performed.

### Runtime dependencies

| Library | Declared version | Observed role / status |
|---|---:|---|
| `vue` | `^3.5.40` | Core framework; pervasive |
| `vue-router` | `^5.2.0` | Route configuration/navigation |
| `pinia` | `^4.0.2` | State management; bootstrap and stores |
| `axios` | `^1.20.0` | HTTP; shared API client and other references |
| `primevue` | `^5.0.1` | Main UI component library; extensive global/component use |
| `@primevue/themes` | `^4.5.4` | PrimeVue theme package; declared major differs from PrimeVue 5 and requires peer compatibility verification |
| `primeicons` | `^8.0.0` | PrimeVue icon assets |
| `@fortawesome/fontawesome-svg-core` | `^7.3.1` | Icon core |
| `@fortawesome/free-brands-svg-icons` | `^7.3.1` | Brand icon set |
| `@fortawesome/free-regular-svg-icons` | `^7.3.1` | Regular icon set |
| `@fortawesome/free-solid-svg-icons` | `^7.3.1` | Solid icon set |
| `@fortawesome/vue-fontawesome` | `^3.0.0-5` | Vue Font Awesome integration |
| `tailwindcss` | `^3.4.19` (dev dependency) | Utility CSS; CSS imports and config references |
| `animate.css` | `^4.1.1` | Global animation styles |
| `chart.js` | `^4.5.1` | Chart engine |
| `vue-chartjs` | `^5.3.2` | Vue chart bindings |
| `cropperjs` | `^1.6.2` | Image crop/edit flow |
| `dompurify` | `^3.3.1` | HTML sanitization in Markdown/content path |
| `marked` | `^17.0.1` | Markdown parsing |
| `prismjs` | `^1.30.0` | Code syntax highlighting |
| `github-markdown-css` | `^5.9.0` | Markdown presentation |
| `vue3-markdown-it` | `^1.0.10` | Markdown component/plugin; imported in bootstrap |
| `gsap` | `^3.15.0` | Animation; AI UI implementation report also describes use |
| `nprogress` | `^0.2.0` | Router/API progress indicator |
| `lodash` | `^4.18.1` | Utility functions |
| `dagre` | `^0.8.5` | Graph layout; references found |
| `@vue-flow/core` | `^1.48.2` | Node/edge graph UI |
| `@vue-flow/background` | `^1.3.2` | Vue Flow background |
| `@vue-flow/controls` | `^1.1.3` | Vue Flow controls |
| `@vue-flow/minimap` | `^1.5.4` | Vue Flow minimap |
| `vuedraggable` | `^4.1.0` | Drag-and-drop list integration |
| `vue-draggable-plus` | `^0.6.1` | Additional drag/drop library; evaluate overlap with `vuedraggable` before extending |
| `vee-validate` | `^4.15.1` | Form validation |
| `@vee-validate/zod` | `^4.15.1` | Zod adapter for VeeValidate |
| `zod` | `^3.25.0` | Schema validation |
| `@vueuse/core` | `^10.11.1` | Vue composables/utilities |
| `@tanstack/vue-query` | `^5.107.1` | Server-state/query plugin |
| `vue-i18n` | `^11.4.18` | Internationalization |
| `floating-vue` | `^5.4.0` | Tooltip/popover positioning |
| `vue-virtual-scroller` | `^3.0.5` | Virtualized lists |
| `@tiptap/vue-3` | `^3.33.1` | Rich-text editor integration |
| `@tiptap/starter-kit` | `^3.33.1` | Tiptap base extensions |
| `filepond` | `^4.32.12` | File upload UI; references found |
| `vue-sonner` | `^2.0.9` | Toast notifications |
| `quill` | `^2.0.3` | No direct `src/` reference found in static scan; usage UNKNOWN / verify before removal |

### Development dependencies

| Library | Declared version | Observed role / status |
|---|---:|---|
| `vite` | `^8.1.5` | Frontend dev server/build |
| `@vitejs/plugin-vue` | `^6.0.8` | Vue SFC support in Vite config |
| `vitest` | `^4.1.10` | Unit test runner; config/spec files present |
| `@vue/test-utils` | `^2.4.11` | Vue component test utility; spec reference found |
| `jsdom` | `^29.1.1` | Test DOM dependency; direct source use not found |
| `eslint` | `^10.7.0` | Lint script/config |
| `@eslint/js` | `^10.0.1` | ESLint base config; direct source reference not found |
| `eslint-config-prettier` | `^10.1.8` | Formatting/lint compatibility; direct source reference not found |
| `eslint-plugin-oxlint` | `~1.73.0` | ESLint/Oxlint integration; direct source reference not found |
| `eslint-plugin-vue` | `~10.9.2` | Vue linting; direct source reference not found |
| `vue-eslint-parser` | `^10.4.1` | Vue ESLint parsing; direct source reference not found |
| `globals` | `^17.7.0` | Lint configuration dependency; direct source reference not found |
| `oxlint` | `^1.73.0` | Lint command dependency |
| `prettier` | `3.9.5` | Format command |
| `npm-run-all2` | `^9.0.2` | `run-s` script runner |
| `sass` | `^1.104.0` | SCSS compilation |
| `postcss` | `^8.5.28` | CSS processing |
| `autoprefixer` | `^10.5.5` | CSS prefixing |
| `vite-plugin-pwa` | `^1.3.0` | PWA plugin used in Vite config |
| `vite-plugin-vue-devtools` | `^8.1.5` | Declared; direct config/source use not observed |
| `@vitest/eslint-plugin` | `^1.6.23` | Declared; direct source/config use not observed |

### Dependency governance

- Treat `package.json` and `package-lock.json` as a pair. Use `npm ci` for reproducible installs.
- The lockfile is included, but exact dependency tree/peer compatibility was not runtime-validated in this audit.
- Resolve the PrimeVue 5 / `@primevue/themes` 4 major-version mismatch by inspecting lockfile peer metadata and official compatibility before changing either version.
- Vue Router 5, Vue 3, Vite 8, Vitest 4, and Node engine compatibility must be validated together in CI/runtime; do not assume support from the manifest alone.
- There are two drag/drop packages (`vuedraggable`, `vue-draggable-plus`), two Markdown approaches (`marked` and `vue3-markdown-it`), and two editor families (`Tiptap` and Quill). Prefer the already-used implementation in the target feature; do not add another parallel implementation.
- `quill` has no direct `src/` reference in the static scan. It is **candidate unused**, not safe to remove until checking lazy/dynamic imports, plugins, generated code, and all consumers.
- A dependency with no textual reference may be config-only, transitive, dynamically loaded, or unused. Confirm before removal.
- Never install a new package merely for convenience when an existing dependency or shared component already provides the capability.
- Any new dependency proposal must state: why existing packages are insufficient, exact version/compatibility, bundle/runtime impact, license/security considerations, and affected lockfile changes.

## 6. Backend Architecture

### Django project configuration

- Django settings module: `backend_django.settings`.
- Root URL configuration: `backend_django.urls`.
- ASGI application: `backend_django.asgi.application`.
- WSGI application: `backend_django.wsgi.application`.
- Custom user model: `users_accounts.User`.
- Default DRF authentication: `rest_framework_simplejwt.authentication.JWTAuthentication`.
- Default DRF permission: `IsAuthenticated`.
- Middleware includes Django security/session/common/CSRF/auth/messages/clickjacking, CORS middleware, and allauth account middleware.
- Django app registrations are listed in Section 3.

### Backend source conventions

Most domain apps contain some combination of `models.py`, `serializers.py`, `views.py`, `urls.py`, `admin.py`, `apps.py`, `tests.py`, and `migrations/`. Dedicated service modules/directories exist in AI, automation, core, goals, jobs, knowledge, learning, scraper, tasks, and other domains.

Rules:

1. Models define persistence and invariants; serializers validate API input/output.
2. Views/ViewSets should remain thin and delegate reusable business operations to domain services.
3. Keep authorization checks on the backend and scope private querysets to `request.user`.
4. Avoid cross-domain model manipulation from unrelated views; use explicit service functions.
5. Keep external provider calls behind adapters/services with bounded timeouts and normalized errors.
6. Do not perform slow external calls or long-running work synchronously if an existing Celery path is intended for it.
7. Every model/schema change requires a migration, migration review, and tests; never edit an already-applied migration to change deployed history.
8. Preserve existing import paths/compatibility shims unless usage has been traced and migration is coordinated.
9. Add tests for permission boundaries, invalid payloads, state transitions, and side effects.
10. Do not treat an endpoint's presence in `urls.py` as proof its business operation is complete.

### Backend app structure

`ai/` has a modular subpackage layout for permissions, models, tasks, tests, services, serializers, and API handlers in addition to compatibility/root modules. Prefer the established subpackages for new AI code, but inspect import compatibility before relocating legacy modules.

`automation/` includes engine/runtime and AI/service subdirectories, workflow runner, permission policy, window manager, Channels consumer/routing, and Celery task modules. This app can interact with desktop/window automation dependencies; any action with external or local side effects must require explicit permission and be audited.

`codex/` includes service modules, tests, management code, catalog, tasks, and build workspace/manifest APIs. It also has governance metadata in root `PROJECT_CONTEXT.json` and `project_manifest.json`. Those manifests explicitly state that protected items must not be modified, moved, renamed, replaced, or deleted without human approval. Current protected list is empty; the governance rule still applies if populated later.

## 7. Backend Libraries

Declared in root `requirements.txt`:

| Package | Declared range | Role evidenced by configuration/source |
|---|---|---|
| Django | `>=5.2,<6.1` | Web framework |
| djangorestframework | `>=3.16,<4` | REST API |
| djangorestframework-simplejwt | `>=5.5,<6` | JWT auth; access 15 minutes, refresh 14 days, rotation and blacklist configured |
| django-allauth | `>=65,<66` | Account/social auth; Google provider registered |
| django-cors-headers | `>=4.7,<5` | CORS middleware/settings |
| django-filter | `>=25,<26` | Declared; exact filter usage should be verified per view |
| channels | `>=4.2,<5` | ASGI/WebSocket infrastructure |
| daphne | `>=4.2,<5` | ASGI server package; registered in apps |
| celery | `>=5.5,<6` | Background tasks |
| django-celery-results | `>=2.6,<3` | Celery result persistence app |
| django-celery-beat | `>=2.8,<3` | Periodic task scheduling app |
| redis | `>=6,<7` | Redis client |
| channels-redis | `>=4.3,<5` | Redis channel layer backend |
| psycopg[binary] | `>=3.2,<4` | PostgreSQL driver |
| python-decouple | `>=3.8,<4` | Environment configuration |
| python-dotenv | `>=1.1,<2` | `.env` loading |
| requests | `>=2.32,<3` | HTTP integrations |
| cryptography | `>=45,<47` | Credential encryption/security |
| pydantic | `>=2.11,<3` | Structured validation/configuration where used |
| openai | `>=2,<3` | OpenAI integration |
| rich | `>=14,<15` | Terminal output |
| psutil | `>=7,<8` | Process/system information |
| pyautogui | `>=0.9.54,<1` | Desktop automation |
| pyperclip | `>=1.9,<2` | Clipboard automation |
| pygetwindow | `>=0.0.9,<1` | Window management |
| pywin32 | `>=311` on Windows | Windows-specific automation |
| pywinauto | `>=0.6.9,<1` on Windows | Windows UI automation |
| beautifulsoup4 | `>=4.13,<5` | HTML parsing/scraping |
| lxml | `>=6,<7` | HTML/XML parsing |

Exact installed versions are **UNKNOWN — REQUIRES VERIFICATION** because no Python lockfile or pinned environment snapshot was found. Python interpreter version is also **UNKNOWN — REQUIRES VERIFICATION**.

## 8. Database Architecture

### Engine selection

`backend_django/backend_django/settings.py` selects the database through `DATABASE_ENGINE`:

- Default: `sqlite3`, file at `backend_django/db.sqlite3`.
- When `DATABASE_ENGINE=postgresql`: PostgreSQL via `django.db.backends.postgresql`, with `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, and `POSTGRES_PORT`.
- When `ENVIRONMENT=production`, settings explicitly reject a non-PostgreSQL engine.

Therefore: PostgreSQL is the configured production target; SQLite is the default local/development path. The included SQLite file does not prove which database is deployed.

### Schema and migrations

The archive contains 58 Python migration files under app migration directories. Model files are present across the registered apps. This audit did not perform a live schema introspection, apply migrations, compare migration state to a database, or generate an ER diagram.

For every database change:

1. Inspect model definitions and related models in all affected apps.
2. Review constraints, indexes, `on_delete`, nullable/default behavior, and ownership.
3. Generate a migration only in an approved implementation task.
4. Inspect migration operations manually.
5. Test both a fresh database and an upgrade from a representative prior migration state.
6. Use transactions for multi-record operations requiring atomicity.
7. Avoid destructive migrations without an explicit data migration/backup/rollback plan.
8. Never use the uploaded `db.sqlite3` as proof of production schema or production data.

Relationships and full table cardinalities: **UNKNOWN — REQUIRES VERIFICATION** through model/migration and live DB review before producing a definitive ERD.

## 9. API Architecture

### Root API prefixes confirmed in `backend_django/backend_django/urls.py`

| Prefix | Django include |
|---|---|
| `/api/codex/` | `codex.urls` |
| `/api/users/` | `users_accounts.urls` |
| `/api/core/` | `core.urls` |
| `/api/knowledge/` | `knowledge.urls` |
| `/api/learning/` | `learning.urls` |
| `/api/scraper/` | `scraper.urls` |
| `/api/ai/` | `ai.urls` |
| `/api/goals/` | `goals.urls` |
| `/api/tasks/` | `tasks.urls` |
| `/api/jobs/` | `jobs_opportunity.urls` |
| `/api/social/` | `social.urls` |
| `/api/automation/` | `automation.urls` |
| `/api/notifications/` | `notification.urls` |
| `/api/memory/` | `memory.urls` |
| `/api/projects/` | `projects.urls` |
| `/api/challenges/` | `challenges.urls` |
| `/api/finance/` | `personal_finance.urls` |

The project URL file also declares explicit Codex build workspace and manifest paths before including `codex.urls`. The endpoint audit flags two duplicate Codex paths; verify resolver ordering and remove duplication only as a separately tested change.

### Existing API audit artifact

`API_ENDPOINT_AUDIT.csv` contains 396 route records:

| Domain | Records |
|---|---:|
| Codex | 78 |
| Learning | 70 |
| Jobs Opportunity | 62 |
| Personal Finance | 48 |
| Automation | 37 |
| AI | 15 |
| Tasks | 14 |
| Knowledge | 12 |
| Scraper | 12 |
| Challenges | 8 |
| Projects | 7 |
| Social | 7 |
| Users Accounts | 7 |
| Goals | 6 |
| Notification | 6 |
| Core | 3 |
| Memory | 2 |
| MCP | 1 |
| Explain | 1 |

The audit file itself marks most entries as runtime-not-tested: 176 static router routes, 124 static actions whose payloads require serializer/ViewSet confirmation, 92 static URL routes, two duplicate Codex paths, and two records without a verification status. These records are a useful inventory, not a live API test report. `mcp` and `explain` entries in the audit should not be assumed to be registered Django apps or root URL prefixes.

### Canonical frontend API pattern

- Base client: `frontend_vue/src/services/api.js`.
- Canonical endpoint builder: `frontend_vue/src/services/endpoints.js`.
- Domain services include `usersAccounts.js`, `goals.js`, `tasks.js`, `learning.js`, `knowledge.js`, `jobs.js`, `scraperApi.js`, `ai.js`, `AIService.js`, `codex.js`, `AutomationService.js`, `workflowService.js`, `notifications.js`, `social.js`, `projects.js`, `dashboard.js`, and `ecosystemApi.js`.

The integration guide `API_INTEGRATION_GUIDE.md` describes `/api/` as the API root and recommends `VITE_API_BASE_URL=http://127.0.0.1:8000/api` with `/api` included exactly once. `api.js` itself defaults to `http://127.0.0.1:8000/api`. `main.js` also sets the global Axios default base URL from `VITE_API_URL` or `VITE_API_BASE_URL`, defaulting to `http://127.0.0.1:8000` (without `/api`). There are multiple Axios clients/files. Treat this as a configuration-consistency risk: all domain services must use the intended shared client and one canonical base URL. Do not silently change this contract; trace every client first.

### Endpoint contract rules

For every endpoint change, document and test:

- Prefix, path, HTTP method, route name/action.
- Authentication and permission requirements.
- Query/path parameters.
- Request serializer/schema.
- Response schema and status codes.
- Pagination/filter/order behavior.
- Error response structure.
- Frontend service method and consuming view/store/composable.
- Side effects, Celery task dispatch, and emitted events.

Never invent an endpoint based only on a frontend URL builder or audit spreadsheet. Verify `urls.py`, view/action, serializer, service, and model.

## 10. Frontend–Backend Integration

### Authentication contract visible in source

- DRF defaults to JWT authentication and `IsAuthenticated`.
- SimpleJWT settings: access token lifetime 15 minutes; refresh token lifetime 14 days; refresh rotation enabled; blacklist after rotation enabled; last-login update enabled.
- Frontend API client reads `localStorage` keys `user.access` and `user.refresh`.
- On 401 it attempts refresh through `/users/refresh/`.
- When rotated refresh token is returned, frontend persists both access and refresh tokens; this is necessary because old refresh tokens are blacklisted after rotation.
- Auth expiry and refresh events are dispatched as browser custom events.

### Integration rules

1. Use the shared Axios client from domain services; do not create ad-hoc clients without a documented reason.
2. Keep API base URL environment-driven. Never hardcode production hosts or page-level localhost URLs.
3. Keep endpoint builders centralized and preserve trailing-slash conventions used by Django routes.
4. Handle loading, empty, success, validation, authorization, network, and server-error states explicitly.
5. Do not assume all APIs return the same pagination or response envelope. Inspect the actual serializer/view.
6. Preserve the backend's user scoping and authorization checks.
7. When changing request/response fields, update serializer, service, store/composable, and every consuming view/component together.
8. For file upload, inspect backend validators, content-type/size rules, and whether the request requires multipart headers.
9. For WebSockets, inspect the ASGI route, consumer authentication, origin policy, and channel layer. Do not assume a frontend WebSocket client exists just because Channels is installed.
10. Token storage currently uses localStorage. Treat this as an existing implementation, not an ideal security guarantee; do not broaden token exposure or log token values. Any migration to HttpOnly cookies requires a coordinated backend/frontend/CSRF design.

### API mismatch watchlist

- `main.js` global Axios default and `services/api.js` shared client have different default base URL conventions (`/` versus `/api`).
- `axiosInstance.js` is an additional service file; inspect its consumers before consolidation.
- Two duplicate Codex build routes are called out by the endpoint audit.
- The integration guide describes API/service mappings, but it explicitly does not establish runtime health.
- The endpoint audit includes MCP/Explain rows whose root app registration is not shown in current `INSTALLED_APPS`; verify their implementation path before treating them as active backend modules.

## 11. Authentication & Authorization

- Custom user model: `users_accounts.User`.
- DRF default authentication: SimpleJWT.
- DRF default permission: `IsAuthenticated`.
- allauth account and Google social provider are installed/configured.
- User-facing domain querysets must scope private objects to `request.user`.
- Object-level permissions must be checked for detail/actions, not only list endpoints.
- Frontend route guards are UX controls only; they never replace backend authorization.
- Do not expose credentials, tokens, private profile data, AI provider secrets, or finance data in API responses/logs.
- Test cross-user access for list, retrieve, update, delete, nested actions, downloads, and WebSocket messages.
- Confirm allauth signup/login/social callback behavior in runtime; source configuration alone does not prove provider setup is valid.

## 12. Real-Time Communication

`backend_django/asgi.py` constructs a `ProtocolTypeRouter` with HTTP handled by Django and WebSocket handled by `URLRouter(websocket_urlpatterns)` imported from `core.debug_console.routing`.

`automation/` also contains `consumers.py` and `routing.py`; whether these routes are included in the project-level ASGI router must be traced before claiming they are live.

Channel layer configuration:

- Default backend: in-memory channel layer.
- Optional Redis channel layer when `CHANNEL_LAYERS_BACKEND=redis`, using `REDIS_URL`.

Rules:

- In-memory Channels is not a multi-process production channel layer.
- For multi-worker production WebSockets, configure Redis and validate authentication, origin checks, group membership, and reconnect behavior.
- Do not send sensitive payloads to broad groups.
- Add tests for unauthorized connection, user isolation, disconnect cleanup, and message schema.
- Frontend WebSocket integration is **UNKNOWN — REQUIRES VERIFICATION** per feature; do not infer it from backend packages alone.

## 13. Background Tasks

Celery is configured with broker/result backend defaulting to Redis. `django_celery_results` and `django_celery_beat` are installed. Celery settings use JSON serialization and bounded broker/result retry behavior. Multiple apps contain `tasks.py`.

Rules:

- Keep long-running AI, scraping, generation, and automation jobs in task modules where appropriate.
- API endpoints should return an explicit task/run identifier and status contract when work is asynchronous.
- Make tasks idempotent where retries are possible.
- Enforce user ownership at enqueue time and again when loading task resources.
- Use bounded retries, provider timeouts, and clear failure states.
- Never log secrets or full sensitive prompts/provider payloads.
- A Celery task declaration is not proof a worker or beat process is running.
- Deployment commands and worker topology are **UNKNOWN — REQUIRES VERIFICATION**; confirm from the actual deployment environment.

## 14. AI & External Integrations

### AI code organization

The `ai/` app includes provider/configuration, credential security, prompts, models, serializers, services, views, API handlers (`api/chat.py`, `api/diagnostics.py`), tasks, permissions, tests, and learning-action integration. A modular subpackage structure is present alongside root-level modules for compatibility.

The project settings declare AI defaults and environment-backed provider configuration. The production AI credential encryption key is required to be at least 32 characters. Production `SECRET_KEY` must be unique and at least 50 characters. Provider secrets must never be committed or included in documentation.

The previous implementation report states that the AI path includes provider fallback, Ollama configuration, OpenAI/Gemini-related integration, credential-safe management responses, bounded provider timeouts, and Markdown/code rendering. Treat those as **reported implementation claims** until the current call path and runtime tests independently prove them.

### AI engineering rules

1. Keep provider-specific request/response logic in provider adapters; normalize outputs and errors.
2. Keep credential resolution scoped to the authenticated user when credentials are user-owned.
3. Never return API keys or decrypted credential values from serializers/views.
4. Use bounded connect/read/overall deadlines and bounded retries.
5. Distinguish rate limiting, quota/billing exhaustion, invalid model/configuration, authentication failure, transient network errors, and provider outage.
6. Fallback must continue only to eligible providers and must preserve the original failure context safely.
7. Do not silently switch model/provider or send data to another provider without honoring user configuration and privacy settings.
8. Keep prompts versioned/centralized where the existing prompt profile mechanism applies.
9. Validate tool/action plans and require authorization/confirmation before side effects.
10. AI-generated HTML/Markdown is untrusted. Sanitize HTML before rendering; do not trust model output as executable code.
11. Record usage/observability without storing secrets or unnecessary personal data.
12. Test adapters with mocked HTTP, credential security, fallback ordering, quota errors, malformed responses, timeouts, and user isolation.
13. A successful local mock/unit test is not proof of live OpenAI, Gemini, Ollama, DeepSeek, or OpenRouter connectivity.

### Other external integrations

- `jobs_opportunity` and `scraper` contain source/scraping code and tasks.
- `social` configures Google allauth provider through project settings.
- `automation` contains desktop/window automation dependencies and engine code.
- GitHub/MCP integrations may be represented in Codex/service/catalog code; exact external service status and credential availability are **UNKNOWN — REQUIRES VERIFICATION**.

## 15. Security & Data Protection

Non-negotiable rules:

- Never expose `SECRET_KEY`, database passwords, provider API keys, OAuth secrets, refresh/access tokens, encryption keys, or raw `.env` contents.
- Never commit real credentials. `.env.example` must contain placeholders only.
- Validate all incoming data at serializer/service boundaries.
- Enforce authorization in backend views/services/querysets; never trust frontend flags or hidden controls.
- Scope every user-owned object and nested relation to the authenticated user.
- Validate uploads by size, extension, MIME/content, storage policy, and safe filename; inspect existing `knowledge/file_validation.py` and related validators before extending.
- Sanitize untrusted HTML/Markdown before browser rendering.
- Protect WebSocket routes with authentication, origin controls, and user-specific groups.
- Use HTTPS and secure cookies/HSTS/host settings in production.
- Keep CORS allowlists explicit; do not enable allow-all origins in production.
- Do not log secrets, request bodies containing private data, full prompts, file contents, or query strings that may carry tokens.
- Avoid unsafe desktop automation actions; apply explicit user consent, permission policy, audit logging, and least privilege.
- Treat Codex project manifests/protected-item rules as governance constraints.
- Finance and other sensitive user domains require strict ownership, authorization, and response minimization.

## 16. Performance Standards

- Use pagination for potentially unbounded collections.
- Avoid N+1 queries; use `select_related` / `prefetch_related` after inspecting actual relations.
- Add indexes only when query patterns justify them; verify migration impact.
- Bound external HTTP calls and avoid blocking web workers on slow providers.
- Use Celery for appropriate long-running jobs.
- Avoid loading large datasets/files fully into browser memory when streaming/pagination/virtualization is available.
- Use Vue Query or established caching patterns consistently for server state; avoid duplicate caches with Pinia without a clear reason.
- Keep PWA caching rules from caching authenticated/private API responses unless a reviewed security policy explicitly allows it.
- Measure before adding caching or optimization complexity.

## 17. Error Handling & Observability

- Backend errors should use stable, structured API responses and correct HTTP status codes.
- Keep serializer validation errors distinguishable from authentication, permission, not-found, conflict, rate-limit, and provider failures.
- Frontend services should normalize errors centrally while preserving field-level validation details for forms.
- Views must expose actionable error states and retry affordances without leaking stack traces.
- Use bounded structured logs with request correlation where available.
- Do not log access tokens, refresh tokens, credentials, full private prompts, or uploaded content.
- The shared frontend API client emits request metadata and removes query/hash portions from URLs before telemetry events. Preserve that privacy behavior.
- Production must not display raw debug traces or sensitive provider response bodies.

## 18. Testing & Quality Standards

### Existing test tooling/evidence

Backend:
- Django test modules exist in the registered apps.
- The archive contains approximately 40 test-named Python files and 58 migration Python files.
- AI includes provider/security tests; knowledge includes metadata and file-validation tests; core includes API contract and settings-related tests.
- Django runtime test execution was not performed in this read-only archive audit.

Frontend:
- Vitest configuration and test files exist.
- Examples include goals store tests, Codex capability tests, and a basic component test.
- `package.json` scripts define `test:unit`, lint, format, and build.
- Frontend dependency installation/build was not performed during this audit.

### Commands (from manifests/scripts)

Frontend, from `frontend_vue/`:

```bash
npm ci
npm run dev
npm run build
npm run preview
npm run test:unit
npm run lint
npm run format
```

Note: the declared lint scripts use `--fix`; review the resulting diff before accepting lint changes. `npm run format` writes files.

Backend, from `backend_django/`:

```bash
python manage.py check
python manage.py test
python manage.py makemigrations --check --dry-run
python manage.py migrate --plan
python manage.py runserver
```

The above are standard Django commands; `migrate --plan` is read-only planning, while `migrate` applies schema changes and requires explicit authorization.

Project helper scripts exist at root `scripts/`:
- `run_backend.sh`
- `run_frontend.sh`
- `verify_release.sh`
- `check_frontend_imports.py`
- `verify_source.py`
- `validate_codex_release.py`

Inspect script contents before running because some verification scripts may write files or invoke commands.

### Required test strategy for changes

- Backend: model/service/serializer/view tests, permission tests, API contract tests, task tests, migration tests where schema changes.
- Frontend: component/store/service tests, validation/error-state tests, route guard tests, and build.
- Integration: authenticated API tests across the actual frontend/backend contract.
- AI: adapter mocks plus live-provider smoke tests only with approved credentials and explicit authorization.
- WebSockets: authentication, authorization, reconnect, group isolation.
- Automation: dry-run/permission tests before real desktop actions.
- State which tests ran, exact command, result, and environment. Never claim tests passed if they were not run.

## 19. Development Workflow

For every new feature or bug fix:

1. Read this document and the relevant domain's current source.
2. Inspect existing components, services, composables, stores, models, serializers, views, routes, tests, and migrations.
3. Identify the owner app and all cross-app consumers.
4. Trace the complete flow from UI to service to API to serializer/view/service/model and back.
5. Write down current behavior and the expected contract before editing.
6. Reuse installed libraries and shared components.
7. Make the smallest coherent change; avoid unrelated refactors.
8. Preserve backward compatibility unless a versioned contract change is approved.
9. Add/update tests at the layer where behavior is implemented.
10. Run relevant static checks, tests, and build.
11. Review `git diff` for unrelated changes, generated files, secrets, and lockfile churn.
12. Update documentation and API integration records when contracts or architecture change.
13. Report limitations and unverified behavior honestly.

### Read-only analysis mode

When the user asks for audit/documentation only:
- Do not edit application source, dependency manifests, lockfiles, database files, or environment configuration.
- Do not run migrations, database writes, destructive scripts, or real external actions.
- Create only the explicitly requested documentation artifact.
- Do not “fix while auditing.”

## 20. Build & Run Commands

### Frontend

Node engine declared in `frontend_vue/package.json`: `^22.18.0 || >=24.12.0`.

```bash
cd frontend_vue
npm ci
npm run dev
npm run build
npm run preview
```

### Backend

```bash
cd backend_django
python -m venv .venv
# Activate the environment using the platform-specific command.
pip install -r ../requirements.txt
python manage.py check
python manage.py runserver
```

Production database configuration must set `ENVIRONMENT=production`, `DATABASE_ENGINE=postgresql`, and the required PostgreSQL variables. Production secrets must be supplied through a secret manager/environment, not source control.

### Celery / Redis

Redis and Celery are configured in Django settings. Exact worker/beat invocation and deployment process are not documented in a confirmed deployment manifest. **UNKNOWN — REQUIRES VERIFICATION.** Typical commands should only be adopted after inspecting `backend_django/celery.py`, task autodiscovery, and the deployment environment.

### Deployment

No Docker Compose, Dockerfile, Nginx configuration, or CI workflow was identified in the inspected archive. Production deployment topology, static/media serving, process supervision, backups, and release rollback are **UNKNOWN — REQUIRES VERIFICATION**.

## 21. Library Governance

- Existing dependencies are shared project resources; use them anywhere their capability is needed, but do not load every library into every page.
- Prefer a shared wrapper/composable/service over repeated one-off implementations.
- Check `package.json`, `package-lock.json`, `requirements.txt`, imports, plugin registration, and runtime usage before proposing a dependency.
- Do not add a duplicate chart, editor, drag/drop, Markdown, validation, HTTP, or notification package without a documented technical reason.
- Do not change package versions or Python ranges as incidental cleanup.
- Never remove a package based only on a text search; check dynamic imports, config plugins, templates, scripts, and lockfile dependency relationships.
- After a dependency change, run reproducible install, compatibility checks, tests, and production build in an environment with network/package access.
- Document why each new package is necessary and which existing options were evaluated.

## 22. Feature Completion Checklist

A feature is not complete merely because files or routes exist. Use this checklist:

- [ ] Business requirement and ownership are clear.
- [ ] Model/schema and relationships are correct (if persistence is required).
- [ ] Migration is reviewed and reversible/operationally safe.
- [ ] Serializer/input validation is complete.
- [ ] Service/business logic is implemented and reusable.
- [ ] View/ViewSet and URL are registered.
- [ ] Authentication and object-level authorization are enforced.
- [ ] Querysets are scoped to the correct user/tenant.
- [ ] Side effects/tasks/events are handled safely and idempotently.
- [ ] Frontend service uses the shared API client and canonical endpoint.
- [ ] Store/composable and UI are connected to real backend data.
- [ ] Loading, empty, success, validation, permission, and error states exist.
- [ ] Responsive, RTL/LTR, and accessibility behavior is checked where relevant.
- [ ] Tests cover happy path, invalid input, permissions, and failure paths.
- [ ] API contract/integration documentation is updated.
- [ ] Build/checks/tests were run and their results recorded.
- [ ] External integration is smoke-tested only when credentials and approval exist.
- [ ] Feature status is reported accurately: COMPLETE, PARTIAL, INCOMPLETE, NOT CONNECTED, NOT IMPLEMENTED, or NOT VERIFIED.

## 23. Known Issues & Technical Debt (Evidence-based)

These are audit observations and verification needs, not automatic change requests:

1. **API base URL divergence:** `main.js` sets global Axios defaults with a root URL fallback while `services/api.js` uses an `/api` fallback. Multiple Axios-related service files exist. Trace and standardize deliberately.
2. **PrimeVue theme peer compatibility:** `primevue` is declared at major 5 while `@primevue/themes` is declared at major 4. Validate package-lock peer dependencies and actual runtime.
3. **Duplicate capability packages:** two drag/drop libraries, two Markdown approaches, and two rich-text editor packages are declared. Determine per-feature usage before consolidation.
4. **Potential unused Quill dependency:** no direct source reference was found in the static scan. Verify dynamic usage before removal.
5. **Codex duplicate route declarations:** the endpoint audit flags two duplicate Codex paths at project and app URL levels. Confirm Django resolver behavior and frontend expectations.
6. **Endpoint audit not runtime validated:** the 396-row audit is static; many records explicitly say runtime not tested or payload needs confirmation.
7. **MCP/Explain audit rows:** endpoint audit has entries for `mcp` and `explain`; these do not appear as registered apps in current `INSTALLED_APPS`. Trace exact implementation and URL inclusion.
8. **WebSocket coverage:** ASGI explicitly wires the core debug-console route; automation has separate consumer/routing files whose inclusion in the root router needs verification.
9. **Default in-memory Channels layer:** unsuitable for multi-process production real-time delivery unless Redis layer is configured.
10. **PWA metadata branding:** Vite manifest still has “Script Youtube” / “My Awesome App” copy.
11. **SCSS migration is incomplete by prior report:** `IMPLEMENTATION_AUDIT_REPORT_PRODUCTION.md` describes a new AI page stylesheet while retaining legacy styles for compatibility. Do not assume every view has an isolated stylesheet.
12. **Production runtime is not proven:** previous project reports state Django tests and frontend build were blocked in their environment due to missing dependencies/network restrictions. Re-run in a provisioned environment.
13. **Deployment infrastructure is not documented in the archive:** no Docker/Compose/Nginx/CI deployment files were identified.
14. **Archive packaging anomalies require review:** some archive paths appear to contain nested path segments whose names themselves end in `.vue` or `.md` (for example nested component-looking paths). Confirm the extracted working tree and original repository path layout before relying on every file path or running build tools.
15. **No Python lockfile / version pin:** `requirements.txt` contains ranges; exact runtime Python and installed package versions are unknown.

## 24. Non-Negotiable Rules

1. The current source code is the evidence; roadmap descriptions are not proof of implementation.
2. Never invent modules, routes, serializers, models, fields, environment variables, or response contracts.
3. Never claim a feature works without tests or direct runtime evidence.
4. Never expose secrets or copy `.env` values into docs/logs.
5. Never trust frontend authorization.
6. Never bypass user ownership scoping.
7. Never change database schema without migrations and approval.
8. Never modify protected Codex manifest items without explicit human approval.
9. Never introduce duplicate dependencies or parallel implementations without justification.
10. Never break the existing API contract without a coordinated migration plan.
11. Never remove compatibility modules before tracing all imports and external consumers.
12. Never run destructive commands, migrations, external provider calls, desktop automation, or production writes without explicit authorization.
13. Keep changes scoped; do not combine unrelated refactors with feature work.
14. Report tests not run and runtime assumptions clearly.

## 25. AI Agent Execution Protocol

At the start of every task, an AI coding agent must:

1. Read `AI_PROJECT_RULES.md`, `README.md`, and the relevant domain documentation.
2. Inspect `PROJECT_CONTEXT.json` and `project_manifest.json`; respect protected-item instructions.
3. Identify the exact app/module owning the requested behavior.
4. Inspect the actual files and imports before proposing edits.
5. Trace frontend consumer → service → endpoint → view → serializer → service/model → persistence/side effect.
6. Search for existing library/component/service capability before creating a new one.
7. Identify security, user-scope, migration, API compatibility, and cross-module impacts.
8. State assumptions as `INFERRED — NOT VERIFIED` and missing evidence as `UNKNOWN — REQUIRES VERIFICATION`.
9. Make no unrelated changes and do not silently broaden scope.
10. Run only safe, relevant checks authorized by the task.
11. Review the complete diff and verify no secrets/generated artifacts were introduced.
12. Deliver a concise report containing changed files, behavior, API/schema impact, tests run, tests not run, risks, and remaining verification.

### Required completion report format

```text
Task:
Owning module:
Files inspected:
Files changed:
API contract impact:
Database/migration impact:
Security/permission impact:
Tests/checks executed:
Tests/checks not executed:
Runtime/external verification:
Known limitations:
Final status: COMPLETE / PARTIAL / NOT VERIFIED
```

---

## Appendix A — Key project files

- `README.md` — product intent and roadmap context.
- `requirements.txt` — backend dependency ranges.
- `frontend_vue/package.json` — frontend scripts, dependencies, Node engine.
- `frontend_vue/package-lock.json` — npm lockfile.
- `frontend_vue/src/main.js` — frontend bootstrap/global registration.
- `frontend_vue/src/router/index.js` — frontend route table/guards.
- `frontend_vue/src/services/api.js` — shared Axios client and token refresh.
- `frontend_vue/src/services/endpoints.js` — endpoint builders.
- `backend_django/backend_django/settings.py` — Django apps, database, auth, Celery, Channels, security configuration.
- `backend_django/backend_django/urls.py` — root API URL registration.
- `backend_django/backend_django/asgi.py` — HTTP/WebSocket protocol routing.
- `backend_django/backend_django/wsgi.py` — WSGI entry point.
- `API_ENDPOINT_AUDIT.csv` — static API route inventory.
- `API_INTEGRATION_GUIDE.md` — documented frontend/backend mapping.
- `BACKEND_FRONTEND_INTEGRATION_MATRIX.md` — integration matrix.
- `FEATURE_REGISTER.csv` — feature register; roadmap/completeness must be verified against code.
- `IMPLEMENTATION_AUDIT_REPORT_PRODUCTION.md` — prior implementation and verification claims, not independent runtime proof.
- `PROJECT_CONTEXT.json`, `project_manifest.json` — Codex governance metadata.
- `scripts/` — run and verification helper scripts.

## Appendix B — Audit limitations

This document was generated from static inspection of the supplied ZIP. The audit did not:

- Install Python or npm dependencies.
- Run Django checks/tests or a frontend production build.
- Start PostgreSQL, Redis, Celery, Channels, or the Vite app.
- Call OpenAI, Gemini, Ollama, Google OAuth, GitHub, or other external services.
- Apply migrations or query the included SQLite database.
- Perform authenticated end-to-end tests.
- Verify production infrastructure, deployed environment variables, secrets, or live API responses.

Consequently, all runtime claims remain unverified unless explicitly supported by a separately recorded test result. Revalidate this document against the live repository whenever the architecture, dependencies, routes, or deployment configuration changes.


## 26. Module Dependency & Communication Rules

- `users_accounts` owns identity; domain apps must reference the configured custom user model through Django's swappable user mechanism rather than importing a concrete default user class.
- `core` is the shared infrastructure/domain support app; avoid turning it into a dumping ground for unrelated business logic.
- `ai` may support other domains (for example learning/goals/task planning), but domain ownership remains with the calling app. Keep AI orchestration separate from the persistence rules of the consuming domain.
- `knowledge` and `learning` have an explicitly documented integration in the API guide; Learning may call Knowledge through its domain service. Preserve ownership and permissions at both ends.
- `jobs_opportunity` contains scraping-related functionality while a separate `scraper` app also exists. Before adding a scraper feature, determine whether it belongs to generic source/run management or job-domain ingestion.
- `automation` and `codex` can cause operational side effects. Keep policy/permission checks at the action boundary and persist audit evidence where the existing model/service design supports it.
- Avoid importing views from other apps. Prefer stable service interfaces and serializers/contracts.
- For cross-app transactions, define transaction boundaries explicitly and test rollback behavior.

## 27. API Documentation & Contract Maintenance

- Update `API_ENDPOINT_AUDIT.csv`, `API_INTEGRATION_GUIDE.md`, and `BACKEND_FRONTEND_INTEGRATION_MATRIX.md` when a route, method, payload, response, or frontend consumer changes.
- Mark whether each route is statically declared, tested through API tests, or verified end-to-end. Do not use a generic “complete” status for all three.
- Keep examples aligned with real serializer fields and response envelopes.
- Record authentication and permission requirements for each sensitive endpoint.
- Record whether an endpoint is synchronous or returns a background task/run identifier.
- Identify deprecated/duplicate routes and provide a compatibility window before removal.
- Do not document undocumented behavior as a stable contract merely because a frontend currently depends on it; first verify and formalize it.

## 28. Runtime, Environment & Release Configuration

- Read `.env.example` for variable names and intended defaults, but never copy actual environment values into documentation.
- `ENVIRONMENT=production` triggers strict production settings, including PostgreSQL-only database selection and minimum secret requirements.
- Production must use explicit `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`, HTTPS/security settings, and managed secrets.
- Confirm Redis availability and configure the Redis Channels backend when multi-process WebSocket support is required.
- Confirm Celery worker and beat process configuration independently from Django web startup.
- Validate static/media storage and serving outside Django's development static helper before production.
- Release validation must include backend checks/tests, migration plan review, frontend clean install/build/tests, API smoke tests, and rollback readiness.
- The uploaded archive did not provide a verified deployment topology; never invent a production command, container service name, or hosting provider.

## 29. Audit Findings & Verification Register

| Finding | Evidence | Required next verification |
|---|---|---|
| API inventory contains 396 rows | `API_ENDPOINT_AUDIT.csv` | Run authenticated API contract tests and reconcile missing/duplicate rows |
| 17 domain apps registered | Django `INSTALLED_APPS` | Verify app startup and migrations in provisioned environment |
| PostgreSQL is required in production mode | `settings.py` guard | Verify production environment values and successful DB connection |
| SQLite is the default non-production engine | `settings.py` | Confirm local developer setup; do not infer deployment engine |
| JWT refresh rotation is enabled | SimpleJWT settings and frontend client | Exercise concurrent refresh and blacklisted-token behavior |
| Redis/Celery configured | Django settings and task modules | Start broker/worker/beat and test task lifecycle |
| Channels ASGI route exists | `asgi.py`, `core.debug_console.routing` | Verify auth and route coverage; inspect automation routing inclusion |
| Frontend dependencies declared | `package.json` and lockfile | `npm ci`, peer checks, test and production build |
| Prior audit reports cite blocked runtime checks | `IMPLEMENTATION_AUDIT_REPORT_PRODUCTION.md`, `IMPLEMENTATION_NOTES.md` | Re-run in a network-enabled environment with dependencies |
| Archive has path-layout anomalies | ZIP member names and extracted layout | Compare against the source repository before treating anomalous paths as canonical |

No item in this register should be considered fixed merely because it is documented here.

## 30. Document Ownership & Update Policy

`AI_PROJECT_RULES.md` is a maintained engineering reference, not a substitute for code review or tests.

Update it when any of the following changes:
- Django app registration, root URL routing, or app ownership.
- Frontend architecture, route/layout conventions, or shared API client.
- Dependency declarations, lockfiles, or supported runtime versions.
- Database engine, model relationships, migration strategy, or storage.
- Authentication, authorization, token lifecycle, or security controls.
- AI providers, credential handling, tool/action permissions, or background execution.
- Celery/Redis/Channels topology.
- Build, test, release, or deployment procedures.

Every update must cite concrete repository paths and distinguish confirmed facts from inferred or unverified behavior. Remove stale statements rather than accumulating contradictory instructions. The source tree and executable configuration remain authoritative if this document becomes stale.



