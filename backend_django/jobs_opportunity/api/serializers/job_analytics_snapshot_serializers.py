from rest_framework import serializers
from jobs_opportunity.models import JobAnalyticsSnapshot


class JobAnalyticsSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAnalyticsSnapshot
        fields = "__all__"
        read_only_fields = ["user", "created_at"]
