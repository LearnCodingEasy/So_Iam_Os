from django.contrib import admin
from .models import (
    CompanyProfile, JobAlert, JobAnalyticsSnapshot, JobApplication, JobApplicationEvent,
    JobCoverLetter, JobInterview, JobMatch, JobOpportunity, JobPreference,
    JobRecommendation, JobReadiness, JobResume, JobSavedSearch, JobSkillGap,
    JobSkillRequirement, JobSource,
)

admin.site.register([
    JobSource, JobOpportunity, JobSkillRequirement, JobMatch, JobApplication,
    JobApplicationEvent, JobInterview, JobResume, JobCoverLetter, JobPreference,
    JobSavedSearch, JobSkillGap, JobReadiness, JobRecommendation, JobAlert,
    CompanyProfile, JobAnalyticsSnapshot,
])
