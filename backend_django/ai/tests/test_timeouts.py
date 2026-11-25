"""Timeout hierarchy: request -> agent -> provider -> global -> safe default."""
from unittest.mock import patch

import requests
from django.test import SimpleTestCase, override_settings

from ai.exceptions import AIProviderError
from ai.providers.ollama import OllamaProvider, _timeout_error
from ai.services.timeouts import (
    celery_limits, resolve_timeout, user_setting_timeout, validate_timeout,
)


@override_settings(
    AI_TIMEOUT_MIN_SECONDS=5, AI_TIMEOUT_MAX_SECONDS=600,
    AI_PROVIDER_TIMEOUT_SECONDS=35, AI_PROVIDER_TIMEOUTS={"ollama": 120},
)
class TimeoutResolutionTests(SimpleTestCase):
    def test_request_wins(self):
        self.assertEqual(resolve_timeout(request=180, agent=90, provider="ollama"), (180, "request"))

    def test_agent_beats_provider(self):
        self.assertEqual(resolve_timeout(agent=90, provider="ollama"), (90, "agent"))

    def test_provider_beats_global(self):
        self.assertEqual(resolve_timeout(provider="ollama"), (120, "provider"))

    def test_global_used_for_provider_without_override(self):
        self.assertEqual(resolve_timeout(provider="openai"), (35, "global"))

    @override_settings(AI_PROVIDER_TIMEOUT_SECONDS=None, AI_PROVIDER_TIMEOUTS={})
    def test_safe_default(self):
        self.assertEqual(resolve_timeout(provider="openai"), (60, "default"))

    def test_request_out_of_bounds_rejected(self):
        for bad in (0, 1, 4, 601, 10**6, -5, "abc", True):
            with self.assertRaises(ValueError, msg=repr(bad)):
                resolve_timeout(request=bad)

    def test_bounds_inclusive(self):
        self.assertEqual(validate_timeout(5), 5)
        self.assertEqual(validate_timeout("600"), 600)

    def test_invalid_config_layer_is_skipped_not_fatal(self):
        self.assertEqual(resolve_timeout(agent=99999, provider="ollama"), (120, "provider"))

    def test_untouched_legacy_user_setting_is_unset(self):
        class S: timeout_seconds = 35
        self.assertIsNone(user_setting_timeout(S))
        S.timeout_seconds = 240
        self.assertEqual(user_setting_timeout(S), 240)

    def test_celery_limits_exceed_max_timeout(self):
        soft, hard = celery_limits()
        self.assertGreater(soft, 600)
        self.assertGreater(hard, soft)


class OllamaTimeoutClassificationTests(SimpleTestCase):
    def test_connect_vs_read(self):
        c = _timeout_error(requests.ConnectTimeout(), (5, 120))
        r = _timeout_error(requests.ReadTimeout(), (5, 120))
        self.assertEqual((c.category, c.timeout_kind), ("timeout", "connect"))
        self.assertEqual((r.category, r.timeout_kind), ("timeout", "read"))
        self.assertIn("120s", str(r))
        self.assertIn("5s", str(c))

    @override_settings(OLLAMA_BASE_URL="http://127.0.0.1:11434")
    def test_provider_passes_requested_timeout_to_http_client(self):
        provider = OllamaProvider()
        with patch("ai.providers.ollama.requests.post", side_effect=requests.ReadTimeout()) as post:
            with self.assertRaises(AIProviderError) as ctx:
                provider.generate([{"role": "user", "content": "hi"}], timeout_seconds=180)
        self.assertEqual(post.call_args.kwargs["timeout"][1], 180)
        self.assertEqual(ctx.exception.timeout_kind, "read")
