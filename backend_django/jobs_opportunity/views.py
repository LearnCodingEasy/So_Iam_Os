from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import JobApplication, JobMatch, JobOpportunity, JobSource
from .serializers import JobApplicationSerializer, JobMatchSerializer, JobOpportunitySerializer, JobSourceSerializer
from .services import JobMatchingService, JobService


class JobSourceViewSet(viewsets.ModelViewSet):
    serializer_class = JobSourceSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return JobSource.objects.filter(user=self.request.user)
    def perform_create(self, serializer): serializer.save(user=self.request.user)
    @action(detail=True, methods=["post"])
    def test(self, request, pk=None):
        source = self.get_object()
        return Response({"ok": bool(source.feed_url or source.base_url), "source_id": source.id, "message": "Source configuration is reachable by the sync worker."})


class JobOpportunityViewSet(viewsets.ModelViewSet):
    serializer_class = JobOpportunitySerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = JobOpportunity.objects.filter(user=self.request.user).prefetch_related("skill_requirements__skill", "matches")
        q = self.request.query_params.get("q")
        if q: qs = qs.filter(Q(title__icontains=q) | Q(company__icontains=q) | Q(description__icontains=q) | Q(location__icontains=q))
        if self.request.query_params.get("remote") == "true": qs = qs.filter(is_remote=True)
        if self.request.query_params.get("job_type"): qs = qs.filter(job_type=self.request.query_params["job_type"])
        return qs
    def perform_create(self, serializer):
        data = dict(serializer.validated_data)
        job = JobService.create_job(self.request.user, **data)
        self._created = job
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data); serializer.is_valid(raise_exception=True)
        skill_ids = request.data.get("skill_ids", [])
        data = dict(serializer.validated_data); data["skill_ids"] = skill_ids
        job = JobService.create_job(request.user, **data)
        return Response(self.get_serializer(job).data, status=201)
    @action(detail=True, methods=["post"])
    def refresh_match(self, request, pk=None):
        match = JobMatchingService.calculate(request.user, self.get_object())
        return Response(JobMatchSerializer(match, context={"request": request}).data)
    @action(detail=True, methods=["post"])
    def apply(self, request, pk=None):
        application = JobService.apply(request.user, self.get_object(), status=request.data.get("status", "saved"), notes=request.data.get("notes", ""))
        return Response(JobApplicationSerializer(application).data)


class JobMatchViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobMatchSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = JobMatch.objects.filter(user=self.request.user).select_related("job").order_by("-score")
        minimum = self.request.query_params.get("min_score")
        if minimum: qs = qs.filter(score__gte=int(minimum))
        return qs
    @action(detail=False, methods=["post"])
    def refresh(self, request):
        matches = JobMatchingService.refresh_for_user(request.user)
        return Response(JobMatchSerializer(matches, many=True, context={"request": request}).data)


class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return JobApplication.objects.filter(user=self.request.user).select_related("job")
    def perform_create(self, serializer): serializer.save(user=self.request.user)
