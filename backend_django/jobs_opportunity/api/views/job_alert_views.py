from rest_framework.decorators import action
from rest_framework.response import Response
from jobs_opportunity.models import JobAlert
from jobs_opportunity.api.serializers import JobAlertSerializer
from jobs_opportunity.api.views.user_owned_views import UserOwnedViewSet


class JobAlertViewSet(UserOwnedViewSet):
    serializer_class = JobAlertSerializer

    def get_queryset(self): return JobAlert.objects.filter(
        user=self.request.user)

    def perform_create(self, serializer): serializer.save(
        user=self.request.user)

    @action(detail=True, methods=["post"])
    def read(self, request, pk=None):
        obj = self.get_object()
        obj.is_read = True
        obj.save(update_fields=["is_read"])
        return Response(self.get_serializer(obj).data)
