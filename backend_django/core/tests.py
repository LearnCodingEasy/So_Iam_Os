from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from goals.models import Goal
from tasks.models import Task

class DashboardTests(APITestCase):
    def test_dashboard_is_database_driven(self):
        User=get_user_model(); user=User.objects.create_user(email='dash@example.com',password='StrongPass123',name='Dashboard')
        Goal.objects.create(user=user,title='Ship OS')
        Task.objects.create(user=user,title='First task')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(user).access_token}')
        response=self.client.get('/api/core/dashboard/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['stats']['goals']['total'],1)
        self.assertEqual(response.data['stats']['tasks']['today'],1)
