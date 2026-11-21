# ai architecture

## Module structure
- Models: 11 Python files under models/.
- API: 15 Python files under api/.
- Services: 28 Python files under services/.
- Tests: 7; migrations: 15 (not run).

## Processing pattern
Where present, URL declarations bind handlers in api/views; handlers use serializers and models, with services/tasks for selected operations. Exact app-specific classes and references are listed in api.md and services-and-workflows.md. This is not assumed to be uniform.

## Source directory inventory

### api
api/chat.py
api/diagnostics.py
api/urls.py
api/__init__.py
api/serializers/conversations.py
api/serializers/feedback.py
api/serializers/learning.py
api/serializers/observability.py
api/serializers/prompts.py
api/serializers/providers.py
api/serializers/settings.py
api/serializers/workflows.py
api/serializers/__init__.py
api/views/ai_views.py
api/views/__init__.py

### models
models/audit.py
models/budgets.py
models/conversations.py
models/executions.py
models/feedback.py
models/prompts.py
models/providers.py
models/settings.py
models/usage.py
models/workflows.py
models/__init__.py

### services
services/agent_executor.py
services/agent_selector.py
services/audit_service.py
services/budget_service.py
services/capabilities.py
services/context_inspector.py
services/context_service.py
services/conversation_service.py
services/core.py
services/credential_service.py
services/diagnostics.py
services/exceptions.py
services/execution_service.py
services/fallback_service.py
services/feedback_service.py
services/learning_actions.py
services/permissions.py
services/prompts.py
services/prompt_template_service.py
services/providers.py
services/provider_manager.py
services/provider_service.py
services/security.py
services/task_planner.py
services/tests.py
services/usage_service.py
services/workflow_service.py
services/__init__.py

### tasks
tasks/ai_tasks.py
tasks/__init__.py

### tests
tests/test_ai.py
tests/test_ai_repair_regressions.py
tests/test_credential_security.py
tests/test_production_architecture.py
tests/test_provider_adapters.py
tests/test_provider_switching_e2e.py
tests/__init__.py

### migrations
migrations/0001_initial.py
migrations/0002_aiproviderconfig.py
migrations/0003_ai_provider_choices.py
migrations/0004_ai_platform.py
migrations/0005_rename_ai_aiaudit_user_id_0a9e2c_idx_ai_aiauditl_user_id_5994b6_idx_and_more.py
migrations/0006_remove_aiauditlog_ai_aiauditl_user_id_5994b6_idx_and_more.py
migrations/0007_restore_ai_observability.py
migrations/0008_alter_aiauditlog_resource_and_more.py
migrations/0009_remove_aiauditlog_ai_aiaudit_user_created_idx_and_more.py
migrations/0010_repair_aiexecution_requested_provider.py
migrations/0011_ai_production_reliability.py
migrations/0012_rename_ai_aibudget_user_id_8b8c65_idx_ai_aibudget_user_id_40709d_idx_and_more.py
migrations/0013_remove_aiauditlog_ai_aiauditl_user_id_5994b6_idx_and_more.py
migrations/0014_aiauditlog.py
migrations/__init__.py


Shared architecture links: [backend catalog](../../02-system-component-catalog.md), [data relationships](../../06-database-and-model-catalog.md), [security and permissions](../../07-authentication-and-permissions.md).
