# tasks architecture

## Module structure
- Models: 2 Python files under models/.
- API: 6 Python files under api/.
- Services: 3 Python files under services/.
- Tests: 2; migrations: 3 (not run).

## Processing pattern
Where present, URL declarations bind handlers in api/views; handlers use serializers and models, with services/tasks for selected operations. Exact app-specific classes and references are listed in api.md and services-and-workflows.md. This is not assumed to be uniform.

## Source directory inventory

### api
api/urls.py
api/__init__.py
api/serializers/tasks_serializers.py
api/serializers/__init__.py
api/views/tasks_views.py
api/views/__init__.py

### models
models/task.py
models/__init__.py

### services
services/daily_generation.py
services/tasks_services.py
services/__init__.py

### tasks
admin.py
apps.py
tasks.py
__init__.py
api/urls.py
api/__init__.py
api/serializers/tasks_serializers.py
api/serializers/__init__.py
api/views/tasks_views.py
api/views/__init__.py
migrations/0001_initial.py
migrations/0002_task_milestone.py
migrations/__init__.py
models/task.py
models/__init__.py
services/daily_generation.py
services/tasks_services.py
services/__init__.py
tests/test_tasks.py
tests/__init__.py

### tests
tests/test_tasks.py
tests/__init__.py

### migrations
migrations/0001_initial.py
migrations/0002_task_milestone.py
migrations/__init__.py


Shared architecture links: [backend catalog](../../02-system-component-catalog.md), [data relationships](../../06-database-and-model-catalog.md), [security and permissions](../../07-authentication-and-permissions.md).
