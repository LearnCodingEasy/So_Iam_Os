from rest_framework import serializers
from jobs_opportunity.models import JobInterview


class JobInterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobInterview
        fields = "__all__"

    def validate_application(self, application):
        request = self.context.get("request")
        if request and application.user_id != request.user.id:
            raise serializers.ValidationError(
                "This application does not belong to the current user.")
        return application
