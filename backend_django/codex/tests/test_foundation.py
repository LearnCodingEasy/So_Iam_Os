from django.test import TestCase
from codex.models import ProjectRegistry,Feature,APIEndpoint

class CodexFoundationModelTests(TestCase):
    def test_registry_constraints_and_api_frontend_place(self):
        p=ProjectRegistry.objects.create(key="test",name="Test")
        Feature.objects.create(project=p,key="app:test",name="Test")
        api=APIEndpoint.objects.create(project=p,method="GET",path="/api/test/",name="test")
        self.assertEqual(api.frontend_route,"/codex")
        self.assertEqual(api.frontend_section,"API Registry")
