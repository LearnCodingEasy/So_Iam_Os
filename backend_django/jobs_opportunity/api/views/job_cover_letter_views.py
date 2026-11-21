from jobs_opportunity.models import JobCoverLetter
from jobs_opportunity.api.serializers import JobCoverLetterSerializer
from jobs_opportunity.api.views.user_owned_views import UserOwnedViewSet


class JobCoverLetterViewSet(UserOwnedViewSet):
    serializer_class = JobCoverLetterSerializer

    def get_queryset(self): return JobCoverLetter.objects.filter(
        user=self.request.user).select_related("job", "resume")
    def perform_create(self, serializer): serializer.save(
        user=self.request.user)
