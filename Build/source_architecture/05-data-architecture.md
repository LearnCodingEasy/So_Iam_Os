# Data Architecture

## Persistence model

**VERIFIED:** Django apps define ORM models and foreign-key relationships. `backend_django/backend_django/settings.py` configures SQLite by default, PostgreSQL when selected, and a production guard requiring PostgreSQL. This describes configuration logic only; no database was opened.

## Ownership and principal relationships

| Relationship | Source evidence | Meaning supported by code |
|---|---|---|
| User → personal records | `users_accounts/models/user.py`; owner foreign keys in domain models | Many records are directly user-owned; some child records inherit access through their parent |
| Goal ↔ learning | `goals/models/goal.py` links learning goals and skills; `tasks/models/task.py` links goal/milestone and learning objects | Planning and learning concepts are relationally connected |
| Learning ↔ knowledge | `learning/models/learning_topic.py` references a knowledge item; knowledge views connect items to topics | Knowledge can be associated with learning topics |
| Job → skill | `jobs_opportunity/models/job_skill_requirement.py` links job opportunity and `learning.Skill` | Job requirements use the learning skill entity |
| Skill gap → learning | `jobs_opportunity/models/job_skill_gap.py` references skill and learning goal | A skill gap can be associated with a learning goal |
| Project → goals/tasks | `projects/models/project_goal.py`; `projects/models/project_task.py` | Project links are explicit join records |
| Finance → general goal | `personal_finance/models/savings_goal.py` optionally references `goals.Goal` | A savings goal may connect to a general goal |
| AI conversation → messages | `ai/models/conversations.py` | Messages belong to conversations; executions/usage/feedback provide related AI records |
| Automation workflow → graph/run | `automation/models/workflow.py`, `workflow_node.py`, `workflow_edge.py`, `task_run.py` | Workflow graphs and executions are represented as separate related entities |

## Domain entity groups

- Goals: Goal, GoalMilestone, GoalActivity, GoalPlanProposal (`backend_django/goals/models/`).
- Tasks: Task (`backend_django/tasks/models/task.py`).
- Learning: Skill, LearningGoal, LearningPath, LearningTopic, Lesson, progress, assessment, review, and revision entities (`backend_django/learning/models/`).
- Knowledge: KnowledgeItem and KnowledgeFile (`backend_django/knowledge/models/`).
- Jobs: JobOpportunity, JobMatch, JobApplication, JobSkillRequirement, JobSkillGap, resume/cover-letter and recommendation entities (`backend_django/jobs_opportunity/models/`).
- Finance: Transaction, Category, Budget, Debt, payment, SavingsGoal, Subscription and scenario entities (`backend_django/personal_finance/models/`).
- Codex and AI: project registry, changes, snapshots, policies, conversations, provider credentials, executions, usage, and audit entities (`backend_django/codex/models/`, `backend_django/ai/models/`).

## Ownership boundaries and unknowns

**VERIFIED:** Ownership is implemented in several endpoint patterns: user-filtered querysets, serializer validation of related owners, and create methods assigning `request.user`. Examples: `backend_django/goals/api/views/goals_views.py`, `backend_django/learning/api/views/user_owned_queryset_mixin_views.py`, and `backend_django/personal_finance/api/views/owned_views.py`.

**UNKNOWN:** A complete cross-app audit of every foreign-key write, uniqueness constraint, deletion cascade, and tenant-access path is outside this summary. Migrations were inspected only as allowed source where needed; none were executed. No schema was compared against a live database.

See [Security and Operations](./06-security-and-operations.md) for the authorization implications and [domain documents](./domains/goals-tasks-projects-and-challenges.md) for domain-level details.
