
from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import (
    Skill,
    LearningGoal,
    LearningPath,
    LearningTopic,
    Assessment,
)

from .services import (
    ProgressService,
    AssessmentService,
)


User = get_user_model()


class LearningModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="learning_test_user@example.com",
            password="test-password-123",
        )

        self.skill = Skill.objects.create(
            name="Django",
            slug="django",
            category="Backend",
        )

        self.goal = LearningGoal.objects.create(
            user=self.user,
            title="Master Django",
            skill=self.skill,
            target_level=Skill.LEVEL_ADVANCED,
        )

        self.path = LearningPath.objects.create(
            user=self.user,
            goal=self.goal,
            title="Django Advanced Path",
        )

        self.topic = LearningTopic.objects.create(
            path=self.path,
            skill=self.skill,
            title="Django ORM",
            order=1,
        )

    def test_learning_goal_belongs_to_user(self):
        self.assertEqual(
            self.goal.user,
            self.user,
        )

    def test_learning_path_belongs_to_goal(self):
        self.assertEqual(
            self.path.goal,
            self.goal,
        )

    def test_topic_belongs_to_path(self):
        self.assertEqual(
            self.topic.path,
            self.path,
        )


class ProgressServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="progress_user@example.com",
            password="test-password-123",
        )

        skill = Skill.objects.create(
            name="Vue.js",
            slug="vue-js",
        )

        goal = LearningGoal.objects.create(
            user=self.user,
            title="Learn Vue",
            skill=skill,
        )

        path = LearningPath.objects.create(
            user=self.user,
            goal=goal,
            title="Vue Path",
        )

        self.topic = LearningTopic.objects.create(
            path=path,
            title="Vue Composition API",
        )

    def test_update_progress(self):
        progress = ProgressService.update_progress(
            user=self.user,
            topic=self.topic,
            progress_percent=50,
            practice_completed=True,
        )

        self.assertEqual(
            progress.progress_percent,
            50,
        )

        self.assertTrue(
            progress.practice_completed
        )

        self.topic.refresh_from_db()

        self.assertEqual(
            self.topic.status,
            LearningTopic.STATUS_IN_PROGRESS,
        )

    def test_complete_topic(self):
        ProgressService.update_progress(
            user=self.user,
            topic=self.topic,
            progress_percent=100,
        )

        self.topic.refresh_from_db()

        self.assertEqual(
            self.topic.status,
            LearningTopic.STATUS_COMPLETED,
        )


class AssessmentServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="assessment_user@example.com",
            password="test-password-123",
        )

        skill = Skill.objects.create(
            name="Python",
            slug="python",
        )

        goal = LearningGoal.objects.create(
            user=self.user,
            title="Learn Python",
            skill=skill,
        )

        path = LearningPath.objects.create(
            user=self.user,
            goal=goal,
            title="Python Path",
        )

        topic = LearningTopic.objects.create(
            path=path,
            title="Python Basics",
        )

        self.assessment = Assessment.objects.create(
            topic=topic,
            title="Python Test",
            passing_score=70,
        )

    def test_passing_assessment(self):
        attempt = AssessmentService.submit_attempt(
            user=self.user,
            assessment=self.assessment,
            score=85,
        )

        self.assertTrue(
            attempt.passed
        )

    def test_failed_assessment(self):
        attempt = AssessmentService.submit_attempt(
            user=self.user,
            assessment=self.assessment,
            score=50,
        )

        self.assertFalse(
            attempt.passed
        )
