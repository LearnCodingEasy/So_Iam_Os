
from django.conf import settings
from django.db import models


class KnowledgeItem(models.Model):
    """
    Represents a piece of knowledge owned by a user.

    Knowledge can be:
    - note
    - document
    - article
    - documentation
    - idea
    - project documentation
    - learning material
    - reference
    """

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

    class Visibility(models.TextChoices):
        PRIVATE = "private", "Private"
        SHARED = "shared", "Shared"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="knowledge_items",
    )
    learning_topic = models.ForeignKey(
        "learning.LearningTopic",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="knowledge_items",
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    content = models.TextField(
        blank=True,
    )

    knowledge_type = models.CharField(
        max_length=30,
        choices=KnowledgeType.choices,
        default=KnowledgeType.NOTE,
    )

    source_url = models.URLField(
        blank=True,
    )

    source_name = models.CharField(
        max_length=255,
        blank=True,
    )

    tags = models.JSONField(
        default=list,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    visibility = models.CharField(
        max_length=20,
        choices=Visibility.choices,
        default=Visibility.PRIVATE,
    )

    is_archived = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-updated_at"]

        indexes = [
            models.Index(
                fields=["user", "knowledge_type"],
            ),
            models.Index(
                fields=["user", "is_archived"],
            ),
            models.Index(
                fields=["user", "created_at"],
            ),
        ]

    def __str__(self):
        return self.title


class KnowledgeFile(models.Model):
    """
    Represents a physical file attached to a KnowledgeItem.

    A single KnowledgeItem can contain multiple files.
    """

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

    knowledge = models.ForeignKey(
        KnowledgeItem,
        on_delete=models.CASCADE,
        related_name="files",
    )

    file = models.FileField(
        upload_to="knowledge/files/%Y/%m/",
    )

    original_name = models.CharField(
        max_length=255,
    )

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

    description = models.TextField(
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["knowledge", "file_type"],
            ),
            models.Index(
                fields=["knowledge", "created_at"],
            ),
        ]

    def __str__(self):
        return self.original_name
