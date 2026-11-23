from django.contrib.auth import get_user_model
from django.test import TestCase

from challenges.models import Challenge, ChallengeStep
from challenges.services import challenge_service

User = get_user_model()


class ChallengeServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="ch-svc@example.com", password="pw-12345-test", name="Owner")
        self.challenge = Challenge.objects.create(user=self.user, title="Build API")
        for i in range(4):
            ChallengeStep.objects.create(challenge=self.challenge, title="s%s" % i, order=i)

    def test_percent_for(self):
        self.assertEqual(challenge_service.percent_for(1, 4), 25)
        self.assertEqual(challenge_service.percent_for(1, 0), 0)

    def test_complete_step_advances_and_caps(self):
        for _ in range(6):
            row = challenge_service.complete_step(user=self.user, challenge=self.challenge)
        self.assertEqual((row.completed_steps, row.progress_percent), (4, 100))

    def test_set_progress_derives_percent_and_is_upsert(self):
        challenge_service.set_progress(user=self.user, challenge=self.challenge, completed_steps=2)
        row = challenge_service.set_progress(user=self.user, challenge=self.challenge, completed_steps=3)
        self.assertEqual(row.progress_percent, 75)
        self.assertEqual(self.challenge.progress_rows.count(), 1)

    def test_passing_attempt_completes_progress_failing_does_not(self):
        challenge_service.record_attempt(user=self.user, challenge=self.challenge, answer="x", score=40)
        self.assertEqual(self.challenge.progress_rows.count(), 0)
        challenge_service.record_attempt(user=self.user, challenge=self.challenge, answer="y", score=90)
        row = self.challenge.progress_rows.get()
        self.assertEqual((row.progress_percent, row.completed_steps), (100, 4))
