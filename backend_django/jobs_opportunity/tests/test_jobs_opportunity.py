from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.test import SimpleTestCase
from rest_framework_simplejwt.tokens import RefreshToken
from learning.models import Skill
from jobs_opportunity.feature_catalog import FEATURES
from jobs_opportunity.models import JobOpportunity, JobSkillRequirement, JobPreference


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


class XPathScraperExtractionTests(SimpleTestCase):
    """Regression tests for card-relative XPath extraction used by Wuzzuf."""

    def test_extracts_title_and_absolute_job_url_from_xpath_card(self):
        from jobs_opportunity.scraper import extract_jobs

        html = '''
        <html><body>
          <article class="job-card">
            <div><div><h2><a href="/jobs/123">Django Developer</a></h2></div></div>
          </article>
        </body></html>
        '''
        mapping = {
            "card": {"selector_type": "xpath", "selector": "//article[@class='job-card']"},
            "title": {"selector_type": "xpath", "selector": "./div/div[1]/h2/a"},
            "url": {"selector_type": "xpath", "selector": "./div/div[1]/h2/a", "attribute": "href"},
        }
        jobs = extract_jobs(html, mapping)
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["title"], "Django Developer")
        self.assertEqual(jobs[0]["url"], "/jobs/123")

    def test_xpath_text_extraction_handles_multiple_nested_text_nodes(self):
        from jobs_opportunity.scraper import extract_jobs

        html = '''<article class="job-card"><div><div><h2><a href="/jobs/456">Senior <span>Python</span> Engineer</a></h2></div></div></article>'''
        jobs = extract_jobs(html, {
            "card": {"selector_type": "xpath", "selector": "//article[@class='job-card']"},
            "title": {"selector_type": "xpath", "selector": "./div/div[1]/h2/a"},
        })
        self.assertEqual(jobs[0]["title"], "Senior Python Engineer")
