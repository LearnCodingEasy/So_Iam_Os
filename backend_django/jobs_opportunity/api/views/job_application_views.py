from rest_framework.decorators import action
from rest_framework.response import Response
from jobs_opportunity.models import JobApplication, JobApplicationEvent
from jobs_opportunity.api.serializers import JobApplicationEventSerializer, JobApplicationSerializer
from jobs_opportunity.api.views.user_owned_views import UserOwnedViewSet


class JobApplicationViewSet(UserOwnedViewSet):
    serializer_class = JobApplicationSerializer

    def get_queryset(self): return JobApplication.objects.filter(
        user=self.request.user).select_related("job", "resume", "cover_letter")

    def perform_create(self, serializer):
        app = serializer.save(user=self.request.user)
        JobApplicationEvent.objects.create(
            application=app, event_type="created", title="Application created")

    @action(detail=True, methods=["get"])
    def timeline(self, request, pk=None):
        return Response(JobApplicationEventSerializer(self.get_object().events.all(), many=True).data)

    @action(detail=True, methods=["post"])
    def event(self, request, pk=None):
        app = self.get_object()
        event = JobApplicationEvent.objects.create(application=app, event_type=request.data.get("event_type", "note"), title=request.data.get(
            "title", "Application update"), note=request.data.get("note", ""), metadata=request.data.get("metadata", {}))
        return Response(JobApplicationEventSerializer(event).data, status=201)
