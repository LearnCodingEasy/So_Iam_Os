from rest_framework import serializers
from .models import (
    CompanyProfile, JobAlert, JobAnalyticsSnapshot, JobApplication, JobApplicationEvent,
    JobCoverLetter, JobInterview, JobMatch, JobOpportunity, JobPreference,
    JobRecommendation, JobReadiness, JobResume, JobSavedSearch, JobSkillGap, JobSkillRequirement, JobSource,
)


class JobSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSource
        fields = "__all__"
        read_only_fields = ["user", "last_synced_at", "last_sync_status", "last_sync_error", "last_sync_count", "created_at", "updated_at"]

    def validate(self, attrs):
        if attrs.get("feed_url") and attrs.get("source_type") not in {"rss", "api"}:
            raise serializers.ValidationError({"source_type": "A feed URL requires RSS or API source type."})
        return attrs


class JobSkillRequirementSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source="skill.name", read_only=True)
    class Meta:
        model = JobSkillRequirement
        fields = ["id", "skill", "skill_name", "required_level", "importance", "requirement_type"]


class JobOpportunitySerializer(serializers.ModelSerializer):
    skill_requirements = JobSkillRequirementSerializer(many=True, read_only=True)
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
        read_only_fields = ["user", "created_at", "updated_at", "discovered_at", "normalized_title", "canonical_key", "match", "readiness", "skill_requirements"]

    def validate_source(self, source):
        request = self.context.get("request")
        if source and request and source.user_id != request.user.id:
            raise serializers.ValidationError("This source does not belong to the current user.")
        return source

    def validate_company_profile(self, value):
        request = self.context.get("request")
        if value and request and value.user_id != request.user.id:
            raise serializers.ValidationError("This company does not belong to the current user.")
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


class JobMatchSerializer(serializers.ModelSerializer):
    job_detail = JobOpportunitySerializer(source="job", read_only=True)
    class Meta:
        model = JobMatch
        fields = ["id", "job", "job_detail", "score", "skill_score", "experience_score", "preference_score", "goal_score", "salary_score", "location_score", "matched_skills", "missing_skills", "reasons", "breakdown", "calculated_at"]


class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    company = serializers.CharField(source="job.company", read_only=True)
    class Meta:
        model = JobApplication
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]

    def validate_job(self, job):
        request = self.context.get("request")
        if request and job.user_id != request.user.id:
            raise serializers.ValidationError("This job does not belong to the current user.")
        return job


class JobApplicationEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplicationEvent
        fields = "__all__"
        read_only_fields = ["id"]


class JobInterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobInterview
        fields = "__all__"

    def validate_application(self, application):
        request = self.context.get("request")
        if request and application.user_id != request.user.id:
            raise serializers.ValidationError("This application does not belong to the current user.")
        return application


class JobResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResume
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]


class JobCoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCoverLetter
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        job = attrs.get("job")
        resume = attrs.get("resume")
        if request and job and job.user_id != request.user.id:
            raise serializers.ValidationError({"job": "Job does not belong to current user."})
        if request and resume and resume.user_id != request.user.id:
            raise serializers.ValidationError({"resume": "Resume does not belong to current user."})
        return attrs


class JobPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPreference
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]


class JobSavedSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSavedSearch
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at", "last_run_at"]


class JobSkillGapSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    class Meta:
        model = JobSkillGap
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]


class JobReadinessSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    class Meta:
        model = JobReadiness
        fields = "__all__"
        read_only_fields = ["user", "calculated_at"]


class JobRecommendationSerializer(serializers.ModelSerializer):
    job_detail = JobOpportunitySerializer(source="job", read_only=True)
    class Meta:
        model = JobRecommendation
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]


class JobAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAlert
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at", "normalized_name"]


class JobAnalyticsSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAnalyticsSnapshot
        fields = "__all__"
        read_only_fields = ["user", "created_at"]
