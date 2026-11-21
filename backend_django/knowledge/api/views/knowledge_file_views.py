from rest_framework import viewsets
from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError,
)
from rest_framework.parsers import (
    JSONParser,
    FormParser,
    MultiPartParser,
)
from rest_framework.permissions import IsAuthenticated



from knowledge.api.serializers import (
    KnowledgeFileSerializer,
)
from knowledge.models import KnowledgeFile


# ====================================================
# 📎 Knowledge File ViewSet
# ====================================================

class KnowledgeFileViewSet(viewsets.ModelViewSet):
    """
    API for KnowledgeFile.

    Files are always scoped through their KnowledgeItem owner.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    parser_classes = [
        MultiPartParser,
        FormParser,
        JSONParser,
    ]

    serializer_class = KnowledgeFileSerializer

    # ================================================
    # 📚 Queryset
    # ================================================

    def get_queryset(self):
        return (
            KnowledgeFile.objects
            .filter(
                knowledge__user=self.request.user,
            )
            .select_related(
                "knowledge",
            )
            .order_by(
                "-created_at"
            )
        )

    # ================================================
    # ➕ Create
    # ================================================

    def perform_create(self, serializer):
        knowledge = serializer.validated_data.get(
            "knowledge"
        )

        if not knowledge:
            raise ValidationError(
                {
                    "knowledge": (
                        "Knowledge item is required."
                    )
                }
            )

        if knowledge.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this knowledge item."
            )

        uploaded_file = (
            serializer.validated_data.get(
                "file"
            )
        )

        if uploaded_file:
            if not serializer.validated_data.get(
                "original_name"
            ):
                serializer.validated_data[
                    "original_name"
                ] = uploaded_file.name

            serializer.validated_data[
                "file_size"
            ] = uploaded_file.size

            serializer.validated_data[
                "mime_type"
            ] = (
                getattr(
                    uploaded_file,
                    "content_type",
                    "",
                )
                or ""
            )

        serializer.save()

    # ================================================
    # ✏️ Update
    # ================================================

    def perform_update(self, serializer):
        instance = self.get_object()

        if (
            instance.knowledge.user_id
            != self.request.user.id
        ):
            raise PermissionDenied(
                "You do not own this file."
            )

        serializer.save()

    # ================================================
    # 🗑️ Delete
    # ================================================

    def perform_destroy(self, instance):
        if (
            instance.knowledge.user_id
            != self.request.user.id
        ):
            raise PermissionDenied(
                "You do not own this file."
            )

        instance.delete()
