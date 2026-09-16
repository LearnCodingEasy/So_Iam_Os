
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from .models import KnowledgeFile, KnowledgeItem
from .serializers import KnowledgeFileSerializer, KnowledgeItemSerializer
from .services import (
    archive_knowledge,
    create_knowledge,
    create_knowledge_file,
    delete_knowledge_file,
    update_knowledge,
)

from django.core.exceptions import PermissionDenied

#
import logging

logger = logging.getLogger(__name__)

class KnowledgeItemViewSet(viewsets.ModelViewSet):
    serializer_class = KnowledgeItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logger.info("SIGNUP REQUEST | method=%s | path=%s",
            KnowledgeItem.objects
            .filter(
                user=self.request.user,
                is_archived=False,
            )
            .prefetch_related("files")
            .order_by("-updated_at") )
        logger.debug("SIGNUP DATA | keys=%s",)

        return (
            KnowledgeItem.objects
            .filter(
                user=self.request.user,
                is_archived=False,
            )
            .prefetch_related("files")
            .order_by("-updated_at")
        )

    def perform_create(self, serializer):

        learning_topic = serializer.validated_data.get(
            "learning_topic"
        )

        if learning_topic:
            if (
                learning_topic.path.user_id
                != self.request.user.id
            ):
                raise PermissionDenied(
                    "You do not own this learning topic."
                )

        create_knowledge(
            user=self.request.user,
            validated_data=serializer.validated_data,
        )
        
    

    def perform_update(self, serializer):

        learning_topic = serializer.validated_data.get(
            "learning_topic"
        )

        if learning_topic:

            if (
                learning_topic.path.user_id
                != self.request.user.id
            ):
                raise PermissionDenied(
                    "You do not own this learning topic."
                )

        update_knowledge(
            knowledge=self.get_object(),
            validated_data=serializer.validated_data,
        )

    def perform_destroy(self, instance):
        archive_knowledge(
            knowledge=instance,
        )

    @action(
        detail=True,
        methods=["get", "post"],
        url_path="files",
        parser_classes=[
            MultiPartParser,
            FormParser,
            JSONParser,
        ],
    )
    def files(self, request, pk=None):
        knowledge = self.get_object()

        if request.method == "GET":
            files = knowledge.files.all()

            serializer = KnowledgeFileSerializer(
                files,
                many=True,
                context={"request": request},
            )

            return Response(serializer.data)

        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response(
                {
                    "detail": "No file was provided."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        description = request.data.get(
            "description",
            "",
        )

        knowledge_file = create_knowledge_file(
            knowledge=knowledge,
            uploaded_file=uploaded_file,
            description=description,
        )

        serializer = KnowledgeFileSerializer(
            knowledge_file,
            context={"request": request},
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class KnowledgeFileViewSet(viewsets.GenericViewSet):
    serializer_class = KnowledgeFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    parser_classes = [
        MultiPartParser,
        FormParser,
        JSONParser,
    ]

    def get_queryset(self):
        return KnowledgeFile.objects.filter(
            knowledge__user=self.request.user,
            knowledge__is_archived=False,
        )

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            pk=self.kwargs["pk"],
        )

    def retrieve(self, request, pk=None):
        knowledge_file = self.get_object()

        serializer = self.get_serializer(
            knowledge_file,
            context={"request": request},
        )

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        knowledge_file = self.get_object()

        delete_knowledge_file(
            knowledge_file=knowledge_file,
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
