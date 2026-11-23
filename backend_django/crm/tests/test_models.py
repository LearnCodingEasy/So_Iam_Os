from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from crm.models import Company, Contact, CustomerRelationship, Interaction

User = get_user_model()


class CrmModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="crm-models@example.com", password="pw-12345-test", name="Owner")

    def test_contact_full_name_and_defaults(self):
        contact = Contact.objects.create(user=self.user, first_name="Ada", last_name="Lovelace")
        self.assertEqual(contact.full_name, "Ada Lovelace")
        self.assertEqual(str(contact), "Ada Lovelace")
        self.assertEqual(contact.status, "active")
        self.assertEqual(Contact.objects.create(user=self.user, first_name="Solo").full_name, "Solo")

    def test_relationship_is_one_per_contact(self):
        contact = Contact.objects.create(user=self.user, first_name="Ada")
        CustomerRelationship.objects.create(user=self.user, contact=contact)
        with self.assertRaises(IntegrityError), transaction.atomic():
            CustomerRelationship.objects.create(user=self.user, contact=contact)

    def test_company_deletion_keeps_contacts(self):
        company = Company.objects.create(user=self.user, name="Acme")
        contact = Contact.objects.create(user=self.user, first_name="Ada", company=company)
        company.delete()
        contact.refresh_from_db()
        self.assertIsNone(contact.company)

    def test_interaction_defaults(self):
        contact = Contact.objects.create(user=self.user, first_name="Ada")
        self.assertEqual(Interaction.objects.create(user=self.user, contact=contact, subject="Hi").interaction_type, "note")
