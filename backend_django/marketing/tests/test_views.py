from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from crm.models import Contact
from marketing.models import Campaign, MarketingChannel

User = get_user_model()


class MarketingApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="mk-api@example.com", password="pw-12345-test", name="Owner")
        self.other = User.objects.create_user(email="mk-api2@example.com", password="pw-12345-test", name="Other")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def _campaign(self, **extra):
        payload = {"name": "Launch", "budget": "500.00"}
        payload.update(extra)
        return self.client.post("/api/marketing/campaigns/", payload, format="json")

    def test_authentication_required(self):
        self.assertEqual(APIClient().get("/api/marketing/campaigns/").status_code, 401)

    def test_campaigns_isolated(self):
        theirs = Campaign.objects.create(user=self.other, name="Theirs")
        self._campaign()
        self.assertEqual([c["name"] for c in self.client.get("/api/marketing/campaigns/").json()], ["Launch"])
        self.assertEqual(self.client.get("/api/marketing/campaigns/%s/performance/" % theirs.pk).status_code, 404)

    def test_campaign_validation(self):
        self.assertEqual(self._campaign(budget="-1").status_code, 400)
        self.assertEqual(self._campaign(start_date="2026-05-01", end_date="2026-04-01").status_code, 400)
        self.assertEqual(self._campaign(name=" ").status_code, 400)

    def test_foreign_channel_rejected(self):
        theirs = MarketingChannel.objects.create(user=self.other, name="X")
        self.assertEqual(self._campaign(channel=theirs.pk).status_code, 400)

    def test_content_schedule_and_publish(self):
        campaign_id = self._campaign().json()["id"]
        bad = self.client.post("/api/marketing/content/", {"title": "T", "status": "scheduled"}, format="json")
        self.assertEqual(bad.status_code, 400)
        created = self.client.post("/api/marketing/content/", {"title": "T", "campaign": campaign_id, "published_at": "2020-01-01T00:00:00Z"}, format="json").json()
        self.assertIsNone(created["published_at"])
        published = self.client.post("/api/marketing/content/%s/publish/" % created["id"]).json()
        self.assertEqual(published["status"], "published")
        self.assertIsNotNone(published["published_at"])

    def test_lead_source_links_only_own_contacts(self):
        mine = Contact.objects.create(user=self.user, first_name="Ada")
        theirs = Contact.objects.create(user=self.other, first_name="X")
        bad = self.client.post("/api/marketing/lead-sources/", {"name": "Webinar", "contacts": [mine.pk, theirs.pk]}, format="json")
        self.assertEqual(bad.status_code, 400)
        ok = self.client.post("/api/marketing/lead-sources/", {"name": "Webinar", "contacts": [mine.pk]}, format="json")
        self.assertEqual(ok.status_code, 201)
        self.assertEqual(ok.json()["leads_count"], 1)

    def test_performance_and_overview_endpoints(self):
        campaign_id = self._campaign(spent="100.00").json()["id"]
        contact = Contact.objects.create(user=self.user, first_name="Ada")
        self.client.post("/api/marketing/lead-sources/", {"name": "W", "campaign": campaign_id, "contacts": [contact.pk]}, format="json")
        performance = self.client.get("/api/marketing/campaigns/%s/performance/" % campaign_id).json()
        self.assertEqual((performance["leads"], performance["cost_per_lead"]), (1, "100.00"))
        overview = self.client.get("/api/marketing/campaigns/overview/").json()
        self.assertEqual((overview["campaigns"], overview["leads"]), (1, 1))
