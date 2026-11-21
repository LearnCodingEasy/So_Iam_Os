"""jobs_opportunity models package (split from models.py)."""

from .common import PERCENT
from .job_source import JobSource
from .job_source_sync_run import JobSourceSyncRun
from .company_profile import CompanyProfile
from .job_opportunity import JobOpportunity
from .job_skill_requirement import JobSkillRequirement
from .job_match import JobMatch
from .job_application import JobApplication
from .job_application_event import JobApplicationEvent
from .job_interview import JobInterview
from .job_resume import JobResume
from .job_cover_letter import JobCoverLetter
from .job_preference import JobPreference
from .job_saved_search import JobSavedSearch
from .job_skill_gap import JobSkillGap
from .job_readiness import JobReadiness
from .job_recommendation import JobRecommendation
from .job_alert import JobAlert
from .job_analytics_snapshot import JobAnalyticsSnapshot

__all__ = ['PERCENT', 'JobSource', 'JobSourceSyncRun', 'CompanyProfile', 'JobOpportunity', 'JobSkillRequirement', 'JobMatch', 'JobApplication', 'JobApplicationEvent', 'JobInterview', 'JobResume', 'JobCoverLetter', 'JobPreference', 'JobSavedSearch', 'JobSkillGap', 'JobReadiness', 'JobRecommendation', 'JobAlert', 'JobAnalyticsSnapshot']
