from rest_framework import serializers
from jobs_opportunity.models import JobAlert


class JobAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAlert
        fields = "__all__"
        read_only_fields = ["user", "created_at"]
