from django.db import models

from .knowledge_item import KnowledgeItem


# ====================================================
# 📎 Knowledge File
# ====================================================

class KnowledgeFile(models.Model):
    """
    Represents a physical file attached to a KnowledgeItem.

    A single KnowledgeItem can contain multiple files.
    """

    # ================================================
    # 📄 File Types
    # ================================================

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

    # ================================================
    # 🧠 Parent Knowledge
    # ================================================

    knowledge = models.ForeignKey(
        KnowledgeItem,
        on_delete=models.CASCADE,
        related_name="files",
    )

    # ================================================
    # 📁 Physical File
    # ================================================

    file = models.FileField(
        upload_to="knowledge/files/%Y/%m/",
    )

    original_name = models.CharField(
        max_length=255,
    )

    # ================================================
    # 🏷️ File Classification
    # ================================================

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

    # ================================================
    # 📝 Description
    # ================================================

    description = models.TextField(
        blank=True,
    )

    # ================================================
    # ⚙️ Metadata
    # ================================================

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

    # ================================================
    # 🔤 String
    # ================================================

    def __str__(self):
        return self.original_name

    # ================================================
    # 🧹 Delete physical file
    # ================================================

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
