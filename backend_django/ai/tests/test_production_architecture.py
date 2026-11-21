from django.test import SimpleTestCase

class AIArchitectureTests(SimpleTestCase):
    def test_capabilities_count(self):
        from ai.services.capabilities import get_capabilities
        self.assertEqual(len(get_capabilities()), 50)

    def test_provider_registry(self):
        from ai.providers import get_ai_provider
        from ai.providers.ollama import OllamaProvider
        self.assertIsNotNone(get_ai_provider)
        self.assertEqual(OllamaProvider.name, 'ollama')

    def test_model_package_exports(self):
        from ai.models import AISettings, AIConversation, AIExecution, AIFeedback
        self.assertTrue(all([AISettings, AIConversation, AIExecution, AIFeedback]))
