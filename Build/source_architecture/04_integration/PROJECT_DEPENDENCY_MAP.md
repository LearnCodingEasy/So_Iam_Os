# Project Dependency and Integration Map

> Distinguishes three evidence types: (1) root URL inclusion, (2) model relation declarations, and (3) frontend routes. These edges are not interchangeable and do not prove runtime workflows.

## Backend application URL inclusion

| Backend app | Root API prefix |
|---|---|
| `agents` | `/api/agents/` |
| `ai` | `/api/ai/` |
| `ai_tools_laboratory` | `/api/ai-tools/` |
| `allauth` | `/accounts/` |
| `analytics` | `/api/analytics/` |
| `architecture` | `/api/architecture/` |
| `automation` | `/api/automation/` |
| `challenges` | `/api/challenges/` |
| `codex` | `/api/codex/` |
| `core` | `/api/core/` |
| `crm` | `/api/crm/` |
| `goals` | `/api/goals/` |
| `jobs_opportunity` | `/api/jobs/` |
| `knowledge` | `/api/knowledge/` |
| `learning` | `/api/learning/` |
| `marketing` | `/api/marketing/` |
| `memory` | `/api/memory/` |
| `notification` | `/api/notifications/` |
| `personal_finance` | `/api/finance/` |
| `projects` | `/api/projects/` |
| `revenue` | `/api/revenue/` |
| `sales` | `/api/sales/` |
| `scraper` | `/api/scraper/` |
| `social` | `/api/social/` |
| `tasks` | `/api/tasks/` |
| `users_accounts` | `/api/users/` |

## Model-level cross-application relations

| From | Relation field | Relation type | Target expression |
|---|---|---|---|
| `agents.AgentConfiguration` | `agent` | `ForeignKey` | `agents.Agent` |
| `agents.AgentRun` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `agents.AgentRun` | `agent` | `ForeignKey` | `agents.Agent` |
| `agents.AgentRun` | `configuration` | `ForeignKey` | `agents.AgentConfiguration` |
| `agents.Agent` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `agents.AgentExecution` | `run` | `ForeignKey` | `agents.AgentRun` |
| `ai.AIConversation` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `ai.AIMessage` | `conversation` | `ForeignKey` | `AIConversation` |
| `ai.AISettings` | `user` | `OneToOneField` | `settings.AUTH_USER_MODEL` |
| `ai.AISettings` | `default_prompt_profile` | `ForeignKey` | `ai.AIPromptProfile` |
| `ai.AIPromptProfile` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `ai.AIUsageRecord` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `ai.AIUsageRecord` | `execution` | `OneToOneField` | `ai.AIExecution` |
| `ai.AIProviderCredential` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `ai.AIProviderConfig` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `ai.AIExecution` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `ai.AIExecution` | `conversation` | `ForeignKey` | `AIConversation` |
| `ai.AIFeedback` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `ai.AIFeedback` | `message` | `ForeignKey` | `ai.AIMessage` |
| `ai.AIWorkflowDefinition` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `ai.AIWorkflowRun` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `ai.AIWorkflowRun` | `workflow` | `ForeignKey` | `ai.AIWorkflowDefinition` |
| `ai.AIWorkflowRun` | `execution` | `ForeignKey` | `ai.AIExecution` |
| `ai.AIBudgetPolicy` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `ai.AIBudgetReservation` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `ai.AIBudgetReservation` | `policy` | `ForeignKey` | `AIBudgetPolicy` |
| `ai.AiAuditLog` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `ai_tools_laboratory.Tool` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `ai_tools_laboratory.Tool` | `category` | `ForeignKey` | `ai_tools_laboratory.ToolCategory` |
| `ai_tools_laboratory.ToolExecution` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `ai_tools_laboratory.ToolExecution` | `tool` | `ForeignKey` | `ai_tools_laboratory.Tool` |
| `ai_tools_laboratory.ToolExecution` | `configuration` | `ForeignKey` | `ai_tools_laboratory.ToolConfiguration` |
| `ai_tools_laboratory.ToolConfiguration` | `tool` | `ForeignKey` | `ai_tools_laboratory.Tool` |
| `ai_tools_laboratory.ToolCategory` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `analytics.Report` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `analytics.Metric` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `analytics.AnalyticsEvent` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `analytics.MetricSnapshot` | `metric` | `ForeignKey` | `analytics.Metric` |
| `architecture.Dependency` | `source` | `ForeignKey` | `architecture.Component` |
| `architecture.Dependency` | `target` | `ForeignKey` | `architecture.Component` |
| `architecture.Component` | `architecture` | `ForeignKey` | `architecture.Architecture` |
| `architecture.ArchitectureDecision` | `architecture` | `ForeignKey` | `architecture.Architecture` |
| `architecture.ArchitectureDecision` | `superseded_by` | `ForeignKey` | `architecture.ArchitectureDecision` |
| `architecture.Architecture` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `automation.Task` | `created_by` | `ForeignKey` | `User` |
| `automation.Task` | `program` | `ForeignKey` | `Program` |
| `automation.TaskRun` | `created_by` | `ForeignKey` | `User` |
| `automation.TaskRun` | `workflow` | `ForeignKey` | `Workflow` |
| `automation.Workflow` | `created_by` | `ForeignKey` | `User` |
| `automation.Action` | `created_by` | `ForeignKey` | `User` |
| `automation.Action` | `node` | `ForeignKey` | `WorkflowNode` |
| `automation.Program` | `created_by` | `ForeignKey` | `User` |
| `automation.WorkflowNode` | `created_by` | `ForeignKey` | `User` |
| `automation.WorkflowNode` | `workflow` | `ForeignKey` | `Workflow` |
| `automation.WorkflowNode` | `program` | `ForeignKey` | `Program` |
| `automation.WorkflowNode` | `element` | `ForeignKey` | `ProgramElement` |
| `automation.WorkflowEdge` | `created_by` | `ForeignKey` | `User` |
| `automation.WorkflowEdge` | `workflow` | `ForeignKey` | `Workflow` |
| `automation.WorkflowEdge` | `source_node` | `ForeignKey` | `WorkflowNode` |
| `automation.WorkflowEdge` | `target_node` | `ForeignKey` | `WorkflowNode` |
| `automation.ScreenState` | `created_by` | `ForeignKey` | `User` |
| `automation.ScreenState` | `task_run` | `ForeignKey` | `TaskRun` |
| `automation.ProgramElement` | `created_by` | `ForeignKey` | `User` |
| `automation.ProgramElement` | `program` | `ForeignKey` | `Program` |
| `automation.ProgramElement` | `parent_element` | `ForeignKey` | `self` |
| `automation.Delay` | `created_by` | `ForeignKey` | `User` |
| `challenges.ChallengeAttempt` | `challenge` | `ForeignKey` | `Challenge` |
| `challenges.ChallengeAttempt` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `challenges.ChallengeProgress` | `challenge` | `ForeignKey` | `Challenge` |
| `challenges.ChallengeProgress` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `challenges.Challenge` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `challenges.Challenge` | `skill` | `ForeignKey` | `learning.Skill` |
| `challenges.Challenge` | `project` | `ForeignKey` | `projects.Project` |
| `challenges.Challenge` | `goal` | `ForeignKey` | `goals.Goal` |
| `challenges.ChallengeStep` | `challenge` | `ForeignKey` | `Challenge` |
| `codex.ArchitectureEdge` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.ArchitectureEdge` | `source` | `ForeignKey` | `ArchitectureNode` |
| `codex.ArchitectureEdge` | `target` | `ForeignKey` | `ArchitectureNode` |
| `codex.CodexAgentDefinition` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.LocalAIJob` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.LocalAIJob` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `codex.CodexFinding` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.CodexExecutionRequest` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.CodexExecutionRequest` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `codex.CodexWorkflowStep` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.CodexConversation` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.CodexConversation` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `codex.ChangeSet` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.ChangeSet` | `created_by` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `codex.APIEndpoint` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.CodexPolicy` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.CodexPolicy` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `codex.FileRegistry` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.CodexMessage` | `conversation` | `ForeignKey` | `CodexConversation` |
| `codex.CodexChangeFile` | `changeset` | `ForeignKey` | `ChangeSet` |
| `codex.ProtectedFeature` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.ProtectedFeature` | `feature` | `ForeignKey` | `Feature` |
| `codex.CodexAgentRun` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.CodexAgentRun` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `codex.ProtectedItem` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.ProtectedItem` | `approved_by` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `codex.Feature` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.CodexCapabilityRun` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.CodexCapabilityRun` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `codex.CodexAnalysis` | `conversation` | `ForeignKey` | `CodexConversation` |
| `codex.CodexAuditEvent` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.CodexAuditEvent` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `codex.CodexFeatureDefinition` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.ArchitectureNode` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.ProjectSnapshot` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.ProjectSnapshot` | `created_by` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `codex.CodexTool` | `project` | `ForeignKey` | `ProjectRegistry` |
| `codex.CodexToolDefinition` | `project` | `ForeignKey` | `ProjectRegistry` |
| `core.UserLearningSettings` | `user` | `OneToOneField` | `settings.AUTH_USER_MODEL` |
| `core.UserLearningSettings` | `current_learning_goal` | `ForeignKey` | `learning.LearningGoal` |
| `crm.Interaction` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `crm.Interaction` | `contact` | `ForeignKey` | `crm.Contact` |
| `crm.CustomerRelationship` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `crm.CustomerRelationship` | `contact` | `OneToOneField` | `crm.Contact` |
| `crm.Company` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `crm.Contact` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `crm.Contact` | `company` | `ForeignKey` | `crm.Company` |
| `goals.Goal` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `goals.Goal` | `learning_goals` | `ManyToManyField` | `learning.LearningGoal` |
| `goals.Goal` | `skills` | `ManyToManyField` | `learning.Skill` |
| `goals.Goal` | `related_goals` | `ManyToManyField` | `self` |
| `goals.GoalMilestone` | `goal` | `ForeignKey` | `Goal` |
| `goals.GoalMilestone` | `depends_on` | `ManyToManyField` | `self` |
| `goals.GoalActivity` | `goal` | `ForeignKey` | `Goal` |
| `goals.GoalActivity` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `goals.GoalPlanProposal` | `goal` | `ForeignKey` | `Goal` |
| `goals.GoalPlanProposal` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.JobMatch` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.JobMatch` | `job` | `ForeignKey` | `JobOpportunity` |
| `jobs_opportunity.JobSkillRequirement` | `job` | `ForeignKey` | `JobOpportunity` |
| `jobs_opportunity.JobSkillRequirement` | `skill` | `ForeignKey` | `learning.Skill` |
| `jobs_opportunity.JobResume` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.CompanyProfile` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.JobReadiness` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.JobReadiness` | `job` | `ForeignKey` | `JobOpportunity` |
| `jobs_opportunity.JobApplicationEvent` | `application` | `ForeignKey` | `JobApplication` |
| `jobs_opportunity.JobAnalyticsSnapshot` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.JobCoverLetter` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.JobCoverLetter` | `job` | `ForeignKey` | `JobOpportunity` |
| `jobs_opportunity.JobCoverLetter` | `resume` | `ForeignKey` | `JobResume` |
| `jobs_opportunity.JobAlert` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.JobSavedSearch` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.JobSkillGap` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.JobSkillGap` | `job` | `ForeignKey` | `JobOpportunity` |
| `jobs_opportunity.JobSkillGap` | `skill` | `ForeignKey` | `learning.Skill` |
| `jobs_opportunity.JobSkillGap` | `learning_goal` | `ForeignKey` | `learning.LearningGoal` |
| `jobs_opportunity.JobApplication` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.JobApplication` | `job` | `ForeignKey` | `JobOpportunity` |
| `jobs_opportunity.JobApplication` | `resume` | `ForeignKey` | `JobResume` |
| `jobs_opportunity.JobApplication` | `cover_letter` | `ForeignKey` | `JobCoverLetter` |
| `jobs_opportunity.JobRecommendation` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.JobRecommendation` | `job` | `ForeignKey` | `JobOpportunity` |
| `jobs_opportunity.JobSource` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.JobOpportunity` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.JobOpportunity` | `source` | `ForeignKey` | `JobSource` |
| `jobs_opportunity.JobOpportunity` | `company_profile` | `ForeignKey` | `CompanyProfile` |
| `jobs_opportunity.JobOpportunity` | `required_skills` | `ManyToManyField` | `learning.Skill` |
| `jobs_opportunity.JobSourceSyncRun` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.JobSourceSyncRun` | `source` | `ForeignKey` | `JobSource` |
| `jobs_opportunity.JobPreference` | `user` | `OneToOneField` | `settings.AUTH_USER_MODEL` |
| `jobs_opportunity.JobInterview` | `application` | `ForeignKey` | `JobApplication` |
| `knowledge.KnowledgeFile` | `knowledge` | `ForeignKey` | `KnowledgeItem` |
| `knowledge.KnowledgeItem` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `learning.AssessmentChoice` | `question` | `ForeignKey` | `AssessmentQuestion` |
| `learning.LearningProgress` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `learning.LearningProgress` | `topic` | `ForeignKey` | `LearningTopic` |
| `learning.LearningNote` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `learning.LearningNote` | `topic` | `ForeignKey` | `LearningTopic` |
| `learning.LearningNote` | `lesson` | `ForeignKey` | `Lesson` |
| `learning.LearningNote` | `knowledge_item` | `ForeignKey` | `knowledge.KnowledgeItem` |
| `learning.ApplicationSubmission` | `application` | `ForeignKey` | `KnowledgeApplication` |
| `learning.LearningSession` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `learning.LearningSession` | `topic` | `ForeignKey` | `LearningTopic` |
| `learning.LearningSession` | `lesson` | `ForeignKey` | `Lesson` |
| `learning.KnowledgeApplication` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `learning.KnowledgeApplication` | `topic` | `ForeignKey` | `LearningTopic` |
| `learning.KnowledgeApplication` | `lesson` | `ForeignKey` | `Lesson` |
| `learning.KnowledgeApplication` | `knowledge_item` | `ForeignKey` | `knowledge.KnowledgeItem` |
| `learning.AssessmentAttempt` | `assessment` | `ForeignKey` | `Assessment` |
| `learning.AssessmentAttempt` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `learning.AssessmentQuestion` | `assessment` | `ForeignKey` | `Assessment` |
| `learning.LearningPath` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `learning.LearningPath` | `goal` | `ForeignKey` | `LearningGoal` |
| `learning.Assessment` | `topic` | `ForeignKey` | `LearningTopic` |
| `learning.LearningTopic` | `path` | `ForeignKey` | `LearningPath` |
| `learning.LearningTopic` | `skill` | `ForeignKey` | `Skill` |
| `learning.LearningTopic` | `prerequisites` | `ManyToManyField` | `self` |
| `learning.LearningTopic` | `knowledge_item` | `ForeignKey` | `knowledge.KnowledgeItem` |
| `learning.ApplicationReview` | `submission` | `ForeignKey` | `ApplicationSubmission` |
| `learning.ApplicationReview` | `application` | `ForeignKey` | `KnowledgeApplication` |
| `learning.LearningGoal` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `learning.LearningGoal` | `skill` | `ForeignKey` | `Skill` |
| `learning.LearningResource` | `topic` | `ForeignKey` | `LearningTopic` |
| `learning.LearningResource` | `lesson` | `ForeignKey` | `Lesson` |
| `learning.AssessmentResponse` | `attempt` | `ForeignKey` | `AssessmentAttempt` |
| `learning.AssessmentResponse` | `question` | `ForeignKey` | `AssessmentQuestion` |
| `learning.AssessmentResponse` | `selected_choices` | `ManyToManyField` | `AssessmentChoice` |
| `learning.LearningRevision` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `learning.LearningRevision` | `topic` | `ForeignKey` | `LearningTopic` |
| `learning.LearningRevision` | `source_review` | `ForeignKey` | `ApplicationReview` |
| `learning.Lesson` | `topic` | `ForeignKey` | `LearningTopic` |
| `marketing.MarketingContent` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `marketing.MarketingContent` | `campaign` | `ForeignKey` | `marketing.Campaign` |
| `marketing.Campaign` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `marketing.Campaign` | `channel` | `ForeignKey` | `marketing.MarketingChannel` |
| `marketing.LeadSource` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `marketing.LeadSource` | `channel` | `ForeignKey` | `marketing.MarketingChannel` |
| `marketing.LeadSource` | `campaign` | `ForeignKey` | `marketing.Campaign` |
| `marketing.LeadSource` | `contacts` | `ManyToManyField` | `crm.Contact` |
| `marketing.MarketingChannel` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `memory.MemoryItem` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `notification.Notification` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `notification.Notification` | `content_type` | `ForeignKey` | `ContentType` |
| `notification.Notification` | `content_object` | `GenericForeignKey` | `content_type` |
| `personal_finance.FinancialProfile` | `user` | `OneToOneField` | `settings.AUTH_USER_MODEL` |
| `personal_finance.Budget` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `personal_finance.Budget` | `category` | `ForeignKey` | `Category` |
| `personal_finance.Debt` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `personal_finance.Category` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `personal_finance.FinancialScenario` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `personal_finance.Transaction` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `personal_finance.Transaction` | `category` | `ForeignKey` | `Category` |
| `personal_finance.LoanPayment` | `loan` | `ForeignKey` | `LendingBorrowing` |
| `personal_finance.LoanPayment` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `personal_finance.RecurringCashflow` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `personal_finance.DebtPayment` | `debt` | `ForeignKey` | `Debt` |
| `personal_finance.DebtPayment` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `personal_finance.DebtPayment` | `transaction` | `OneToOneField` | `Transaction` |
| `personal_finance.FinancialHabit` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `personal_finance.FinancialAlert` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `personal_finance.SavingsGoal` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `personal_finance.SavingsGoal` | `general_goal` | `ForeignKey` | `goals.Goal` |
| `personal_finance.Subscription` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `personal_finance.SavingPlan` | `goal` | `OneToOneField` | `SavingsGoal` |
| `personal_finance.SavingPlan` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `personal_finance.LendingBorrowing` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `projects.ProjectMember` | `project` | `ForeignKey` | `Project` |
| `projects.ProjectMember` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `projects.ProjectGoal` | `project` | `ForeignKey` | `Project` |
| `projects.ProjectGoal` | `goal` | `ForeignKey` | `goals.Goal` |
| `projects.Project` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `projects.ProjectContext` | `project` | `OneToOneField` | `Project` |
| `projects.ProjectTask` | `project` | `ForeignKey` | `Project` |
| `projects.ProjectTask` | `task` | `ForeignKey` | `tasks.Task` |
| `revenue.RevenueSource` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `revenue.RevenueStream` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `revenue.RevenueStream` | `source` | `ForeignKey` | `revenue.RevenueSource` |
| `revenue.RevenueRecord` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `revenue.RevenueRecord` | `stream` | `ForeignKey` | `revenue.RevenueStream` |
| `revenue.RevenueRecord` | `sale` | `ForeignKey` | `sales.Sale` |
| `revenue.RecurringRevenue` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `revenue.RecurringRevenue` | `stream` | `ForeignKey` | `revenue.RevenueStream` |
| `sales.SalesActivity` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `sales.SalesActivity` | `deal` | `ForeignKey` | `sales.Deal` |
| `sales.Offer` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `sales.Offer` | `project` | `ForeignKey` | `projects.Project` |
| `sales.Sale` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `sales.Sale` | `deal` | `ForeignKey` | `sales.Deal` |
| `sales.Sale` | `offer` | `ForeignKey` | `sales.Offer` |
| `sales.Sale` | `contact` | `ForeignKey` | `crm.Contact` |
| `sales.Deal` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `sales.Deal` | `contact` | `ForeignKey` | `crm.Contact` |
| `sales.Deal` | `offer` | `ForeignKey` | `sales.Offer` |
| `scraper.ScrapingJob` | `website` | `ForeignKey` | `Website` |
| `scraper.ScrapingConfig` | `parent` | `ForeignKey` | `ParentSelector` |
| `scraper.ScrapedData` | `job` | `ForeignKey` | `ScrapingJob` |
| `scraper.ParentSelector` | `website` | `ForeignKey` | `Website` |
| `scraper.Website` | `created_by` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `social.Friendship` | `user1` | `ForeignKey` | `User` |
| `social.Friendship` | `user2` | `ForeignKey` | `User` |
| `social.SocialProfile` | `user` | `OneToOneField` | `User` |
| `social.FriendshipRequest` | `sender` | `ForeignKey` | `User` |
| `social.FriendshipRequest` | `receiver` | `ForeignKey` | `User` |
| `social.SocialRecommendation` | `user` | `ForeignKey` | `User` |
| `social.SocialRecommendation` | `candidate` | `ForeignKey` | `User` |
| `social.UserBlock` | `blocker` | `ForeignKey` | `User` |
| `social.UserBlock` | `blocked` | `ForeignKey` | `User` |
| `social.Follow` | `follower` | `ForeignKey` | `User` |
| `social.Follow` | `following` | `ForeignKey` | `User` |
| `tasks.Task` | `user` | `ForeignKey` | `settings.AUTH_USER_MODEL` |
| `tasks.Task` | `goal` | `ForeignKey` | `goals.Goal` |
| `tasks.Task` | `milestone` | `ForeignKey` | `goals.GoalMilestone` |
| `tasks.Task` | `learning_goal` | `ForeignKey` | `learning.LearningGoal` |
| `tasks.Task` | `learning_path` | `ForeignKey` | `learning.LearningPath` |
| `tasks.Task` | `learning_topic` | `ForeignKey` | `learning.LearningTopic` |
| `tasks.Task` | `skill` | `ForeignKey` | `learning.Skill` |

## Relationship interpretation

- A relation declared in a model is a persistence-level coupling. It may affect migrations, serializers, deletion behavior, query performance, permissions, and tests.
- An import or service call is a code-level dependency; it must be traced separately from ORM relations.
- A frontend API service calling an endpoint is an integration edge; this catalogue does not yet claim every endpoint has a corresponding UI consumer.
- Async task/event dependencies must be traced from task enqueue sites through Celery configuration and task implementation.

## High-value cross-domain areas to validate

| Domain group | Source-backed reason to trace | Verification needed |
|---|---|---|
| Goals / Tasks / Projects / Challenges | Existing model and documentation evidence describes cross-references among planning entities | Resolve every FK target, serializer, permissions, deletion policy, and UI flow |
| Learning / Knowledge / Skills | Learning models and skill references are documented; learning topics reference knowledge and skills in existing source evidence | Trace CRUD/API/UI and learning progress side effects |
| Jobs / Learning / Skills | Job skill requirements/gaps reference learning skill entities in existing source evidence | Verify job ingestion, skill matching, and gap-to-learning workflow |
| Finance / Goals | Savings-goal association is documented | Verify financial calculations, user ownership, and goal synchronization |
| AI / Codex / Agents / Automation | Multiple routed/backend domains exist | Trace credential handling, execution boundaries, task queues, audit logs, and permission checks |

## Known integration gaps retained from prior static audits

- Complete operation-level request/response/error/permission contracts are not yet exhaustive.
- Frontend service-to-backend operation mapping is representative, not exhaustive.
- Model field/constraint/index/ownership coverage is not exhaustive.
- Runtime and background task behavior have not been verified.