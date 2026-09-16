from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users_accounts.models import User

from .models import KnowledgeFile, KnowledgeItem


class KnowledgeFileAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="knowledge_file_test@example.com",
            password="test-password-123",
        )

        self.other_user = User.objects.create_user(
            email="other_knowledge_file@example.com",
            password="test-password-123",
        )

        self.knowledge = KnowledgeItem.objects.create(
            user=self.user,
            title="Django Learning",
            content="Django architecture",
        )

    def authenticate(self):
        self.client.force_authenticate(
            user=self.user
        )

    def test_upload_file_to_knowledge(self):
        self.authenticate()

        uploaded_file = SimpleUploadedFile(
            "django.txt",
            b"Django architecture notes",
            content_type="text/plain",
        )

        url = reverse(
            "knowledge-item-files",
            kwargs={
                "pk": self.knowledge.id,
            },
        )

        response = self.client.post(
            url,
            {
                "file": uploaded_file,
                "description": "Django notes",
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            KnowledgeFile.objects.count(),
            1,
        )

        knowledge_file = KnowledgeFile.objects.first()

        self.assertEqual(
            knowledge_file.knowledge,
            self.knowledge,
        )

        self.assertEqual(
            knowledge_file.original_name,
            "django.txt",
        )

        self.assertEqual(
            knowledge_file.file_type,
            KnowledgeFile.FileType.TEXT,
        )

        self.assertEqual(
            knowledge_file.mime_type,
            "text/plain",
        )

    def test_list_knowledge_files(self):
        self.authenticate()

        KnowledgeFile.objects.create(
            knowledge=self.knowledge,
            file=SimpleUploadedFile(
                "notes.txt",
                b"notes",
                content_type="text/plain",
            ),
            original_name="notes.txt",
            file_type=KnowledgeFile.FileType.TEXT,
            mime_type="text/plain",
            file_size=5,
        )

        url = reverse(
            "knowledge-item-files",
            kwargs={
                "pk": self.knowledge.id,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_user_cannot_access_other_user_knowledge_files(self):
        other_knowledge = KnowledgeItem.objects.create(
            user=self.other_user,
            title="Other User Knowledge",
        )

        knowledge_file = KnowledgeFile.objects.create(
            knowledge=other_knowledge,
            file=SimpleUploadedFile(
                "private.txt",
                b"private data",
                content_type="text/plain",
            ),
            original_name="private.txt",
            file_type=KnowledgeFile.FileType.TEXT,
            mime_type="text/plain",
            file_size=12,
        )

        self.authenticate()

        url = reverse(
            "knowledge-file-detail",
            kwargs={
                "pk": knowledge_file.id,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_delete_own_knowledge_file(self):
        self.authenticate()

        knowledge_file = KnowledgeFile.objects.create(
            knowledge=self.knowledge,
            file=SimpleUploadedFile(
                "delete.txt",
                b"delete me",
                content_type="text/plain",
            ),
            original_name="delete.txt",
            file_type=KnowledgeFile.FileType.TEXT,
            mime_type="text/plain",
            file_size=9,
        )

        url = reverse(
            "knowledge-file-detail",
            kwargs={
                "pk": knowledge_file.id,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            KnowledgeFile.objects.filter(
                id=knowledge_file.id
            ).exists()
        )
