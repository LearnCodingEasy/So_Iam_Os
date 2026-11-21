# goals architecture

## Module structure
- Models: 5 Python files under models/.
- API: 6 Python files under api/.
- Services: 3 Python files under services/.
- Tests: 2; migrations: 4 (not run).

## Processing pattern
Where present, URL declarations bind handlers in api/views; handlers use serializers and models, with services/tasks for selected operations. Exact app-specific classes and references are listed in api.md and services-and-workflows.md. This is not assumed to be uniform.

## Source directory inventory

### api
api/urls.py
api/__init__.py
api/serializers/goals_serializers.py
api/serializers/__init__.py
api/views/goals_views.py
api/views/__init__.py

### models
models/goal.py
models/goal_activity.py
models/goal_milestone.py
models/goal_plan_proposal.py
models/__init__.py

### services
services/coach.py
services/goals_services.py
services/__init__.py

### tests
tests/test_goals.py
tests/__init__.py

### migrations
migrations/0001_initial.py
migrations/0002_goal_intelligence.py
migrations/0003_rename_goals_goal_user_cat_status_idx_goals_goal_user_id_500d12_idx_and_more.py
migrations/__init__.py


Shared architecture links: [backend catalog](../../02-system-component-catalog.md), [data relationships](../../06-database-and-model-catalog.md), [security and permissions](../../07-authentication-and-permissions.md).
