from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from learning.models import Skill
from .feature_catalog import FEATURES
from .models import JobOpportunity, JobSkillRequirement, JobPreference


class JobsAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='jobs@example.com', password='StrongPass123', name='Jobs')
        self.other = User.objects.create_user(email='other@example.com', password='StrongPass123', name='Other')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.user).access_token}')
        self.skill = Skill.objects.create(name='Django', slug='django')
        self.job = JobOpportunity.objects.create(user=self.other, title='Private', company='Other')
        self.own = JobOpportunity.objects.create(user=self.user, title='Backend Engineer', company='Acme', is_remote=True, description='Django backend engineer')
        JobSkillRequirement.objects.create(job=self.own, skill=self.skill)

    def test_user_isolation(self):
        response = self.client.get('/api/jobs/opportunities/')
        self.assertEqual(response.status_code, 200)
        rows = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        ids = {row['id'] for row in rows}
        self.assertIn(self.own.id, ids)
        self.assertNotIn(self.job.id, ids)

    def test_match_endpoint(self):
        response = self.client.post(f'/api/jobs/opportunities/{self.own.id}/refresh_match/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('score', response.data)
        self.assertIn('breakdown', response.data)

    def test_workspace_has_150_features(self):
        self.assertEqual(len(FEATURES), 150)
        response = self.client.get('/api/jobs/workspace/features/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 150)

    def test_preferences_and_readiness(self):
        response = self.client.get('/api/jobs/preferences/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user'], str(self.user.id))
        response = self.client.get('/api/jobs/readiness/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard(self):
        response = self.client.get('/api/jobs/workspace/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('jobs', response.data)
        self.assertIn('application_conversion_rate', response.data)
