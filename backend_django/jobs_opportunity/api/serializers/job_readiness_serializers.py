from rest_framework import serializers
from jobs_opportunity.models import JobReadiness


class JobReadinessSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)

    class Meta:
        model = JobReadiness
        fields = "__all__"
        read_only_fields = ["user", "calculated_at"]
