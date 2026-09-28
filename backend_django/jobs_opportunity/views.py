from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .feature_catalog import FEATURES
from .models import (
    CompanyProfile, JobAlert, JobAnalyticsSnapshot, JobApplication, JobApplicationEvent,
    JobCoverLetter, JobInterview, JobMatch, JobOpportunity, JobPreference,
    JobRecommendation, JobReadiness, JobResume, JobSavedSearch, JobSkillGap, JobSource,
)
from .serializers import (
    CompanyProfileSerializer, JobAlertSerializer, JobAnalyticsSnapshotSerializer, JobApplicationEventSerializer,
    JobApplicationSerializer, JobCoverLetterSerializer, JobInterviewSerializer, JobMatchSerializer,
    JobOpportunitySerializer, JobPreferenceSerializer, JobReadinessSerializer, JobRecommendationSerializer,
    JobResumeSerializer, JobSavedSearchSerializer, JobSkillGapSerializer, JobSourceSerializer,
)
from .services import JobAnalyticsService, JobGapService, JobMatchingService, JobParserService, JobRecommendationService, JobService, ReadinessService


class UserOwnedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]


class JobSourceViewSet(UserOwnedViewSet):
    serializer_class = JobSourceSerializer
    def get_queryset(self): return JobSource.objects.filter(user=self.request.user)
    def perform_create(self, serializer): serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def test(self, request, pk=None):
        source = self.get_object()
        return Response({"ok": bool(source.feed_url or source.base_url), "source_id": source.id, "message": "Source configuration is ready for the sync worker."})

    @action(detail=True, methods=["post"])
    def sync(self, request, pk=None):
        from .tasks import sync_job_source
        source_id = self.get_object().id
        if request.data.get("background") is True:
            task = sync_job_source.delay(source_id)
            return Response({"queued": True, "task_id": task.id})
        result = sync_job_source(source_id)
        return Response(result)


class JobOpportunityViewSet(UserOwnedViewSet):
    serializer_class = JobOpportunitySerializer

    def get_queryset(self):
        qs = JobOpportunity.objects.filter(user=self.request.user).select_related("source", "company_profile").prefetch_related("skill_requirements__skill", "matches", "readiness_records")
        p = self.request.query_params
        q = p.get("q")
        if q: qs = qs.filter(Q(title__icontains=q) | Q(company__icontains=q) | Q(description__icontains=q) | Q(location__icontains=q))
        if p.get("remote") == "true": qs = qs.filter(is_remote=True)
        if p.get("job_type"): qs = qs.filter(job_type=p["job_type"])
        if p.get("experience"): qs = qs.filter(experience_level=p["experience"])
        if p.get("location"): qs = qs.filter(location__icontains=p["location"])
        if p.get("skill"): qs = qs.filter(skill_requirements__skill__slug__iexact=p["skill"]).distinct()
        if p.get("salary_min"): qs = qs.filter(salary_max__gte=p["salary_min"])
        if p.get("salary_max"): qs = qs.filter(salary_min__lte=p["salary_max"])
        if p.get("source"): qs = qs.filter(source_id=p["source"])
        if p.get("active") in {"true", "false"}: qs = qs.filter(is_active=p["active"] == "true")
        if p.get("fresh") == "true": qs = qs.order_by("-published_at", "-discovered_at")
        return qs.distinct()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        data["skill_ids"] = request.data.get("skill_ids", [])
        job = JobService.create_job(request.user, **data)
        return Response(self.get_serializer(job).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def refresh_match(self, request, pk=None):
        match = JobMatchingService.calculate(request.user, self.get_object())
        return Response(JobMatchSerializer(match, context={"request": request}).data)

    @action(detail=True, methods=["post"])
    def analyze(self, request, pk=None):
        job = JobParserService.analyze(self.get_object())
        JobMatchingService.calculate(request.user, job)
        return Response(self.get_serializer(job).data)

    @action(detail=True, methods=["get"])
    def readiness(self, request, pk=None):
        readiness = ReadinessService.calculate(request.user, self.get_object())
        return Response(JobReadinessSerializer(readiness).data)

    @action(detail=True, methods=["get"])
    def similar(self, request, pk=None):
        job = self.get_object()
        terms = [x for x in [job.company, job.location, job.job_type] if x]
        qs = self.get_queryset().exclude(pk=job.pk)
        if terms:
            qs = qs.filter(Q(company__icontains=job.company) | Q(location__icontains=job.location) | Q(job_type=job.job_type))
        return Response(self.get_serializer(qs[:20], many=True).data)

    @action(detail=False, methods=["get"])
    def compare(self, request):
        ids = [x for x in request.query_params.get("ids", "").split(",") if x]
        return Response(self.get_serializer(self.get_queryset().filter(id__in=ids), many=True).data)

    @action(detail=True, methods=["post"])
    def apply(self, request, pk=None):
        application = JobService.apply(request.user, self.get_object(), status=request.data.get("status", "saved"), notes=request.data.get("notes", ""), resume_id=request.data.get("resume"), cover_letter_id=request.data.get("cover_letter"), deadline=request.data.get("deadline"), expected_salary=request.data.get("expected_salary"))
        return Response(JobApplicationSerializer(application, context={"request": request}).data)


class JobMatchViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobMatchSerializer
    def get_queryset(self):
        qs = JobMatch.objects.filter(user=self.request.user).select_related("job").order_by("-score")
        if self.request.query_params.get("min_score"):
            qs = qs.filter(score__gte=int(self.request.query_params["min_score"]))
        return qs
    @action(detail=False, methods=["post"])
    def refresh(self, request):
        matches = JobMatchingService.refresh_for_user(request.user)
        return Response(JobMatchSerializer(matches, many=True, context={"request": request}).data)


class JobApplicationViewSet(UserOwnedViewSet):
    serializer_class = JobApplicationSerializer
    def get_queryset(self): return JobApplication.objects.filter(user=self.request.user).select_related("job", "resume", "cover_letter")
    def perform_create(self, serializer):
        app = serializer.save(user=self.request.user)
        JobApplicationEvent.objects.create(application=app, event_type="created", title="Application created")
    @action(detail=True, methods=["get"])
    def timeline(self, request, pk=None):
        return Response(JobApplicationEventSerializer(self.get_object().events.all(), many=True).data)
    @action(detail=True, methods=["post"])
    def event(self, request, pk=None):
        app = self.get_object()
        event = JobApplicationEvent.objects.create(application=app, event_type=request.data.get("event_type", "note"), title=request.data.get("title", "Application update"), note=request.data.get("note", ""), metadata=request.data.get("metadata", {}))
        return Response(JobApplicationEventSerializer(event).data, status=201)


class CompanyProfileViewSet(UserOwnedViewSet):
    serializer_class = CompanyProfileSerializer
    def get_queryset(self): return CompanyProfile.objects.filter(user=self.request.user)
    def perform_create(self, serializer): serializer.save(user=self.request.user)
    @action(detail=True, methods=["post"])
    def toggle_follow(self, request, pk=None):
        company = self.get_object(); company.is_followed = not company.is_followed; company.save(update_fields=["is_followed", "updated_at"])
        return Response(self.get_serializer(company).data)
    @action(detail=True, methods=["post"])
    def toggle_blacklist(self, request, pk=None):
        company = self.get_object(); company.is_blacklisted = not company.is_blacklisted; company.save(update_fields=["is_blacklisted", "updated_at"])
        return Response(self.get_serializer(company).data)


class JobInterviewViewSet(UserOwnedViewSet):
    serializer_class = JobInterviewSerializer
    def get_queryset(self): return JobInterview.objects.filter(application__user=self.request.user).select_related("application", "application__job")


class JobResumeViewSet(UserOwnedViewSet):
    serializer_class = JobResumeSerializer
    def get_queryset(self): return JobResume.objects.filter(user=self.request.user)
    def perform_create(self, serializer): serializer.save(user=self.request.user)
    @action(detail=True, methods=["post"])
    def make_default(self, request, pk=None):
        resume = self.get_object(); JobResume.objects.filter(user=request.user).exclude(pk=resume.pk).update(is_default=False); resume.is_default=True; resume.save(update_fields=["is_default", "updated_at"]); return Response(self.get_serializer(resume).data)


class JobCoverLetterViewSet(UserOwnedViewSet):
    serializer_class = JobCoverLetterSerializer
    def get_queryset(self): return JobCoverLetter.objects.filter(user=self.request.user).select_related("job", "resume")
    def perform_create(self, serializer): serializer.save(user=self.request.user)


class JobPreferenceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        obj, _ = JobPreference.objects.get_or_create(user=request.user)
        return Response(JobPreferenceSerializer(obj).data)
    def create(self, request):
        obj, _ = JobPreference.objects.get_or_create(user=request.user)
        serializer = JobPreferenceSerializer(obj, data=request.data, partial=True, context={"request": request}); serializer.is_valid(raise_exception=True); serializer.save(user=request.user); return Response(serializer.data)
    @action(detail=False, methods=["patch", "put"])
    def update_preferences(self, request):
        obj, _ = JobPreference.objects.get_or_create(user=request.user)
        serializer = JobPreferenceSerializer(obj, data=request.data, partial=True, context={"request": request}); serializer.is_valid(raise_exception=True); serializer.save(user=request.user); return Response(serializer.data)


class JobSavedSearchViewSet(UserOwnedViewSet):
    serializer_class = JobSavedSearchSerializer
    def get_queryset(self): return JobSavedSearch.objects.filter(user=self.request.user)
    def perform_create(self, serializer): serializer.save(user=self.request.user)
    @action(detail=True, methods=["post"])
    def run(self, request, pk=None):
        search = self.get_object(); params = {**search.filters}
        if search.query: params["q"] = search.query
        qs = JobOpportunity.objects.filter(user=request.user, is_active=True)
        if params.get("q"): qs = qs.filter(Q(title__icontains=params["q"]) | Q(company__icontains=params["q"]) | Q(description__icontains=params["q"]))
        search.last_run_at = __import__("django.utils.timezone", fromlist=["now"]).now(); search.save(update_fields=["last_run_at", "updated_at"])
        return Response(JobOpportunitySerializer(qs[:100], many=True, context={"request": request}).data)


class JobSkillGapViewSet(UserOwnedViewSet):
    serializer_class = JobSkillGapSerializer
    def get_queryset(self): return JobSkillGap.objects.filter(user=self.request.user).select_related("job", "skill", "learning_goal")
    @action(detail=True, methods=["post"])
    def start_learning(self, request, pk=None):
        goal = JobGapService.create_learning_goal(request.user, self.get_object())
        return Response({"learning_goal_id": goal.id, "title": goal.title})


class JobReadinessViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobReadinessSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return JobReadiness.objects.filter(user=self.request.user).select_related("job").order_by("-score")
    @action(detail=False, methods=["post"])
    def refresh(self, request):
        JobMatchingService.refresh_for_user(request.user)
        return Response(JobReadinessSerializer(self.get_queryset(), many=True).data)


class JobRecommendationViewSet(UserOwnedViewSet):
    serializer_class = JobRecommendationSerializer
    def get_queryset(self): return JobRecommendation.objects.filter(user=self.request.user).select_related("job").order_by("-score")
    @action(detail=False, methods=["post"])
    def refresh(self, request):
        rows = JobRecommendationService.refresh(request.user)
        return Response(self.get_serializer(rows, many=True).data)
    @action(detail=True, methods=["post"])
    def seen(self, request, pk=None):
        obj = self.get_object(); obj.is_seen=True; obj.save(update_fields=["is_seen", "updated_at"]); return Response(self.get_serializer(obj).data)
    @action(detail=True, methods=["post"])
    def save(self, request, pk=None):
        obj = self.get_object(); obj.is_saved=True; obj.is_dismissed=False; obj.save(update_fields=["is_saved", "is_dismissed", "updated_at"]); return Response(self.get_serializer(obj).data)
    @action(detail=True, methods=["post"])
    def dismiss(self, request, pk=None):
        obj = self.get_object(); obj.is_dismissed=True; obj.save(update_fields=["is_dismissed", "updated_at"]); return Response(self.get_serializer(obj).data)


class JobAlertViewSet(UserOwnedViewSet):
    serializer_class = JobAlertSerializer
    def get_queryset(self): return JobAlert.objects.filter(user=self.request.user)
    def perform_create(self, serializer): serializer.save(user=self.request.user)
    @action(detail=True, methods=["post"])
    def read(self, request, pk=None):
        obj=self.get_object(); obj.is_read=True; obj.save(update_fields=["is_read"]); return Response(self.get_serializer(obj).data)


class JobAnalyticsSnapshotViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobAnalyticsSnapshotSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return JobAnalyticsSnapshot.objects.filter(user=self.request.user)


class JobsWorkspaceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        return Response(JobAnalyticsService.dashboard(request.user))

    @action(detail=False, methods=["get"])
    def features(self, request):
        return Response({"count": len(FEATURES), "features": [{"id": i + 1, "category": c, "name": n, "status": "available"} for i, (c, n) in enumerate(FEATURES)]})

    @action(detail=False, methods=["post"])
    def refresh_all(self, request):
        matches = JobMatchingService.refresh_for_user(request.user)
        recommendations = JobRecommendationService.refresh(request.user)
        analytics = JobAnalyticsService.dashboard(request.user)
        return Response({"matches": len(matches), "recommendations": len(recommendations), "analytics": analytics})

    @action(detail=False, methods=["get"])
    def compare(self, request):
        ids = [int(x) for x in request.query_params.get("ids", "").split(",") if x.isdigit()]
        jobs = JobOpportunity.objects.filter(user=request.user, id__in=ids).prefetch_related("skill_requirements__skill")
        return Response(JobOpportunitySerializer(jobs, many=True, context={"request": request}).data)
