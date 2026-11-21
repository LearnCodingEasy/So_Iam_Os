from rest_framework import serializers
from learning.models import ApplicationReview
from learning.api.serializers.application_submission_serializers import ApplicationSubmissionSerializer
from learning.api.serializers.knowledge_application_serializers import KnowledgeApplicationSerializer


# ===================================================
# Application Review
# ===================================================


class ApplicationReviewSerializer(
    serializers.ModelSerializer
):
    mastery_display = serializers.CharField(
        source="get_mastery_level_display",
        read_only=True,
    )

    submission_detail = ApplicationSubmissionSerializer(
        source="submission",
        read_only=True,
    )

    application_detail = KnowledgeApplicationSerializer(
        source="application",
        read_only=True,
    )

    class Meta:
        model = ApplicationReview
        fields = (
            "id",
            "submission",
            "submission_detail",
            "application",
            "application_detail",
            "score",
            "mastery_level",
            "mastery_display",
            "understood",
            "applied",
            "strengths",
            "weaknesses",
            "errors",
            "needs_review",
            "knowledge_gaps",
            "recommendations",
            "feedback",
            "ai_metadata",
            "reviewed_by",
            "reviewed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "mastery_display",
            "submission_detail",
            "application_detail",
            "reviewed_at",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        submission = attrs.get(
            "submission",
            self.instance.submission
            if self.instance
            else None,
        )

        application = attrs.get(
            "application",
            self.instance.application
            if self.instance
            else None,
        )

        if submission and application:
            if (
                submission.application_id
                != application.id
            ):
                raise serializers.ValidationError(
                    {
                        "application": (
                            "Application must match "
                            "the submission's application."
                        )
                    }
                )

        return attrs
