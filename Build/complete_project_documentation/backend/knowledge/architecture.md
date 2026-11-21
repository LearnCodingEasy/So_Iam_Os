# knowledge architecture

## Module structure
- Models: 3 Python files under models/.
- API: 8 Python files under api/.
- Services: 3 Python files under services/.
- Tests: 4; migrations: 2 (not run).

## Processing pattern
Where present, URL declarations bind handlers in api/views; handlers use serializers and models, with services/tasks for selected operations. Exact app-specific classes and references are listed in api.md and services-and-workflows.md. This is not assumed to be uniform.

## Source directory inventory

### api
api/urls.py
api/__init__.py
api/serializers/knowledge_file_serializers.py
api/serializers/knowledge_item_serializers.py
api/serializers/__init__.py
api/views/knowledge_file_views.py
api/views/knowledge_item_views.py
api/views/__init__.py

### models
models/knowledge_file.py
models/knowledge_item.py
models/__init__.py

### services
services/file_service.py
services/knowledge_service.py
services/__init__.py

### tasks
tasks/knowledge_file_tasks.py
tasks/__init__.py

### tests
tests/test_api.py
tests/test_file_validation.py
tests/test_metadata_extractor.py
tests/__init__.py

### migrations
migrations/0001_initial.py
migrations/__init__.py


Shared architecture links: [backend catalog](../../02-system-component-catalog.md), [data relationships](../../06-database-and-model-catalog.md), [security and permissions](../../07-authentication-and-permissions.md).
