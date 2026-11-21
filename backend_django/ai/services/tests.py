"""Focused contract tests for the modular AI services."""
from django.test import SimpleTestCase, TestCase
from ai.services.task_planner import TaskPlanner
from ai.services.workflow_service import WorkflowService


class TaskPlannerTests(SimpleTestCase):
    def test_proposal_requires_title_and_confirmation(self):
        proposal = TaskPlanner.proposal(title="  Build API  ", steps=[" test ", ""])
        self.assertEqual(proposal["title"], "Build API")
        self.assertEqual(proposal["steps"], ["test"])
        self.assertTrue(proposal["requires_confirmation"])

    def test_empty_title_is_rejected(self):
        with self.assertRaises(ValueError):
            TaskPlanner.proposal(title=" ")


class WorkflowServiceTests(SimpleTestCase):
    def test_valid_graph(self):
        result = WorkflowService.validate({
            "nodes": [{"id": "a"}, {"id": "b"}],
            "edges": [{"source": "a", "target": "b"}],
        })
        self.assertTrue(result["valid"])

    def test_unknown_edge_endpoint_is_rejected(self):
        result = WorkflowService.validate({
            "nodes": [{"id": "a"}],
            "edges": [{"source": "a", "target": "missing"}],
        })
        self.assertFalse(result["valid"])


class AIFallbackResponseTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.user = get_user_model().objects.create_user(
            email="fallback-test@example.com", password="StrongPass123")

    def test_invalid_primary_response_moves_to_configured_fallback(self):
        from unittest.mock import patch
        from django.test import override_settings
        from ai.services.core import AIFallbackChainService
        from ai.services.exceptions import AIResponseError

        class Provider:
            def __init__(self, name):
                self.name = name

            def generate(self, **kwargs):
                if self.name == "ollama":
                    raise AIResponseError("invalid JSON")
                return {"content": "fallback response", "provider": self.name, "model": "test-model"}

        def provider_factory(name, user=None):
            return Provider(name)

        with override_settings(OPENAI_API_KEY="test-key", AI_MAX_PROVIDER_ATTEMPTS=3):
            with patch("ai.providers.get_ai_provider", side_effect=provider_factory):
                result = AIFallbackChainService.generate_completion(
                    messages=[{"role": "user", "content": "hello"}],
                    user=self.user,
                    preferred_provider="ollama",
                )

        self.assertEqual(result["provider"], "openai")
        self.assertEqual(result["content"], "fallback response")


class FallbackUserIsolationTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        from ai.models import AIProviderCredential
        User = get_user_model()
        self.user = User.objects.create_user(
            email="fallback-owner@example.com", password="StrongPass123"
        )
        self.other_user = User.objects.create_user(
            email="fallback-other@example.com", password="StrongPass123"
        )
        credential = AIProviderCredential(user=self.other_user, provider="openai")
        credential.set_api_key("other-users-secret")
        credential.save()

    def test_other_users_credentials_are_not_used_as_fallback(self):
        from unittest.mock import patch
        from django.test import override_settings
        from ai.services.core import AIFallbackChainService

        class Provider:
            def __init__(self, name):
                self.name = name

            def generate(self, **kwargs):
                return {"content": "local response", "provider": self.name, "model": "local"}

        def factory(name, user=None):
            return Provider(name)

        with override_settings(
            OPENAI_API_KEY="", GEMINI_API_KEY="", GOOGLE_API_KEY="",
            DEEPSEEK_API_KEY="", OPENROUTER_API_KEY="",
            AI_MAX_PROVIDER_ATTEMPTS=3,
        ):
            with patch("ai.providers.get_ai_provider", side_effect=factory) as mocked:
                result = AIFallbackChainService.generate_completion(
                    messages=[{"role": "user", "content": "hello"}],
                    user=self.user,
                    preferred_provider="openai",
                )

        self.assertEqual(result["provider"], "ollama")
        attempted = [call.args[0] for call in mocked.call_args_list]
        self.assertNotIn("openai", attempted)

    def test_user_credential_is_available_only_to_its_owner(self):
        from ai.providers import get_ai_provider
        from ai.providers.openai import OpenAIProvider

        provider = get_ai_provider("openai", user=self.other_user)
        self.assertIsInstance(provider, OpenAIProvider)
        self.assertEqual(provider.api_key, "other-users-secret")


class OpenAIRequestAuthenticationTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        from ai.models import AIProviderCredential
        self.user = get_user_model().objects.create_user(
            email="openai-auth-test@example.com", password="StrongPass123"
        )
        credential = AIProviderCredential(user=self.user, provider="openai")
        credential.set_api_key("test-openai-key")
        credential.save()

    def test_openai_request_sends_bearer_header_and_does_not_follow_redirects(self):
        from unittest.mock import patch, Mock
        from ai.providers import get_ai_provider

        response = Mock()
        response.ok = True
        response.json.return_value = {
            "choices": [{"message": {"content": "ok"}}]
        }
        with patch("ai.providers.openai.requests.post", return_value=response) as post:
            result = get_ai_provider("openai", user=self.user).generate(
                messages=[{"role": "user", "content": "hello"}]
            )

        self.assertEqual(result["content"], "ok")
        self.assertEqual(
            post.call_args.kwargs["headers"]["Authorization"],
            "Bearer test-openai-key",
        )
        self.assertFalse(post.call_args.kwargs["allow_redirects"])

    def test_openai_401_error_does_not_echo_response_body(self):
        from unittest.mock import patch, Mock
        from ai.providers import get_ai_provider
        from ai.services.exceptions import AIProviderError

        response = Mock()
        response.ok = False
        response.status_code = 401
        response.text = '{"error":"secret-provider-detail"}'
        with patch("ai.providers.openai.requests.post", return_value=response):
            with self.assertRaises(AIProviderError) as caught:
                get_ai_provider("openai", user=self.user).generate(
                    messages=[{"role": "user", "content": "hello"}]
                )

        self.assertIn("HTTP 401", str(caught.exception))
        self.assertNotIn("secret-provider-detail", str(caught.exception))



class ProviderFailureClassificationTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.user = get_user_model().objects.create_user(
            email="provider-classification@example.com", password="StrongPass123"
        )

    def test_provider_specific_invalid_request_falls_back(self):
        from unittest.mock import patch
        from django.test import override_settings
        from ai.services.core import AIFallbackChainService
        from ai.services.exceptions import AIProviderError

        class Provider:
            def __init__(self, name):
                self.name = name

            def generate(self, **kwargs):
                if self.name == "ollama":
                    raise AIProviderError(
                        "Request rejected.", category="invalid_request_or_model",
                        retryable=False, status_code=404,
                    )
                return {"content": "fallback", "provider": self.name, "model": "fallback-model"}

        with override_settings(OPENAI_API_KEY="configured", AI_MAX_PROVIDER_ATTEMPTS=3):
            with patch("ai.providers.get_ai_provider", side_effect=lambda name, user=None: Provider(name)):
                result = AIFallbackChainService.generate_completion(
                    messages=[{"role": "user", "content": "hello"}],
                    user=self.user, preferred_provider="ollama",
                )

        self.assertEqual(result["provider"], "openai")

    def test_quota_exhaustion_is_not_retryable(self):
        from unittest.mock import Mock
        from ai.providers.base import _provider_http_error

        response = Mock()
        response.status_code = 429
        response.headers = {}
        response.json.return_value = {"error": {"code": "insufficient_quota"}}
        error = _provider_http_error("openai", response)

        self.assertEqual(error.category, "quota_exhausted")
        self.assertFalse(error.retryable)

    def test_http_failure_classification_is_safe_and_retry_aware(self):
        from unittest.mock import Mock
        from ai.providers.base import _provider_http_error

        response = Mock()
        response.status_code = 429
        response.headers = {"Retry-After": "12"}
        response.text = "private response body"
        error = _provider_http_error("openai", response)

        self.assertEqual(error.category, "rate_limit")
        self.assertTrue(error.retryable)
        self.assertEqual(error.retry_after, 12)
        self.assertNotIn("private response body", str(error))

    def test_auth_failure_is_not_retried_for_same_provider(self):
        from unittest.mock import Mock
        from ai.providers.base import _provider_http_error

        response = Mock()
        response.status_code = 401
        response.headers = {}
        error = _provider_http_error("openai", response)

        self.assertEqual(error.category, "authentication")
        self.assertFalse(error.retryable)
