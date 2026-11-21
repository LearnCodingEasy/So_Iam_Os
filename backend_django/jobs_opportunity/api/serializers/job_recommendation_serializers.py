from rest_framework import serializers
from jobs_opportunity.models import JobRecommendation
from jobs_opportunity.api.serializers.job_opportunity_serializers import JobOpportunitySerializer


class JobRecommendationSerializer(serializers.ModelSerializer):
    job_detail = JobOpportunitySerializer(source="job", read_only=True)

    class Meta:
        model = JobRecommendation
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]
