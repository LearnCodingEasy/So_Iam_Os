from rest_framework.routers import DefaultRouter

from analytics.api.views import MetricViewSet, MetricSnapshotViewSet, AnalyticsEventViewSet, ReportViewSet

router = DefaultRouter()
router.register('metrics', MetricViewSet, basename='metric')
router.register('snapshots', MetricSnapshotViewSet, basename='metric-snapshot')
router.register('events', AnalyticsEventViewSet, basename='analytics-event')
router.register('reports', ReportViewSet, basename='report')

urlpatterns = router.urls
