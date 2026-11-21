from rest_framework import serializers
from jobs_opportunity.models import JobCoverLetter


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
            raise serializers.ValidationError(
                {"job": "Job does not belong to current user."})
        if request and resume and resume.user_id != request.user.id:
            raise serializers.ValidationError(
                {"resume": "Resume does not belong to current user."})
        return attrs
