import logging

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import AIError
from .models import AIConversation, AIProviderCredential, AISettings, AIPromptProfile
from .permissions import AIAuthenticatedPermission
from .providers import get_ai_provider
from .serializers import (
    AIChatSerializer, AIConversationSerializer, AISettingsSerializer,
    AIProviderCredentialSerializer, AIPromptProfileSerializer,
    AILearningPlanSerializer,
)
from .services import AIService

logger = logging.getLogger(__name__)


class AIChatView(APIView):
    permission_classes = [AIAuthenticatedPermission]

    def post(self, request):
        serializer = AIChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            result = AIService(request.user).chat(
                message=data["message"], conversation_id=data.get(
                    "conversation_id"),
                provider=data.get("provider"), model=data.get("model", ""),
            )
        except AIError as exc:
            return Response({"success": False, "error": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception:
            logger.exception(
                "Unexpected AI error for user %s", request.user.pk)
            return Response({"success": False, "error": "An unexpected AI error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "success": True,
            "conversation_id": result["conversation"].id,
            "message": {"id": result["assistant_message"].id, "role": "assistant", "content": result["assistant_message"].content, "provider": result["provider"], "model": result["model"]},
            "learning": result.get("learning"),
            "learning_action": result.get("learning_action"),
        })


class AIConversationListCreateView(APIView):
    permission_classes = [AIAuthenticatedPermission]

    def get(self, request):
        qs = AIConversation.objects.filter(
            user=request.user, is_active=True).prefetch_related("messages")
        return Response(AIConversationSerializer(qs, many=True).data)

    def post(self, request):
        service = AIService(request.user)
        conversation = service.create_conversation(title=request.data.get(
            "title", ""), provider=request.data.get("provider"), model=request.data.get("model", ""))
        return Response(AIConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


class AIConversationDetailView(APIView):
    permission_classes = [AIAuthenticatedPermission]

    def get_object(self, request, pk):
        return AIConversation.objects.prefetch_related("messages").filter(pk=pk, user=request.user).first()

    def get(self, request, pk):
        conversation = self.get_object(request, pk)
        if not conversation:
            return Response({"detail": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(AIConversationSerializer(conversation).data)

    def delete(self, request, pk):
        conversation = self.get_object(request, pk)
        if not conversation:
            return Response({"detail": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)
        conversation.is_active = False
        conversation.save(update_fields=["is_active", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class AISettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        obj = AIService(request.user).get_settings()
        return Response(AISettingsSerializer(obj, context={"request": request}).data)

    def patch(self, request):
        obj = AIService(request.user).get_settings()
        serializer = AISettingsSerializer(
            obj, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AIProviderCredentialListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = AIProviderCredential.objects.filter(user=request.user)
        return Response(AIProviderCredentialSerializer(qs, many=True, context={"request": request}).data)

    def post(self, request):
        serializer = AIProviderCredentialSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AIProviderCredentialDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, provider):
        deleted, _ = AIProviderCredential.objects.filter(
            user=request.user, provider=provider).delete()
        if not deleted:
            return Response({"detail": "Credential not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AIProviderModelsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, provider):
        try:
            result = get_ai_provider(provider, user=request.user).list_models()
        except AIError as exc:
            return Response({"success": False, "error": str(exc), "provider": provider, "models": []}, status=status.HTTP_502_BAD_GATEWAY)
        return Response({"success": True, "provider": provider, "models": result})


class AIPromptProfileViewSetMixin:
    pass


class AIPromptProfileListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = AIPromptProfile.objects.filter(user=request.user)
        return Response(AIPromptProfileSerializer(qs, many=True).data)

    def post(self, request):
        serializer = AIPromptProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(user=request.user)
        if obj.is_default:
            AISettings.objects.update_or_create(user=request.user, defaults={
                                                "default_prompt_profile": obj})
        return Response(AIPromptProfileSerializer(obj).data, status=status.HTTP_201_CREATED)


class AIPromptProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return AIPromptProfile.objects.filter(pk=pk, user=request.user).first()

    def get(self, request, pk):
        obj = self.get_object(request, pk)
        if not obj:
            return Response({"detail": "Prompt profile not found."}, status=404)
        return Response(AIPromptProfileSerializer(obj).data)

    def patch(self, request, pk):
        obj = self.get_object(request, pk)
        if not obj:
            return Response({"detail": "Prompt profile not found."}, status=404)
        serializer = AIPromptProfileSerializer(
            obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        if obj.is_default:
            AISettings.objects.update_or_create(user=request.user, defaults={
                                                "default_prompt_profile": obj})
        return Response(serializer.data)

    def delete(self, request, pk):
        obj = self.get_object(request, pk)
        if not obj:
            return Response({"detail": "Prompt profile not found."}, status=404)
        obj.delete()
        return Response(status=204)


class AILearningPlanPreviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = (request.data.get("message")
                   or request.data.get("prompt") or "").strip()
        if not message:
            return Response({"detail": "message is required."}, status=400)
        try:
            plan = __import__("ai.learning_actions", fromlist=["AILearningActionService"]).AILearningActionService.generate_ai_plan(
                message=message, provider=request.data.get("provider") or AIService(
                    request.user).get_settings().preferred_provider,
                model=request.data.get("model") or AIService(request.user).get_settings().preferred_model, user=request.user,
            )
        except Exception as exc:
            return Response({"success": False, "error": str(exc)}, status=502)
        return Response({"success": True, "plan": plan})


class AILearningPlanApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AILearningPlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = AIService(request.user).approve_learning_plan(
                serializer.validated_data)
        except Exception as exc:
            logger.exception(
                "Learning plan approval failed for user %s", request.user.pk)
            return Response({"success": False, "error": str(exc)}, status=400)
        return Response({"success": True, "learning": AIService(request.user).serialize_learning_result(result)}, status=201 if result["created"] else 200)


class AILearningPlanAsyncView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = (request.data.get("message") or request.data.get("prompt") or "").strip()
        if not message:
            return Response({"detail": "message is required."}, status=400)
        from .tasks import generate_learning_plan
        task = generate_learning_plan.delay(request.user.id, message, request.data.get("provider"), request.data.get("model"))
        return Response({"task_id": task.id, "status": "pending"}, status=202)


class AITaskStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        from celery.result import AsyncResult
        result = AsyncResult(task_id)
        payload = {"task_id": task_id, "status": result.status.lower()}
        if result.successful(): payload["result"] = result.result
        if result.failed(): payload["error"] = str(result.result)
        return Response(payload)
