from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.decorators import action
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
from rest_framework.response import Response

from learning.models import LearningTopic

from .models import KnowledgeItem, KnowledgeFile
from .serializers import (
    KnowledgeItemSerializer,
    KnowledgeItemDetailSerializer,
    KnowledgeFileSerializer,
)
from .services import KnowledgeService


# ============================================================
# 🧠 Knowledge Item ViewSet
# ============================================================

class KnowledgeItemViewSet(viewsets.ModelViewSet):
    """
    Main API for KnowledgeItem.

    Every operation is scoped to the authenticated user.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    parser_classes = [
        JSONParser,
        FormParser,
        MultiPartParser,
    ]

    serializer_class = KnowledgeItemSerializer

    # ========================================================
    # 📚 Queryset
    # ========================================================

    def get_queryset(self):
        include_archived = (
            self.request.query_params
            .get(
                "include_archived",
                "false",
            )
            .lower()
            == "true"
        )

        queryset = (
            KnowledgeService
            .get_user_knowledge(
                user=self.request.user,
                include_archived=include_archived,
            )
        )

        # ----------------------------------------------------
        # Search
        # ----------------------------------------------------

        search = self.request.query_params.get(
            "search"
        )

        if search:
            queryset = (
                queryset
                .filter(
                    title__icontains=search
                )
                |
                queryset.filter(
                    description__icontains=search
                )
                |
                queryset.filter(
                    content__icontains=search
                )
            ).filter(
                user=self.request.user,
            ).distinct()

        # ----------------------------------------------------
        # Knowledge type
        # ----------------------------------------------------

        knowledge_type = (
            self.request.query_params
            .get("knowledge_type")
        )

        if knowledge_type:
            queryset = queryset.filter(
                knowledge_type=knowledge_type
            )

        # ----------------------------------------------------
        # Learning topic relation
        # ----------------------------------------------------

        learning_topic = self.request.query_params.get(
            "learning_topic"
        )

        if learning_topic:
            queryset = queryset.filter(
                learning_topics__id=learning_topic
            )

        # ----------------------------------------------------
        # Visibility
        # ----------------------------------------------------

        visibility = (
            self.request.query_params
            .get("visibility")
        )

        if visibility:
            queryset = queryset.filter(
                visibility=visibility
            )

        return queryset

    # ========================================================
    # 🎨 Serializer
    # ========================================================

    def get_serializer_class(self):
        if self.action == "retrieve":
            return KnowledgeItemDetailSerializer

        return KnowledgeItemSerializer

    # ========================================================
    # ➕ Create
    # ========================================================

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

    # ========================================================
    # ✏️ Update
    # ========================================================

    def perform_update(self, serializer):
        instance = self.get_object()

        if instance.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this knowledge item."
            )

        serializer.save()

    # ========================================================
    # 🗑️ Delete
    # ========================================================

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this knowledge item."
            )

        instance.delete()

    # ========================================================
    # 🗄️ Archive
    # ========================================================

    @action(
        detail=True,
        methods=["post"],
        url_path="archive",
    )
    def archive(self, request, pk=None):
        knowledge = self.get_object()

        knowledge = (
            KnowledgeService.archive_knowledge(
                user=request.user,
                knowledge=knowledge,
            )
        )

        serializer = self.get_serializer(
            knowledge
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # ========================================================
    # ♻️ Restore
    # ========================================================

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
    )
    def restore(self, request, pk=None):
        knowledge = self.get_object()

        knowledge = (
            KnowledgeService.restore_knowledge(
                user=request.user,
                knowledge=knowledge,
            )
        )

        serializer = self.get_serializer(
            knowledge
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # ========================================================
    # 🔗 Connect to Learning Topic
    # ========================================================

    @action(
        detail=True,
        methods=["post"],
        url_path="connect-topic",
    )
    def connect_topic(self, request, pk=None):
        knowledge = self.get_object()

        topic_id = request.data.get(
            "topic_id"
        )

        if not topic_id:
            raise ValidationError(
                {
                    "topic_id": (
                        "This field is required."
                    )
                }
            )

        try:
            topic = (
                LearningTopic.objects
                .select_related(
                    "path",
                    "path__user",
                )
                .get(
                    id=topic_id,
                )
            )
        except LearningTopic.DoesNotExist:
            raise ValidationError(
                {
                    "topic_id": (
                        "Learning topic does not exist."
                    )
                }
            )

        try:
            topic = (
                KnowledgeService
                .connect_to_topic(
                    user=request.user,
                    knowledge=knowledge,
                    topic=topic,
                )
            )
        except PermissionError as exc:
            raise PermissionDenied(
                str(exc)
            )

        return Response(
            {
                "message": (
                    "Knowledge item connected "
                    "to learning topic successfully."
                ),
                "topic_id": topic.id,
                "knowledge_item_id": knowledge.id,
            },
            status=status.HTTP_200_OK,
        )

    # ========================================================
    # 🔌 Disconnect from Topic
    # ========================================================

    @action(
        detail=True,
        methods=["post"],
        url_path="disconnect-topic",
    )
    def disconnect_topic(
        self,
        request,
        pk=None,
    ):
        knowledge = self.get_object()

        topic_id = request.data.get(
            "topic_id"
        )

        if not topic_id:
            raise ValidationError(
                {
                    "topic_id": (
                        "This field is required."
                    )
                }
            )

        try:
            topic = (
                LearningTopic.objects
                .select_related(
                    "path",
                )
                .get(
                    id=topic_id,
                    knowledge_item=knowledge,
                )
            )
        except LearningTopic.DoesNotExist:
            raise ValidationError(
                {
                    "topic_id": (
                        "This learning topic is "
                        "not connected to this knowledge item."
                    )
                }
            )

        try:
            KnowledgeService.disconnect_from_topic(
                user=request.user,
                topic=topic,
            )
        except PermissionError as exc:
            raise PermissionDenied(
                str(exc)
            )

        return Response(
            {
                "message": (
                    "Knowledge item disconnected "
                    "from learning topic successfully."
                ),
                "topic_id": topic.id,
            },
            status=status.HTTP_200_OK,
        )

    # ========================================================
    # 📎 Files
    # ========================================================

    @action(
        detail=True,
        methods=["get"],
        url_path="files",
    )
    def files(self, request, pk=None):
        knowledge = self.get_object()

        files = (
            knowledge.files
            .all()
            .order_by("-created_at")
        )

        serializer = KnowledgeFileSerializer(
            files,
            many=True,
            context={
                "request": request,
            },
        )

        return Response(
            serializer.data
        )

    # ========================================================
    # 📤 Upload File
    # ========================================================

    @action(
        detail=True,
        methods=["post"],
        url_path="upload-file",
        parser_classes=[
            MultiPartParser,
            FormParser,
        ],
    )
    def upload_file(
        self,
        request,
        pk=None,
    ):
        knowledge = self.get_object()

        uploaded_file = request.FILES.get(
            "file"
        )

        if not uploaded_file:
            raise ValidationError(
                {
                    "file": (
                        "A file is required."
                    )
                }
            )

        try:
            knowledge_file = (
                KnowledgeService.add_file(
                    user=request.user,
                    knowledge=knowledge,
                    file=uploaded_file,
                    original_name=(
                        request.data.get(
                            "original_name"
                        )
                        or uploaded_file.name
                    ),
                    file_type=(
                        request.data.get(
                            "file_type"
                        )
                        or "other"
                    ),
                    description=(
                        request.data.get(
                            "description"
                        )
                        or ""
                    ),
                )
            )

        except PermissionError as exc:
            raise PermissionDenied(
                str(exc)
            )

        from .tasks import process_knowledge_file
        process_knowledge_file.delay(knowledge_file.id)

        serializer = KnowledgeFileSerializer(
            knowledge_file,
            context={
                "request": request,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    # ========================================================
    # 🗑️ Archive All
    # ========================================================

    @action(
        detail=False,
        methods=["post"],
        url_path="archive-all",
    )
    def archive_all(
        self,
        request,
    ):
        queryset = self.get_queryset()

        updated = queryset.update(
            is_archived=True
        )

        return Response(
            {
                "message": (
                    "Knowledge items archived successfully."
                ),
                "updated": updated,
            }
        )


# ============================================================
# 📎 Knowledge File ViewSet
# ============================================================

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

    # ========================================================
    # 📚 Queryset
    # ========================================================

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

    # ========================================================
    # ➕ Create
    # ========================================================

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

    # ========================================================
    # ✏️ Update
    # ========================================================

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

    # ========================================================
    # 🗑️ Delete
    # ========================================================

    def perform_destroy(self, instance):
        if (
            instance.knowledge.user_id
            != self.request.user.id
        ):
            raise PermissionDenied(
                "You do not own this file."
            )

        instance.delete()