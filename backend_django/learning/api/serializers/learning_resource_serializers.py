from rest_framework import serializers
from learning.models import LearningResource
from learning.api.serializers.common import ensure_owner, get_request_user


# ===================================================
# Learning Resource
# ===================================================


class LearningResourceSerializer(serializers.ModelSerializer):
    reference_type_display = serializers.CharField(
        source="get_reference_type_display",
        read_only=True,
    )

    file_url = serializers.SerializerMethodField()

    class Meta:
        model = LearningResource
        fields = (
            "id",
            "topic",
            "lesson",
            "title",
            "description",
            "reference_type",
            "reference_type_display",
            "url",
            "file",
            "file_url",
            "content",
            "caption",
            "order",
            "created_at",
        )
        read_only_fields = (
            "id",
            "reference_type_display",
            "file_url",
            "created_at",
        )

    def get_file_url(self, obj):
        if not obj.file:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(
                obj.file.url
            )

        return obj.file.url

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

        reference_type = attrs.get(
            "reference_type",
            (
                self.instance.reference_type
                if self.instance
                else LearningResource.ResourceType.WEBSITE
            ),
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

        if reference_type == LearningResource.ResourceType.FILE:
            file = attrs.get(
                "file",
                self.instance.file if self.instance else None,
            )

            if not file:
                raise serializers.ValidationError(
                    {
                        "file": (
                            "A file is required for file resources."
                        )
                    }
                )

        url_required_types = {
            LearningResource.ResourceType.WEBSITE,
            LearningResource.ResourceType.DOCUMENTATION,
            LearningResource.ResourceType.ARTICLE,
            LearningResource.ResourceType.VIDEO,
        }

        if reference_type in url_required_types:
            url = attrs.get(
                "url",
                self.instance.url if self.instance else "",
            )

            if not url:
                raise serializers.ValidationError(
                    {
                        "url": (
                            "A URL is required for this resource type."
                        )
                    }
                )

        return attrs
