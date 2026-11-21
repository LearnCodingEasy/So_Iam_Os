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


    def test_dashboard_cache_is_isolated_per_user(self):
        User = get_user_model()
        first = User.objects.create_user(
            email="first-dashboard@example.com",
            password="StrongPass123",
            name="First",
        )
        second = User.objects.create_user(
            email="second-dashboard@example.com",
            password="StrongPass123",
            name="Second",
        )
        Goal.objects.create(user=first, title="First user's goal")
        Goal.objects.create(user=second, title="Second user's goal")
        Goal.objects.create(user=second, title="Another goal")

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(first).access_token}"
        )
        first_response = self.client.get("/api/core/dashboard/")
        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(first_response.data["stats"]["goals"]["total"], 1)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(second).access_token}"
        )
        second_response = self.client.get("/api/core/dashboard/")
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(second_response.data["stats"]["goals"]["total"], 2)
