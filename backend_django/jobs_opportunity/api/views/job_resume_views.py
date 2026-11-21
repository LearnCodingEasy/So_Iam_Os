from rest_framework.decorators import action
from rest_framework.response import Response
from jobs_opportunity.models import JobResume
from jobs_opportunity.api.serializers import JobResumeSerializer
from jobs_opportunity.api.views.user_owned_views import UserOwnedViewSet


class JobResumeViewSet(UserOwnedViewSet):
    serializer_class = JobResumeSerializer

    def get_queryset(self): return JobResume.objects.filter(
        user=self.request.user)

    def perform_create(self, serializer): serializer.save(
        user=self.request.user)

    @action(detail=True, methods=["post"])
    def make_default(self, request, pk=None):
        resume = self.get_object()
        JobResume.objects.filter(user=request.user).exclude(
            pk=resume.pk).update(is_default=False)
        resume.is_default = True
        resume.save(update_fields=["is_default", "updated_at"])
        return Response(self.get_serializer(resume).data)
