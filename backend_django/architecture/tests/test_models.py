from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from architecture.models import Architecture, ArchitectureDecision, Component, Dependency

User = get_user_model()


class ArchitectureModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="arch-models@example.com", password="pw-12345-test", name="Owner")
        self.arch = Architecture.objects.create(user=self.user, name="So_Iam_Os")

    def test_defaults(self):
        self.assertEqual((self.arch.status, self.arch.version), ("draft", "1.0"))
        decision = ArchitectureDecision.objects.create(architecture=self.arch, title="Use Django")
        self.assertEqual(decision.status, "proposed")

    def test_component_name_unique_per_architecture(self):
        Component.objects.create(architecture=self.arch, name="api")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Component.objects.create(architecture=self.arch, name="api")

    def test_dependency_unique_per_type(self):
        a = Component.objects.create(architecture=self.arch, name="a")
        b = Component.objects.create(architecture=self.arch, name="b")
        Dependency.objects.create(source=a, target=b)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Dependency.objects.create(source=a, target=b)
