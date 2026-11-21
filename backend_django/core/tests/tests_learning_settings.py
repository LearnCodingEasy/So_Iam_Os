from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from learning.models import LearningGoal, LearningPath, LearningTopic, Skill
from core.models import UserLearningSettings

class LearningSettingsAPITests(APITestCase):
    def setUp(self):
        User=get_user_model()
        self.user=User.objects.create_user(email="settings@example.com", password="StrongPass123", name="Settings")
        self.client.force_authenticate(self.user)
        self.skill=Skill.objects.create(name="Django", slug="django")
        self.goal=LearningGoal.objects.create(user=self.user, skill=self.skill, title="Advanced Django")
    def test_learning_settings_persist(self):
        response=self.client.patch("/api/core/learning-settings/", {"daily_learning_tasks":7,"current_learning_goal":self.goal.id,"task_generation_enabled":True}, format="json")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data["daily_learning_tasks"],7)
        self.assertEqual(UserLearningSettings.objects.get(user=self.user).current_learning_goal_id,self.goal.id)
