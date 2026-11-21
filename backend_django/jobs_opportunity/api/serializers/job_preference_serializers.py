from rest_framework import serializers
from jobs_opportunity.models import JobPreference


class JobPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPreference
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]
