from django.db import transaction


from knowledge.models import KnowledgeFile


# ====================================================
# 📎 Knowledge File Service
# ====================================================

class KnowledgeFileService:
    """
    Business logic for KnowledgeFile.
    """

    # ================================================
    # 📎 Add File
    # ================================================

    @staticmethod
    @transaction.atomic
    def add_file(
        *,
        user,
        knowledge,
        file,
        original_name=None,
        file_type="other",
        mime_type="",
        description="",
        metadata=None,
    ):
        if knowledge.user_id != user.id:
            raise PermissionError(
                "You do not own this knowledge item."
            )

        if not file:
            raise ValueError("A file is required.")

        from pathlib import Path
        from knowledge.validators import validate_knowledge_upload

        validate_knowledge_upload(file)
        # Keep only a display basename; never persist client-supplied path segments.
        original_name = Path(str(original_name or file.name).replace("\\", "/")).name[:255]

        file_size = (
            getattr(
                file,
                "size",
                0,
            )
            or 0
        )

        mime_type = (
            mime_type
            or getattr(
                file,
                "content_type",
                "",
            )
            or ""
        )

        knowledge_file = (
            KnowledgeFile.objects.create(
                knowledge=knowledge,
                file=file,
                original_name=original_name,
                file_type=file_type,
                mime_type=mime_type,
                file_size=file_size,
                description=description,
                metadata=metadata or {},
            )
        )

        return knowledge_file

    # ================================================
    # 🗑️ Delete File
    # ================================================

    @staticmethod
    @transaction.atomic
    def delete_file(
        *,
        user,
        knowledge_file,
    ):
        if knowledge_file.knowledge.user_id != user.id:
            raise PermissionError(
                "You do not own this file."
            )

        knowledge_file.delete()
