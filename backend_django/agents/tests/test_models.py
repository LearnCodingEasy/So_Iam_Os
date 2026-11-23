from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from agents.models import Agent, AgentConfiguration, AgentRun

User = get_user_model()


class AgentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="agent-models@example.com", password="pw-12345-test", name="Owner")

    def test_new_agent_defaults_to_draft_and_requires_approval(self):
        agent = Agent.objects.create(user=self.user, name="Researcher")
        self.assertEqual(agent.status, Agent.STATUS_DRAFT)
        self.assertTrue(agent.requires_approval)
        self.assertEqual(str(agent), "Researcher")

    def test_configuration_version_is_unique_per_agent(self):
        agent = Agent.objects.create(user=self.user, name="Researcher")
        AgentConfiguration.objects.create(agent=agent, version=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            AgentConfiguration.objects.create(agent=agent, version=1)

    def test_terminal_statuses_are_declared(self):
        self.assertEqual(set(AgentRun.TERMINAL_STATUSES), {"succeeded", "failed", "cancelled"})
