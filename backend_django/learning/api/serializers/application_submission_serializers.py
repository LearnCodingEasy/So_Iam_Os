from rest_framework import serializers
from learning.models import ApplicationSubmission
from learning.api.serializers.common import ensure_owner, get_request_user
from learning.api.serializers.knowledge_application_serializers import KnowledgeApplicationSerializer


# ===================================================
# Application Submission
# ===================================================


class ApplicationSubmissionSerializer(
    serializers.ModelSerializer
):
    application_detail = KnowledgeApplicationSerializer(
        source="application",
        read_only=True,
    )

    class Meta:
        model = ApplicationSubmission
        fields = (
            "id",
            "application",
            "application_detail",
            "version",
            "title",
            "content",
            "submitted_at",
        )
        read_only_fields = (
            "id",
            "version",
            "submitted_at",
        )

    def validate_application(self, application):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            application,
            "application",
        )

        return application

    def create(self, validated_data):
        application = validated_data["application"]

        last_submission = (
            ApplicationSubmission.objects
            .filter(application=application)
            .order_by("-version")
            .first()
        )

        next_version = (
            last_submission.version + 1
            if last_submission
            else 1
        )

        return ApplicationSubmission.objects.create(
            version=next_version,
            **validated_data,
        )
