from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from crm.models import Contact, CustomerRelationship, Interaction
from crm.services import crm_service

User = get_user_model()


class CrmServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="crm-svc@example.com", password="pw-12345-test", name="Owner")
        self.contact = Contact.objects.create(user=self.user, first_name="Ada")

    def test_pipeline_summary_counts_every_stage(self):
        CustomerRelationship.objects.create(user=self.user, contact=self.contact, stage="customer")
        second = Contact.objects.create(user=self.user, first_name="Bob")
        CustomerRelationship.objects.create(user=self.user, contact=second)
        summary = crm_service.pipeline_summary(self.user)
        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["stages"]["customer"], 1)
        self.assertEqual(summary["stages"]["lead"], 1)
        self.assertEqual(summary["stages"]["churned"], 0)

    def test_pipeline_is_per_user(self):
        other = User.objects.create_user(email="crm-svc2@example.com", password="pw-12345-test", name="Other")
        theirs = Contact.objects.create(user=other, first_name="X")
        CustomerRelationship.objects.create(user=other, contact=theirs)
        self.assertEqual(crm_service.pipeline_summary(self.user)["total"], 0)

    def test_due_follow_ups_window_and_order(self):
        now = timezone.now()
        Interaction.objects.create(user=self.user, contact=self.contact, subject="late", follow_up_at=now - timedelta(days=1))
        Interaction.objects.create(user=self.user, contact=self.contact, subject="soon", follow_up_at=now + timedelta(days=2))
        Interaction.objects.create(user=self.user, contact=self.contact, subject="far", follow_up_at=now + timedelta(days=30))
        Interaction.objects.create(user=self.user, contact=self.contact, subject="none")
        subjects = [i.subject for i in crm_service.due_follow_ups(self.user, 7)]
        self.assertEqual(subjects, ["late", "soon"])
