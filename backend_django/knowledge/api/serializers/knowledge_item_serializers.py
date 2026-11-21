from django.contrib.auth import get_user_model
from rest_framework import serializers

from knowledge.models import KnowledgeItem


User = get_user_model()


from .knowledge_file_serializers import KnowledgeFileSerializer


# ====================================================
# 🧠 Knowledge Item Serializer
# ====================================================

class KnowledgeItemSerializer(serializers.ModelSerializer):
    """
    Main serializer for KnowledgeItem.

    Designed for the Vue learning/knowledge UI.
    """

    files = KnowledgeFileSerializer(
        many=True,
        read_only=True,
    )

    files_count = serializers.SerializerMethodField()

    learning_topics = serializers.SerializerMethodField()

    learning_topics_count = serializers.SerializerMethodField()

    learning_notes_count = serializers.SerializerMethodField()

    learning_applications_count = (
        serializers.SerializerMethodField()
    )

    class Meta:
        model = KnowledgeItem

        fields = [
            "id",
            "user",
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

            # Files
            "files",
            "files_count",

            # Learning integration
            "learning_topics",
            "learning_topics_count",
            "learning_notes_count",
            "learning_applications_count",

            # Timestamps
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "files",
            "files_count",
            "learning_topics",
            "learning_topics_count",
            "learning_notes_count",
            "learning_applications_count",
            "created_at",
            "updated_at",
        ]

    # ================================================
    # 📎 Files count
    # ================================================

    def get_files_count(self, obj):
        return getattr(
            obj,
            "files_count",
            None,
        ) or obj.files.count()

    # ================================================
    # 📚 Learning topics
    # ================================================

    def get_learning_topics(self, obj):
        """
        Return lightweight learning topic information.

        We intentionally do not import LearningTopicSerializer
        here to avoid circular imports between knowledge and
        learning serializers.
        """

        topics = obj.learning_topics.all()

        return [
            {
                "id": topic.id,
                "title": topic.title,
                "status": topic.status,
                "order": topic.order,
                "path_id": topic.path_id,
                "path_title": (
                    topic.path.title
                    if getattr(topic, "path", None)
                    else None
                ),
            }
            for topic in topics
        ]

    # ================================================
    # 📊 Learning topics count
    # ================================================

    def get_learning_topics_count(self, obj):
        annotated = getattr(
            obj,
            "annotated_learning_topics_count",
            None,
        )

        if annotated is not None:
            return annotated

        return obj.learning_topics.count()

    # ================================================
    # 📝 Learning notes count
    # ================================================

    def get_learning_notes_count(self, obj):
        annotated = getattr(
            obj,
            "annotated_learning_notes_count",
            None,
        )

        if annotated is not None:
            return annotated

        return obj.learning_notes.count()

    # ================================================
    # 🛠️ Applications count
    # ================================================

    def get_learning_applications_count(self, obj):
        annotated = getattr(
            obj,
            "annotated_learning_applications_count",
            None,
        )

        if annotated is not None:
            return annotated

        return obj.learning_applications.count()

    # ================================================
    # 🔐 Ownership
    # ================================================

    def validate(self, attrs):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        return attrs


# ====================================================
# 🧠 Knowledge Detail Serializer
# ====================================================

class KnowledgeItemDetailSerializer(
    KnowledgeItemSerializer
):
    """
    Detailed serializer.

    Used when opening a single knowledge item.
    """

    class Meta(KnowledgeItemSerializer.Meta):
        fields = KnowledgeItemSerializer.Meta.fields
