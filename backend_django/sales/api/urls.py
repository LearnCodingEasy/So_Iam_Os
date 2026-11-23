from rest_framework.routers import DefaultRouter

from sales.api.views import OfferViewSet, DealViewSet, SaleViewSet, SalesActivityViewSet

router = DefaultRouter()
router.register('offers', OfferViewSet, basename='offer')
router.register('deals', DealViewSet, basename='deal')
router.register('sales', SaleViewSet, basename='sale')
router.register('activities', SalesActivityViewSet, basename='sales-activity')

urlpatterns = router.urls
