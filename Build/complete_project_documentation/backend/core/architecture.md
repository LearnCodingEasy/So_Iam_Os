# core architecture

## Module structure
- Models: 3 Python files under models/.
- API: 6 Python files under api/.
- Services: 2 Python files under services/.
- Tests: 4; migrations: 2 (not run).

## Processing pattern
Where present, URL declarations bind handlers in api/views; handlers use serializers and models, with services/tasks for selected operations. Exact app-specific classes and references are listed in api.md and services-and-workflows.md. This is not assumed to be uniform.

## Source directory inventory

### api
api/urls.py
api/__init__.py
api/serializers/core_serializers.py
api/serializers/__init__.py
api/views/core_views.py
api/views/__init__.py

### models
models/base_model.py
models/user_learning_settings.py
models/__init__.py

### services
services/core_services.py
services/__init__.py

### tests
tests/tests_learning_settings.py
tests/test_api_contract.py
tests/test_core.py
tests/__init__.py

### migrations
migrations/0001_initial.py
migrations/__init__.py


Shared architecture links: [backend catalog](../../02-system-component-catalog.md), [data relationships](../../06-database-and-model-catalog.md), [security and permissions](../../07-authentication-and-permissions.md).
