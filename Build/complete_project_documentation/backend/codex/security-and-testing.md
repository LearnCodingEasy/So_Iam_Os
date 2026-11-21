# codex security and testing

## Permission/ownership evidence

- codex/api/views/agent_plan_views.py:L10: permission_classes = [CodexAuthenticated]
- codex/api/views/agent_plan_views.py:L15: 'request', ''), request.user)
- codex/api/views/agent_plan_views.py:L17: project=project, user=request.user, request=request.data.get('request', ''), plan=result)
- codex/api/views/agent_run_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/api_endpoint_views.py:L10: permission_classes = [CodexAuthenticated]
- codex/api/views/apply_changes_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/apply_changes_views.py:L14: return Response(apply_changes(request.user, project, request.data.get('title', 'Codex change'), request.data.get('objective', ''), request.data.get('changes', []), request.data.get('confirm') is True), status=201)
- codex/api/views/architecture_module_analyzer_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/audit_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/automation_intent_views.py:L10: permission_classes = [CodexAuthenticated]
- codex/api/views/automation_intent_views.py:L14: policy = ensure_policy(project, request.user)
- codex/api/views/automation_intent_views.py:L22: CodexAuditEvent.objects.create(project=project, user=request.user,
- codex/api/views/base_views.py:L6: permission_classes = [CodexAuthenticated]
- codex/api/views/build_manifest_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/build_workspace_views.py:L10: permission_classes = [CodexAuthenticated]
- codex/api/views/capability_agent_execute_views.py:L12: return Response(execute_agent(self.project(create=True), request.user, key, request.data or {}))
- codex/api/views/capability_registry_mixin_views.py:L11: permission_classes = [CodexAuthenticated]
- codex/api/views/capability_tool_execute_views.py:L12: return Response(execute_tool(self.project(create=True), request.user, key, request.data or {}))
- codex/api/views/code_review_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/code_review_views.py:L13: return Response({'path': request.data.get('path', ''), 'findings': code_review(project, request.data.get('path', ''), request.user)})
- codex/api/views/context_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/create_snapshot_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/create_snapshot_views.py:L13: user=request.user, label=request.data.get("label", "Codex snapshot"))
- codex/api/views/debug_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/debug_views.py:L13: return Response(debug_error(project, request.data.get('error', ''), request.user))
- codex/api/views/documentation_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/documentation_views.py:L13: return Response(generate_docs(project, request.data.get('target', ''), request.user))
- codex/api/views/duplicate_scan_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/duplicate_scan_views.py:L13: return Response({'duplicates': duplicate_scan(project, request.user)})
- codex/api/views/explain_feature_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/explain_feature_views.py:L13: return Response(explain_feature(project, request.data.get('query', ''), request.user))
- codex/api/views/file_views.py:L11: permission_classes = [CodexAuthenticated]
- codex/api/views/graph_views.py:L10: permission_classes = [CodexAuthenticated]
- codex/api/views/impact_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/intelligence_bootstrap_views.py:L15: permission_classes = [CodexAuthenticated]
- codex/api/views/intelligence_bootstrap_views.py:L21: ensure_policy(project, request.user)
- codex/api/views/intelligence_bootstrap_views.py:L23: findings = security_scan(project, request.user)
- codex/api/views/local_ai_job_views.py:L14: permission_classes = [CodexAuthenticated]
- codex/api/views/local_ai_job_views.py:L19: permission_classes = [CodexAuthenticated]
- codex/api/views/local_ai_job_views.py:L35: job = create_local_job(project, request.user,
- codex/api/views/local_ai_job_views.py:L41: permission_classes = [CodexAuthenticated]
- codex/api/views/local_file_open_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/markdown_navigation_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/open_ai_codex_views.py:L13: permission_classes = [CodexAuthenticated]
- codex/api/views/open_ai_codex_views.py:L65: user=request.user,
- codex/api/views/open_ai_codex_views.py:L85: user=request.user,
- codex/api/views/overview_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/plan_change_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/plan_change_views.py:L12: obj = ChangePlanner.plan(user=request.user, title=request.data.get(
- codex/api/views/policy_views.py:L10: permission_classes = [CodexAuthenticated]
- codex/api/views/policy_views.py:L14: return Response({'permissions': ensure_policy(project, request.user).permissions})
- codex/api/views/policy_views.py:L18: policy = ensure_policy(project, request.user)
- codex/api/views/policy_views.py:L23: CodexAuditEvent.objects.create(project=project, user=request.user, event_type='policy',
- codex/api/views/project_context_export_views.py:L24: # Personal data is always scoped to request.user. Raw knowledge content is opt-in.
- codex/api/views/project_context_export_views.py:L32: request.user,
- codex/api/views/project_views.py:L10: permission_classes = [CodexAuthenticated]
- codex/api/views/prompt_generator_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/protected_manifest_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/protected_registry_views.py:L15: permission_classes = [CodexAuthenticated]
- codex/api/views/protected_registry_views.py:L27: item = freeze_item(project, request.user, request.data)
- codex/api/views/rollback_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/rollback_views.py:L14: return Response(rollback_changes(request.user, project, changeset_id, request.data.get('confirm') is True))
- codex/api/views/safe_commands_views.py:L11: permission_classes = [CodexAuthenticated]
- codex/api/views/safe_commands_views.py:L15: policy = ensure_policy(project, request.user)
- codex/api/views/safe_commands_views.py:L24: result = run_safe(request.user, project, key)
- codex/api/views/safe_commands_views.py:L26: CodexAuditEvent.objects.create(project=project, user=request.user, event_type='command',
- codex/api/views/scan_views.py:L8: permission_classes = [CodexAuthenticated]
- codex/api/views/search_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/security_scan_views.py:L10: permission_classes = [CodexAuthenticated]
- codex/api/views/security_scan_views.py:L14: return Response({'findings': security_scan(project, request.user)})
- codex/api/views/selected_files_context_views.py:L10: permission_classes = [CodexAuthenticated]
- codex/api/views/snapshot_views.py:L10: permission_classes = [CodexAuthenticated]
- codex/api/views/test_plan_views.py:L9: permission_classes = [CodexAuthenticated]
- codex/api/views/test_plan_views.py:L13: return Response(test_plan(project, request.data.get('target', ''), request.user))
- codex/api/views/tools_views.py:L10: permission_classes = [CodexAuthenticated]
- codex/api/views/workflow_views.py:L9: permission_classes = [CodexAuthenticated]


## Tests
- codex/api/views/test_plan_views.py
- codex/tests/test_build_workspace.py
- codex/tests/test_capability_registry.py
- codex/tests/test_extensions.py
- codex/tests/test_foundation.py
- codex/tests/test_user_context.py
- codex/tests/__init__.py


Tests were not run. This scan is not a complete authorization/security review. Shared guidance: [authentication and permissions](../../07-authentication-and-permissions.md).
