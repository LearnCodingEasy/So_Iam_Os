from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from challenges.models import Challenge, ChallengeStep
from goals.models import Goal

User = get_user_model()
BASE = "/api/challenges/"


class ChallengeApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="ch-api@example.com", password="pw-12345-test", name="Owner")
        self.other = User.objects.create_user(email="ch-api2@example.com", password="pw-12345-test", name="Other")
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.foreign = Challenge.objects.create(user=self.other, title="Not mine")
        self.mine = Challenge.objects.create(user=self.user, title="Mine")

    def test_authentication_required(self):
        self.assertEqual(APIClient().get(BASE + "challenges/").status_code, 401)

    def test_list_is_isolated_per_user(self):
        titles = [r["title"] for r in self.client.get(BASE + "challenges/").json()]
        self.assertEqual(titles, ["Mine"])
        self.assertEqual(self.client.get("%schallenges/%s/" % (BASE, self.foreign.pk)).status_code, 404)

    def test_create_ignores_forged_user_and_rejects_blank_title(self):
        ok = self.client.post(BASE + "challenges/", {"title": "New", "user": self.other.pk}, format="json")
        self.assertEqual(ok.status_code, 201)
        self.assertEqual(Challenge.objects.get(pk=ok.json()["id"]).user, self.user)
        self.assertEqual(self.client.post(BASE + "challenges/", {"title": " "}, format="json").status_code, 400)

    def test_foreign_goal_link_rejected(self):
        goal = Goal.objects.create(user=self.other, title="Foreign goal")
        response = self.client.post(BASE + "challenges/", {"title": "x", "goal": goal.pk}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_add_step_to_foreign_challenge(self):
        response = self.client.post(BASE + "steps/", {"challenge": self.foreign.pk, "title": "s"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(ChallengeStep.objects.filter(challenge=self.foreign).count(), 0)
        ok = self.client.post(BASE + "steps/", {"challenge": self.mine.pk, "title": "s"}, format="json")
        self.assertEqual(ok.status_code, 201)

    def test_cannot_attempt_or_track_foreign_challenge(self):
        a = self.client.post(BASE + "attempts/", {"challenge": self.foreign.pk, "answer": "x"}, format="json")
        p = self.client.post(BASE + "progress/", {"challenge": self.foreign.pk}, format="json")
        self.assertEqual((a.status_code, p.status_code), (400, 400))

    def test_attempt_score_validation_and_passing_completes_progress(self):
        bad = self.client.post(BASE + "attempts/", {"challenge": self.mine.pk, "score": 101}, format="json")
        self.assertEqual(bad.status_code, 400)
        ok = self.client.post(BASE + "attempts/", {"challenge": self.mine.pk, "answer": "a", "score": 80}, format="json")
        self.assertEqual(ok.status_code, 201)
        rows = self.client.get(BASE + "progress/?challenge=%s" % self.mine.pk).json()
        self.assertEqual(rows[0]["progress_percent"], 100)

    def test_progress_post_is_upsert_not_server_error(self):
        for _ in range(2):
            r = self.client.post(BASE + "progress/", {"challenge": self.mine.pk, "progress_percent": 30}, format="json")
            self.assertEqual(r.status_code, 201)
        self.assertEqual(self.mine.progress_rows.count(), 1)

    def test_complete_step_action(self):
        for i in range(2):
            ChallengeStep.objects.create(challenge=self.mine, title="s%s" % i, order=i)
        r = self.client.post("%schallenges/%s/complete-step/" % (BASE, self.mine.pk)).json()
        self.assertEqual((r["completed_steps"], r["progress_percent"]), (1, 50))
        self.assertEqual(self.client.post("%schallenges/%s/complete-step/" % (BASE, self.foreign.pk)).status_code, 404)

    def test_progress_cannot_exceed_steps(self):
        r = self.client.post(BASE + "progress/", {"challenge": self.mine.pk, "completed_steps": 5}, format="json")
        self.assertEqual(r.status_code, 400)
