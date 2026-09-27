from django.db import transaction
from django.db.models import Count

from learning.models import LearningTopic

from .models import KnowledgeItem, KnowledgeFile


# ====================================================
# 🧠 Knowledge Service
# ====================================================

class KnowledgeService:
    """
    Business logic for KnowledgeItem.
    """

    # ================================================
    # 📚 Get user knowledge
    # ================================================

    @staticmethod
    def get_user_knowledge(
        *,
        user,
        include_archived=False,
    ):

        queryset = (
            KnowledgeItem.objects
            .filter(user=user)
            .select_related("user")
            .prefetch_related(
                "files",
                "learning_topics__path",
            )
            .annotate(
                files_count=Count(
                    "files",
                    distinct=True,
                ),
                annotated_learning_topics_count=Count(
                    "learning_topics",
                    distinct=True,
                ),
                annotated_learning_notes_count=Count(
                    "learning_notes",
                    distinct=True,
                ),
                annotated_learning_applications_count=Count(
                    "learning_applications",
                    distinct=True,
                ),
            )
        )

        if not include_archived:
            queryset = queryset.filter(
                is_archived=False,
            )

        return queryset

    # ================================================
    # ➕ Create
    # ================================================

    @staticmethod
    @transaction.atomic
    def create_knowledge(
        *,
        user,
        **data,
    ):
        return KnowledgeItem.objects.create(
            user=user,
            **data,
        )

    # ================================================
    # ✏️ Update
    # ================================================

    @staticmethod
    @transaction.atomic
    def update_knowledge(
        *,
        user,
        knowledge,
        **data,
    ):
        if knowledge.user_id != user.id:
            raise PermissionError(
                "You do not own this knowledge item."
            )

        for field, value in data.items():
            setattr(
                knowledge,
                field,
                value,
            )

        knowledge.save()

        return knowledge

    # ================================================
    # 🗄️ Archive
    # ================================================

    @staticmethod
    @transaction.atomic
    def archive_knowledge(
        *,
        user,
        knowledge,
    ):
        if knowledge.user_id != user.id:
            raise PermissionError(
                "You do not own this knowledge item."
            )

        knowledge.is_archived = True

        knowledge.save(
            update_fields=[
                "is_archived",
                "updated_at",
            ]
        )

        return knowledge

    # ================================================
    # ♻️ Restore
    # ================================================

    @staticmethod
    @transaction.atomic
    def restore_knowledge(
        *,
        user,
        knowledge,
    ):
        if knowledge.user_id != user.id:
            raise PermissionError(
                "You do not own this knowledge item."
            )

        knowledge.is_archived = False

        knowledge.save(
            update_fields=[
                "is_archived",
                "updated_at",
            ]
        )

        return knowledge

    # ================================================
    # 🔗 Connect Knowledge to Learning Topic
    # ================================================

    @staticmethod
    @transaction.atomic
    def connect_to_topic(
        *,
        user,
        knowledge,
        topic,
    ):
        """
        Connect a KnowledgeItem to a LearningTopic.

        Ownership:
            KnowledgeItem → current user
            LearningTopic → current user's learning path
        """

        if knowledge.user_id != user.id:
            raise PermissionError(
                "You do not own this knowledge item."
            )

        if topic.path.user_id != user.id:
            raise PermissionError(
                "You do not own this learning topic."
            )

        # ----------------------------------------------------
        # If topic already points to another knowledge item,
        # explicitly replace it.
        # ----------------------------------------------------

        topic.knowledge_item = knowledge

        topic.save(
            update_fields=[
                "knowledge_item",
                "updated_at",
            ]
        )

        return topic

    # ================================================
    # 🔌 Disconnect from Learning Topic
    # ================================================

    @staticmethod
    @transaction.atomic
    def disconnect_from_topic(
        *,
        user,
        topic,
    ):
        if topic.path.user_id != user.id:
            raise PermissionError(
                "You do not own this learning topic."
            )

        topic.knowledge_item = None

        topic.save(
            update_fields=[
                "knowledge_item",
                "updated_at",
            ]
        )

        return topic

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

        max_size = 25 * 1024 * 1024
        if getattr(file, "size", 0) > max_size:
            raise ValueError("Maximum knowledge file size is 25 MB.")

        allowed = {".md", ".markdown", ".txt", ".pdf", ".docx"}
        from pathlib import Path
        suffix = Path(file.name).suffix.lower()
        if suffix not in allowed:
            raise ValueError("Only MD, TXT, PDF and DOCX files are allowed for knowledge processing.")

        original_name = (
            original_name
            or file.name
        )

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

    # ================================================
    # 🔎 Search
    # ================================================

    @staticmethod
    def search(
        *,
        user,
        query=None,
        knowledge_type=None,
        is_archived=False,
    ):
        queryset = (
            KnowledgeItem.objects
            .filter(
                user=user,
                is_archived=is_archived,
            )
            .select_related("user")
            .prefetch_related(
                "files",
                "learning_topics__path",
            )
            .annotate(
                files_count=Count(
                    "files",
                    distinct=True,
                ),
                annotated_learning_topics_count=Count(
                    "learning_topics",
                    distinct=True,
                ),
                learning_notes_count=Count(
                    "learning_notes",
                    distinct=True,
                ),
                learning_applications_count=Count(
                    "learning_applications",
                    distinct=True,
                ),
            )
        )

        if query:
            queryset = queryset.filter(
                title__icontains=query
            ) | queryset.filter(
                description__icontains=query
            ) | queryset.filter(
                content__icontains=query
            )

            queryset = queryset.filter(
                user=user,
                is_archived=is_archived,
            )

        if knowledge_type:
            queryset = queryset.filter(
                knowledge_type=knowledge_type
            )

        return queryset.distinct()
