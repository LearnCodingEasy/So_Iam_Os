# codex API

Project prefix: /api/codex/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: codex/api/urls.py

- L6: router.register('projects', ProjectViewSet, basename='codex-project')

- L7: router.register('features', FeatureViewSet, basename='codex-feature')

- L8: router.register('files', FileViewSet, basename='codex-file')

- L9: router.register('apis', APIEndpointViewSet, basename='codex-api')

- L10: router.register('protected', ProtectedFeatureViewSet, basename='codex-protected')

- L11: router.register('changes', ChangeSetViewSet, basename='codex-change')

- L12: router.register('snapshots', SnapshotViewSet, basename='codex-snapshot')

- L13: router.register('feature-definitions', FeatureDefinitionViewSet, basename='codex-feature-definition')

- L14: router.register('tool-definitions', ToolDefinitionViewSet, basename='codex-tool-definition')

- L15: router.register('agent-definitions', AgentDefinitionViewSet, basename='codex-agent-definition')

- L16: router.register('protected-items', ProtectedItemViewSet, basename='codex-protected-item')

- L17: router.register('workflow-steps', WorkflowStepViewSet, basename='codex-workflow-step')

- L18: router.register('local-ai-job-records', LocalAIJobViewSet, basename='codex-local-ai-job-record')

- L22: path('build/workspace/', BuildWorkspaceView.as_view()),

- L23: path('build/manifest/', BuildManifestView.as_view()),

- L24: path('overview/', OverviewView.as_view()),

- L25: path('ai/', OpenAICodexView.as_view()),

- L26: path('scan/', ScanView.as_view()),

- L27: path('context/', ContextView.as_view()),

- L28: path('changes/plan/', PlanChangeView.as_view()),

- L29: path('snapshots/create/', CreateSnapshotView.as_view()),

- L30: path('intelligence/bootstrap/', IntelligenceBootstrapView.as_view()),

- L31: path('intelligence/search/', SearchView.as_view()),

- L32: path('intelligence/graph/', GraphView.as_view()),

- L33: path('intelligence/impact/', ImpactView.as_view()),

- L34: path('intelligence/security/', SecurityScanView.as_view()),

- L35: path('intelligence/duplicates/', DuplicateScanView.as_view()),

- L36: path('intelligence/review/', CodeReviewView.as_view()),

- L37: path('intelligence/test-plan/', TestPlanView.as_view()),

- L38: path('agent/plan/', AgentPlanView.as_view()),

- L39: path('agent/runs/', AgentRunView.as_view()),

- L40: path('policy/', PolicyView.as_view()),

- L41: path('tools/', ToolsView.as_view()),

- L42: path('audit/', AuditView.as_view()),

- L43: path('commands/', SafeCommandsView.as_view()),

- L44: path('automation/intent/', AutomationIntentView.as_view()),

- L45: path('changes/apply/', ApplyChangesView.as_view()),

- L46: path('changes/<int:changeset_id>/rollback/', RollbackView.as_view()),

- L47: path('intelligence/explain/', ExplainFeatureView.as_view()),

- L48: path('intelligence/debug/', DebugView.as_view()),

- L49: path('intelligence/docs/', DocumentationView.as_view()),

- L50: path('registry/features/', CapabilityFeaturesView.as_view()),

- L51: path('registry/tools/', CapabilityToolsView.as_view()),

- L52: path('registry/agents/', CapabilityAgentsView.as_view()),

- L53: path('registry/summary/', CapabilitySummaryView.as_view()),

- L54: path('registry/health/', CapabilityHealthView.as_view()),

- L55: path('registry/bootstrap/', CapabilityBootstrapView.as_view()),

- L56: path('registry/validate/', CapabilityValidateView.as_view()),

- L57: path('registry/runs/', CapabilityRunsView.as_view()),

- L58: path('registry/tools/<str:key>/execute/', CapabilityToolExecuteView.as_view()),

- L59: path('registry/agents/<str:key>/execute/', CapabilityAgentExecuteView.as_view()),

- L60: path('context/export/', ProjectContextExportView.as_view()),

- L61: path('files/<int:file_id>/content/', FileContentView.as_view()),

- L62: path('governance/protected-items/', ProtectedRegistryView.as_view()),

- L63: path('governance/manifest/', ProtectedManifestView.as_view()),

- L64: path('workflow/', WorkflowView.as_view()),

- L65: path('local-ai/jobs/', LocalAIJobsView.as_view()),

- L66: path('local-ai/jobs/<int:job_id>/', LocalAIJobDetailView.as_view()),

- L67: path('prompts/generate/', PromptGeneratorView.as_view()),

- L68: path('markdown/navigation/', MarkdownNavigationView.as_view()),

- L69: path('files/open-local/', LocalFileOpenView.as_view()),

- L70: path('architecture/analyze/', ArchitectureModuleAnalyzerView.as_view()),

- L71: path('files/context/', SelectedFilesContextView.as_view()),

- L72: path('', include(router.urls)),

## Handler declarations: codex/api/views/agent_definition_views.py
L7: class AgentDefinitionViewSet(BaseViewSet):
L9: serializer_class = AgentDefinitionSerializer

## Handler declarations: codex/api/views/agent_plan_views.py
L9: class AgentPlanView(APIView):
L10: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/agent_run_views.py
L8: class AgentRunView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/api_endpoint_views.py
L7: class APIEndpointViewSet(ReadOnlyModelViewSet):
L9: serializer_class = APIEndpointSerializer
L10: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/apply_changes_views.py
L8: class ApplyChangesView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/architecture_module_analyzer_views.py
L8: class ArchitectureModuleAnalyzerView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/audit_views.py
L8: class AuditView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/automation_intent_views.py
L9: class AutomationIntentView(APIView):
L10: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/base_views.py
L5: class BaseViewSet(ModelViewSet):
L6: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/build_manifest_views.py
L7: class BuildManifestView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/build_workspace_views.py
L8: class BuildWorkspaceView(APIView):
L10: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/capability_agents_views.py
L9: class CapabilityAgentsView(CapabilityRegistryMixin, APIView):

## Handler declarations: codex/api/views/capability_agent_execute_views.py
L9: class CapabilityAgentExecuteView(CapabilityRegistryMixin, APIView):

## Handler declarations: codex/api/views/capability_bootstrap_views.py
L7: class CapabilityBootstrapView(CapabilityRegistryMixin, APIView):

## Handler declarations: codex/api/views/capability_features_views.py
L9: class CapabilityFeaturesView(CapabilityRegistryMixin, APIView):

## Handler declarations: codex/api/views/capability_health_views.py
L7: class CapabilityHealthView(CapabilityRegistryMixin, APIView):

## Handler declarations: codex/api/views/capability_registry_mixin_views.py
L10: class CapabilityRegistryMixin:
L11: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/capability_runs_views.py
L7: class CapabilityRunsView(CapabilityRegistryMixin, APIView):

## Handler declarations: codex/api/views/capability_summary_views.py
L7: class CapabilitySummaryView(CapabilityRegistryMixin, APIView):

## Handler declarations: codex/api/views/capability_tools_views.py
L9: class CapabilityToolsView(CapabilityRegistryMixin, APIView):

## Handler declarations: codex/api/views/capability_tool_execute_views.py
L9: class CapabilityToolExecuteView(CapabilityRegistryMixin, APIView):

## Handler declarations: codex/api/views/capability_validate_views.py
L8: class CapabilityValidateView(CapabilityRegistryMixin, APIView):

## Handler declarations: codex/api/views/change_set_views.py
L6: class ChangeSetViewSet(BaseViewSet):
L8: serializer_class = ChangeSetSerializer

## Handler declarations: codex/api/views/code_review_views.py
L8: class CodeReviewView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/context_views.py
L8: class ContextView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/create_snapshot_views.py
L8: class CreateSnapshotView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/debug_views.py
L8: class DebugView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/documentation_views.py
L8: class DocumentationView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/duplicate_scan_views.py
L8: class DuplicateScanView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/explain_feature_views.py
L8: class ExplainFeatureView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/feature_views.py
L7: class FeatureDefinitionViewSet(BaseViewSet):
L9: serializer_class = FeatureDefinitionSerializer
L13: class FeatureViewSet(BaseViewSet):
L15: serializer_class = FeatureSerializer

## Handler declarations: codex/api/views/file_content_views.py
L10: class FileContentView(CapabilityRegistryMixin, APIView):

## Handler declarations: codex/api/views/file_views.py
L8: class FileViewSet(ReadOnlyModelViewSet):
L10: serializer_class = FileSerializer
L11: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/graph_views.py
L9: class GraphView(APIView):
L10: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/impact_views.py
L8: class ImpactView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/intelligence_bootstrap_views.py
L14: class IntelligenceBootstrapView(APIView):
L15: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/local_ai_job_views.py
L11: class LocalAIJobViewSet(ReadOnlyModelViewSet):
L13: serializer_class = LocalAIJobSerializer
L14: permission_classes = [CodexAuthenticated]
L18: class LocalAIJobsView(APIView):
L19: permission_classes = [CodexAuthenticated]
L40: class LocalAIJobDetailView(APIView):
L41: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/local_file_open_views.py
L8: class LocalFileOpenView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/markdown_navigation_views.py
L8: class MarkdownNavigationView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/open_ai_codex_views.py
L12: class OpenAICodexView(APIView):
L13: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/overview_views.py
L8: class OverviewView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/plan_change_views.py
L8: class PlanChangeView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/policy_views.py
L9: class PolicyView(APIView):
L10: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/project_context_export_views.py
L10: class ProjectContextExportView(CapabilityRegistryMixin, APIView):

## Handler declarations: codex/api/views/project_views.py
L7: class ProjectViewSet(ReadOnlyModelViewSet):
L9: serializer_class = ProjectSerializer
L10: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/prompt_generator_views.py
L8: class PromptGeneratorView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/protected_feature_views.py
L6: class ProtectedFeatureViewSet(BaseViewSet):
L8: serializer_class = ProtectedFeatureSerializer

## Handler declarations: codex/api/views/protected_item_views.py
L7: class ProtectedItemViewSet(BaseViewSet):
L9: serializer_class = ProtectedItemSerializer
L12: def perform_update(self, serializer):
L19: def perform_destroy(self, instance):

## Handler declarations: codex/api/views/protected_manifest_views.py
L8: class ProtectedManifestView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/protected_registry_views.py
L14: class ProtectedRegistryView(APIView):
L15: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/rollback_views.py
L8: class RollbackView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/safe_commands_views.py
L10: class SafeCommandsView(APIView):
L11: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/scan_views.py
L7: class ScanView(APIView):
L8: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/search_views.py
L8: class SearchView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/security_scan_views.py
L9: class SecurityScanView(APIView):
L10: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/selected_files_context_views.py
L9: class SelectedFilesContextView(APIView):
L10: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/snapshot_views.py
L7: class SnapshotViewSet(ReadOnlyModelViewSet):
L9: serializer_class = SnapshotSerializer
L10: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/test_plan_views.py
L8: class TestPlanView(APIView):
L9: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/tools_views.py
L9: class ToolsView(APIView):
L10: permission_classes = [CodexAuthenticated]

## Handler declarations: codex/api/views/tool_definition_views.py
L7: class ToolDefinitionViewSet(BaseViewSet):
L9: serializer_class = ToolDefinitionSerializer

## Handler declarations: codex/api/views/workflow_step_views.py
L7: class WorkflowStepViewSet(BaseViewSet):
L9: serializer_class = WorkflowStepSerializer

## Handler declarations: codex/api/views/workflow_views.py
L8: class WorkflowView(APIView):
L9: permission_classes = [CodexAuthenticated]


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
