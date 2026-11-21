import logging
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.db import transaction
from ai.exceptions import AIError
from ai.models import AIConversation, AIProviderCredential, AISettings, AIPromptProfile, AIExecution, AIBudgetPolicy, AIWorkflowDefinition, AIWorkflowRun
from learning.models import LearningTopic, LearningProgress
from ai.permissions import AIAuthenticatedPermission
from ai.providers import get_ai_provider
from ai.api.serializers import AIChatSerializer, AIConversationSerializer, AISettingsSerializer, AIProviderCredentialSerializer, AIProviderTestSerializer, AIPromptProfileSerializer, AIWorkflowDefinitionSerializer, AILearningPlanSerializer, AIExecutionSerializer, AIBudgetPolicySerializer, AiAuditLogSerializer, AIFeedbackSerializer
from ai.services import AIService


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
                idempotency_key=data.get("idempotency_key") or request.headers.get(
                    "Idempotency-Key", ""),
                system_prompt=data.get("system_prompt", ""),
                temperature=data.get("temperature"),
                max_tokens=data.get("max_tokens"),
            )
        except AIError as exc:
            error_code = getattr(exc, "category", "ai_error")
            response_status = (
                status.HTTP_409_CONFLICT
                if error_code in {"request_in_progress", "previous_attempt_failed", "idempotency_result_unavailable"}
                else status.HTTP_502_BAD_GATEWAY
            )
            return Response({
                "success": False,
                "error": str(exc),
                "error_code": error_code,
                "retryable": bool(getattr(exc, "retryable", False)),
                "provider_status": getattr(exc, "status_code", None),
            }, status=response_status)
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
            user=request.user, is_active=True, deleted_at__isnull=True).prefetch_related("messages")
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

    def post(self, request, pk):
        action = request.data.get("action", "")
        conversation = self.get_object(request, pk)
        if not conversation:
            return Response({"detail": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)
        from django.utils import timezone
        if action == "archive":
            conversation.archived_at = timezone.now()
            conversation.is_active = False
        elif action == "restore":
            conversation.archived_at = None
            conversation.deleted_at = None
            conversation.is_active = True
        elif action == "delete":
            conversation.deleted_at = timezone.now()
            conversation.is_active = False
        else:
            return Response({"detail": "action must be archive, restore, or delete."}, status=status.HTTP_400_BAD_REQUEST)
        conversation.save(
            update_fields=["archived_at", "deleted_at", "is_active", "updated_at"])
        return Response(AIConversationSerializer(conversation).data)


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
        # DELETE is idempotent: a retry after a successful deletion must not
        # turn a successful client operation into a misleading 404.
        AIProviderCredential.objects.filter(
            user=request.user, provider=provider
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AIProviderModelsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, provider):
        try:
            result = get_ai_provider(provider, user=request.user).list_models()
        except AIError as exc:
            return Response({
                "success": False,
                "error": str(exc),
                "error_code": getattr(exc, "category", "ai_error"),
                "retryable": bool(getattr(exc, "retryable", False)),
                "provider_status": getattr(exc, "status_code", None),
                "provider": provider,
                "models": [],
            }, status=status.HTTP_502_BAD_GATEWAY)
        return Response({"success": True, "provider": provider, "models": result})


class AIProviderTestView(APIView):
    """Verify both provider connectivity and an actual model generation."""
    permission_classes = [IsAuthenticated]

    def post(self, request, provider):
        serializer = AIProviderTestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        selected_model = serializer.validated_data.get("model") or None
        try:
            provider_obj = get_ai_provider(provider, user=request.user)
            result = provider_obj.generate(
                messages=[{
                    "role": "user",
                    "content": "Reply with exactly: OK",
                }],
                model=selected_model,
                max_tokens=8,
                timeout_seconds=max(
                    3,
                    min(60, int(getattr(
                        settings, "AI_PROVIDER_TEST_TIMEOUT_SECONDS", 20
                    ))),
                ),
            )
            generated_text = str((result or {}).get("content") or "").strip()
            if not generated_text:
                raise AIError("The provider returned an empty test response.")
            from django.utils import timezone
            AIProviderCredential.objects.filter(
                user=request.user, provider=provider
            ).update(status="valid", last_validated_at=timezone.now())
            return Response({
                "success": True,
                "provider": provider,
                "connected": True,
                "generation_verified": True,
                "model": (result or {}).get("model") or selected_model or "",
                "response_preview": generated_text[:120],
            })
        except AIError as exc:
            from django.utils import timezone
            AIProviderCredential.objects.filter(
                user=request.user, provider=provider
            ).update(status="invalid", last_validated_at=timezone.now())
            return Response({
                "success": False,
                "provider": provider,
                "connected": False,
                "generation_verified": False,
                "error": str(exc),
                "error_code": getattr(exc, "category", "ai_error"),
                "retryable": bool(getattr(exc, "retryable", False)),
                "provider_status": getattr(exc, "status_code", None),
                "model": selected_model or "",
            }, status=status.HTTP_502_BAD_GATEWAY)
        except Exception:
            logger.exception(
                "AI provider generation test failed for provider %s", provider)
            return Response({
                "success": False,
                "provider": provider,
                "connected": False,
                "generation_verified": False,
                "error": "Provider test failed unexpectedly.",
                "error_code": "provider_test_error",
                "retryable": False,
                "model": selected_model or "",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AIProviderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from ai.services.provider_manager import ProviderManager
        return Response({"providers": ProviderManager.list_for_user(request.user)})


class AIExecutionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = AIExecution.objects.filter(
            user=request.user).order_by("-created_at")[:200]
        return Response(AIExecutionSerializer(qs, many=True).data)


class AIBudgetListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = AIBudgetPolicy.objects.filter(
            user=request.user).order_by("scope", "scope_key")
        return Response(AIBudgetPolicySerializer(qs, many=True).data)

    def post(self, request):
        serializer = AIBudgetPolicySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj, _ = AIBudgetPolicy.objects.update_or_create(
            user=request.user,
            scope=serializer.validated_data["scope"],
            scope_key=serializer.validated_data.get("scope_key", ""),
            defaults=serializer.validated_data,
        )
        return Response(AIBudgetPolicySerializer(obj).data, status=status.HTTP_200_OK)


class AIAuditListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from ai.models import AiAuditLog
        queryset = AiAuditLog.objects.filter(user=request.user).order_by("-created_at")[:500]
        return Response(AiAuditLogSerializer(queryset, many=True).data)


class AIFeedbackView(APIView):
    """Persist feedback only for assistant messages owned by the requester."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AIFeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        from ai.services.feedback_service import FeedbackService
        data = serializer.validated_data
        try:
            feedback = FeedbackService.upsert(
                user=request.user,
                message_id=data["message_id"],
                sentiment=data["sentiment"],
                reason=data.get("reason", ""),
                comment=data.get("comment", ""),
                feedback_category=data.get("feedback_category", ""),
                rating=data.get("rating"),
            )
        except ValueError:
            return Response({"detail": "Assistant message not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "id": feedback.pk,
            "message_id": feedback.message_id,
            "sentiment": feedback.sentiment,
            "reason": feedback.reason,
            "comment": feedback.comment,
            "created_at": feedback.created_at,
        }, status=status.HTTP_200_OK)


class AIBudgetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return AIBudgetPolicy.objects.filter(user=request.user, pk=pk).first()

    def patch(self, request, pk):
        obj = self.get_object(request, pk)
        if obj is None:
            return Response({"detail": "Budget policy not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AIBudgetPolicySerializer(
            obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        obj = self.get_object(request, pk)
        if obj is not None:
            obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AIWorkflowListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = AIWorkflowDefinition.objects.filter(
            user=request.user).order_by("-updated_at")
        return Response(AIWorkflowDefinitionSerializer(qs, many=True).data)

    def post(self, request):
        serializer = AIWorkflowDefinitionSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data["name"]
        latest_version = AIWorkflowDefinition.objects.filter(
            user=request.user, name=name
        ).order_by("-version").values_list("version", flat=True).first() or 0
        obj = serializer.save(user=request.user, version=latest_version + 1)
        return Response(AIWorkflowDefinitionSerializer(obj).data, status=status.HTTP_201_CREATED)


class AIWorkflowDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return AIWorkflowDefinition.objects.filter(user=request.user, pk=pk).first()

    def get(self, request, pk):
        obj = self.get_object(request, pk)
        if obj is None:
            return Response({"detail": "Workflow not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(AIWorkflowDefinitionSerializer(obj).data)

    def patch(self, request, pk):
        obj = self.get_object(request, pk)
        if obj is None:
            return Response({"detail": "Workflow not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AIWorkflowDefinitionSerializer(
            obj, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        obj = self.get_object(request, pk)
        if obj is not None:
            obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AIWorkflowRunsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        workflow = AIWorkflowDefinition.objects.filter(
            user=request.user, pk=pk).first()
        if workflow is None:
            return Response({"detail": "Workflow not found."}, status=status.HTTP_404_NOT_FOUND)
        runs = AIWorkflowRun.objects.filter(
            user=request.user, workflow=workflow).order_by("-created_at")[:100]
        return Response([{
            "id": run.pk, "status": run.status, "input_data": run.input_data,
            "output_data": run.output_data, "error": run.error,
            "started_at": run.started_at, "finished_at": run.finished_at,
            "created_at": run.created_at,
        } for run in runs])


class AIUsageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from ai.services.usage_service import UsageService
        return Response(UsageService.summarize(user=request.user))


class AIContextInspectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        from ai.services.context_inspector import ContextInspector
        result = ContextInspector.inspect_conversation(
            user=request.user, conversation_id=pk)
        if result is None:
            return Response({"detail": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(result)


class AIWorkflowValidateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from ai.services.workflow_service import WorkflowService
        result = WorkflowService.validate(request.data)
        return Response(result, status=status.HTTP_200_OK if result.get("valid") else status.HTTP_400_BAD_REQUEST)


class AITaskProposalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from ai.services.task_planner import TaskPlanner
        try:
            proposal = TaskPlanner.proposal(
                title=request.data.get("title", ""),
                description=request.data.get("description", ""),
                steps=request.data.get("steps") or [],
                priority=request.data.get("priority", "medium"),
                due_date=request.data.get("due_date"),
            )
        except (TypeError, ValueError) as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(proposal, status=status.HTTP_200_OK)


class AIAgentSelectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from ai.services.agent_selector import AgentSelector
        try:
            selection = AgentSelector.select(
                user=request.user,
                message=request.data.get("message", ""),
                provider=request.data.get("provider"),
                model=request.data.get("model"),
                task_type=request.data.get("task_type", "chat"),
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "provider": selection.provider,
            "model": selection.model,
            "reason": selection.reason,
        })


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
            AIPromptProfile.objects.filter(user=request.user).exclude(
                pk=obj.pk).update(is_default=False)
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
            AIPromptProfile.objects.filter(user=request.user).exclude(
                pk=obj.pk).update(is_default=False)
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
        message = (request.data.get("message")
                   or request.data.get("prompt") or "").strip()
        if not message:
            return Response({"detail": "message is required."}, status=400)
        from uuid import uuid4
        from ai.tasks import generate_learning_plan
        from ai.models import AiAuditLog

        task_id = str(uuid4())
        # Create the ownership record before dispatch so a fast worker cannot
        # race the first status poll while the Celery state is still PENDING.
        ownership_record = AiAuditLog.objects.create(
            user=request.user,
            action="learning_async_submitted",
            resource=task_id,
            details={"task_id": task_id, "status": "pending"},
        )
        try:
            generate_learning_plan.apply_async(
                args=(
                    request.user.id,
                    message,
                    request.data.get("provider"),
                    request.data.get("model"),
                ),
                task_id=task_id,
            )
        except Exception:
            ownership_record.delete()
            logger.exception("Could not enqueue AI learning task for user %s", request.user.pk)
            return Response(
                {"detail": "AI learning task could not be queued."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        return Response({"task_id": task_id, "status": "pending"}, status=202)


class AITaskStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        from celery.result import AsyncResult
        from ai.tasks import generate_learning_plan

        result = AsyncResult(task_id, app=generate_learning_plan.app)
        info = result.info
        owner_id = info.get("user_id") if isinstance(info, dict) else None
        if owner_id is not None:
            owned = str(owner_id) == str(request.user.id)
        else:
            # A PENDING task has no result metadata yet. Verify its owner via
            # the submission audit row rather than exposing task existence.
            from ai.models import AiAuditLog
            owned = AiAuditLog.objects.filter(
                user=request.user,
                action="learning_async_submitted",
                resource=str(task_id),
            ).exists()
        if not owned:
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        payload = {"task_id": task_id, "status": result.status.lower()}
        if result.successful():
            payload["result"] = info.get("result") if isinstance(
                info, dict) else result.result
        elif result.failed():
            payload["error"] = "AI task failed."
        return Response(payload)


class AITopicChatView(APIView):
    permission_classes = [AIAuthenticatedPermission]

    def post(self, request):
        topic_id = request.data.get("topic_id")
        message = (request.data.get("message") or "").strip()
        if not topic_id or not message:
            return Response({"detail": "topic_id and message are required."}, status=400)
        topic = LearningTopic.objects.select_related("path__goal", "path__goal__skill", "skill", "knowledge_item").filter(
            id=topic_id, path__user=request.user).first()
        if not topic:
            return Response({"detail": "Topic not found."}, status=404)
        progress = LearningProgress.objects.filter(
            user=request.user, topic=topic).first()
        knowledge = topic.knowledge_item
        context = {
            "topic": {"id": topic.id, "title": topic.title, "description": topic.description, "difficulty": topic.difficulty},
            "goal": {"title": topic.path.goal.title, "current_level": topic.path.goal.current_level, "target_level": topic.path.goal.target_level},
            "skill": topic.skill.name if topic.skill else None,
            "progress": {"progress_percent": progress.progress_percent, "mastery_level": progress.mastery_level} if progress else None,
            "knowledge": {"title": knowledge.title, "content": (knowledge.content or "")[:16000]} if knowledge else None,
        }
        conversation_id = request.data.get("conversation_id")
        if conversation_id:
            conversation = AIConversation.objects.filter(
                id=conversation_id, user=request.user, is_active=True).first()
        else:
            conversation = None
        service = AIService(request.user)
        created_conversation = conversation is None
        if not conversation:
            conversation = service.create_conversation(title=f"Topic: {topic.title}", provider=request.data.get(
                "provider"), model=request.data.get("model", ""))
        conversation.metadata = {
            **(conversation.metadata or {}), "topic_id": topic.id, "topic_title": topic.title}
        conversation.save(update_fields=["metadata", "updated_at"])
        provider_name, model = AIService(request.user).resolve_selection(
            conversation, request.data.get("provider"), request.data.get("model", ""))
        history = list(conversation.messages.filter(
            role__in=["user", "assistant"]).order_by("created_at"))[-12:]
        prompt = (
            "You are a topic tutor. Use the supplied topic knowledge as the primary source. "
            "If the source does not contain an answer, say that clearly and distinguish general explanation from source-backed facts.\\n\\n"
            "Context:\\n" +
            __import__("json").dumps(context, ensure_ascii=False, default=str)
        )
        messages = [{"role": "system", "content": prompt}] + [
            {"role": item.role, "content": item.content} for item in history
        ] + [{"role": "user", "content": message}]
        from ai.services import AIFallbackChainService
        try:
            result = AIFallbackChainService.generate_completion(
                messages=messages, user=request.user,
                preferred_provider=provider_name, model=model or None,
                temperature=0.4, max_tokens=3000,
            )
        except AIError as exc:
            if created_conversation:
                conversation.delete()
            return Response(
                {"success": False, "code": "ai_provider_unavailable",
                    "error": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        except Exception:
            if created_conversation:
                conversation.delete()
            logger.exception(
                "AI topic chat failed for user=%s topic=%s", request.user.pk, topic.pk)
            return Response(
                {"success": False, "code": "ai_internal_error",
                    "error": "The AI tutor could not complete this request."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        from ai.models import AIMessage
        user_message = AIMessage.objects.create(
            conversation=conversation, role="user", content=message,
            metadata={"topic_id": topic.id},
        )
        assistant = AIMessage.objects.create(
            conversation=conversation, role="assistant", content=result["content"],
            provider=result["provider"], model=result["model"],
            metadata={"topic_id": topic.id},
        )
        if AIService.should_persist_selection(result["provider"], provider_name):
            conversation.provider = result["provider"]
            conversation.model = result["model"]
        conversation.save(update_fields=["provider", "model", "updated_at"])
        return Response({"success": True, "conversation_id": conversation.id, "message": {"id": assistant.id, "role": "assistant", "content": assistant.content, "provider": assistant.provider, "model": assistant.model}})


class AIAgentPlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        intent = (request.data.get("request")
                  or request.data.get("message") or "").strip()
        if not intent:
            return Response({"detail": "request is required."}, status=400)
        lower = intent.lower()
        nodes = []
        if any(x in lower for x in ["كل يوم", "every day", "schedule", "الساعة", "at 8"]):
            nodes.append({"type": "schedule", "label": "Schedule"})
        if any(x in lower for x in ["وظائف", "jobs", "فرص"]):
            nodes += [{"type": "load_profile", "label": "Load User Profile"}, {"type": "search_jobs",
                                                                               "label": "Search Jobs"}, {"type": "ai_matching", "label": "AI Matching"}, {"type": "rank", "label": "Rank"}]
        elif any(x in lower for x in ["تعلم", "learning", "learn"]):
            nodes += [{"type": "load_skills", "label": "Load Skills"},
                      {"type": "learning_plan", "label": "Create Learning Plan"}]
        else:
            nodes += [{"type": "ai_reason", "label": "AI Reasoning"}]
        nodes.append({"type": "notification", "label": "Notification"})
        edges = [{"source": i, "target": i+1} for i in range(len(nodes)-1)]
        return Response({"intent": intent, "nodes": nodes, "edges": edges, "valid": True, "explanation": "Rule-based workflow suggestion; this is not an AI-generated response or an executed workflow. Execution requires the existing automation permissions and approval flow."})


class AIHealthView(APIView):
    permission_classes = [AIAuthenticatedPermission]

    def get(self, request):
        from ai.services.diagnostics import AIDiagnostics
        return Response(AIDiagnostics(request.user).run())


class AICapabilitiesView(APIView):
    permission_classes = [AIAuthenticatedPermission]

    def get(self, request):
        from ai.services.capabilities import get_capabilities
        features = get_capabilities()
        return Response({"features": features, "count": len(features)})


class AIChatStreamView(APIView):
    permission_classes = [AIAuthenticatedPermission]

    def post(self, request):
        import json
        from django.http import StreamingHttpResponse
        from django.utils import timezone
        from ai.services import AIService, AIFallbackChainService
        from ai.services.execution_service import ExecutionService
        from ai.models import AIMessage

        serializer = AIChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        idempotency_key = data.get("idempotency_key") or request.headers.get("Idempotency-Key", "")
        if idempotency_key:
            existing_execution = AIExecution.objects.filter(
                user=request.user,
                idempotency_key=idempotency_key,
            ).first()
            if existing_execution is not None:
                if existing_execution.status == AIExecution.Status.SUCCEEDED:
                    assistant_id = (existing_execution.metadata or {}).get("assistant_message_id")
                    assistant = AIMessage.objects.select_related("conversation").filter(
                        pk=assistant_id,
                        conversation_id=existing_execution.conversation_id,
                        role=AIMessage.ROLE_ASSISTANT,
                        conversation__user=request.user,
                    ).first() if assistant_id else None
                    if assistant is not None:
                        def replay_stream():
                            yield f"event: meta\ndata: {json.dumps({'conversation_id': assistant.conversation_id, 'provider': assistant.provider, 'model': assistant.model})}\n\n"
                            yield f"data: {json.dumps({'delta': assistant.content}, ensure_ascii=False)}\n\n"
                            yield f"event: done\ndata: {json.dumps({'message_id': assistant.pk, 'content': assistant.content}, ensure_ascii=False)}\n\n"
                        replay_response = StreamingHttpResponse(replay_stream(), content_type="text/event-stream")
                        replay_response["Cache-Control"] = "no-cache"
                        replay_response["X-Accel-Buffering"] = "no"
                        replay_response["Idempotency-Replayed"] = "true"
                        return replay_response
                    return Response({
                        "success": False,
                        "error": "The previous request completed but its stored response is unavailable.",
                        "error_code": "idempotency_result_unavailable",
                        "retryable": False,
                    }, status=status.HTTP_409_CONFLICT)
                if existing_execution.status == AIExecution.Status.RUNNING:
                    return Response({
                        "success": False,
                        "error": "This request is already being processed. Retry with the same request key shortly.",
                        "error_code": "request_in_progress",
                        "retryable": True,
                    }, status=status.HTTP_409_CONFLICT)
                return Response({
                    "success": False,
                    "error": "The previous attempt with this request key failed. Start a new attempt to retry it.",
                    "error_code": "previous_attempt_failed",
                    "retryable": True,
                }, status=status.HTTP_409_CONFLICT)

        service = AIService(request.user)
        is_new_conversation = data.get("conversation_id") is None
        conversation = service.get_or_create_conversation(
            conversation_id=data.get("conversation_id"),
            provider=data.get("provider"),
            model=data.get("model", ""),
        )
        selected_provider, selected_model = service.resolve_selection(
            conversation, data.get("provider"), data.get("model", ""))
        settings_obj = service.get_settings()
        messages = service.build_messages(conversation, current_message=data["message"])
        if data.get("system_prompt") and messages and messages[0].get("role") == "system":
            messages[0]["content"] = data["system_prompt"].strip()[:8000]

        def event_stream():
            execution = None
            full = []
            actual_provider = selected_provider
            actual_model = selected_model
            meta_sent = False
            persisted = False
            try:
                try:
                    execution = ExecutionService.start(
                        user=request.user,
                        conversation=conversation,
                        provider=selected_provider or "",
                        model=selected_model,
                        task_type="chat_stream",
                        metadata={"requested_provider": selected_provider or ""},
                        idempotency_key=idempotency_key,
                    )
                except Exception:
                    logger.exception("AI streaming execution observability could not be started")

                for chunk in AIFallbackChainService.stream_completion(
                    messages=messages,
                    user=request.user,
                    preferred_provider=selected_provider,
                    model=selected_model or None,
                    temperature=data.get("temperature") if data.get("temperature") is not None else settings_obj.temperature,
                    max_tokens=data.get("max_tokens"),
                    fallback_enabled=settings_obj.fallback_enabled,
                    timeout_seconds=settings_obj.timeout_seconds,
                    model_is_explicit=bool(data.get("model")),
                ):
                    actual_provider = chunk.get("provider") or actual_provider
                    actual_model = chunk.get("model") or actual_model
                    if not meta_sent:
                        yield f"event: meta\ndata: {json.dumps({'conversation_id': conversation.id, 'provider': actual_provider, 'model': actual_model})}\n\n"
                        meta_sent = True
                    delta = chunk.get("delta") or ""
                    if delta:
                        full.append(delta)
                        yield f"data: {json.dumps({'delta': delta}, ensure_ascii=False)}\n\n"

                content = "".join(full).strip()
                if not content:
                    raise AIError("The AI provider returned an empty response.")
                with transaction.atomic():
                    AIMessage.objects.create(
                        conversation=conversation,
                        role=AIMessage.ROLE_USER,
                        content=data["message"],
                        provider=actual_provider,
                        model=actual_model,
                    )
                    assistant = AIMessage.objects.create(
                        conversation=conversation,
                        role=AIMessage.ROLE_ASSISTANT,
                        content=content,
                        provider=actual_provider,
                        model=actual_model,
                    )
                    if AIService.should_persist_selection(actual_provider, selected_provider):
                        conversation.provider = actual_provider
                        conversation.model = actual_model
                    conversation.last_message_at = timezone.now()
                    conversation.message_count = conversation.messages.count()
                    if not conversation.title:
                        conversation.title = data["message"][:255]
                    conversation.save(update_fields=[
                        "provider", "model", "title", "last_message_at",
                        "message_count", "updated_at",
                    ])
                persisted = True
                if execution is not None:
                    try:
                        ExecutionService.finish(
                            execution,
                            status="succeeded",
                            provider=actual_provider,
                            model=actual_model,
                            fallback_count=1 if actual_provider != selected_provider else 0,
                            genuine_result=True,
                            metadata={
                                "streaming": True,
                                "assistant_message_id": assistant.pk,
                                "conversation_id": conversation.pk,
                            },
                        )
                    except Exception:
                        logger.exception("AI streaming execution success could not be persisted")
                if not meta_sent:
                    yield f"event: meta\ndata: {json.dumps({'conversation_id': conversation.id, 'provider': actual_provider, 'model': actual_model})}\n\n"
                yield f"event: done\ndata: {json.dumps({'message_id': assistant.id, 'content': content}, ensure_ascii=False)}\n\n"
            except GeneratorExit:
                # A disconnected browser must not leave an execution RUNNING
                # forever. If persistence already completed, finish() keeps
                # the terminal success state; otherwise mark it cancelled.
                if execution is not None and not persisted:
                    try:
                        ExecutionService.finish(
                            execution,
                            status="cancelled",
                            provider=actual_provider,
                            model=actual_model,
                            genuine_result=False,
                            error_code="client_disconnected",
                            error_message="The client disconnected before the response was persisted.",
                            metadata={"streaming": True, "cancelled_by_client": True},
                        )
                    except Exception:
                        logger.exception("AI streaming cancellation could not be persisted")
                raise
            except Exception as exc:
                logger.exception("AI streaming failed for user=%s", request.user.pk)
                if execution is not None:
                    try:
                        ExecutionService.finish(
                            execution,
                            status="failed",
                            provider=actual_provider,
                            model=actual_model,
                            genuine_result=False,
                            error_code=getattr(exc, "category", "stream_error"),
                            error_message=str(exc),
                            metadata={"streaming": True},
                        )
                    except Exception:
                        logger.exception("AI streaming execution failure could not be persisted")
                if is_new_conversation and not persisted:
                    conversation.delete()
                safe_error = str(exc) if isinstance(exc, AIError) else "AI streaming failed unexpectedly."
                yield f"event: error\ndata: {json.dumps({'error': safe_error}, ensure_ascii=False)}\n\n"

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response
