"""End-to-end provider switching/fallback tests through the real /api/ai/chat/ endpoint.

A real local HTTP server emulates Ollama and an OpenAI-compatible API, so the
full chain (view -> AIService -> AIFallbackChainService -> provider adapter ->
`requests` -> socket) is exercised without any mocks of the adapters.
"""
import json
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework.test import APITestCase

from ai.models import AIExecution, AIProviderCredential, AISettings


class FakeProviders:
    """Mutable behaviour switches shared with the handler."""
    ollama = "ok"       # ok | 500
    ollama_models = {"gemma3:4b"}
    openai = "ok"       # ok | 401 | 429
    hits = []


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body):
        raw = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        payload = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        FakeProviders.hits.append((self.path, payload.get("model")))
        if self.path == "/api/chat":
            if FakeProviders.ollama == "500":
                return self._send(500, {"error": "boom"})
            if payload.get("model") not in FakeProviders.ollama_models:
                return self._send(404, {"error": "model not found"})
            return self._send(200, {"message": {"role": "assistant", "content": "hi from ollama"}, "done": True})
        if self.path == "/v1/chat/completions":
            if FakeProviders.openai == "401":
                return self._send(401, {"error": {"code": "invalid_api_key"}})
            if FakeProviders.openai == "429":
                return self._send(429, {"error": {"code": "rate_limit"}})
            if payload.get("stream"):
                raw = (b'data: {"choices":[{"delta":{"content":"hi from openai"}}]}\n\n'
                       b'data: [DONE]\n\n')
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
                return
            return self._send(200, {"choices": [{"message": {"content": "hi from openai"}}]})
        self._send(404, {})


def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p


@override_settings(AI_RETRY_BACKOFF_SECONDS=0.05, AI_MAX_RETRIES_PER_PROVIDER=1,
                   AI_MAX_PROVIDER_ATTEMPTS=5, AI_TOTAL_DEADLINE_SECONDS=30)
class ProviderSwitchingE2E(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.server.server_address[1]
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); super().tearDownClass()

    def setUp(self):
        FakeProviders.ollama, FakeProviders.openai = "ok", "ok"
        FakeProviders.ollama_models = {"gemma3:4b"}
        FakeProviders.hits = []
        self.user = get_user_model().objects.create_user(email="e2e@example.com", password="StrongPass123")
        self.client.force_authenticate(self.user)
        self.settings_cm = override_settings(OLLAMA_BASE_URL=self.base, OLLAMA_MODEL="gemma3:4b",
                                             OPENAI_API_KEY="", AI_DEFAULT_PROVIDER="ollama")
        self.settings_cm.enable()
        self.addCleanup(self.settings_cm.disable)

    def add_openai(self, priority=10):
        cred = AIProviderCredential(user=self.user, provider="openai",
                                    metadata={"base_url": self.base + "/v1", "priority": priority, "enabled": True})
        cred.set_api_key("sk-test-key"); cred.save()

    def chat(self, **extra):
        return self.client.post("/api/ai/chat/", {"message": "hello", **extra}, format="json")

    def test_01_primary_local_ollama_works(self):
        r = self.chat(provider="ollama")
        self.assertEqual(r.status_code, 200, r.content)
        self.assertEqual(r.data["message"]["provider"], "ollama")

    def test_02_primary_down_falls_back_to_openai(self):
        self.add_openai()
        FakeProviders.ollama = "500"
        r = self.chat(provider="ollama")
        self.assertEqual(r.status_code, 200, r.content)
        self.assertEqual(r.data["message"]["provider"], "openai")
        ex = AIExecution.objects.filter(user=self.user).latest("id")
        self.assertEqual((ex.status, ex.fallback_count), ("succeeded", 1))

    def test_03_primary_recovers_after_fallback_in_same_conversation(self):
        self.add_openai()
        AISettings.objects.update_or_create(user=self.user, defaults={"preferred_provider": "ollama"})
        FakeProviders.ollama = "500"
        first = self.chat()
        self.assertEqual(first.data["message"]["provider"], "openai")
        FakeProviders.ollama = "ok"
        second = self.chat(conversation_id=first.data["conversation_id"])
        self.assertEqual(second.status_code, 200, second.content)
        self.assertEqual(second.data["message"]["provider"], "ollama",
                         "user's configured primary must be preferred again once healthy")

    def test_04_stale_model_from_other_provider_does_not_break_primary(self):
        self.add_openai()
        AISettings.objects.update_or_create(user=self.user, defaults={
            "preferred_provider": "ollama", "preferred_model": "gpt-4o-mini"})
        r = self.chat()
        self.assertEqual(r.status_code, 200, r.content)
        self.assertEqual(r.data["message"]["provider"], "ollama",
                         "a model that belongs to another provider must not disable the primary")

    def test_05_fallback_disabled_reports_primary_failure(self):
        self.add_openai()
        AISettings.objects.update_or_create(user=self.user, defaults={"preferred_provider": "ollama", "fallback_enabled": False})
        FakeProviders.ollama = "500"
        r = self.chat()
        self.assertEqual(r.status_code, 502)
        self.assertFalse(any(p == "/v1/chat/completions" for p, _ in FakeProviders.hits))

    def test_06_connection_refused_primary_then_fallback(self):
        self.add_openai()
        with override_settings(OLLAMA_BASE_URL=f"http://127.0.0.1:{free_port()}"):
            r = self.chat(provider="ollama")
        self.assertEqual(r.status_code, 200, r.content)
        self.assertEqual(r.data["message"]["provider"], "openai")

    def test_07_invalid_credentials_on_primary_is_not_silently_swallowed(self):
        self.add_openai()
        FakeProviders.openai = "401"
        r = self.chat(provider="openai")
        self.assertEqual(r.status_code, 502)
        self.assertEqual(r.data["error_code"], "authentication")

    def test_08_all_providers_fail_ends_with_failed_execution_no_loop(self):
        self.add_openai()
        FakeProviders.ollama, FakeProviders.openai = "500", "429"
        r = self.chat(provider="ollama")
        self.assertEqual(r.status_code, 502)
        self.assertLessEqual(len(FakeProviders.hits), 5)
        ex = AIExecution.objects.filter(user=self.user).latest("id")
        self.assertEqual(ex.status, "failed")

    # ---- streaming endpoint (/api/ai/chat/stream/) shares the same selection rules
    def stream(self, **extra):
        r = self.client.post("/api/ai/chat/stream/", {"message": "hello", **extra}, format="json")
        body = b"".join(r.streaming_content).decode() if hasattr(r, "streaming_content") else ""
        return r, body

    def test_09_stream_stale_model_recovers_on_primary(self):
        AISettings.objects.update_or_create(user=self.user, defaults={
            "preferred_provider": "ollama", "preferred_model": "gpt-4o-mini"})
        r, body = self.stream()
        self.assertEqual(r.status_code, 200)
        self.assertIn("hi from ollama", body)

    def test_10_stream_fallback_does_not_demote_primary(self):
        from ai.models import AIConversation
        self.add_openai()
        AISettings.objects.update_or_create(user=self.user, defaults={"preferred_provider": "ollama"})
        FakeProviders.ollama = "500"
        r, body = self.stream()
        self.assertEqual(r.status_code, 200)
        self.assertIn("hi from openai", body, body[:600])
        conv = AIConversation.objects.filter(user=self.user).latest("id")
        self.assertEqual(conv.provider, "ollama", "stream fallback must not overwrite the selected primary")
