"""Focused contract tests for the modular AI services."""
from django.test import SimpleTestCase
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
