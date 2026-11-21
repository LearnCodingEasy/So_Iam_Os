from rest_framework import serializers
from learning.models import LearningSession
from learning.api.serializers.common import ensure_owner, get_request_user


# ===================================================
# Learning Session
# ===================================================


class LearningSessionSerializer(serializers.ModelSerializer):
    activity_type_display = serializers.CharField(
        source="get_activity_type_display",
        read_only=True,
    )

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = LearningSession
        fields = (
            "id",
            "user",
            "topic",
            "lesson",
            "activity_type",
            "activity_type_display",
            "started_at",
            "ended_at",
            "duration_seconds",
            "completed",
            "metadata",
        )
        read_only_fields = (
            "id",
            "user",
            "activity_type_display",
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

    def validate(self, attrs):
        topic = attrs.get(
            "topic",
            self.instance.topic if self.instance else None,
        )

        lesson = attrs.get(
            "lesson",
            self.instance.lesson if self.instance else None,
        )

        if lesson and topic:
            if lesson.topic_id != topic.id:
                raise serializers.ValidationError(
                    {
                        "lesson": (
                            "Lesson must belong to the selected topic."
                        )
                    }
                )

        started_at = attrs.get(
            "started_at",
            self.instance.started_at if self.instance else None,
        )

        ended_at = attrs.get(
            "ended_at",
            self.instance.ended_at if self.instance else None,
        )

        if started_at and ended_at and ended_at < started_at:
            raise serializers.ValidationError(
                {
                    "ended_at": (
                        "End time cannot precede start time."
                    )
                }
            )

        return attrs

    def create(self, validated_data):
        user = get_request_user(self)

        return LearningSession.objects.create(
            user=user,
            **validated_data,
        )
