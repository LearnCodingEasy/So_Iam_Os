# jobs_opportunity API

Project prefix: /api/jobs/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: jobs_opportunity/api/urls.py

- L5: router.register(r"sources", JobSourceViewSet, basename="job-source")

- L6: router.register(r"opportunities", JobOpportunityViewSet, basename="job-opportunity")

- L7: router.register(r"matches", JobMatchViewSet, basename="job-match")

- L8: router.register(r"applications", JobApplicationViewSet, basename="job-application")

- L9: router.register(r"companies", CompanyProfileViewSet, basename="job-company")

- L10: router.register(r"interviews", JobInterviewViewSet, basename="job-interview")

- L11: router.register(r"resumes", JobResumeViewSet, basename="job-resume")

- L12: router.register(r"cover-letters", JobCoverLetterViewSet, basename="job-cover-letter")

- L13: router.register(r"preferences", JobPreferenceViewSet, basename="job-preference")

- L14: router.register(r"saved-searches", JobSavedSearchViewSet, basename="job-saved-search")

- L15: router.register(r"skill-gaps", JobSkillGapViewSet, basename="job-skill-gap")

- L16: router.register(r"readiness", JobReadinessViewSet, basename="job-readiness")

- L17: router.register(r"recommendations", JobRecommendationViewSet, basename="job-recommendation")

- L18: router.register(r"alerts", JobAlertViewSet, basename="job-alert")

- L19: router.register(r"analytics", JobAnalyticsSnapshotViewSet, basename="job-analytics")

- L20: router.register(r"workspace", JobsWorkspaceViewSet, basename="jobs-workspace")

## Handler declarations: jobs_opportunity/api/views/company_profile_views.py
L8: class CompanyProfileViewSet(UserOwnedViewSet):
L9: serializer_class = CompanyProfileSerializer
L11: def get_queryset(self): return CompanyProfile.objects.filter(
L14: def perform_create(self, serializer): serializer.save(
L17: @action(detail=True, methods=["post"])
L24: @action(detail=True, methods=["post"])

## Handler declarations: jobs_opportunity/api/views/jobs_workspace_views.py
L11: class JobsWorkspaceViewSet(viewsets.ViewSet):
L12: permission_classes = [IsAuthenticated]
L14: @action(detail=False, methods=["get"])
L18: @action(detail=False, methods=["get"])
L22: @action(detail=False, methods=["post"])
L30: @action(detail=False, methods=["get"])

## Handler declarations: jobs_opportunity/api/views/job_alert_views.py
L8: class JobAlertViewSet(UserOwnedViewSet):
L9: serializer_class = JobAlertSerializer
L11: def get_queryset(self): return JobAlert.objects.filter(
L14: def perform_create(self, serializer): serializer.save(
L17: @action(detail=True, methods=["post"])

## Handler declarations: jobs_opportunity/api/views/job_analytics_snapshot_views.py
L7: class JobAnalyticsSnapshotViewSet(viewsets.ReadOnlyModelViewSet):
L8: serializer_class = JobAnalyticsSnapshotSerializer
L9: permission_classes = [IsAuthenticated]
L10: def get_queryset(self): return JobAnalyticsSnapshot.objects.filter(

## Handler declarations: jobs_opportunity/api/views/job_application_views.py
L8: class JobApplicationViewSet(UserOwnedViewSet):
L9: serializer_class = JobApplicationSerializer
L11: def get_queryset(self): return JobApplication.objects.filter(
L14: def perform_create(self, serializer):
L19: @action(detail=True, methods=["get"])
L23: @action(detail=True, methods=["post"])

## Handler declarations: jobs_opportunity/api/views/job_cover_letter_views.py
L6: class JobCoverLetterViewSet(UserOwnedViewSet):
L7: serializer_class = JobCoverLetterSerializer
L9: def get_queryset(self): return JobCoverLetter.objects.filter(
L11: def perform_create(self, serializer): serializer.save(

## Handler declarations: jobs_opportunity/api/views/job_interview_views.py
L6: class JobInterviewViewSet(UserOwnedViewSet):
L7: serializer_class = JobInterviewSerializer
L8: def get_queryset(self): return JobInterview.objects.filter(

## Handler declarations: jobs_opportunity/api/views/job_match_views.py
L9: class JobMatchViewSet(viewsets.ReadOnlyModelViewSet):
L10: serializer_class = JobMatchSerializer
L12: def get_queryset(self):
L20: @action(detail=False, methods=["post"])

## Handler declarations: jobs_opportunity/api/views/job_opportunity_views.py
L11: class JobOpportunityViewSet(UserOwnedViewSet):
L12: serializer_class = JobOpportunitySerializer
L14: def get_queryset(self):
L53: @action(detail=True, methods=["post"])
L58: @action(detail=True, methods=["post"])
L64: @action(detail=True, methods=["get"])
L69: @action(detail=True, methods=["get"])
L79: @action(detail=False, methods=["get"])
L84: @action(detail=True, methods=["post"], url_path="generate_cover_letter")
L134: @action(detail=True, methods=["post"])

## Handler declarations: jobs_opportunity/api/views/job_preference_views.py
L9: class JobPreferenceViewSet(viewsets.ViewSet):
L10: permission_classes = [IsAuthenticated]
L24: @action(detail=False, methods=["patch", "put"])

## Handler declarations: jobs_opportunity/api/views/job_readiness_views.py
L10: class JobReadinessViewSet(viewsets.ReadOnlyModelViewSet):
L11: serializer_class = JobReadinessSerializer
L12: permission_classes = [IsAuthenticated]
L14: def get_queryset(self): return JobReadiness.objects.filter(
L17: @action(detail=False, methods=["post"])

## Handler declarations: jobs_opportunity/api/views/job_recommendation_views.py
L9: class JobRecommendationViewSet(UserOwnedViewSet):
L10: serializer_class = JobRecommendationSerializer
L12: def get_queryset(self): return JobRecommendation.objects.filter(
L15: @action(detail=False, methods=["post"])
L20: @action(detail=True, methods=["post"])
L27: @action(detail=True, methods=["post"])
L35: @action(detail=True, methods=["post"])

## Handler declarations: jobs_opportunity/api/views/job_resume_views.py
L8: class JobResumeViewSet(UserOwnedViewSet):
L9: serializer_class = JobResumeSerializer
L11: def get_queryset(self): return JobResume.objects.filter(
L14: def perform_create(self, serializer): serializer.save(
L17: @action(detail=True, methods=["post"])

## Handler declarations: jobs_opportunity/api/views/job_saved_search_views.py
L9: class JobSavedSearchViewSet(UserOwnedViewSet):
L10: serializer_class = JobSavedSearchSerializer
L12: def get_queryset(self): return JobSavedSearch.objects.filter(
L15: def perform_create(self, serializer): serializer.save(
L18: @action(detail=True, methods=["post"])

## Handler declarations: jobs_opportunity/api/views/job_skill_gap_views.py
L9: class JobSkillGapViewSet(UserOwnedViewSet):
L10: serializer_class = JobSkillGapSerializer
L12: def get_queryset(self): return JobSkillGap.objects.filter(
L15: @action(detail=True, methods=["post"])

## Handler declarations: jobs_opportunity/api/views/job_source_views.py
L11: class JobSourceViewSet(UserOwnedViewSet):
L12: serializer_class = JobSourceSerializer
L14: def get_queryset(self): return JobSource.objects.filter(
L17: def perform_create(self, serializer): serializer.save(
L20: @action(detail=False, methods=["post"], url_path="sync-all")
L68: @action(detail=False, methods=["get"], url_path="sync-runs")
L88: @action(detail=True, methods=["post"])
L121: @action(detail=True, methods=["post"])
L183: @action(detail=True, methods=["post"])

## Handler declarations: jobs_opportunity/api/views/user_owned_views.py
L5: class UserOwnedViewSet(viewsets.ModelViewSet):
L6: permission_classes = [IsAuthenticated]


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
