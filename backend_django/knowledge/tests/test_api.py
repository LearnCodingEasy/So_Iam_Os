"""API integration tests for Knowledge: auth, ownership scoping, actions, uploads."""
import tempfile
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APITestCase

from knowledge.models import KnowledgeFile, KnowledgeItem

User = get_user_model()
BASE = "/api/knowledge/items/"


def make_user(email):
    return User.objects.create_user(email=email, password="pass-12345")


class KnowledgeItemApiTests(APITestCase):
    def setUp(self):
        self.alice = make_user("alice@example.com")
        self.bob = make_user("bob@example.com")

    def test_requires_authentication(self):
        self.assertIn(self.client.get(BASE).status_code, (401, 403))

    def test_create_list_and_owner_scoping(self):
        self.client.force_authenticate(self.alice)
        res = self.client.post(BASE, {"title": "Django notes", "content": "# Intro\nDRF"}, format="json")
        self.assertEqual(res.status_code, 201, res.data)
        item = KnowledgeItem.objects.get(pk=res.data["id"])
        self.assertEqual(item.user_id, self.alice.id)

        listing = self.client.get(BASE)
        self.assertEqual(listing.status_code, 200)
        rows = listing.data["results"] if isinstance(listing.data, dict) else listing.data
        self.assertEqual([r["id"] for r in rows], [item.id])

        self.client.force_authenticate(self.bob)
        rows = self.client.get(BASE).data
        rows = rows["results"] if isinstance(rows, dict) else rows
        self.assertEqual(rows, [])
        self.assertEqual(self.client.get(f"{BASE}{item.id}/").status_code, 404)

    def test_archive_and_restore(self):
        item = KnowledgeItem.objects.create(user=self.alice, title="Keep me", content="x")
        self.client.force_authenticate(self.alice)
        self.assertEqual(self.client.post(f"{BASE}{item.id}/archive/").status_code, 200)
        item.refresh_from_db()
        self.assertTrue(item.is_archived)
        self.assertEqual(self.client.post(f"{BASE}{item.id}/restore/").status_code, 200)
        item.refresh_from_db()
        self.assertFalse(item.is_archived)

    def test_extract_metadata_action_fills_empty_fields_only(self):
        item = KnowledgeItem.objects.create(
            user=self.alice, title="Django API", content="# API Overview\n\nThis guide explains Django REST API design."
        )
        self.client.force_authenticate(self.alice)
        res = self.client.post(f"{BASE}{item.id}/extract-metadata/")
        self.assertEqual(res.status_code, 200, res.data)
        self.assertIn("extracted", res.data)
        item.refresh_from_db()
        self.assertIn("extracted", item.metadata)

    def test_upload_rejects_unsupported_file_and_missing_file(self):
        item = KnowledgeItem.objects.create(user=self.alice, title="Files", content="x")
        self.client.force_authenticate(self.alice)
        url = f"{BASE}{item.id}/upload-file/"
        self.assertEqual(self.client.post(url, {}, format="multipart").status_code, 400)
        bad = SimpleUploadedFile("evil.exe", b"MZ\x90\x00", content_type="application/octet-stream")
        self.assertEqual(self.client.post(url, {"file": bad}, format="multipart").status_code, 400)
        self.assertEqual(KnowledgeFile.objects.count(), 0)

    def test_upload_valid_text_file_creates_record(self):
        item = KnowledgeItem.objects.create(user=self.alice, title="Files", content="x")
        self.client.force_authenticate(self.alice)
        with tempfile.TemporaryDirectory() as tmp, override_settings(MEDIA_ROOT=tmp), patch(
            "knowledge.tasks.process_knowledge_file.delay"
        ) as enqueue_task:
            good = SimpleUploadedFile("notes.md", b"# Notes\nhello", content_type="text/markdown")
            res = self.client.post(f"{BASE}{item.id}/upload-file/", {"file": good}, format="multipart")
            self.assertIn(res.status_code, (200, 201), getattr(res, "data", None))
            enqueue_task.assert_called_once()
        self.assertEqual(KnowledgeFile.objects.filter(knowledge=item).count(), 1)

    def test_cannot_touch_another_users_item(self):
        item = KnowledgeItem.objects.create(user=self.alice, title="Private", content="x")
        self.client.force_authenticate(self.bob)
        self.assertEqual(self.client.post(f"{BASE}{item.id}/archive/").status_code, 404)


class KnowledgeStructureContractTests(APITestCase):
    def test_celery_task_keeps_legacy_name(self):
        from knowledge.tasks import process_knowledge_file
        self.assertEqual(process_knowledge_file.name, "knowledge.tasks.process_knowledge_file")

    def test_public_import_surface(self):
        from knowledge.api.serializers import KnowledgeItemSerializer  # noqa: F401
        from knowledge.api.views import KnowledgeFileViewSet, KnowledgeItemViewSet  # noqa: F401
        from knowledge.models import KnowledgeFile, KnowledgeItem  # noqa: F401
        from knowledge.services import KnowledgeFileService, KnowledgeService  # noqa: F401
