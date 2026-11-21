from rest_framework import serializers
from jobs_opportunity.models import JobOpportunity
from jobs_opportunity.api.serializers.job_skill_requirement_serializers import JobSkillRequirementSerializer


class JobOpportunitySerializer(serializers.ModelSerializer):
    skill_requirements = JobSkillRequirementSerializer(
        many=True, read_only=True)
    match = serializers.SerializerMethodField()
    readiness = serializers.SerializerMethodField()

    class Meta:
        model = JobOpportunity
        fields = [
            "id", "user", "source", "company_profile", "external_id", "canonical_key",
            "title", "normalized_title", "company", "description", "responsibilities",
            "benefits", "extracted_requirements", "url", "location", "location_type",
            "is_remote", "job_type", "experience_level", "salary_min", "salary_max",
            "salary_estimated", "salary_period", "currency", "tags", "metadata", "ai_summary",
            "red_flags", "published_at", "application_deadline", "expires_at", "discovered_at",
            "last_checked_at", "freshness_score", "is_active", "is_expired", "created_at",
            "updated_at", "skill_requirements", "match", "readiness",
        ]
        read_only_fields = ["user", "created_at", "updated_at", "discovered_at",
                            "normalized_title", "canonical_key", "match", "readiness", "skill_requirements"]

    def validate_source(self, source):
        request = self.context.get("request")
        if source and request and source.user_id != request.user.id:
            raise serializers.ValidationError(
                "This source does not belong to the current user.")
        return source

    def validate_company_profile(self, value):
        request = self.context.get("request")
        if value and request and value.user_id != request.user.id:
            raise serializers.ValidationError(
                "This company does not belong to the current user.")
        return value

    def get_match(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return None
        m = obj.matches.filter(user=request.user).first()
        return None if not m else {"score": m.score, "matched_skills": m.matched_skills, "missing_skills": m.missing_skills, "reasons": m.reasons, "breakdown": m.breakdown}

    def get_readiness(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return None
        r = obj.readiness_records.filter(user=request.user).first()
        return None if not r else {"score": r.score, "level": r.level, "next_actions": r.next_actions, "breakdown": r.breakdown}
