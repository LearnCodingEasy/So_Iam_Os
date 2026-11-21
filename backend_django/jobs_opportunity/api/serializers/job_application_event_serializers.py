from rest_framework import serializers
from jobs_opportunity.models import JobApplicationEvent


class JobApplicationEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplicationEvent
        fields = "__all__"
        read_only_fields = ["id"]
