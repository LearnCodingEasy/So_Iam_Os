from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from jobs_opportunity.models import JobMatch
from jobs_opportunity.api.serializers import JobMatchSerializer
from jobs_opportunity.services import JobMatchingService


class JobMatchViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobMatchSerializer

    def get_queryset(self):
        qs = JobMatch.objects.filter(
            user=self.request.user).select_related("job").order_by("-score")
        if self.request.query_params.get("min_score"):
            qs = qs.filter(score__gte=int(
                self.request.query_params["min_score"]))
        return qs

    @action(detail=False, methods=["post"])
    def refresh(self, request):
        matches = JobMatchingService.refresh_for_user(request.user)
        return Response(JobMatchSerializer(matches, many=True, context={"request": request}).data)
