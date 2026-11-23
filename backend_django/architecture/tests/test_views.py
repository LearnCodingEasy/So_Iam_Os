from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from architecture.models import Architecture, Component

User = get_user_model()


class ArchitectureApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="arch-api@example.com", password="pw-12345-test", name="Owner")
        self.other = User.objects.create_user(email="arch-api2@example.com", password="pw-12345-test", name="Other")
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.arch = Architecture.objects.create(user=self.user, name="Mine")

    def _component(self, name, arch=None):
        return self.client.post("/api/architecture/components/", {"architecture": (arch or self.arch).pk, "name": name}, format="json")

    def test_authentication_required(self):
        self.assertEqual(APIClient().get("/api/architecture/architectures/").status_code, 401)

    def test_architectures_isolated(self):
        theirs = Architecture.objects.create(user=self.other, name="Theirs")
        self.assertEqual([a["name"] for a in self.client.get("/api/architecture/architectures/").json()], ["Mine"])
        self.assertEqual(self.client.get("/api/architecture/architectures/%s/" % theirs.pk).status_code, 404)
        self.assertEqual(self.client.get("/api/architecture/architectures/%s/graph/" % theirs.pk).status_code, 404)

    def test_cannot_add_component_to_foreign_architecture(self):
        theirs = Architecture.objects.create(user=self.other, name="Theirs")
        self.assertEqual(self._component("x", theirs).status_code, 400)
        self.assertEqual(Component.objects.filter(architecture=theirs).count(), 0)

    def test_duplicate_component_name_is_400(self):
        self.assertEqual(self._component("api").status_code, 201)
        self.assertEqual(self._component("api").status_code, 400)

    def test_dependency_rules(self):
        a = self._component("a").json()["id"]
        b = self._component("b").json()["id"]
        ok = self.client.post("/api/architecture/dependencies/", {"source": a, "target": b}, format="json")
        self.assertEqual(ok.status_code, 201)
        self_loop = self.client.post("/api/architecture/dependencies/", {"source": a, "target": a}, format="json")
        self.assertEqual(self_loop.status_code, 400)
        cycle = self.client.post("/api/architecture/dependencies/", {"source": b, "target": a, "dependency_type": "calls"}, format="json")
        self.assertEqual(cycle.status_code, 400)
        self.assertIn("circular", str(cycle.json()))
        other_arch = Architecture.objects.create(user=self.user, name="Second")
        c = self._component("c", other_arch).json()["id"]
        cross = self.client.post("/api/architecture/dependencies/", {"source": a, "target": c}, format="json")
        self.assertEqual(cross.status_code, 400)

    def test_dependency_to_foreign_component_rejected(self):
        theirs = Architecture.objects.create(user=self.other, name="Theirs")
        foreign = Component.objects.create(architecture=theirs, name="f")
        a = self._component("a").json()["id"]
        response = self.client.post("/api/architecture/dependencies/", {"source": a, "target": foreign.pk}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_graph_endpoint(self):
        a = self._component("a").json()["id"]
        b = self._component("b").json()["id"]
        self.client.post("/api/architecture/dependencies/", {"source": a, "target": b}, format="json")
        graph = self.client.get("/api/architecture/architectures/%s/graph/" % self.arch.pk).json()
        self.assertEqual(len(graph["nodes"]), 2)
        self.assertEqual(graph["edges"][0]["target"], b)

    def test_decision_supersede_rules(self):
        d1 = self.client.post("/api/architecture/decisions/", {"architecture": self.arch.pk, "title": "Old"}, format="json").json()
        bad = self.client.post("/api/architecture/decisions/", {"architecture": self.arch.pk, "title": "X", "status": "superseded"}, format="json")
        self.assertEqual(bad.status_code, 400)
        d2 = self.client.post("/api/architecture/decisions/", {"architecture": self.arch.pk, "title": "New", "status": "accepted"}, format="json").json()
        done = self.client.patch("/api/architecture/decisions/%s/" % d1["id"], {"status": "superseded", "superseded_by": d2["id"]}, format="json")
        self.assertEqual(done.status_code, 200)
        selfref = self.client.patch("/api/architecture/decisions/%s/" % d2["id"], {"superseded_by": d2["id"]}, format="json")
        self.assertEqual(selfref.status_code, 400)
