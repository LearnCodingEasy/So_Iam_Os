# So_Iam_Os — Project Structure & Architecture Standard

**Document:** `Project_structure.md`  
**Project:** So_Iam_Os  
**Frontend:** Vue.js  
**Backend:** Python, Django, Django REST Framework  
**Architecture:** Modular Application Architecture  
**Applications:** 25

---

# 1. PROJECT ARCHITECTURE PRINCIPLES

So_Iam_Os consists of 25 independent but interconnected applications.

Each application must have:

- A clearly defined responsibility.
- Its own frontend services.
- Its own Pinia store.
- Its own Vue views.
- Its own Django models.
- Its own API.
- Its own serializers.
- Its own business services.
- Its own validators.
- Its own background tasks when needed.
- Its own tests.

## 1.1 Frontend Architecture

The frontend follows this structure:

```text
Frontend/
│
├── services/
│   └── <Application_Name>/
│       └── <Application_Name>.js
│
├── stores/
│   └── <application_name>/
│       └── <applicationName>Store.js
│
└── views/
    └── <application_name>/
        └── <applicationName>View.vue
```

### Frontend responsibilities

| Directory | Responsibility                                     |
| --------- | -------------------------------------------------- |
| services  | API communication and frontend business operations |
| stores    | Centralized application state using Pinia          |
| views     | User interface and page-level presentation         |

Rules:

1. API requests must be handled through services.
2. Pinia stores must manage application state.
3. Views must consume stores and services rather than duplicate API logic.
4. Do not place backend business logic inside Vue components.
5. Do not duplicate API endpoints across applications.
6. Use consistent naming conventions.

## 1.2 Backend Architecture

Every Django application follows this standard:

```text
<application_name>/
│
├── migrations/
│   └── __init__.py
│
├── models/
│   ├── __init__.py
│   └── domain_models.py
│
├── api/
│   ├── __init__.py
│   │
│   ├── views/
│   │   ├── __init__.py
│   │   └── domain_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── domain_serializers.py
│   │
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   └── domain_service.py
│
├── validators/
│   ├── __init__.py
│   └── domain_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── domain_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

### Backend responsibilities

| Directory       | Responsibility                            |
| --------------- | ----------------------------------------- |
| migrations      | Database schema changes                   |
| models          | Database entities and relationships       |
| api/views       | HTTP request handling                     |
| api/serializers | Input validation and data representation  |
| api/urls.py     | Application API routing                   |
| services        | Business logic and application operations |
| validators      | Domain-specific validation                |
| tasks           | Background and asynchronous operations    |
| tests           | Automated testing                         |
| admin.py        | Django Admin configuration                |
| apps.py         | Django application configuration          |

### Backend rules

1. Views must remain lightweight.
2. Business logic belongs in services.
3. Models must represent the application's domain.
4. Serializers must validate API input and output.
5. Validators must handle reusable domain validation.
6. Tasks must handle background operations when necessary.
7. Models belonging to another application must not be duplicated.
8. Cross-application relationships must use explicit Django relationships or well-defined service/API contracts.
9. Every application must have independent tests.
10. Do not create unnecessary files or empty architectural layers.

---

# 2. APPLICATIONS MASTER LIST

The project contains the following 25 applications:

```python
SO_IAM_OS_APPLICATIONS = [
    "agents",
    "ai",
    "ai_tools_laboratory",
    "analytics",
    "architecture",
    "automation",
    "challenges",
    "codex",
    "core",
    "crm",
    "goals",
    "jobs_opportunity",
    "knowledge",
    "learning",
    "marketing",
    "memory",
    "notification",
    "personal_finance",
    "projects",
    "revenue",
    "sales",
    "scraper",
    "social",
    "tasks",
    "users_accounts",
]
```

---

# 3. FRONTEND — COMPLETE APPLICATION STRUCTURE

All applications must follow the same frontend architectural pattern.

```text
Frontend/
│
├── services/
│   │
│   ├── Agents/
│   │   └── Agents.js
│   │
│   ├── AI/
│   │   └── AI.js
│   │
│   ├── AI_Tools_Laboratory/
│   │   └── AI_Tools_Laboratory.js
│   │
│   ├── Analytics/
│   │   └── Analytics.js
│   │
│   ├── Architecture/
│   │   └── Architecture.js
│   │
│   ├── Automation/
│   │   └── Automation.js
│   │
│   ├── Challenges/
│   │   └── Challenges.js
│   │
│   ├── Codex/
│   │   └── Codex.js
│   │
│   ├── Core/
│   │   └── Core.js
│   │
│   ├── CRM/
│   │   └── CRM.js
│   │
│   ├── Goals/
│   │   └── Goals.js
│   │
│   ├── Jobs_Opportunity/
│   │   └── Jobs_Opportunity.js
│   │
│   ├── Knowledge/
│   │   └── Knowledge.js
│   │
│   ├── Learning/
│   │   └── Learning.js
│   │
│   ├── Marketing/
│   │   └── Marketing.js
│   │
│   ├── Memory/
│   │   └── Memory.js
│   │
│   ├── Notification/
│   │   └── Notification.js
│   │
│   ├── Personal_Finance/
│   │   └── Personal_Finance.js
│   │
│   ├── Projects/
│   │   └── Projects.js
│   │
│   ├── Revenue/
│   │   └── Revenue.js
│   │
│   ├── Sales/
│   │   └── Sales.js
│   │
│   ├── Scraper/
│   │   └── Scraper.js
│   │
│   ├── Social/
│   │   └── Social.js
│   │
│   ├── Tasks/
│   │   └── Tasks.js
│   │
│   └── Users_Accounts/
│       └── Users_Accounts.js
│
├── stores/
│   │
│   ├── agents/
│   │   └── agentsStore.js
│   │
│   ├── ai/
│   │   └── aiStore.js
│   │
│   ├── ai_tools_laboratory/
│   │   └── aiToolsLaboratoryStore.js
│   │
│   ├── analytics/
│   │   └── analyticsStore.js
│   │
│   ├── architecture/
│   │   └── architectureStore.js
│   │
│   ├── automation/
│   │   └── automationStore.js
│   │
│   ├── challenges/
│   │   └── challengesStore.js
│   │
│   ├── codex/
│   │   └── codexStore.js
│   │
│   ├── core/
│   │   └── coreStore.js
│   │
│   ├── crm/
│   │   └── crmStore.js
│   │
│   ├── goals/
│   │   └── goalsStore.js
│   │
│   ├── jobs_opportunity/
│   │   └── jobsOpportunityStore.js
│   │
│   ├── knowledge/
│   │   └── knowledgeStore.js
│   │
│   ├── learning/
│   │   └── learningStore.js
│   │
│   ├── marketing/
│   │   └── marketingStore.js
│   │
│   ├── memory/
│   │   └── memoryStore.js
│   │
│   ├── notification/
│   │   └── notificationStore.js
│   │
│   ├── personal_finance/
│   │   └── personalFinanceStore.js
│   │
│   ├── projects/
│   │   └── projectsStore.js
│   │
│   ├── revenue/
│   │   └── revenueStore.js
│   │
│   ├── sales/
│   │   └── salesStore.js
│   │
│   ├── scraper/
│   │   └── scraperStore.js
│   │
│   ├── social/
│   │   └── socialStore.js
│   │
│   ├── tasks/
│   │   └── tasksStore.js
│   │
│   └── users_accounts/
│       └── usersAccountsStore.js
│
└── views/
    │
    ├── agents/
    │   └── agentsView.vue
    │
    ├── ai/
    │   └── aiView.vue
    │
    ├── ai_tools_laboratory/
    │   └── aiToolsLaboratoryView.vue
    │
    ├── analytics/
    │   └── analyticsView.vue
    │
    ├── architecture/
    │   └── architectureView.vue
    │
    ├── automation/
    │   └── automationView.vue
    │
    ├── challenges/
    │   └── challengesView.vue
    │
    ├── codex/
    │   └── codexView.vue
    │
    ├── core/
    │   └── coreView.vue
    │
    ├── crm/
    │   └── crmView.vue
    │
    ├── goals/
    │   └── goalsView.vue
    │
    ├── jobs_opportunity/
    │   └── jobsOpportunityView.vue
    │
    ├── knowledge/
    │   └── knowledgeView.vue
    │
    ├── learning/
    │   └── learningView.vue
    │
    ├── marketing/
    │   └── marketingView.vue
    │
    ├── memory/
    │   └── memoryView.vue
    │
    ├── notification/
    │   └── notificationView.vue
    │
    ├── personal_finance/
    │   └── personalFinanceView.vue
    │
    ├── projects/
    │   └── projectsView.vue
    │
    ├── revenue/
    │   └── revenueView.vue
    │
    ├── sales/
    │   └── salesView.vue
    │
    ├── scraper/
    │   └── scraperView.vue
    │
    ├── social/
    │   └── socialView.vue
    │
    ├── tasks/
    │   └── tasksView.vue
    │
    └── users_accounts/
        └── usersAccountsView.vue
```

---

# 4. BACKEND — APPLICATION STRUCTURE

Each Django application follows the common backend standard defined in Section 1.2.

The following sections specify the domain-specific files and responsibilities for each application.

## 4.1 agents

**Purpose:** Manage AI agents, configurations, executions, and orchestration.

```text
agents/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── agent.py
│   ├── agent_configuration.py
│   ├── agent_execution.py
│   └── agent_run.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── agent_views.py
│   │   └── execution_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── agent_serializers.py
│   │   └── execution_serializers.py
│   ├── urls.py
│
├── services/
│   ├── __init__.py
│   ├── agent_service.py
│   ├── execution_service.py
│   └── orchestration_service.py
│
├── validators/
│   ├── __init__.py
│   └── agent_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── agent_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   ├── test_execution.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.2 ai

**Purpose:** Manage AI providers, models, requests, and AI integrations.

```text
ai/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── ai_model.py
│   ├── ai_provider.py
│   └── ai_request.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── ai_views.py
│   │   └── provider_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── ai_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── ai_service.py
│   ├── provider_service.py
│   └── request_service.py
│
├── validators/
│   ├── __init__.py
│   └── ai_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── ai_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.3 ai_tools_laboratory

**Purpose:** Manage AI tools, categories, configurations, and tool executions.

```text
ai_tools_laboratory/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── tool.py
│   ├── tool_category.py
│   ├── tool_configuration.py
│   └── tool_execution.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── tool_views.py
│   │   ├── category_views.py
│   │   └── execution_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── tool_serializers.py
│   │   └── execution_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── tool_service.py
│   ├── catalog_service.py
│   └── execution_service.py
│
├── validators/
│   ├── __init__.py
│   └── tool_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── tool_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   ├── test_execution.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.4 analytics

**Purpose:** Collect, process, and analyze system and business metrics.

```text
analytics/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── metric.py
│   ├── metric_snapshot.py
│   ├── report.py
│   └── analytics_event.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── metric_views.py
│   │   └── report_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── metric_serializers.py
│   │   └── report_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── analytics_service.py
│   ├── metric_service.py
│   └── reporting_service.py
│
├── validators/
│   ├── __init__.py
│   └── analytics_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── analytics_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.5 architecture

**Purpose:** Manage system architecture, components, dependencies, and architecture decisions.

```text
architecture/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── architecture.py
│   ├── architecture_decision.py
│   ├── component.py
│   └── dependency.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── architecture_views.py
│   │   └── decision_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── architecture_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── architecture_service.py
│   └── decision_service.py
│
├── validators/
│   ├── __init__.py
│   └── architecture_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── architecture_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.6 automation

**Purpose:** Manage workflows, triggers, steps, and automated executions.

```text
automation/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── workflow.py
│   ├── workflow_step.py
│   ├── trigger.py
│   └── execution.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── workflow_views.py
│   │   └── execution_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── workflow_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── workflow_service.py
│   ├── trigger_service.py
│   └── execution_service.py
│
├── validators/
│   ├── __init__.py
│   └── workflow_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── workflow_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_workflows.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.7 challenges

**Purpose:** Manage practical challenges, steps, submissions, and evaluation.

```text
challenges/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── challenge.py
│   ├── challenge_step.py
│   └── submission.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── challenge_views.py
│   │   └── submission_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── challenge_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── challenge_service.py
│   └── submission_service.py
│
├── validators/
│   ├── __init__.py
│   └── challenge_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── challenge_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.8 codex

**Purpose:** Store reusable code, examples, snippets, and technical resources.

```text
codex/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── code_snippet.py
│   ├── code_example.py
│   └── code_language.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   └── codex_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── codex_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── codex_service.py
│   └── code_execution_service.py
│
├── validators/
│   ├── __init__.py
│   └── code_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── codex_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_execution.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.9 core

**Purpose:** Provide shared system infrastructure and common domain-independent functionality.

```text
core/
│
├── migrations/
├── models/
│   ├── __init__.py
│   └── core_models.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   └── core_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── core_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   └── core_service.py
│
├── validators/
│   ├── __init__.py
│   └── core_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── core_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.10 crm

**Purpose:** Manage contacts, customer relationships, interactions, and customer pipelines.

```text
crm/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── contact.py
│   ├── company.py
│   ├── interaction.py
│   └── customer_relationship.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── contact_views.py
│   │   └── interaction_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── crm_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── contact_service.py
│   ├── interaction_service.py
│   └── customer_service.py
│
├── validators/
│   ├── __init__.py
│   └── crm_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── crm_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.11 goals

**Purpose:** Manage personal and business goals, milestones, and progress.

```text
goals/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── goal.py
│   ├── milestone.py
│   └── goal_progress.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   └── goal_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── goal_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   └── goal_service.py
│
├── validators/
│   ├── __init__.py
│   └── goal_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── goal_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.12 jobs_opportunity

**Purpose:** Discover and manage jobs, freelance opportunities, and business opportunities.

```text
jobs_opportunity/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── job.py
│   ├── opportunity.py
│   ├── source.py
│   └── application.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── job_views.py
│   │   ├── opportunity_views.py
│   │   └── application_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── job_serializers.py
│   │   └── opportunity_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── job_service.py
│   ├── opportunity_service.py
│   └── application_service.py
│
├── validators/
│   ├── __init__.py
│   └── opportunity_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── opportunity_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.13 knowledge

**Purpose:** Manage knowledge items, documents, files, and knowledge sources.

```text
knowledge/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── document.py
│   └── knowledge_base.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── document_views.py
│   │   └── knowledge_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── document_serializers.py
│   │   └── knowledge_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── document_service.py
│   ├── knowledge_service.py
│   └── file_service.py
│
├── validators/
│   ├── __init__.py
│   └── file_validator.py
│
├── extractors/
│   ├── __init__.py
│   ├── metadata_extractor.py
│   └── text_extractor.py
│
├── tasks/
│   ├── __init__.py
│   └── document_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   ├── test_views.py
│   ├── test_file_validation.py
│   └── test_metadata_extractor.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.14 learning

**Purpose:** Transform knowledge into structured learning paths, topics, steps, and applications.

```text
learning/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── learning_path.py
│   ├── learning_topic.py
│   ├── learning_step.py
│   ├── learning_note.py
│   └── learning_application.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── path_views.py
│   │   ├── topic_views.py
│   │   └── application_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── path_serializers.py
│   │   ├── topic_serializers.py
│   │   └── application_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── learning_service.py
│   ├── topic_service.py
│   └── application_service.py
│
├── validators/
│   ├── __init__.py
│   └── learning_validator.py
│
├── extractors/
│   ├── __init__.py
│   └── lesson_extractor.py
│
├── tasks/
│   ├── __init__.py
│   └── learning_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.15 marketing

**Purpose:** Manage marketing strategies, campaigns, content promotion, and lead generation.

```text
marketing/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── campaign.py
│   ├── marketing_channel.py
│   ├── marketing_content.py
│   └── lead_source.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── campaign_views.py
│   │   └── marketing_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── marketing_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── campaign_service.py
│   ├── marketing_service.py
│   └── lead_generation_service.py
│
├── validators/
│   ├── __init__.py
│   └── marketing_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── marketing_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.16 memory

**Purpose:** Store and retrieve contextual information and user memories for AI operations.

```text
memory/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── memory.py
│   ├── memory_item.py
│   ├── memory_context.py
│   └── memory_embedding.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   └── memory_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── memory_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── memory_service.py
│   ├── context_service.py
│   └── retrieval_service.py
│
├── validators/
│   ├── __init__.py
│   └── memory_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── memory_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_retrieval.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.17 notification

**Purpose:** Manage notifications, delivery, preferences, and notification history.

```text
notification/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── notification.py
│   ├── notification_type.py
│   ├── notification_preference.py
│   └── notification_delivery.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── notification_views.py
│   │   └── preference_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── notification_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── notification_service.py
│   ├── delivery_service.py
│   └── preference_service.py
│
├── validators/
│   ├── __init__.py
│   └── notification_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── notification_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.18 personal_finance

**Purpose:** Manage personal income, expenses, budgets, savings, and financial planning.

```text
personal_finance/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── financial_account.py
│   ├── transaction.py
│   ├── budget.py
│   └── savings_goal.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── account_views.py
│   │   ├── transaction_views.py
│   │   └── budget_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── finance_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── finance_service.py
│   ├── transaction_service.py
│   └── budget_service.py
│
├── validators/
│   ├── __init__.py
│   └── finance_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── finance_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.19 projects

**Purpose:** Manage projects, project members, resources, and project progress.

```text
projects/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── project.py
│   ├── project_member.py
│   └── project_resource.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── project_views.py
│   │   └── member_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── project_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   └── project_service.py
│
├── validators/
│   ├── __init__.py
│   └── project_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── project_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.20 revenue

**Purpose:** Manage business revenue, income sources, revenue records, and recurring revenue.

```text
revenue/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── revenue_record.py
│   ├── revenue_source.py
│   ├── revenue_stream.py
│   └── recurring_revenue.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── revenue_views.py
│   │   └── source_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── revenue_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── revenue_service.py
│   ├── attribution_service.py
│   └── recurring_revenue_service.py
│
├── validators/
│   ├── __init__.py
│   └── revenue_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── revenue_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.21 sales

**Purpose:** Manage sales opportunities, offers, deals, and transactions.

```text
sales/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── deal.py
│   ├── offer.py
│   ├── sale.py
│   └── sales_activity.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── deal_views.py
│   │   └── sales_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── sales_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── sales_service.py
│   ├── deal_service.py
│   └── offer_service.py
│
├── validators/
│   ├── __init__.py
│   └── sales_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── sales_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.22 scraper

**Purpose:** Collect and process external data from authorized sources.

```text
scraper/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── scraping_source.py
│   ├── scraping_job.py
│   ├── scraped_record.py
│   └── scraping_execution.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── source_views.py
│   │   └── scraping_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── scraper_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── scraper_service.py
│   ├── source_service.py
│   └── extraction_service.py
│
├── validators/
│   ├── __init__.py
│   └── scraper_validator.py
│
├── extractors/
│   ├── __init__.py
│   └── data_extractor.py
│
├── tasks/
│   ├── __init__.py
│   └── scraper_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_extractors.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.23 social

**Purpose:** Manage social media accounts, posts, publishing, and engagement.

```text
social/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── social_account.py
│   ├── social_post.py
│   ├── social_platform.py
│   └── social_engagement.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── account_views.py
│   │   └── post_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── social_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── social_service.py
│   ├── publishing_service.py
│   └── engagement_service.py
│
├── validators/
│   ├── __init__.py
│   └── social_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── social_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.24 tasks

**Purpose:** Manage tasks, dependencies, assignments, and task execution.

```text
tasks/
│
├── migrations/
├── models/
│   ├── __init__.py
│   ├── task.py
│   ├── task_dependency.py
│   └── task_execution.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── task_views.py
│   │   └── execution_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── task_serializers.py
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── task_service.py
│   └── execution_service.py
│
├── validators/
│   ├── __init__.py
│   └── task_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── task_workers.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

## 4.25 users_accounts

**Purpose:** Manage users, profiles, accounts, authentication, and access control.

```text
users_accounts/
│
├── migrations/
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── profile.py
│   └── account.py
│
├── api/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── user_views.py
│   │   ├── profile_views.py
│   │   └── account_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── user_serializers.py
│   │   ├── profile_serializers.py
│   │   └── account_serializers.py
│   │
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── user_service.py
│   ├── profile_service.py
│   └── account_service.py
│
├── validators/
│   ├── __init__.py
│   └── account_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── account_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
│
├── admin.py
├── apps.py
└── __init__.py
```

---

# 5. APPLICATION RESPONSIBILITY MATRIX

| Application         | Primary responsibility        | Main outputs                |
| ------------------- | ----------------------------- | --------------------------- |
| agents              | AI agent execution            | Agent results               |
| ai                  | AI integration                | AI responses                |
| ai_tools_laboratory | AI tool management            | Tool catalog and executions |
| analytics           | Measurement                   | Metrics and insights        |
| architecture        | System design                 | Architecture decisions      |
| automation          | Workflow execution            | Automated processes         |
| challenges          | Practical evaluation          | Submissions and results     |
| codex               | Reusable technical knowledge  | Code assets                 |
| core                | Shared infrastructure         | Common services             |
| crm                 | Customer relationships        | Contacts and interactions   |
| goals               | Objectives and milestones     | Goals and progress          |
| jobs_opportunity    | Market opportunities          | Jobs and opportunities      |
| knowledge           | Knowledge management          | Knowledge records           |
| learning            | Learning management           | Learning paths and topics   |
| marketing           | Marketing operations          | Campaigns and leads         |
| memory              | Context management            | Memories and context        |
| notification        | Notifications                 | Delivered notifications     |
| personal_finance    | Personal financial management | Financial records           |
| projects            | Project management            | Projects and resources      |
| revenue             | Business revenue              | Revenue records             |
| sales               | Sales management              | Deals and sales             |
| scraper             | External data collection      | Collected records           |
| social              | Social media management       | Posts and engagement        |
| tasks               | Work management               | Tasks and execution         |
| users_accounts      | User management               | Users and accounts          |

---

# 6. APPLICATION RELATIONSHIPS

The applications must work together as one integrated ecosystem.

## 6.1 AI & Intelligence Layer

```text
users_accounts
      ↓
core
      ↓
ai
      ↕
memory
      ↕
agents
      ↕
ai_tools_laboratory
```

## 6.2 Knowledge & Learning Layer

```text
knowledge
    ↓
learning
    ↓
challenges
    ↓
codex
    ↓
projects
```

## 6.3 Creation & Execution Layer

```text
architecture
      ↓
projects
      ↓
tasks
      ↓
automation
      ↓
agents
```

## 6.4 Market Intelligence Layer

```text
scraper
    ↓
jobs_opportunity
    ↓
analytics
```

## 6.5 Marketing & Sales Layer

```text
social
   ↓
marketing
   ↓
crm
   ↓
sales
   ↓
revenue
```

## 6.6 Financial Layer

```text
sales
   ↓
revenue
   ↓
personal_finance
   ↓
analytics
```

## 6.7 Goals & Feedback Layer

```text
goals
  ↓
projects / tasks / learning
  ↓
analytics
  ↓
memory
  ↓
ai
```

Notification is a shared supporting application that can receive events from all relevant domains.

---

# 7. KNOWLEDGE-TO-REVENUE BUSINESS FLOW

The overall business objective of So_Iam_Os is:

**Transform personal knowledge into measurable value and sustainable income.**

The primary workflow:

```text
                  SO_IAM_OS
                      │
                      ▼
                   KNOWLEDGE
                      │
                      ▼
                    LEARNING
                      │
                      ▼
                   CHALLENGES
                      │
                      ▼
                 VERIFIED SKILLS
                      │
                      ▼
                    CODEX
                      │
                      ▼
                 KNOWLEDGE ASSETS
                      │
                      ▼
                   PROJECTS
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       CONTENT     PRODUCTS     SERVICES
          │           │           │
          └───────────┼───────────┘
                      ▼
                   MARKETING
                      │
                      ▼
                  OPPORTUNITIES
                      │
                      ▼
                     CRM
                      │
                      ▼
                    SALES
                      │
                      ▼
                   REVENUE
                      │
                      ▼
                PERSONAL FINANCE
                      │
                      ▼
                  ANALYTICS
                      │
                      ▼
                    GOALS
                      │
                      ▼
                   IMPROVEMENT
                      │
                      └──────→ KNOWLEDGE
```

AI, Agents, Memory, Automation, and AI Tools Laboratory support this entire workflow.

---

# 8. CROSS-APPLICATION ARCHITECTURE RULES

## 8.1 Ownership

Every business entity must have one clearly defined owning application.

Examples:

- KnowledgeItem belongs to Knowledge.
- LearningTopic belongs to Learning.
- Challenge belongs to Challenges.
- CodeSnippet belongs to Codex.
- Project belongs to Projects.
- Contact belongs to CRM.
- Deal belongs to Sales.
- RevenueRecord belongs to Revenue.

Other applications may reference these entities but must not duplicate their ownership.

## 8.2 Communication

Applications should communicate through:

1. Explicit Django foreign keys when appropriate.
2. Domain services with clear responsibilities.
3. REST APIs for external or frontend integration.
4. Events for asynchronous cross-application workflows.
5. Background tasks for long-running operations.

Avoid circular dependencies.

## 8.3 Database

- Use one authoritative source for each business entity.
- Protect existing database records.
- Avoid destructive migrations.
- Use explicit ownership and permissions.
- Preserve relationships between knowledge, assets, projects, customers, and revenue.
- Ensure that revenue attribution can be traced back to its originating source when evidence exists.

## 8.4 Security

- Enforce user-level access control.
- Validate permissions in backend services and APIs.
- Protect sensitive financial information.
- Secure external integrations.
- Require approval for consequential AI actions.

## 8.5 Testing

Every application should have:

```text
tests/
│
├── __init__.py
├── test_models.py
├── test_services.py
└── test_views.py
```

Additional test files should be added when the application has specialized functionality, such as:

- AI provider integration.
- Agent execution.
- File extraction.
- Code execution.
- Workflow execution.
- Revenue attribution.
- Financial calculations.

---

# 9. ARCHITECTURAL CONSISTENCY

The following rules are mandatory.

1. Every application must follow the same architectural principles.
2. Frontend services must communicate with the correct backend APIs.
3. Stores must not become a second business-logic layer.
4. Vue views must not contain duplicated API implementation.
5. Django views must not contain complex business logic.
6. Services must have clearly defined ownership.
7. Serializers must not replace domain services.
8. Models must not contain unrelated application responsibilities.
9. Cross-application operations must have explicit contracts.
10. All important business operations must be tested.
11. Every meaningful architectural change must be documented.
12. Existing working functionality must be preserved.

---

# 10. PROJECT SUCCESS CRITERIA

So_Iam_Os is successful when it can support the complete journey:

```text
I KNOW SOMETHING
       ↓
I SAVE IT
       ↓
I UNDERSTAND IT
       ↓
I PRACTICE IT
       ↓
I DEVELOP A SKILL
       ↓
I CREATE A REUSABLE ASSET
       ↓
I BUILD A PROJECT OR PRODUCT
       ↓
I FIND MARKET DEMAND
       ↓
I REACH POTENTIAL CUSTOMERS
       ↓
I MAKE SALES
       ↓
I GENERATE REVENUE
       ↓
I MEASURE THE RESULTS
       ↓
I IMPROVE MY KNOWLEDGE
```

The primary strategic objective is:

# KNOWLEDGE → CAPABILITY → ASSETS → VALUE → CUSTOMERS → REVENUE → GROWTH

---

# 11. IMPLEMENTATION AND MAINTENANCE RULES

This document defines the target structural standard. It does not authorize automatically creating, moving, deleting, or renaming existing files.

Before applying structural changes:

1. Inspect the actual repository.
2. Compare existing frontend folders with this document.
3. Compare every Django application with its defined structure.
4. Identify missing files.
5. Identify duplicated responsibilities.
6. Identify naming inconsistencies.
7. Identify broken imports and API relationships.
8. Identify migration risks.
9. Prepare an application-by-application implementation plan.
10. Present the proposed changes for approval.

Implementation must be incremental.

For every application, record:

```text
Application:
Current Structure:
Target Structure:
Existing Files:
Missing Files:
Duplicated Files:
Required Changes:
Dependencies:
Migration Risks:
Tests:
Implementation Status:
```

Do not create empty files simply to make the directory tree look complete.

Do not rename existing applications or alter database tables without an approved migration plan.

---

# 12. FINAL ARCHITECTURAL STANDARD

This file is the central reference for the structural organization of the 25 So_Iam_Os applications.

All future development should respect:

- Consistent frontend architecture.
- Consistent backend architecture.
- Clear domain ownership.
- Independent application responsibilities.
- Controlled cross-application communication.
- Reusable business services.
- Reliable APIs.
- Automated testing.
- Documented architectural decisions.
- Knowledge-to-Revenue business objectives.

**Final Mission:**

Build So_Iam_Os as an integrated Personal Knowledge-to-Value-to-Revenue Operating System.

Every application must contribute to the larger ecosystem without losing its own clear responsibility.

**One ecosystem. 25 applications. One business vision.**
