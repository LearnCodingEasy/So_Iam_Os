from rest_framework.routers import DefaultRouter
from .views import (
    CompanyProfileViewSet, JobAlertViewSet, JobAnalyticsSnapshotViewSet, JobApplicationViewSet,
    JobCoverLetterViewSet, JobInterviewViewSet, JobMatchViewSet, JobOpportunityViewSet,
    JobPreferenceViewSet, JobReadinessViewSet, JobRecommendationViewSet, JobResumeViewSet,
    JobSavedSearchViewSet, JobSkillGapViewSet, JobSourceViewSet, JobsWorkspaceViewSet,
)

router = DefaultRouter()
router.register(r"sources", JobSourceViewSet, basename="job-source")
router.register(r"opportunities", JobOpportunityViewSet, basename="job-opportunity")
router.register(r"matches", JobMatchViewSet, basename="job-match")
router.register(r"applications", JobApplicationViewSet, basename="job-application")
router.register(r"companies", CompanyProfileViewSet, basename="job-company")
router.register(r"interviews", JobInterviewViewSet, basename="job-interview")
router.register(r"resumes", JobResumeViewSet, basename="job-resume")
router.register(r"cover-letters", JobCoverLetterViewSet, basename="job-cover-letter")
router.register(r"preferences", JobPreferenceViewSet, basename="job-preference")
router.register(r"saved-searches", JobSavedSearchViewSet, basename="job-saved-search")
router.register(r"skill-gaps", JobSkillGapViewSet, basename="job-skill-gap")
router.register(r"readiness", JobReadinessViewSet, basename="job-readiness")
router.register(r"recommendations", JobRecommendationViewSet, basename="job-recommendation")
router.register(r"alerts", JobAlertViewSet, basename="job-alert")
router.register(r"analytics", JobAnalyticsSnapshotViewSet, basename="job-analytics")
router.register(r"workspace", JobsWorkspaceViewSet, basename="jobs-workspace")
urlpatterns = router.urls
