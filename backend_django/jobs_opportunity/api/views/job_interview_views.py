from jobs_opportunity.models import JobInterview
from jobs_opportunity.api.serializers import JobInterviewSerializer
from jobs_opportunity.api.views.user_owned_views import UserOwnedViewSet


class JobInterviewViewSet(UserOwnedViewSet):
    serializer_class = JobInterviewSerializer
    def get_queryset(self): return JobInterview.objects.filter(
        application__user=self.request.user).select_related("application", "application__job")
