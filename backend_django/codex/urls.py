from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='codex-project')
router.register('features', FeatureViewSet, basename='codex-feature')
router.register('files', FileViewSet, basename='codex-file')
router.register('apis', APIEndpointViewSet, basename='codex-api')
router.register('protected', ProtectedFeatureViewSet, basename='codex-protected')
router.register('changes', ChangeSetViewSet, basename='codex-change')
router.register('snapshots', SnapshotViewSet, basename='codex-snapshot')
router.register('feature-definitions', FeatureDefinitionViewSet, basename='codex-feature-definition')
router.register('tool-definitions', ToolDefinitionViewSet, basename='codex-tool-definition')
router.register('agent-definitions', AgentDefinitionViewSet, basename='codex-agent-definition')
router.register('protected-items', ProtectedItemViewSet, basename='codex-protected-item')
router.register('workflow-steps', WorkflowStepViewSet, basename='codex-workflow-step')
router.register('local-ai-job-records', LocalAIJobViewSet, basename='codex-local-ai-job-record')


urlpatterns = [
    path('build/workspace/', BuildWorkspaceView.as_view()),
    path('build/manifest/', BuildManifestView.as_view()),
    path('overview/', OverviewView.as_view()),
    path('ai/', OpenAICodexView.as_view()),
    path('scan/', ScanView.as_view()),
    path('context/', ContextView.as_view()),
    path('changes/plan/', PlanChangeView.as_view()),
    path('snapshots/create/', CreateSnapshotView.as_view()),
    path('intelligence/bootstrap/', IntelligenceBootstrapView.as_view()),
    path('intelligence/search/', SearchView.as_view()),
    path('intelligence/graph/', GraphView.as_view()),
    path('intelligence/impact/', ImpactView.as_view()),
    path('intelligence/security/', SecurityScanView.as_view()),
    path('intelligence/duplicates/', DuplicateScanView.as_view()),
    path('intelligence/review/', CodeReviewView.as_view()),
    path('intelligence/test-plan/', TestPlanView.as_view()),
    path('agent/plan/', AgentPlanView.as_view()),
    path('agent/runs/', AgentRunView.as_view()),
    path('policy/', PolicyView.as_view()),
    path('tools/', ToolsView.as_view()),
    path('audit/', AuditView.as_view()),
    path('commands/', SafeCommandsView.as_view()),
    path('automation/intent/', AutomationIntentView.as_view()),
    path('changes/apply/', ApplyChangesView.as_view()),
    path('changes/<int:changeset_id>/rollback/', RollbackView.as_view()),
    path('intelligence/explain/', ExplainFeatureView.as_view()),
    path('intelligence/debug/', DebugView.as_view()),
    path('intelligence/docs/', DocumentationView.as_view()),
    path('registry/features/', CapabilityFeaturesView.as_view()),
    path('registry/tools/', CapabilityToolsView.as_view()),
    path('registry/agents/', CapabilityAgentsView.as_view()),
    path('registry/summary/', CapabilitySummaryView.as_view()),
    path('registry/health/', CapabilityHealthView.as_view()),
    path('registry/bootstrap/', CapabilityBootstrapView.as_view()),
    path('registry/validate/', CapabilityValidateView.as_view()),
    path('registry/runs/', CapabilityRunsView.as_view()),
    path('registry/tools/<str:key>/execute/', CapabilityToolExecuteView.as_view()),
    path('registry/agents/<str:key>/execute/', CapabilityAgentExecuteView.as_view()),
    path('context/export/', ProjectContextExportView.as_view()),
    path('files/<int:file_id>/content/', FileContentView.as_view()),
    path('governance/protected-items/', ProtectedRegistryView.as_view()),
    path('governance/manifest/', ProtectedManifestView.as_view()),
    path('workflow/', WorkflowView.as_view()),
    path('local-ai/jobs/', LocalAIJobsView.as_view()),
    path('local-ai/jobs/<int:job_id>/', LocalAIJobDetailView.as_view()),
    path('prompts/generate/', PromptGeneratorView.as_view()),
    path('markdown/navigation/', MarkdownNavigationView.as_view()),
    path('files/open-local/', LocalFileOpenView.as_view()),
    path('architecture/analyze/', ArchitectureModuleAnalyzerView.as_view()),
    path('files/context/', SelectedFilesContextView.as_view()),
    path('', include(router.urls)),
]
