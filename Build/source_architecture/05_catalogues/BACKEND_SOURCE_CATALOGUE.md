# Backend Source Catalogue

> Generated from source tree on 2026-11-23. Static inventory only. 26 app directories contain `apps.py`; 25 are registered in `INSTALLED_APPS`; URL mounts are taken from the project URL configuration.

| App | Root URL mount(s) | API URL modules | Model classes (AST) | Source files (all) |
|---|---|---:|---:|---:|
| `agents` | `/api/agents/` | 1 | 4 | 27 |
| `ai` | `/api/ai/` | 1 | 14 | 93 |
| `ai_tools_laboratory` | `/api/ai-tools/` | 1 | 4 | 26 |
| `analytics` | `/api/analytics/` | 1 | 4 | 26 |
| `architecture` | `/api/architecture/` | 1 | 4 | 26 |
| `automation` | `/api/automation/` | 1 | 10 | 70 |
| `challenges` | `/api/challenges/` | 1 | 4 | 25 |
| `codex` | `/api/codex/` | 1 | 26 | 143 |
| `core` | `/api/core/` | 1 | 2 | 33 |
| `crm` | `/api/crm/` | 1 | 4 | 26 |
| `goals` | `/api/goals/` | 1 | 4 | 23 |
| `jobs_opportunity` | `/api/jobs/` | 1 | 18 | 81 |
| `knowledge` | `/api/knowledge/` | 1 | 2 | 30 |
| `learning` | `/api/learning/` | 1 | 18 | 80 |
| `marketing` | `/api/marketing/` | 1 | 4 | 26 |
| `memory` | `/api/memory/` | 1 | 1 | 15 |
| `notification` | `/api/notifications/` | 1 | 1 | 16 |
| `personal_finance` | `/api/finance/` | 1 | 15 | 61 |
| `projects` | `/api/projects/` | 1 | 5 | 19 |
| `revenue` | `/api/revenue/` | 1 | 4 | 26 |
| `sales` | `/api/sales/` | 1 | 4 | 26 |
| `scraper` | `/api/scraper/` | 1 | 5 | 23 |
| `skills` | Not found in project root URL includes | 0 | 0 | 7 |
| `social` | `/api/social/` | 1 | 6 | 24 |
| `tasks` | `/api/tasks/` | 1 | 1 | 20 |
| `users_accounts` | `/api/users/` | 1 | 0 | 17 |

## Per-app source entry points

**Registration caveat:** `skills/` is not in `INSTALLED_APPS`; it is included below only because it contains `apps.py`.

### `agents`

- URL mount(s): `/api/agents/`.
- API URL modules: `backend_django/agents/api/urls.py`.
- Models discovered: `AgentConfiguration`, `AgentRun`, `Agent`, `AgentExecution`.
- Representative source files:
  - `backend_django/agents/apps.py`
  - `backend_django/agents/models.py`
  - `backend_django/agents/api/urls.py`
  - `backend_django/agents/admin.py`
  - `backend_django/agents/api/__init__.py`
  - `backend_django/agents/models/__init__.py`
  - `backend_django/agents/models/agent.py`
  - `backend_django/agents/models/agent_configuration.py`
  - `backend_django/agents/models/agent_execution.py`
  - `backend_django/agents/models/agent_run.py`
  - `backend_django/agents/services/__init__.py`
  - `backend_django/agents/services/agent_service.py`
  - `backend_django/agents/services/execution_service.py`

### `ai`

- URL mount(s): `/api/ai/`.
- API URL modules: `backend_django/ai/api/urls.py`.
- Models discovered: `AIConversation`, `AIMessage`, `AISettings`, `AIPromptProfile`, `AIUsageRecord`, `AIProviderCredential`, `AIProviderConfig`, `AIExecution`, `AIFeedback`, `AIWorkflowDefinition`, `AIWorkflowRun`, `AIBudgetPolicy`, `AIBudgetReservation`, `AiAuditLog`.
- Representative source files:
  - `backend_django/ai/apps.py`
  - `backend_django/ai/api/urls.py`
  - `backend_django/ai/admin.py`
  - `backend_django/ai/api/__init__.py`
  - `backend_django/ai/api/chat.py`
  - `backend_django/ai/api/diagnostics.py`
  - `backend_django/ai/models/__init__.py`
  - `backend_django/ai/models/audit.py`
  - `backend_django/ai/models/budgets.py`
  - `backend_django/ai/models/conversations.py`
  - `backend_django/ai/models/executions.py`
  - `backend_django/ai/models/feedback.py`
  - `backend_django/ai/models/prompts.py`
  - `backend_django/ai/models/providers.py`
  - `backend_django/ai/services/__init__.py`
  - `backend_django/ai/services/agent_executor.py`

### `ai_tools_laboratory`

- URL mount(s): `/api/ai-tools/`.
- API URL modules: `backend_django/ai_tools_laboratory/api/urls.py`.
- Models discovered: `Tool`, `ToolExecution`, `ToolConfiguration`, `ToolCategory`.
- Representative source files:
  - `backend_django/ai_tools_laboratory/apps.py`
  - `backend_django/ai_tools_laboratory/models.py`
  - `backend_django/ai_tools_laboratory/api/urls.py`
  - `backend_django/ai_tools_laboratory/admin.py`
  - `backend_django/ai_tools_laboratory/api/__init__.py`
  - `backend_django/ai_tools_laboratory/models/__init__.py`
  - `backend_django/ai_tools_laboratory/models/tool.py`
  - `backend_django/ai_tools_laboratory/models/tool_category.py`
  - `backend_django/ai_tools_laboratory/models/tool_configuration.py`
  - `backend_django/ai_tools_laboratory/models/tool_execution.py`
  - `backend_django/ai_tools_laboratory/services/__init__.py`
  - `backend_django/ai_tools_laboratory/services/tool_service.py`

### `analytics`

- URL mount(s): `/api/analytics/`.
- API URL modules: `backend_django/analytics/api/urls.py`.
- Models discovered: `Report`, `Metric`, `AnalyticsEvent`, `MetricSnapshot`.
- Representative source files:
  - `backend_django/analytics/apps.py`
  - `backend_django/analytics/models.py`
  - `backend_django/analytics/api/urls.py`
  - `backend_django/analytics/admin.py`
  - `backend_django/analytics/api/__init__.py`
  - `backend_django/analytics/models/__init__.py`
  - `backend_django/analytics/models/analytics_event.py`
  - `backend_django/analytics/models/metric.py`
  - `backend_django/analytics/models/metric_snapshot.py`
  - `backend_django/analytics/models/report.py`
  - `backend_django/analytics/services/__init__.py`
  - `backend_django/analytics/services/analytics_service.py`

### `architecture`

- URL mount(s): `/api/architecture/`.
- API URL modules: `backend_django/architecture/api/urls.py`.
- Models discovered: `Dependency`, `Component`, `ArchitectureDecision`, `Architecture`.
- Representative source files:
  - `backend_django/architecture/apps.py`
  - `backend_django/architecture/models.py`
  - `backend_django/architecture/api/urls.py`
  - `backend_django/architecture/admin.py`
  - `backend_django/architecture/api/__init__.py`
  - `backend_django/architecture/models/__init__.py`
  - `backend_django/architecture/models/architecture.py`
  - `backend_django/architecture/models/architecture_decision.py`
  - `backend_django/architecture/models/component.py`
  - `backend_django/architecture/models/dependency.py`
  - `backend_django/architecture/services/__init__.py`
  - `backend_django/architecture/services/architecture_service.py`

### `automation`

- URL mount(s): `/api/automation/`.
- API URL modules: `backend_django/automation/api/urls.py`.
- Models discovered: `Task`, `TaskRun`, `Workflow`, `Action`, `Program`, `WorkflowNode`, `WorkflowEdge`, `ScreenState`, `ProgramElement`, `Delay`.
- Representative source files:
  - `backend_django/automation/apps.py`
  - `backend_django/automation/api/urls.py`
  - `backend_django/automation/tasks.py`
  - `backend_django/automation/admin.py`
  - `backend_django/automation/api/__init__.py`
  - `backend_django/automation/models/__init__.py`
  - `backend_django/automation/models/action.py`
  - `backend_django/automation/models/delay.py`
  - `backend_django/automation/models/program.py`
  - `backend_django/automation/models/program_element.py`
  - `backend_django/automation/models/screen_state.py`
  - `backend_django/automation/models/task.py`
  - `backend_django/automation/models/task_run.py`
  - `backend_django/automation/services/automation.py`
  - `backend_django/automation/services/macos_scanner.py`
  - `backend_django/automation/services/program_service.py`

### `challenges`

- URL mount(s): `/api/challenges/`.
- API URL modules: `backend_django/challenges/api/urls.py`.
- Models discovered: `ChallengeAttempt`, `ChallengeProgress`, `Challenge`, `ChallengeStep`.
- Representative source files:
  - `backend_django/challenges/apps.py`
  - `backend_django/challenges/api/urls.py`
  - `backend_django/challenges/admin.py`
  - `backend_django/challenges/api/__init__.py`
  - `backend_django/challenges/models/__init__.py`
  - `backend_django/challenges/models/challenge.py`
  - `backend_django/challenges/models/challenge_attempt.py`
  - `backend_django/challenges/models/challenge_progress.py`
  - `backend_django/challenges/models/challenge_step.py`
  - `backend_django/challenges/services/__init__.py`
  - `backend_django/challenges/services/challenge_service.py`

### `codex`

- URL mount(s): `/api/codex/`.
- API URL modules: `backend_django/codex/api/urls.py`.
- Models discovered: `ArchitectureEdge`, `CodexAgentDefinition`, `LocalAIJob`, `CodexFinding`, `CodexExecutionRequest`, `CodexWorkflowStep`, `CodexConversation`, `ChangeSet`, `APIEndpoint`, `CodexPolicy`, `FileRegistry`, `CodexMessage`, `CodexChangeFile`, `ProtectedFeature`, `CodexAgentRun`, `ProtectedItem`, `Feature`, `CodexCapabilityRun`, `CodexAnalysis`, `CodexAuditEvent`, `CodexFeatureDefinition`, `ArchitectureNode`, `ProjectSnapshot`, `CodexTool`, `CodexToolDefinition`, `ProjectRegistry`.
- Representative source files:
  - `backend_django/codex/apps.py`
  - `backend_django/codex/api/urls.py`
  - `backend_django/codex/tasks.py`
  - `backend_django/codex/admin.py`
  - `backend_django/codex/api/__init__.py`
  - `backend_django/codex/models/__init__.py`
  - `backend_django/codex/models/api_endpoint.py`
  - `backend_django/codex/models/architecture_edge.py`
  - `backend_django/codex/models/architecture_node.py`
  - `backend_django/codex/models/change_set.py`
  - `backend_django/codex/models/codex_agent_definition.py`
  - `backend_django/codex/models/codex_agent_run.py`
  - `backend_django/codex/models/codex_analysis.py`
  - `backend_django/codex/services/__init__.py`
  - `backend_django/codex/services/build_workspace.py`
  - `backend_django/codex/services/capabilities.py`

### `core`

- URL mount(s): `/api/core/`.
- API URL modules: `backend_django/core/api/urls.py`.
- Models discovered: `BaseModel`, `UserLearningSettings`.
- Representative source files:
  - `backend_django/core/apps.py`
  - `backend_django/core/api/urls.py`
  - `backend_django/core/admin.py`
  - `backend_django/core/api/__init__.py`
  - `backend_django/core/api/owned.py`
  - `backend_django/core/models/__init__.py`
  - `backend_django/core/models/base_model.py`
  - `backend_django/core/models/user_learning_settings.py`
  - `backend_django/core/services/__init__.py`
  - `backend_django/core/services/core_services.py`

### `crm`

- URL mount(s): `/api/crm/`.
- API URL modules: `backend_django/crm/api/urls.py`.
- Models discovered: `Interaction`, `CustomerRelationship`, `Company`, `Contact`.
- Representative source files:
  - `backend_django/crm/apps.py`
  - `backend_django/crm/models.py`
  - `backend_django/crm/api/urls.py`
  - `backend_django/crm/admin.py`
  - `backend_django/crm/api/__init__.py`
  - `backend_django/crm/models/__init__.py`
  - `backend_django/crm/models/company.py`
  - `backend_django/crm/models/contact.py`
  - `backend_django/crm/models/customer_relationship.py`
  - `backend_django/crm/models/interaction.py`
  - `backend_django/crm/services/__init__.py`
  - `backend_django/crm/services/crm_service.py`

### `goals`

- URL mount(s): `/api/goals/`.
- API URL modules: `backend_django/goals/api/urls.py`.
- Models discovered: `Goal`, `GoalMilestone`, `GoalActivity`, `GoalPlanProposal`.
- Representative source files:
  - `backend_django/goals/apps.py`
  - `backend_django/goals/api/urls.py`
  - `backend_django/goals/admin.py`
  - `backend_django/goals/api/__init__.py`
  - `backend_django/goals/models/__init__.py`
  - `backend_django/goals/models/goal.py`
  - `backend_django/goals/models/goal_activity.py`
  - `backend_django/goals/models/goal_milestone.py`
  - `backend_django/goals/models/goal_plan_proposal.py`
  - `backend_django/goals/services/__init__.py`
  - `backend_django/goals/services/coach.py`
  - `backend_django/goals/services/goals_services.py`

### `jobs_opportunity`

- URL mount(s): `/api/jobs/`.
- API URL modules: `backend_django/jobs_opportunity/api/urls.py`.
- Models discovered: `JobMatch`, `JobSkillRequirement`, `JobResume`, `CompanyProfile`, `JobReadiness`, `JobApplicationEvent`, `JobAnalyticsSnapshot`, `JobCoverLetter`, `JobAlert`, `JobSavedSearch`, `JobSkillGap`, `JobApplication`, `JobRecommendation`, `JobSource`, `JobOpportunity`, `JobSourceSyncRun`, `JobPreference`, `JobInterview`.
- Representative source files:
  - `backend_django/jobs_opportunity/apps.py`
  - `backend_django/jobs_opportunity/api/urls.py`
  - `backend_django/jobs_opportunity/tasks.py`
  - `backend_django/jobs_opportunity/admin.py`
  - `backend_django/jobs_opportunity/api/__init__.py`
  - `backend_django/jobs_opportunity/models/__init__.py`
  - `backend_django/jobs_opportunity/models/common.py`
  - `backend_django/jobs_opportunity/models/company_profile.py`
  - `backend_django/jobs_opportunity/models/job_alert.py`
  - `backend_django/jobs_opportunity/models/job_analytics_snapshot.py`
  - `backend_django/jobs_opportunity/models/job_application.py`
  - `backend_django/jobs_opportunity/models/job_application_event.py`
  - `backend_django/jobs_opportunity/models/job_cover_letter.py`
  - `backend_django/jobs_opportunity/services/__init__.py`
  - `backend_django/jobs_opportunity/services/jobs_opportunity_services.py`

### `knowledge`

- URL mount(s): `/api/knowledge/`.
- API URL modules: `backend_django/knowledge/api/urls.py`.
- Models discovered: `KnowledgeFile`, `KnowledgeItem`.
- Representative source files:
  - `backend_django/knowledge/apps.py`
  - `backend_django/knowledge/api/urls.py`
  - `backend_django/knowledge/admin.py`
  - `backend_django/knowledge/api/__init__.py`
  - `backend_django/knowledge/models/__init__.py`
  - `backend_django/knowledge/models/knowledge_file.py`
  - `backend_django/knowledge/models/knowledge_item.py`
  - `backend_django/knowledge/services/__init__.py`
  - `backend_django/knowledge/services/file_service.py`
  - `backend_django/knowledge/services/knowledge_service.py`
  - `backend_django/knowledge/tasks/__init__.py`
  - `backend_django/knowledge/tasks/knowledge_file_tasks.py`

### `learning`

- URL mount(s): `/api/learning/`.
- API URL modules: `backend_django/learning/api/urls.py`.
- Models discovered: `AssessmentChoice`, `Skill`, `LearningProgress`, `LearningNote`, `ApplicationSubmission`, `LearningSession`, `KnowledgeApplication`, `AssessmentAttempt`, `AssessmentQuestion`, `LearningPath`, `Assessment`, `LearningTopic`, `ApplicationReview`, `LearningGoal`, `LearningResource`, `AssessmentResponse`, `LearningRevision`, `Lesson`.
- Representative source files:
  - `backend_django/learning/apps.py`
  - `backend_django/learning/api/urls.py`
  - `backend_django/learning/admin.py`
  - `backend_django/learning/api/__init__.py`
  - `backend_django/learning/models/__init__.py`
  - `backend_django/learning/models/application_review.py`
  - `backend_django/learning/models/application_submission.py`
  - `backend_django/learning/models/assessment.py`
  - `backend_django/learning/models/assessment_attempt.py`
  - `backend_django/learning/models/assessment_choice.py`
  - `backend_django/learning/models/assessment_question.py`
  - `backend_django/learning/models/assessment_response.py`
  - `backend_django/learning/services/__init__.py`
  - `backend_django/learning/services/ai_content.py`
  - `backend_django/learning/services/ai_service.py`
  - `backend_django/learning/services/assessment.py`

### `marketing`

- URL mount(s): `/api/marketing/`.
- API URL modules: `backend_django/marketing/api/urls.py`.
- Models discovered: `MarketingContent`, `Campaign`, `LeadSource`, `MarketingChannel`.
- Representative source files:
  - `backend_django/marketing/apps.py`
  - `backend_django/marketing/models.py`
  - `backend_django/marketing/api/urls.py`
  - `backend_django/marketing/admin.py`
  - `backend_django/marketing/api/__init__.py`
  - `backend_django/marketing/models/__init__.py`
  - `backend_django/marketing/models/campaign.py`
  - `backend_django/marketing/models/lead_source.py`
  - `backend_django/marketing/models/marketing_channel.py`
  - `backend_django/marketing/models/marketing_content.py`
  - `backend_django/marketing/services/__init__.py`
  - `backend_django/marketing/services/marketing_service.py`

### `memory`

- URL mount(s): `/api/memory/`.
- API URL modules: `backend_django/memory/api/urls.py`.
- Models discovered: `MemoryItem`.
- Representative source files:
  - `backend_django/memory/apps.py`
  - `backend_django/memory/api/urls.py`
  - `backend_django/memory/admin.py`
  - `backend_django/memory/api/__init__.py`
  - `backend_django/memory/models/__init__.py`
  - `backend_django/memory/models/memory_item.py`

### `notification`

- URL mount(s): `/api/notifications/`.
- API URL modules: `backend_django/notification/api/urls.py`.
- Models discovered: `Notification`.
- Representative source files:
  - `backend_django/notification/apps.py`
  - `backend_django/notification/api/urls.py`
  - `backend_django/notification/admin.py`
  - `backend_django/notification/api/__init__.py`
  - `backend_django/notification/models/__init__.py`
  - `backend_django/notification/models/notification.py`
  - `backend_django/notification/models/notification_service.py`

### `personal_finance`

- URL mount(s): `/api/finance/`.
- API URL modules: `backend_django/personal_finance/api/urls.py`.
- Models discovered: `FinancialProfile`, `Budget`, `Debt`, `Category`, `FinancialScenario`, `Transaction`, `LoanPayment`, `RecurringCashflow`, `DebtPayment`, `FinancialHabit`, `FinancialAlert`, `SavingsGoal`, `Subscription`, `SavingPlan`, `LendingBorrowing`.
- Representative source files:
  - `backend_django/personal_finance/apps.py`
  - `backend_django/personal_finance/api/urls.py`
  - `backend_django/personal_finance/admin.py`
  - `backend_django/personal_finance/api/__init__.py`
  - `backend_django/personal_finance/models/__init__.py`
  - `backend_django/personal_finance/models/budget.py`
  - `backend_django/personal_finance/models/category.py`
  - `backend_django/personal_finance/models/debt.py`
  - `backend_django/personal_finance/models/debt_payment.py`
  - `backend_django/personal_finance/models/financial_alert.py`
  - `backend_django/personal_finance/models/financial_habit.py`
  - `backend_django/personal_finance/models/financial_profile.py`
  - `backend_django/personal_finance/services/__init__.py`
  - `backend_django/personal_finance/services/personal_finance_services.py`

### `projects`

- URL mount(s): `/api/projects/`.
- API URL modules: `backend_django/projects/api/urls.py`.
- Models discovered: `ProjectMember`, `ProjectGoal`, `Project`, `ProjectContext`, `ProjectTask`.
- Representative source files:
  - `backend_django/projects/apps.py`
  - `backend_django/projects/api/urls.py`
  - `backend_django/projects/admin.py`
  - `backend_django/projects/api/__init__.py`
  - `backend_django/projects/models/__init__.py`
  - `backend_django/projects/models/project.py`
  - `backend_django/projects/models/project_context.py`
  - `backend_django/projects/models/project_goal.py`
  - `backend_django/projects/models/project_member.py`
  - `backend_django/projects/models/project_task.py`

### `revenue`

- URL mount(s): `/api/revenue/`.
- API URL modules: `backend_django/revenue/api/urls.py`.
- Models discovered: `RevenueSource`, `RevenueStream`, `RevenueRecord`, `RecurringRevenue`.
- Representative source files:
  - `backend_django/revenue/apps.py`
  - `backend_django/revenue/models.py`
  - `backend_django/revenue/api/urls.py`
  - `backend_django/revenue/admin.py`
  - `backend_django/revenue/api/__init__.py`
  - `backend_django/revenue/models/__init__.py`
  - `backend_django/revenue/models/recurring_revenue.py`
  - `backend_django/revenue/models/revenue_record.py`
  - `backend_django/revenue/models/revenue_source.py`
  - `backend_django/revenue/models/revenue_stream.py`
  - `backend_django/revenue/services/__init__.py`
  - `backend_django/revenue/services/revenue_service.py`

### `sales`

- URL mount(s): `/api/sales/`.
- API URL modules: `backend_django/sales/api/urls.py`.
- Models discovered: `SalesActivity`, `Offer`, `Sale`, `Deal`.
- Representative source files:
  - `backend_django/sales/apps.py`
  - `backend_django/sales/models.py`
  - `backend_django/sales/api/urls.py`
  - `backend_django/sales/admin.py`
  - `backend_django/sales/api/__init__.py`
  - `backend_django/sales/models/__init__.py`
  - `backend_django/sales/models/deal.py`
  - `backend_django/sales/models/offer.py`
  - `backend_django/sales/models/sale.py`
  - `backend_django/sales/models/sales_activity.py`
  - `backend_django/sales/services/__init__.py`
  - `backend_django/sales/services/sales_service.py`

### `scraper`

- URL mount(s): `/api/scraper/`.
- API URL modules: `backend_django/scraper/api/urls.py`.
- Models discovered: `ScrapingJob`, `ScrapingConfig`, `ScrapedData`, `ParentSelector`, `Website`.
- Representative source files:
  - `backend_django/scraper/apps.py`
  - `backend_django/scraper/api/urls.py`
  - `backend_django/scraper/tasks.py`
  - `backend_django/scraper/admin.py`
  - `backend_django/scraper/api/__init__.py`
  - `backend_django/scraper/models/__init__.py`
  - `backend_django/scraper/models/parent_selector.py`
  - `backend_django/scraper/models/scraped_data.py`
  - `backend_django/scraper/models/scraping_config.py`
  - `backend_django/scraper/models/scraping_job.py`
  - `backend_django/scraper/models/website.py`
  - `backend_django/scraper/services/__init__.py`
  - `backend_django/scraper/services/scraper_services.py`

### `skills`

- URL mount(s): Not found in root URL includes.
- API URL modules: None found by filename scan.
- Models discovered: No model subclass found by static AST scan.
- Representative source files:
  - `backend_django/skills/apps.py`
  - `backend_django/skills/models.py`
  - `backend_django/skills/admin.py`

### `social`

- URL mount(s): `/api/social/`.
- API URL modules: `backend_django/social/api/urls.py`.
- Models discovered: `Friendship`, `SocialProfile`, `FriendshipRequest`, `SocialRecommendation`, `UserBlock`, `Follow`.
- Representative source files:
  - `backend_django/social/apps.py`
  - `backend_django/social/api/urls.py`
  - `backend_django/social/admin.py`
  - `backend_django/social/api/__init__.py`
  - `backend_django/social/models/__init__.py`
  - `backend_django/social/models/common.py`
  - `backend_django/social/models/follow.py`
  - `backend_django/social/models/friendship.py`
  - `backend_django/social/models/friendship_request.py`
  - `backend_django/social/models/social_profile.py`
  - `backend_django/social/models/social_recommendation.py`
  - `backend_django/social/models/user_block.py`
  - `backend_django/social/services/__init__.py`
  - `backend_django/social/services/matching.py`

### `tasks`

- URL mount(s): `/api/tasks/`.
- API URL modules: `backend_django/tasks/api/urls.py`.
- Models discovered: `Task`.
- Representative source files:
  - `backend_django/tasks/apps.py`
  - `backend_django/tasks/api/urls.py`
  - `backend_django/tasks/tasks.py`
  - `backend_django/tasks/admin.py`
  - `backend_django/tasks/api/__init__.py`
  - `backend_django/tasks/models/__init__.py`
  - `backend_django/tasks/models/task.py`
  - `backend_django/tasks/services/__init__.py`
  - `backend_django/tasks/services/daily_generation.py`
  - `backend_django/tasks/services/tasks_services.py`

### `users_accounts`

- URL mount(s): `/api/users/`.
- API URL modules: `backend_django/users_accounts/api/urls.py`.
- Models discovered: No model subclass found by static AST scan.
- Representative source files:
  - `backend_django/users_accounts/apps.py`
  - `backend_django/users_accounts/api/urls.py`
  - `backend_django/users_accounts/admin.py`
  - `backend_django/users_accounts/api/__init__.py`
  - `backend_django/users_accounts/models/__init__.py`
  - `backend_django/users_accounts/models/custom_user_manager.py`
  - `backend_django/users_accounts/models/user.py`
