Frontend

services/
│
├── Core/
│   └── Core.js
│
├── Users_Accounts/
│   └── Users_Accounts.js
│
├── AI/
│   └── AI.js
│
├── AI_Tools_Laboratory/
│   └── AI_Tools_Laboratory.js
│
├── Agents/
│   └── Agents.js
│
├── Skills/
│   └── Skills.js
│
├── Memory/
│   └── Memory.js
│
├── Knowledge/
│   └── Knowledge.js
│
├── Learning/
│   └── Learning.js
│
├── Challenges/
│   └── Challenges.js
│
├── Codex/
│   └── Codex.js
│
├── Projects/
│   └── Projects.js
│
├── Architecture/
│   └── Architecture.js
│
├── Tasks/
│   └── Tasks.js
│
├── Automation/
│   └── Automation.js
│
├── Jobs_Opportunity/
│   └── Jobs_Opportunity.js
│
├── Scraper/
│   └── Scraper.js
│
├── Marketing/
│   └── Marketing.js
│
├── Sales/
│   └── Sales.js
│
├── CRM/
│   └── CRM.js
│
├── Social/
│   └── Social.js
│
├── Analytics/
│   └── Analytics.js
│
├── Revenue/
│   └── Revenue.js
│
├── Goals/
│   └── Goals.js
│
├── Personal_Finance/
│   └── Personal_Finance.js
│
└── Notifications/
    └── Notifications.js



stores/
│
├── core/
│   └── coreStore.js
│
├── users_accounts/
│   └── usersAccountsStore.js
│
├── ai/
│   └── aiStore.js
│
├── ai_tools_laboratory/
│   └── aiToolsLaboratoryStore.js
│
├── agents/
│   └── agentsStore.js
│
├── skills/
│   └── skillsStore.js
│
├── memory/
│   └── memoryStore.js
│
├── knowledge/
│   └── knowledgeStore.js
│
├── learning/
│   └── learningStore.js
│
├── challenges/
│   └── challengesStore.js
│
├── codex/
│   └── codexStore.js
│
├── projects/
│   └── projectsStore.js
│
├── architecture/
│   └── architectureStore.js
│
├── tasks/
│   └── tasksStore.js
│
├── automation/
│   └── automationStore.js
│
├── jobs_opportunity/
│   └── jobsOpportunityStore.js
│
├── scraper/
│   └── scraperStore.js
│
├── marketing/
│   └── marketingStore.js
│
├── sales/
│   └── salesStore.js
│
├── crm/
│   └── crmStore.js
│
├── social/
│   └── socialStore.js
│
├── analytics/
│   └── analyticsStore.js
│
├── revenue/
│   └── revenueStore.js
│
├── goals/
│   └── goalsStore.js
│
├── personal_finance/
│   └── personalFinanceStore.js
│
└── notifications/
    └── notificationsStore.js

views/
│
├── core/
│   └── coreView.vue
│
├── users_accounts/
│   └── usersAccountsView.vue
│
├── ai/
│   └── aiView.vue
│
├── ai_tools_laboratory/
│   └── aiToolsLaboratoryView.vue
│
├── agents/
│   └── agentsView.vue
│
├── skills/
│   └── skillsView.vue
│
├── memory/
│   └── memoryView.vue
│
├── knowledge/
│   └── knowledgeView.vue
│
├── learning/
│   └── learningView.vue
│
├── challenges/
│   └── challengesView.vue
│
├── codex/
│   └── codexView.vue
│
├── projects/
│   └── projectsView.vue
│
├── architecture/
│   └── architectureView.vue
│
├── tasks/
│   └── tasksView.vue
│
├── automation/
│   └── automationView.vue
│
├── jobs_opportunity/
│   └── jobsOpportunityView.vue
│
├── scraper/
│   └── scraperView.vue
│
├── marketing/
│   └── marketingView.vue
│
├── sales/
│   └── salesView.vue
│
├── crm/
│   └── crmView.vue
│
├── social/
│   └── socialView.vue
│
├── analytics/
│   └── analyticsView.vue
│
├── revenue/
│   └── revenueView.vue
│
├── goals/
│   └── goalsView.vue
│
├── personal_finance/
│   └── personalFinanceView.vue
│
└── notifications/
    └── notificationsView.vue


Backend 



core/
│
├── migrations/
│   └── __init__.py
│
├── models/
│   ├── __init__.py
│   └── core_models.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   └── core_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── core_serializers.py
│   │
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

users_accounts/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── profile.py
│   └── account.py
│
├── api/
│   ├── __init__.py
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

ai/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── ai_model.py
│   ├── ai_provider.py
│   └── ai_request.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── ai_views.py
│   │   └── provider_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── ai_serializers.py
│   │
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

ai_tools_laboratory/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── tool.py
│   ├── tool_category.py
│   ├── tool_configuration.py
│   └── tool_execution.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── tool_views.py
│   │   ├── category_views.py
│   │   └── execution_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── tool_serializers.py
│   │   └── execution_serializers.py
│   │
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
agents/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── agent.py
│   ├── agent_configuration.py
│   ├── agent_execution.py
│   └── agent_run.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── agent_views.py
│   │   └── execution_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── agent_serializers.py
│   │   └── execution_serializers.py
│   │
│   └── urls.py
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
skills/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── skill.py
│   ├── skill_category.py
│   └── skill_assessment.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── skill_views.py
│   │   └── assessment_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── skill_serializers.py
│   │
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── skill_service.py
│   └── assessment_service.py
│
├── validators/
│   ├── __init__.py
│   └── skill_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── skill_tasks.py
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
memory/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── memory.py
│   ├── memory_item.py
│   ├── memory_context.py
│   └── memory_embedding.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   └── memory_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── memory_serializers.py
│   │
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
knowledge/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── document.py
│   └── knowledge_base.py
│
├── api/
│   ├── __init__.py
│   │
│   ├── views/
│   │   ├── __init__.py
│   │   ├── document_views.py
│   │   └── knowledge_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── document_serializers.py
│   │   └── knowledge_serializers.py
│   │
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
learning/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── learning_path.py
│   ├── learning_topic.py
│   ├── learning_step.py
│   ├── learning_note.py
│   └── learning_application.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── path_views.py
│   │   ├── topic_views.py
│   │   └── application_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── path_serializers.py
│   │   ├── topic_serializers.py
│   │   └── application_serializers.py
│   │
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
challenges/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── challenge.py
│   ├── challenge_step.py
│   └── submission.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── challenge_views.py
│   │   └── submission_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── challenge_serializers.py
│   │
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
codex/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── code_snippet.py
│   ├── code_example.py
│   └── code_language.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   └── codex_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── codex_serializers.py
│   │
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
projects/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── project.py
│   ├── project_member.py
│   └── project_resource.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── project_views.py
│   │   └── member_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── project_serializers.py
│   │
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
architecture/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── architecture.py
│   ├── architecture_decision.py
│   ├── component.py
│   └── dependency.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── architecture_views.py
│   │   └── decision_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── architecture_serializers.py
│   │
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
tasks/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── task.py
│   ├── task_dependency.py
│   └── task_execution.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── task_views.py
│   │   └── execution_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── task_serializers.py
│   │
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

automation/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── workflow.py
│   ├── workflow_step.py
│   ├── trigger.py
│   └── execution.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── workflow_views.py
│   │   └── execution_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── workflow_serializers.py
│   │
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
jobs_opportunity/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── job.py
│   ├── opportunity.py
│   ├── source.py
│   └── application.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── job_views.py
│   │   ├── opportunity_views.py
│   │   └── application_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── opportunity_serializers.py
│   │
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
├── extractors/
│   ├── __init__.py
│   └── job_extractor.py
│
├── tasks/
│   ├── __init__.py
│   └── opportunity_tasks.py
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
scraper/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── scraper.py
│   ├── scraper_source.py
│   └── scraped_data.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   └── scraper_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── scraper_serializers.py
│   │
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── scraper_service.py
│   └── extraction_service.py
│
├── validators/
│   ├── __init__.py
│   └── scraper_validator.py
│
├── extractors/
│   ├── __init__.py
│   ├── html_extractor.py
│   ├── text_extractor.py
│   └── metadata_extractor.py
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
marketing/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── campaign.py
│   ├── content.py
│   └── audience.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── campaign_views.py
│   │   └── content_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── marketing_serializers.py
│   │
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── campaign_service.py
│   ├── content_service.py
│   └── audience_service.py
│
├── validators/
│   ├── __init__.py
│   └── campaign_validator.py
│
├── tasks/
│   ├── __init__.py
│   └── marketing_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_campaigns.py
│
├── admin.py
├── apps.py
└── __init__.py


sales/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── deal.py
│   ├── pipeline.py
│   └── sales_activity.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── deal_views.py
│   │   └── pipeline_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── sales_serializers.py
│   │
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── deal_service.py
│   └── pipeline_service.py
│
├── validators/
│   ├── __init__.py
│   └── deal_validator.py
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
crm/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── contact.py
│   ├── lead.py
│   ├── company.py
│   └── interaction.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── contact_views.py
│   │   ├── lead_views.py
│   │   └── company_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── crm_serializers.py
│   │
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── contact_service.py
│   ├── lead_service.py
│   └── interaction_service.py
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
analytics/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── metric.py
│   ├── event.py
│   ├── report.py
│   └── dashboard.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── analytics_views.py
│   │   └── report_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── analytics_serializers.py
│   │
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── analytics_service.py
│   ├── metric_service.py
│   └── report_service.py
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
│   └── test_metrics.py
│
├── admin.py
├── apps.py
└── __init__.py
revenue/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── revenue.py
│   ├── transaction.py
│   ├── income_source.py
│   └── payment.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── revenue_views.py
│   │   └── transaction_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── revenue_serializers.py
│   │
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── revenue_service.py
│   ├── transaction_service.py
│   └── payment_service.py
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
│   └── test_transactions.py
│
├── admin.py
├── apps.py
└── __init__.py
goals/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── goal.py
│   ├── goal_milestone.py
│   └── goal_progress.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── goal_views.py
│   │   └── progress_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── goal_serializers.py
│   │
│   └── urls.py
│
├── services/
│   ├── __init__.py
│   ├── goal_service.py
│   └── progress_service.py
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
personal_finance/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── account.py
│   ├── transaction.py
│   ├── budget.py
│   └── financial_goal.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── account_views.py
│   │   ├── transaction_views.py
│   │   └── budget_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── finance_serializers.py
│   │
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
│   └── test_budget.py
│
├── admin.py
├── apps.py
└── __init__.py
notifications/
│
├── migrations/
│   ├── __init__.py
│   └── ملفات Migrations الحالية
│
├── models/
│   ├── __init__.py
│   ├── notification.py
│   ├── notification_preference.py
│   └── notification_template.py
│
├── api/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── notification_views.py
│   │   └── preference_views.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── notification_serializers.py
│   │
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
│   └── test_delivery.py
│
├── admin.py
├── apps.py
└── __init__.py
