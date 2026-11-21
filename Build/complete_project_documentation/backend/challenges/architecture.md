# challenges architecture

## Module structure
- Models: 5 Python files under models/.
- API: 6 Python files under api/.
- Services: 0 Python files under services/.
- Tests: 2; migrations: 2 (not run).

## Processing pattern
Where present, URL declarations bind handlers in api/views; handlers use serializers and models, with services/tasks for selected operations. Exact app-specific classes and references are listed in api.md and services-and-workflows.md. This is not assumed to be uniform.

## Source directory inventory

### api
api/urls.py
api/__init__.py
api/serializers/challenges_serializers.py
api/serializers/__init__.py
api/views/challenges_views.py
api/views/__init__.py

### models
models/challenge.py
models/challenge_attempt.py
models/challenge_progress.py
models/challenge_step.py
models/__init__.py

### tests
tests/test_challenges.py
tests/__init__.py

### migrations
migrations/0001_initial.py
migrations/__init__.py


Shared architecture links: [backend catalog](../../02-system-component-catalog.md), [data relationships](../../06-database-and-model-catalog.md), [security and permissions](../../07-authentication-and-permissions.md).
