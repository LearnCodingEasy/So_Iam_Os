from rest_framework import serializers
from jobs_opportunity.models import JobResume


class JobResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResume
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]
