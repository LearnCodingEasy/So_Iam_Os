# Database Model Catalogue (Static AST Inventory)

> 164 class declarations matched a Django `Model` base expression. This is a discovery aid, not a complete schema dump. Fields, inherited fields, constraints, indexes, managers, database state, and migrations require separate validation.

| App | Model | Source file |
|---|---|---|
| `agents` | `AgentConfiguration` | `backend_django/agents/models/agent_configuration.py` |
| `agents` | `AgentRun` | `backend_django/agents/models/agent_run.py` |
| `agents` | `Agent` | `backend_django/agents/models/agent.py` |
| `agents` | `AgentExecution` | `backend_django/agents/models/agent_execution.py` |
| `ai` | `AIConversation` | `backend_django/ai/models/conversations.py` |
| `ai` | `AIMessage` | `backend_django/ai/models/conversations.py` |
| `ai` | `AISettings` | `backend_django/ai/models/settings.py` |
| `ai` | `AIPromptProfile` | `backend_django/ai/models/prompts.py` |
| `ai` | `AIUsageRecord` | `backend_django/ai/models/usage.py` |
| `ai` | `AIProviderCredential` | `backend_django/ai/models/providers.py` |
| `ai` | `AIProviderConfig` | `backend_django/ai/models/providers.py` |
| `ai` | `AIExecution` | `backend_django/ai/models/executions.py` |
| `ai` | `AIFeedback` | `backend_django/ai/models/feedback.py` |
| `ai` | `AIWorkflowDefinition` | `backend_django/ai/models/workflows.py` |
| `ai` | `AIWorkflowRun` | `backend_django/ai/models/workflows.py` |
| `ai` | `AIBudgetPolicy` | `backend_django/ai/models/budgets.py` |
| `ai` | `AIBudgetReservation` | `backend_django/ai/models/budgets.py` |
| `ai` | `AiAuditLog` | `backend_django/ai/models/audit.py` |
| `ai_tools_laboratory` | `Tool` | `backend_django/ai_tools_laboratory/models/tool.py` |
| `ai_tools_laboratory` | `ToolExecution` | `backend_django/ai_tools_laboratory/models/tool_execution.py` |
| `ai_tools_laboratory` | `ToolConfiguration` | `backend_django/ai_tools_laboratory/models/tool_configuration.py` |
| `ai_tools_laboratory` | `ToolCategory` | `backend_django/ai_tools_laboratory/models/tool_category.py` |
| `analytics` | `Report` | `backend_django/analytics/models/report.py` |
| `analytics` | `Metric` | `backend_django/analytics/models/metric.py` |
| `analytics` | `AnalyticsEvent` | `backend_django/analytics/models/analytics_event.py` |
| `analytics` | `MetricSnapshot` | `backend_django/analytics/models/metric_snapshot.py` |
| `architecture` | `Dependency` | `backend_django/architecture/models/dependency.py` |
| `architecture` | `Component` | `backend_django/architecture/models/component.py` |
| `architecture` | `ArchitectureDecision` | `backend_django/architecture/models/architecture_decision.py` |
| `architecture` | `Architecture` | `backend_django/architecture/models/architecture.py` |
| `automation` | `Task` | `backend_django/automation/models/task.py` |
| `automation` | `TaskRun` | `backend_django/automation/models/task_run.py` |
| `automation` | `Workflow` | `backend_django/automation/models/workflow.py` |
| `automation` | `Action` | `backend_django/automation/models/action.py` |
| `automation` | `Program` | `backend_django/automation/models/program.py` |
| `automation` | `WorkflowNode` | `backend_django/automation/models/workflow_node.py` |
| `automation` | `WorkflowEdge` | `backend_django/automation/models/workflow_edge.py` |
| `automation` | `ScreenState` | `backend_django/automation/models/screen_state.py` |
| `automation` | `ProgramElement` | `backend_django/automation/models/program_element.py` |
| `automation` | `Delay` | `backend_django/automation/models/delay.py` |
| `challenges` | `ChallengeAttempt` | `backend_django/challenges/models/challenge_attempt.py` |
| `challenges` | `ChallengeProgress` | `backend_django/challenges/models/challenge_progress.py` |
| `challenges` | `Challenge` | `backend_django/challenges/models/challenge.py` |
| `challenges` | `ChallengeStep` | `backend_django/challenges/models/challenge_step.py` |
| `codex` | `ArchitectureEdge` | `backend_django/codex/models/architecture_edge.py` |
| `codex` | `CodexAgentDefinition` | `backend_django/codex/models/codex_agent_definition.py` |
| `codex` | `LocalAIJob` | `backend_django/codex/models/local_ai_job.py` |
| `codex` | `CodexFinding` | `backend_django/codex/models/codex_finding.py` |
| `codex` | `CodexExecutionRequest` | `backend_django/codex/models/codex_execution_request.py` |
| `codex` | `CodexWorkflowStep` | `backend_django/codex/models/codex_workflow_step.py` |
| `codex` | `CodexConversation` | `backend_django/codex/models/codex_conversation.py` |
| `codex` | `ChangeSet` | `backend_django/codex/models/change_set.py` |
| `codex` | `APIEndpoint` | `backend_django/codex/models/api_endpoint.py` |
| `codex` | `CodexPolicy` | `backend_django/codex/models/codex_policy.py` |
| `codex` | `FileRegistry` | `backend_django/codex/models/file_registry.py` |
| `codex` | `CodexMessage` | `backend_django/codex/models/codex_message.py` |
| `codex` | `CodexChangeFile` | `backend_django/codex/models/codex_change_file.py` |
| `codex` | `ProtectedFeature` | `backend_django/codex/models/protected_feature.py` |
| `codex` | `CodexAgentRun` | `backend_django/codex/models/codex_agent_run.py` |
| `codex` | `ProtectedItem` | `backend_django/codex/models/protected_item.py` |
| `codex` | `Feature` | `backend_django/codex/models/feature.py` |
| `codex` | `CodexCapabilityRun` | `backend_django/codex/models/codex_capability_run.py` |
| `codex` | `CodexAnalysis` | `backend_django/codex/models/codex_analysis.py` |
| `codex` | `CodexAuditEvent` | `backend_django/codex/models/codex_audit_event.py` |
| `codex` | `CodexFeatureDefinition` | `backend_django/codex/models/codex_feature_definition.py` |
| `codex` | `ArchitectureNode` | `backend_django/codex/models/architecture_node.py` |
| `codex` | `ProjectSnapshot` | `backend_django/codex/models/project_snapshot.py` |
| `codex` | `CodexTool` | `backend_django/codex/models/codex_tool.py` |
| `codex` | `CodexToolDefinition` | `backend_django/codex/models/codex_tool_definition.py` |
| `codex` | `ProjectRegistry` | `backend_django/codex/models/project_registry.py` |
| `core` | `BaseModel` | `backend_django/core/models/base_model.py` |
| `core` | `UserLearningSettings` | `backend_django/core/models/user_learning_settings.py` |
| `crm` | `Interaction` | `backend_django/crm/models/interaction.py` |
| `crm` | `CustomerRelationship` | `backend_django/crm/models/customer_relationship.py` |
| `crm` | `Company` | `backend_django/crm/models/company.py` |
| `crm` | `Contact` | `backend_django/crm/models/contact.py` |
| `goals` | `Goal` | `backend_django/goals/models/goal.py` |
| `goals` | `GoalMilestone` | `backend_django/goals/models/goal_milestone.py` |
| `goals` | `GoalActivity` | `backend_django/goals/models/goal_activity.py` |
| `goals` | `GoalPlanProposal` | `backend_django/goals/models/goal_plan_proposal.py` |
| `jobs_opportunity` | `JobMatch` | `backend_django/jobs_opportunity/models/job_match.py` |
| `jobs_opportunity` | `JobSkillRequirement` | `backend_django/jobs_opportunity/models/job_skill_requirement.py` |
| `jobs_opportunity` | `JobResume` | `backend_django/jobs_opportunity/models/job_resume.py` |
| `jobs_opportunity` | `CompanyProfile` | `backend_django/jobs_opportunity/models/company_profile.py` |
| `jobs_opportunity` | `JobReadiness` | `backend_django/jobs_opportunity/models/job_readiness.py` |
| `jobs_opportunity` | `JobApplicationEvent` | `backend_django/jobs_opportunity/models/job_application_event.py` |
| `jobs_opportunity` | `JobAnalyticsSnapshot` | `backend_django/jobs_opportunity/models/job_analytics_snapshot.py` |
| `jobs_opportunity` | `JobCoverLetter` | `backend_django/jobs_opportunity/models/job_cover_letter.py` |
| `jobs_opportunity` | `JobAlert` | `backend_django/jobs_opportunity/models/job_alert.py` |
| `jobs_opportunity` | `JobSavedSearch` | `backend_django/jobs_opportunity/models/job_saved_search.py` |
| `jobs_opportunity` | `JobSkillGap` | `backend_django/jobs_opportunity/models/job_skill_gap.py` |
| `jobs_opportunity` | `JobApplication` | `backend_django/jobs_opportunity/models/job_application.py` |
| `jobs_opportunity` | `JobRecommendation` | `backend_django/jobs_opportunity/models/job_recommendation.py` |
| `jobs_opportunity` | `JobSource` | `backend_django/jobs_opportunity/models/job_source.py` |
| `jobs_opportunity` | `JobOpportunity` | `backend_django/jobs_opportunity/models/job_opportunity.py` |
| `jobs_opportunity` | `JobSourceSyncRun` | `backend_django/jobs_opportunity/models/job_source_sync_run.py` |
| `jobs_opportunity` | `JobPreference` | `backend_django/jobs_opportunity/models/job_preference.py` |
| `jobs_opportunity` | `JobInterview` | `backend_django/jobs_opportunity/models/job_interview.py` |
| `knowledge` | `KnowledgeFile` | `backend_django/knowledge/models/knowledge_file.py` |
| `knowledge` | `KnowledgeItem` | `backend_django/knowledge/models/knowledge_item.py` |
| `learning` | `AssessmentChoice` | `backend_django/learning/models/assessment_choice.py` |
| `learning` | `Skill` | `backend_django/learning/models/skill.py` |
| `learning` | `LearningProgress` | `backend_django/learning/models/learning_progress.py` |
| `learning` | `LearningNote` | `backend_django/learning/models/learning_note.py` |
| `learning` | `ApplicationSubmission` | `backend_django/learning/models/application_submission.py` |
| `learning` | `LearningSession` | `backend_django/learning/models/learning_session.py` |
| `learning` | `KnowledgeApplication` | `backend_django/learning/models/knowledge_application.py` |
| `learning` | `AssessmentAttempt` | `backend_django/learning/models/assessment_attempt.py` |
| `learning` | `AssessmentQuestion` | `backend_django/learning/models/assessment_question.py` |
| `learning` | `LearningPath` | `backend_django/learning/models/learning_path.py` |
| `learning` | `Assessment` | `backend_django/learning/models/assessment.py` |
| `learning` | `LearningTopic` | `backend_django/learning/models/learning_topic.py` |
| `learning` | `ApplicationReview` | `backend_django/learning/models/application_review.py` |
| `learning` | `LearningGoal` | `backend_django/learning/models/learning_goal.py` |
| `learning` | `LearningResource` | `backend_django/learning/models/learning_resource.py` |
| `learning` | `AssessmentResponse` | `backend_django/learning/models/assessment_response.py` |
| `learning` | `LearningRevision` | `backend_django/learning/models/learning_revision.py` |
| `learning` | `Lesson` | `backend_django/learning/models/lesson.py` |
| `marketing` | `MarketingContent` | `backend_django/marketing/models/marketing_content.py` |
| `marketing` | `Campaign` | `backend_django/marketing/models/campaign.py` |
| `marketing` | `LeadSource` | `backend_django/marketing/models/lead_source.py` |
| `marketing` | `MarketingChannel` | `backend_django/marketing/models/marketing_channel.py` |
| `memory` | `MemoryItem` | `backend_django/memory/models/memory_item.py` |
| `notification` | `Notification` | `backend_django/notification/models/notification.py` |
| `personal_finance` | `FinancialProfile` | `backend_django/personal_finance/models/financial_profile.py` |
| `personal_finance` | `Budget` | `backend_django/personal_finance/models/budget.py` |
| `personal_finance` | `Debt` | `backend_django/personal_finance/models/debt.py` |
| `personal_finance` | `Category` | `backend_django/personal_finance/models/category.py` |
| `personal_finance` | `FinancialScenario` | `backend_django/personal_finance/models/financial_scenario.py` |
| `personal_finance` | `Transaction` | `backend_django/personal_finance/models/transaction.py` |
| `personal_finance` | `LoanPayment` | `backend_django/personal_finance/models/loan_payment.py` |
| `personal_finance` | `RecurringCashflow` | `backend_django/personal_finance/models/recurring_cashflow.py` |
| `personal_finance` | `DebtPayment` | `backend_django/personal_finance/models/debt_payment.py` |
| `personal_finance` | `FinancialHabit` | `backend_django/personal_finance/models/financial_habit.py` |
| `personal_finance` | `FinancialAlert` | `backend_django/personal_finance/models/financial_alert.py` |
| `personal_finance` | `SavingsGoal` | `backend_django/personal_finance/models/savings_goal.py` |
| `personal_finance` | `Subscription` | `backend_django/personal_finance/models/subscription.py` |
| `personal_finance` | `SavingPlan` | `backend_django/personal_finance/models/saving_plan.py` |
| `personal_finance` | `LendingBorrowing` | `backend_django/personal_finance/models/lending_borrowing.py` |
| `projects` | `ProjectMember` | `backend_django/projects/models/project_member.py` |
| `projects` | `ProjectGoal` | `backend_django/projects/models/project_goal.py` |
| `projects` | `Project` | `backend_django/projects/models/project.py` |
| `projects` | `ProjectContext` | `backend_django/projects/models/project_context.py` |
| `projects` | `ProjectTask` | `backend_django/projects/models/project_task.py` |
| `revenue` | `RevenueSource` | `backend_django/revenue/models/revenue_source.py` |
| `revenue` | `RevenueStream` | `backend_django/revenue/models/revenue_stream.py` |
| `revenue` | `RevenueRecord` | `backend_django/revenue/models/revenue_record.py` |
| `revenue` | `RecurringRevenue` | `backend_django/revenue/models/recurring_revenue.py` |
| `sales` | `SalesActivity` | `backend_django/sales/models/sales_activity.py` |
| `sales` | `Offer` | `backend_django/sales/models/offer.py` |
| `sales` | `Sale` | `backend_django/sales/models/sale.py` |
| `sales` | `Deal` | `backend_django/sales/models/deal.py` |
| `scraper` | `ScrapingJob` | `backend_django/scraper/models/scraping_job.py` |
| `scraper` | `ScrapingConfig` | `backend_django/scraper/models/scraping_config.py` |
| `scraper` | `ScrapedData` | `backend_django/scraper/models/scraped_data.py` |
| `scraper` | `ParentSelector` | `backend_django/scraper/models/parent_selector.py` |
| `scraper` | `Website` | `backend_django/scraper/models/website.py` |
| `social` | `Friendship` | `backend_django/social/models/friendship.py` |
| `social` | `SocialProfile` | `backend_django/social/models/social_profile.py` |
| `social` | `FriendshipRequest` | `backend_django/social/models/friendship_request.py` |
| `social` | `SocialRecommendation` | `backend_django/social/models/social_recommendation.py` |
| `social` | `UserBlock` | `backend_django/social/models/user_block.py` |
| `social` | `Follow` | `backend_django/social/models/follow.py` |
| `tasks` | `Task` | `backend_django/tasks/models/task.py` |

## Declared model relationships (heuristic)

| Source app/model | Field | Relation type | Target expression | Source file |
|---|---|---|---|---|
| `agents.AgentConfiguration` | `agent` | `ForeignKey` | `agents.Agent` | `backend_django/agents/models/agent_configuration.py` |
| `agents.AgentRun` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/agents/models/agent_run.py` |
| `agents.AgentRun` | `agent` | `ForeignKey` | `agents.Agent` | `backend_django/agents/models/agent_run.py` |
| `agents.AgentRun` | `configuration` | `ForeignKey` | `agents.AgentConfiguration` | `backend_django/agents/models/agent_run.py` |
| `agents.Agent` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/agents/models/agent.py` |
| `agents.AgentExecution` | `run` | `ForeignKey` | `agents.AgentRun` | `backend_django/agents/models/agent_execution.py` |
| `ai.AIConversation` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/ai/models/conversations.py` |
| `ai.AIMessage` | `conversation` | `ForeignKey` | `AIConversation` | `backend_django/ai/models/conversations.py` |
| `ai.AISettings` | `user` | `OneToOneField` | `settings.AUTH_USER_MODEL` | `backend_django/ai/models/settings.py` |
| `ai.AISettings` | `default_prompt_profile` | `ForeignKey` | `ai.AIPromptProfile` | `backend_django/ai/models/settings.py` |
| `ai.AIPromptProfile` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/ai/models/prompts.py` |
| `ai.AIUsageRecord` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/ai/models/usage.py` |
| `ai.AIUsageRecord` | `execution` | `OneToOneField` | `ai.AIExecution` | `backend_django/ai/models/usage.py` |
| `ai.AIProviderCredential` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/ai/models/providers.py` |
| `ai.AIProviderConfig` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/ai/models/providers.py` |
| `ai.AIExecution` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/ai/models/executions.py` |
| `ai.AIExecution` | `conversation` | `ForeignKey` | `AIConversation` | `backend_django/ai/models/executions.py` |
| `ai.AIFeedback` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/ai/models/feedback.py` |
| `ai.AIFeedback` | `message` | `ForeignKey` | `ai.AIMessage` | `backend_django/ai/models/feedback.py` |
| `ai.AIWorkflowDefinition` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/ai/models/workflows.py` |
| `ai.AIWorkflowRun` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/ai/models/workflows.py` |
| `ai.AIWorkflowRun` | `workflow` | `ForeignKey` | `ai.AIWorkflowDefinition` | `backend_django/ai/models/workflows.py` |
| `ai.AIWorkflowRun` | `execution` | `ForeignKey` | `ai.AIExecution` | `backend_django/ai/models/workflows.py` |
| `ai.AIBudgetPolicy` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/ai/models/budgets.py` |
| `ai.AIBudgetReservation` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/ai/models/budgets.py` |
| `ai.AIBudgetReservation` | `policy` | `ForeignKey` | `AIBudgetPolicy` | `backend_django/ai/models/budgets.py` |
| `ai.AiAuditLog` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/ai/models/audit.py` |
| `ai_tools_laboratory.Tool` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/ai_tools_laboratory/models/tool.py` |
| `ai_tools_laboratory.Tool` | `category` | `ForeignKey` | `ai_tools_laboratory.ToolCategory` | `backend_django/ai_tools_laboratory/models/tool.py` |
| `ai_tools_laboratory.ToolExecution` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/ai_tools_laboratory/models/tool_execution.py` |
| `ai_tools_laboratory.ToolExecution` | `tool` | `ForeignKey` | `ai_tools_laboratory.Tool` | `backend_django/ai_tools_laboratory/models/tool_execution.py` |
| `ai_tools_laboratory.ToolExecution` | `configuration` | `ForeignKey` | `ai_tools_laboratory.ToolConfiguration` | `backend_django/ai_tools_laboratory/models/tool_execution.py` |
| `ai_tools_laboratory.ToolConfiguration` | `tool` | `ForeignKey` | `ai_tools_laboratory.Tool` | `backend_django/ai_tools_laboratory/models/tool_configuration.py` |
| `ai_tools_laboratory.ToolCategory` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/ai_tools_laboratory/models/tool_category.py` |
| `analytics.Report` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/analytics/models/report.py` |
| `analytics.Metric` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/analytics/models/metric.py` |
| `analytics.AnalyticsEvent` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/analytics/models/analytics_event.py` |
| `analytics.MetricSnapshot` | `metric` | `ForeignKey` | `analytics.Metric` | `backend_django/analytics/models/metric_snapshot.py` |
| `architecture.Dependency` | `source` | `ForeignKey` | `architecture.Component` | `backend_django/architecture/models/dependency.py` |
| `architecture.Dependency` | `target` | `ForeignKey` | `architecture.Component` | `backend_django/architecture/models/dependency.py` |
| `architecture.Component` | `architecture` | `ForeignKey` | `architecture.Architecture` | `backend_django/architecture/models/component.py` |
| `architecture.ArchitectureDecision` | `architecture` | `ForeignKey` | `architecture.Architecture` | `backend_django/architecture/models/architecture_decision.py` |
| `architecture.ArchitectureDecision` | `superseded_by` | `ForeignKey` | `architecture.ArchitectureDecision` | `backend_django/architecture/models/architecture_decision.py` |
| `architecture.Architecture` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/architecture/models/architecture.py` |
| `automation.Task` | `created_by` | `ForeignKey` | `User` | `backend_django/automation/models/task.py` |
| `automation.Task` | `program` | `ForeignKey` | `Program` | `backend_django/automation/models/task.py` |
| `automation.TaskRun` | `created_by` | `ForeignKey` | `User` | `backend_django/automation/models/task_run.py` |
| `automation.TaskRun` | `workflow` | `ForeignKey` | `Workflow` | `backend_django/automation/models/task_run.py` |
| `automation.Workflow` | `created_by` | `ForeignKey` | `User` | `backend_django/automation/models/workflow.py` |
| `automation.Action` | `created_by` | `ForeignKey` | `User` | `backend_django/automation/models/action.py` |
| `automation.Action` | `node` | `ForeignKey` | `WorkflowNode` | `backend_django/automation/models/action.py` |
| `automation.Program` | `created_by` | `ForeignKey` | `User` | `backend_django/automation/models/program.py` |
| `automation.WorkflowNode` | `created_by` | `ForeignKey` | `User` | `backend_django/automation/models/workflow_node.py` |
| `automation.WorkflowNode` | `workflow` | `ForeignKey` | `Workflow` | `backend_django/automation/models/workflow_node.py` |
| `automation.WorkflowNode` | `program` | `ForeignKey` | `Program` | `backend_django/automation/models/workflow_node.py` |
| `automation.WorkflowNode` | `element` | `ForeignKey` | `ProgramElement` | `backend_django/automation/models/workflow_node.py` |
| `automation.WorkflowEdge` | `created_by` | `ForeignKey` | `User` | `backend_django/automation/models/workflow_edge.py` |
| `automation.WorkflowEdge` | `workflow` | `ForeignKey` | `Workflow` | `backend_django/automation/models/workflow_edge.py` |
| `automation.WorkflowEdge` | `source_node` | `ForeignKey` | `WorkflowNode` | `backend_django/automation/models/workflow_edge.py` |
| `automation.WorkflowEdge` | `target_node` | `ForeignKey` | `WorkflowNode` | `backend_django/automation/models/workflow_edge.py` |
| `automation.ScreenState` | `created_by` | `ForeignKey` | `User` | `backend_django/automation/models/screen_state.py` |
| `automation.ScreenState` | `task_run` | `ForeignKey` | `TaskRun` | `backend_django/automation/models/screen_state.py` |
| `automation.ProgramElement` | `created_by` | `ForeignKey` | `User` | `backend_django/automation/models/program_element.py` |
| `automation.ProgramElement` | `program` | `ForeignKey` | `Program` | `backend_django/automation/models/program_element.py` |
| `automation.ProgramElement` | `parent_element` | `ForeignKey` | `self` | `backend_django/automation/models/program_element.py` |
| `automation.Delay` | `created_by` | `ForeignKey` | `User` | `backend_django/automation/models/delay.py` |
| `challenges.ChallengeAttempt` | `challenge` | `ForeignKey` | `Challenge` | `backend_django/challenges/models/challenge_attempt.py` |
| `challenges.ChallengeAttempt` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/challenges/models/challenge_attempt.py` |
| `challenges.ChallengeProgress` | `challenge` | `ForeignKey` | `Challenge` | `backend_django/challenges/models/challenge_progress.py` |
| `challenges.ChallengeProgress` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/challenges/models/challenge_progress.py` |
| `challenges.Challenge` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/challenges/models/challenge.py` |
| `challenges.Challenge` | `skill` | `ForeignKey` | `learning.Skill` | `backend_django/challenges/models/challenge.py` |
| `challenges.Challenge` | `project` | `ForeignKey` | `projects.Project` | `backend_django/challenges/models/challenge.py` |
| `challenges.Challenge` | `goal` | `ForeignKey` | `goals.Goal` | `backend_django/challenges/models/challenge.py` |
| `challenges.ChallengeStep` | `challenge` | `ForeignKey` | `Challenge` | `backend_django/challenges/models/challenge_step.py` |
| `codex.ArchitectureEdge` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/architecture_edge.py` |
| `codex.ArchitectureEdge` | `source` | `ForeignKey` | `ArchitectureNode` | `backend_django/codex/models/architecture_edge.py` |
| `codex.ArchitectureEdge` | `target` | `ForeignKey` | `ArchitectureNode` | `backend_django/codex/models/architecture_edge.py` |
| `codex.CodexAgentDefinition` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/codex_agent_definition.py` |
| `codex.LocalAIJob` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/local_ai_job.py` |
| `codex.LocalAIJob` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/codex/models/local_ai_job.py` |
| `codex.CodexFinding` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/codex_finding.py` |
| `codex.CodexExecutionRequest` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/codex_execution_request.py` |
| `codex.CodexExecutionRequest` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/codex/models/codex_execution_request.py` |
| `codex.CodexWorkflowStep` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/codex_workflow_step.py` |
| `codex.CodexConversation` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/codex_conversation.py` |
| `codex.CodexConversation` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/codex/models/codex_conversation.py` |
| `codex.ChangeSet` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/change_set.py` |
| `codex.ChangeSet` | `created_by` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/codex/models/change_set.py` |
| `codex.APIEndpoint` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/api_endpoint.py` |
| `codex.CodexPolicy` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/codex_policy.py` |
| `codex.CodexPolicy` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/codex/models/codex_policy.py` |
| `codex.FileRegistry` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/file_registry.py` |
| `codex.CodexMessage` | `conversation` | `ForeignKey` | `CodexConversation` | `backend_django/codex/models/codex_message.py` |
| `codex.CodexChangeFile` | `changeset` | `ForeignKey` | `ChangeSet` | `backend_django/codex/models/codex_change_file.py` |
| `codex.ProtectedFeature` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/protected_feature.py` |
| `codex.ProtectedFeature` | `feature` | `ForeignKey` | `Feature` | `backend_django/codex/models/protected_feature.py` |
| `codex.CodexAgentRun` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/codex_agent_run.py` |
| `codex.CodexAgentRun` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/codex/models/codex_agent_run.py` |
| `codex.ProtectedItem` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/protected_item.py` |
| `codex.ProtectedItem` | `approved_by` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/codex/models/protected_item.py` |
| `codex.Feature` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/feature.py` |
| `codex.CodexCapabilityRun` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/codex_capability_run.py` |
| `codex.CodexCapabilityRun` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/codex/models/codex_capability_run.py` |
| `codex.CodexAnalysis` | `conversation` | `ForeignKey` | `CodexConversation` | `backend_django/codex/models/codex_analysis.py` |
| `codex.CodexAuditEvent` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/codex_audit_event.py` |
| `codex.CodexAuditEvent` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/codex/models/codex_audit_event.py` |
| `codex.CodexFeatureDefinition` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/codex_feature_definition.py` |
| `codex.ArchitectureNode` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/architecture_node.py` |
| `codex.ProjectSnapshot` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/project_snapshot.py` |
| `codex.ProjectSnapshot` | `created_by` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/codex/models/project_snapshot.py` |
| `codex.CodexTool` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/codex_tool.py` |
| `codex.CodexToolDefinition` | `project` | `ForeignKey` | `ProjectRegistry` | `backend_django/codex/models/codex_tool_definition.py` |
| `core.UserLearningSettings` | `user` | `OneToOneField` | `settings.AUTH_USER_MODEL` | `backend_django/core/models/user_learning_settings.py` |
| `core.UserLearningSettings` | `current_learning_goal` | `ForeignKey` | `learning.LearningGoal` | `backend_django/core/models/user_learning_settings.py` |
| `crm.Interaction` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/crm/models/interaction.py` |
| `crm.Interaction` | `contact` | `ForeignKey` | `crm.Contact` | `backend_django/crm/models/interaction.py` |
| `crm.CustomerRelationship` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/crm/models/customer_relationship.py` |
| `crm.CustomerRelationship` | `contact` | `OneToOneField` | `crm.Contact` | `backend_django/crm/models/customer_relationship.py` |
| `crm.Company` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/crm/models/company.py` |
| `crm.Contact` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/crm/models/contact.py` |
| `crm.Contact` | `company` | `ForeignKey` | `crm.Company` | `backend_django/crm/models/contact.py` |
| `goals.Goal` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/goals/models/goal.py` |
| `goals.Goal` | `learning_goals` | `ManyToManyField` | `learning.LearningGoal` | `backend_django/goals/models/goal.py` |
| `goals.Goal` | `skills` | `ManyToManyField` | `learning.Skill` | `backend_django/goals/models/goal.py` |
| `goals.Goal` | `related_goals` | `ManyToManyField` | `self` | `backend_django/goals/models/goal.py` |
| `goals.GoalMilestone` | `goal` | `ForeignKey` | `Goal` | `backend_django/goals/models/goal_milestone.py` |
| `goals.GoalMilestone` | `depends_on` | `ManyToManyField` | `self` | `backend_django/goals/models/goal_milestone.py` |
| `goals.GoalActivity` | `goal` | `ForeignKey` | `Goal` | `backend_django/goals/models/goal_activity.py` |
| `goals.GoalActivity` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/goals/models/goal_activity.py` |
| `goals.GoalPlanProposal` | `goal` | `ForeignKey` | `Goal` | `backend_django/goals/models/goal_plan_proposal.py` |
| `goals.GoalPlanProposal` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/goals/models/goal_plan_proposal.py` |
| `jobs_opportunity.JobMatch` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/jobs_opportunity/models/job_match.py` |
| `jobs_opportunity.JobMatch` | `job` | `ForeignKey` | `JobOpportunity` | `backend_django/jobs_opportunity/models/job_match.py` |
| `jobs_opportunity.JobSkillRequirement` | `job` | `ForeignKey` | `JobOpportunity` | `backend_django/jobs_opportunity/models/job_skill_requirement.py` |
| `jobs_opportunity.JobSkillRequirement` | `skill` | `ForeignKey` | `learning.Skill` | `backend_django/jobs_opportunity/models/job_skill_requirement.py` |
| `jobs_opportunity.JobResume` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/jobs_opportunity/models/job_resume.py` |
| `jobs_opportunity.CompanyProfile` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/jobs_opportunity/models/company_profile.py` |
| `jobs_opportunity.JobReadiness` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/jobs_opportunity/models/job_readiness.py` |
| `jobs_opportunity.JobReadiness` | `job` | `ForeignKey` | `JobOpportunity` | `backend_django/jobs_opportunity/models/job_readiness.py` |
| `jobs_opportunity.JobApplicationEvent` | `application` | `ForeignKey` | `JobApplication` | `backend_django/jobs_opportunity/models/job_application_event.py` |
| `jobs_opportunity.JobAnalyticsSnapshot` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/jobs_opportunity/models/job_analytics_snapshot.py` |
| `jobs_opportunity.JobCoverLetter` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/jobs_opportunity/models/job_cover_letter.py` |
| `jobs_opportunity.JobCoverLetter` | `job` | `ForeignKey` | `JobOpportunity` | `backend_django/jobs_opportunity/models/job_cover_letter.py` |
| `jobs_opportunity.JobCoverLetter` | `resume` | `ForeignKey` | `JobResume` | `backend_django/jobs_opportunity/models/job_cover_letter.py` |
| `jobs_opportunity.JobAlert` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/jobs_opportunity/models/job_alert.py` |
| `jobs_opportunity.JobSavedSearch` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/jobs_opportunity/models/job_saved_search.py` |
| `jobs_opportunity.JobSkillGap` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/jobs_opportunity/models/job_skill_gap.py` |
| `jobs_opportunity.JobSkillGap` | `job` | `ForeignKey` | `JobOpportunity` | `backend_django/jobs_opportunity/models/job_skill_gap.py` |
| `jobs_opportunity.JobSkillGap` | `skill` | `ForeignKey` | `learning.Skill` | `backend_django/jobs_opportunity/models/job_skill_gap.py` |
| `jobs_opportunity.JobSkillGap` | `learning_goal` | `ForeignKey` | `learning.LearningGoal` | `backend_django/jobs_opportunity/models/job_skill_gap.py` |
| `jobs_opportunity.JobApplication` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/jobs_opportunity/models/job_application.py` |
| `jobs_opportunity.JobApplication` | `job` | `ForeignKey` | `JobOpportunity` | `backend_django/jobs_opportunity/models/job_application.py` |
| `jobs_opportunity.JobApplication` | `resume` | `ForeignKey` | `JobResume` | `backend_django/jobs_opportunity/models/job_application.py` |
| `jobs_opportunity.JobApplication` | `cover_letter` | `ForeignKey` | `JobCoverLetter` | `backend_django/jobs_opportunity/models/job_application.py` |
| `jobs_opportunity.JobRecommendation` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/jobs_opportunity/models/job_recommendation.py` |
| `jobs_opportunity.JobRecommendation` | `job` | `ForeignKey` | `JobOpportunity` | `backend_django/jobs_opportunity/models/job_recommendation.py` |
| `jobs_opportunity.JobSource` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/jobs_opportunity/models/job_source.py` |
| `jobs_opportunity.JobOpportunity` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/jobs_opportunity/models/job_opportunity.py` |
| `jobs_opportunity.JobOpportunity` | `source` | `ForeignKey` | `JobSource` | `backend_django/jobs_opportunity/models/job_opportunity.py` |
| `jobs_opportunity.JobOpportunity` | `company_profile` | `ForeignKey` | `CompanyProfile` | `backend_django/jobs_opportunity/models/job_opportunity.py` |
| `jobs_opportunity.JobOpportunity` | `required_skills` | `ManyToManyField` | `learning.Skill` | `backend_django/jobs_opportunity/models/job_opportunity.py` |
| `jobs_opportunity.JobSourceSyncRun` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/jobs_opportunity/models/job_source_sync_run.py` |
| `jobs_opportunity.JobSourceSyncRun` | `source` | `ForeignKey` | `JobSource` | `backend_django/jobs_opportunity/models/job_source_sync_run.py` |
| `jobs_opportunity.JobPreference` | `user` | `OneToOneField` | `settings.AUTH_USER_MODEL` | `backend_django/jobs_opportunity/models/job_preference.py` |
| `jobs_opportunity.JobInterview` | `application` | `ForeignKey` | `JobApplication` | `backend_django/jobs_opportunity/models/job_interview.py` |
| `knowledge.KnowledgeFile` | `knowledge` | `ForeignKey` | `KnowledgeItem` | `backend_django/knowledge/models/knowledge_file.py` |
| `knowledge.KnowledgeItem` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/knowledge/models/knowledge_item.py` |
| `learning.AssessmentChoice` | `question` | `ForeignKey` | `AssessmentQuestion` | `backend_django/learning/models/assessment_choice.py` |
| `learning.LearningProgress` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/learning/models/learning_progress.py` |
| `learning.LearningProgress` | `topic` | `ForeignKey` | `LearningTopic` | `backend_django/learning/models/learning_progress.py` |
| `learning.LearningNote` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/learning/models/learning_note.py` |
| `learning.LearningNote` | `topic` | `ForeignKey` | `LearningTopic` | `backend_django/learning/models/learning_note.py` |
| `learning.LearningNote` | `lesson` | `ForeignKey` | `Lesson` | `backend_django/learning/models/learning_note.py` |
| `learning.LearningNote` | `knowledge_item` | `ForeignKey` | `knowledge.KnowledgeItem` | `backend_django/learning/models/learning_note.py` |
| `learning.ApplicationSubmission` | `application` | `ForeignKey` | `KnowledgeApplication` | `backend_django/learning/models/application_submission.py` |
| `learning.LearningSession` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/learning/models/learning_session.py` |
| `learning.LearningSession` | `topic` | `ForeignKey` | `LearningTopic` | `backend_django/learning/models/learning_session.py` |
| `learning.LearningSession` | `lesson` | `ForeignKey` | `Lesson` | `backend_django/learning/models/learning_session.py` |
| `learning.KnowledgeApplication` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/learning/models/knowledge_application.py` |
| `learning.KnowledgeApplication` | `topic` | `ForeignKey` | `LearningTopic` | `backend_django/learning/models/knowledge_application.py` |
| `learning.KnowledgeApplication` | `lesson` | `ForeignKey` | `Lesson` | `backend_django/learning/models/knowledge_application.py` |
| `learning.KnowledgeApplication` | `knowledge_item` | `ForeignKey` | `knowledge.KnowledgeItem` | `backend_django/learning/models/knowledge_application.py` |
| `learning.AssessmentAttempt` | `assessment` | `ForeignKey` | `Assessment` | `backend_django/learning/models/assessment_attempt.py` |
| `learning.AssessmentAttempt` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/learning/models/assessment_attempt.py` |
| `learning.AssessmentQuestion` | `assessment` | `ForeignKey` | `Assessment` | `backend_django/learning/models/assessment_question.py` |
| `learning.LearningPath` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/learning/models/learning_path.py` |
| `learning.LearningPath` | `goal` | `ForeignKey` | `LearningGoal` | `backend_django/learning/models/learning_path.py` |
| `learning.Assessment` | `topic` | `ForeignKey` | `LearningTopic` | `backend_django/learning/models/assessment.py` |
| `learning.LearningTopic` | `path` | `ForeignKey` | `LearningPath` | `backend_django/learning/models/learning_topic.py` |
| `learning.LearningTopic` | `skill` | `ForeignKey` | `Skill` | `backend_django/learning/models/learning_topic.py` |
| `learning.LearningTopic` | `prerequisites` | `ManyToManyField` | `self` | `backend_django/learning/models/learning_topic.py` |
| `learning.LearningTopic` | `knowledge_item` | `ForeignKey` | `knowledge.KnowledgeItem` | `backend_django/learning/models/learning_topic.py` |
| `learning.ApplicationReview` | `submission` | `ForeignKey` | `ApplicationSubmission` | `backend_django/learning/models/application_review.py` |
| `learning.ApplicationReview` | `application` | `ForeignKey` | `KnowledgeApplication` | `backend_django/learning/models/application_review.py` |
| `learning.LearningGoal` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/learning/models/learning_goal.py` |
| `learning.LearningGoal` | `skill` | `ForeignKey` | `Skill` | `backend_django/learning/models/learning_goal.py` |
| `learning.LearningResource` | `topic` | `ForeignKey` | `LearningTopic` | `backend_django/learning/models/learning_resource.py` |
| `learning.LearningResource` | `lesson` | `ForeignKey` | `Lesson` | `backend_django/learning/models/learning_resource.py` |
| `learning.AssessmentResponse` | `attempt` | `ForeignKey` | `AssessmentAttempt` | `backend_django/learning/models/assessment_response.py` |
| `learning.AssessmentResponse` | `question` | `ForeignKey` | `AssessmentQuestion` | `backend_django/learning/models/assessment_response.py` |
| `learning.AssessmentResponse` | `selected_choices` | `ManyToManyField` | `AssessmentChoice` | `backend_django/learning/models/assessment_response.py` |
| `learning.LearningRevision` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/learning/models/learning_revision.py` |
| `learning.LearningRevision` | `topic` | `ForeignKey` | `LearningTopic` | `backend_django/learning/models/learning_revision.py` |
| `learning.LearningRevision` | `source_review` | `ForeignKey` | `ApplicationReview` | `backend_django/learning/models/learning_revision.py` |
| `learning.Lesson` | `topic` | `ForeignKey` | `LearningTopic` | `backend_django/learning/models/lesson.py` |
| `marketing.MarketingContent` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/marketing/models/marketing_content.py` |
| `marketing.MarketingContent` | `campaign` | `ForeignKey` | `marketing.Campaign` | `backend_django/marketing/models/marketing_content.py` |
| `marketing.Campaign` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/marketing/models/campaign.py` |
| `marketing.Campaign` | `channel` | `ForeignKey` | `marketing.MarketingChannel` | `backend_django/marketing/models/campaign.py` |
| `marketing.LeadSource` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/marketing/models/lead_source.py` |
| `marketing.LeadSource` | `channel` | `ForeignKey` | `marketing.MarketingChannel` | `backend_django/marketing/models/lead_source.py` |
| `marketing.LeadSource` | `campaign` | `ForeignKey` | `marketing.Campaign` | `backend_django/marketing/models/lead_source.py` |
| `marketing.LeadSource` | `contacts` | `ManyToManyField` | `crm.Contact` | `backend_django/marketing/models/lead_source.py` |
| `marketing.MarketingChannel` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/marketing/models/marketing_channel.py` |
| `memory.MemoryItem` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/memory/models/memory_item.py` |
| `notification.Notification` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/notification/models/notification.py` |
| `notification.Notification` | `content_type` | `ForeignKey` | `ContentType` | `backend_django/notification/models/notification.py` |
| `notification.Notification` | `content_object` | `GenericForeignKey` | `content_type` | `backend_django/notification/models/notification.py` |
| `personal_finance.FinancialProfile` | `user` | `OneToOneField` | `settings.AUTH_USER_MODEL` | `backend_django/personal_finance/models/financial_profile.py` |
| `personal_finance.Budget` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/personal_finance/models/budget.py` |
| `personal_finance.Budget` | `category` | `ForeignKey` | `Category` | `backend_django/personal_finance/models/budget.py` |
| `personal_finance.Debt` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/personal_finance/models/debt.py` |
| `personal_finance.Category` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/personal_finance/models/category.py` |
| `personal_finance.FinancialScenario` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/personal_finance/models/financial_scenario.py` |
| `personal_finance.Transaction` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/personal_finance/models/transaction.py` |
| `personal_finance.Transaction` | `category` | `ForeignKey` | `Category` | `backend_django/personal_finance/models/transaction.py` |
| `personal_finance.LoanPayment` | `loan` | `ForeignKey` | `LendingBorrowing` | `backend_django/personal_finance/models/loan_payment.py` |
| `personal_finance.LoanPayment` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/personal_finance/models/loan_payment.py` |
| `personal_finance.RecurringCashflow` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/personal_finance/models/recurring_cashflow.py` |
| `personal_finance.DebtPayment` | `debt` | `ForeignKey` | `Debt` | `backend_django/personal_finance/models/debt_payment.py` |
| `personal_finance.DebtPayment` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/personal_finance/models/debt_payment.py` |
| `personal_finance.DebtPayment` | `transaction` | `OneToOneField` | `Transaction` | `backend_django/personal_finance/models/debt_payment.py` |
| `personal_finance.FinancialHabit` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/personal_finance/models/financial_habit.py` |
| `personal_finance.FinancialAlert` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/personal_finance/models/financial_alert.py` |
| `personal_finance.SavingsGoal` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/personal_finance/models/savings_goal.py` |
| `personal_finance.SavingsGoal` | `general_goal` | `ForeignKey` | `goals.Goal` | `backend_django/personal_finance/models/savings_goal.py` |
| `personal_finance.Subscription` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/personal_finance/models/subscription.py` |
| `personal_finance.SavingPlan` | `goal` | `OneToOneField` | `SavingsGoal` | `backend_django/personal_finance/models/saving_plan.py` |
| `personal_finance.SavingPlan` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/personal_finance/models/saving_plan.py` |
| `personal_finance.LendingBorrowing` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/personal_finance/models/lending_borrowing.py` |
| `projects.ProjectMember` | `project` | `ForeignKey` | `Project` | `backend_django/projects/models/project_member.py` |
| `projects.ProjectMember` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/projects/models/project_member.py` |
| `projects.ProjectGoal` | `project` | `ForeignKey` | `Project` | `backend_django/projects/models/project_goal.py` |
| `projects.ProjectGoal` | `goal` | `ForeignKey` | `goals.Goal` | `backend_django/projects/models/project_goal.py` |
| `projects.Project` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/projects/models/project.py` |
| `projects.ProjectContext` | `project` | `OneToOneField` | `Project` | `backend_django/projects/models/project_context.py` |
| `projects.ProjectTask` | `project` | `ForeignKey` | `Project` | `backend_django/projects/models/project_task.py` |
| `projects.ProjectTask` | `task` | `ForeignKey` | `tasks.Task` | `backend_django/projects/models/project_task.py` |
| `revenue.RevenueSource` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/revenue/models/revenue_source.py` |
| `revenue.RevenueStream` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/revenue/models/revenue_stream.py` |
| `revenue.RevenueStream` | `source` | `ForeignKey` | `revenue.RevenueSource` | `backend_django/revenue/models/revenue_stream.py` |
| `revenue.RevenueRecord` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/revenue/models/revenue_record.py` |
| `revenue.RevenueRecord` | `stream` | `ForeignKey` | `revenue.RevenueStream` | `backend_django/revenue/models/revenue_record.py` |
| `revenue.RevenueRecord` | `sale` | `ForeignKey` | `sales.Sale` | `backend_django/revenue/models/revenue_record.py` |
| `revenue.RecurringRevenue` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/revenue/models/recurring_revenue.py` |
| `revenue.RecurringRevenue` | `stream` | `ForeignKey` | `revenue.RevenueStream` | `backend_django/revenue/models/recurring_revenue.py` |
| `sales.SalesActivity` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/sales/models/sales_activity.py` |
| `sales.SalesActivity` | `deal` | `ForeignKey` | `sales.Deal` | `backend_django/sales/models/sales_activity.py` |
| `sales.Offer` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/sales/models/offer.py` |
| `sales.Offer` | `project` | `ForeignKey` | `projects.Project` | `backend_django/sales/models/offer.py` |
| `sales.Sale` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/sales/models/sale.py` |
| `sales.Sale` | `deal` | `ForeignKey` | `sales.Deal` | `backend_django/sales/models/sale.py` |
| `sales.Sale` | `offer` | `ForeignKey` | `sales.Offer` | `backend_django/sales/models/sale.py` |
| `sales.Sale` | `contact` | `ForeignKey` | `crm.Contact` | `backend_django/sales/models/sale.py` |
| `sales.Deal` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/sales/models/deal.py` |
| `sales.Deal` | `contact` | `ForeignKey` | `crm.Contact` | `backend_django/sales/models/deal.py` |
| `sales.Deal` | `offer` | `ForeignKey` | `sales.Offer` | `backend_django/sales/models/deal.py` |
| `scraper.ScrapingJob` | `website` | `ForeignKey` | `Website` | `backend_django/scraper/models/scraping_job.py` |
| `scraper.ScrapingConfig` | `parent` | `ForeignKey` | `ParentSelector` | `backend_django/scraper/models/scraping_config.py` |
| `scraper.ScrapedData` | `job` | `ForeignKey` | `ScrapingJob` | `backend_django/scraper/models/scraped_data.py` |
| `scraper.ParentSelector` | `website` | `ForeignKey` | `Website` | `backend_django/scraper/models/parent_selector.py` |
| `scraper.Website` | `created_by` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/scraper/models/website.py` |
| `social.Friendship` | `user1` | `ForeignKey` | `User` | `backend_django/social/models/friendship.py` |
| `social.Friendship` | `user2` | `ForeignKey` | `User` | `backend_django/social/models/friendship.py` |
| `social.SocialProfile` | `user` | `OneToOneField` | `User` | `backend_django/social/models/social_profile.py` |
| `social.FriendshipRequest` | `sender` | `ForeignKey` | `User` | `backend_django/social/models/friendship_request.py` |
| `social.FriendshipRequest` | `receiver` | `ForeignKey` | `User` | `backend_django/social/models/friendship_request.py` |
| `social.SocialRecommendation` | `user` | `ForeignKey` | `User` | `backend_django/social/models/social_recommendation.py` |
| `social.SocialRecommendation` | `candidate` | `ForeignKey` | `User` | `backend_django/social/models/social_recommendation.py` |
| `social.UserBlock` | `blocker` | `ForeignKey` | `User` | `backend_django/social/models/user_block.py` |
| `social.UserBlock` | `blocked` | `ForeignKey` | `User` | `backend_django/social/models/user_block.py` |
| `social.Follow` | `follower` | `ForeignKey` | `User` | `backend_django/social/models/follow.py` |
| `social.Follow` | `following` | `ForeignKey` | `User` | `backend_django/social/models/follow.py` |
| `tasks.Task` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` | `backend_django/tasks/models/task.py` |
| `tasks.Task` | `goal` | `ForeignKey` | `goals.Goal` | `backend_django/tasks/models/task.py` |
| `tasks.Task` | `milestone` | `ForeignKey` | `goals.GoalMilestone` | `backend_django/tasks/models/task.py` |
| `tasks.Task` | `learning_goal` | `ForeignKey` | `learning.LearningGoal` | `backend_django/tasks/models/task.py` |
| `tasks.Task` | `learning_path` | `ForeignKey` | `learning.LearningPath` | `backend_django/tasks/models/task.py` |
| `tasks.Task` | `learning_topic` | `ForeignKey` | `learning.LearningTopic` | `backend_django/tasks/models/task.py` |
| `tasks.Task` | `skill` | `ForeignKey` | `learning.Skill` | `backend_django/tasks/models/task.py` |

## Interpretation rules

- Target expressions may be strings, imported classes, `settings.AUTH_USER_MODEL`, or dynamic expressions; preserve the source expression rather than guessing the resolved target.
- Reverse relations, generic relations, custom through models, abstract base fields, and relationships constructed outside model class bodies may not be represented.
- Do not treat model references as proof of a complete user workflow or API integration.