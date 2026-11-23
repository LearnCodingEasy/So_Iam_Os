from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from crm.models import Company, Contact

User = get_user_model()


class CrmApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="crm-api@example.com", password="pw-12345-test", name="Owner")
        self.other = User.objects.create_user(email="crm-api2@example.com", password="pw-12345-test", name="Other")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def _contact(self, **extra):
        payload = {"first_name": "Ada", "last_name": "Lovelace"}
        payload.update(extra)
        return self.client.post("/api/crm/contacts/", payload, format="json")

    def test_authentication_required(self):
        self.assertEqual(APIClient().get("/api/crm/contacts/").status_code, 401)

    def test_contact_crud_and_full_name(self):
        created = self._contact(email="ada@example.com").json()
        self.assertEqual(created["full_name"], "Ada Lovelace")
        patched = self.client.patch("/api/crm/contacts/%s/" % created["id"], {"job_title": "Engineer"}, format="json").json()
        self.assertEqual(patched["job_title"], "Engineer")
        self.assertEqual(self.client.delete("/api/crm/contacts/%s/" % created["id"]).status_code, 204)
        self.assertEqual(self.client.get("/api/crm/contacts/").json(), [])

    def test_validation(self):
        self.assertEqual(self._contact(first_name=" ").status_code, 400)
        self.assertEqual(self._contact(email="not-an-email").status_code, 400)

    def test_contacts_are_isolated_and_searchable(self):
        Contact.objects.create(user=self.other, first_name="Secret")
        self._contact()
        self._contact(first_name="Grace", last_name="Hopper")
        names = [c["first_name"] for c in self.client.get("/api/crm/contacts/").json()]
        self.assertEqual(sorted(names), ["Ada", "Grace"])
        found = self.client.get("/api/crm/contacts/?search=hopper").json()
        self.assertEqual([c["first_name"] for c in found], ["Grace"])

    def test_cannot_use_foreign_company(self):
        company = Company.objects.create(user=self.other, name="Theirs")
        self.assertEqual(self._contact(company=company.pk).status_code, 400)

    def test_interaction_for_foreign_contact_rejected(self):
        theirs = Contact.objects.create(user=self.other, first_name="X")
        response = self.client.post("/api/crm/interactions/", {"contact": theirs.pk, "subject": "Hi"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_follow_up_cannot_precede_interaction_and_listing(self):
        contact_id = self._contact().json()["id"]
        now = timezone.now()
        bad = self.client.post("/api/crm/interactions/", {
            "contact": contact_id, "subject": "Call", "occurred_at": now.isoformat(),
            "follow_up_at": (now - timedelta(days=1)).isoformat()}, format="json")
        self.assertEqual(bad.status_code, 400)
        good = self.client.post("/api/crm/interactions/", {
            "contact": contact_id, "subject": "Call", "interaction_type": "call",
            "follow_up_at": (now + timedelta(days=1)).isoformat()}, format="json")
        self.assertEqual(good.status_code, 201)
        rows = self.client.get("/api/crm/interactions/follow-ups/?days=3").json()
        self.assertEqual([r["subject"] for r in rows], ["Call"])
        self.assertEqual(self.client.get("/api/crm/interactions/follow-ups/?days=abc").status_code, 200)

    def test_relationship_pipeline_and_stage_stamp(self):
        contact_id = self._contact().json()["id"]
        rel = self.client.post("/api/crm/relationships/", {"contact": contact_id}, format="json").json()
        self.assertEqual(rel["stage"], "lead")
        duplicate = self.client.post("/api/crm/relationships/", {"contact": contact_id}, format="json")
        self.assertEqual(duplicate.status_code, 400)
        updated = self.client.patch("/api/crm/relationships/%s/" % rel["id"], {"stage": "customer"}, format="json").json()
        self.assertEqual(updated["stage"], "customer")
        self.assertNotEqual(updated["stage_changed_at"], rel["stage_changed_at"])
        self.assertEqual(self.client.get("/api/crm/relationships/pipeline/").json()["stages"]["customer"], 1)
        bad = self.client.patch("/api/crm/relationships/%s/" % rel["id"], {"health_score": 101}, format="json")
        self.assertEqual(bad.status_code, 400)
