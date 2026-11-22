from django.test import TestCase
from rest_framework.test import APIClient

from users_accounts.models import User
from challenges.models import Challenge


class ChallengeOwnershipAPITests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@example.test", password="test-password", name="Owner"
        )
        self.other_user = User.objects.create_user(
            email="other@example.test", password="test-password", name="Other"
        )
        self.challenge = Challenge.objects.create(
            user=self.owner, title="Private challenge"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.other_user)

    def test_cannot_create_step_for_another_users_challenge(self):
        response = self.client.post(
            "/api/challenges/steps/",
            {"challenge": self.challenge.pk, "title": "Unauthorized step"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(self.challenge.steps.exists())

    def test_cannot_create_attempt_for_another_users_challenge(self):
        response = self.client.post(
            "/api/challenges/attempts/",
            {"challenge": self.challenge.pk, "answer": "Unauthorized answer"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(self.challenge.attempts.exists())

    def test_cannot_create_progress_for_another_users_challenge(self):
        response = self.client.post(
            "/api/challenges/progress/",
            {"challenge": self.challenge.pk, "progress_percent": 50},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(self.challenge.progress_rows.exists())
