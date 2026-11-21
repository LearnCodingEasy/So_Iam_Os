from rest_framework import serializers
from learning.models import Lesson
from learning.api.serializers.common import ensure_owner, get_request_user


# ===================================================
# Lesson
# ===================================================


class LessonMinimalSerializer(serializers.ModelSerializer):
    content_format_display = serializers.CharField(
        source="get_content_format_display",
        read_only=True,
    )

    class Meta:
        model = Lesson
        fields = (
            "id",
            "topic",
            "title",
            "description",
            "content_format",
            "content_format_display",
            "order",
            "estimated_minutes",
            "is_active",
        )
        read_only_fields = fields


class LessonSerializer(serializers.ModelSerializer):
    content_format_display = serializers.CharField(
        source="get_content_format_display",
        read_only=True,
    )

    class Meta:
        model = Lesson
        fields = (
            "id",
            "topic",
            "title",
            "description",
            "content",
            "content_format",
            "content_format_display",
            "order",
            "estimated_minutes",
            "learning_objectives",
            "key_concepts",
            "examples",
            "practical_instructions",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "content_format_display",
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
        json_fields = (
            "learning_objectives",
            "key_concepts",
            "examples",
            "practical_instructions",
        )

        for field in json_fields:
            if field in attrs:
                value = attrs[field]

                if not isinstance(value, list):
                    raise serializers.ValidationError(
                        {
                            field: "This field must be a JSON list."
                        }
                    )

        return attrs
