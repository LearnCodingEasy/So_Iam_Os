from types import SimpleNamespace

from django.test import TestCase

from goals.models import Goal
from goals.services import GoalService
from learning.models import LearningGoal, LearningPath, LearningTopic, Skill
from tasks.models import Task
from tasks.serializers import TaskSerializer
from tasks.services import TaskService
from users_accounts.models import User


class TaskIntegrationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="task-owner@example.test", password="not-a-real-secret", name="Owner")
        self.other = User.objects.create_user(email="task-other@example.test", password="not-a-real-secret", name="Other")

    def test_completing_tasks_recalculates_goal_progress_from_real_tasks(self):
        goal = Goal.objects.create(user=self.user, title="Ship feature")
        first = Task.objects.create(user=self.user, goal=goal, title="Implement")
        Task.objects.create(user=self.user, goal=goal, title="Test")

        TaskService.complete(first)
        goal.refresh_from_db()
        self.assertEqual(goal.progress_percent, 50)
        self.assertEqual(goal.status, Goal.Status.ACTIVE)

        second = goal.tasks.get(title="Test")
        TaskService.complete(second)
        goal.refresh_from_db()
        self.assertEqual(goal.progress_percent, 100)
        self.assertEqual(goal.status, Goal.Status.COMPLETED)
        self.assertIsNotNone(goal.completed_at)

    def test_task_serializer_rejects_learning_topic_owned_by_another_user(self):
        skill = Skill.objects.create(name="Python", slug="python-test-owner-scope")
        learning_goal = LearningGoal.objects.create(user=self.other, title="Other learning", skill=skill)
        path = LearningPath.objects.create(user=self.other, goal=learning_goal, title="Other path")
        topic = LearningTopic.objects.create(path=path, title="Other topic")
        request = SimpleNamespace(user=self.user)

        serializer = TaskSerializer(
            data={"title": "Do not link", "learning_topic": topic.pk},
            context={"request": request},
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("learning_topic", serializer.errors)
