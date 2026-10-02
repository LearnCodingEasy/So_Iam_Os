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

urlpatterns = [
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
    path('', include(router.urls)),
]
