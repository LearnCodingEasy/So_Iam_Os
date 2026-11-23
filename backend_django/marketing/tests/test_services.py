from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from crm.models import Contact
from marketing.models import Campaign, LeadSource, MarketingContent
from marketing.services import marketing_service

User = get_user_model()


class MarketingServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="mk-svc@example.com", password="pw-12345-test", name="Owner")
        self.campaign = Campaign.objects.create(user=self.user, name="Launch", budget=Decimal("500"), spent=Decimal("200"))

    def _lead(self, name, *sources):
        contact = Contact.objects.create(user=self.user, first_name=name)
        for source in sources:
            source.contacts.add(contact)
        return contact

    def test_performance_counts_distinct_leads(self):
        a = LeadSource.objects.create(user=self.user, name="A", campaign=self.campaign)
        b = LeadSource.objects.create(user=self.user, name="B", campaign=self.campaign)
        self._lead("shared", a, b)
        self._lead("only-a", a)
        result = marketing_service.campaign_performance(self.campaign)
        self.assertEqual(result["leads"], 2)
        self.assertEqual(result["cost_per_lead"], "100.00")
        self.assertEqual((result["budget"], result["spent"], result["remaining"]), ("500.00", "200.00", "300.00"))
        self.assertFalse(result["over_budget"])

    def test_no_leads_means_no_cost_per_lead(self):
        result = marketing_service.campaign_performance(self.campaign)
        self.assertEqual(result["leads"], 0)
        self.assertIsNone(result["cost_per_lead"])

    def test_over_budget_flag_and_content_counts(self):
        self.campaign.spent = Decimal("600")
        self.campaign.save()
        MarketingContent.objects.create(user=self.user, title="a", campaign=self.campaign)
        MarketingContent.objects.create(user=self.user, title="b", campaign=self.campaign, status="published")
        result = marketing_service.campaign_performance(self.campaign)
        self.assertTrue(result["over_budget"])
        self.assertEqual(result["content"], {"total": 2, "by_status": {"draft": 1, "published": 1}})

    def test_mark_published_sets_time_once(self):
        content = MarketingContent.objects.create(user=self.user, title="a")
        first = marketing_service.mark_published(content).published_at
        self.assertIsNotNone(first)
        self.assertEqual(marketing_service.mark_published(content).published_at, first)

    def test_overview_is_scoped_to_user(self):
        other = User.objects.create_user(email="mk-svc2@example.com", password="pw-12345-test", name="Other")
        Campaign.objects.create(user=other, name="Theirs", budget=999)
        result = marketing_service.overview(self.user)
        self.assertEqual((result["campaigns"], result["budget"], result["leads"]), (1, "500.00", 0))
