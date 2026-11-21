from rest_framework.decorators import action
from rest_framework.response import Response
from jobs_opportunity.models import JobRecommendation
from jobs_opportunity.api.serializers import JobRecommendationSerializer
from jobs_opportunity.services import JobRecommendationService
from jobs_opportunity.api.views.user_owned_views import UserOwnedViewSet


class JobRecommendationViewSet(UserOwnedViewSet):
    serializer_class = JobRecommendationSerializer

    def get_queryset(self): return JobRecommendation.objects.filter(
        user=self.request.user).select_related("job").order_by("-score")

    @action(detail=False, methods=["post"])
    def refresh(self, request):
        rows = JobRecommendationService.refresh(request.user)
        return Response(self.get_serializer(rows, many=True).data)

    @action(detail=True, methods=["post"])
    def seen(self, request, pk=None):
        obj = self.get_object()
        obj.is_seen = True
        obj.save(update_fields=["is_seen", "updated_at"])
        return Response(self.get_serializer(obj).data)

    @action(detail=True, methods=["post"])
    def save(self, request, pk=None):
        obj = self.get_object()
        obj.is_saved = True
        obj.is_dismissed = False
        obj.save(update_fields=["is_saved", "is_dismissed", "updated_at"])
        return Response(self.get_serializer(obj).data)

    @action(detail=True, methods=["post"])
    def dismiss(self, request, pk=None):
        obj = self.get_object()
        obj.is_dismissed = True
        obj.save(update_fields=["is_dismissed", "updated_at"])
        return Response(self.get_serializer(obj).data)
