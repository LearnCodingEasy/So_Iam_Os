from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from jobs_opportunity.models import JobAnalyticsSnapshot
from jobs_opportunity.api.serializers import JobAnalyticsSnapshotSerializer


class JobAnalyticsSnapshotViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobAnalyticsSnapshotSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return JobAnalyticsSnapshot.objects.filter(
        user=self.request.user)
