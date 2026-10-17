from django.test import TestCase
from codex.catalog import FEATURES, TOOLS, AGENTS
from codex.models import ProjectRegistry, CodexFeatureDefinition, CodexToolDefinition, CodexAgentDefinition
from codex.services.capabilities import ensure_capability_catalog, execute_tool, execute_agent, catalog_summary

class CapabilityRegistryTests(TestCase):
    def setUp(self):
        self.project = ProjectRegistry.objects.create(key='test_so_iam_os', name='TEST')
        ensure_capability_catalog(self.project)

    def test_catalog_has_exact_requested_counts(self):
        self.assertEqual(len(FEATURES), 300)
        self.assertEqual(len(TOOLS), 300)
        self.assertEqual(len(AGENTS), 300)
        self.assertEqual(CodexFeatureDefinition.objects.filter(project=self.project).count(), 300)
        self.assertEqual(CodexToolDefinition.objects.filter(project=self.project).count(), 300)
        self.assertEqual(CodexAgentDefinition.objects.filter(project=self.project).count(), 300)

    def test_catalog_keys_are_unique(self):
        for model in (CodexFeatureDefinition, CodexToolDefinition, CodexAgentDefinition):
            keys=list(model.objects.filter(project=self.project).values_list('key', flat=True))
            self.assertEqual(len(keys), len(set(keys)))

    def test_every_tool_has_executable_contract(self):
        for definition in CodexToolDefinition.objects.filter(project=self.project):
            result=execute_tool(self.project, None, definition.key, {})
            self.assertEqual(result['validation']['registered'], True, definition.key)
            self.assertEqual(result['status'], 'completed', definition.key)

    def test_every_agent_has_executable_contract(self):
        for definition in CodexAgentDefinition.objects.filter(project=self.project):
            result=execute_agent(self.project, None, definition.key, {'request':'contract smoke test'})
            self.assertEqual(result['validation']['registered'], True, definition.key)
            self.assertEqual(result['status'], 'completed', definition.key)

    def test_summary_matches_contract(self):
        summary=catalog_summary(self.project)
        self.assertEqual(summary['features'], 300)
        self.assertEqual(summary['tools'], 300)
        self.assertEqual(summary['agents'], 300)
