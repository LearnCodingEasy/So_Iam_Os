# Project Feature Registry

> **Evidence discipline:** entries below are source declarations, not proof of end-to-end working features. `DECLARED` means a route/mount exists in the supplied source. `NOT_RUNTIME_VERIFIED` means no runtime behavior was tested. Feature completeness must be upgraded only after tracing UI → service → API → permission → model/task and verifying tests or runtime.

## Frontend route registry

| Route name | Path | Component | Evidence status | Runtime status |
|---|---|---|---|---|
| `/` | `home` | `HomeView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/About` | `About` | `AboutView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/login` | `login` | `LoginView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/auth-callback` | `AuthCallback` | `AuthCallback,` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/profile/:id` | `profile` | `ProfileView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/knowledge` | `knowledge` | `() => import('../views/knowledge/knowledgeView.vue')` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/learning` | `learning` | `LearningView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/learning/topics/:topicId` | `learning-topic` | `() => import('@/views/learning/LearningTopic.vue')` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/goals` | `goals` | `GoalsView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/tasks/today` | `today-tasks` | `TodayTasksView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/progress` | `progress` | `MyProgressView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/jobs` | `jobs` | `JobsView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/scraper` | `scraper` | `ScraperView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/tasks` | `tasks` | `TasksCalendar` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/codex` | `codex` | `CodexView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/projects` | `projects` | `ProjectsView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/challenges` | `challenges` | `ChallengesView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/finance` | `finance` | `FinanceView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/agents` | `agents` | `AgentsView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/ai-tools` | `ai-tools-laboratory` | `AiToolsLaboratoryView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/analytics` | `analytics` | `AnalyticsView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/architecture` | `architecture` | `ArchitectureView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/crm` | `crm` | `CrmView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/marketing` | `marketing` | `MarketingView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/revenue` | `revenue` | `RevenueView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/sales` | `sales` | `SalesView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/memory` | `memory` | `MemoryView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/ai/agents` | `ai-agents` | `AgentPlanner` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/social` | `social` | `SocialView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/notifications` | `notifications` | `NotificationsView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/system/frontend` | `frontend-enhancements` | `FrontendEnhancementCenter` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/settings` | `settings` | `SettingsView` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/ai` | `ai-chat` | `AIChat` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/ai/control` | `ai-control` | `AIControl` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/ai/operations` | `ai-operations` | `() => import('@/views/ai/AIOperationsView.vue')` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/dashboard` | `dashboard` | `Dashboard` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/automation` | `automation` | `Automation` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/automation_Dashboard` | `automation_Dashboard` | `automation_Dashboard` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/automation_ProgramList` | `automation_ProgramList` | `ProgramList` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/automation_programs_create` | `automation_programs_create` | `ProgramCreate` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/automation/:id` | `automation_programs_edit` | `ProgramEdit` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/automation_TaskCreate` | `automation_TaskCreate` | `TaskCreate` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/automation_TaskEditor` | `automation_TaskEditor` | `TaskEditor` | DECLARED | NOT_RUNTIME_VERIFIED |
| `/:catchAll(.*)` | `NotFound` | `NotFound,` | DECLARED | NOT_RUNTIME_VERIFIED |

## Backend API app mounts

The archive contains 26 app-like directories; 25 are registered in `INSTALLED_APPS`. The `skills/` scaffold is not registered and has no API mount. The actual `Skill` entity is defined in the `learning` app.

| App | Prefix | Included URL module | Evidence status |
|---|---|---|---|
| `agents` | `/api/agents/` | `agents.api.urls` (root include expression) | DECLARED |
| `ai` | `/api/ai/` | `ai.api.urls` (root include expression) | DECLARED |
| `ai_tools_laboratory` | `/api/ai-tools/` | `ai_tools_laboratory.api.urls` (root include expression) | DECLARED |
| `allauth` | `/accounts/` | `allauth.api.urls` (root include expression) | DECLARED |
| `analytics` | `/api/analytics/` | `analytics.api.urls` (root include expression) | DECLARED |
| `architecture` | `/api/architecture/` | `architecture.api.urls` (root include expression) | DECLARED |
| `automation` | `/api/automation/` | `automation.api.urls` (root include expression) | DECLARED |
| `challenges` | `/api/challenges/` | `challenges.api.urls` (root include expression) | DECLARED |
| `codex` | `/api/codex/` | `codex.api.urls` (root include expression) | DECLARED |
| `core` | `/api/core/` | `core.api.urls` (root include expression) | DECLARED |
| `crm` | `/api/crm/` | `crm.api.urls` (root include expression) | DECLARED |
| `goals` | `/api/goals/` | `goals.api.urls` (root include expression) | DECLARED |
| `jobs_opportunity` | `/api/jobs/` | `jobs_opportunity.api.urls` (root include expression) | DECLARED |
| `knowledge` | `/api/knowledge/` | `knowledge.api.urls` (root include expression) | DECLARED |
| `learning` | `/api/learning/` | `learning.api.urls` (root include expression) | DECLARED |
| `marketing` | `/api/marketing/` | `marketing.api.urls` (root include expression) | DECLARED |
| `memory` | `/api/memory/` | `memory.api.urls` (root include expression) | DECLARED |
| `notification` | `/api/notifications/` | `notification.api.urls` (root include expression) | DECLARED |
| `personal_finance` | `/api/finance/` | `personal_finance.api.urls` (root include expression) | DECLARED |
| `projects` | `/api/projects/` | `projects.api.urls` (root include expression) | DECLARED |
| `revenue` | `/api/revenue/` | `revenue.api.urls` (root include expression) | DECLARED |
| `sales` | `/api/sales/` | `sales.api.urls` (root include expression) | DECLARED |
| `scraper` | `/api/scraper/` | `scraper.api.urls` (root include expression) | DECLARED |
| `social` | `/api/social/` | `social.api.urls` (root include expression) | DECLARED |
| `tasks` | `/api/tasks/` | `tasks.api.urls` (root include expression) | DECLARED |
| `users_accounts` | `/api/users/` | `users_accounts.api.urls` (root include expression) | DECLARED |

## Feature status taxonomy

| Status | Meaning | Minimum evidence to assign |
|---|---|---|
| `IMPLEMENTED_VERIFIED` | End-to-end behavior demonstrated | UI/service/API/model plus passing focused tests or recorded runtime verification |
| `PARTIAL` | Some layers exist, required workflow incomplete | Explicit missing layer(s) recorded |
| `IN_PROGRESS` | Active implementation evidenced | Current task/branch/owner evidence |
| `PLANNED` | Approved but absent from source | Approved specification/decision |
| `BROKEN` | Reproducible failure | Reproduction steps and failing test/log |
| `NOT_VERIFIED` | Evidence insufficient | Default status until traced |

## Rules

- A frontend route is not an implemented feature by itself.
- An API URL include is not an endpoint count; expand nested routers and decorators before claiming operations.
- A model class is not proof of UI or API support.
- Do not convert the project vision in README into an implementation claim.
- Add one row per user-visible capability only after source tracing; attach exact source paths and test evidence.