from rest_framework import serializers
from learning.models import LearningProgress
from learning.api.serializers.common import ensure_owner, get_request_user


# ===================================================
# Learning Progress
# ===================================================


class LearningProgressSerializer(serializers.ModelSerializer):
    mastery_display = serializers.CharField(
        source="get_mastery_level_display",
        read_only=True,
    )

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = LearningProgress
        fields = (
            "id",
            "user",
            "topic",
            "progress_percent",
            "practice_completed",
            "notes",
            "mastery_level",
            "mastery_display",
            "last_ai_score",
            "needs_review",
            "lesson_completed",
            "quick_check_completed",
            "assessment_completed",
            "last_activity_at",
            "completed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "last_ai_score",
            "needs_review",
            "last_activity_at",
            "completed_at",
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

    def create(self, validated_data):
        user = get_request_user(self)

        return LearningProgress.objects.create(
            user=user,
            **validated_data,
        )
