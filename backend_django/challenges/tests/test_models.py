from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from challenges.models import Challenge, ChallengeProgress, ChallengeStep

User = get_user_model()


class ChallengeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="ch-models@example.com", password="pw-12345-test", name="Owner")

    def test_defaults(self):
        challenge = Challenge.objects.create(user=self.user, title="FizzBuzz")
        self.assertEqual(challenge.status, Challenge.Status.ACTIVE)
        self.assertEqual(challenge.type, Challenge.Type.LEARNING)
        self.assertEqual(challenge.difficulty, "intermediate")

    def test_steps_are_ordered(self):
        challenge = Challenge.objects.create(user=self.user, title="Ordered")
        ChallengeStep.objects.create(challenge=challenge, title="second", order=2)
        ChallengeStep.objects.create(challenge=challenge, title="first", order=1)
        self.assertEqual([s.title for s in challenge.steps.all()], ["first", "second"])

    def test_one_progress_row_per_user_and_challenge(self):
        challenge = Challenge.objects.create(user=self.user, title="Unique")
        ChallengeProgress.objects.create(challenge=challenge, user=self.user)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ChallengeProgress.objects.create(challenge=challenge, user=self.user)
