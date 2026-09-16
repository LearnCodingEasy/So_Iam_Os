import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import AIError
from .models import AIConversation
from .permissions import AIAuthenticatedPermission
from .serializers import (
    AIChatSerializer,
    AIConversationSerializer,
)
from .services import AIService


logger = logging.getLogger(__name__)


class AIChatView(APIView):
    permission_classes = [
        AIAuthenticatedPermission,
    ]

    def post(self, request):
        serializer = AIChatSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        data = serializer.validated_data

        try:
            service = AIService(
                user=request.user
            )

            result = service.chat(
                message=data["message"],
                conversation_id=data.get(
                    "conversation_id"
                ),
                provider=data.get(
                    "provider"
                ),
                model=data.get(
                    "model",
                    "",
                ),
            )

        except AIError as exc:
            logger.warning(
                "AI error for user %s: %s",
                request.user.pk,
                exc,
            )

            return Response(
                {
                    "success": False,
                    "error": str(exc),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        except Exception:
            logger.exception(
                "Unexpected AI error for user %s",
                request.user.pk,
            )

            return Response(
                {
                    "success": False,
                    "error": "An unexpected AI error occurred.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "success": True,
                "conversation_id": result["conversation"].id,

                "message": {
                    "id": result["assistant_message"].id,
                    "role": "assistant",
                    "content": result["assistant_message"].content,
                    "provider": result["provider"],
                    "model": result["model"],
                },

                "learning": result.get("learning"),

                "learning_action": result.get(
                    "learning_action"
                ),
            },
            status=status.HTTP_200_OK,
        )


class AIConversationListCreateView(APIView):
    permission_classes = [
        AIAuthenticatedPermission,
    ]

    def get(self, request):
        conversations = (
            AIConversation.objects
            .filter(
                user=request.user,
                is_active=True,
            )
            .prefetch_related("messages")
        )

        serializer = AIConversationSerializer(
            conversations,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        service = AIService(
            user=request.user
        )

        conversation = service.create_conversation(
            title=request.data.get(
                "title",
                "",
            ),
            provider=request.data.get(
                "provider"
            ),
            model=request.data.get(
                "model",
                "",
            ),
        )

        serializer = AIConversationSerializer(
            conversation
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class AIConversationDetailView(APIView):
    permission_classes = [
        AIAuthenticatedPermission,
    ]

    def get(self, request, pk):
        try:
            conversation = (
                AIConversation.objects
                .prefetch_related("messages")
                .get(
                    pk=pk,
                    user=request.user,
                )
            )
        except AIConversation.DoesNotExist:
            return Response(
                {
                    "detail": "Conversation not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AIConversationSerializer(
            conversation
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        try:
            conversation = (
                AIConversation.objects.get(
                    pk=pk,
                    user=request.user,
                )
            )
        except AIConversation.DoesNotExist:
            return Response(
                {
                    "detail": "Conversation not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        conversation.is_active = False
        conversation.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
