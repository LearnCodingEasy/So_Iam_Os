from unittest.mock import Mock, patch

from django.test import SimpleTestCase, override_settings

from ai.providers.openai import OpenAIProvider


class OpenAIProviderAdapterTests(SimpleTestCase):
    @override_settings(OPENAI_API_KEY="test-key", OPENAI_BASE_URL="https://api.openai.com/v1")
    @patch("ai.providers.openai.requests.post")
    def test_reasoning_models_use_max_completion_tokens_without_temperature(self, mock_post):
        response = Mock()
        response.ok = True
        response.json.return_value = {
            "choices": [{"message": {"content": "OK"}}]
        }
        mock_post.return_value = response

        provider = OpenAIProvider()
        provider.generate(
            messages=[{"role": "user", "content": "Hello"}],
            model="gpt-5.1",
            temperature=0.4,
            max_tokens=20,
            timeout_seconds=5,
        )

        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["max_completion_tokens"], 20)
        self.assertNotIn("max_tokens", payload)
        self.assertNotIn("temperature", payload)

    @override_settings(OPENAI_API_KEY="test-key", OPENAI_BASE_URL="https://api.openai.com/v1")
    @patch("ai.providers.openai.requests.post")
    def test_standard_models_keep_max_tokens_and_temperature(self, mock_post):
        response = Mock()
        response.ok = True
        response.json.return_value = {
            "choices": [{"message": {"content": "OK"}}]
        }
        mock_post.return_value = response

        provider = OpenAIProvider()
        provider.generate(
            messages=[{"role": "user", "content": "Hello"}],
            model="gpt-4o-mini",
            temperature=0.3,
            max_tokens=20,
            timeout_seconds=5,
        )

        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["max_tokens"], 20)
        self.assertEqual(payload["temperature"], 0.3)
