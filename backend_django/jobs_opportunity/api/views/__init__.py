"""jobs_opportunity views package (split from views.py)."""

from .user_owned_views import UserOwnedViewSet
from .job_source_views import JobSourceViewSet
from .job_opportunity_views import JobOpportunityViewSet
from .job_match_views import JobMatchViewSet
from .job_application_views import JobApplicationViewSet
from .company_profile_views import CompanyProfileViewSet
from .job_interview_views import JobInterviewViewSet
from .job_resume_views import JobResumeViewSet
from .job_cover_letter_views import JobCoverLetterViewSet
from .job_preference_views import JobPreferenceViewSet
from .job_saved_search_views import JobSavedSearchViewSet
from .job_skill_gap_views import JobSkillGapViewSet
from .job_readiness_views import JobReadinessViewSet
from .job_recommendation_views import JobRecommendationViewSet
from .job_alert_views import JobAlertViewSet
from .job_analytics_snapshot_views import JobAnalyticsSnapshotViewSet
from .jobs_workspace_views import JobsWorkspaceViewSet

__all__ = ['UserOwnedViewSet', 'JobSourceViewSet', 'JobOpportunityViewSet', 'JobMatchViewSet', 'JobApplicationViewSet', 'CompanyProfileViewSet', 'JobInterviewViewSet', 'JobResumeViewSet', 'JobCoverLetterViewSet', 'JobPreferenceViewSet', 'JobSavedSearchViewSet', 'JobSkillGapViewSet', 'JobReadinessViewSet', 'JobRecommendationViewSet', 'JobAlertViewSet', 'JobAnalyticsSnapshotViewSet', 'JobsWorkspaceViewSet']
