from django.contrib.auth import get_user_model
from django.test import TestCase

from agents.models import Agent, AgentExecution, AgentRun
from agents.services import agent_service, execution_service

User = get_user_model()


class FakeExecutor:
    def __init__(self, result=None, error=None):
        self.result, self.error, self.calls = result, error, []

    def execute(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return self.result


class AgentServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="agent-svc@example.com", password="pw-12345-test", name="Owner")
        self.agent = Agent.objects.create(user=self.user, name="A", status=Agent.STATUS_ACTIVE,
                                          requires_approval=False, system_prompt="Be brief.")

    def test_configuration_versions_increment(self):
        first = agent_service.create_configuration(agent=self.agent)
        second = agent_service.create_configuration(agent=self.agent, temperature=0.7)
        self.assertEqual((first.version, second.version), (1, 2))

    def test_only_one_configuration_is_active(self):
        first = agent_service.create_configuration(agent=self.agent)
        second = agent_service.create_configuration(agent=self.agent)
        agent_service.activate_configuration(first)
        agent_service.activate_configuration(second)
        first.refresh_from_db()
        second.refresh_from_db()
        self.assertFalse(first.is_active)
        self.assertTrue(second.is_active)
        self.assertEqual(agent_service.get_active_configuration(self.agent), second)

    def test_run_requires_active_agent(self):
        draft = Agent.objects.create(user=self.user, name="Draft")
        with self.assertRaises(execution_service.AgentRunError):
            execution_service.create_run(user=self.user, agent=draft, goal="x")

    def test_run_of_another_users_agent_is_rejected(self):
        other = User.objects.create_user(email="agent-svc2@example.com", password="pw-12345-test", name="Other")
        with self.assertRaises(execution_service.AgentRunError):
            execution_service.create_run(user=other, agent=self.agent, goal="x")

    def test_approval_flow(self):
        self.agent.requires_approval = True
        self.agent.save()
        run = execution_service.create_run(user=self.user, agent=self.agent, goal="Plan")
        self.assertEqual(run.status, AgentRun.STATUS_AWAITING_APPROVAL)
        with self.assertRaises(execution_service.AgentRunError):
            execution_service.execute_run(run, executor=FakeExecutor({"content": "x"}))
        run = execution_service.approve_run(run)
        self.assertEqual(run.status, AgentRun.STATUS_PENDING)
        self.assertIsNotNone(run.approved_at)

    def test_execute_success_records_result_and_step(self):
        agent_service.activate_configuration(agent_service.create_configuration(agent=self.agent, temperature=0.5))
        run = execution_service.create_run(user=self.user, agent=self.agent, goal="Summarise", input_data={"k": 1})
        executor = FakeExecutor({"content": "Done", "provider": "openai", "model": "m"})
        run = execution_service.execute_run(run, executor=executor)
        self.assertEqual(run.status, AgentRun.STATUS_SUCCEEDED)
        self.assertEqual(run.result["content"], "Done")
        self.assertIsNotNone(run.finished_at)
        step = AgentExecution.objects.get(run=run)
        self.assertEqual(step.status, AgentExecution.STATUS_SUCCEEDED)
        self.assertEqual(executor.calls[0]["temperature"], 0.5)
        self.assertEqual(executor.calls[0]["messages"][0], {"role": "system", "content": "Be brief."})

    def test_execute_failure_is_reported_not_faked(self):
        run = execution_service.create_run(user=self.user, agent=self.agent, goal="Summarise")
        run = execution_service.execute_run(run, executor=FakeExecutor(error=ValueError("No provider")))
        self.assertEqual(run.status, AgentRun.STATUS_FAILED)
        self.assertIn("No provider", run.error)
        self.assertEqual(AgentExecution.objects.get(run=run).status, AgentExecution.STATUS_FAILED)

    def test_cancel_rejects_finished_runs(self):
        run = execution_service.create_run(user=self.user, agent=self.agent, goal="x")
        run = execution_service.cancel_run(run)
        self.assertEqual(run.status, AgentRun.STATUS_CANCELLED)
        with self.assertRaises(execution_service.AgentRunError):
            execution_service.cancel_run(run)
