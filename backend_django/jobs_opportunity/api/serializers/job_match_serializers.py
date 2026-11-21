from rest_framework import serializers
from jobs_opportunity.models import JobMatch
from jobs_opportunity.api.serializers.job_opportunity_serializers import JobOpportunitySerializer


class JobMatchSerializer(serializers.ModelSerializer):
    job_detail = JobOpportunitySerializer(source="job", read_only=True)

    class Meta:
        model = JobMatch
        fields = ["id", "job", "job_detail", "score", "skill_score", "experience_score", "preference_score", "goal_score",
                  "salary_score", "location_score", "matched_skills", "missing_skills", "reasons", "breakdown", "calculated_at"]
