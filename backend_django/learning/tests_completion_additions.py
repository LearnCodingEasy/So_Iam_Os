from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from .models import LearningGoal, LearningPath, LearningTopic, Skill

class TopicCompletionIntegrationTests(APITestCase):
    def setUp(self):
        User=get_user_model(); self.user=User.objects.create_user(email="learning@example.com",password="StrongPass123",name="Learning")
        self.client.force_authenticate(self.user); skill=Skill.objects.create(name="Django",slug="django")
        goal=LearningGoal.objects.create(user=self.user,skill=skill,title="Learn Django")
        path=LearningPath.objects.create(user=self.user,goal=goal,title="Django Path")
        self.topic1=LearningTopic.objects.create(path=path,skill=skill,title="ORM",order=1)
        self.topic2=LearningTopic.objects.create(path=path,skill=skill,title="Optimization",order=2)
    def test_completion_returns_next_topic_and_persists(self):
        response=self.client.post(f"/api/learning/topics/{self.topic1.id}/complete/")
        self.assertEqual(response.status_code,200)
        self.topic1.refresh_from_db(); self.assertEqual(self.topic1.status,"completed")
        self.assertEqual(response.data["next_topic"]["id"],self.topic2.id)
