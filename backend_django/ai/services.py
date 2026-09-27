import json

from django.conf import settings
from django.db import transaction

from .exceptions import AIError
from .models import AIConversation, AIMessage, AISettings, AIPromptProfile
from .providers import get_ai_provider
from .learning_actions import looks_like_learning_request, AILearningActionService
from .prompts import build_system_prompt


class AIContextBuilder:
    def __init__(self, user, max_items=20):
        self.user = user
        self.max_items = max_items

    def build(self):
        context = {"user_id": self.user.pk,
                   "user_name": getattr(self.user, "full_name", "")}
        try:
            from knowledge.models import KnowledgeItem
            knowledge = KnowledgeItem.objects.filter(
                user=self.user, is_archived=False).order_by("-updated_at")[:self.max_items]
            context["knowledge"] = [
                {"id": x.id, "title": x.title, "type": x.knowledge_type, "content": x.content[:1500]} for x in knowledge]
        except Exception:
            context["knowledge"] = []
        try:
            from goals.models import Goal
            goals = Goal.objects.filter(user=self.user).exclude(status__in=[
                "completed", "cancelled", "archived"]).order_by("target_date")[:self.max_items]
            context["goals"] = [{"id": x.id, "title": x.title, "progress": x.progress_percent, "status": x.status,
                                 "target_date": x.target_date.isoformat() if x.target_date else None} for x in goals]
        except Exception:
            context["goals"] = []
        try:
            from tasks.models import Task
            from django.utils import timezone
            tasks = Task.objects.filter(user=self.user, scheduled_date=timezone.localdate()).exclude(
                status__in=["completed", "cancelled"]).order_by("sort_order")[:self.max_items]
            context["today_tasks"] = [{"id": x.id, "title": x.title, "status": x.status,
                                       "priority": x.priority, "estimated_minutes": x.estimated_minutes} for x in tasks]
        except Exception:
            context["today_tasks"] = []
        try:
            from learning.models import LearningGoal, LearningPath
            learning_goals = LearningGoal.objects.filter(user=self.user).exclude(
                status__in=["completed", "archived"]).select_related("skill")[:self.max_items]
            context["learning_goals"] = [{"id": x.id, "title": x.title, "skill": x.skill.name if x.skill else None,
                                          "target_level": x.target_level, "status": x.status} for x in learning_goals]
            paths = LearningPath.objects.filter(user=self.user).exclude(
                status="archived").order_by("-updated_at")[:self.max_items]
            context["learning_paths"] = [
                {"id": x.id, "title": x.title, "goal_id": x.goal_id, "status": x.status} for x in paths]
        except Exception:
            context["learning_goals"] = []
            context["learning_paths"] = []
        return context


class AIService:
    def __init__(self, user):
        self.user = user

    def get_settings(self):
        obj, _ = AISettings.objects.get_or_create(user=self.user)
        return obj

    def create_conversation(self, title="", provider=None, model=""):
        config = self.get_settings()
        provider = provider or config.preferred_provider or getattr(
            settings, "AI_DEFAULT_PROVIDER", "ollama")
        model = model or config.preferred_model
        return AIConversation.objects.create(user=self.user, title=title, provider=provider, model=model)

    def get_or_create_conversation(self, conversation_id=None, provider=None, model=""):
        if conversation_id:
            try:
                return AIConversation.objects.get(id=conversation_id, user=self.user)
            except AIConversation.DoesNotExist as exc:
                raise AIError("Conversation does not exist.") from exc
        return self.create_conversation(provider=provider, model=model)

    def build_messages(self, conversation, current_message=""):
        config = self.get_settings()
        context = AIContextBuilder(self.user).build() if config.context_enabled else {
            "user_id": self.user.pk}
        profile = config.default_prompt_profile
        if profile:
            system_prompt = profile.system_prompt or build_system_prompt(
                context=context)
            if profile.context_instructions:
                system_prompt += "\n\nContext instructions:\n" + profile.context_instructions
        else:
            system_prompt = build_system_prompt(context=context)
        system_prompt += "\n\nRelevant application context:\n" + \
            json.dumps(context, ensure_ascii=False, default=str)
        messages = [{"role": "system", "content": system_prompt}]
        history = list(conversation.messages.filter(role__in=[
                       AIMessage.ROLE_USER, AIMessage.ROLE_ASSISTANT]).order_by("created_at"))[-30:]
        for item in history:
            messages.append({"role": item.role, "content": item.content})
        if current_message and (not messages or messages[-1].get("content") != current_message):
            messages.append({"role": "user", "content": current_message})
        return messages

    def execute_learning_action(self, message, provider=None, model=""):
        if not looks_like_learning_request(message):
            return None, None
        try:
            plan = AILearningActionService.generate_ai_plan(message=message, provider=provider or getattr(
                settings, "AI_DEFAULT_PROVIDER", "ollama"), model=model or "", user=self.user)
        except Exception as exc:
            return None, {"type": "create_learning_plan", "status": "failed", "error": str(exc)}
        return None, {"type": "create_learning_plan", "status": "preview_ready", "plan": plan}

    def serialize_learning_result(self, result):
        if not result:
            return None
        return {
            "created": result["created"],
            "skill": {"id": result["skill"].id, "name": result["skill"].name, "slug": result["skill"].slug},
            "goal": {"id": result["goal"].id, "title": result["goal"].title, "description": result["goal"].description, "status": result["goal"].status, "target_level": result["goal"].target_level},
            "path": {"id": result["path"].id, "title": result["path"].title, "description": result["path"].description, "status": result["path"].status},
            "topics": [{"id": x.id, "title": x.title, "description": x.description, "order": x.order, "status": x.status, "estimated_minutes": x.estimated_minutes} for x in result["topics"]],
        }

    def approve_learning_plan(self, plan):
        required = {"skill", "topics"}
        if not required.issubset(plan):
            raise AIError("A valid learning plan is required.")
        return AILearningActionService(user=self.user).create_learning_plan(
            skill_name=plan["skill"], level=plan.get("level", "beginner"), target_level=plan.get("target_level", "advanced"),
            goal_title=plan.get("goal_title") or None, goal_description=plan.get("goal_description", ""), reason=plan.get("reason", ""),
            path_title=plan.get("path_title") or None, path_description=plan.get("path_description", ""), topics=plan.get("topics") or [],
        )

    def chat(self, message, conversation_id=None, provider=None, model=""):
        conversation = self.get_or_create_conversation(
            conversation_id=conversation_id, provider=provider, model=model)
        selected_provider = provider or conversation.provider
        selected_model = model or conversation.model or ""
        config = self.get_settings()
        profile = config.default_prompt_profile
        user_message = AIMessage.objects.create(
            conversation=conversation, role=AIMessage.ROLE_USER, content=message)
        messages = self.build_messages(conversation, current_message=message)
        provider_obj = get_ai_provider(selected_provider, user=self.user)
        result = provider_obj.generate(messages=messages, model=selected_model or None,
                                       temperature=profile.temperature if profile else None, max_tokens=profile.max_tokens if profile else None)
        with transaction.atomic():
            assistant_message = AIMessage.objects.create(conversation=conversation, role=AIMessage.ROLE_ASSISTANT, content=result["content"], provider=result["provider"], model=result["model"], metadata={
                                                         "provider": result["provider"], "model": result["model"]})
            conversation.provider = result["provider"]
            conversation.model = result["model"]
            if not conversation.title:
                conversation.title = message[:255]
            conversation.save(
                update_fields=["provider", "model", "title", "updated_at"])
        _, learning_action = self.execute_learning_action(
            message, selected_provider, selected_model)
        return {"conversation": conversation, "user_message": user_message, "assistant_message": assistant_message, "provider": result["provider"], "model": result["model"], "learning": None, "learning_action": learning_action}
