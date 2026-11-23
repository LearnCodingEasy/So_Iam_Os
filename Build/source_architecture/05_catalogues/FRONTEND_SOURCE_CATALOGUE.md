# Frontend Source Catalogue

> Static file and router inventory. Frontend files: 358; Vue SFCs: 142; route declarations extracted: 44. These are counts of the supplied archive.

## Router declarations

| Path | Route name | Component expression |
|---|---|---|
| `/` | `home` | `HomeView` |
| `/About` | `About` | `AboutView` |
| `/login` | `login` | `LoginView` |
| `/auth-callback` | `AuthCallback` | `AuthCallback,` |
| `/profile/:id` | `profile` | `ProfileView` |
| `/knowledge` | `knowledge` | `() => import('../views/knowledge/knowledgeView.vue')` |
| `/learning` | `learning` | `LearningView` |
| `/learning/topics/:topicId` | `learning-topic` | `() => import('@/views/learning/LearningTopic.vue')` |
| `/goals` | `goals` | `GoalsView` |
| `/tasks/today` | `today-tasks` | `TodayTasksView` |
| `/progress` | `progress` | `MyProgressView` |
| `/jobs` | `jobs` | `JobsView` |
| `/scraper` | `scraper` | `ScraperView` |
| `/tasks` | `tasks` | `TasksCalendar` |
| `/codex` | `codex` | `CodexView` |
| `/projects` | `projects` | `ProjectsView` |
| `/challenges` | `challenges` | `ChallengesView` |
| `/finance` | `finance` | `FinanceView` |
| `/agents` | `agents` | `AgentsView` |
| `/ai-tools` | `ai-tools-laboratory` | `AiToolsLaboratoryView` |
| `/analytics` | `analytics` | `AnalyticsView` |
| `/architecture` | `architecture` | `ArchitectureView` |
| `/crm` | `crm` | `CrmView` |
| `/marketing` | `marketing` | `MarketingView` |
| `/revenue` | `revenue` | `RevenueView` |
| `/sales` | `sales` | `SalesView` |
| `/memory` | `memory` | `MemoryView` |
| `/ai/agents` | `ai-agents` | `AgentPlanner` |
| `/social` | `social` | `SocialView` |
| `/notifications` | `notifications` | `NotificationsView` |
| `/system/frontend` | `frontend-enhancements` | `FrontendEnhancementCenter` |
| `/settings` | `settings` | `SettingsView` |
| `/ai` | `ai-chat` | `AIChat` |
| `/ai/control` | `ai-control` | `AIControl` |
| `/ai/operations` | `ai-operations` | `() => import('@/views/ai/AIOperationsView.vue')` |
| `/dashboard` | `dashboard` | `Dashboard` |
| `/automation` | `automation` | `Automation` |
| `/automation_Dashboard` | `automation_Dashboard` | `automation_Dashboard` |
| `/automation_ProgramList` | `automation_ProgramList` | `ProgramList` |
| `/automation_programs_create` | `automation_programs_create` | `ProgramCreate` |
| `/automation/:id` | `automation_programs_edit` | `ProgramEdit` |
| `/automation_TaskCreate` | `automation_TaskCreate` | `TaskCreate` |
| `/automation_TaskEditor` | `automation_TaskEditor` | `TaskEditor` |
| `/:catchAll(.*)` | `NotFound` | `NotFound,` |

## Frontend structure

- `src/views/`: 53 files.
- `src/components/`: 93 files.
- `src/services/`: 41 files.
- `src/stores/`: 32 files.
- `src/router/`: 1 files.
- `src/composables/`: 9 files.
- `src/utils/`: 1 files.