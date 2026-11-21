from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from jobs_opportunity.feature_catalog import FEATURES
from jobs_opportunity.models import JobOpportunity
from jobs_opportunity.api.serializers import JobOpportunitySerializer
from jobs_opportunity.services import JobAnalyticsService, JobMatchingService, JobRecommendationService


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
        analytics = JobAnalyticsService.dashboard(
            request.user, persist_snapshot=True)
        return Response({"matches": len(matches), "recommendations": len(recommendations), "analytics": analytics})

    @action(detail=False, methods=["get"])
    def compare(self, request):
        ids = [int(x) for x in request.query_params.get(
            "ids", "").split(",") if x.isdigit()]
        jobs = JobOpportunity.objects.filter(
            user=request.user, id__in=ids).prefetch_related("skill_requirements__skill")
        return Response(JobOpportunitySerializer(jobs, many=True, context={"request": request}).data)
