# jobs_opportunity security and testing

## Permission/ownership evidence

- jobs_opportunity/api/views/company_profile_views.py:L11: def get_queryset(self): return CompanyProfile.objects.filter(
- jobs_opportunity/api/views/company_profile_views.py:L12: user=self.request.user)
- jobs_opportunity/api/views/company_profile_views.py:L15: user=self.request.user)
- jobs_opportunity/api/views/jobs_workspace_views.py:L3: from rest_framework.permissions import IsAuthenticated
- jobs_opportunity/api/views/jobs_workspace_views.py:L12: permission_classes = [IsAuthenticated]
- jobs_opportunity/api/views/jobs_workspace_views.py:L16: return Response(JobAnalyticsService.dashboard(request.user))
- jobs_opportunity/api/views/jobs_workspace_views.py:L24: matches = JobMatchingService.refresh_for_user(request.user)
- jobs_opportunity/api/views/jobs_workspace_views.py:L25: recommendations = JobRecommendationService.refresh(request.user)
- jobs_opportunity/api/views/jobs_workspace_views.py:L27: request.user, persist_snapshot=True)
- jobs_opportunity/api/views/jobs_workspace_views.py:L35: user=request.user, id__in=ids).prefetch_related("skill_requirements__skill")
- jobs_opportunity/api/views/job_alert_views.py:L11: def get_queryset(self): return JobAlert.objects.filter(
- jobs_opportunity/api/views/job_alert_views.py:L12: user=self.request.user)
- jobs_opportunity/api/views/job_alert_views.py:L15: user=self.request.user)
- jobs_opportunity/api/views/job_analytics_snapshot_views.py:L2: from rest_framework.permissions import IsAuthenticated
- jobs_opportunity/api/views/job_analytics_snapshot_views.py:L9: permission_classes = [IsAuthenticated]
- jobs_opportunity/api/views/job_analytics_snapshot_views.py:L10: def get_queryset(self): return JobAnalyticsSnapshot.objects.filter(
- jobs_opportunity/api/views/job_analytics_snapshot_views.py:L11: user=self.request.user)
- jobs_opportunity/api/views/job_application_views.py:L11: def get_queryset(self): return JobApplication.objects.filter(
- jobs_opportunity/api/views/job_application_views.py:L12: user=self.request.user).select_related("job", "resume", "cover_letter")
- jobs_opportunity/api/views/job_application_views.py:L15: app = serializer.save(user=self.request.user)
- jobs_opportunity/api/views/job_cover_letter_views.py:L9: def get_queryset(self): return JobCoverLetter.objects.filter(
- jobs_opportunity/api/views/job_cover_letter_views.py:L10: user=self.request.user).select_related("job", "resume")
- jobs_opportunity/api/views/job_cover_letter_views.py:L12: user=self.request.user)
- jobs_opportunity/api/views/job_interview_views.py:L8: def get_queryset(self): return JobInterview.objects.filter(
- jobs_opportunity/api/views/job_interview_views.py:L9: application__user=self.request.user).select_related("application", "application__job")
- jobs_opportunity/api/views/job_match_views.py:L12: def get_queryset(self):
- jobs_opportunity/api/views/job_match_views.py:L14: user=self.request.user).select_related("job").order_by("-score")
- jobs_opportunity/api/views/job_match_views.py:L22: matches = JobMatchingService.refresh_for_user(request.user)
- jobs_opportunity/api/views/job_opportunity_views.py:L14: def get_queryset(self):
- jobs_opportunity/api/views/job_opportunity_views.py:L15: qs = JobOpportunity.objects.filter(user=self.request.user).select_related(
- jobs_opportunity/api/views/job_opportunity_views.py:L50: job = JobService.create_job(request.user, **data)
- jobs_opportunity/api/views/job_opportunity_views.py:L55: match = JobMatchingService.calculate(request.user, self.get_object())
- jobs_opportunity/api/views/job_opportunity_views.py:L60: job = JobParserService.analyze(self.get_object(), user=request.user, use_ai=True)
- jobs_opportunity/api/views/job_opportunity_views.py:L61: JobMatchingService.calculate(request.user, job)
- jobs_opportunity/api/views/job_opportunity_views.py:L66: readiness = ReadinessService.calculate(request.user, self.get_object())
- jobs_opportunity/api/views/job_opportunity_views.py:L73: qs = self.get_queryset().exclude(pk=job.pk)
- jobs_opportunity/api/views/job_opportunity_views.py:L82: return Response(self.get_serializer(self.get_queryset().filter(id__in=ids), many=True).data)
- jobs_opportunity/api/views/job_opportunity_views.py:L96: pk=resume_id, user=request.user).first()
- jobs_opportunity/api/views/job_opportunity_views.py:L101: user=request.user, is_default=True).first()
- jobs_opportunity/api/views/job_opportunity_views.py:L103: settings_obj, _ = AISettings.objects.get_or_create(user=request.user)
- jobs_opportunity/api/views/job_opportunity_views.py:L115: result = AIProviderFallbackChain(user=request.user).generate(
- jobs_opportunity/api/views/job_opportunity_views.py:L129: user=request.user, job=job, resume=resume,
- jobs_opportunity/api/views/job_opportunity_views.py:L136: application = JobService.apply(request.user, self.get_object(), status=request.data.get("status", "saved"), notes=request.data.get("notes", ""), resume_id=request.data.get(
- jobs_opportunity/api/views/job_preference_views.py:L3: from rest_framework.permissions import IsAuthenticated
- jobs_opportunity/api/views/job_preference_views.py:L10: permission_classes = [IsAuthenticated]
- jobs_opportunity/api/views/job_preference_views.py:L13: obj, _ = JobPreference.objects.get_or_create(user=request.user)
- jobs_opportunity/api/views/job_preference_views.py:L17: obj, _ = JobPreference.objects.get_or_create(user=request.user)
- jobs_opportunity/api/views/job_preference_views.py:L21: serializer.save(user=request.user)
- jobs_opportunity/api/views/job_preference_views.py:L26: obj, _ = JobPreference.objects.get_or_create(user=request.user)
- jobs_opportunity/api/views/job_preference_views.py:L30: serializer.save(user=request.user)
- jobs_opportunity/api/views/job_readiness_views.py:L3: from rest_framework.permissions import IsAuthenticated
- jobs_opportunity/api/views/job_readiness_views.py:L12: permission_classes = [IsAuthenticated]
- jobs_opportunity/api/views/job_readiness_views.py:L14: def get_queryset(self): return JobReadiness.objects.filter(
- jobs_opportunity/api/views/job_readiness_views.py:L15: user=self.request.user).select_related("job").order_by("-score")
- jobs_opportunity/api/views/job_readiness_views.py:L19: JobMatchingService.refresh_for_user(request.user)
- jobs_opportunity/api/views/job_readiness_views.py:L20: return Response(JobReadinessSerializer(self.get_queryset(), many=True).data)
- jobs_opportunity/api/views/job_recommendation_views.py:L12: def get_queryset(self): return JobRecommendation.objects.filter(
- jobs_opportunity/api/views/job_recommendation_views.py:L13: user=self.request.user).select_related("job").order_by("-score")
- jobs_opportunity/api/views/job_recommendation_views.py:L17: rows = JobRecommendationService.refresh(request.user)
- jobs_opportunity/api/views/job_resume_views.py:L11: def get_queryset(self): return JobResume.objects.filter(
- jobs_opportunity/api/views/job_resume_views.py:L12: user=self.request.user)
- jobs_opportunity/api/views/job_resume_views.py:L15: user=self.request.user)
- jobs_opportunity/api/views/job_resume_views.py:L20: JobResume.objects.filter(user=request.user).exclude(
- jobs_opportunity/api/views/job_saved_search_views.py:L12: def get_queryset(self): return JobSavedSearch.objects.filter(
- jobs_opportunity/api/views/job_saved_search_views.py:L13: user=self.request.user)
- jobs_opportunity/api/views/job_saved_search_views.py:L16: user=self.request.user)
- jobs_opportunity/api/views/job_saved_search_views.py:L24: qs = JobOpportunity.objects.filter(user=request.user, is_active=True)
- jobs_opportunity/api/views/job_skill_gap_views.py:L12: def get_queryset(self): return JobSkillGap.objects.filter(
- jobs_opportunity/api/views/job_skill_gap_views.py:L13: user=self.request.user).select_related("job", "skill", "learning_goal")
- jobs_opportunity/api/views/job_skill_gap_views.py:L18: request.user, self.get_object())
- jobs_opportunity/api/views/job_source_views.py:L14: def get_queryset(self): return JobSource.objects.filter(
- jobs_opportunity/api/views/job_source_views.py:L15: user=self.request.user)
- jobs_opportunity/api/views/job_source_views.py:L18: user=self.request.user)
- jobs_opportunity/api/views/job_source_views.py:L23: sources = self.get_queryset().filter(enabled=True, source_type__in=[JobSource.SourceType.API, JobSource.SourceType.RSS, JobSource.SourceType.SCRAPER]).exclude(base_url="", feed_url="")
- jobs_opportunity/api/views/job_source_views.py:L31: user=request.user,
- jobs_opportunity/api/views/job_source_views.py:L70: runs = JobSourceSyncRun.objects.filter(user=request.user).select_related("source")[:100]
- jobs_opportunity/api/views/job_source_views.py:L101: user=request.user,
- jobs_opportunity/api/views/user_owned_views.py:L2: from rest_framework.permissions import IsAuthenticated
- jobs_opportunity/api/views/user_owned_views.py:L6: permission_classes = [IsAuthenticated]


## Tests
- jobs_opportunity/tests/test_jobs_opportunity.py
- jobs_opportunity/tests/test_rss_parser.py
- jobs_opportunity/tests/__init__.py


Tests were not run. This scan is not a complete authorization/security review. Shared guidance: [authentication and permissions](../../07-authentication-and-permissions.md).
