from rest_framework import serializers
from learning.models import KnowledgeApplication
from learning.api.serializers.common import ensure_owner, get_request_user


# ===================================================
# Knowledge Application
# ===================================================


class KnowledgeApplicationSerializer(
    serializers.ModelSerializer
):
    application_type_display = serializers.CharField(
        source="get_application_type_display",
        read_only=True,
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = KnowledgeApplication
        fields = (
            "id",
            "user",
            "topic",
            "lesson",
            "knowledge_item",
            "title",
            "content",
            "application_type",
            "application_type_display",
            "status",
            "status_display",
            "submitted_at",
            "reviewed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "application_type_display",
            "status_display",
            "submitted_at",
            "reviewed_at",
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
                            "Lesson must belong to "
                            "the selected topic."
                        )
                    }
                )

        return attrs

    def create(self, validated_data):
        # user = get_request_user(self)

        return KnowledgeApplication.objects.create(
            # user=user,
            **validated_data,
        )
