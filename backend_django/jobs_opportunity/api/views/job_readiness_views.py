from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from jobs_opportunity.models import JobReadiness
from jobs_opportunity.api.serializers import JobReadinessSerializer
from jobs_opportunity.services import JobMatchingService


class JobReadinessViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobReadinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): return JobReadiness.objects.filter(
        user=self.request.user).select_related("job").order_by("-score")

    @action(detail=False, methods=["post"])
    def refresh(self, request):
        JobMatchingService.refresh_for_user(request.user)
        return Response(JobReadinessSerializer(self.get_queryset(), many=True).data)
