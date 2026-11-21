from django.conf import settings
from django.db import models


# ====================================================
# 🧠 Knowledge Item
# ====================================================

class KnowledgeItem(models.Model):
    """
    Represents a piece of knowledge owned by a user.

    Knowledge can be connected to the Learning system through
    LearningTopic. The relationship is intentionally owned by
    LearningTopic:

        KnowledgeItem
            ↑
            │
        LearningTopic

    This allows the same knowledge item to be reused by
    multiple learning topics when needed.
    """

    # ========================================================
    # 📚 Knowledge Types
    # ========================================================

    class KnowledgeType(models.TextChoices):
        NOTE = "note", "Note"
        DOCUMENT = "document", "Document"
        ARTICLE = "article", "Article"
        DOCUMENTATION = "documentation", "Documentation"
        IDEA = "idea", "Idea"
        PROJECT = "project", "Project"
        LEARNING = "learning", "Learning"
        REFERENCE = "reference", "Reference"
        OTHER = "other", "Other"

    # ================================================
    # 👁️ Visibility
    # ================================================

    class Visibility(models.TextChoices):
        PRIVATE = "private", "Private"
        SHARED = "shared", "Shared"

    # ================================================
    # 👤 Owner
    # ================================================

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="knowledge_items",
    )

    # ================================================
    # 📝 Basic Information
    # ================================================

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    content = models.TextField(
        blank=True,
    )

    # ================================================
    # 🏷️ Classification
    # ================================================

    knowledge_type = models.CharField(
        max_length=30,
        choices=KnowledgeType.choices,
        default=KnowledgeType.NOTE,
    )

    # ================================================
    # 🔗 Source
    # ================================================

    source_url = models.URLField(
        blank=True,
    )

    source_name = models.CharField(
        max_length=255,
        blank=True,
    )

    # ================================================
    # 🏷️ Tags
    # ================================================

    tags = models.JSONField(
        default=list,
        blank=True,
    )

    # ================================================
    # ⚙️ Metadata
    # ================================================

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    # ================================================
    # 👁️ Visibility
    # ================================================

    visibility = models.CharField(
        max_length=20,
        choices=Visibility.choices,
        default=Visibility.PRIVATE,
    )

    # ================================================
    # 📦 Archive
    # ================================================

    is_archived = models.BooleanField(
        default=False,
    )

    # ================================================
    # 🕒 Timestamps
    # ================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # ================================================
    # 🗂️ Meta
    # ================================================

    class Meta:
        ordering = [
            "-updated_at",
        ]

        indexes = [
            models.Index(
                fields=[
                    "user",
                    "knowledge_type",
                ],
                name="knowledge_user_type_idx",
            ),

            models.Index(
                fields=[
                    "user",
                    "is_archived",
                ],
                name="knowledge_user_archived_idx",
            ),

            models.Index(
                fields=[
                    "user",
                    "created_at",
                ],
                name="knowledge_user_created_idx",
            ),

            models.Index(
                fields=[
                    "user",
                    "updated_at",
                ],
                name="knowledge_user_updated_idx",
            ),
        ]

    # ================================================
    # 🔤 String
    # ================================================

    def __str__(self):
        return self.title

    # ================================================
    # 🧠 Learning Integration
    # ================================================

    @property
    def learning_topics_count(self):
        """
        Number of learning topics using this knowledge item.
        """

        return self.learning_topics.count()

    @property
    def learning_notes_count(self):
        """
        Number of learning notes connected to this knowledge item.
        """

        return self.learning_notes.count()

    @property
    def learning_applications_count(self):
        """
        Number of practical learning applications connected
        to this knowledge item.
        """

        return self.learning_applications.count()
