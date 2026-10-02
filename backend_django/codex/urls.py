from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, FeatureViewSet, FileViewSet, APIEndpointViewSet, ProtectedFeatureViewSet, ChangeSetViewSet, SnapshotViewSet, OverviewView, ScanView, ContextView, PlanChangeView, CreateSnapshotView,     OpenAICodexView


router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="codex-project")
# router.register("ai", OpenAICodexView, basename="codex-ai")
router.register("features", FeatureViewSet, basename="codex-feature")
router.register("files", FileViewSet, basename="codex-file")
router.register("apis", APIEndpointViewSet, basename="codex-api")
router.register("protected", ProtectedFeatureViewSet,
                basename="codex-protected")
router.register("changes", ChangeSetViewSet, basename="codex-change")
router.register("snapshots", SnapshotViewSet, basename="codex-snapshot")
urlpatterns = [
    path("overview/", OverviewView.as_view()),
    path("ai/", OpenAICodexView.as_view()),
    path("scan/", ScanView.as_view()),
    path("context/", ContextView.as_view()),
    path("changes/plan/", PlanChangeView.as_view()),
    path("snapshots/create/", CreateSnapshotView.as_view()),
    path("", include(router.urls)),

]
