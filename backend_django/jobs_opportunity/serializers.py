from rest_framework import serializers
from .models import JobApplication, JobMatch, JobOpportunity, JobSkillRequirement, JobSource


class JobSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSource
        fields = "__all__"
        read_only_fields = ["user", "last_synced_at", "last_sync_status", "last_sync_error", "created_at", "updated_at"]
    def validate(self, attrs):
        request=self.context.get("request")
        if request and attrs.get("feed_url") and attrs["source_type"] not in {"rss","api"}:
            raise serializers.ValidationError({"source_type":"A feed URL requires RSS or API source type."})
        return attrs


class JobSkillRequirementSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source="skill.name", read_only=True)
    class Meta:
        model = JobSkillRequirement
        fields = ["id", "skill", "skill_name", "required_level", "importance"]


class JobOpportunitySerializer(serializers.ModelSerializer):
    skill_requirements = JobSkillRequirementSerializer(many=True, read_only=True)
    match = serializers.SerializerMethodField()
    class Meta:
        model = JobOpportunity
        fields = ["id", "source", "external_id", "title", "company", "description", "url", "location", "is_remote", "job_type", "salary_min", "salary_max", "currency", "metadata", "published_at", "discovered_at", "is_active", "skill_requirements", "match", "created_at", "updated_at"]
        read_only_fields = ["user", "created_at", "updated_at", "discovered_at", "match"]
    def validate_source(self, source):
        request=self.context.get("request")
        if source and request and source.user_id != request.user.id:
            raise serializers.ValidationError("This source does not belong to the current user.")
        return source

    def get_match(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return None
        m = obj.matches.filter(user=request.user).first()
        return None if not m else {"score": m.score, "matched_skills": m.matched_skills, "missing_skills": m.missing_skills, "reasons": m.reasons}


class JobMatchSerializer(serializers.ModelSerializer):
    job_detail = JobOpportunitySerializer(source="job", read_only=True)
    class Meta:
        model = JobMatch
        fields = ["id", "job", "job_detail", "score", "matched_skills", "missing_skills", "reasons", "calculated_at"]


class JobApplicationSerializer(serializers.ModelSerializer):
    def validate_job(self, job):
        request=self.context.get("request")
        if request and job.user_id != request.user.id:
            raise serializers.ValidationError("This job does not belong to the current user.")
        return job
    class Meta:
        model = JobApplication
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]
