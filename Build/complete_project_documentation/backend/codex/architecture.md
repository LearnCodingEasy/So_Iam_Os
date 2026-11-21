# codex architecture

## Module structure
- Models: 27 Python files under models/.
- API: 79 Python files under api/.
- Services: 13 Python files under services/.
- Tests: 7; migrations: 6 (not run).

## Processing pattern
Where present, URL declarations bind handlers in api/views; handlers use serializers and models, with services/tasks for selected operations. Exact app-specific classes and references are listed in api.md and services-and-workflows.md. This is not assumed to be uniform.

## Source directory inventory

### api
api/urls.py
api/__init__.py
api/serializers/agent_definition_serializers.py
api/serializers/api_endpoint_serializers.py
api/serializers/capability_run_serializers.py
api/serializers/change_set_serializers.py
api/serializers/feature_serializers.py
api/serializers/file_serializers.py
api/serializers/local_ai_job_serializers.py
api/serializers/project_serializers.py
api/serializers/protected_feature_serializers.py
api/serializers/protected_item_serializers.py
api/serializers/snapshot_serializers.py
api/serializers/tool_definition_serializers.py
api/serializers/workflow_step_serializers.py
api/serializers/__init__.py
api/views/agent_definition_views.py
api/views/agent_plan_views.py
api/views/agent_run_views.py
api/views/api_endpoint_views.py
api/views/apply_changes_views.py
api/views/architecture_module_analyzer_views.py
api/views/audit_views.py
api/views/automation_intent_views.py
api/views/base_views.py
api/views/build_manifest_views.py
api/views/build_workspace_views.py
api/views/capability_agents_views.py
api/views/capability_agent_execute_views.py
api/views/capability_bootstrap_views.py
api/views/capability_features_views.py
api/views/capability_health_views.py
api/views/capability_registry_mixin_views.py
api/views/capability_runs_views.py
api/views/capability_summary_views.py
api/views/capability_tools_views.py
api/views/capability_tool_execute_views.py
api/views/capability_validate_views.py
api/views/change_set_views.py
api/views/code_review_views.py
api/views/context_views.py
api/views/create_snapshot_views.py
api/views/debug_views.py
api/views/documentation_views.py
api/views/duplicate_scan_views.py
api/views/explain_feature_views.py
api/views/feature_views.py
api/views/file_content_views.py
api/views/file_views.py
api/views/graph_views.py
api/views/impact_views.py
api/views/intelligence_bootstrap_views.py
api/views/local_ai_job_views.py
api/views/local_file_open_views.py
api/views/markdown_navigation_views.py
api/views/open_ai_codex_views.py
api/views/overview_views.py
api/views/plan_change_views.py
api/views/policy_views.py
api/views/project_context_export_views.py
api/views/project_views.py
api/views/prompt_generator_views.py
api/views/protected_feature_views.py
api/views/protected_item_views.py
api/views/protected_manifest_views.py
api/views/protected_registry_views.py
api/views/rollback_views.py
api/views/safe_commands_views.py
api/views/scan_views.py
api/views/search_views.py
api/views/security_scan_views.py
api/views/selected_files_context_views.py
api/views/snapshot_views.py
api/views/test_plan_views.py
api/views/tools_views.py
api/views/tool_definition_views.py
api/views/workflow_step_views.py
api/views/workflow_views.py
api/views/__init__.py

### models
models/api_endpoint.py
models/architecture_edge.py
models/architecture_node.py
models/change_set.py
models/codex_agent_definition.py
models/codex_agent_run.py
models/codex_analysis.py
models/codex_audit_event.py
models/codex_capability_run.py
models/codex_change_file.py
models/codex_conversation.py
models/codex_execution_request.py
models/codex_feature_definition.py
models/codex_finding.py
models/codex_message.py
models/codex_policy.py
models/codex_tool.py
models/codex_tool_definition.py
models/codex_workflow_step.py
models/feature.py
models/file_registry.py
models/local_ai_job.py
models/project_registry.py
models/project_snapshot.py
models/protected_feature.py
models/protected_item.py
models/__init__.py

### services
services/build_workspace.py
services/capabilities.py
services/change_planner.py
services/context_builder.py
services/execution.py
services/extensions.py
services/intelligence.py
services/openai_service.py
services/project_context.py
services/project_scanner.py
services/snapshot_service.py
services/user_context.py
services/__init__.py

### management
management/__init__.py
management/commands/codex_bootstrap_governance.py
management/commands/codex_export_context.py
management/commands/codex_scan.py
management/commands/codex_seed_capabilities.py
management/commands/__init__.py

### tests
tests/test_build_workspace.py
tests/test_capability_registry.py
tests/test_extensions.py
tests/test_foundation.py
tests/test_user_context.py
tests/__init__.py

### migrations
migrations/0001_initial.py
migrations/0002_codexconversation_codexanalysis_codexmessage.py
migrations/0003_codex_intelligence.py
migrations/0004_codex_capability_registry.py
migrations/0005_codex_protection_workflow_localai.py
migrations/__init__.py


Shared architecture links: [backend catalog](../../02-system-component-catalog.md), [data relationships](../../06-database-and-model-catalog.md), [security and permissions](../../07-authentication-and-permissions.md).
