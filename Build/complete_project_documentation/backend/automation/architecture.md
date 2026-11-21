# automation architecture

## Module structure
- Models: 11 Python files under models/.
- API: 25 Python files under api/.
- Services: 6 Python files under services/.
- Tests: 2; migrations: 2 (not run).

## Processing pattern
Where present, URL declarations bind handlers in api/views; handlers use serializers and models, with services/tasks for selected operations. Exact app-specific classes and references are listed in api.md and services-and-workflows.md. This is not assumed to be uniform.

## Source directory inventory

### api
api/urls.py
api/__init__.py
api/serializers/action_serializers.py
api/serializers/delay_serializers.py
api/serializers/program_element_serializers.py
api/serializers/program_serializers.py
api/serializers/screen_state_serializers.py
api/serializers/task_run_serializers.py
api/serializers/task_serializers.py
api/serializers/workflow_edge_serializers.py
api/serializers/workflow_node_serializers.py
api/serializers/workflow_serializers.py
api/serializers/__init__.py
api/views/action_views.py
api/views/common.py
api/views/delay_views.py
api/views/program_element_views.py
api/views/program_views.py
api/views/screen_state_views.py
api/views/task_run_views.py
api/views/task_views.py
api/views/workflow_edge_views.py
api/views/workflow_node_views.py
api/views/workflow_views.py
api/views/__init__.py

### models
models/action.py
models/delay.py
models/program.py
models/program_element.py
models/screen_state.py
models/task.py
models/task_run.py
models/workflow.py
models/workflow_edge.py
models/workflow_node.py
models/__init__.py

### services
services/automation.py
services/macos_scanner.py
services/program_service.py
services/scanner_service.py
services/screenshot.py
services/window_service.py

### tests
tests/test_automation.py
tests/__init__.py

### migrations
migrations/0001_initial.py
migrations/__init__.py


Shared architecture links: [backend catalog](../../02-system-component-catalog.md), [data relationships](../../06-database-and-model-catalog.md), [security and permissions](../../07-authentication-and-permissions.md).
