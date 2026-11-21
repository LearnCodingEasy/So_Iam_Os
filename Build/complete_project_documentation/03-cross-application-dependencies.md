# Cross-Application Dependencies

## Source-grounded relationships
| From | To | Evidence |
|---|---|---|
| tasks.Task | Goal, GoalMilestone, LearningGoal, LearningPath, LearningTopic, Skill | backend_django/tasks/models/task.py |
| goals.Goal | LearningGoal and Skill | backend_django/goals/models/goal.py |
| learning.LearningTopic | KnowledgeItem and Skill | backend_django/learning/models/learning_topic.py |
| jobs.JobSkillRequirement | learning.Skill | backend_django/jobs_opportunity/models/job_skill_requirement.py |
| jobs.JobSkillGap | Skill and LearningGoal | backend_django/jobs_opportunity/models/job_skill_gap.py |
| projects.ProjectTask / ProjectGoal | tasks.Task / goals.Goal | backend_django/projects/models/project_task.py and project_goal.py |
| finance.SavingsGoal | goals.Goal | backend_django/personal_finance/models/savings_goal.py |
| challenges.Challenge | Skill, Project, Goal | backend_django/challenges/models/challenge.py |

~~~mermaid
flowchart TD
 User[users_accounts.User] --> Goals[goals]
 User --> Tasks[tasks]
 User --> Learning[learning]
 User --> Knowledge[knowledge]
 User --> Jobs[jobs_opportunity]
 User --> Finance[personal_finance]
 Goals --> Tasks
 Goals --> Learning
 Tasks --> Learning
 Learning --> Knowledge
 Jobs --> Learning
 Projects[projects] --> Goals
 Projects --> Tasks
 Finance --> Goals
~~~

Edges are model/service references. They do not prove transaction coordination or a complete UI workflow.

## Cross-layer dependencies
**VERIFIED:** Root Django URLs include app URL modules (backend_django/backend_django/urls.py). Vue router selects views (frontend_vue/src/router/index.js); feature services use shared HTTP and endpoint modules (frontend_vue/src/services/Shared/). Celery autodiscovers tasks (backend_django/backend_django/celery.py).

## Potential cycles and limits
**UNKNOWN:** Full import-cycle and call-graph analysis is pending. Model references cannot establish a runtime call cycle. App-level catalogs will record direct imports and discovered consumers.

