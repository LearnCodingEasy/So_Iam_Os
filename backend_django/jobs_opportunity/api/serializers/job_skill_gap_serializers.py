from rest_framework import serializers
from jobs_opportunity.models import JobSkillGap


class JobSkillGapSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)

    class Meta:
        model = JobSkillGap
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]
