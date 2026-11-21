from rest_framework import serializers
from learning.models import LearningRevision
from learning.api.serializers.application_review_serializers import ApplicationReviewSerializer
from learning.api.serializers.common import ensure_owner, get_request_user


# ===================================================
# Learning Revision
# ===================================================


class LearningRevisionSerializer(
    serializers.ModelSerializer
):
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    source_review_detail = ApplicationReviewSerializer(
        source="source_review",
        read_only=True,
    )

    class Meta:
        model = LearningRevision
        fields = (
            "id",
            "user",
            "topic",
            "source_review",
            "source_review_detail",
            "concepts",
            "recommendation",
            "status",
            "status_display",
            "scheduled_for",
            "started_at",
            "completed_at",
            "outcome",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "source_review_detail",
            "status_display",
            "created_at",
            "updated_at",
        )

    def validate_topic(self, topic):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            topic.path,
            "topic",
        )

        return topic

    def validate_source_review(self, source_review):
        if source_review:
            user = get_request_user(self)

            if user is None:
                raise serializers.ValidationError(
                    "Authentication is required."
                )

            application = source_review.application

            ensure_owner(
                user,
                application,
                "source_review",
            )

        return source_review

    def validate(self, attrs):
        started_at = attrs.get(
            "started_at",
            self.instance.started_at
            if self.instance
            else None,
        )

        completed_at = attrs.get(
            "completed_at",
            self.instance.completed_at
            if self.instance
            else None,
        )

        if (
            started_at
            and completed_at
            and completed_at < started_at
        ):
            raise serializers.ValidationError(
                {
                    "completed_at": (
                        "Cannot precede start time."
                    )
                }
            )

        return attrs

    def create(self, validated_data):
        user = get_request_user(self)

        return LearningRevision.objects.create(
            user=user,
            **validated_data,
        )
