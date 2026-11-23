from django.contrib.auth import get_user_model
from django.test import TestCase

from codex.models import ProjectRegistry, ProtectedItem, CodexWorkflowStep, LocalAIJob
from codex.services.extensions import bootstrap_workflow, freeze_item, build_prompt


class CodexExtensionTests(TestCase):
    def setUp(self):
        self.project = ProjectRegistry.objects.create(key="test-project", name="Test Project")
        self.user = get_user_model().objects.create_user(username="codex-test", password="test-password")

    def test_workflow_bootstrap_has_five_gated_steps(self):
        result = bootstrap_workflow(self.project)
        self.assertEqual(result["total"], 5)
        self.assertEqual(CodexWorkflowStep.objects.filter(project=self.project).count(), 5)

    def test_protected_item_is_frozen(self):
        item = freeze_item(self.project, self.user, {
            "key": "file:frontend_vue/src/views/Codex/CodexView.vue",
            "item_type": "file",
            "path": "frontend_vue/src/views/Codex/CodexView.vue",
            "reason": "Approved release artifact",
        })
        self.assertTrue(item.approved)
        self.assertTrue(item.frozen)
        self.assertEqual(ProtectedItem.objects.filter(project=self.project).count(), 1)

    def test_prompt_contains_governance_contract(self):
        prompt = build_prompt(self.project, "bug", "Fix a Codex API regression", ["backend_django/codex/views.py"])
        self.assertIn("protected", prompt.lower())
        self.assertIn("backend_django/codex/views.py", prompt)
