from rest_framework.routers import DefaultRouter

from revenue.api.views import RevenueSourceViewSet, RevenueStreamViewSet, RevenueRecordViewSet, RecurringRevenueViewSet

router = DefaultRouter()
router.register('sources', RevenueSourceViewSet, basename='revenue-source')
router.register('streams', RevenueStreamViewSet, basename='revenue-stream')
router.register('records', RevenueRecordViewSet, basename='revenue-record')
router.register('recurring', RecurringRevenueViewSet, basename='recurring-revenue')

urlpatterns = router.urls
