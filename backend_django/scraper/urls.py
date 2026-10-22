from rest_framework.routers import DefaultRouter
from .views import WebsiteViewSet, ParentSelectorViewSet, ScrapingConfigViewSet, ScrapingJobViewSet

router = DefaultRouter()
router.register("sources", WebsiteViewSet, basename="scraper-source")
router.register("selectors", ParentSelectorViewSet, basename="scraper-selector")
router.register("configs", ScrapingConfigViewSet, basename="scraper-config")
router.register("runs", ScrapingJobViewSet, basename="scraper-run")
urlpatterns = router.urls
