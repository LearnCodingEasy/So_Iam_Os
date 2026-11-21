import json

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from ..exceptions import AIError
from ..models import AIConversation, AIMessage, AISettings, AIPromptProfile
from ..providers import get_ai_provider
from ..learning_actions import looks_like_learning_request, AILearningActionService
from ..prompts import build_system_prompt


import logging

from ..exceptions import AIConfigurationError, AIProviderError, AIResponseError

logger = logging.getLogger(__name__)


class AIFallbackChainService:
    """Bounded, error-aware AI gateway used by all application services."""

    PROVIDER_ORDER = ("openai", "gemini", "deepseek", "openrouter", "ollama")

    @classmethod
    def generate_completion(
        cls,
        messages,
        user=None,
        preferred_provider=None,
        model=None,
        temperature=None,
        max_tokens=None,
        *,
        task_type="chat",
        conversation=None,
        idempotency_key="",
        fallback_enabled=True,
        model_is_explicit=True,
    ):
        import random
        import time

        from ..models import AIProviderCredential
        from ..providers import get_ai_provider
        from ..services.execution_service import ExecutionService

        if not isinstance(messages, list) or not messages:
            raise ValueError("At least one AI message is required.")
        if any(
            not isinstance(item, dict)
            or item.get("role") not in {"system", "user", "assistant"}
            or not isinstance(item.get("content"), str)
            or not item["content"].strip()
            for item in messages
        ):
            raise ValueError(
                "AI messages must contain a valid role and non-empty text content."
            )

        ordered = []
        preferred = str(preferred_provider or "").strip().lower()
        if preferred:
            ordered.append(preferred)

        credentials = {}
        if user is not None and getattr(user, "is_authenticated", False):
            credentials = {
                row.provider: row
                for row in AIProviderCredential.objects.filter(
                    user=user, encrypted_api_key__gt=""
                )
            }

        # User-defined priorities are stored in credential metadata. Lower numbers win.
        priority_rows = []
        for provider_name, credential in credentials.items():
            if str((credential.metadata or {}).get("enabled", True)).lower() in {"false", "0", "no"}:
                continue
            try:
                priority = int((credential.metadata or {}).get("priority", 100))
            except (TypeError, ValueError):
                priority = 100
            priority_rows.append((priority, provider_name))
        priority_rows.sort()
        if fallback_enabled:
            ordered.extend(name for _, name in priority_rows if name not in ordered)
            ordered.extend(name for name in cls.PROVIDER_ORDER if name not in ordered)

        env_keys = {
            "openai": ("OPENAI_API_KEY",),
            "gemini": ("GEMINI_API_KEY", "GOOGLE_API_KEY"),
            "deepseek": ("DEEPSEEK_API_KEY",),
            "openrouter": ("OPENROUTER_API_KEY",),
        }
        max_provider_attempts = max(
            1,
            min(5, int(getattr(settings, "AI_MAX_PROVIDER_ATTEMPTS", 3) or 3)),
        )
        max_retries_per_provider = max(
            0,
            min(2, int(getattr(settings, "AI_MAX_RETRIES_PER_PROVIDER", 1) or 0)),
        )
        deadline = max(
            5,
            int(getattr(settings, "AI_TOTAL_DEADLINE_SECONDS", 45) or 45),
        )
        backoff_base = max(
            0.05,
            float(getattr(settings, "AI_RETRY_BACKOFF_SECONDS", 0.5) or 0.5),
        )
        started = time.monotonic()
        attempts = 0
        retry_count = 0
        fallback_count = 0
        last_error = None
        execution = None

        if user is not None and getattr(user, "is_authenticated", False):
            try:
                execution = ExecutionService.start(
                    user=user,
                    conversation=conversation,
                    provider=preferred_provider or "",
                    model=model or "",
                    task_type=task_type,
                    metadata={"requested_provider": preferred_provider or ""},
                    idempotency_key=idempotency_key or "",
                )
            except Exception:
                logger.exception("AI execution observability could not be started")

        def finish_failure(exc):
            if execution is None:
                return
            try:
                ExecutionService.finish(
                    execution,
                    status="failed",
                    provider=getattr(exc, "provider", "") or execution.provider,
                    retry_count=retry_count,
                    fallback_count=fallback_count,
                    genuine_result=False,
                    error_code=getattr(exc, "category", "unknown"),
                    error_message=str(exc),
                    metadata={"attempts": attempts},
                )
            except Exception:
                logger.exception("AI execution failure could not be persisted")

        for provider_name in ordered:
            if attempts >= max_provider_attempts:
                break

            configured_env_key = any(
                bool(str(getattr(settings, setting, "") or "").strip())
                for setting in env_keys.get(provider_name, ())
            )
            has_user_credential = provider_name in credentials
            if provider_name != "ollama" and not (has_user_credential or configured_env_key):
                continue
            if has_user_credential and str((credentials[provider_name].metadata or {}).get("enabled", True)).lower() in {"false", "0", "no"}:
                continue

            provider_retries = 0
            # A model restored from stored state (conversation/settings) may belong
            # to a different provider. It is dropped once for this provider if the
            # provider rejects it, instead of disabling the provider entirely.
            drop_stored_model = False
            while provider_retries <= max_retries_per_provider:
                if attempts >= max_provider_attempts or time.monotonic() - started >= deadline:
                    break
                attempts += 1
                try:
                    provider_obj = get_ai_provider(provider_name, user=user)
                    selected_model = (
                        model
                        if provider_name == (preferred_provider or "").lower() and not drop_stored_model
                        else None
                    )
                    remaining_seconds = max(1, int(deadline - (time.monotonic() - started)))
                    provider_timeout = min(
                        max(1, int(getattr(settings, "AI_PROVIDER_TIMEOUT_SECONDS", 30))),
                        remaining_seconds,
                    )
                    result = provider_obj.generate(
                        messages=messages,
                        model=selected_model,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        timeout_seconds=provider_timeout,
                    )
                    if not isinstance(result, dict) or not str(result.get("content") or "").strip():
                        raise AIResponseError("The provider returned an empty response.")
                    result = {
                        **result,
                        "requested_provider": preferred_provider or provider_name,
                        "retry_count": retry_count,
                        "fallback_count": fallback_count,
                        "execution_status": "succeeded",
                        "genuine_result": True,
                    }
                    if execution is not None:
                        result["execution_id"] = execution.pk
                        try:
                            ExecutionService.finish(
                                execution,
                                status="succeeded",
                                provider=result.get("provider") or provider_name,
                                model=result.get("model") or selected_model or "",
                                retry_count=retry_count,
                                fallback_count=fallback_count,
                                genuine_result=True,
                                metadata={
                                    "attempts": attempts,
                                    "actual_provider": result.get("provider") or provider_name,
                                },
                            )
                        except Exception:
                            logger.exception("AI execution success could not be persisted")
                    return result
                except AIConfigurationError as exc:
                    last_error = exc
                    # A preferred provider can be unavailable because its key,
                    # endpoint, or model configuration is missing. When fallback
                    # is enabled, continue to another configured provider instead
                    # of aborting the entire request. With fallback disabled, keep
                    # the explicit configuration error visible to the caller.
                    logger.warning(
                        "AI provider %s is not configured; fallback %s.",
                        provider_name,
                        "is enabled" if fallback_enabled else "is disabled",
                    )
                    if not fallback_enabled:
                        finish_failure(exc)
                        raise
                    break
                except (AIProviderError, AIResponseError) as exc:
                    last_error = exc
                    if (
                        getattr(exc, "category", "") == "invalid_request_or_model"
                        and selected_model
                        and not model_is_explicit
                        and not drop_stored_model
                    ):
                        drop_stored_model = True
                        logger.warning(
                            "AI provider %s rejected a stored model; retrying once with its default model.",
                            provider_name,
                        )
                        continue
                    if provider_name == preferred and getattr(exc, "category", "") in {
                        "authentication", "quota_exhausted"
                    }:
                        finish_failure(exc)
                        raise
                    # A provider-specific model/request failure must not abort the
                    # global chain; another configured provider may still satisfy the request.
                    retry_after = getattr(exc, "retry_after", None)
                    should_retry = (
                        getattr(exc, "retryable", False)
                        and provider_retries < max_retries_per_provider
                        and time.monotonic() - started < deadline
                    )
                    if should_retry:
                        delay = float(retry_after or (
                            backoff_base * (2 ** provider_retries)
                            + random.uniform(0, backoff_base)
                        ))
                        remaining = deadline - (time.monotonic() - started)
                        if remaining <= 0:
                            break
                        time.sleep(min(delay, remaining))
                        provider_retries += 1
                        retry_count += 1
                        continue

                    logger.warning(
                        "AI provider %s failed; fallback remains eligible (category=%s).",
                        provider_name,
                        getattr(exc, "category", "provider_error"),
                    )
                    break

            if last_error is not None and provider_name != ordered[-1]:
                fallback_count += 1

        if last_error:
            finish_failure(last_error)
            raise last_error

        error = AIConfigurationError(
            "No eligible AI provider is configured. Add a provider credential or configure an application-level provider."
        )
        finish_failure(error)
        raise error


    @classmethod
    def stream_completion(
        cls,
        messages,
        user=None,
        preferred_provider=None,
        model=None,
        temperature=None,
        max_tokens=None,
        *,
        fallback_enabled=True,
        timeout_seconds=None,
        model_is_explicit=True,
    ):
        """Stream from the preferred provider, falling back only before output starts."""
        from ..models import AIProviderCredential
        from ..providers import get_ai_provider

        preferred = str(preferred_provider or "").strip().lower()
        ordered = [preferred] if preferred else []
        credentials = {}
        if user is not None and getattr(user, "is_authenticated", False):
            credentials = {
                row.provider: row
                for row in AIProviderCredential.objects.filter(
                    user=user, encrypted_api_key__gt=""
                )
            }

        if fallback_enabled:
            priority_rows = []
            for provider_name, credential in credentials.items():
                metadata = credential.metadata or {}
                if str(metadata.get("enabled", True)).lower() in {"false", "0", "no"}:
                    continue
                try:
                    priority = int(metadata.get("priority", 100))
                except (TypeError, ValueError):
                    priority = 100
                priority_rows.append((priority, provider_name))
            priority_rows.sort()
            ordered.extend(name for _, name in priority_rows if name not in ordered)
            ordered.extend(name for name in cls.PROVIDER_ORDER if name not in ordered)

        env_keys = {
            "openai": ("OPENAI_API_KEY",),
            "gemini": ("GEMINI_API_KEY", "GOOGLE_API_KEY"),
            "deepseek": ("DEEPSEEK_API_KEY",),
            "openrouter": ("OPENROUTER_API_KEY",),
        }
        attempts = 0
        last_error = None
        max_attempts = max(1, min(5, int(getattr(settings, "AI_MAX_PROVIDER_ATTEMPTS", 5) or 5)))

        for provider_name in ordered:
            if attempts >= max_attempts:
                break
            credential = credentials.get(provider_name)
            if credential and str((credential.metadata or {}).get("enabled", True)).lower() in {"false", "0", "no"}:
                continue
            has_env_key = any(
                bool(str(getattr(settings, key, "") or "").strip())
                for key in env_keys.get(provider_name, ())
            )
            if provider_name != "ollama" and not (credential or has_env_key):
                continue

            attempts += 1
            drop_stored_model = False
            while True:
                selected_model = model if provider_name == preferred and not drop_stored_model else None
                emitted_content = False
                try:
                    provider_obj = get_ai_provider(provider_name, user=user)
                    for item in provider_obj.generate_stream(
                        messages=messages,
                        model=selected_model,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        timeout_seconds=timeout_seconds,
                    ):
                        if not isinstance(item, dict):
                            continue
                        delta = item.get("delta") or item.get("content") or ""
                        if delta:
                            emitted_content = True
                            yield {
                                **item,
                                "delta": str(delta),
                                "provider": item.get("provider") or provider_name,
                                "model": item.get("model") or selected_model or "",
                            }
                        if item.get("done"):
                            break
                    if emitted_content:
                        return
                    raise AIResponseError(f"{provider_name} returned an empty streaming response.")
                except AIConfigurationError as exc:
                    last_error = exc
                    if not fallback_enabled:
                        raise
                    logger.warning(
                        "Streaming AI provider %s is not configured; trying fallback.",
                        provider_name,
                    )
                    break
                except (AIProviderError, AIResponseError) as exc:
                    if provider_name == preferred and getattr(exc, "category", "") in {
                        "authentication", "quota_exhausted"
                    }:
                        raise
                    # Once a delta has been sent, switching providers would duplicate
                    # or corrupt the user's visible answer. Only pre-output failures fall back.
                    if emitted_content:
                        raise
                    if (
                        getattr(exc, "category", "") == "invalid_request_or_model"
                        and selected_model
                        and not model_is_explicit
                        and not drop_stored_model
                    ):
                        drop_stored_model = True
                        logger.warning(
                            "Streaming provider %s rejected a stored model; retrying once with its default model.",
                            provider_name,
                        )
                        continue
                    last_error = exc
                    if not fallback_enabled:
                        raise
                    break

        if last_error is not None:
            raise last_error
        raise AIConfigurationError(
            "No eligible AI provider is configured for streaming."
        )


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
        try:
            from memory.models import MemoryItem
            context["memory"] = [{"id": x.id, "type": x.type, "key": x.key, "content": x.content[:1000], "importance": x.importance}
                                 for x in MemoryItem.objects.filter(user=self.user, is_active=True).order_by("-importance", "-updated_at")[:self.max_items]]
        except Exception:
            context["memory"] = []
        try:
            from jobs_opportunity.models import JobOpportunity
            context["job_opportunities"] = [{"id": x.id, "title": x.title, "company": x.company, "location": x.location, "remote": x.is_remote}
                                            for x in JobOpportunity.objects.filter(user=self.user, is_active=True).order_by("-published_at")[:10]]
        except Exception:
            context["job_opportunities"] = []
        try:
            from projects.models import Project
            context["projects"] = [{"id": x.id, "title": x.title, "status": x.status, "description": x.description[:500]}
                                   for x in Project.objects.filter(user=self.user).order_by("-updated_at")[:10]]
        except Exception:
            context["projects"] = []
        return context


class AIService:
    def __init__(self, user):
        self.user = user

    def get_settings(self):
        # Seed new user preferences from the application default exactly once;
        # never overwrite an existing user-managed provider selection.
        obj, _ = AISettings.objects.get_or_create(
            user=self.user,
            defaults={
                "preferred_provider": getattr(settings, "AI_DEFAULT_PROVIDER", "ollama"),
            },
        )
        return obj

    def resolve_selection(self, conversation, provider=None, model=""):
        """Single source of truth for which provider/model a request should try first.

        A stored model is only valid for the provider it was stored with, so it is
        never sent to a different provider.
        """
        config = self.get_settings()
        selected_provider = provider or conversation.provider or config.preferred_provider
        if model:
            selected_model = model
        elif selected_provider == conversation.provider and conversation.model:
            selected_model = conversation.model
        elif selected_provider == config.preferred_provider and config.preferred_model:
            selected_model = config.preferred_model
        else:
            selected_model = ""
        return selected_provider, selected_model

    @staticmethod
    def should_persist_selection(result_provider, selected_provider):
        """Fallback answers must not overwrite the user's selected primary."""
        return result_provider == selected_provider

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
            plan = AILearningActionService.generate_ai_plan(
                message=message,
                provider=provider or getattr(settings, "AI_DEFAULT_PROVIDER", "ollama"),
                model=model or "",
                user=self.user,
            )
        except AIError as exc:
            return None, {
                "type": "create_learning_plan",
                "status": "failed",
                "error": str(exc),
            }
        except Exception:
            logger.exception("AI learning action failed for user=%s", self.user.pk)
            return None, {
                "type": "create_learning_plan",
                "status": "failed",
                "error": "The learning plan could not be generated.",
            }
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

    def chat(self, message, conversation_id=None, provider=None, model="", idempotency_key="", system_prompt="", temperature=None, max_tokens=None):
        if idempotency_key:
            from ..models import AIExecution
            existing = AIExecution.objects.filter(
                user=self.user,
                idempotency_key=idempotency_key,
            ).first()
            if existing is not None:
                if existing.status == AIExecution.Status.SUCCEEDED:
                    assistant_id = (existing.metadata or {}).get("assistant_message_id")
                    assistant = AIMessage.objects.select_related("conversation").filter(
                        pk=assistant_id,
                        conversation_id=existing.conversation_id,
                        role=AIMessage.ROLE_ASSISTANT,
                        conversation__user=self.user,
                    ).first() if assistant_id else None
                    if assistant is not None:
                        return {
                            "conversation": assistant.conversation,
                            "user_message": None,
                            "assistant_message": assistant,
                            "provider": assistant.provider,
                            "model": assistant.model,
                            "learning": None,
                            "learning_action": None,
                            "replayed": True,
                        }
                    raise AIError(
                        "The previous request completed but its stored response is unavailable.",
                        category="idempotency_result_unavailable",
                        retryable=False,
                    )
                if existing.status == AIExecution.Status.RUNNING:
                    raise AIError(
                        "This request is already being processed. Retry with the same request key shortly.",
                        category="request_in_progress",
                        retryable=True,
                    )
                raise AIError(
                    "The previous attempt with this request key failed. Start a new attempt to retry it.",
                    category="previous_attempt_failed",
                    retryable=True,
                )

        is_new_conversation = conversation_id is None
        conversation = self.get_or_create_conversation(
            conversation_id=conversation_id, provider=provider, model=model)
        config = self.get_settings()
        selected_provider, selected_model = self.resolve_selection(conversation, provider, model)
        profile = config.default_prompt_profile
        if profile is not None and profile.user_id != self.user.pk:
            profile = None
        messages = self.build_messages(conversation, current_message=message)
        if system_prompt and messages and messages[0].get("role") == "system":
            messages[0]["content"] = system_prompt.strip()[:8000]

        try:
            result = AIFallbackChainService.generate_completion(
                messages=messages,
                user=self.user,
                preferred_provider=selected_provider,
                model=selected_model or None,
                temperature=temperature if temperature is not None else (profile.temperature if profile else config.temperature),
                max_tokens=max_tokens if max_tokens is not None else (profile.max_tokens if profile else None),
                task_type="chat",
                conversation=conversation,
                idempotency_key=idempotency_key or "",
                fallback_enabled=config.fallback_enabled,
                model_is_explicit=bool(model),
            )
        except Exception:
            # Failed requests must not leave a persisted user turn or empty
            # conversation that looks like a successful interaction.
            if is_new_conversation:
                conversation.delete()
            raise

        with transaction.atomic():
            user_message = AIMessage.objects.create(
                conversation=conversation,
                role=AIMessage.ROLE_USER,
                content=message,
            )
            assistant_message = AIMessage.objects.create(
                conversation=conversation,
                role=AIMessage.ROLE_ASSISTANT,
                content=result["content"],
                provider=result["provider"],
                model=result["model"],
                metadata={"provider": result["provider"], "model": result["model"]},
            )
            # Keep the user's selected primary on the conversation. The provider that
            # actually answered (which may be a fallback) is recorded on the message
            # and on the execution, so one outage never demotes the primary for good.
            if self.should_persist_selection(result["provider"], selected_provider):
                conversation.provider = result["provider"]
                conversation.model = result["model"]
            if not conversation.title:
                conversation.title = message[:255]
            conversation.last_message_at = timezone.now()
            conversation.message_count = conversation.messages.count()
            conversation.save(update_fields=["provider", "model", "title", "last_message_at", "message_count", "updated_at"])

        execution_id = result.get("execution_id")
        if execution_id:
            from ..models import AIExecution
            execution = AIExecution.objects.filter(pk=execution_id, user=self.user).first()
            if execution is not None:
                execution.metadata = {
                    **(execution.metadata or {}),
                    "assistant_message_id": assistant_message.pk,
                    "conversation_id": conversation.pk,
                }
                execution.save(update_fields=["metadata"])

        _, learning_action = self.execute_learning_action(
            message, result.get("provider") or selected_provider,
            result.get("model") or selected_model,
        )
        return {
            "conversation": conversation,
            "user_message": user_message,
            "assistant_message": assistant_message,
            "provider": result["provider"],
            "model": result["model"],
            "learning": None,
            "learning_action": learning_action,
        }
