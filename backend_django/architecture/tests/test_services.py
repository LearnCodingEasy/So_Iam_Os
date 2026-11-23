from django.contrib.auth import get_user_model
from django.test import TestCase

from architecture.models import Architecture, Component, Dependency
from architecture.services import architecture_service

User = get_user_model()


class ArchitectureServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="arch-svc@example.com", password="pw-12345-test", name="Owner")
        self.arch = Architecture.objects.create(user=self.user, name="Sys")
        self.a, self.b, self.c, self.lone = (
            Component.objects.create(architecture=self.arch, name=n) for n in ("a", "b", "c", "lone")
        )
        Dependency.objects.create(source=self.a, target=self.b)
        Dependency.objects.create(source=self.b, target=self.c)

    def test_cycle_detection(self):
        self.assertTrue(architecture_service.would_create_cycle(self.c, self.a))
        self.assertTrue(architecture_service.would_create_cycle(self.b, self.a))
        self.assertTrue(architecture_service.would_create_cycle(self.a, self.a))
        self.assertFalse(architecture_service.would_create_cycle(self.a, self.c))
        self.assertFalse(architecture_service.would_create_cycle(self.lone, self.a))

    def test_graph_metrics(self):
        graph = architecture_service.build_graph(self.arch)
        self.assertEqual(graph["metrics"]["components"], 4)
        self.assertEqual(graph["metrics"]["dependencies"], 2)
        self.assertEqual(graph["metrics"]["isolated"], [self.lone.pk])
        self.assertIn(graph["metrics"]["most_depended_on"], (self.b.pk, self.c.pk))
        self.assertEqual({(e["source"], e["target"]) for e in graph["edges"]}, {(self.a.pk, self.b.pk), (self.b.pk, self.c.pk)})

    def test_empty_graph(self):
        empty = Architecture.objects.create(user=self.user, name="Empty")
        graph = architecture_service.build_graph(empty)
        self.assertEqual(graph["nodes"], [])
        self.assertIsNone(graph["metrics"]["most_depended_on"])
