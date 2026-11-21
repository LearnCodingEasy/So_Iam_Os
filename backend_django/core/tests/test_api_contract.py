from django.test import SimpleTestCase
from django.urls import resolve


class ApiContractRoutingTests(SimpleTestCase):
    """Smoke-test the endpoint paths used by the Vue service contract."""

    def assert_route(self, path, expected_url_name=None):
        match = resolve(path)
        if expected_url_name:
            self.assertEqual(match.url_name, expected_url_name)
        self.assertIsNotNone(match.func)

    def test_learning_topic_actions(self):
        self.assert_route("/api/learning/topics/1/start/")
        self.assert_route("/api/learning/topics/1/complete/")
        self.assert_route("/api/learning/topics/1/skip/")
        self.assert_route("/api/learning/topics/1/generate-content/")

    def test_learning_path_actions(self):
        self.assert_route("/api/learning/paths/1/start/")
        self.assert_route("/api/learning/paths/1/complete/")
        self.assert_route("/api/learning/paths/1/pause/")
        self.assert_route("/api/learning/paths/1/reorder-topics/")

    def test_learning_session_finish(self):
        self.assert_route("/api/learning/sessions/1/finish/")

    def test_assessment_actions(self):
        self.assert_route("/api/learning/assessments/1/learner/")
        self.assert_route("/api/learning/assessments/1/start/")
        self.assert_route("/api/learning/assessments/1/submit/")

    def test_goal_and_task_actions(self):
        self.assert_route("/api/goals/1/complete/")
        self.assert_route("/api/goals/1/pause/")
        self.assert_route("/api/goals/1/resume/")
        self.assert_route("/api/goals/1/progress/")
        self.assert_route("/api/tasks/today/")
        self.assert_route("/api/tasks/1/complete/")
        self.assert_route("/api/tasks/1/postpone/")

    def test_knowledge_actions(self):
        self.assert_route("/api/knowledge/items/1/archive/")
        self.assert_route("/api/knowledge/items/1/restore/")
        self.assert_route("/api/knowledge/items/1/connect-topic/")
        self.assert_route("/api/knowledge/items/1/disconnect-topic/")
        self.assert_route("/api/knowledge/items/1/files/")
        self.assert_route("/api/knowledge/items/1/upload-file/")

    def test_notification_routes(self):
        self.assert_route("/api/notifications/")
        self.assert_route("/api/notifications/unread-count/")
        self.assert_route("/api/notifications/read-all/")
        self.assert_route("/api/notifications/1/read/")
        self.assert_route("/api/notifications/1/archive/")

    def test_social_routes(self):
        self.assert_route("/api/social/profile/")
        self.assert_route("/api/social/recommendations/")
        self.assert_route("/api/social/friends/00000000-0000-0000-0000-000000000001/request/")

    def test_jobs_routes(self):
        self.assert_route("/api/jobs/opportunities/1/readiness/")
        self.assert_route("/api/jobs/opportunities/1/apply/")
