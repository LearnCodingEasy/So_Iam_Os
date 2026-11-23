from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from agents.models import Agent
from agents.tests.test_services import FakeExecutor

User = get_user_model()


class AgentApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="agent-api@example.com", password="pw-12345-test", name="Owner")
        self.other = User.objects.create_user(email="agent-api2@example.com", password="pw-12345-test", name="Other")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def _agent(self, **extra):
        data = {"name": "Researcher", "status": "active", "requires_approval": False}
        data.update(extra)
        return self.client.post("/api/agents/agents/", data, format="json")

    def test_authentication_is_required(self):
        response = APIClient().get("/api/agents/agents/")
        self.assertEqual(response.status_code, 401)

    def test_agents_are_isolated_per_user(self):
        Agent.objects.create(user=self.other, name="Not mine")
        self.assertEqual(self._agent().status_code, 201)
        names = [row["name"] for row in self.client.get("/api/agents/agents/").json()]
        self.assertEqual(names, ["Researcher"])
        foreign = Agent.objects.get(name="Not mine")
        self.assertEqual(self.client.get("/api/agents/agents/%s/" % foreign.pk).status_code, 404)

    def test_user_field_cannot_be_forged(self):
        response = self._agent(user=str(self.other.pk))
        self.assertEqual(Agent.objects.get(pk=response.json()["id"]).user, self.user)

    def test_blank_name_rejected(self):
        self.assertEqual(self._agent(name="  ").status_code, 400)

    def test_configuration_for_foreign_agent_is_rejected(self):
        foreign = Agent.objects.create(user=self.other, name="Foreign")
        response = self.client.post("/api/agents/configurations/", {"agent": foreign.pk}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_configuration_versioning_and_activation(self):
        agent_id = self._agent().json()["id"]
        first = self.client.post("/api/agents/configurations/", {"agent": agent_id}, format="json").json()
        second = self.client.post("/api/agents/configurations/", {"agent": agent_id, "max_steps": 5}, format="json").json()
        self.assertEqual((first["version"], second["version"]), (1, 2))
        active = self.client.post("/api/agents/configurations/%s/activate/" % second["id"]).json()
        self.assertTrue(active["is_active"])
        bad = self.client.post("/api/agents/configurations/", {"agent": agent_id, "temperature": 9}, format="json")
        self.assertEqual(bad.status_code, 400)

    def test_run_execute_flow_and_executions_are_read_only(self):
        agent_id = self._agent(requires_approval=True).json()["id"]
        run = self.client.post("/api/agents/runs/", {"agent": agent_id, "goal": "Summarise"}, format="json").json()
        self.assertEqual(run["status"], "awaiting_approval")
        too_early = self.client.post("/api/agents/runs/%s/execute/" % run["id"])
        self.assertEqual(too_early.status_code, 409)
        self.assertEqual(self.client.post("/api/agents/runs/%s/approve/" % run["id"]).json()["status"], "pending")
        with patch("agents.services.execution_service._default_executor",
                   return_value=FakeExecutor({"content": "Summary"})):
            done = self.client.post("/api/agents/runs/%s/execute/" % run["id"]).json()
        self.assertEqual(done["status"], "succeeded")
        steps = self.client.get("/api/agents/executions/?run=%s" % run["id"]).json()
        self.assertEqual(len(steps), 1)
        self.assertEqual(self.client.post("/api/agents/executions/", {}, format="json").status_code, 405)

    def test_run_for_draft_agent_is_rejected(self):
        agent_id = self._agent(status="draft").json()["id"]
        response = self.client.post("/api/agents/runs/", {"agent": agent_id, "goal": "x"}, format="json")
        self.assertEqual(response.status_code, 400)
