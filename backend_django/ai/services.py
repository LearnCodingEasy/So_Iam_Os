from django.conf import settings
from django.db import transaction

from .exceptions import AIError
from .models import (
    AIConversation,
    AIMessage,
)
from .providers import get_ai_provider
from .learning_actions import (
    looks_like_learning_request,
    extract_learning_skill,
    AILearningActionService,
)
from .serializers import AILearningPlanSerializer
from .prompts import build_system_prompt


class AIContextBuilder:
    """
    Builds the context that will be sent to the AI.
    """

    def __init__(self, user):
        self.user = user

    def build(self):
        return {
            "user_id": self.user.pk,
        }


class AIService:
    """
    Main service responsible for AI interactions
    and AI-driven actions.
    """

    def __init__(self, user):
        self.user = user

    # ---------------------------------------------------------
    # CONVERSATIONS
    # ---------------------------------------------------------

    def create_conversation(
        self,
        title="",
        provider=None,
        model="",
    ):
        provider = provider or getattr(
            settings,
            "AI_DEFAULT_PROVIDER",
            "ollama",
        )

        return AIConversation.objects.create(
            user=self.user,
            title=title,
            provider=provider,
            model=model,
        )

    def get_or_create_conversation(
        self,
        conversation_id=None,
        provider=None,
        model="",
    ):
        if conversation_id:
            try:
                return AIConversation.objects.get(
                    id=conversation_id,
                    user=self.user,
                )
            except AIConversation.DoesNotExist:
                raise AIError(
                    "Conversation does not exist."
                )

        return self.create_conversation(
            provider=provider,
            model=model,
        )

    # ---------------------------------------------------------
    # AI MESSAGE CONTEXT
    # ---------------------------------------------------------

    def build_messages(self, conversation):
        context_builder = AIContextBuilder(
            user=self.user
        )

        context = context_builder.build()

        system_prompt = build_system_prompt(
            context=context
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        history = (
            conversation.messages
            .filter(
                role__in=[
                    AIMessage.ROLE_USER,
                    AIMessage.ROLE_ASSISTANT,
                ]
            )
            .order_by("created_at")
        )

        for message in history:
            messages.append(
                {
                    "role": message.role,
                    "content": message.content,
                }
            )

        return messages

    # ---------------------------------------------------------
    # LEARNING ACTION
    # ---------------------------------------------------------

    def execute_learning_action(self, message):
        """
        Detect and execute a learning request.

        Example:

            عايز أتعلم Django

        becomes:

            Learning Request
                    ↓
                 Django
                    ↓
                 Skill
                    ↓
              LearningGoal
                    ↓
              LearningPath
                    ↓
              LearningTopics
        """

        if not looks_like_learning_request(message):
            return None, None

        skill_name = extract_learning_skill(message)

        if not skill_name:
            return None, {
                "type": "create_learning_plan",
                "status": "failed",
                "error": "Could not determine the learning skill.",
            }

        plan_data = {
            "intent": "create_learning_plan",
            "skill": skill_name,
            "level": "beginner",
            "target_level": "advanced",
            "goal_title": f"Learn {skill_name}",
            "goal_description": (
                f"Learn {skill_name} "
                "through a structured learning path."
            ),
            "reason": "",
            "path_title": (
                f"{skill_name} Learning Path"
            ),
            "path_description": (
                f"A structured learning path "
                f"for learning {skill_name}."
            ),
        }

        serializer = AILearningPlanSerializer(
            data=plan_data
        )

        serializer.is_valid(
            raise_exception=True
        )

        data = serializer.validated_data

        try:
            learning_result = (
                AILearningActionService(
                    user=self.user
                ).create_learning_plan(
                    skill_name=data["skill"],
                    level=data["level"],
                    target_level=data["target_level"],
                    goal_title=data["goal_title"],
                    goal_description=data["goal_description"],
                    reason=data["reason"],
                    path_title=data["path_title"],
                    path_description=data["path_description"],
                    topics=data.get("topics") or None,
                )
            )

        except Exception as exc:
            return None, {
                "type": "create_learning_plan",
                "status": "failed",
                "error": str(exc),
            }

        learning_action = {
            "type": "create_learning_plan",
            "status": (
                "created"
                if learning_result["created"]
                else "already_exists"
            ),
        }

        return learning_result, learning_action

    # ---------------------------------------------------------
    # SERIALIZE LEARNING RESULT
    # ---------------------------------------------------------

    def serialize_learning_result(self, result):
        if not result:
            return None

        skill = result["skill"]
        goal = result["goal"]
        path = result["path"]
        topics = result["topics"]

        return {
            "created": result["created"],

            "skill": {
                "id": skill.id,
                "name": skill.name,
                "slug": skill.slug,
            },

            "goal": {
                "id": goal.id,
                "title": goal.title,
                "description": goal.description,
                "status": goal.status,
                "target_level": goal.target_level,
            },

            "path": {
                "id": path.id,
                "title": path.title,
                "description": path.description,
                "status": path.status,
            },

            "topics": [
                {
                    "id": topic.id,
                    "title": topic.title,
                    "description": topic.description,
                    "order": topic.order,
                    "status": topic.status,
                    "estimated_minutes": topic.estimated_minutes,
                }
                for topic in topics
            ],
        }

    # ---------------------------------------------------------
    # CHAT
    # ---------------------------------------------------------

    def chat(
        self,
        message,
        conversation_id=None,
        provider=None,
        model="",
    ):
        conversation = self.get_or_create_conversation(
            conversation_id=conversation_id,
            provider=provider,
            model=model,
        )

        selected_provider = (
            provider or conversation.provider
        )

        selected_model = (
            model or conversation.model or ""
        )

        # -----------------------------------------------------
        # Save user message
        # -----------------------------------------------------

        user_message = AIMessage.objects.create(
            conversation=conversation,
            role=AIMessage.ROLE_USER,
            content=message,
        )

        # -----------------------------------------------------
        # Execute Learning action
        # -----------------------------------------------------

        learning_result, learning_action = (
            self.execute_learning_action(message)
        )

        # -----------------------------------------------------
        # AI response
        # -----------------------------------------------------

        messages = self.build_messages(
            conversation
        )

        ai_provider = get_ai_provider(
            selected_provider
        )

        result = ai_provider.generate(
            messages=messages,
            model=selected_model or None,
        )

        # -----------------------------------------------------
        # Save assistant response
        # -----------------------------------------------------

        with transaction.atomic():

            assistant_message = AIMessage.objects.create(
                conversation=conversation,
                role=AIMessage.ROLE_ASSISTANT,
                content=result["content"],
                provider=result["provider"],
                model=result["model"],
                metadata={
                    "provider": result["provider"],
                    "model": result["model"],
                },
            )

            conversation.provider = result["provider"]
            conversation.model = result["model"]

            if not conversation.title:
                conversation.title = message[:255]

            conversation.save(
                update_fields=[
                    "provider",
                    "model",
                    "title",
                    "updated_at",
                ]
            )

        return {
            "conversation": conversation,

            "user_message": user_message,

            "assistant_message": assistant_message,

            "provider": result["provider"],

            "model": result["model"],

            "learning": (
                self.serialize_learning_result(
                    learning_result
                )
                if learning_result
                else None
            ),

            "learning_action": learning_action,
        }
