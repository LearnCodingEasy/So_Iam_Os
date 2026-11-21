from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from jobs_opportunity.models import JobOpportunity, JobSavedSearch
from jobs_opportunity.api.serializers import JobOpportunitySerializer, JobSavedSearchSerializer
from jobs_opportunity.api.views.user_owned_views import UserOwnedViewSet


class JobSavedSearchViewSet(UserOwnedViewSet):
    serializer_class = JobSavedSearchSerializer

    def get_queryset(self): return JobSavedSearch.objects.filter(
        user=self.request.user)

    def perform_create(self, serializer): serializer.save(
        user=self.request.user)

    @action(detail=True, methods=["post"])
    def run(self, request, pk=None):
        search = self.get_object()
        params = {**search.filters}
        if search.query:
            params["q"] = search.query
        qs = JobOpportunity.objects.filter(user=request.user, is_active=True)
        if params.get("q"):
            qs = qs.filter(Q(title__icontains=params["q"]) | Q(
                company__icontains=params["q"]) | Q(description__icontains=params["q"]))
        search.last_run_at = __import__(
            "django.utils.timezone", fromlist=["now"]).now()
        search.save(update_fields=["last_run_at", "updated_at"])
        return Response(JobOpportunitySerializer(qs[:100], many=True, context={"request": request}).data)
