from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch
from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from goals.models import Goal, GoalActivity, GoalMilestone, GoalPlanProposal
from goals.services import GoalAnalyticsService, GoalService
from goals.services.coach import GoalCoachService
from goals.api.serializers import GoalMilestoneSerializer
from tasks.models import Task

User = get_user_model()


class GoalServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="goal-owner@example.test", password="safe-test-password", name="Goal Owner")
        self.goal = Goal.objects.create(user=self.user, title="Learn Django", target_date=timezone.localdate() + timedelta(days=60))

    def test_progress_validation_and_completion(self):
        GoalService.update_progress(self.goal, 45, self.user)
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.progress_percent, 45)
        with self.assertRaises(ValueError):
            GoalService.update_progress(self.goal, 101, self.user)
        GoalService.complete(self.goal, self.user, "All criteria met")
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.status, Goal.Status.COMPLETED)
        self.assertEqual(self.goal.progress_percent, 100)
        self.assertTrue(self.goal.completed_at)

    def test_invalid_status_transition_is_rejected(self):
        self.goal.status = Goal.Status.ARCHIVED
        self.goal.save(update_fields=["status"])
        with self.assertRaises(ValueError):
            GoalService.set_status(self.goal, Goal.Status.ACTIVE, self.user)

    def test_weighted_milestone_progress(self):
        GoalMilestone.objects.create(goal=self.goal, title="Foundation", sequence=0, weight=Decimal("25"), progress_percent=100)
        GoalMilestone.objects.create(goal=self.goal, title="Advanced", sequence=1, weight=Decimal("75"), progress_percent=40)
        GoalService.recalculate_from_milestones(self.goal)
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.progress_percent, 55)

    def test_task_completion_updates_goal_progress(self):
        first = Task.objects.create(user=self.user, goal=self.goal, title="Install Django", scheduled_date=timezone.localdate())
        second = Task.objects.create(user=self.user, goal=self.goal, title="Build API", scheduled_date=timezone.localdate())
        GoalService.recalculate_for_task(first)
        GoalService.recalculate_for_task(second)
        GoalService.recalculate_from_tasks(self.goal)
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.progress_percent, 0)
        second.status = Task.Status.COMPLETED
        second.save(update_fields=["status"])
        GoalService.recalculate_for_task(second)
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.progress_percent, 50)

    def test_milestone_dependency_cycle_is_rejected(self):
        first = GoalMilestone.objects.create(goal=self.goal, title="First", sequence=0)
        second = GoalMilestone.objects.create(goal=self.goal, title="Second", sequence=1)
        first.depends_on.add(second)
        serializer = GoalMilestoneSerializer(
            second,
            data={"depends_on": [first.id]},
            partial=True,
            context={"request": SimpleNamespace(user=self.user)},
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("depends_on", serializer.errors)

    def test_numeric_measurement_is_not_double_counted_with_task_progress(self):
        measured = Goal.objects.create(user=self.user, title="Read 10 books", initial_value=Decimal("0"), target_value=Decimal("10"), current_value=Decimal("5"), progress_percent=50, metadata={"progress_source": "measurement"})
        task = Task.objects.create(user=self.user, goal=measured, title="Read book six")
        task.status = Task.Status.COMPLETED
        task.save(update_fields=["status"])
        GoalService.recalculate_for_task(task)
        measured.refresh_from_db()
        self.assertEqual(measured.progress_percent, 50)
        self.assertEqual(measured.metadata.get("progress_source"), "measurement")

    def test_analytics_are_user_scoped(self):
        other = User.objects.create_user(email="another-owner@example.test", password="safe-test-password", name="Another Owner")
        Goal.objects.create(user=other, title="Private goal")
        result = GoalAnalyticsService.dashboard(self.user)
        self.assertEqual(result["total"], 1)

    def test_activity_is_recorded(self):
        GoalService.update_progress(self.goal, 20, self.user)
        self.assertTrue(GoalActivity.objects.filter(goal=self.goal, event_type="progress_updated").exists())

    def test_approved_plan_creates_milestones_and_tasks_once(self):
        proposal = GoalPlanProposal.objects.create(
            goal=self.goal, user=self.user, provider="test-provider",
            payload={"milestones": [{"title": "Foundation", "weight": 100, "tasks": [
                {"title": "Read Django docs", "priority": "medium", "estimated_minutes": 45}
            ]}]},
        )
        milestones = GoalService.approve_plan(proposal, self.user)
        self.assertEqual(len(milestones), 1)
        self.assertEqual(self.goal.tasks.count(), 1)
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, GoalPlanProposal.Status.APPROVED)
        with self.assertRaises(ValueError):
            GoalService.approve_plan(proposal, self.user)
        self.assertEqual(self.goal.tasks.count(), 1)

    def test_milestone_task_completion_updates_weighted_goal_progress(self):
        milestone = GoalMilestone.objects.create(goal=self.goal, title="Build API", sequence=0, weight=100)
        task = Task.objects.create(user=self.user, goal=self.goal, milestone=milestone, title="Implement endpoint")
        task.status = Task.Status.COMPLETED
        task.save(update_fields=["status"])
        GoalService.recalculate_for_task(task)
        milestone.refresh_from_db()
        self.goal.refresh_from_db()
        self.assertEqual(milestone.progress_percent, 100)
        self.assertEqual(self.goal.progress_percent, 100)

    @patch("ai.services.AIFallbackChainService.generate_completion")
    def test_goal_coach_uses_existing_fallback_service_and_returns_proposal(self, generate):
        generate.return_value = {
            "provider": "openai",
            "model": "test-model",
            "content": '{"summary":"A plan","success_criteria":["Ship API"],"milestones":[{"title":"Foundation","weight":100,"tasks":[]}]}',
        }
        payload, provider = GoalCoachService.propose_plan(self.goal, self.user)
        self.assertEqual(provider, "openai")
        self.assertEqual(payload["milestones"][0]["title"], "Foundation")
        generate.assert_called_once()

    @patch("ai.services.AIFallbackChainService.generate_completion")
    def test_goal_coach_answers_without_mutating_goal(self, generate):
        generate.return_value = {"provider": "openai", "model": "test-model", "content": "Focus on the overdue task."}
        answer = GoalCoachService.answer(self.goal, self.user, "What should I do next?")
        self.assertEqual(answer["content"], "Focus on the overdue task.")
        self.assertEqual(self.goal.activity.count(), 0)
        generate.assert_called_once()


class GoalAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="api-owner@example.test", password="safe-test-password", name="API Owner")
        self.other = User.objects.create_user(email="api-other@example.test", password="safe-test-password", name="API Other")
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.goal = Goal.objects.create(user=self.user, title="Owned goal")
        self.other_goal = Goal.objects.create(user=self.other, title="Private goal")

    def test_list_is_scoped_to_authenticated_user(self):
        response = self.client.get("/api/goals/")
        self.assertEqual(response.status_code, 200)
        payload = response.data.get("results", []) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["title"], "Owned goal")

    def test_other_users_goal_is_not_accessible(self):
        response = self.client.get(f"/api/goals/{self.other_goal.id}/")
        self.assertEqual(response.status_code, 404)

    def test_analytics_endpoint(self):
        response = self.client.get("/api/goals/analytics/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total"], 1)

    def test_invalid_progress_is_rejected(self):
        response = self.client.post(f"/api/goals/{self.goal.id}/progress/", {"progress_percent": 130}, format="json")
        self.assertEqual(response.status_code, 400)
