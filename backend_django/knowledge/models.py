from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


# ============================================================
# 🧠 Knowledge Item
# ============================================================

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

    # ========================================================
    # 👁️ Visibility
    # ========================================================

    class Visibility(models.TextChoices):
        PRIVATE = "private", "Private"
        SHARED = "shared", "Shared"

    # ========================================================
    # 👤 Owner
    # ========================================================

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="knowledge_items",
    )

    # ========================================================
    # 📝 Basic Information
    # ========================================================

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    content = models.TextField(
        blank=True,
    )

    # ========================================================
    # 🏷️ Classification
    # ========================================================

    knowledge_type = models.CharField(
        max_length=30,
        choices=KnowledgeType.choices,
        default=KnowledgeType.NOTE,
    )

    # ========================================================
    # 🔗 Source
    # ========================================================

    source_url = models.URLField(
        blank=True,
    )

    source_name = models.CharField(
        max_length=255,
        blank=True,
    )

    # ========================================================
    # 🏷️ Tags
    # ========================================================

    tags = models.JSONField(
        default=list,
        blank=True,
    )

    # ========================================================
    # ⚙️ Metadata
    # ========================================================

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    # ========================================================
    # 👁️ Visibility
    # ========================================================

    visibility = models.CharField(
        max_length=20,
        choices=Visibility.choices,
        default=Visibility.PRIVATE,
    )

    # ========================================================
    # 📦 Archive
    # ========================================================

    is_archived = models.BooleanField(
        default=False,
    )

    # ========================================================
    # 🕒 Timestamps
    # ========================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # ========================================================
    # 🗂️ Meta
    # ========================================================

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


# ====================================================
# 📎 Knowledge File
# ====================================================

class KnowledgeFile(models.Model):
    """
    Represents a physical file attached to a KnowledgeItem.

    A single KnowledgeItem can contain multiple files.
    """

    # ========================================================
    # 📄 File Types
    # ========================================================

    class FileType(models.TextChoices):
        PDF = "pdf", "PDF"
        WORD = "word", "Word"
        EXCEL = "excel", "Excel"
        POWERPOINT = "powerpoint", "PowerPoint"
        MARKDOWN = "markdown", "Markdown"
        TEXT = "text", "Text"
        IMAGE = "image", "Image"
        AUDIO = "audio", "Audio"
        VIDEO = "video", "Video"
        CODE = "code", "Code"
        OTHER = "other", "Other"

    # ========================================================
    # 🧠 Parent Knowledge
    # ========================================================

    knowledge = models.ForeignKey(
        KnowledgeItem,
        on_delete=models.CASCADE,
        related_name="files",
    )

    # ========================================================
    # 📁 Physical File
    # ========================================================

    file = models.FileField(
        upload_to="knowledge/files/%Y/%m/",
    )

    original_name = models.CharField(
        max_length=255,
    )

    # ========================================================
    # 🏷️ File Classification
    # ========================================================

    file_type = models.CharField(
        max_length=30,
        choices=FileType.choices,
        default=FileType.OTHER,
    )

    mime_type = models.CharField(
        max_length=150,
        blank=True,
    )

    file_size = models.PositiveBigIntegerField(
        default=0,
    )

    # ========================================================
    # 📝 Description
    # ========================================================

    description = models.TextField(
        blank=True,
    )

    # ========================================================
    # ⚙️ Metadata
    # ========================================================

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class ProcessingStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    processing_status = models.CharField(
        max_length=20,
        choices=ProcessingStatus.choices,
        default=ProcessingStatus.COMPLETED,
    )
    processed_at = models.DateTimeField(null=True, blank=True)
    processing_error = models.TextField(blank=True)

    # ========================================================
    # 🕒 Timestamps
    # ========================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # ========================================================
    # 🗂️ Meta
    # ========================================================

    class Meta:
        ordering = [
            "-created_at",
        ]

        indexes = [
            models.Index(
                fields=[
                    "knowledge",
                    "file_type",
                ],
                name="knowledge_file_type_idx",
            ),

            models.Index(
                fields=[
                    "knowledge",
                    "created_at",
                ],
                name="knowledge_file_created_idx",
            ),
        ]

    # ========================================================
    # 🔤 String
    # ========================================================

    def __str__(self):
        return self.original_name

    # ========================================================
    # 🧹 Delete physical file
    # ========================================================

    def delete(self, *args, **kwargs):
        """
        Delete the database record and the physical file.
        """

        file = self.file

        super().delete(*args, **kwargs)

        if file:
            file.delete(
                save=False,
            )
