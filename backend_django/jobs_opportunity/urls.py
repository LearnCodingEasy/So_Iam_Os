from rest_framework.routers import DefaultRouter
from .views import JobApplicationViewSet, JobMatchViewSet, JobOpportunityViewSet, JobSourceViewSet
router = DefaultRouter()
router.register(r"sources", JobSourceViewSet, basename="job-source")
router.register(r"opportunities", JobOpportunityViewSet, basename="job-opportunity")
router.register(r"matches", JobMatchViewSet, basename="job-match")
router.register(r"applications", JobApplicationViewSet, basename="job-application")
urlpatterns = router.urls
