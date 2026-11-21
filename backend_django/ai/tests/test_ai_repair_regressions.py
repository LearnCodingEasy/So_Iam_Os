from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase, override_settings


class AIModelExportRegressionTests(SimpleTestCase):
    def test_budget_reservation_and_audit_models_are_exported(self):
        from ai.models import AIBudgetReservation, AiAuditLog

        self.assertIsNotNone(AIBudgetReservation)
        self.assertIsNotNone(AiAuditLog)


class ProviderEndpointValidationTests(SimpleTestCase):
    @override_settings(
        ENVIRONMENT="production",
        OPENAI_API_KEY="test-key",
        OPENAI_BASE_URL="http://127.0.0.1:8080/v1",
    )
    def test_external_provider_rejects_insecure_private_production_endpoint(self):
        from ai.exceptions import AIConfigurationError
        from ai.providers.openai import OpenAIProvider

        with self.assertRaises(AIConfigurationError):
            OpenAIProvider()


class FallbackPolicyRegressionTests(SimpleTestCase):
    def test_disabled_fallback_does_not_switch_provider(self):
        from ai.exceptions import AIProviderError
        from ai.services.core import AIFallbackChainService

        class FailedProvider:
            def generate(self, **kwargs):
                raise AIProviderError("primary unavailable", category="network_error")

        with patch("ai.providers.get_ai_provider", return_value=FailedProvider()) as factory:
            with self.assertRaises(AIProviderError):
                AIFallbackChainService.generate_completion(
                    messages=[{"role": "user", "content": "hello"}],
                    preferred_provider="ollama",
                    fallback_enabled=False,
                )

        # Network failures are retryable, so the same provider may be retried (bounded),
        # but with fallback disabled no other provider may ever be requested.
        requested = {call.args[0] for call in factory.call_args_list}
        self.assertEqual(requested, {"ollama"})
        self.assertLessEqual(factory.call_count, 2)


class CredentialUpsertRegressionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="credential-upsert@example.com",
            password="StrongPass123",
        )

    def test_updating_api_key_preserves_existing_provider_metadata(self):
        from ai.models import AIProviderCredential
        from ai.api.serializers import AIProviderCredentialSerializer

        credential = AIProviderCredential(
            user=self.user,
            provider="openai",
            metadata={
                "base_url": "https://proxy.example.test/v1",
                "model": "gpt-4o-mini",
                "priority": 7,
                "enabled": True,
            },
        )
        credential.set_api_key("old-secret")
        credential.save()

        request = SimpleNamespace(user=self.user)
        serializer = AIProviderCredentialSerializer(
            data={"provider": "openai", "api_key": "new-secret"},
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()

        self.assertEqual(updated.get_api_key(), "new-secret")
        self.assertEqual(updated.metadata["base_url"], "https://proxy.example.test/v1")
        self.assertEqual(updated.metadata["model"], "gpt-4o-mini")
        self.assertEqual(updated.metadata["priority"], 7)
        self.assertTrue(updated.metadata["enabled"])


class ExecutionAuditRegressionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="execution-audit@example.com",
            password="StrongPass123",
        )

    def test_execution_lifecycle_writes_to_current_audit_schema(self):
        from ai.models import AiAuditLog
        from ai.services.execution_service import ExecutionService

        execution = ExecutionService.start(
            user=self.user,
            provider="openai",
            model="gpt-4o-mini",
            task_type="chat",
        )
        ExecutionService.finish(
            execution,
            status="succeeded",
            provider="openai",
            model="gpt-4o-mini",
            genuine_result=True,
        )

        records = list(AiAuditLog.objects.filter(user=self.user).order_by("action"))
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].details["execution_id"], execution.pk)
        self.assertEqual(records[1].details["execution_id"], execution.pk)


class StreamingFallbackRegressionTests(SimpleTestCase):
    def test_stream_falls_back_when_primary_fails_before_first_delta(self):
        from ai.exceptions import AIProviderError
        from ai.services.core import AIFallbackChainService

        class Provider:
            def __init__(self, name):
                self.name = name

            def generate_stream(self, **kwargs):
                if self.name == "ollama":
                    raise AIProviderError("local provider unavailable", category="network_error")
                yield {"delta": "fallback answer", "provider": self.name, "model": "fallback-model"}

        with override_settings(OPENAI_API_KEY="configured", AI_MAX_PROVIDER_ATTEMPTS=3):
            with patch("ai.providers.get_ai_provider", side_effect=lambda name, user=None: Provider(name)):
                chunks = list(AIFallbackChainService.stream_completion(
                    messages=[{"role": "user", "content": "hello"}],
                    preferred_provider="ollama",
                    fallback_enabled=True,
                ))

        self.assertEqual("".join(chunk["delta"] for chunk in chunks), "fallback answer")
        self.assertEqual(chunks[0]["provider"], "openai")

    def test_stream_does_not_switch_after_partial_output(self):
        from ai.exceptions import AIProviderError
        from ai.services.core import AIFallbackChainService

        class PartialProvider:
            def generate_stream(self, **kwargs):
                yield {"delta": "partial", "provider": "ollama", "model": "local"}
                raise AIProviderError("connection lost", category="network_error")

        with patch("ai.providers.get_ai_provider", return_value=PartialProvider()) as factory:
            stream = AIFallbackChainService.stream_completion(
                messages=[{"role": "user", "content": "hello"}],
                preferred_provider="ollama",
                fallback_enabled=True,
            )
            self.assertEqual(next(stream)["delta"], "partial")
            with self.assertRaises(AIProviderError):
                next(stream)

        factory.assert_called_once_with("ollama", user=None)


class UserProviderDefaultRegressionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="provider-default@example.com",
            password="StrongPass123",
        )

    @override_settings(AI_DEFAULT_PROVIDER="openai")
    def test_new_user_settings_inherit_application_provider_default(self):
        from ai.services.core import AIService

        settings_obj = AIService(self.user).get_settings()
        self.assertEqual(settings_obj.preferred_provider, "openai")

    @override_settings(AI_DEFAULT_PROVIDER="gemini")
    def test_existing_user_provider_preference_is_not_overwritten(self):
        from ai.models import AISettings
        from ai.services.core import AIService

        AISettings.objects.create(user=self.user, preferred_provider="openai")
        settings_obj = AIService(self.user).get_settings()
        self.assertEqual(settings_obj.preferred_provider, "openai")


class PreferredProviderErrorPolicyTests(SimpleTestCase):
    def test_preferred_provider_authentication_failure_is_not_hidden_by_fallback(self):
        from ai.exceptions import AIProviderError
        from ai.services.core import AIFallbackChainService

        class FailedProvider:
            def generate(self, **kwargs):
                raise AIProviderError("authentication failed", category="authentication", retryable=False)

        with override_settings(OPENAI_API_KEY="configured", AI_MAX_PROVIDER_ATTEMPTS=3):
            with patch("ai.providers.get_ai_provider", return_value=FailedProvider()) as factory:
                with self.assertRaises(AIProviderError):
                    AIFallbackChainService.generate_completion(
                        messages=[{"role": "user", "content": "hello"}],
                        preferred_provider="ollama",
                        fallback_enabled=True,
                    )

        factory.assert_called_once_with("ollama", user=None)


class ProviderConfigurationFallbackTests(SimpleTestCase):
    def test_missing_preferred_provider_configuration_uses_available_fallback(self):
        from ai.exceptions import AIConfigurationError
        from ai.services.core import AIFallbackChainService

        class WorkingProvider:
            def generate(self, **kwargs):
                return {
                    "content": "fallback answer",
                    "provider": "openai",
                    "model": "gpt-4o-mini",
                }

        def provider_factory(name, user=None):
            if name == "ollama":
                raise AIConfigurationError("Ollama endpoint is unavailable.")
            return WorkingProvider()

        with override_settings(
            OPENAI_API_KEY="configured-test-key",
            AI_MAX_PROVIDER_ATTEMPTS=5,
        ):
            with patch("ai.providers.get_ai_provider", side_effect=provider_factory):
                result = AIFallbackChainService.generate_completion(
                    messages=[{"role": "user", "content": "hello"}],
                    preferred_provider="ollama",
                    fallback_enabled=True,
                )

        self.assertEqual(result["content"], "fallback answer")
        self.assertEqual(result["provider"], "openai")

    def test_missing_preferred_provider_configuration_is_visible_when_fallback_disabled(self):
        from ai.exceptions import AIConfigurationError
        from ai.services.core import AIFallbackChainService

        with patch(
            "ai.providers.get_ai_provider",
            side_effect=AIConfigurationError("Ollama endpoint is unavailable."),
        ) as factory:
            with self.assertRaises(AIConfigurationError):
                AIFallbackChainService.generate_completion(
                    messages=[{"role": "user", "content": "hello"}],
                    preferred_provider="ollama",
                    fallback_enabled=False,
                )

        factory.assert_called_once_with("ollama", user=None)

    def test_streaming_can_fallback_after_preferred_provider_configuration_error(self):
        from ai.exceptions import AIConfigurationError
        from ai.services.core import AIFallbackChainService

        class WorkingStreamProvider:
            def generate_stream(self, **kwargs):
                yield {
                    "delta": "stream fallback",
                    "provider": "openai",
                    "model": "gpt-4o-mini",
                }

        def provider_factory(name, user=None):
            if name == "ollama":
                raise AIConfigurationError("Ollama endpoint is unavailable.")
            return WorkingStreamProvider()

        with override_settings(
            OPENAI_API_KEY="configured-test-key",
            AI_MAX_PROVIDER_ATTEMPTS=5,
        ):
            with patch("ai.providers.get_ai_provider", side_effect=provider_factory):
                chunks = list(AIFallbackChainService.stream_completion(
                    messages=[{"role": "user", "content": "hello"}],
                    preferred_provider="ollama",
                    fallback_enabled=True,
                ))

        self.assertEqual("".join(chunk["delta"] for chunk in chunks), "stream fallback")
        self.assertEqual(chunks[0]["provider"], "openai")


class AsyncLearningTaskOwnershipTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="async-owner@example.com",
            password="StrongPass123",
        )
        self.other_user = get_user_model().objects.create_user(
            email="async-other@example.com",
            password="StrongPass123",
        )

    def test_pending_task_is_visible_only_to_audited_owner(self):
        from rest_framework.test import APIRequestFactory, force_authenticate
        from ai.models import AiAuditLog
        from ai.api.views import AITaskStatusView

        AiAuditLog.objects.create(
            user=self.user,
            action="learning_async_submitted",
            resource="task-pending-123",
            details={"task_id": "task-pending-123", "status": "pending"},
        )
        factory = APIRequestFactory()
        request = factory.get("/api/ai/tasks/task-pending-123/")
        force_authenticate(request, user=self.user)

        class PendingResult:
            state = "PENDING"
            status = "PENDING"
            info = None

            @staticmethod
            def successful():
                return False

            @staticmethod
            def failed():
                return False

        from celery import current_app
        current_app.tasks  # finalize the Celery app before AsyncResult is patched
        with patch("celery.result.AsyncResult", return_value=PendingResult()):
            response = AITaskStatusView.as_view()(request, task_id="task-pending-123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "pending")

        request = factory.get("/api/ai/tasks/task-pending-123/")
        force_authenticate(request, user=self.other_user)
        with patch("celery.result.AsyncResult", return_value=PendingResult()):
            response = AITaskStatusView.as_view()(request, task_id="task-pending-123")
        self.assertEqual(response.status_code, 404)


class ChatIdempotencyRegressionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="chat-idempotency@example.com",
            password="StrongPass123",
        )

    def test_successful_request_key_replays_saved_assistant_message(self):
        from ai.models import AIConversation, AIExecution, AIMessage
        from ai.services.core import AIService

        conversation = AIConversation.objects.create(
            user=self.user,
            title="Existing conversation",
            provider="openai",
            model="gpt-4o-mini",
        )
        assistant = AIMessage.objects.create(
            conversation=conversation,
            role=AIMessage.ROLE_ASSISTANT,
            content="Previously generated response",
            provider="openai",
            model="gpt-4o-mini",
        )
        AIExecution.objects.create(
            user=self.user,
            conversation=conversation,
            task_type="chat",
            status=AIExecution.Status.SUCCEEDED,
            idempotency_key="same-request-key",
            metadata={"assistant_message_id": assistant.pk},
        )

        result = AIService(self.user).chat(
            message="same user request",
            idempotency_key="same-request-key",
        )
        self.assertTrue(result["replayed"])
        self.assertEqual(result["assistant_message"].pk, assistant.pk)
        self.assertEqual(result["assistant_message"].content, "Previously generated response")
        self.assertEqual(conversation.messages.count(), 1)

    def test_running_request_key_is_not_executed_twice(self):
        from ai.exceptions import AIError
        from ai.models import AIExecution
        from ai.services.core import AIService

        AIExecution.objects.create(
            user=self.user,
            task_type="chat",
            status=AIExecution.Status.RUNNING,
            idempotency_key="in-flight-key",
        )
        with self.assertRaises(AIError) as raised:
            AIService(self.user).chat(
                message="same user request",
                idempotency_key="in-flight-key",
            )
        self.assertEqual(raised.exception.category, "request_in_progress")
