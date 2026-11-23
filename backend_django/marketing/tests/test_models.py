from django.contrib.auth import get_user_model
from django.test import TestCase

from crm.models import Contact
from marketing.models import Campaign, LeadSource, MarketingChannel, MarketingContent

User = get_user_model()


class MarketingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="mk-models@example.com", password="pw-12345-test", name="Owner")

    def test_defaults(self):
        campaign = Campaign.objects.create(user=self.user, name="Launch")
        self.assertEqual((campaign.status, str(campaign.budget), str(campaign.spent)), ("draft", "0", "0"))
        self.assertEqual(MarketingChannel.objects.create(user=self.user, name="X").channel_type, "social")
        content = MarketingContent.objects.create(user=self.user, title="Post")
        self.assertEqual((content.status, content.content_type, content.published_at), ("draft", "post", None))

    def test_deleting_campaign_keeps_content_and_lead_source(self):
        campaign = Campaign.objects.create(user=self.user, name="Launch")
        content = MarketingContent.objects.create(user=self.user, title="Post", campaign=campaign)
        source = LeadSource.objects.create(user=self.user, name="Webinar", campaign=campaign)
        campaign.delete()
        content.refresh_from_db()
        source.refresh_from_db()
        self.assertIsNone(content.campaign)
        self.assertIsNone(source.campaign)

    def test_lead_source_contacts(self):
        contact = Contact.objects.create(user=self.user, first_name="Ada")
        source = LeadSource.objects.create(user=self.user, name="Webinar")
        source.contacts.add(contact)
        self.assertEqual(list(contact.lead_sources.all()), [source])
