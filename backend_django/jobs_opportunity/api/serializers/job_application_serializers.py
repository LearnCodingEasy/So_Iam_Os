from rest_framework import serializers
from jobs_opportunity.models import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    company = serializers.CharField(source="job.company", read_only=True)

    class Meta:
        model = JobApplication
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]

    def validate_resume(self, resume):
        request = self.context.get("request")
        if resume and request and resume.user_id != request.user.id:
            raise serializers.ValidationError(
                "This resume does not belong to the current user.")
        return resume

    def validate_cover_letter(self, cover_letter):
        request = self.context.get("request")
        if cover_letter and request and cover_letter.user_id != request.user.id:
            raise serializers.ValidationError(
                "This cover letter does not belong to the current user.")
        return cover_letter

    def validate_job(self, job):
        request = self.context.get("request")
        if request and job.user_id != request.user.id:
            raise serializers.ValidationError(
                "This job does not belong to the current user.")
        return job
