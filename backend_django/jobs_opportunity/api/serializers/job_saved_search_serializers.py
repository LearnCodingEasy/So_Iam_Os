from rest_framework import serializers
from jobs_opportunity.models import JobSavedSearch


class JobSavedSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSavedSearch
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at", "last_run_at"]
