from rest_framework import serializers

from .models import KnowledgeFile, KnowledgeItem


class KnowledgeFileSerializer(serializers.ModelSerializer):
    """
    Serializer for files attached to a KnowledgeItem.
    """

    file_url = serializers.SerializerMethodField()

    class Meta:
        model = KnowledgeFile
        fields = [
            "id",
            "knowledge",
            "file",
            "file_url",
            "original_name",
            "file_type",
            "mime_type",
            "file_size",
            "description",
            "metadata",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "knowledge",
            "file_url",
            "original_name",
            "file_type",
            "mime_type",
            "file_size",
            "created_at",
            "updated_at",
        ]

    def get_file_url(self, obj):
        """
        Return the absolute URL of the uploaded file.
        """

        if not obj.file:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(
                obj.file.url
            )

        return obj.file.url


class KnowledgeItemSerializer(serializers.ModelSerializer):

    files = KnowledgeFileSerializer(
        many=True,
        read_only=True,
    )

    files_count = serializers.IntegerField(
        source="files.count",
        read_only=True,
    )

    class Meta:
        model = KnowledgeItem

        fields = [
            "id",
            "user",

            "learning_topic",

            "title",
            "description",
            "content",
            "knowledge_type",
            "source_url",
            "source_name",
            "tags",
            "metadata",
            "visibility",
            "is_archived",

            "files",
            "files_count",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "files",
            "files_count",
            "created_at",
            "updated_at",
        ]

    def validate_tags(self, value):

        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Tags must be a list."
            )

        return value
