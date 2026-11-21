# Database and Model Catalog — Initial Index

## Configuration
**VERIFIED:** backend_django/backend_django/settings.py defaults to SQLite and supports PostgreSQL when DATABASE_ENGINE selects it; a production guard requires PostgreSQL. It configures media root and Redis cache defaults. No database was opened.

## Model families
| Family | Source |
|---|---|
| User | backend_django/users_accounts/models/ |
| Goals/milestones/activity/proposals | backend_django/goals/models/ |
| Tasks | backend_django/tasks/models/ |
| Learning paths/topics/progress/assessment/review | backend_django/learning/models/ |
| Knowledge items/files | backend_django/knowledge/models/ |
| Projects and goal/task links | backend_django/projects/models/ |
| Opportunities/matches/applications | backend_django/jobs_opportunity/models/ |
| Finance ledger/debts/savings/scenarios | backend_django/personal_finance/models/ |
| AI provider/conversation/execution/budget | backend_django/ai/models/ |
| Codex registry/change/snapshot/policy/audit | backend_django/codex/models/ |
| Automation graph/task-run/screen | backend_django/automation/models/ |
| Other installed apps | challenges, core, memory, notification, scraper, social model directories |

Cross-application edges are cataloged in 03-cross-application-dependencies.md. Every model, field, relation, constraint, index, method, and ownership rule still needs per-app models.md documentation.

## Coverage status
**PARTIAL:** This is an index, not a field-level schema reference. **UNKNOWN:** live schema, applied migrations, and stored data integrity.

