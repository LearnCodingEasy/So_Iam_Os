from pathlib import Path

from .models import KnowledgeFile, KnowledgeItem


# ============================================================
# KnowledgeItem Services
# ============================================================


def create_knowledge(*, user, validated_data):
    """
    Create a new KnowledgeItem for the authenticated user.
    """

    return KnowledgeItem.objects.create(
        user=user,
        **validated_data,
    )


def update_knowledge(*, knowledge, validated_data):
    """
    Update an existing KnowledgeItem.
    """

    for field, value in validated_data.items():
        setattr(
            knowledge,
            field,
            value,
        )

    knowledge.save()

    return knowledge


def archive_knowledge(*, knowledge):
    """
    Soft-delete / archive a KnowledgeItem.

    The KnowledgeItem and its attached files remain in the database,
    but the item is no longer returned by the normal API queryset.
    """

    knowledge.is_archived = True

    knowledge.save(
        update_fields=[
            "is_archived",
            "updated_at",
        ]
    )

    return knowledge


# ============================================================
# KnowledgeFile Services
# ============================================================


def detect_file_type(filename):
    """
    Detect KnowledgeFile.FileType from the uploaded filename.
    """

    extension = Path(filename).suffix.lower()

    mapping = {
        # PDF
        ".pdf": KnowledgeFile.FileType.PDF,

        # Word
        ".doc": KnowledgeFile.FileType.WORD,
        ".docx": KnowledgeFile.FileType.WORD,

        # Excel
        ".xls": KnowledgeFile.FileType.EXCEL,
        ".xlsx": KnowledgeFile.FileType.EXCEL,

        # PowerPoint
        ".ppt": KnowledgeFile.FileType.POWERPOINT,
        ".pptx": KnowledgeFile.FileType.POWERPOINT,

        # Markdown
        ".md": KnowledgeFile.FileType.MARKDOWN,

        # Text
        ".txt": KnowledgeFile.FileType.TEXT,

        # Images
        ".jpg": KnowledgeFile.FileType.IMAGE,
        ".jpeg": KnowledgeFile.FileType.IMAGE,
        ".png": KnowledgeFile.FileType.IMAGE,
        ".gif": KnowledgeFile.FileType.IMAGE,
        ".webp": KnowledgeFile.FileType.IMAGE,
        ".svg": KnowledgeFile.FileType.IMAGE,

        # Audio
        ".mp3": KnowledgeFile.FileType.AUDIO,
        ".wav": KnowledgeFile.FileType.AUDIO,
        ".ogg": KnowledgeFile.FileType.AUDIO,

        # Video
        ".mp4": KnowledgeFile.FileType.VIDEO,
        ".webm": KnowledgeFile.FileType.VIDEO,
        ".mov": KnowledgeFile.FileType.VIDEO,

        # Code
        ".py": KnowledgeFile.FileType.CODE,
        ".js": KnowledgeFile.FileType.CODE,
        ".ts": KnowledgeFile.FileType.CODE,
        ".vue": KnowledgeFile.FileType.CODE,
        ".html": KnowledgeFile.FileType.CODE,
        ".css": KnowledgeFile.FileType.CODE,
        ".scss": KnowledgeFile.FileType.CODE,
        ".json": KnowledgeFile.FileType.CODE,
        ".xml": KnowledgeFile.FileType.CODE,
        ".yaml": KnowledgeFile.FileType.CODE,
        ".yml": KnowledgeFile.FileType.CODE,
        ".sql": KnowledgeFile.FileType.CODE,
        ".sh": KnowledgeFile.FileType.CODE,
        ".bat": KnowledgeFile.FileType.CODE,
    }

    return mapping.get(
        extension,
        KnowledgeFile.FileType.OTHER,
    )


def create_knowledge_file(
    *,
    knowledge,
    uploaded_file,
    description="",
    metadata=None,
):
    """
    Create a KnowledgeFile attached to a KnowledgeItem.
    """

    if metadata is None:
        metadata = {}

    knowledge_file = KnowledgeFile.objects.create(
        knowledge=knowledge,
        file=uploaded_file,
        original_name=uploaded_file.name,
        file_type=detect_file_type(
            uploaded_file.name
        ),
        mime_type=getattr(
            uploaded_file,
            "content_type",
            "",
        ) or "",
        file_size=uploaded_file.size,
        description=description,
        metadata=metadata,
    )

    return knowledge_file


def delete_knowledge_file(*, knowledge_file):
    """
    Delete the physical file from storage
    and then delete its database record.
    """

    if knowledge_file.file:
        knowledge_file.file.delete(
            save=False
        )

    knowledge_file.delete()
