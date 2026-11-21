from django.contrib.auth import get_user_model
from rest_framework import serializers

from knowledge.models import KnowledgeFile


User = get_user_model()


# ============================================================
# 📎 Knowledge File Serializer
# ============================================================

class KnowledgeFileSerializer(serializers.ModelSerializer):
    """
    Serializer for files attached to KnowledgeItem.
    """

    file_url = serializers.SerializerMethodField()
    file_size_display = serializers.SerializerMethodField()

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
            "file_size_display",
            "description",
            "metadata",
            "processing_status", "processed_at", "processing_error",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "file_url",
            "file_size",
            "created_at",
            "updated_at",
        ]

    # ================================================
    # 🔗 File URL
    # ================================================

    def get_file_url(self, obj):
        if not obj.file:
            return None

        request = self.context.get("request")

        try:
            url = obj.file.url
        except ValueError:
            return None

        if request:
            return request.build_absolute_uri(url)

        return url

    # ================================================
    # 📦 Human readable size
    # ================================================

    def get_file_size_display(self, obj):
        size = obj.file_size or 0

        if size < 1024:
            return f"{size} B"

        if size < 1024 ** 2:
            return f"{size / 1024:.1f} KB"

        if size < 1024 ** 3:
            return f"{size / (1024 ** 2):.1f} MB"

        return f"{size / (1024 ** 3):.1f} GB"

    def validate_file(self, value):
        if value:
            from knowledge.validators import validate_knowledge_upload
            try:
                validate_knowledge_upload(value)
            except ValueError as exc:
                raise serializers.ValidationError(str(exc)) from exc
        return value

    # ================================================
    # 💾 Create
    # ================================================

    def create(self, validated_data):
        uploaded_file = validated_data.get("file")

        if uploaded_file:
            if not validated_data.get("original_name"):
                validated_data["original_name"] = (
                    uploaded_file.name
                )

            if not validated_data.get("file_size"):
                validated_data["file_size"] = (
                    uploaded_file.size
                )

            if not validated_data.get("mime_type"):
                validated_data["mime_type"] = (
                    getattr(
                        uploaded_file,
                        "content_type",
                        "",
                    )
                    or ""
                )

        return super().create(
            validated_data
        )

    # ================================================
    # 🔄 Update
    # ================================================

    def update(self, instance, validated_data):
        uploaded_file = validated_data.get("file")

        if uploaded_file:
            if not validated_data.get("original_name"):
                validated_data["original_name"] = (
                    uploaded_file.name
                )

            validated_data["file_size"] = (
                uploaded_file.size
            )

            validated_data["mime_type"] = (
                getattr(
                    uploaded_file,
                    "content_type",
                    "",
                )
                or ""
            )

        return super().update(
            instance,
            validated_data,
        )
